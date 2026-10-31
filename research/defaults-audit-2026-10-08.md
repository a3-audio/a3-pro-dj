# Defaults audit and the Space set (2026-10-08)

A review of the A³ system's defaults from the DJ's side, one table per device: what each value is,
whether to keep it, and why. Written by the pro-DJ role on 2026-10-08, with the research in
[motion perception](../knowledge/spatial/motion-perception.md) (cited as **B1…B6**) and the
[movement lab](mj-lab/) as its basis. File and line references are to the A³ repositories as of that
day and will drift.

**Source column:** **research** = derived from the research (tag R); **DJ practice** = what a CDJ/DJM or
common DJ software does (*verify* where it was from memory; the CDJ-3000 rows have since been checked,
see [CDJ-3000](../knowledge/gear/cdj-3000.md)); **guess-test** = needs the listening test or a measurement.

**Verdict:** **keep** · **change** (implemented in a3-motion-ui) · **propose**
(for the maintainer) · **measure** (cannot judge before the band filter's Hz/octave measurement, C0, or
a measurement on the system).

**Outcome:** the speed-key change and the Space set were reviewed and merged (a3-motion-ui, 2026-10-08).
Everything marked *propose* or *measure* was handed to the maintainer; check the repositories for what
became of each.

## A³ Motion (a3-motion-ui)

