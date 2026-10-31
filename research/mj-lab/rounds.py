"""The experiment rounds. Each round is a dict of conditions; run with
    nice -n 19 python3 go.py <round> [<round> ...]"""
import sys
from dataclasses import replace
from sim import Config
from flight import FlightTuning
from hearing import HearingTuning, Band
from crowd import CrowdTuning
from mj import MJPolicy
from lab import sweep, summary


def base(seed, ships=2, flight=None, mj=None, band=None, hearing=None, crowd=None, **kw):
    return Config(seed=seed, ships=ships,
                  flight=flight or FlightTuning(),
                  mj=mj or MJPolicy(),
                  bands=[band or Band() for _ in range(4)],
                  hearing=hearing or HearingTuning(),
                  crowd=crowd or CrowdTuning(), **kw)


R = {}

R["r1_speed"] = {f"lap {l} bars": (lambda s, l=l: base(s, flight=FlightTuning(orbitLapBars=l)))
                 for l in (1, 2, 4, 8)}
R["r1_ships"] = {f"{n} ships": (lambda s, n=n: base(s, ships=n)) for n in (1, 2, 3, 4)}
R["r1_pulse"] = {
    "pulse off": lambda s: base(s, flight=FlightTuning(pulseMode="off")),
    "per beat (plan)": lambda s: base(s, flight=FlightTuning(pulseMode="beat")),
    "half bar": lambda s: base(s, flight=FlightTuning(pulseMode="half")),
    "bar only": lambda s: base(s, flight=FlightTuning(pulseMode="bar")),
    "per beat x3 depth": lambda s: base(s, flight=FlightTuning(pulseMode="beat", pulseDepth=0.9, pulseDownbeatDepth=1.8)),
}
R["r1_band"] = {f"{int(f)} Hz {o} oct": (lambda s, f=f, o=o: base(s, band=Band(f, o)))
                for f, o in ((250, 2), (1000, 2), (3000, 2), (8000, 2), (3000, 0.5), (3000, 1), (3000, 4))}
R["r1_gravity"] = {
    "no bodies": lambda s: base(s, mj=MJPolicy(bodies="none")),
    "static bodies": lambda s: base(s, mj=MJPolicy(bodies="static")),
    "closed loop": lambda s: base(s, mj=MJPolicy(bodies="loop")),
    "loop + escort": lambda s: base(s, mj=MJPolicy(bodies="loop", escort="rotate")),
    "loop + dead zones": lambda s: base(s, mj=MJPolicy(bodies="loop", deadZones=True)),
}

R["r2_gravity_G"] = {f"G {g}": (lambda s, g=g: base(s, flight=FlightTuning(gravity=g)))
                     for g in (0.02, 0.008, 0.004, 0.002, 0.001)}
R["r2_steer"] = {
    "plan steer, G .004": lambda s: base(s, flight=FlightTuning(gravity=0.004)),
    "stiff steer, G .004": lambda s: base(s, flight=FlightTuning(gravity=0.004, steerStiffness=1.5, steerDamping=1.2, steerMax=0.6)),
    "stiff steer, G .01": lambda s: base(s, flight=FlightTuning(gravity=0.01, steerStiffness=1.5, steerDamping=1.2, steerMax=0.6)),
    "stiff steer, G .02": lambda s: base(s, flight=FlightTuning(gravity=0.02, steerStiffness=1.5, steerDamping=1.2, steerMax=0.6)),
    "plan steer, gravMax .3": lambda s: base(s, flight=FlightTuning(gravityMax=0.3)),
    "plan steer, soft .2": lambda s: base(s, flight=FlightTuning(softening=0.2)),
}

R["r3_cap"] = {f"gravMax {g}": (lambda s, g=g: base(s, flight=FlightTuning(gravityMax=g)))
               for g in (0.1, 0.15, 0.2, 0.25, 0.3, 0.4)}
R["r3_cap_escort"] = {
    "cap .2 patrol": lambda s: base(s, flight=FlightTuning(gravityMax=0.2)),
    "cap .2 escort rotate": lambda s: base(s, flight=FlightTuning(gravityMax=0.2), mj=MJPolicy(escort="rotate")),
    "cap .2 escort, capture .3": lambda s: base(s, flight=FlightTuning(gravityMax=0.2, captureRadius=0.3), mj=MJPolicy(escort="rotate")),
    "cap .2 no bodies": lambda s: base(s, flight=FlightTuning(gravityMax=0.2), mj=MJPolicy(bodies="none")),
}

LAB = dict(gravityMax=0.2)
R["r4_control"] = {
    "0 ships (silence moves nothing)": lambda s: base(s, ships=0, flight=FlightTuning(**LAB)),
    "2 ships, crowd ignores sound": lambda s: base(s, flight=FlightTuning(**LAB), crowd=CrowdTuning(walk=0.0)),
    "2 ships, default": lambda s: base(s, flight=FlightTuning(**LAB)),
    "2 ships, walk x3": lambda s: base(s, flight=FlightTuning(**LAB), crowd=CrowdTuning(walk=0.024)),
    "2 ships, no social": lambda s: base(s, flight=FlightTuning(**LAB), crowd=CrowdTuning(socialPull=0.0)),
}

# ---- from round 5 on: the lab's flight tuning (gravity never stronger than steering)
LAB = dict(gravityMax=0.3)


def FT(**kw):
    return FlightTuning(**{**LAB, **kw})


R["r5_speed"] = {f"lap {l} bars": (lambda s, l=l: base(s, flight=FT(orbitLapBars=l)))
                 for l in (0.5, 1, 2, 4, 8)}
