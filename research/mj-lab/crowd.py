"""The crowd: listener agents who hear the moving bands (hearing.py), get
engaged, bored or tired, and drift on the floor. A MODEL; the behaviour rules
are MJ hypotheses unless a research row is named.
"""

import math
import random
from dataclasses import dataclass

from hearing import (DEG, HearingTuning, Band, band_profile, mama,
                     perceived_direction, az_el, wrap, dome_point)


@dataclass
class CrowdTuning:
    count: int = 72
    walk: float = 0.008          # floor units per beat at full desire (~0.05 m/s at 6 m, 126 BPM)
    explore: float = 0.006       # random walk when unsatisfied
    satisfiedAt: float = 0.30    # reward EMA at which a listener stops exploring
    rewardBeats: float = 8.0
    socialRadius: float = 0.25
    socialPull: float = 0.003
    personalSpace: float = 0.06
    crowdedAt: int = 3           # only the lonely look for company
    start: str = "clumps"        # clumps | uniform | front | grid
    frozen: bool = False         # listeners do not move (perception maps)


class Listener:
    __slots__ = ("x", "y", "F", "rEMA", "eventRate", "heading", "hist",
                 "u_exp", "surprise", "last_event", "acc")

    def __init__(self, x, y, heading, n_ships, hist_len):
        self.x, self.y = x, y
        self.F = 0.0
        self.rEMA = 0.0
        self.eventRate = 0.0
        self.heading = heading
        # ring buffers of perceived directions per ship
        self.hist = [[None] * hist_len for _ in range(n_ships)]
        self.u_exp = [(0.0, 0.0)] * n_ships
        self.surprise = [0.0] * n_ships
        self.last_event = [-99.0] * n_ships
        # accumulators for metrics
        self.acc = dict(r=0.0, perceived=0, clarity=0.0, salient=0.0, F=0.0,
                        bored=0, active=0, events=0, onbeat=0, blur=0.0, n=0,
                        vection=0.0, att=0.0, load=0.0)


def spawn(rng, ct: CrowdTuning, h: HearingTuning, n_ships, hist_len):
    people = []
    edge = h.floorEdge
    centres = [(rng.uniform(-0.5, 0.5), rng.uniform(-0.4, 0.6)) for _ in range(3)]
    if ct.start == "grid":
        k = 0.85 / 4
        for gx in range(-4, 5):
            for gy in range(-4, 5):
                x, y = gx * k, gy * k
                if math.hypot(x, y) <= edge + 1e-9:
                    people.append(Listener(x, y, 0.0, n_ships, hist_len))
        return people
    for i in range(ct.count):
        if ct.start == "uniform" or (ct.start == "clumps" and i % 3 == 0):
            r = edge * math.sqrt(rng.random())
            a = rng.random() * 2 * math.pi
            x, y = r * math.cos(a), r * math.sin(a)
        elif ct.start == "front":
            x, y = rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.75)
        else:
            cx, cy = centres[i % 3]
            x, y = cx + rng.gauss(0, 0.08), cy + rng.gauss(0, 0.08)
        r = math.hypot(x, y)
        if r > edge:
            x, y = x * edge / r, y * edge / r
        people.append(Listener(x, y, rng.random() * 2 * math.pi, n_ships, hist_len))
    return people


class Ear:
    """Per-run constants for the hearing model."""

    def __init__(self, h: HearingTuning, bands, bpm, sample_beats, gain3d=1.0):
        self.h = h
        self.prof = [band_profile(b, h) for b in bands]
        self.bpm = bpm
        self.sample_beats = sample_beats
        sec_per_beat = 60.0 / bpm
        self.k_short = max(1, round(h.windowShortS / sec_per_beat / sample_beats))
        self.k_long = max(self.k_short + 1, round(h.windowLongS / sec_per_beat / sample_beats))
        self.w_short = self.k_short * sample_beats * sec_per_beat
        self.w_long = self.k_long * sample_beats * sec_per_beat
        self.hist_len = self.k_long + 1
        self.gain3d = gain3d