| Setting | Where | Current | Verdict | Proposed | Source |
|---|---|---|---|---|---|
| **Speed keys, fresh device** | `src/a3-motion-ui/SettingsPersistence.hh:61` | `{0, -3, -4, -6}` → on the first, one-bar take: 1 bar, ½ beat, ¼ beat, 1/16 beat per lap = 180 / 1440 / 2880 / 11 520 °/s at 120 BPM | **change** (done) | `{2, 1, 0, -1}` → 4 bars, 2 bars, 1 bar, 2 beats = 45 / 90 / 180 / 360 °/s. A settings file that exists but has no `speedButtons` still gets the old four (legacy courtesy kept). | research: B1, Féron 2010 (UL ≈ 900 °/s), Carlile & Best 2002 (≥ 2× to hear faster). Three of the old four were above the limit where a room hears direction. A configured device's own settings already read `[2, -4, -1, 0]`: the performer had moved away from −3 and −6 by hand. |
| Speed keys on a configured device | the device's own settings file (not in git) | e.g. `[2, -4, -1, 0]` | keep | — the performer's habit; −4 is a deliberate effect key on a one-bar take (¼ beat lap = flutter). Code default does not touch it. | DJ practice |
| First take length | `src/a3-motion-ui/SessionFile.hh:76` (`recordLengthLog2 = 0`) | 1 bar | keep | — recording by hand is quick at one bar; the new speed keys then play it at 4 bars. | DJ practice (a 1-bar loop is the default on a CDJ's auto-beat-loop *verify*) |
| Clip `speedLog2` | `src/a3-motion-engine/ClipSettings.hh:64` | 0 (as recorded) | keep | — | — |
| Clip `elevationBase` | `ClipSettings.hh:107`, `pattern/clips/system/Default.json` | 0 = north pole (overhead) | **propose** (not changed: files that omit the field would change meaning) | `Default.json` only: 0.45 (just above ear level). A figure at the pole sweeps tiny arcs; azimuth movement near the zenith is mostly below the MAMA. | research: B2/B3 (elevation weakest, ≥ 30° excursion), Grantham 1986 |
| Clip `reach` | `ClipSettings.hh:96` | 0.5 | keep | — | guess-test |
| Clip `envelopeAttack/Decay` | `ClipSettings.hh:123–124` | 2 / 3 = ¼ bar / ½ bar | keep | — on the bar grid, accent lands with the beat. | DJ practice |
| Clip `envelopeMax` (3d ceiling) | `ClipSettings.hh:125` | 1.0 | keep | — | — |
| Clip `fadeReach` | `ClipSettings.hh:158` | 0 | keep (open question) | — the 0.25 guess still waits for its hand test. | guess-test |
| TempoLfo table (spin, swell, sway, sweeps) | `src/a3-motion-engine/TempoLfo.hh` (`lfoBarsPerCycle`) | 32 … ¼ bar per cycle, steps 1…8 | keep, **propose a soft warning** | Steps 7–8 (½, ¼ bar per turn = 720 / 1440 °/s added) are effects; a dimmer key colour above step 6 would say so without forbidding it. | research: B1 |
| Envelope steps | `src/a3-motion-engine/Envelope.hh:45ff` | 1/16 … 4 bars | **propose** | Add 8 and 16 bars (steps 7–8): the research's riser is 8–16 bars (B6); today the longest is 4. Needs the action table and the ACTION page to grow. | research: B6 |
| FREQ / Q / 3D step per detent and per finger step | `src/a3-motion-ui/components/A3MotionUIComponent.cc:1867` | 0.02 (50 steps over the range) | **measure** | Decide after C0: if 0.02 of FREQ is more than ⅓ octave, go to 0.01 for FREQ only. | guess-test |
| Mixer step per detent | `A3MotionUIComponent.cc:8984` | 0.02 | keep | — | — |
| FREQ default (shipped sets) | `pattern/sessions/system/*.json` | 0.35 – 0.6 (mostly 0.45) | **measure** | Target ≈ 3 kHz centre; Space uses 0.55 as a guess. Map after C0. | research: B4 |
| Q default (shipped sets) | same | 0.05 – 0.3 | **measure** | Target ≈ 2 octaves wide; never narrower than 1 oct. Space uses 0.05 (the widest any set uses). | research: B4, Yost & Zhong 2014 |
| FREQ/Q → Isolator3 | `a3-core/.../a3-core.py:923–931` | linear 0.05…0.9 for both | **measure** (C0) | Once Hz/oct are known: a log-in-Hz FREQ map so a detent is the same musical step everywhere. | research: B4 |
| Tap tempo: taps needed | `src/a3-motion-engine/tempo/TempoEstimator.hh:53` | 2 taps give a tempo | **propose** | 4 (one bar) before the tempo is taken; 2 taps is one interval, ±1 tap-jitter of 20 ms = ±5 BPM at 120. Keep "first tap is the downbeat". | DJ practice (DJM tap averages several taps *verify*) + guess-test |
| Tap timeout | `TempoEstimator.hh:55` | 2 s | keep | — (30 BPM floor) | — |
| Meter ballistics | `src/a3-motion-engine/MeterBallistics.hh:41–47` | attack 0, release 20 dB/s, hold 1.5 s | keep | — slightly livelier than IEC 60268-18 (20 dB in 1.7 s ≈ 12 dB/s), right for a booth. Decided system-wide 2026-10-07. | DJ practice |
| Rec mode, clock mode | `SettingsPersistence.hh:41–46` | Touch, internal | keep | — | — |

### FPV gravity flight (the phase-2 flight plan's `FlightTuning`; branch `feat/fpv-gravity`, not on main at the time)

Proposals only; the flight is not on main and is another session's branch.

| Constant | Plan value | Verdict | Proposed | Source |
|---|---|---|---|---|
| `orbitLapBars` | 4 | keep | — 45 °/s at 120, the research default path | research: B1 |
| `orbitPrecessionBars` | 32 | keep | — "the room drifts", inaudible alone, fine as variety | research: B1 |
| `orbitRadius`, `orbitEccentricity` | 0.7, 0.2 | keep | — | guess-test |
| `speedMax` | 0.9 floor units/beat | keep, **add an angular cap** | At r = 0.7 this is ≈ 74 °/beat (147 °/s at 120): fine. Near the centre the same linear speed is many times the angular speed; cap the *angular* speed at 180 °/beat (1 lap per 2 beats) and at 90 °/beat when the channel's FREQ is low. | research: B1 |
| Slingshot gain (test `ACloseFlybySlingsTheShipOut`) | > 1.2× | **propose** | ≥ 2×, or accept that a sling is heard as a bend, not as speed | research: B1 (Carlile & Best; Locke 2016) |
| `captureRadius` × √mass | 0.15 | **propose** | ≥ 0.25 for a body at r ≈ 0.5, so the escort orbit subtends ≥ 30° | research: B2 |
| `captureLapBars` | 2 | keep | — | research: B1 |
| `wanderRadius` | 0.12 | keep | — ≈ ±10° at the path radius: "life", not a wobble | research: B2 |
| `pulseDepth` / `pulseDownbeatDepth` | 0.3 / 0.6 per beat | **propose** | Pulse on half bars or bars; keep the downbeat accent; log the per-beat angular deviation in a test and require ≥ 20–30° if it is meant to be heard | research: B5 (Chandler & Grantham 336 ms) |
| `gravity`, `gravityMax` | 0.02, 1.5 | **propose** (lab, interim) | `gravityMax = steerMax = 0.3`: the lab log (round 2, 02:48) finds that with the plan values ships fall into a group and park (perceived motion 6–10 %); capping gravity at what the ship can steer back gives perceived 80 % and half the boredom of the bare orbit. No value of G alone works (a cliff, not a slope). | lab simulation (`mj-lab/log.md`) |
| `steerStiffness` (no feed-forward) | 0.6 | **propose** (lab, interim) | The ship trails the rabbit by 0.19–0.24 in an empty room; the plan's Task-4 test (< 0.1) would fail. Add the rabbit's acceleration as feed-forward. | lab simulation |
| `maxFlightBodies` | 8 | keep | — | — |
| Ships moving at once | 4 | **propose** | Default the flight to the channels with 3d above a threshold, so a quiet deck does not add a mover | research: A3 (few elements) |

---

## StemDeck (read only)

| Setting | Where | Current | Verdict | Proposed | Source |
|---|---|---|---|---|---|
| Tempo range steps | `stemdeck/Source/DeckPanel.cpp:6` | ±8 %, ±16 %, ±50 % | **propose** | ±6, ±10, ±16, WIDE | DJ practice: CDJ-3000X manual p. 78 (±6/±10/±16/WIDE, checked later) |
| Tempo range at start | `DeckPanel.cpp:133`, `DeckPanel.h:78` | ±8 % | **propose** | ±10 % (CDJ default *verify*) | DJ practice |
| Jog: seconds per turn | `Source/JogWheel.h:33` | 1.8 s (33⅓ rpm) | keep | — | DJ practice |
| AutoDJ mix length | `Source/AutoDj.h:47` | 16 bars | keep | — | DJ practice |
| Meter ballistics | `Source/MeterBallistics.h:9–11` | 0 ms / 20 dB/s / 1.5 s | keep | — same as Motion and the desk | system decision 2026-10-07 |
| Meter scale floor | `Source/MeterBallistics.h:44` | −48 dBFS | keep | — matches the desk's LED scale | — |

## The desk (a3-mixer, read only)

| Setting | Where | Current | Verdict | Proposed | Source |
|---|---|---|---|---|---|
| Channel LED thresholds | `software/scripts/a3_mixer_meters.py:41` | −36 −24 −18 −12 −9 −6 −3 0 dBFS | keep | — | DJ practice |
| Clip hold on the displays | `software/scripts/a3-mixer-set-display/display_panel.py:190` | 1.0 s | **propose** | 1.5 s, the same as the peak hold, so a clip is never gone before its hold mark | guess-test (consistency) |
| Encoder counts per click | `software/scripts/a3_mixer_encoders.py:28` | 4 (marked "not yet measured") | **measure** | count on the desk | — |
| Push hold-off | `a3_mixer_encoders.py:34` | 50 ms | keep | — | — |
| Tap flash | `software/scripts/a3_mixer_panel.py:69` | 60 ms | keep | — | — |

## beat-analyzer (read only)

| Setting | Where | Current | Verdict | Proposed | Source |
|---|---|---|---|---|---|
| BPM window | `.env.example` / `build/.env` (`BPM_MIN=60`, `BPM_MAX=140`); code default `src/app/beat_analyzer_app.cpp:229–230` (60 / 200) | 60–140 on the live system | **propose** | 75–150 (one octave, no gap) or per-night genre presets. A 150 hardtechno or 174 DnB track counts at 75 / 87 today. For motion that is fine (half-time grid), but the number disagrees with the CDJ display the DJ reads. Code default 60–200 is wider than an octave and disagrees with the `.env`. | DJ practice (rekordbox offers fixed one-octave-ish ranges such as 78–155 *verify*) |
| OSC send rate (VU) | `beat_analyzer_app.cpp:221` | 25 Hz | keep | — | — |
| VU RMS attack / release | `beat_analyzer_app.cpp:217–218` | 0.8 / 0.2 | keep | — raw peaks drive the displays now | — |
| Pro DJ Link device number | `beat_analyzer_app.cpp:394` | 7 | keep | — | DJ practice |

## Core's truth (read only)

| Setting | Where | Current | Verdict | Source |
|---|---|---|---|---|
| `meters` block | `a3-core/.../usr/share/a3/a3-osc.json:184` | attack 0 ms, release 20 dB/s, hold 1.5 s | keep | system decision 2026-10-07 |

---


## The Space set: motion a room can hear

A set of A³ Motion built to the research limits, shipped in a3-motion-ui's library.

The name is short, unlike any other set, and says what the set is for. Set it up when the room
should *hear* the movement. Every value comes from `auditory-motion-research.md`.

| Ch | Clip (shape) | Lap @ speed | 3d | Why |
|---|---|---|---|---|
| 1 | **Space Anchor** (Wander Drift) | 16 bars, reach 0.15, ear level | 0.15 | Put the deck carrying the bassline here. Under 150 Hz a club hears no direction, so this one barely moves (A2, 4DSOUND). |
| 2 | **Space Orbit** (Orbit Circle) | 4 bars = 45 °/s at 120 | 0.42 | The reference path: clear and readable from anywhere in the crowd (B1). |
| 3 | **Space Pendulum** (Orbit Pendulum) | 4 bars, a reversal every 2 | 0.36 | Swings through the room. A reversal is the clearest bend there is, a "fly-over" schema (Kendall). |
| 4 | **Space Corners** (Edge Square) | 2 bars, a 90° corner every half bar | 0.26 | Bends ≥ 30° that land on the beat grid (B2). |
| alt | **Space Lift** (Orbit Ellipse) | 4 bars, height sweeps over 16 bars, upwards | — | For the bright deck (hats, air). Elevation needs 6–12 kHz, and it moves at most half as fast as the lap (B3). Reached by A6. |

Only two channels get a clear 3d (≥ 0.3). The research's rule is "few things moving at once", and in
a DJ set usually only two decks are playing anyway.

**Buttons** (the same on all four channels; left = more, right = less):

| | more | less |
|---|---|---|
| A1/A2 | **Move Bend**: throws the figure 45° round for 2 bars. A jump rather than a glide, because short glides fall under the ear's 336 ms. | **Move Plain** (hold): strips spin and every sweep, so one path is left. |
| A3/A4 | **Lift Bright** (hold): about 30° up, with the cutoff opening. A dark band moved up is not heard moving up. | **Speed Quarter** (hold): 4× slower. Slowing down is heard more easily than speeding up. |
| A5/A6 | **FX Wide Climb** (hold): cutoff climbs over 4 bars, 3d up, Q untouched (a narrow band stops moving). | **Cue Space Lift** |

FREQ 0.55 and Q 0.05 on all four channels are a **guess** (the widest Q any set uses, a bit brighter
than Groove). They cannot be put in Hz or octaves until C0 has measured Isolator3. The tests hold
the set to the research numbers:
- every lap is a power of two between 2 and 16 bars;
- |spin| ≤ 4;
- a height sweep is ≥ 2× the lap;
- no squeeze or plane sweeps;
- at most 2 channels with a clear 3d, plus the anchor;
- every bend is ≥ 30°;
- every lap is ≥ 2 beats after any button;
- a height move is ≥ 20° and always opens the cutoff;
- no button narrows Q.

**Not verified by ear.** This is data that passes the tests, not a set anyone has listened to yet.
Smoke test:
- load Space;
- check that Anchor stays put and that Orbit and Pendulum read as paths from the edge of the room;
- check that Bend is heard as a bend and Lift Bright as up.