R["r5_ships"] = {f"{n} ships": (lambda s, n=n: base(s, ships=n, flight=FT())) for n in (1, 2, 3, 4)}
R["r5_pulse"] = {
    "pulse off": lambda s: base(s, flight=FT(pulseMode="off")),
    "per beat (plan)": lambda s: base(s, flight=FT(pulseMode="beat")),
    "half bar": lambda s: base(s, flight=FT(pulseMode="half")),
    "bar only": lambda s: base(s, flight=FT(pulseMode="bar")),
    "per beat x3 depth": lambda s: base(s, flight=FT(pulseMode="beat", pulseDepth=0.9, pulseDownbeatDepth=1.8)),
    "bar only x3 depth": lambda s: base(s, flight=FT(pulseMode="bar", pulseDownbeatDepth=1.8)),
}
R["r5_band"] = {f"{int(f)} Hz {o} oct": (lambda s, f=f, o=o: base(s, flight=FT(), band=Band(f, o)))
                for f, o in ((250, 2), (1000, 2), (3000, 2), (6000, 2), (8000, 2), (3000, 0.5), (3000, 1), (3000, 4))}
R["r5_gravity"] = {
    "no bodies": lambda s: base(s, flight=FT(), mj=MJPolicy(bodies="none")),
    "static bodies": lambda s: base(s, flight=FT(), mj=MJPolicy(bodies="static")),
    "closed loop": lambda s: base(s, flight=FT(), mj=MJPolicy(bodies="loop")),
    "loop + escort": lambda s: base(s, flight=FT(), mj=MJPolicy(bodies="loop", escort="rotate")),
    "loop + dead zones": lambda s: base(s, flight=FT(), mj=MJPolicy(bodies="loop", deadZones=True)),
}

R["r6_moves"] = {
    "lab baseline": lambda s: base(s, flight=FT()),
    "hold 1 bar in 8": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=8)),
    "hold 1 bar in 4": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=4)),
    "double 2 bars in 8": lambda s: base(s, flight=FT(), mj=MJPolicy(speedMove=2.0)),
    "halve 2 bars in 8": lambda s: base(s, flight=FT(), mj=MJPolicy(speedMove=0.5)),
    "counter-rotation": lambda s: base(s, flight=FT(), mj=MJPolicy(counter=True)),
    "kick every bar .4": lambda s: base(s, flight=FT(kickEveryBars=1)),
    "kick every 2 bars .4": lambda s: base(s, flight=FT(kickEveryBars=2)),
    "kick every 2 bars .8": lambda s: base(s, flight=FT(kickEveryBars=2, kickSpeed=0.8)),
    "escort rotate": lambda s: base(s, flight=FT(), mj=MJPolicy(escort="rotate")),
}

# ---- robustness: do the rankings survive a different listener model?
CORE = {
    "ref (2 ships, lap 4, 3k/2oct, loop)": dict(),
    "1 ship": dict(ships=1),
    "4 ships": dict(ships=4),
    "lap 2 bars": dict(flight=dict(orbitLapBars=2)),
    "lap 8 bars": dict(flight=dict(orbitLapBars=8)),
    "8k/2oct": dict(band=Band(8000, 2)),
    "3k/1oct": dict(band=Band(3000, 1)),
    "no bodies": dict(mj=dict(bodies="none")),
}
PERTURB = {
    "default": dict(),
    "MAMA x0.7": dict(hearing=dict(mamaScale=0.7)),
    "MAMA x1.4": dict(hearing=dict(mamaScale=1.4)),
    "side factor 2.5": dict(hearing=dict(kSide=2.5)),
    "side factor 8": dict(hearing=dict(kSide=8.0)),
    "habituation strong": dict(hearing=dict(novelFloor=0.05)),
    "habituation weak": dict(hearing=dict(novelFloor=0.5)),
    "fatigue x0.5": dict(hearing=dict(kLoad=0.02, kOverload=0.025, kVection=0.025, kBlur=0.015)),
    "fatigue x2": dict(hearing=dict(kLoad=0.08, kOverload=0.1, kVection=0.1, kBlur=0.06)),
    "crowd 40": dict(crowd=dict(count=40)),
    "crowd 120": dict(crowd=dict(count=120)),
    "140 BPM": dict(bpm=140.0),
    "start uniform": dict(crowd=dict(start="uniform")),
    "dt 1/128": dict(dt=1.0 / 128.0),
}


def build(seed, core, pert):
    kw = {}
    fl = dict(LAB)
    fl.update(core.get("flight", {}))
    kw["flight"] = FlightTuning(**fl)
    kw["hearing"] = HearingTuning(**pert.get("hearing", {}))
    kw["crowd"] = CrowdTuning(**pert.get("crowd", {}))
    kw["mj"] = MJPolicy(**core.get("mj", {}))
    if "band" in core:
        kw["band"] = core["band"]
    for k in ("ships",):
        if k in core:
            kw[k] = core[k]
    for k in ("bpm", "dt"):
        if k in pert:
            kw[k] = pert[k]
    return base(seed, **kw)


for pn, pert in PERTURB.items():
    R["r8_" + pn.replace(" ", "_").replace("/", "-")] = {
        cn: (lambda s, core=core, pert=pert: build(s, core, pert)) for cn, core in CORE.items()}

R["r7_band_gravity"] = {
    f"{lab} {b}": (lambda s, band=band, b=b: base(s, flight=FT(), band=band, mj=MJPolicy(bodies=b)))
    for lab, band in (("3k/2oct", Band(3000, 2)), ("8k/2oct", Band(8000, 2)), ("3k/4oct", Band(3000, 4)))
    for b in ("none", "loop")}
