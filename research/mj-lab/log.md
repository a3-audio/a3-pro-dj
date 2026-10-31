# MJ Lab log

Virtual experiment: how sound movement in the A³ dome attracts (or tires) listeners.
Model, not evidence. Ran on the rig's audio machine under `nice -n 19`, at most 2 worker processes
(it shares the machine with the live audio). No OSC, no audio, no services.

## 2026-10-08 02:37:01 CEST — start

- Read: dj-pro skill, knowledge/spatial/motion-perception.md, fpv-phase-2-plan.md, flight/*.cc (read only).
- Earliest end: start + 4 h.

## 2026-10-08 02:45:11 CEST — round 0: port and sanity

- Ported flight (plan Tasks 1-7; FlightTuning/gravityAt/gravityPulse/rabbitAt match the C++ in the worktree).
  stepShip/FlightWorld/escort written from the plan text (not yet in C++).
- check_flight.py with plan start values:
  - empty room, no wander: the ship runs **0.19 (mean) / 0.24 (max) behind and inside the rabbit**. A PD steer
    without acceleration feed-forward has a steady error a_c/kSteer; the plan's Task-4 test (< 0.1) would fail.
  - a mass-2 group at 0.25 bends the closest approach from 0.47 to 0.35 (bends: yes).
  - **escort collapses**: target circle 0.21, the ship sits at 0.024-0.029 from the group (gravity beats steerMax
    inside ~0.25 for mass 1, ~0.4 for mass 3). Seen from the room that is "parked" (research B2).
- One 64-bar run = ~7 s single core. Sweeps use 2 workers under nice.

## 2026-10-08 02:45:11 CEST — round 1a: gravity with plan start values (6 seeds, 2 ships, 64 bars)

- H: guest groups as bodies make the motion more varied and more attractive than the bare orbit.
- Result: the opposite with plan values. No bodies: perceived 93 %, boredom 0.61 (circling is perceived but
  habituated). Any bodies: perceived **6-10 %**, turnStd 145-500 deg/beat: ships fall into the groups and spin in
  the softening core, i.e. they park overhead. Engagement 0.17 -> 0.01.
- Refinement: gravity must bend, not capture. Next: sweep G and the steer limits.

## 2026-10-08 02:48:59 CEST — round 2: where gravity stops capturing (6 seeds each)

- G sweep (plan steer): 0.02 capture (perceived 0.10); 0.008 half the seeds capture (0.62 ± 0.35);
  0.004 and below: same as no bodies (perceived 0.91-0.93, boredom 0.55-0.60). **A cliff, not a slope**: no
  value of G gives "bends but does not capture". Stiffer steering moves the cliff only a little.
- Larger softening (0.2) makes it worse (wider capture basin).
- **gravityMax = steerMax = 0.3** (plan G 0.02): perceived 0.80, boredom **0.29** (half of the bare orbit),
  events 1.27/listener/bar, turnStd 20 deg/beat. The cap is the lever: a ship can be pulled hard but never
  harder than it can steer back.
- Next: sweep gravityMax below steerMax, and re-run escort under the cap.

## 2026-10-08 03:11:23 CEST — model fix + round 3/4 + round 5 (lab tuning: gravityMax = steerMax = 0.3)

- **Model fix**: the dome mapping now ports HeightMap::mapTo3D (polar angle linear in floor radius, reach 0.5:
  room edge at 26° elevation) instead of an orthographic hemisphere. Rounds 2-3 re-run on it; same picture.
- Added metric bottomQuarter (mean engagement of the 25 % least served listeners: "does everyone get something").
- Round 3, gravityMax 0.1 … 0.4: boredom falls steadily (0.62 → 0.35 at 0.3), perceived falls (0.90 → 0.81),
  at 0.4 capture is back (perceived 0.48). Engagement stays flat (0.152-0.157): what gravity adds in surprise,
  it takes in salience — the ship goes over the crowd, where a 3 kHz band's motion is mostly elevation, which
  the model (Langendijk & Bronkhorst) hears poorly.
- Round 4 controls: silence → grouped 0.67; ships but the crowd ignores them → 0.76; default → 0.84; walk ×3 →
  0.95 (largest group 0.93). The crowd does follow the sound in the model, and following concentrates it.
- Round 5 (2 ships, closed loop, 6 seeds):
  - speed: lap 4 bars best (eng 0.152). 2 bars 0.137 (fatigue 0.26). 1 bar −0.03 (ships cannot keep up:
    speedMax 0.9 < 1.1 needed; 4.3 events/bar → overload). 8 bars 0.092 (perceived only 0.51). → research B1 default holds.
  - ships: 1 → 0.096 (perceived 0.55), **2 → 0.152**, 3 → 0.140 (fatigue 0.18), 4 → 0.073 (fatigue 0.37,
    bottom quarter < 0). Fatigue is an assumption of the model → robustness check pending.
  - pulse: **no effect**. Beat wobble of a ship's azimuth: 3.1° off, 3.7° plan, 3.7° at 3× depth. The plan's
    pulse moves a ship by < 1° per beat; research B5 needs 20-30°. The pulse is not audible as a beat.
  - band: 6-8 kHz 2 oct 0.205-0.207 > 3 kHz 4 oct 0.191 > 3 kHz 2 oct 0.152 > 1 kHz / 250 Hz ~0.095 >
    3 kHz 1 oct 0.084 > 0.5 oct 0.016. Width matters more than centre; ≥ 2 oct with energy above 4 kHz.

## 2026-10-08 03:16:29 CEST — round 5 gravity + round 6: MJ moves (paired by seed vs lab baseline, 6 seeds)

- r5 gravity: no bodies 0.156 / bottom quarter 0.129 / boredom 0.68; closed loop 0.152 / 0.099 / 0.35;
  static 0.153 / 0.096 / 0.31; escort 0.131 / 0.078 / 0.14 (fatigue 0.12). Dead zones never fired (no group
  got tired enough). Gravity trades boredom for fairness: ships go where the groups are, loners get less.
- Lab extensions to the flight (not in the plan): integrated rabbit phase with a per-ship rate (double, halve,
  reverse on a bar line), holds (ship stands still for a bar, rabbit runs on), a velocity kick on the one.
- r6 paired Δ engagement (± SE, seeds up):
  - hold 1 bar in 4: **+0.021 ± 0.006 (5/6)**, boredom −0.31, fatigue +0.065
  - double speed 2 bars in 8: **+0.016 ± 0.002 (6/6)**, bottom quarter +0.024 (6/6) — the most robust gain
  - hold 1 bar in 8: +0.013 ± 0.006 (4/6)
  - halve 2 bars in 8: −0.010; counter-rotation −0.019 (ships meet head-on twice a lap, separation throws them off)
  - kicks .4-.8 on the one: −0.04 … −0.10 (fatigue +0.08 … +0.31): too much
  - escort rotation: −0.021 (fatigue +0.06)
- Reading: contrast moves in TIME (stop, double) beat contrast moves in SPACE (kicks, escort) in this model.
  Next: smaller kicks, escort variants, mass, band × gravity, combos.

## 2026-10-08 03:24:17 CEST — round 7: band × gravity, small kicks, escort variants, mass, combos (6 seeds)

- band × gravity: with 3 kHz/2 oct the bodies cost a little (0.156 → 0.152); with 8 kHz/2 oct they gain
  (0.198 → 0.207). The elevation reading holds: gravity pulls ships over the crowd, where only a band with
  6-12 kHz moves audibly.
- kicks .15-.25 every 2-8 bars: all slightly worse than none (−0.004 … −0.022). Spatial jolts do not pay here.
- escort: every variant worse except a **wide capture (0.3, i.e. 0.52 for a mass-3 crowd)**: 0.153 vs 0.152,
  bottom quarter better (0.109). Narrow escorts park (research B2: ≥ 30°).
- mass ×0.5: engagement equal, bottom quarter 0.114 (better), boredom 0.55 (worse). ×2: worse.
- **combo hold 1 bar in 8 + double 2 bars in 8: 0.186** (+0.034 vs baseline); **with 8 kHz/2 oct 0.236**;
  the same moves without bodies 0.171. Moves in time + a high wide band + bodies is the best set so far.

## 2026-10-08 03:36:57 CEST — round 8 (robustness, first half) + new code for rounds 9-15

- r8: 8 core conditions × 4 seeds, re-run under changed listener assumptions; robust.py tabulates whether each
  ranking keeps its sign (paired vs reference). First 7 variants:
  - always held: 2 ships > 1; lap 4 > lap 8; 8 kHz/2 oct > 3 kHz/2 oct; 2 oct > 1 oct; bodies cut boredom.
  - fragile: 2 ships > 4 fails when hearing is worse (MAMA ×1.4: more ships make up for missed motion);
    lap 4 > lap 2 fails with worse hearing / stronger side penalty / weak habituation (faster laps are heard more);
    "bodies cost the least served" flips in 3 of 7.
- New code: set programmes (policy changes by phrase), a dive band (switch FREQ to 8 kHz while a ship is over a
  group), rounds r9 (steering + cap ratio, 128-bar sets, ship count with moves), r10 programmes, r11 move
  robustness, r13 dive band, r14 tempo, r15 elevation reach.

## 2026-10-08 03:48:14 CEST — round 8 complete: which rankings survive (14 listener variants × 8 conditions × 4 seeds)

| claim | held |
|---|---|
| 2 ships beat 1 | 14/14 |
| lap 4 bars beats lap 8 | 14/14 |
| 8 kHz/2 oct beats 3 kHz/2 oct | 14/14 |
| 2 oct beats 1 oct | 14/14 |
| bodies cut boredom | 14/14 |
| 2 ships beat 4 | 12/14 (fails: MAMA ×1.4, fatigue ×0.5) |
| bodies cost the least served | 11/14 |
| lap 4 bars beats lap 2 | **8/14** — fragile: worse hearing, a stronger side penalty, weak habituation, half fatigue or other crowd sizes favour lap 2 |

- dt 1/128 (the plan's tick) vs 1/64: every ranking identical, values within 0.003. The cheaper step is fine.
- Refinement: "lap 4 vs lap 2" is a toss-up the model cannot settle; the robust statement is "not 1 bar, not 8".
  That fits the move result: cruise at 4 bars, double to 2 bars for 2 bars in 8. Listening test block 1 decides.

## 2026-10-08 03:51:11 CEST — round 9: steering, cap ratio, 128-bar sets

- Stiffer steering (2.5 / 1.6 / steerMax 0.6) with the cap at 0.3 / 0.45 / 0.6 / 0.8 = ratio 0.5 / 0.75 / 1 / 1.33
  of steerMax: engagement 0.155 / 0.160 / **0.164** / 0.085 (capture returns at 1.33, perceived 0.56).
  **The rule is the ratio**, not a number: gravityMax ≤ steerMax, and right at it is best.
- Stiff steering also fixes the plan's tracking error (0.19 → 0.06 behind the rabbit).
- 128-bar sets: hold+double stays best (0.192; with 8 kHz 0.245). Over a long set the crowd concentrates more with
  bodies (largest group 0.88 vs 0.75 without): the rich-get-richer loop is slow but real in the model.
- Next: r10 programmes, r13 dive band, r14 tempo, r15 reach, r11 move robustness, r16 DJ effects, r17 shootout.

## 2026-10-08 03:59:11 CEST — rounds 9-15: ship count with moves, programmes, dive band, tempo, reach (6 seeds)

- Ship count with hold+double on: 1 → 0.144, **2 → 0.186**, 3 → 0.095, 4 → −0.093 (fatigue 0.68). Moves add
  events, so the cost of every extra moving ship rises: two is even more clearly the number.
- Programmes (136 bars): constant hold+double 0.194 > alternate 1/2 ships 0.177 > baseline 0.156 > phrase
  programme (intro lap 8 with 1 ship, groove, peak, stop-start break) 0.142 > alternate 2/3 ships 0.134.
  Limit: the model has no song structure, so it cannot reward a build-up; it only scores steady state.
- Dive band (3 kHz, switch to 8 kHz over a group): +0.006 over plain 3 kHz; 8 kHz always is +0.050;
  3 kHz at 4 oct +0.043. Choose a high or wide band and keep it; switching only over groups buys little.
- Tempo: at 174 BPM lap 4 bars 0.181 vs lap 2 −0.067 (4.7 events/bar); at 100 BPM lap 2 0.162 vs lap 4 0.149.
  The best cruise is an angular speed, not a bar count: ~50-75 °/s. Lap 2 bars below ~110 BPM, 4 bars above.
- Elevation reach of the path (HeightMap reach): 0.3 → 0.140, 0.4 → 0.169, 0.5 → 0.186, 0.6 → 0.196,
  0.7 → 0.201. A lower path (more azimuth, less zenith) is heard better; the plan's default 0.5 is fine,
  0.6-0.7 is better.

## 2026-10-08 04:03:44 CEST — round 11: do the moves survive other listeners? (4 seeds per variant)

- hold+double vs baseline: +0.024 … +0.042 (4/4 seeds) under weak/strong habituation, MAMA ×1.4, side factor 8,
  crowd 120; **−0.026 (0/4) when fatigue is twice as fast**. With 8 kHz: +0.074 … +0.097, again negative under
  fatigue ×2.
- the plan's cap (1.5): −0.10 … −0.25 in every variant (0/4 seeds anywhere). The capture verdict is the most
  robust result of the night.
- Refinement: the moves are only as good as the floor's stamina, which nobody has measured. Idea: a closed-loop
  MJ that pauses holds and doublings while mean fatigue > 0.12 (resumes < 0.06). Round 18 tests it.

## 2026-10-08 04:07:17 CEST — round 16 (DJ effects) and round 18 (closed-loop MJ)

- Effects on the 2nd ship for 2 bars in 16 (on top of hold+double), paired vs none: all slightly negative.
  ping-pong step every beat −0.008, every 2 beats −0.017, **full glide every 2 beats −0.028** (a step reads better
  than a glide, as research B6 says), swirl 1 lap/beat −0.013, 1 lap/2 beats −0.019. (A 1/16-bar glide equals a
  step at this sample rate.) Effects are seasoning, not a source of attention, in this model.
- Adaptive MJ with calm thresholds 0.12/0.06: hedges the fast-fatigue floor (0.121 vs hold+double 0.098,
  baseline 0.119) but gives away most of the gain on the default floor (0.154 vs 0.186): the default floor sits at
  fatigue ~0.14 with the moves on. Thresholds too low. Round 18b: 0.2/0.12 and 0.25/0.15.

## 2026-10-08 04:11:18 CEST — round 17: shootout, plan as written vs lab defaults (12 seeds, 96 bars)

| | engagement | bottom quarter | perceived | boredom | fatigue |
|---|---|---|---|---|---|
| A plan as written, 4 ships | −0.016 | −0.041 | 0.15 | 0.07 | 0.13 |
| B plan as written, 2 ships | 0.008 | 0.000 | 0.10 | 0.16 | 0.03 |
| C bare orbit, no bodies | 0.159 | 0.130 | 0.91 | 0.60 | 0.04 |
| D plan + cap rule | 0.157 | 0.104 | 0.82 | 0.38 | 0.05 |
| E lab flight (stiff steer, cap = steer, wide escort) | 0.162 | 0.108 | 0.86 | 0.45 | 0.04 |
| F E + hold/double | 0.191 | 0.140 | 0.89 | 0.14 | 0.15 |
| G F + 8 kHz/2 oct | **0.242** | **0.189** | 0.94 | 0.13 | 0.19 |

- The plan as written is the only configuration worse than a bare circle: parked ships. Each lab step adds.

## 2026-10-08 04:14:53 CEST — round 18b: fatigue-threshold MJ, refined; round 19 queued: a learning MJ

- Thresholds 0.2/0.12 and 0.25/0.15: on the default floor they keep most of the gain (0.178 / 0.183 vs 0.186),
  but on the fast-tiring floor they do not hedge any more (0.075 / 0.095 vs baseline 0.119). 0.12/0.06 hedged that
  floor but threw away the gain on the default one. **A fixed fatigue threshold cannot do both**: the floors differ
  in their resting fatigue, and the MJ does not know which floor it has.
- Refinement: let the MJ learn instead. r19: every 8 bars it picks "moves on" or "off", scores the floor's mean
  reward over the second half of the block, keeps the better, explores 25 %. 96-bar sets, 5 listener variants.

## 2026-10-08 04:19:27 CEST — round 19: a learning MJ (96 bars, 6 seeds, 5 listener variants)

| floor | baseline | hold+double always | learning MJ |
|---|---|---|---|
| default | 0.154 | **0.188** | 0.179 |
| fatigue ×2 | **0.119** | 0.091 | 0.110 |
| fatigue ×0.5 | 0.168 | **0.232** | 0.213 |
| habituation weak | 0.253 | **0.278** | **0.278** |
| habituation strong | 0.109 | **0.148** | 0.137 |

- Worst case against the best choice for that floor: baseline −0.064, always-on −0.028, **learning −0.019**.
  Always-on is best on average (0.187 vs 0.183); learning is the hedge for a floor nobody has measured.
- 96 bars is only ~11 blocks of 8 bars to learn in. r20: 192-bar sets, 8-bar vs 4-bar blocks.

## 2026-10-08 04:21:32 CEST — pictures and report draft

- figs.py: trajectories (bare, plan, lab, escort, lab defaults, plan with 4 ships), perception maps (frozen grid),
  crowd heat series (closed loop vs none), four-frame strips (escort set; four ships), azimuth-over-time chart.
  Checked by rendering with headless Firefox (ImageMagick's SVG renderer drops long paths).
- report.html built by report.py from results/*.json + figs/*.svg; light/dark tokens, phone width checked at 390 px
  (wide tables scroll inside their box). Defaults table generated from mj-defaults-from-lab.md.
- Code for r21 (DJ-placed body scenes × cap) and r23 (move cadence: hold beats, hold period, doubling period).
  Regression check: hold+double seed 1 reproduces r7 exactly (0.21274).

## 2026-10-08 04:26:31 CEST — round 20: the learning MJ over 192 bars

- default floor: always 0.198, learning 0.188 (8-bar blocks) / 0.186 (4-bar, explore .15), none 0.157.
- fatigue ×2: none 0.122, always 0.092, learning 0.111 / 0.115. habituation strong: always 0.152, learning 0.141 / 0.138.
- Longer sets do not make it learn much better: the floor's reward is a noisy signal over a block (ships, groups
  and the other ship all move it). The learning MJ stays a hedge (worst case −0.011 vs −0.030 for always-on),
  not a winner. Shorter blocks with less exploring: no real difference.
- Queued r24: plan / plan+cap / lab flight / lab+moves / bare orbit under all 14 listener variants.

## 2026-10-08 04:30:59 CEST — rounds 21 (DJ-placed scenes) and 23 (move cadence), 6 seeds

- r21, bodies tapped in by hand (crowd still listening): the plan's cap captures in **every** scene (heard
  3-48 %, engagement ≤ 0.03). cap = steer (0.3): 0.159 (one hotspot at the centre), **0.200 (three groups spread
  out)**, 0.197 (crowd + dead zone on the path), 0.173 (eight mixed). Stiff steering with cap 0.6: a little lower
  everywhere (0.151-0.189) — it returns ships to the path sooner, so more boredom. Stiff steering fixes tracking but
  is not a gain in itself: keep it optional.
- Several modest bodies spread over the floor beat one heavy one (0.200 vs 0.159): bends from several directions.
- r23 cadence, paired vs no moves: **hold the last 2 beats of every 4 bars: +0.030 (6/6), fatigue only +0.028** —
  the best single move and the cheapest. Hold 1 bar/16: nothing. Doubling 2 bars/16, 1 bar/4, 4 bars/16: +0.014 …
  +0.019. Combo ref (hold 1 bar/8 + double 2/8): +0.034 at fatigue +0.079.
- Next r25: around "hold 2 beats / 4 bars" (1 beat, 2-bar periods, with doublings).

## 2026-10-08 04:42:37 CEST — round 24: does the shootout order survive the 14 listener variants? (64 bars, 4 seeds)

| claim (paired engagement) | held |
|---|---|
| plan + cap beats plan as written | **14/14** (+0.10 … +0.25) |
| lab flight (stiff steer, cap = steer) beats plan + cap | 12/14 (small: +0.000 … +0.024) |
| lab flight beats the bare orbit | 9/14 — gravity alone is a wash for engagement |
| hold + double beat no moves | 11/14 (fails: side factor 2.5, weak habituation, fatigue ×2) |
| lab + moves beats the bare orbit | 11/14 |

- The ordering the report recommends is robust where it matters (never the plan's cap) and honest where it is
  not (gravity alone does not win attention; moves depend on how fast a floor tires and how quickly it habituates).

## 2026-10-08 04:44:33 CEST — round 25: the breath (6 seeds, paired vs no moves)

- **Hold 1 beat every 2 bars ("the breath": the ship stops on beat 4 of every second bar, restarts on the one):
  +0.034 ± 0.009 (6/6), fatigue only +0.009** — as good as hold-1-bar-in-8 + double-2-in-8 (+0.034, fatigue
  +0.079) at a ninth of the fatigue. Hold 2 beats/2 bars: too much (+0.016, fatigue +0.093). Hold 1 beat/4 bars:
  +0.020, fatigue +0.004. Hold 2 beats/4 bars + double 2/16: +0.036, fatigue +0.052.
- Short, frequent stops on the last beat are the cheapest attention in the model: a small gap that the
  1-s velocity window registers as a stop and a start, both on the grid.
- Next: r26, does the breath survive all 18 listener variants (it should, if fatigue was the weak point of the
  combo); r27, a final 12-seed shootout with it.

## 2026-10-08 04:55:58 CEST — round 8b: four more listener variants (speaker layout, facing)

- Speakers 8 ring only, 16+8; listeners facing the centre, facing anywhere (their drift direction).
- Every core claim keeps its sign in all four, including lap 4 > lap 2. Totals over 18 variants: 2 > 1 ships
  18/18, lap 4 > 8 18/18, 8 kHz > 3 kHz 18/18, 2 oct > 1 oct 18/18, bodies cut boredom 18/18, 2 > 4 ships 16/18,
  lap 4 > 2 12/18, bodies cost the least served 13/18.

## 2026-10-08 04:59:34 CEST — round 26: the breath under all 18 listener variants (4 seeds each)

- **Breath vs no moves: positive in 18 of 18 variants, in every seed (72/72)**, +0.003 … +0.048, fatigue
  +0.002 … +0.059. It survives fatigue ×2 (+0.028), where hold+double loses (−0.026, 0/4).
- hold+double: positive in 16/18, lost under fatigue ×2 and side factor 2.5; fatigue +0.04 … +0.17.
- Verdict: the breath (stop on beat 4 of every second bar, restart on the one) is the most robust move of the
  night and becomes the recommended default beat link.

## 2026-10-08 05:06:18 CEST — round 27: final shootout (12 seeds, 96 bars)

| | engagement | bottom quarter | heard | boredom | fatigue |
|---|---|---|---|---|---|
| P plan as written | 0.008 | 0.000 | 0.10 | 0.16 | 0.03 |
| C bare orbit | 0.154 | 0.130 | 0.93 | 0.70 | 0.03 |
| D plan + cap rule | 0.157 | 0.104 | 0.82 | 0.38 | 0.05 |
| D + breath | 0.196 | 0.127 | 0.84 | 0.14 | 0.07 |
| D + breath + double 2/16 | 0.204 | 0.134 | 0.86 | 0.10 | 0.11 |
| D + breath, 3 kHz/4 oct | 0.244 | 0.173 | 0.87 | 0.13 | 0.08 |
| **D + breath, 8 kHz/2 oct** | **0.262** | **0.192** | 0.90 | 0.12 | 0.10 |
| D + hold/double, 8 kHz/2 oct | 0.243 | 0.189 | 0.94 | 0.13 | 0.19 |

- The recommended set: plan flight + cap rule + the breath + a high or wide band. Plain plan steering is enough.

## 2026-10-08 05:09:39 CEST — round 28: the shape of the breath (6 seeds, paired vs no moves)

- both ships together on beat 4 every 2nd bar +0.034; staggered (ships alternate bars) +0.024; stopping on the one
  instead of beat 4 +0.032; one ship only +0.014; **every bar +0.056 (fatigue +0.025)**; breath + double 2/16 +0.041.
- Ships with the breath: 1 → 0.113, **2 → 0.186**, 3 → 0.157, 4 → 0.048. Two ships again.
- Next r29: denser gates — half-beat stops, beats 2 and 4 — to find where the breath turns into a stutter.

## 2026-10-08 05:11:11 CEST — round 29: where the breath turns into a stutter (6 seeds)

- one beat on beat 4 every bar: **+0.056 (6/6), fatigue +0.025**; every 2nd bar +0.034; half a beat every bar
  +0.024; beats 2 and 4 every bar −0.002; half-beats on 2 and 4 +0.002 (boredom up: a regular stutter is just
  another steady pattern). With 8 kHz/2 oct: +0.118.
- The stop has to be long enough to be integrated (one beat = 476 ms at 126 BPM; half a beat = 238 ms is under the
  ~336 ms of Chandler & Grantham) and rare enough to stay an event (once a bar, not twice).
- Next: r30 robustness of the every-bar breath (18 variants), r31 tempo (100 / 126 / 174 BPM).

## 2026-10-08 05:13:23 CEST — round 31: the breath across tempo (6 seeds, paired vs no moves)

- 1-beat stop every bar: +0.054 (100 BPM), +0.056 (126), +0.042 (174), 6/6 seeds each; half-beat stops +0.017 …
  +0.029; 2-beat stops every 2nd bar fall to −0.004 at 174 BPM (fatigue +0.14). One beat on the grid works from
  100 to 174 BPM.

## 2026-10-08 05:23:33 CEST — round 30: the every-bar breath under 18 listener variants (4 seeds)

- **Breath every bar vs no moves: positive in 18/18 variants and 72/72 seeds**, +0.022 … +0.075, fatigue
  +0.007 … +0.115; better than the every-2nd-bar breath in 17/18 (not with side factor 2.5).
- Recommended beat link from here on: one beat of stillness on beat 4 of every bar, restart on the one.
- Next: r32, the final 12-seed shootout with it.

## 2026-10-08 05:29:04 CEST — round 32: final shootout with the every-bar breath (12 seeds, 96 bars)

| | engagement | bottom quarter | heard | boredom | fatigue |
|---|---|---|---|---|---|
| P plan as written | 0.008 | 0.000 | 0.10 | 0.16 | 0.03 |
| C bare orbit | 0.154 | 0.130 | 0.93 | 0.70 | 0.03 |
| D plan + cap rule | 0.157 | 0.104 | 0.82 | 0.38 | 0.05 |
| D + breath every 2nd bar | 0.196 | 0.127 | 0.84 | 0.14 | 0.07 |
| D + breath every bar | 0.217 | 0.141 | 0.86 | 0.07 | 0.09 |
| D + breath every bar, 3 kHz/4 oct | 0.266 | 0.189 | 0.88 | 0.07 | 0.10 |
| **D + breath every bar, 8 kHz/2 oct** | **0.282** | **0.205** | 0.91 | 0.05 | 0.12 |
| … + double 2 bars in 16 | 0.267 | 0.188 | 0.92 | 0.04 | 0.18 |

- Recommended set confirmed: the plan's flight with gravityMax = steerMax, the breath on every bar, two ships,
  8 kHz/2 oct (or 3 kHz/4 oct). A doubling on top now costs more than it brings.
- Next r33: with the breath on, do the planets still matter? (no bodies / closed loop / three placed groups /
  lighter masses / a wide 4-bar escort; 3 kHz and 8 kHz.)

## 2026-10-08 05:31:17 CEST — round 33: with the breath on, do the planets still matter? (6 seeds)

| | 3 kHz/2 oct | 8 kHz/2 oct |
|---|---|---|
| breath, no bodies | **0.260** | **0.332** |
| breath, three groups placed by hand | 0.225 | 0.298 |
| breath, closed loop, masses ×0.5 | 0.230 | 0.300 |
| breath, closed loop | 0.208 | 0.270 |
| breath, closed loop + wide escort 4/16 | 0.194 | 0.249 |

- **Once the ships breathe, the planets cost more than they give in this model.** The breath already removes the
  boredom gravity was meant to remove (boredom 0.05-0.07 with or without bodies); what gravity still does — pull
  ships over the crowd, where motion becomes overhead motion, and serve groups over loners — is all cost here.
- This turns the night's question round and needs care: it rests on the model's elevation-cue assumption
  (Langendijk & Bronkhorst) and on scoring the whole floor. Robustness check queued (r34, 18 variants).

## 2026-10-08 05:38:24 CEST — round 34: planets vs no planets with the breath, 18 listener variants (4 seeds)

- No bodies beat the closed loop in **18/18 variants, 72/72 seeds** (+0.028 … +0.075); half masses beat full
  masses in 18/18 (+0.019 … +0.043).
- But none of the 18 variants touches the assumption the result leans on: that overhead motion of a band is hard to
  hear. r35 removes it (elevation heard exactly like azimuth, verticalPenalty and the 6-12 kHz rule switched off).

## 2026-10-08 05:43:20 CEST — rounds 35-36: why do the planets cost with the breath on?

- r35: hearing overhead motion exactly as well as horizontal motion changes nothing: no bodies still ahead
  (8 kHz: 0.338 vs 0.277). The elevation assumption is not the cause.
- r36: switching off precedence + off-centre blur, proximity loudness, fatigue, or all of them plus perfect overhead
  hearing: no bodies stays ahead in 6/6 seeds every time (+0.027 … +0.066). The cost is not in the ears.
- Diagnosis from the paths: with bodies the ships fly slower (median 0.35 vs 0.47 floor units/beat) and further in
  (median radius 0.69 vs 0.85). Climbing out of a well with a capped steer costs speed; the planets act as brakes and
  pull the path in towards the zenith. Less angle per second for most of the floor.
- r37: can the planets be useful? Repelling groups, gravity only on beat 1, lighter masses.

## 2026-10-08 05:44:53 CEST — round 37: can the planets be useful? (breath on, 8 kHz/2 oct, 6 seeds, vs no bodies)

- closed loop −0.062; masses ×0.5 −0.032; ×0.25 −0.013; groups that repel −0.037; **gravity only during beat 1
  of each bar −0.017; on beat 1 at half mass −0.009** (0/6 up everywhere: no form of gravity beats none here).
- The beat-1 gate keeps the bends (turn variation 23.5 vs 20.9 deg/beat for the always-on loop, radius spread 0.099
  vs 0.076 without bodies) at a sixth of the cost, and the bends now land on the one — the beat link the breathing
  pulse could not give. If the planets are wanted as a gesture, this is the form that costs least.
- r38: is that robust across the 18 listener variants?

## 2026-10-08 05:53:11 CEST — round 38: gated planets across the 18 listener variants (breath on, 4 seeds)

- vs no bodies: gravity on beat 1 at half mass −0.002 … −0.014 (ahead only at 140 BPM, +0.004); always-on closed loop
  −0.028 … −0.075. The gate is about eight times cheaper in every variant, but never free.
- Final position: no bodies is the model's optimum; if the DJ wants planets (and the plan does — it is the gesture),
  gate them to beat 1 and halve their masses, and the cost is about 2 % of the engagement.
- Next: r39 recommended set, 12 seeds; r40 192-bar sets.

## 2026-10-08 05:57:04 CEST — round 39: the recommended set (12 seeds, 96 bars)

| | engagement | bottom quarter | heard | boredom | fatigue |
|---|---|---|---|---|---|
| P plan as written | 0.008 | 0.000 | 0.10 | 0.16 | 0.03 |
| C bare orbit, 8 kHz | 0.195 | 0.166 | 0.96 | 0.70 | 0.05 |
| breath, no bodies, 8 kHz | **0.337** | **0.254** | 0.96 | 0.05 | 0.10 |
| **R: cap rule + breath + planets gated to beat 1 at half mass, 8 kHz** | 0.329 | 0.246 | 0.95 | 0.04 | 0.11 |
| R, 3 kHz/4 oct | 0.314 | 0.228 | 0.93 | 0.05 | 0.09 |
| R, 3 ships | 0.174 | 0.100 | 0.98 | 0.01 | 0.41 |

- The recommended set keeps the planets (the maintainer's concept) at a cost of 0.008 against none, and is 40 times
  the plan as written. Three ships tire the floor (fatigue 0.41).

## 2026-10-08 05:58:42 CEST — round 40: 192-bar sets (6 seeds)

- breath, no bodies 0.350; recommended set 0.344; plan + cap without moves 0.157. No drift: fatigue stays at
  0.10-0.11 over 192 bars, boredom at 0.03-0.04.
- Over 192 bars the model's crowd ends up as one group (largest 0.93-0.96) in every condition, bodies or not: the
  walking-towards-the-sound rule concentrates it. That is the crowd model, not the MJ; a real floor has walls,
  bars and friends. Flagged as a limit.
- Next r41: the recommended set at 100 / 174 BPM, crowds of 40 / 120, a uniform start (6 seeds).

## 2026-10-08 06:01:38 CEST — round 41: the recommended set in other rooms (6 seeds)

- plan as written / bare orbit 8 kHz / recommended 8 kHz: 100 BPM 0.008 / 0.197 / 0.317; 174 BPM 0.008 / 0.204 / 0.265;
  crowd 40 0.013 / 0.197 / 0.321; crowd 120 0.006 / 0.198 / 0.319; uniform start 0.027 / 0.209 / 0.289.
  The order holds everywhere; at 174 BPM the margin shrinks (fatigue 0.145).

## 2026-10-08 06:04:03 CEST — round 42: the price of the gated planets, 24 seeds

- recommended set vs the same without bodies: engagement −0.0069 ± 0.0007 (0/24 seeds up), least-served quarter
  −0.008, boredom −0.011, fatigue +0.012. About 2 % of the engagement, in every seed: small, real, and the price of
  keeping the maintainer's planets.

## 2026-10-08 06:05:36 CEST — round 43: lap length with the recommended set (6 seeds)

- With the breath on, a 2-bar lap is bad at every tempo: 100 BPM 0.063 vs 0.317 (lap 4), 126 BPM 0.059 vs 0.323;
  fatigue 0.42 — after each stop the ship sprints to catch a fast rabbit. At 174 BPM lap 4 (0.265) beats lap 8 (0.209).
- Refinement of the lap rule: **with the breath, 4 bars at every tempo tried (100-174 BPM)**. "2 bars below ~110 BPM"
  only held for a ship that never stops.

## 2026-10-08 06:06:52 CEST — round 44: path height with the recommended set (6 seeds)

- reach 0.4 → 0.290, 0.5 → 0.323, 0.6 → 0.337, 0.7 → 0.345 (fatigue 0.10 → 0.15; least-served quarter 0.18 → 0.28).
  The low path holds with the breath and gated planets too; the gain is mostly at the edges of the floor.

## 2026-10-08 06:08:04 CEST — round 45: hand-placed scenes with the recommended set (gated, half mass, 6 seeds)

- vs no bodies: one hotspot −0.004, three groups −0.007, crowd + dead zone −0.009, eight mixed −0.015 (0/6 up each);
  bend activity rises in the same order (+0.7 … +5.1 deg/beat). With the gate the cost simply follows how much the
  bodies bend: few bodies are cheap, eight are not. The earlier "spread beats one heavy" (r21) was for always-on
  gravity without the breath.

## 2026-10-08 06:14:55 CEST — round 46: the recommended set across all 18 listener variants (4 seeds)

- vs a bare circle in the same 8 kHz band: +0.062 … +0.175, **18/18 variants, 72/72 seeds**.
- vs the plan as written: +0.250 … +0.449, 18/18, 72/72.

## 2026-10-08 06:16:05 CEST — round 47: escort as a gesture inside the recommended set (4 bars in 16, 6 seeds)

- vs the set without escorts: capture radius 0.15 (plan) −0.030 (0/6), 0.3 −0.014, **0.45 −0.006 (2/6 up)**.
  The wider the escort orbit, the closer to free; at the plan's radius it parks. Escort stays a gesture with a price.

## 2026-10-08 06:17:25 CEST — round 48: does the beat-1 gate need the cap? (6 seeds)

- Recommended set with gravityMax 0.3 / 0.6 / 1.0 / 1.5: 0.323 / 0.322 / 0.322 / 0.322 — no difference.
- Plan values (cap 1.5, full mass, no breath) with only the gate added: 0.168 vs 0.006 as written, motion heard 89 %.
- **Gating gravity to beat 1 alone also prevents capture**: three free beats a bar let the steer pull every ship out.
  The cap rule and the gate are two independent fixes; the defaults keep both (belt and braces).

## 2026-10-08 06:22:07 CEST — round 49: the gate as the smallest possible fix (18 variants, 4 seeds)

- The plan exactly as written plus only pulseMode = gate, vs as written: +0.101 … +0.301, 18/18 variants, 72/72 seeds.
  If the maintainer changes one thing in FlightTuning, the gate (or the cap rule) is it.

## 2026-10-08 06:23:17 CEST — round 50: a crowd that starts packed in front of the booth (6 seeds)

- plan as written −0.000, bare orbit 8 kHz 0.203, recommended 0.290, breath without bodies 0.295. Same order as
  everywhere else; the gated planets cost 0.005 here.

## 2026-10-08 06:24:19 CEST — round 51: call and response (recommended set, 6 seeds)

- Regression check after the last code change: hold+double seed 1 still 0.21274.
- vs both ships stopping on beat 4: ship 2 stopping on beat 2 instead **+0.006 (6/6), fatigue −0.014**; on beat 3
  +0.004 (6/6). Small but consistent: one ship breathes on the 4, the other on the 2 — the floor always has one
  ship moving, and each restart is still on a beat.

## 2026-10-08 06:28:55 CEST — round 52: call and response across the 18 listener variants (4 seeds)

- 4-and-2 vs both on 4: −0.003 … +0.030, ahead in 14/18 variants and 62/72 seeds. A small, mostly robust
  refinement — an option, not a rule.

## 2026-10-08 06:30:20 CEST — round 53: band choice inside the recommended set (6 seeds)

- 6 kHz/2 oct 0.322, 8 kHz/2 oct 0.323, 5 kHz/3 oct 0.323, 3 kHz/4 oct 0.309, 3 kHz/2 oct 0.252, 8 kHz/1 oct 0.235.
  Anything centred at 5-8 kHz with ≥ 2 octaves is equivalent; width matters more than the exact centre.

## 2026-10-08 06:35:02 CEST — end

- Start 02:34:55, end 06:35:02: just over 4 hours. 4852 seeded runs in 50 rounds (r1-r53, results/*.json).
- Deliverables: mj-playbook.md (v2), report.html (built by report.py), mj-defaults-from-lab.md, figs/*.svg, this log.
- Strongest findings: (1) the plan's gravity cap captures every ship — fix with gravityMax = steerMax or gate gravity
  to beat 1; (2) the breath (one beat of stillness on beat 4 of every bar) is the most robust attention move;
  (3) once ships breathe, planets cost (they brake the ships) — keep them light and gated; (4) 2 ships, lap 4 bars,
  low path, 5-8 kHz at ≥ 2 oct; (5) the breathing gravity pulse is inaudible as a beat.
- A model, not evidence: the listening test in the research note (part C) plus the items in report section 12 decide.
