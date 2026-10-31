"""Port of the FPV phase-2 gravity flight (fpv-phase-2-plan.md, Tasks 1-7).

Faithful to the plan and to the C++ already written in
a3-motion-ui feat/fpv-gravity (FlightTuning, gravityAt, gravityPulse,
rabbitAt). ShipDynamics / FlightWorld were not written yet when this was
ported, so stepShip, wander, separation and escort follow the plan's text.

Time is in beats, lengths in floor units (room edge = radius 1).
Fixed step, seeded randomness only.
"""

import math
import random
from dataclasses import dataclass, field, replace

TWO_PI = 2.0 * math.pi
MAX_BODIES = 8


@dataclass
class FlightTuning:
    gravity: float = 0.02
    softening: float = 0.08
    gravityMax: float = 1.5
    orbitRadius: float = 0.7
    orbitEccentricity: float = 0.2
    orbitLapBars: float = 4.0
    orbitPrecessionBars: float = 32.0
    steerStiffness: float = 0.6
    steerDamping: float = 0.8
    steerMax: float = 0.3
    damping: float = 0.05
    speedMin: float = 0.08
    speedMax: float = 0.9
    rimSoft: float = 0.9
    rimStiffness: float = 4.0
    captureRadius: float = 0.15
    captureLapBars: float = 2.0
    separation: float = 0.004
    wanderRadius: float = 0.12
    pulseDepth: float = 0.3
    pulseDownbeatDepth: float = 0.6
    # Lab extension (not in the plan): which beats get a pulse.
    # "beat" = the plan (every beat, the one harder); "bar" = only the one;
    # "half" = beats 1 and 3; "off" = constant 1.
    pulseMode: str = "beat"
    # Lab extension: a velocity kick on the one (an audible beat link, B5/B6).
    # Every kickEveryBars bars (staggered per ship), the ship gets kickSpeed
    # floor units per beat towards the heaviest body, or across the room.
    kickEveryBars: int = 0
    kickSpeed: float = 0.4


# ---------- small vector helpers (tuples are fast enough and immutable) ----------

def vlen(x, y):
    return math.hypot(x, y)


def clamp_length(x, y, m):
    l = math.hypot(x, y)
    if l <= m or l <= 0.0:
        return x, y
    k = m / l
    return x * k, y * k


# ---------- Task 1: gravity ----------

def gravity_at(px, py, bodies, pulse, t: FlightTuning):
    eps2 = t.softening * t.softening
    sx = sy = 0.0
    for (bx, by, m) in bodies[:MAX_BODIES]:
        dx, dy = bx - px, by - py
        r2 = dx * dx + dy * dy + eps2
        k = m / (r2 * math.sqrt(r2))
        sx += dx * k
        sy += dy * k
    g = pulse * t.gravity
    return clamp_length(sx * g, sy * g, t.gravityMax)


# ---------- Task 2: the beat pulse ----------

def gravity_pulse(beats, beats_per_bar, t: FlightTuning):
    if t.pulseMode == "off":
        return 1.0
    if t.pulseMode == "gate":   # lab extension: gravity acts only during beat 1 of each bar
        return 1.0 if int(math.floor(beats)) % beats_per_bar == 0 else 0.0
    beat_in_bar = int(math.floor(beats)) % beats_per_bar
    frac = beats - math.floor(beats)
    if t.pulseMode == "beat":
        depth = t.pulseDownbeatDepth if beat_in_bar == 0 else t.pulseDepth
    elif t.pulseMode == "bar":
        if beat_in_bar != 0:
            return 1.0
        depth = t.pulseDownbeatDepth
    elif t.pulseMode == "half":
        if beat_in_bar == 0:
            depth = t.pulseDownbeatDepth
        elif beat_in_bar == beats_per_bar // 2:
            depth = t.pulseDepth
        else:
            return 1.0
    else:
        raise ValueError(t.pulseMode)
    s = 1.0 - frac
    return 1.0 + depth * s * s


# ---------- Task 3: the big path ----------

def _ellipse(beats, bpb, t):
    prec = t.orbitPrecessionBars * bpb
    turn = TWO_PI * (beats / prec - math.floor(beats / prec))
    return (t.orbitRadius * (1 + t.orbitEccentricity),
            t.orbitRadius * (1 - t.orbitEccentricity), turn)


def _rot(x, y, a):
    c, s = math.cos(a), math.sin(a)
    return c * x - s * y, s * x + c * y


def rabbit_at(beats, channel, bpb, t: FlightTuning, phase_offset=0.0):
    lap = t.orbitLapBars * bpb
    ph = beats / lap - 0.25 * channel + phase_offset
    return rabbit_from_phase(ph, 1.0 / lap, beats, bpb, t)