R["r7_kick"] = {
    "lab baseline": lambda s: base(s, flight=FT()),
    "kick .15 / 4 bars": lambda s: base(s, flight=FT(kickEveryBars=4, kickSpeed=0.15)),
    "kick .25 / 4 bars": lambda s: base(s, flight=FT(kickEveryBars=4, kickSpeed=0.25)),
    "kick .15 / 2 bars": lambda s: base(s, flight=FT(kickEveryBars=2, kickSpeed=0.15)),
    "kick .25 / 2 bars": lambda s: base(s, flight=FT(kickEveryBars=2, kickSpeed=0.25)),
    "kick .25 / 8 bars": lambda s: base(s, flight=FT(kickEveryBars=8, kickSpeed=0.25)),
}
R["r7_escort"] = {
    "lab baseline": lambda s: base(s, flight=FT()),
    "escort most bored": lambda s: base(s, flight=FT(), mj=MJPolicy(escort="rotate")),
    "escort largest": lambda s: base(s, flight=FT(), mj=MJPolicy(escort="rotate", escortPick="largest")),
    "escort smallest": lambda s: base(s, flight=FT(), mj=MJPolicy(escort="rotate", escortPick="smallest")),
    "escort 4 of 16 bars": lambda s: base(s, flight=FT(), mj=MJPolicy(escort="rotate", escortBars=4, patrolBars=12)),
    "escort wide (capture .3)": lambda s: base(s, flight=FT(captureRadius=0.3), mj=MJPolicy(escort="rotate")),
    "escort wide, slow (4-bar lap)": lambda s: base(s, flight=FT(captureRadius=0.3, captureLapBars=4), mj=MJPolicy(escort="rotate")),
}
R["r7_mass"] = {
    "lab baseline": lambda s: base(s, flight=FT()),
    "mass x0.5": lambda s: base(s, flight=FT(), mj=MJPolicy(massScale=0.5)),
    "mass x2": lambda s: base(s, flight=FT(), mj=MJPolicy(massScale=2.0)),
    "groups from 8 people": lambda s: base(s, flight=FT(), mj=MJPolicy(minGroup=8)),
    "body follows slowly": lambda s: base(s, flight=FT(), mj=MJPolicy(follow=0.15)),
}
R["r7_combo"] = {
    "lab baseline": lambda s: base(s, flight=FT()),
    "hold 1/8, one ship": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=8, moveShips=1)),
    "double 2/8, one ship": lambda s: base(s, flight=FT(), mj=MJPolicy(speedMove=2.0, moveShips=1)),
    "hold 1/8 + double 2/8": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=8, speedMove=2.0)),
    "hold 1/8 + double, 8k": lambda s: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(hold=8, speedMove=2.0)),
    "hold 1/8 + double, no bodies": lambda s: base(s, flight=FT(), mj=MJPolicy(bodies="none", hold=8, speedMove=2.0)),
}

STIFF = dict(steerStiffness=2.5, steerDamping=1.6, steerMax=0.6)
R["r9_steer"] = {
    "lab (plan steer, cap .3)": lambda s: base(s, flight=FT()),
    "stiff steer, cap .3 (ratio .5)": lambda s: base(s, flight=FlightTuning(gravityMax=0.3, **STIFF)),
    "stiff steer, cap .45 (ratio .75)": lambda s: base(s, flight=FlightTuning(gravityMax=0.45, **STIFF)),
    "stiff steer, cap .6 (ratio 1)": lambda s: base(s, flight=FlightTuning(gravityMax=0.6, **STIFF)),
    "stiff steer, cap .8 (ratio 1.33)": lambda s: base(s, flight=FlightTuning(gravityMax=0.8, **STIFF)),
    "stiff steer, no bodies": lambda s: base(s, flight=FlightTuning(gravityMax=0.6, **STIFF), mj=MJPolicy(bodies="none")),
}
BEST = dict(hold=8, speedMove=2.0)
R["r9_long"] = {
    "128 bars: lab baseline": lambda s: base(s, bars=128, flight=FT()),
    "128 bars: no bodies": lambda s: base(s, bars=128, flight=FT(), mj=MJPolicy(bodies="none")),
    "128 bars: hold+double": lambda s: base(s, bars=128, flight=FT(), mj=MJPolicy(**BEST)),
    "128 bars: hold+double, 8k": lambda s: base(s, bars=128, flight=FT(), band=Band(8000, 2), mj=MJPolicy(**BEST)),
}
R["r9_ships_moves"] = {
    f"{n} ships, hold+double": (lambda s, n=n: base(s, ships=n, flight=FT(), mj=MJPolicy(**BEST)))
    for n in (1, 2, 3, 4)}

PHRASE = ((8, dict(ships=1, rate=0.5, hold=0, speedMove=1.0)),     # intro: one ship, lap 8
          (8, dict(ships=2, rate=1.0, hold=8, speedMove=1.0)),     # groove: two ships, lap 4
          (8, dict(ships=2, rate=1.0, hold=8, speedMove=2.0)),     # peak: doublings
          (8, dict(ships=1, rate=1.0, hold=4, speedMove=1.0)))     # break: one ship, stop-start
R["r10_program"] = {
    "constant: hold+double": lambda s: base(s, bars=136, flight=FT(), mj=MJPolicy(**BEST)),
    "phrase programme (32 bars)": lambda s: base(s, bars=136, flight=FT(), mj=MJPolicy(program=PHRASE)),
    "1 and 2 ships, 8 bars each": lambda s: base(s, bars=136, flight=FT(),
                                                 mj=MJPolicy(program=((8, dict(ships=1)), (8, dict(ships=2))), **BEST)),
    "2 and 3 ships, 8 bars each": lambda s: base(s, ships=3, bars=136, flight=FT(),
                                                 mj=MJPolicy(program=((8, dict(ships=2)), (8, dict(ships=3))), **BEST)),
    "constant baseline": lambda s: base(s, bars=136, flight=FT()),
}
R["r13_dive"] = {
    "3k always": lambda s: base(s, flight=FT(), mj=MJPolicy(**BEST)),
    "8k always": lambda s: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(**BEST)),
    "3k, 8k over groups": lambda s: base(s, flight=FT(), diveBand=Band(8000, 2), mj=MJPolicy(**BEST)),
    "3k/4oct always": lambda s: base(s, flight=FT(), band=Band(3000, 4), mj=MJPolicy(**BEST)),
    "1k, 8k over groups": lambda s: base(s, flight=FT(), band=Band(1000, 2), diveBand=Band(8000, 2), mj=MJPolicy(**BEST)),
}
R["r14_bpm"] = {f"{bpm} BPM, lap {l}": (lambda s, bpm=bpm, l=l: base(s, bpm=float(bpm), flight=FT(orbitLapBars=l)))
                for bpm in (100, 126, 174) for l in (2, 4, 8)}
R["r15_reach"] = {f"reach {r}": (lambda s, r=r: base(s, reach=r, flight=FT(), mj=MJPolicy(**BEST)))
                  for r in (0.3, 0.4, 0.5, 0.6, 0.7)}
