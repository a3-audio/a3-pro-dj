"""The automatic MJ: turns the crowd into gravity bodies (the closed loop) and
decides which ship escorts whom. Rules are the playbook's, tagged there."""

import math
from dataclasses import dataclass


@dataclass
class MJPolicy:
    bodies: str = "loop"        # none | static | loop
    linkRadius: float = 0.12    # single-linkage radius for "a group" (~0.7 m at 6 m)
    minGroup: int = 4
    massScale: float = 1.0
    deadZones: bool = False     # a tired group becomes a dead zone (X, -2)
    tiredAt: float = 0.45
    follow: float = 0.5         # body follows its group's centroid, per bar
    escort: str = "none"        # none | rotate
    escortShips: int = 1        # how many ships take escort turns
    escortPick: str = "bored"   # bored | largest | smallest
    escortBars: int = 8
    patrolBars: int = 8
    # lab moves (MJ hypotheses, playbook rules 5, 13, 17)
    hold: int = 0               # >0: every `hold` bars the ship stands still for its last bar
    holdBeats: int = 4          # how many beats at the end of that bar it stands still
    holdStagger: int = 2        # bars between ships' holds (2 = together for a 2-bar period)
    holdAt: str = "end"         # end: stop on the last beats, restart on the one; start: stop on the one
    holdPattern: tuple = ()     # beats (0-based) of a hold bar on which the ship stands still, overrides holdBeats
    holdLen: float = 1.0        # how long each pattern stop lasts, in beats
    holdPattern2: tuple = ()    # if set, odd ships use this pattern (call and response)
    speedEvery: int = 8         # the speed move comes every `speedEvery` bars ...
    speedBars: int = 2          # ... for this many bars, from the middle of the period
    fixedBodies: tuple = ()     # DJ-placed bodies ((x, y, mass), ...) instead of the crowd's
    speedMove: float = 1.0      # rate multiplier for 2 bars in every 8 (2 = double, 0.5 = halve)
    counter: bool = False       # even ships fly the path the other way round
    moveShips: int = 4          # how many ships take part in hold / speed moves
    # a set programme: ((bars, {ships, rate, hold, speedMove}), ...) repeated;
    # empty = constant policy. MJ hypothesis: vary the policy with the music.
    program: tuple = ()
    # a DJ-effect throw on the last ship (playbook section 6), every effectEvery bars
    # for effectBars bars: pingpong = jump/glide between two opposite points every
    # effectBeats beats (glide = share of that time spent gliding); swirl = a fast
    # circle, one lap per effectBeats beats.
    # closed-loop MJ: when the floor's mean fatigue passes `calmAbove`, holds and
    # speed moves pause until it falls below `calmBelow` (hysteresis)
    adaptive: bool = False
    calmAbove: float = 0.12
    calmBelow: float = 0.06
    # learning MJ: every `banditBlock` bars it chooses moves on/off, scores the
    # floor's mean reward over the second half of the block, keeps the better arm
    # and still explores with probability `explore`. MJ hypothesis.
    bandit: bool = False
    banditBlock: int = 8
    explore: float = 0.25
    effect: str = "none"
    effectEvery: int = 16
    effectBars: int = 2
    effectBeats: float = 1.0
    effectGlide: float = 0.0


def clusters(people, link):
    n = len(people)
    seen = [False] * n
    out = []
    L2 = link * link
    for i in range(n):
        if seen[i]:
            continue
        seen[i] = True
        stack, members = [i], []
        while stack:
            k = stack.pop()
            members.append(k)
            xk, yk = people[k].x, people[k].y
            for j in range(n):
                if not seen[j]:
                    dx, dy = people[j].x - xk, people[j].y - yk
                    if dx * dx + dy * dy < L2:
                        seen[j] = True
                        stack.append(j)
        out.append(members)
    out.sort(key=len, reverse=True)
    return out


def mass_for(size, policy):
    if size < policy.minGroup:
        return 0.0
    if size < 8:
        m = 1.0
    elif size < 15:
        m = 2.0
    else:
        m = 3.0
    return m * policy.massScale


