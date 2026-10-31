"""MJ Lab simulation: ships fly the FPV gravity model over a crowd that hears
them through a research-built perception model and drifts on the floor; the
crowd's groups become the ships' gravity bodies.

    nice -n 19 python3 sim.py            # one default run, prints metrics

Standard library only. Seeded and fixed-step: same config, same numbers.
"""

import math
import random
import json
import sys
from dataclasses import dataclass, field, asdict, replace

from flight import FlightTuning, FlightWorld, Orders, gravity_pulse, rabbit_at, PATROL, ESCORT
from hearing import HearingTuning, Band, dome_point, band_profile
from crowd import CrowdTuning, spawn, Ear, hear, move, social
from mj import MJPolicy, AutoMJ, clusters


@dataclass
class Config:
    seed: int = 1
    bpm: float = 126.0
    bpb: int = 4
    bars: int = 64
    warmBars: int = 8
    ships: int = 4
    dt: float = 1.0 / 64.0          # beats per flight step (the plan's tick is 1/128)
    sampleBeats: float = 0.25       # one perception sample per 1/16 note
    gain3d: float = 1.0
    reach: float = 0.5              # the clip's ElevationParams.reach
    diveBand: object = None         # MJ move: switch to this band while a ship is over a group
    diveRadius: float = 0.3
    bands: list = field(default_factory=lambda: [Band() for _ in range(4)])
    flight: FlightTuning = field(default_factory=FlightTuning)
    hearing: HearingTuning = field(default_factory=HearingTuning)
    crowd: CrowdTuning = field(default_factory=CrowdTuning)
    mj: MJPolicy = field(default_factory=MJPolicy)
    trace: bool = False