for pn in ("habituation weak", "habituation strong", "fatigue x2", "MAMA x1.4", "side factor 8", "crowd 120"):
    pert = PERTURB[pn]
    R["r11_" + pn.replace(" ", "_")] = {
        "baseline": (lambda s, pert=pert: build(s, {}, pert)),
        "hold+double": (lambda s, pert=pert: build(s, {"mj": dict(BEST)}, pert)),
        "hold+double 8k": (lambda s, pert=pert: build(s, {"mj": dict(BEST), "band": Band(8000, 2)}, pert)),
        "cap 1.5 (plan)": (lambda s, pert=pert: build(s, {"flight": dict(gravityMax=1.5)}, pert)),
    }

R["r16_effects"] = {
    "no effect": lambda s: base(s, flight=FT(), mj=MJPolicy(**BEST)),
    "ping-pong step / beat": lambda s: base(s, flight=FT(), mj=MJPolicy(effect="pingpong", effectBeats=1, **BEST)),
    "ping-pong step / 2 beats": lambda s: base(s, flight=FT(), mj=MJPolicy(effect="pingpong", effectBeats=2, **BEST)),
    "ping-pong glide / 2 beats": lambda s: base(s, flight=FT(), mj=MJPolicy(effect="pingpong", effectBeats=2, effectGlide=1.0, **BEST)),
    "ping-pong 1/16-bar glide / 2 beats": lambda s: base(s, flight=FT(), mj=MJPolicy(effect="pingpong", effectBeats=2, effectGlide=0.125, **BEST)),
    "swirl 1 lap / 2 beats": lambda s: base(s, flight=FT(), mj=MJPolicy(effect="swirl", effectBeats=2, **BEST)),
    "swirl 1 lap / beat": lambda s: base(s, flight=FT(), mj=MJPolicy(effect="swirl", effectBeats=1, **BEST)),
}

# ---- the closing shootout: the plan as written vs the lab's defaults (12 seeds, 96 bars)
LABDEF = dict(gravityMax=0.6, captureRadius=0.3, **STIFF)
R["r17_shootout"] = {
    "A plan as written, 4 ships": lambda s: base(s, ships=4, bars=96, flight=FlightTuning()),
    "B plan as written, 2 ships": lambda s: base(s, bars=96, flight=FlightTuning()),
    "C bare orbit, 2 ships, no bodies": lambda s: base(s, bars=96, flight=FlightTuning(**LABDEF), mj=MJPolicy(bodies="none")),
    "D plan + cap rule": lambda s: base(s, bars=96, flight=FlightTuning(gravityMax=0.3)),
    "E lab flight (stiff steer, cap = steer, wide escort)": lambda s: base(s, bars=96, flight=FlightTuning(**LABDEF)),
    "F lab flight + hold/double": lambda s: base(s, bars=96, flight=FlightTuning(**LABDEF), mj=MJPolicy(**BEST)),
    "G lab flight + hold/double + 8k/2oct": lambda s: base(s, bars=96, flight=FlightTuning(**LABDEF), band=Band(8000, 2), mj=MJPolicy(**BEST)),
}

ADAPT = dict(adaptive=True, **BEST)
R["r18_adaptive"] = {}
for pn in ("default", "fatigue x2", "fatigue x0.5", "habituation weak"):
    pert = PERTURB[pn]
    R["r18_adaptive"][pn + ": baseline"] = (lambda s, pert=pert: build(s, {}, pert))
    R["r18_adaptive"][pn + ": hold+double"] = (lambda s, pert=pert: build(s, {"mj": dict(BEST)}, pert))
    R["r18_adaptive"][pn + ": adaptive"] = (lambda s, pert=pert: build(s, {"mj": dict(ADAPT)}, pert))

R["r18b_adaptive"] = {}
for pn in ("default", "fatigue x2", "fatigue x0.5", "habituation weak"):
    pert = PERTURB[pn]
    R["r18b_adaptive"][pn + ": baseline"] = (lambda s, pert=pert: build(s, {}, pert))
    R["r18b_adaptive"][pn + ": hold+double"] = (lambda s, pert=pert: build(s, {"mj": dict(BEST)}, pert))
    for hi, lo in ((0.2, 0.12), (0.25, 0.15)):
        R["r18b_adaptive"][f"{pn}: adaptive {hi}/{lo}"] = (
            lambda s, pert=pert, hi=hi, lo=lo: build(s, {"mj": dict(adaptive=True, calmAbove=hi, calmBelow=lo, **BEST)}, pert))

R["r19_bandit"] = {}
for pn in ("default", "fatigue x2", "fatigue x0.5", "habituation weak", "habituation strong"):
    pert = PERTURB[pn]
    R["r19_bandit"][pn + ": baseline"] = (lambda s, pert=pert: build(s, {}, pert))
    R["r19_bandit"][pn + ": hold+double"] = (lambda s, pert=pert: build(s, {"mj": dict(BEST)}, pert))
    R["r19_bandit"][pn + ": learning MJ"] = (lambda s, pert=pert: build(s, {"mj": dict(bandit=True, **BEST)}, pert))


def _bars(cfg, n):
    cfg.bars = n
    return cfg


for _k, _f in list(R["r19_bandit"].items()):
    R["r19_bandit"][_k] = (lambda s, _f=_f: _bars(_f(s), 96))

R["r20_bandit_long"] = {}
for pn in ("default", "fatigue x2", "habituation strong"):
    pert = PERTURB[pn]
    R["r20_bandit_long"][pn + ": baseline"] = (lambda s, pert=pert: _bars(build(s, {}, pert), 192))
    R["r20_bandit_long"][pn + ": hold+double"] = (lambda s, pert=pert: _bars(build(s, {"mj": dict(BEST)}, pert), 192))
    R["r20_bandit_long"][pn + ": learning, 8-bar blocks"] = (lambda s, pert=pert: _bars(build(s, {"mj": dict(bandit=True, **BEST)}, pert), 192))
    R["r20_bandit_long"][pn + ": learning, 4-bar blocks, explore .15"] = (
        lambda s, pert=pert: _bars(build(s, {"mj": dict(bandit=True, banditBlock=4, explore=0.15, **BEST)}, pert), 192))

