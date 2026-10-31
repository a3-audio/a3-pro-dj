"""Traced showcase runs -> SVG figures in figs/."""
import os, math, json, sys
from sim import Config, run
from flight import FlightTuning
from hearing import Band
from crowd import CrowdTuning
from mj import MJPolicy
import svg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
LAB = dict(gravityMax=0.3)


def save(name, s):
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(s)


def traced(**kw):
    cfg = Config(trace=True, **kw)
    return cfg, run(cfg)


def trajectories(name, title, note, bars=(40, 48), **kw):
    cfg, r = traced(**kw)
    tr = r["trace"]
    a, b = int(bars[0] * 4 / cfg.sampleBeats), int(bars[1] * 4 / cfg.sampleBeats)
    save(name, svg.trajectories(tr, a, b, cfg.ships, title, bar=bars[1] - 1, extra_note=note))
    return cfg, r


def perception_map(name, title, metric, **kw):
    cfg, r = traced(crowd=CrowdTuning(start="grid", frozen=True), mj=MJPolicy(bodies="none"), **kw)
    L = r["trace"]["listeners"]
    f = svg.Floor(260, 0, 0, pad=14)
    body = [f.room()]
    vals = [l[metric] for l in L]
    vmax = max(vals) or 1
    k = 0.85 / 4
    for l in L:
        x0, y0 = f.xy(l["x"] - k / 2, l["y"] + k / 2)
        x1, y1 = f.xy(l["x"] + k / 2, l["y"] - k / 2)
        step = min(6, max(0, int(l[metric] / vmax * 6 + 0.5)))
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"><title>%s %.2f</title></rect>'
                    % (x0, y0, x1 - x0 - 1, y1 - y0 - 1, svg.SEQ[step], metric, l[metric]))
        body.append('<text x="%.1f" y="%.1f" font-size="7" text-anchor="middle" fill="%s">%.2f</text>'
                    % ((x0 + x1) / 2, (y0 + y1) / 2 + 2.5, "#ffffff" if step >= 4 else "#0b0b0b", l[metric]))
    body.append(f.room().replace(svg.GRID, svg.MUTED))
    tr = r["trace"]
    pts = [tr["ships"][s][0] for s in range(len(tr["ships"]) - 64, len(tr["ships"]))]
    body.append(f.path(pts, svg.SHIP[0], 2))
    save(name, svg.wrap(260, 270, "".join(body), title))
    return r


if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    if "traj" in which or "all" in which:
        trajectories("traj_bare", "Bare orbit, no bodies: 2 ships, bars 40-48",
                     "no bodies: the ships circle", ships=2, seed=3, mj=MJPolicy(bodies="none"))
        trajectories("traj_plan", "Plan start values with guest groups: bars 40-48",
                     "gravity 0.02, cap 1.5: ships fall into the groups", ships=2, seed=3)
        trajectories("traj_lab", "Lab tuning, gravity cap = steering cap: bars 40-48",
                     "cap 0.3: bends and slings, back to the path", ships=2, seed=3,
                     flight=FlightTuning(**LAB))
        trajectories("traj_labdef", "Lab defaults + hold/double: bars 40-48",
                     "stiff steer, cap = steer; holds and doublings", ships=2, seed=3,
                     flight=FlightTuning(gravityMax=0.6, captureRadius=0.3, steerStiffness=2.5, steerDamping=1.6, steerMax=0.6),
                     mj=MJPolicy(hold=8, speedMove=2.0))
        trajectories("traj_plan4", "Plan as written, four ships: bars 40-48",
                     "gravity 0.02, cap 1.5, 4 ships", ships=4, seed=3)
        trajectories("traj_escort", "Lab tuning + escort rotation: bars 40-48",
                     "ship 1 escorts a group 8 bars, patrols 8", ships=2, seed=3,
                     flight=FlightTuning(**LAB), mj=MJPolicy(escort="rotate"))
    if "map" in which or "all" in which:
        perception_map("map_perceived", "Where a 4-bar orbit is heard (share of time)", "perceived",
                       ships=1, bars=24, flight=FlightTuning(wanderRadius=0))
        perception_map("map_bored", "Where it is heard but habituated", "bored",
                       ships=1, bars=24, flight=FlightTuning(wanderRadius=0))


def frames(name, title, bars, trail_bars=2, size=170, **kw):
    cfg, r = traced(**kw)
    tr = r["trace"]
    per_bar = int(cfg.bpb / cfg.sampleBeats)
    W = len(bars) * (size + 6)
    body = []
    for i, b in enumerate(bars):
        f = svg.Floor(size, i * (size + 6), 0, pad=8)
        body.append(f.room(label_front=(i == 0)))
        body.append(f.people(tr["crowd"][b], by_fatigue=True, r=1.5))
        body.append(f.bodies(tr["bodies"][b], label=False))
        a, z = max(0, (b - trail_bars) * per_bar), b * per_bar
        for ch in range(cfg.ships):
            body.append(f.path([tr["ships"][s][ch] for s in range(a, z)], svg.SHIP[ch], 1.8))
            X, Y = f.xy(*tr["ships"][z - 1][ch])
            body.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="%s" stroke="%s" stroke-width="1.5"/>' % (X, Y, svg.SHIP[ch], svg.SURF))
        esc_ = [o for o in tr["orders"][b] if o[0] == 1]
        body.append('<text x="%.1f" y="%d" font-size="10" text-anchor="middle" fill="%s">bar %d%s</text>'
                    % (i * (size + 6) + size / 2, size + 12, svg.INK2, b, " · escort" if esc_ else ""))
    body.append(svg.legend_ships(cfg.ships, 8, size + 28))
    body.append('<circle cx="%d" cy="%d" r="2" fill="%s"/><text x="%d" y="%d" font-size="9" fill="%s">tired listener</text>'
                % (8 + cfg.ships * 52 + 6, size + 28, svg.DANGER, 8 + cfg.ships * 52 + 12, size + 31, svg.INK2))
    save(name, svg.wrap(W, size + 36, "".join(body), title))
    return r


