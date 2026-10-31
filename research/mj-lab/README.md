# MJ Lab: a simulated dance floor for moving sound

How should sound fly through the A³ dome so that a dance floor follows it, and does not get bored or
dizzy? One night (2026-10-08) of simulation answered that as far as a model can: a virtual floor, a
crowd of listener agents who hear through a perception model built from the psychoacoustics
literature ([motion perception](../../knowledge/spatial/motion-perception.md)), and A³ Motion's
gravity flight ("ships" flying around "bodies", the guest groups) ported to Python.

**It is a model, not evidence.** The crowd's hearing comes from published research; its boredom,
fatigue and drift are hypotheses. Every ranking was re-run under 18 different listener assumptions
(worse hearing, stronger side penalty, faster fatigue, other crowd sizes and speaker layouts) and is
only reported as robust where it held across them. The listening test in
[motion perception](../../knowledge/spatial/motion-perception.md#c-listening-test-one-evening-at-the-system)
is what decides.

## What came out

- [`report.html`](report.html) — the full report with figures, open it in a browser.
- [`mj-defaults-from-lab.md`](mj-defaults-from-lab.md) — the recommended defaults, one row per setting.
- The rules for a performer or an automatic motion jockey went into
  [the MJ playbook](../../knowledge/spatial/mj-playbook.md).
- [`log.md`](log.md) — the lab log, round by round (rounds 0–53), with every hypothesis, result and
  refinement in the order they happened.

The headline results: cap gravity at what a ship can steer back (`gravityMax ≤ steerMax`) or every
ship parks over a group; let moving sounds *breathe* (stand still on beat 4 of every bar, restart on
the one); fly two ships, not four; move a band of 6–8 kHz at 2 octaves (or 3 kHz at 4), never narrower
than one octave.

## Files

| File | What |
|---|---|
| `flight.py` | port of A³ Motion's phase-2 gravity flight (tuning, gravity, pulse, rabbit, ship step, escort) |
| `hearing.py` | how one listener hears a moving band in the dome; every constant names the research row it rests on |
| `crowd.py` | listener agents: hear, get engaged, bored or tired, drift on the floor |
| `mj.py` | the motion-jockey policies (moves, holds, doublings, the breath, adaptive and learning MJs) |
| `sim.py` | one seeded, fixed-step run: `nice -n 19 python3 sim.py` |
| `lab.py` | seeded sweeps over conditions, two worker processes, results to `results/<round>.json` |
| `rounds.py` | the named experiment rounds |
| `go.py` | run rounds by name: `nice -n 19 python3 -u go.py [--seeds N] <round> …` (a name ending in `*` runs every round with that prefix) |
| `robust.py` | tabulates whether a ranking keeps its sign across the listener variants |
| `check_flight.py`, `diag_map.py` | sanity checks of the flight port and the dome mapping |
| `figs.py`, `svg.py` | the figures in `figs/` (SVG) |
| `report.py`, `report_lib.py` | build `report.html` from `results/*.json` and `figs/*.svg` |
| `preview.sh`, `shot.sh` | render SVGs to PNG / screenshot a page with headless Firefox, for checking figures |
| `results/` | raw results of every round (JSON) and the printed summaries (`*.txt`) |
| `figs/` | trajectories, perception maps, crowd heat series, frame strips |
| `mockups/` | overlay mockups for A³ Motion's MJ (OFF / HINT / FLY) and the guest groups, drawn the same night |

Python 3 standard library only; seeded, so the same configuration gives the same numbers. A full
round takes minutes to an hour on two cores. Run it niced, never beside a live set on the same
machine.

## Licence

Code GPL-3.0-or-later; log, report, results, figures and mockups CC-BY-SA-4.0 (see `.reuse/dep5`).