SCENES = {
    "one hotspot, centre": ((0.0, 0.0, 3.0),),
    "three groups": ((0.4, 0.3, 1.0), (-0.45, 0.1, 1.0), (0.05, -0.5, 1.0)),
    "crowd + dead zone on the path": ((0.1, 0.2, 2.0), (-0.75, 0.0, -2.0)),
    "eight mixed": ((0.5, 0.5, 2.0), (-0.5, 0.5, 1.0), (0.5, -0.5, 1.0), (-0.5, -0.5, 3.0),
                    (0.0, 0.7, -2.0), (0.7, 0.0, 1.0), (-0.7, 0.0, 2.0), (0.0, -0.2, 1.0)),
}
R["r21_scenes"] = {}
for sn, bodies in SCENES.items():
    for lab, fl in (("plan (cap 1.5)", dict()), ("cap = steer (0.3)", dict(gravityMax=0.3)),
                    ("stiff, cap = steer (0.6)", dict(gravityMax=0.6, **STIFF))):
        R["r21_scenes"][f"{sn}: {lab}"] = (lambda s, bodies=bodies, fl=fl:
                                           base(s, flight=FlightTuning(**fl), mj=MJPolicy(fixedBodies=bodies)))
R["r23_cadence"] = {
    "no moves": lambda s: base(s, flight=FT()),
    "hold 1 bar / 16": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=16)),
    "hold 1 bar / 8": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=8)),
    "hold 2 beats / 8 bars": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=8, holdBeats=2)),
    "hold 2 beats / 4 bars": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=4, holdBeats=2)),
    "double 2 bars / 16": lambda s: base(s, flight=FT(), mj=MJPolicy(speedMove=2.0, speedEvery=16)),
    "double 1 bar / 4": lambda s: base(s, flight=FT(), mj=MJPolicy(speedMove=2.0, speedEvery=4, speedBars=1)),
    "double 4 bars / 16": lambda s: base(s, flight=FT(), mj=MJPolicy(speedMove=2.0, speedEvery=16, speedBars=4)),
    "hold 1/8 + double 2/8 (ref)": lambda s: base(s, flight=FT(), mj=MJPolicy(**BEST)),
    "hold 1/16 + double 2/16": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=16, speedMove=2.0, speedEvery=16)),
    "hold 2 beats/8 + double 2/8": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=8, holdBeats=2, speedMove=2.0)),
}

# ---- r24: does the shootout order survive other listeners? (64 bars, 4 seeds)
SHOOT = {
    "C bare orbit": dict(flight=dict(LABDEF), mj=dict(bodies="none")),
    "D plan + cap rule": dict(flight=dict(gravityMax=0.3)),
    "E lab flight": dict(flight=dict(LABDEF)),
    "F lab flight + hold/double": dict(flight=dict(LABDEF), mj=dict(BEST)),
    "P plan as written": dict(flight=dict(gravityMax=1.5)),
}
for pn, pert in PERTURB.items():
    R["r24_" + pn.replace(" ", "_").replace("/", "-")] = {
        cn: (lambda s, core=core, pert=pert: build(s, core, pert)) for cn, core in SHOOT.items()}

R["r25_cadence2"] = {
    "no moves": lambda s: base(s, flight=FT()),
    "hold 1/8 + double 2/8 (ref)": lambda s: base(s, flight=FT(), mj=MJPolicy(**BEST)),
    "hold 2 beats / 4 bars": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=4, holdBeats=2)),
    "hold 1 beat / 2 bars": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=2, holdBeats=1)),
    "hold 2 beats / 2 bars": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=2, holdBeats=2)),
    "hold 1 beat / 4 bars": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=4, holdBeats=1)),
    "hold 2 beats/4 + double 2/8": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=4, holdBeats=2, speedMove=2.0)),
    "hold 2 beats/4 + double 2/16": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=4, holdBeats=2, speedMove=2.0, speedEvery=16)),
    "hold 2 beats/4 + double, 8k": lambda s: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(hold=4, holdBeats=2, speedMove=2.0)),
}


# ---- more listener variants for the robustness table (run as r8_*)
for pn, pert in {"speakers 8 ring only": dict(hearing=dict(layout="8")),
                 "speakers 16+8": dict(hearing=dict(layout="16+8")),
                 "listeners face the centre": dict(hearing=dict(facing="centre")),
                 "listeners face anywhere": dict(hearing=dict(facing="random"))}.items():
    PERTURB[pn] = pert
    R["r8_" + pn.replace(" ", "_")] = {
        cn: (lambda s, core=core, pert=pert: build(s, core, pert)) for cn, core in CORE.items()}

BREATH = dict(hold=2, holdBeats=1)
R["r26_breath_robust"] = {}
for pn, pert in PERTURB.items():
    tag = pn
    R["r26_breath_robust"][tag + ": baseline"] = (lambda s, pert=pert: build(s, {}, pert))
    R["r26_breath_robust"][tag + ": breath"] = (lambda s, pert=pert: build(s, {"mj": dict(BREATH)}, pert))
    R["r26_breath_robust"][tag + ": hold+double"] = (lambda s, pert=pert: build(s, {"mj": dict(BEST)}, pert))
R["r27_final"] = {
    "P plan as written": lambda s: base(s, bars=96, flight=FlightTuning()),
    "C bare orbit": lambda s: base(s, bars=96, flight=FT(), mj=MJPolicy(bodies="none")),
    "D plan + cap rule": lambda s: base(s, bars=96, flight=FT()),
    "D + breath": lambda s: base(s, bars=96, flight=FT(), mj=MJPolicy(**BREATH)),
    "D + breath + double 2/16": lambda s: base(s, bars=96, flight=FT(), mj=MJPolicy(speedMove=2.0, speedEvery=16, **BREATH)),
    "D + breath, 8k/2oct": lambda s: base(s, bars=96, flight=FT(), band=Band(8000, 2), mj=MJPolicy(**BREATH)),
    "D + breath, 3k/4oct": lambda s: base(s, bars=96, flight=FT(), band=Band(3000, 4), mj=MJPolicy(**BREATH)),
    "D + hold/double, 8k/2oct": lambda s: base(s, bars=96, flight=FT(), band=Band(8000, 2), mj=MJPolicy(**BEST)),
}