class AutoMJ:
    def __init__(self, policy: MJPolicy):
        self.p = policy
        self.bodies = []            # list of [x, y, mass]
        self.placed = False
        self.escort_target = [-1] * 4
        self.groups = []
        self.calm = False
        self.floor_fatigue = 0.0
        self.floor_reward = 0.0
        self.arm = 1
        self.arm_value = [None, None]
        self.block_scores = []
        import random as _r
        self.rng = _r.Random(12345)

    def update_bar(self, bar, people, warm_bars):
        """Called once per bar. Returns the bodies list for the flight."""
        p = self.p
        self.groups = clusters(people, p.linkRadius)
        if p.bodies == "none" or bar < warm_bars:
            self.bodies = []
            return self.bodies
        if p.fixedBodies:
            self.bodies = [list(b) for b in p.fixedBodies]
            return self.bodies
        if p.bodies == "static" and self.placed:
            return self.bodies
        new = []
        for members in self.groups:
            m = mass_for(len(members), p)
            if m == 0.0:
                break
            cx = sum(people[k].x for k in members) / len(members)
            cy = sum(people[k].y for k in members) / len(members)
            if p.deadZones:
                fat = sum(people[k].F for k in members) / len(members)
                if fat > p.tiredAt:
                    m = -2.0 * p.massScale
            new.append([cx, cy, m])
            if len(new) == 8:
                break
        # keep identity: each new body follows the nearest old one smoothly
        if self.bodies and p.bodies == "loop":
            for b in new:
                best = min(self.bodies, key=lambda o: (o[0] - b[0]) ** 2 + (o[1] - b[1]) ** 2)
                if (best[0] - b[0]) ** 2 + (best[1] - b[1]) ** 2 < 0.04:
                    b[0] = best[0] + p.follow * (b[0] - best[0])
                    b[1] = best[1] + p.follow * (b[1] - best[1])
        self.bodies = new
        self.placed = True
        return self.bodies

    def moves(self, bar, n_ships, warm_bars):
        """Per ship (flying, rate) for this bar: holds, speed moves, direction.
        Ships are staggered so they do not all move at once."""
        p = self.p
        hold, speed, ships, base_rate = p.hold, p.speedMove, n_ships, 1.0
        if p.bandit and bar >= warm_bars:
            k = (bar - warm_bars) % p.banditBlock
            if k >= p.banditBlock // 2:
                self.block_scores.append(self.floor_reward)
            if k == 0 and bar > warm_bars:
                if self.block_scores:
                    sc = sum(self.block_scores) / len(self.block_scores)
                    v = self.arm_value[self.arm]
                    self.arm_value[self.arm] = sc if v is None else 0.5 * v + 0.5 * sc
                self.block_scores = []
                if self.arm_value[0] is None:
                    self.arm = 0
                elif self.arm_value[1] is None:
                    self.arm = 1
                elif self.rng.random() < p.explore:
                    self.arm = 1 - self.arm
                else:
                    self.arm = 0 if self.arm_value[0] > self.arm_value[1] else 1
            if self.arm == 0:
                hold, speed = 0, 1.0
        if p.adaptive:
            if self.calm and self.floor_fatigue < p.calmBelow:
                self.calm = False
            elif not self.calm and self.floor_fatigue > p.calmAbove:
                self.calm = True
            if self.calm:
                hold, speed = 0, 1.0
        if p.program and bar >= warm_bars:
            total = sum(b for b, _ in p.program)
            k = (bar - warm_bars) % total
            for b, seg in p.program:
                if k < b:
                    hold = seg.get("hold", hold)
                    speed = seg.get("speedMove", speed)
                    ships = min(n_ships, seg.get("ships", ships))
                    base_rate = seg.get("rate", base_rate)
                    break
                k -= b
        res = []
        for ch in range(4):
            flying, rate, moving = ch < ships, base_rate, ch < ships
            if p.counter and ch % 2 == 1:
                rate = -rate
            if bar >= warm_bars and ch < p.moveShips:
                b = bar - warm_bars + p.holdStagger * ch
                if hold and b % hold == hold - 1:
                    flying = "hold"
                half = p.speedEvery // 2
                if speed != 1.0 and half <= b % p.speedEvery < half + p.speedBars:
                    rate *= speed
            res.append((flying, rate, moving))
        return res

    def effect_position(self, beats, bar, warm_bars, bpb):
        """Where the effect puts the last ship now, or None."""
        p = self.p
        if p.effect == "none" or bar < warm_bars:
            return None
        k = (bar - warm_bars) % p.effectEvery
        if k < p.effectEvery - p.effectBars:
            return None
        t0 = (bar - warm_bars - k + p.effectEvery - p.effectBars) * bpb + warm_bars * bpb
        u = (beats - t0) / p.effectBeats
        if p.effect == "swirl":
            a = 2 * math.pi * u
            return 0.7 * math.cos(a), 0.7 * math.sin(a)
        n, f = int(math.floor(u)), u - math.floor(u)
        side = 1.0 if n % 2 == 0 else -1.0
        x = 0.8 * side
        g = p.effectGlide
        if g > 0 and f > 1 - g:
            w = (f - (1 - g)) / g
            x = 0.8 * side * (1 - 2 * w)
        return x, 0.0

    def orders(self, bar, n_ships, warm_bars, boredom_of_body):
        """Escort rotation: ship k escorts the most bored attracting group for
        escortBars, then patrols patrolBars. Returns per ship (goal, body)."""
        p = self.p
        res = [(0, -1)] * 4
        if p.escort == "none" or not self.bodies or bar < warm_bars:
            return res
        cycle = p.escortBars + p.patrolBars
        for k in range(min(p.escortShips, n_ships)):
            phase = (bar - warm_bars + k * (cycle // max(1, p.escortShips))) % cycle
            if phase < p.escortBars:
                if phase == 0 or self.escort_target[k] < 0 or self.escort_target[k] >= len(self.bodies):
                    cands = [i for i, b in enumerate(self.bodies) if b[2] > 0
                             and i not in self.escort_target[:k]]
                    if cands:
                        if p.escortPick == "largest":
                            pick = max(cands, key=lambda i: self.bodies[i][2])
                        elif p.escortPick == "smallest":
                            pick = min(cands, key=lambda i: self.bodies[i][2])
                        else:
                            pick = max(cands, key=lambda i: boredom_of_body(i))
                        self.escort_target[k] = pick
                    else:
                        self.escort_target[k] = -1
                res[k] = (1, self.escort_target[k])
            else:
                self.escort_target[k] = -1
        return res