def heat(name, title, bars, **kw):
    cfg, r = traced(**kw)
    save(name, svg.heat_series(r["trace"], bars, title))
    return r


if __name__ == "__main__" and ("frames" in sys.argv[1:] or "all" in sys.argv[1:]):
    frames("frames_lab", "Four frames of a set: lab tuning, closed loop, escort rotation",
           [12, 24, 40, 60], ships=2, seed=2, flight=FlightTuning(**LAB), mj=MJPolicy(escort="rotate"))
    frames("frames_four", "Four ships at once: the floor tires",
           [12, 24, 40, 60], ships=4, seed=2, flight=FlightTuning(**LAB))
    heat("heat_loop", "Crowd density over a 64-bar set, closed loop (bodies shown)",
         [8, 16, 24, 32, 40, 48, 56, 63], ships=2, seed=2, flight=FlightTuning(**LAB))
    heat("heat_none", "Crowd density, the same set with no bodies",
         [8, 16, 24, 32, 40, 48, 56, 63], ships=2, seed=2, flight=FlightTuning(**LAB), mj=MJPolicy(bodies="none"))


def azimuth_series(cfg, r, ch=0, from_bar=16, to_bar=40, step=2):
    tr = r["trace"]
    per_bar = int(cfg.bpb / cfg.sampleBeats)
    a, z = from_bar * per_bar, to_bar * per_bar
    out, prev = [], None
    for s in range(a, z, step):
        x, y = tr["ships"][s][ch]
        ang = math.degrees(math.atan2(y, x))
        if prev is not None:
            d = (ang - prev[1] + 180) % 360 - 180
            ang_u = prev[0] + d
        else:
            ang_u = ang
        prev = (ang_u, ang)
        out.append(ang_u)
    base0 = out[0]
    return [v - base0 for v in out]


if __name__ == "__main__" and ("azimuth" in sys.argv[1:] or "all" in sys.argv[1:]):
    series = []
    for label, kw in (("bare orbit", dict(mj=MJPolicy(bodies="none"))),
                      ("gravity (cap)", dict()),
                      ("hold + double", dict(mj=MJPolicy(hold=8, speedMove=2.0))),
                      ("breath", dict(mj=MJPolicy(hold=1, holdBeats=1)))):
        cfg, r = traced(ships=2, seed=2, flight=FlightTuning(**LAB), **kw)
        series.append((label, azimuth_series(cfg, r)))
    n = min(len(s) for _, s in series)
    series = [(l, s[:n]) for l, s in series]
    xs = [16 + i * 2 * 0.25 / 4 for i in range(n)]
    save("azimuth_time", svg.line_chart(series, "Ship 1 azimuth over 24 bars (degrees travelled)", "bar", "degrees travelled round the room", xs=xs, xticks=[16, 20, 24, 28, 32, 36, 40]))

    zoom = []
    for label, kw in (("bare orbit", dict(mj=MJPolicy(bodies="none"))),
                      ("breath", dict(mj=MJPolicy(bodies="none", hold=1, holdBeats=1)))):
        cfg, r = traced(ships=2, seed=2, flight=FlightTuning(**LAB), **kw)
        zoom.append((label, azimuth_series(cfg, r, from_bar=24, to_bar=28, step=1)))
    n = min(len(s) for _, s in zoom)
    zoom = [(l, s[:n]) for l, s in zoom]
    xs = [24 + i * 0.25 / 4 for i in range(n)]
    save("azimuth_zoom", svg.line_chart(zoom, "The breath, 4 bars close up", "bar", "degrees travelled", xs=xs,
                                        xticks=[24, 25, 26, 27, 28]))


if __name__ == "__main__" and ("final" in sys.argv[1:] or "all" in sys.argv[1:]):
    trajectories("traj_final", "Recommended set: cap rule + breath every bar, bars 40-48",
                 "cap = steer 0.3; each ship stops on beat 4 of every bar", ships=2, seed=3,
                 flight=FlightTuning(**LAB), mj=MJPolicy(hold=1, holdBeats=1))
    frames("frames_final", "Four frames of the recommended set (cap rule, breath every bar, closed loop)",
           [12, 24, 40, 60], ships=2, seed=2, flight=FlightTuning(**LAB), mj=MJPolicy(hold=1, holdBeats=1))
    trajectories("traj_gate", "Breath + gravity only on beat 1, half mass: bars 40-48",
                 "bends land on the one; the path stays wide and fast", ships=2, seed=3,
                 flight=FlightTuning(pulseMode="gate", **LAB), mj=MJPolicy(hold=1, holdBeats=1, massScale=0.5))