R["r28_breath_shape"] = {
    "no moves": lambda s: base(s, flight=FT()),
    "breath (both ships, beat 4, every 2nd bar)": lambda s: base(s, flight=FT(), mj=MJPolicy(**BREATH)),
    "breath staggered (ships alternate bars)": lambda s: base(s, flight=FT(), mj=MJPolicy(holdStagger=1, **BREATH)),
    "breath on the one (stop beat 1)": lambda s: base(s, flight=FT(), mj=MJPolicy(holdAt="start", **BREATH)),
    "breath every bar": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=1, holdBeats=1)),
    "breath, one ship only": lambda s: base(s, flight=FT(), mj=MJPolicy(moveShips=1, **BREATH)),
    "breath + double 2 bars in 16": lambda s: base(s, flight=FT(), mj=MJPolicy(speedMove=2.0, speedEvery=16, **BREATH)),
}
R["r28_breath_ships"] = {f"{n} ships + breath": (lambda s, n=n: base(s, ships=n, flight=FT(), mj=MJPolicy(**BREATH)))
                         for n in (1, 2, 3, 4)}

R["r29_gate"] = {
    "no moves": lambda s: base(s, flight=FT()),
    "breath every 2nd bar (beat 4)": lambda s: base(s, flight=FT(), mj=MJPolicy(**BREATH)),
    "breath every bar (beat 4)": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=1, holdBeats=1)),
    "half-beat breath every bar": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=1, holdPattern=(3,), holdLen=0.5)),
    "beats 2 and 4, every bar": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=1, holdPattern=(1, 3))),
    "half-beats on 2 and 4, every bar": lambda s: base(s, flight=FT(), mj=MJPolicy(hold=1, holdPattern=(1, 3), holdLen=0.5)),
    "every bar, 8k/2oct": lambda s: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(hold=1, holdBeats=1)),
}

BREATH1 = dict(hold=1, holdBeats=1)
R["r30_breath1_robust"] = {}
for pn, pert in PERTURB.items():
    R["r30_breath1_robust"][pn + ": baseline"] = (lambda s, pert=pert: build(s, {}, pert))
    R["r30_breath1_robust"][pn + ": breath every bar"] = (lambda s, pert=pert: build(s, {"mj": dict(BREATH1)}, pert))
    R["r30_breath1_robust"][pn + ": breath every 2nd bar"] = (lambda s, pert=pert: build(s, {"mj": dict(BREATH)}, pert))
R["r31_breath_tempo"] = {}
for bpm in (100, 126, 174):
    R["r31_breath_tempo"][f"{bpm} BPM: no moves"] = (lambda s, bpm=bpm: base(s, bpm=float(bpm), flight=FT()))
    R["r31_breath_tempo"][f"{bpm} BPM: 1-beat breath every bar"] = (lambda s, bpm=bpm: base(s, bpm=float(bpm), flight=FT(), mj=MJPolicy(**BREATH1)))
    R["r31_breath_tempo"][f"{bpm} BPM: half-beat breath every bar"] = (lambda s, bpm=bpm: base(s, bpm=float(bpm), flight=FT(), mj=MJPolicy(hold=1, holdPattern=(3,), holdLen=0.5)))
    R["r31_breath_tempo"][f"{bpm} BPM: 2-beat breath every 2nd bar"] = (lambda s, bpm=bpm: base(s, bpm=float(bpm), flight=FT(), mj=MJPolicy(hold=2, holdBeats=2)))

R["r32_final"] = {
    "P plan as written": lambda s: base(s, bars=96, flight=FlightTuning()),
    "C bare orbit": lambda s: base(s, bars=96, flight=FT(), mj=MJPolicy(bodies="none")),
    "D plan + cap rule": lambda s: base(s, bars=96, flight=FT()),
    "D + breath every 2nd bar": lambda s: base(s, bars=96, flight=FT(), mj=MJPolicy(**BREATH)),
    "D + breath every bar": lambda s: base(s, bars=96, flight=FT(), mj=MJPolicy(**BREATH1)),
    "D + breath every bar, 3k/4oct": lambda s: base(s, bars=96, flight=FT(), band=Band(3000, 4), mj=MJPolicy(**BREATH1)),
    "D + breath every bar, 8k/2oct": lambda s: base(s, bars=96, flight=FT(), band=Band(8000, 2), mj=MJPolicy(**BREATH1)),
    "D + breath every bar + double 2/16, 8k/2oct": lambda s: base(s, bars=96, flight=FT(), band=Band(8000, 2), mj=MJPolicy(speedMove=2.0, speedEvery=16, **BREATH1)),
}

THREE = SCENES["three groups"]
R["r33_breath_gravity"] = {}
for blab, band in (("3k/2oct", Band(3000, 2)), ("8k/2oct", Band(8000, 2))):
    R["r33_breath_gravity"][f"{blab}: breath, no bodies"] = (lambda s, band=band: base(s, flight=FT(), band=band, mj=MJPolicy(bodies="none", **BREATH1)))
    R["r33_breath_gravity"][f"{blab}: breath, closed loop"] = (lambda s, band=band: base(s, flight=FT(), band=band, mj=MJPolicy(**BREATH1)))
    R["r33_breath_gravity"][f"{blab}: breath, three groups placed"] = (lambda s, band=band: base(s, flight=FT(), band=band, mj=MJPolicy(fixedBodies=THREE, **BREATH1)))
    R["r33_breath_gravity"][f"{blab}: breath, loop, mass x0.5"] = (lambda s, band=band: base(s, flight=FT(), band=band, mj=MJPolicy(massScale=0.5, **BREATH1)))
    R["r33_breath_gravity"][f"{blab}: breath, loop + wide escort 4/16"] = (lambda s, band=band: base(s, flight=FT(captureRadius=0.3), band=band,
        mj=MJPolicy(escort="rotate", escortBars=4, patrolBars=12, **BREATH1)))