def rabbit_from_phase(ph, laps_per_beat, beats, bpb, t: FlightTuning):
    """Lab extension: the rabbit at an explicit lap phase moving at an explicit
    (signed) rate, so the MJ can double, halve or reverse a ship on a bar line.
    With ph = beats/lap - channel/4 + offset this is exactly rabbit_at."""
    A, B, turn = _ellipse(beats, bpb, t)
    ph -= math.floor(ph)
    th = TWO_PI * ph
    lx, ly = A * math.cos(th), B * math.sin(th)
    th_rate = TWO_PI * laps_per_beat
    turn_rate = TWO_PI / (t.orbitPrecessionBars * bpb)
    ax, ay = -A * math.sin(th) * th_rate, B * math.cos(th) * th_rate
    wx, wy = -ly * turn_rate, lx * turn_rate
    px, py = _rot(lx, ly, turn)
    vx, vy = _rot(ax + wx, ay + wy, turn)
    return px, py, vx, vy


def nearest_orbit_phase(px, py, beats, bpb, t: FlightTuning):
    A, B, turn = _ellipse(beats, bpb, t)
    qx, qy = _rot(px, py, -turn)
    best, bd = 0.0, float("inf")
    for i in range(64):
        th = TWO_PI * i / 64
        d = math.hypot(A * math.cos(th) - qx, B * math.sin(th) - qy)
        if d < bd:
            bd, best = d, th
    lo, hi = best - TWO_PI / 64, best + TWO_PI / 64
    for _ in range(8):
        mid = 0.5 * (lo + hi)
        tx, ty = A * math.cos(mid) - qx, B * math.sin(mid) - qy
        slope = tx * (-A * math.sin(mid)) + ty * (B * math.cos(mid))
        if slope < 0:
            lo = mid
        else:
            hi = mid
    ph = 0.5 * (lo + hi) / TWO_PI
    return ph - math.floor(ph)


def orbit_guide_points(beats, bpb, count, t):
    A, B, turn = _ellipse(beats, bpb, t)
    return [_rot(A * math.cos(TWO_PI * i / (count - 1)),
                 B * math.sin(TWO_PI * i / (count - 1)), turn) for i in range(count)]


# ---------- Task 4: one ship's step ----------

def step_ship(p, v, goal, grav, sep, dt, t: FlightTuning):
    """Semi-implicit Euler. p, v: (x, y). goal: (gx, gy, gvx, gvy)."""
    px, py = p
    vx, vy = v
    gx, gy, gvx, gvy = goal
    sx = t.steerStiffness * (gx - px) + t.steerDamping * (gvx - vx)
    sy = t.steerStiffness * (gy - py) + t.steerDamping * (gvy - vy)
    sx, sy = clamp_length(sx, sy, t.steerMax)
    ax = sx + grav[0] + sep[0] - t.damping * vx
    ay = sy + grav[1] + sep[1] - t.damping * vy
    r = math.hypot(px, py)
    if r > t.rimSoft:
        k = -t.rimStiffness * (r - t.rimSoft) / r
        ax += k * px
        ay += k * py
    vx += ax * dt
    vy += ay * dt
    sp = math.hypot(vx, vy)
    if sp > t.speedMax:
        vx, vy = vx * t.speedMax / sp, vy * t.speedMax / sp
    elif sp < t.speedMin:
        if sp > 1e-9:
            vx, vy = vx * t.speedMin / sp, vy * t.speedMin / sp
        else:
            dx, dy = gx - px, gy - py
            dl = math.hypot(dx, dy)
            if dl < 1e-9:
                dx, dy, dl = 1.0, 0.0, 1.0
            vx, vy = dx / dl * t.speedMin, dy / dl * t.speedMin
    px += vx * dt
    py += vy * dt
    r = math.hypot(px, py)
    if r > 1.0:
        px, py = px / r, py / r
        # the wall eats the outward part of the velocity
        nx, ny = px, py
        out = vx * nx + vy * ny
        if out > 0:
            vx, vy = vx - out * nx, vy - out * ny
    return (px, py), (vx, vy)


# ---------- Tasks 6-7: four ships, wander, separation, escort ----------

PATROL, ESCORT = 0, 1


@dataclass
class Orders:
    flying: bool = True
    goal: int = PATROL
    body: int = -1