def hear(L: Listener, ships_S, active, beats, idx, ear: Ear, record: bool):
    """One perception sample for one listener. ships_S: dome point per ship.
    Returns per-ship (interest, blur, salience, floor direction weight)."""
    h = ear.h
    qx, qy = L.x, L.y
    r_q = math.hypot(qx, qy)
    if h.facing == "random":
        face = L.heading                   # whichever way they are drifting
    else:
        tx, ty = (0.0, 0.95) if h.facing == "dj" else (0.0, 0.0)
        fx, fy = tx - qx, ty - qy          # facing the DJ booth (or the centre)
        fl = math.hypot(fx, fy)
        face = math.atan2(fy, fx) if fl > 1e-6 else math.pi / 2
    off = 1.0 + h.offCentreBlur * (r_q / h.sweetRadius) ** 2
    hl = ear.hist_len
    frac = beats - math.floor(beats)
    on_beat = frac < h.onBeatWindow or frac > 1 - h.onBeatWindow
    dtb = ear.sample_beats
    out = []
    interests, load, vec_sum, blur_sum = [], 0.0, 0.0, 0.0
    any_detected = False
    max_s, max_sur = 0.0, 0.0
    clar_acc = 0.0
    events_now = 0
    onbeat_now = 0
    for i, S in enumerate(ships_S):
        if not active[i]:
            out.append((0.0, 0.0, 0.0))
            continue
        prof = ear.prof[i]
        dx, dy, dz, dist = perceived_direction(qx, qy, S, h, r_q)
        now = az_el((dx, dy, dz))
        buf = L.hist[i]
        buf[idx % hl] = now
        old_s = buf[(idx - ear.k_short) % hl]
        old_l = buf[(idx - ear.k_long) % hl]
        if old_s is None or old_l is None:
            out.append((0.0, 0.0, 0.0))
            continue
        cos_el = math.cos(now[1])
        daz_s = wrap(now[0] - old_s[0]) * cos_el * DEG
        del_s = (now[1] - old_s[1]) * DEG
        daz_l = wrap(now[0] - old_l[0]) * cos_el * DEG
        del_l = (now[1] - old_l[1]) * DEG
        alpha = wrap(now[0] - face)
        side = 1.0 + h.kSide * math.sin(alpha) ** 2
        base = side * prof["m_band"] * off * h.mamaScale
        ev = prof["elev"] / h.verticalPenalty
        tot_s = math.hypot(daz_s, del_s)
        tot_l = math.hypot(daz_l, del_l)
        eff_s = math.hypot(daz_s, del_s * ev)
        eff_l = math.hypot(daz_l, del_l * ev)
        thr_s = mama(tot_s / ear.w_short, h) * base
        thr_l = mama(tot_l / ear.w_long, h) * base
        z = max(eff_s / thr_s, eff_l / thr_l)
        prox = min(h.proxMax, max(0.5, 1.0 / dist))
        gate = min(1.0, prof["energy"] * prox * ear.gain3d / h.levelRef)
        s = min(1.0, max(0.0, (z - 1.0) / h.zSat)) * gate
        rot = abs(daz_s) / ear.w_short / 360.0
        c_ul = 1.0 / (1.0 + (rot / prof["ul"]) ** 4)
        c = c_ul * prof["clarity_fb"]
        blur = s * (1.0 - c_ul)
        # expectation and events (Locke 2016: ~1 s velocity window)
        ux, uy = daz_l / ear.w_long, del_l / ear.w_long
        ex, ey = L.u_exp[i]
        event = False
        if z > 1.0 and beats - L.last_event[i] >= 1.0:
            mu, me = math.hypot(ux, uy), math.hypot(ex, ey)
            if me < 3.0 and mu > 3.0:
                event = True
            elif me >= 3.0 and mu >= 3.0:
                cosang = (ux * ex + uy * ey) / (mu * me)
                if cosang < math.cos(h.turnEventDeg / DEG):
                    event = True
                elif mu / me > h.speedUpRatio or me / mu > h.slowDownRatio:
                    event = True
        a = dtb / h.expectationBeats
        L.u_exp[i] = (ex + a * (ux - ex), ey + a * (uy - ey))
        if event:
            L.last_event[i] = beats
            L.surprise[i] = 1.0 if on_beat else h.offBeatEventValue
            events_now += 1
            onbeat_now += 1 if on_beat else 0
        else:
            L.surprise[i] *= math.exp(-dtb / h.surpriseDecayBeats)
        nov = h.novelFloor + (1 - h.novelFloor) * L.surprise[i]
        I = s * c * nov
        interests.append(I)
        load += s
        blur_sum += blur
        vec_sum += s * daz_s / ear.w_short
        if z > 1.0:
            any_detected = True
        clar_acc += s * c
        max_s = max(max_s, s)
        max_sur = max(max_sur, L.surprise[i])
        out.append((I, blur, s))
    interests.sort(reverse=True)
    attended = sum(w * v for w, v in zip(h.attention, interests))
    vection = min(1.0, max(0.0, (abs(vec_sum) - h.vectionOnsetDegS) / h.vectionRangeDegS))
    L.eventRate += (events_now / dtb - L.eventRate) * dtb / 4.0
    over = max(0.0, L.eventRate - h.eventComfortPerBeat)
    dF = (h.kLoad * max(0.0, load - h.loadComfort) + h.kVection * vection
          + h.kBlur * blur_sum + h.kOverload * over - L.F / h.recoveryBeats)
    L.F = min(1.0, max(0.0, L.F + dF * dtb))
    r = attended * (1 - L.F) - h.blurPenalty * blur_sum - h.fatiguePenalty * L.F
    if record:
        A = L.acc
        A["r"] += r
        A["perceived"] += 1 if any_detected else 0
        A["salient"] += load
        A["clarity"] += clar_acc
        A["F"] += L.F
        A["blur"] += blur_sum
        A["vection"] += vection
        A["att"] += attended
        A["load"] += load
        if max_s > 0.2:
            A["active"] += 1
            if max_sur < 0.2:
                A["bored"] += 1
        A["events"] += events_now
        A["onbeat"] += onbeat_now
        A["n"] += 1
    return r, out