R["r34_breath_gravity_robust"] = {}
for pn, pert in PERTURB.items():
    R["r34_breath_gravity_robust"][pn + ": breath, no bodies"] = (lambda s, pert=pert: build(s, {"mj": dict(bodies="none", **BREATH1)}, pert))
    R["r34_breath_gravity_robust"][pn + ": breath, closed loop"] = (lambda s, pert=pert: build(s, {"mj": dict(BREATH1)}, pert))
    R["r34_breath_gravity_robust"][pn + ": breath, loop, mass x0.5"] = (lambda s, pert=pert: build(s, {"mj": dict(massScale=0.5, **BREATH1)}, pert))

R["r35_overhead"] = {}
for hl, hk in (("default ears", dict()), ("overhead heard like azimuth", dict(elevationLikeAzimuth=True))):
    for blab, band in (("3k/2oct", Band(3000, 2)), ("8k/2oct", Band(8000, 2))):
        for lab, mj in (("no bodies", dict(bodies="none")), ("closed loop", dict()), ("loop, mass x0.5", dict(massScale=0.5))):
            R["r35_overhead"][f"{hl}, {blab}: breath, {lab}"] = (lambda s, hk=hk, band=band, mj=mj:
                base(s, flight=FT(), band=band, hearing=HearingTuning(**hk), mj=MJPolicy(**mj, **BREATH1)))

R["r36_why"] = {}
for hl, hk in (("default", dict()),
               ("no precedence, no off-centre blur", dict(kPrecedence=0.0, offCentreBlur=0.0)),
               ("no proximity loudness", dict(proxMax=1.0)),
               ("no fatigue", dict(kLoad=0.0, kOverload=0.0, kVection=0.0, kBlur=0.0)),
               ("ideal: all three off + overhead like azimuth", dict(kPrecedence=0.0, offCentreBlur=0.0, proxMax=1.0,
                    kLoad=0.0, kOverload=0.0, kVection=0.0, kBlur=0.0, elevationLikeAzimuth=True))):
    for lab, mj in (("no bodies", dict(bodies="none")), ("closed loop", dict())):
        R["r36_why"][f"{hl}: {lab}"] = (lambda s, hk=hk, mj=mj:
            base(s, flight=FT(), hearing=HearingTuning(**hk), mj=MJPolicy(**mj, **BREATH1)))

R["r37_useful_planets"] = {
    "no bodies": lambda s: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(bodies="none", **BREATH1)),
    "closed loop": lambda s: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(**BREATH1)),
    "loop, mass x0.5": lambda s: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, **BREATH1)),
    "loop, groups repel (x-0.5)": lambda s: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(massScale=-0.5, **BREATH1)),
    "loop, gravity only on beat 1": lambda s: base(s, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(**BREATH1)),
    "loop, gravity on beat 1, mass x0.5": lambda s: base(s, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, **BREATH1)),
    "loop, mass x0.25": lambda s: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(massScale=0.25, **BREATH1)),
}

R["r38_gate_robust"] = {}
for pn, pert in PERTURB.items():
    R["r38_gate_robust"][pn + ": closed loop"] = (lambda s, pert=pert: build(s, {"mj": dict(BREATH1)}, pert))
    R["r38_gate_robust"][pn + ": gravity on beat 1, mass x0.5"] = (lambda s, pert=pert: build(s, {"flight": dict(pulseMode="gate"), "mj": dict(massScale=0.5, **BREATH1)}, pert))
    R["r38_gate_robust"][pn + ": no bodies"] = (lambda s, pert=pert: build(s, {"mj": dict(bodies="none", **BREATH1)}, pert))

REC = dict(flight=dict(pulseMode="gate"), mj=dict(massScale=0.5, **BREATH1))
R["r39_recommended"] = {
    "P plan as written": lambda s: base(s, bars=96, flight=FlightTuning()),
    "C bare orbit, 8k": lambda s: base(s, bars=96, flight=FT(), band=Band(8000, 2), mj=MJPolicy(bodies="none")),
    "breath, no bodies, 8k": lambda s: base(s, bars=96, flight=FT(), band=Band(8000, 2), mj=MJPolicy(bodies="none", **BREATH1)),
    "R recommended: cap rule + breath + gated half-mass planets, 8k": lambda s: base(s, bars=96, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, **BREATH1)),
    "R, 3k/4oct": lambda s: base(s, bars=96, flight=FT(pulseMode="gate"), band=Band(3000, 4), mj=MJPolicy(massScale=0.5, **BREATH1)),
    "R, 3 ships": lambda s: base(s, ships=3, bars=96, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, **BREATH1)),
}
R["r40_long"] = {
    "192 bars: breath, no bodies, 8k": lambda s: base(s, bars=192, flight=FT(), band=Band(8000, 2), mj=MJPolicy(bodies="none", **BREATH1)),
    "192 bars: R recommended, 8k": lambda s: base(s, bars=192, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, **BREATH1)),
    "192 bars: closed loop, no moves, 3k (plan + cap)": lambda s: base(s, bars=192, flight=FT()),
}

R["r41_context"] = {}
for lab, kw in (("100 BPM", dict(bpm=100.0)), ("174 BPM", dict(bpm=174.0)), ("crowd 40", dict(crowd=CrowdTuning(count=40))),
                ("crowd 120", dict(crowd=CrowdTuning(count=120))), ("crowd starts uniform", dict(crowd=CrowdTuning(start="uniform")))):
    R["r41_context"][lab + ": P plan as written"] = (lambda s, kw=kw: base(s, flight=FlightTuning(), **kw))
    R["r41_context"][lab + ": C bare orbit, 8k"] = (lambda s, kw=kw: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(bodies="none"), **kw))
    R["r41_context"][lab + ": R recommended, 8k"] = (lambda s, kw=kw: base(s, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, **BREATH1), **kw))