class FlightWorld:
    def __init__(self, seed, tuning: FlightTuning, n_ships=4):
        self.t = tuning
        self.n = n_ships
        self.p = [(0.0, 0.0)] * 4
        self.v = [(0.0, 0.0)] * 4
        self.phase_offset = [0.0] * 4
        self.wander = [(0.0, 0.0)] * 4
        self.dice = [random.Random(seed * 1000 + ch) for ch in range(4)]
        self.last_bar = -1
        self.escort_sense = [0.0] * 4  # +1 ccw, -1 cw, 0 not decided
        self.escort_body = [-1] * 4
        # lab extension: integrated lap phase, signed rate multiplier per ship
        self.phase = [None] * 4
        self.rate = [1.0] * 4

    def launch(self, ch, p, beats, bpb):
        t = self.t
        ph = nearest_orbit_phase(p[0], p[1], beats, bpb, t)
        lap = t.orbitLapBars * bpb
        natural = beats / lap - 0.25 * ch
        self.phase_offset[ch] = ph - (natural - math.floor(natural))
        _, _, vx, vy = rabbit_at(beats, ch, bpb, t, self.phase_offset[ch])
        sp = math.hypot(vx, vy)
        cruise = min(max(sp, t.speedMin), t.speedMax)
        if sp > 1e-9:
            vx, vy = vx / sp * cruise, vy / sp * cruise
        self.p[ch] = p
        self.v[ch] = (vx, vy)

    def goal_for(self, ch, order, bodies, beats, bpb):
        t = self.t
        if order.goal == ESCORT and 0 <= order.body < len(bodies) and bodies[order.body][2] > 0:
            bx, by, m = bodies[order.body]
            if self.escort_body[ch] != order.body:
                self.escort_body[ch] = order.body
                px, py = self.p[ch]
                vx, vy = self.v[ch]
                cross = (px - bx) * vy - (py - by) * vx
                self.escort_sense[ch] = 1.0 if cross >= 0 else -1.0
            sense = self.escort_sense[ch]
            rad = t.captureRadius * math.sqrt(abs(m))
            px, py = self.p[ch]
            # circle phase follows the bar clock, entered from the ship's side
            omega = sense * TWO_PI / (t.captureLapBars * bpb)
            ang0 = math.atan2(py - by, px - bx)
            # goal leads the ship by a quarter of a beat along the circle
            ang = ang0 + omega * 0.25
            gx, gy = bx + rad * math.cos(ang), by + rad * math.sin(ang)
            gvx, gvy = -math.sin(ang) * rad * omega, math.cos(ang) * rad * omega
            return gx, gy, gvx, gvy
        self.escort_body[ch] = -1
        return self.rabbit(ch, beats, bpb)

    def rabbit(self, ch, beats, bpb):
        t = self.t
        lap = t.orbitLapBars * bpb
        if self.phase[ch] is None:
            self.phase[ch] = beats / lap - 0.25 * ch + self.phase_offset[ch]
        return rabbit_from_phase(self.phase[ch], self.rate[ch] / lap, beats, bpb, t)

    def advance_phases(self, dt, bpb, orders):
        lap = self.t.orbitLapBars * bpb
        for ch in range(self.n):
            if self.phase[ch] is not None:  # the rabbit runs on through a hold
                self.phase[ch] += self.rate[ch] * dt / lap

    def _kicked(self, ch, bodies):
        t = self.t
        px, py = self.p[ch]
        vx, vy = self.v[ch]
        pos = [b for b in bodies if b[2] > 0]
        if pos:
            bx, by, _ = max(pos, key=lambda b: b[2] / ((b[0] - px) ** 2 + (b[1] - py) ** 2 + 0.01))
            dx, dy = bx - px, by - py
        else:
            dx, dy = -px, -py      # across the room
        d = math.hypot(dx, dy)
        if d < 1e-6:
            return vx, vy
        return vx + t.kickSpeed * dx / d, vy + t.kickSpeed * dy / d

    def step(self, orders, bodies, beats, bpb, pulse, dt):
        t = self.t
        bar = int(math.floor(beats / bpb))
        if bar != self.last_bar:
            self.last_bar = bar
            for ch in range(4):
                d = self.dice[ch]
                a = d.random() * TWO_PI
                r = t.wanderRadius * math.sqrt(d.random())
                self.wander[ch] = (r * math.cos(a), r * math.sin(a))
        kick_now = False
        if t.kickEveryBars > 0 and bar != getattr(self, "_kick_bar", -1):
            self._kick_bar = bar
            kick_now = True
        eps2 = t.softening * t.softening
        new_p, new_v = list(self.p), list(self.v)
        for ch in range(self.n):
            o = orders[ch]
            if not o.flying:
                continue
            gx, gy, gvx, gvy = self.goal_for(ch, o, bodies, beats, bpb)
            if o.goal == PATROL or self.escort_body[ch] < 0:
                gx += self.wander[ch][0]
                gy += self.wander[ch][1]
            px, py = self.p[ch]
            sx = sy = 0.0
            for other in range(self.n):
                if other == ch or not orders[other].flying:
                    continue
                qx, qy = self.p[other]
                dx, dy = px - qx, py - qy
                k = t.separation / (dx * dx + dy * dy + eps2)
                sx += dx * k
                sy += dy * k
            if kick_now and (bar + ch) % t.kickEveryBars == 0:
                self.v[ch] = self._kicked(ch, bodies)
            grav = gravity_at(px, py, bodies, pulse, t)
            new_p[ch], new_v[ch] = step_ship(self.p[ch], self.v[ch],
                                             (gx, gy, gvx, gvy), grav, (sx, sy), dt, t)
        self.p, self.v = new_p, new_v
        self.advance_phases(dt, bpb, orders)