def move(L: Listener, ship_floor, per_ship, r, ct: CrowdTuning, h: HearingTuning,
         rng: random.Random, dtb):
    """Approach where motion is salient and pleasant, back off where it blurs
    or tires; explore when unsatisfied. MJ hypothesis throughout."""
    L.rEMA += (r - L.rEMA) * dtb / ct.rewardBeats
    dx = dy = 0.0
    for (px, py), (I, blur, s) in zip(ship_floor, per_ship):
        if s <= 0.0:
            continue
        a = I * (1 - L.F) - h.blurPenalty * blur - (L.F * s if L.F > 0.4 else 0.0)
        vx, vy = px - L.x, py - L.y
        d = math.hypot(vx, vy)
        if d < 0.05:
            continue
        dx += a * vx / d
        dy += a * vy / d
    m = math.hypot(dx, dy)
    if m > 1.0:
        dx, dy = dx / m, dy / m
    sat = min(1.0, max(0.0, L.rEMA / ct.satisfiedAt))
    L.heading += rng.gauss(0, 0.6) * math.sqrt(dtb)
    e = ct.explore * (1 - sat)
    L.x += (ct.walk * dx + e * math.cos(L.heading)) * dtb
    L.y += (ct.walk * dy + e * math.sin(L.heading)) * dtb
    _keep_on_floor(L, h)


def social(people, ct: CrowdTuning, h: HearingTuning, dtb):
    """Weak pull towards nearby people, a push inside personal space."""
    pos = [(p.x, p.y) for p in people]
    R2 = ct.socialRadius ** 2
    P2 = ct.personalSpace ** 2
    for i, L in enumerate(people):
        cx = cy = 0.0
        n = 0
        px_ = py_ = 0.0
        for j, (x, y) in enumerate(pos):
            if i == j:
                continue
            ddx, ddy = x - pos[i][0], y - pos[i][1]
            d2 = ddx * ddx + ddy * ddy
            if d2 < R2:
                cx += ddx
                cy += ddy
                n += 1
                if d2 < P2 and d2 > 1e-12:
                    d = math.sqrt(d2)
                    px_ -= ddx / d * (ct.personalSpace - d)
                    py_ -= ddy / d * (ct.personalSpace - d)
        if 0 < n < ct.crowdedAt:
            L.x += ct.socialPull * cx / n * dtb / ct.socialRadius
            L.y += ct.socialPull * cy / n * dtb / ct.socialRadius
        L.x += 0.5 * px_ * dtb
        L.y += 0.5 * py_ * dtb
        _keep_on_floor(L, h)


def _keep_on_floor(L, h):
    r = math.hypot(L.x, L.y)
    if r > h.floorEdge:
        L.x, L.y = L.x * h.floorEdge / r, L.y * h.floorEdge / r