R["r42_gate_cost"] = {
    "breath, no bodies, 8k": lambda s: base(s, bars=96, flight=FT(), band=Band(8000, 2), mj=MJPolicy(bodies="none", **BREATH1)),
    "R recommended, 8k": lambda s: base(s, bars=96, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, **BREATH1)),
}

R["r43_lap_with_breath"] = {}
for bpm, laps in ((100, (2, 4)), (126, (2, 4)), (174, (4, 8))):
    for l in laps:
        R["r43_lap_with_breath"][f"{bpm} BPM, lap {l}"] = (lambda s, bpm=bpm, l=l: base(s, bpm=float(bpm),
            flight=FT(pulseMode="gate", orbitLapBars=l), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, **BREATH1)))

R["r44_reach_rec"] = {f"R, reach {r}": (lambda s, r=r: base(s, reach=r, flight=FT(pulseMode="gate"), band=Band(8000, 2),
                                                            mj=MJPolicy(massScale=0.5, **BREATH1))) for r in (0.4, 0.5, 0.6, 0.7)}

R["r45_scenes_rec"] = {"no bodies": lambda s: base(s, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(bodies="none", **BREATH1))}
for sn, bodies in SCENES.items():
    half = tuple((x, y, m * 0.5) for x, y, m in bodies)
    R["r45_scenes_rec"][sn] = (lambda s, half=half: base(s, flight=FT(pulseMode="gate"), band=Band(8000, 2),
                                                          mj=MJPolicy(fixedBodies=half, **BREATH1)))

R["r46_rec_robust"] = {}
for pn, pert in PERTURB.items():
    R["r46_rec_robust"][pn + ": bare orbit, 8k"] = (lambda s, pert=pert: build(s, {"mj": dict(bodies="none"), "band": Band(8000, 2)}, pert))
    R["r46_rec_robust"][pn + ": recommended, 8k"] = (lambda s, pert=pert: build(s, {"flight": dict(pulseMode="gate"), "mj": dict(massScale=0.5, **BREATH1), "band": Band(8000, 2)}, pert))
    R["r46_rec_robust"][pn + ": plan as written"] = (lambda s, pert=pert: build(s, {"flight": dict(gravityMax=1.5)}, pert))

R["r47_escort_rec"] = {
    "R": lambda s: base(s, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, **BREATH1)),
    "R + escort 4/16, capture .15": lambda s: base(s, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, escort="rotate", escortBars=4, patrolBars=12, **BREATH1)),
    "R + escort 4/16, capture .3": lambda s: base(s, flight=FT(pulseMode="gate", captureRadius=0.3), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, escort="rotate", escortBars=4, patrolBars=12, **BREATH1)),
    "R + escort 4/16, capture .45": lambda s: base(s, flight=FT(pulseMode="gate", captureRadius=0.45), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, escort="rotate", escortBars=4, patrolBars=12, **BREATH1)),
}

R["r48_gate_cap"] = {f"gate, cap {c}": (lambda s, c=c: base(s, flight=FlightTuning(pulseMode="gate", gravityMax=c), band=Band(8000, 2),
                                                          mj=MJPolicy(massScale=0.5, **BREATH1))) for c in (0.3, 0.6, 1.0, 1.5)}
R["r48_gate_cap"]["gate, cap 1.5, full mass, no breath"] = lambda s: base(s, flight=FlightTuning(pulseMode="gate"))
R["r48_gate_cap"]["plan as written"] = lambda s: base(s, flight=FlightTuning())

R["r49_gate_only"] = {}
for pn, pert in PERTURB.items():
    R["r49_gate_only"][pn + ": plan as written"] = (lambda s, pert=pert: build(s, {"flight": dict(gravityMax=1.5)}, pert))
    R["r49_gate_only"][pn + ": plan + gate only"] = (lambda s, pert=pert: build(s, {"flight": dict(gravityMax=1.5, pulseMode="gate")}, pert))

R["r50_front_crowd"] = {
    "front crowd: plan as written": lambda s: base(s, flight=FlightTuning(), crowd=CrowdTuning(start="front")),
    "front crowd: bare orbit, 8k": lambda s: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(bodies="none"), crowd=CrowdTuning(start="front")),
    "front crowd: R recommended, 8k": lambda s: base(s, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, **BREATH1), crowd=CrowdTuning(start="front")),
    "front crowd: breath, no bodies, 8k": lambda s: base(s, flight=FT(), band=Band(8000, 2), mj=MJPolicy(bodies="none", **BREATH1), crowd=CrowdTuning(start="front")),
}

R["r51_call_response"] = {
    "both stop on 4": lambda s: base(s, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, hold=1, holdPattern=(3,))),
    "ship 1 on 4, ship 2 on 2": lambda s: base(s, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, hold=1, holdPattern=(3,), holdPattern2=(1,))),
    "ship 1 on 4, ship 2 on 3": lambda s: base(s, flight=FT(pulseMode="gate"), band=Band(8000, 2), mj=MJPolicy(massScale=0.5, hold=1, holdPattern=(3,), holdPattern2=(2,))),
}

R["r52_call_response_robust"] = {}
for pn, pert in PERTURB.items():
    R["r52_call_response_robust"][pn + ": both on 4"] = (lambda s, pert=pert: build(s, {"flight": dict(pulseMode="gate"), "band": Band(8000, 2), "mj": dict(massScale=0.5, hold=1, holdPattern=(3,))}, pert))
    R["r52_call_response_robust"][pn + ": 4 and 2"] = (lambda s, pert=pert: build(s, {"flight": dict(pulseMode="gate"), "band": Band(8000, 2), "mj": dict(massScale=0.5, hold=1, holdPattern=(3,), holdPattern2=(1,))}, pert))

R["r53_band_rec"] = {f"R, {int(f)} Hz {o} oct": (lambda s, f=f, o=o: base(s, flight=FT(pulseMode="gate"), band=Band(f, o),
                                                    mj=MJPolicy(massScale=0.5, **BREATH1)))
                     for f, o in ((3000, 2), (3000, 4), (6000, 2), (8000, 2), (8000, 1), (5000, 3))}