def run(cfg: Config):
    rng = random.Random(cfg.seed)
    t = cfg.flight
    world = FlightWorld(cfg.seed, t, cfg.ships)
    for ch in range(cfg.ships):
        x, y, _, _ = rabbit_at(0.0, ch, cfg.bpb, t)
        world.launch(ch, (x, y), 0.0, cfg.bpb)
    ear = Ear(cfg.hearing, cfg.bands, cfg.bpm, cfg.sampleBeats, cfg.gain3d)
    base_prof = list(ear.prof)
    dive_prof = band_profile(cfg.diveBand, cfg.hearing) if cfg.diveBand is not None else None
    people = spawn(rng, cfg.crowd, cfg.hearing, 4, ear.hist_len)
    mjx = AutoMJ(cfg.mj)
    orders = [Orders(flying=(ch < cfg.ships)) for ch in range(4)]
    active = [ch < cfg.ships for ch in range(4)]

    total_beats = cfg.bars * cfg.bpb
    warm_beats = cfg.warmBars * cfg.bpb
    steps_per_sample = max(1, round(cfg.sampleBeats / cfg.dt))
    n_samples = int(total_beats / cfg.sampleBeats)

    ship_trace = []       # per sample: positions of 4 ships
    rabbit_trace = []
    bodies_trace = []     # per bar
    crowd_trace = []      # per bar: positions + fatigue + reward
    group_stats = []      # per bar after warm-up
    orders_trace = []
    body_boredom = {}

    def boredom_of_body(i):
        return body_boredom.get(i, 0.0)

    step_count = 0
    bodies = []
    hold_bar = [False] * 4
    for si in range(n_samples):
        beats = si * cfg.sampleBeats
        bar = int(beats // cfg.bpb)
        if abs(beats - bar * cfg.bpb) < 1e-9:
            bodies = [tuple(b) for b in mjx.update_bar(bar, people, cfg.warmBars)]
            mjx.floor_fatigue = sum(p.F for p in people) / len(people)
            mjx.floor_reward = sum(p.rEMA for p in people) / len(people)
            # boredom per body: mean (1 - reward) of its members, rough
            body_boredom.clear()
            for bi, b in enumerate(bodies):
                near = [p for p in people if (p.x - b[0]) ** 2 + (p.y - b[1]) ** 2 < 0.04]
                if near:
                    body_boredom[bi] = -sum(p.rEMA for p in near) / len(near)
            ords = mjx.orders(bar, cfg.ships, cfg.warmBars, boredom_of_body)
            for ch in range(cfg.ships):
                orders[ch].goal, orders[ch].body = ords[ch]
            hold_bar = [False] * 4
            for ch, (fly, rate, moving) in enumerate(mjx.moves(bar, cfg.ships, cfg.warmBars)):
                hold_bar[ch] = fly == "hold"
                orders[ch].flying = bool(fly) and fly != "hold"
                world.rate[ch] = rate
                active[ch] = moving
            bodies_trace.append([list(b) for b in bodies])
            orders_trace.append([tuple(o) for o in ords])
            crowd_trace.append([(p.x, p.y, p.F, p.rEMA) for p in people])
            if bar >= cfg.warmBars:
                gs = mjx.groups
                n = len(people)
                grouped = sum(len(g) for g in gs if len(g) >= cfg.mj.minGroup)
                group_stats.append(dict(
                    grouped=grouped / n,
                    largest=len(gs[0]) / n if gs else 0.0,
                    groups=sum(1 for g in gs if len(g) >= cfg.mj.minGroup),
                    radius=sum(math.hypot(p.x, p.y) for p in people) / n))
        beat_in_bar = beats - bar * cfg.bpb
        for ch in range(cfg.ships):
            pat = cfg.mj.holdPattern2 if (ch % 2 == 1 and cfg.mj.holdPattern2) else cfg.mj.holdPattern
            if hold_bar[ch] and pat:
                k = int(beat_in_bar)
                orders[ch].flying = not (k in pat and beat_in_bar - k < cfg.mj.holdLen)
            elif hold_bar[ch]:
                if cfg.mj.holdAt == "start":
                    orders[ch].flying = beat_in_bar >= cfg.mj.holdBeats
                else:
                    orders[ch].flying = beat_in_bar < cfg.bpb - cfg.mj.holdBeats
        # flight: fixed steps up to this sample
        for _ in range(steps_per_sample):
            tb = step_count * cfg.dt
            pulse = gravity_pulse(tb, cfg.bpb, t)
            world.step(orders, bodies, tb, cfg.bpb, pulse, cfg.dt)
            step_count += 1
        fx = mjx.effect_position(beats, bar, cfg.warmBars, cfg.bpb)
        e_ch = cfg.ships - 1
        if fx is not None and e_ch >= 0:
            orders[e_ch].flying = False   # the flight waits; the effect owns the ship
            world.p[e_ch] = fx
            if not getattr(world, "_in_effect", False):
                world._in_effect = True
        elif getattr(world, "_in_effect", False) and e_ch >= 0:
            world._in_effect = False
            orders[e_ch].flying = True
            world.launch(e_ch, world.p[e_ch], beats, cfg.bpb)
        ship_trace.append(list(world.p))
        rabbit_trace.append([rabbit_at(beats, ch, cfg.bpb, t, world.phase_offset[ch])[:2]
                             for ch in range(4)])
        S = [dome_point(world.p[ch][0], world.p[ch][1], cfg.reach) for ch in range(4)]
        if cfg.diveBand is not None:
            for ch in range(4):
                px, py = world.p[ch]
                near = any((b[0] - px) ** 2 + (b[1] - py) ** 2 < cfg.diveRadius ** 2 for b in bodies if b[2] > 0)
                ear.prof[ch] = dive_prof if near else base_prof[ch]
        record = beats >= warm_beats
        for L in people:
            r, per = hear(L, S, active, beats, si, ear, record)
            if not cfg.crowd.frozen:
                move(L, world.p, per, r, cfg.crowd, cfg.hearing, rng, cfg.sampleBeats)
        if not cfg.crowd.frozen and si % int(round(1 / cfg.sampleBeats)) == 0:
            social(people, cfg.crowd, cfg.hearing, 1.0)

    res = metrics(cfg, people, ship_trace, rabbit_trace, group_stats, warm_beats)
    if cfg.trace:
        res["trace"] = dict(ships=ship_trace, rabbits=rabbit_trace, bodies=bodies_trace,
                            crowd=crowd_trace, orders=orders_trace,
                            listeners=[dict(x=L.x, y=L.y, **{k: v / max(1, L.acc["n"]) for k, v in L.acc.items()})
                                       for L in people])
    return res


def metrics(cfg, people, ship_trace, rabbit_trace, group_stats, warm_beats):
    sb = cfg.sampleBeats
    w0 = int(warm_beats / sb)
    n_ships = cfg.ships
    lap_samples = int(cfg.flight.orbitLapBars * cfg.bpb / sb)
    lapdev, onpath = [], []
    grid = {}
    for si in range(w0, len(ship_trace)):
        for ch in range(n_ships):
            x, y = ship_trace[si][ch]
            rx, ry = rabbit_trace[si][ch]
            onpath.append(1.0 if math.hypot(x - rx, y - ry) < 0.1 else 0.0)
            if si - lap_samples >= w0:
                ox, oy = ship_trace[si - lap_samples][ch]
                lapdev.append(math.hypot(x - ox, y - oy))
            key = (ch, int((x + 1) * 5), int((y + 1) * 5))
            grid[key] = grid.get(key, 0) + 1
    ent = 0.0
    for ch in range(n_ships):
        cells = [v for (c, _, _), v in grid.items() if c == ch]
        tot = sum(cells)
        e = -sum(v / tot * math.log(v / tot) for v in cells) if tot else 0.0
        ent += e / math.log(100)
    ent /= max(1, n_ships)
    # beat wobble: ship azimuth from the centre minus its 1-beat moving average
    k = int(round(1 / sb))
    wob = []
    for ch in range(n_ships):
        az = [math.atan2(p[ch][1], p[ch][0]) for p in ship_trace[w0:]]
        un = [az[0]]
        for a in az[1:]:
            d = a - un[-1]
            d = (d + math.pi) % (2 * math.pi) - math.pi
            un.append(un[-1] + d)
        for i in range(k, len(un) - k):
            avg = sum(un[i - k:i + k + 1]) / (2 * k + 1)
            wob.append((un[i] - avg) ** 2)
    wobble = math.degrees(math.sqrt(sum(wob) / len(wob))) if wob else 0.0
    # angular speed seen from the centre, deg/s
    spd = []
    sec = sb * 60.0 / cfg.bpm
    for ch in range(n_ships):
        for si in range(w0 + 1, len(ship_trace)):
            a0 = math.atan2(ship_trace[si - 1][ch][1], ship_trace[si - 1][ch][0])
            a1 = math.atan2(ship_trace[si][ch][1], ship_trace[si][ch][0])
            d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
            spd.append(abs(math.degrees(d)) / sec)
    spd.sort()
    # how much the path's turning varies: a circle turns at a constant rate
    hstd, rstd = [], []
    for ch in range(n_ships):
        hd = []
        for si in range(w0 + 2, len(ship_trace), int(round(1 / sb))):
            (x0, y0), (x1, y1), (x2, y2) = ship_trace[si - 2][ch], ship_trace[si - 1][ch], ship_trace[si][ch]
            a = math.atan2(y1 - y0, x1 - x0)
            b = math.atan2(y2 - y1, x2 - x1)
            hd.append(math.degrees((b - a + math.pi) % (2 * math.pi) - math.pi) / sb)
        if hd:
            m = sum(hd) / len(hd)
            hstd.append(math.sqrt(sum((h - m) ** 2 for h in hd) / len(hd)))
        rr = [math.hypot(*p[ch]) for p in ship_trace[w0:]]
        mr = sum(rr) / len(rr)
        rstd.append(math.sqrt(sum((r - mr) ** 2 for r in rr) / len(rr)))
    acc = {key: 0.0 for key in people[0].acc}
    for L in people:
        for key, v in L.acc.items():
            acc[key] += v
    n = max(1.0, acc["n"])
    per = sorted(L.acc["r"] / max(1, L.acc["n"]) for L in people)
    q = max(1, len(per) // 4)
    bottom = sum(per[:q]) / q
    bars_measured = (cfg.bars - cfg.warmBars)
    gs = group_stats or [dict(grouped=0, largest=0, groups=0, radius=0)]
    tail = gs[len(gs) // 2:]
    return dict(
        engagement=acc["r"] / n,
        bottomQuarter=bottom,
        perceived=acc["perceived"] / n,
        clarity=acc["clarity"] / max(1e-9, acc["salient"]),
        fatigue=acc["F"] / n,
        tired=sum(1 for L in people if L.F > 0.5) / len(people),
        blur=acc["blur"] / n,
        vection=acc["vection"] / n,
        attended=acc["att"] / n,
        load=acc["load"] / n,
        boredom=acc["bored"] / max(1.0, acc["active"]),
        eventsPerBar=acc["events"] / len(people) / bars_measured,
        onBeatShare=acc["onbeat"] / max(1.0, acc["events"]),
        grouped=sum(g["grouped"] for g in tail) / len(tail),
        largest=sum(g["largest"] for g in tail) / len(tail),
        groups=sum(g["groups"] for g in tail) / len(tail),
        crowdRadius=sum(g["radius"] for g in tail) / len(tail),
        lapDev=sum(lapdev) / max(1, len(lapdev)),
        onPath=sum(onpath) / max(1, len(onpath)),
        coverage=ent,
        wobbleDeg=wobble,
        turnStd=sum(hstd) / max(1, len(hstd)),
        radiusStd=sum(rstd) / max(1, len(rstd)),
        azSpeedMedian=spd[len(spd) // 2] if spd else 0.0,
        azSpeedP90=spd[int(len(spd) * 0.9)] if spd else 0.0,
    )


if __name__ == "__main__":
    import time
    t0 = time.time()
    r = run(Config())
    print(json.dumps({k: round(v, 4) for k, v in r.items()}, indent=1))
    print("seconds", round(time.time() - t0, 1), file=sys.stderr)
