# Recommended defaults from the MJ Lab (2026-10-08)

**In one line:** keep the plan's flight, set `gravityMax = steerMax`, let every moving ship *breathe* (stand still on
beat 4 of every bar), fly two ships, keep the planets light (half mass, gravity only during beat 1), and move a band of 6-8 kHz at 2 octaves (or 3 kHz at 4).

Final check of that set (12 seeds × 96 bars): engagement 0.329 against 0.008 for the plan as written and 0.195 for a
bare circle in the same band; without planets 0.337.

For the owner of `FlightTuning.hh` and the clip/MJ defaults. Source: `report.html` in this folder (a simulation,
not a listening test). Tags: **sim** = supported by the simulation across its robustness checks; **research** =
from [motion perception](../../knowledge/spatial/motion-perception.md); **guess** = neither, try it on the rig.

| Setting | Value | Plan / today | Tag | Why |
|---|---|---|---|---|
| Gravity cap | `gravityMax = steerMax` (0.3 with the plan's steering) | 1.5 | sim | At 1.5 every ship falls into the nearest group and parks overhead (motion heard 10 % of the time instead of 92 %). Equal to steerMax: bends, slings, recovers. The plan's cap lost in every seed of every listener variant (r11, r24) and in every hand-placed scene (r21). The beat-1 gate (below) is an independent fix: with it even cap 1.5 does not capture (0.168 vs 0.006, r48). Keep both. |
| Gravity strength | `gravity = 0.02` (keep) | 0.02 | sim | With the cap in place G is not the lever; without it there is a cliff between 0.004 and 0.008. |
| Softening | `softening = 0.08` (keep) | 0.08 | sim | 0.2 widens the capture basin and does worse. |
| Steering | keep `0.6 / 0.8 / 0.3`; optionally `steerStiffness 2.5`, `steerDamping 1.6`, `steerMax 0.6` with `gravityMax 0.6` | 0.6 / 0.8 / 0.3 | sim (mixed) | Plan values leave the ship 0.19 behind and inside the rabbit (the plan's own Task-4 test asks < 0.1); the stiff set gives 0.06 and passes. Engagement: stiff better in the closed loop (0.164 vs 0.152), slightly worse with hand-placed groups (it returns to the path sooner). Either way the cap must equal steerMax; at 1.33 × steerMax capture returns. |
| Lap of the big path | `orbitLapBars = 4` (keep), at every tempo when the ships breathe | 4 | sim + research | With the breath, a 2-bar lap tires the floor at 100 and 126 BPM (0.06 vs 0.32: the catch-up sprints after each stop get too fast), and 4 beats 8 at 174 BPM. Without the breath the best cruise is ~50-75 °/s, i.e. 2 bars below ~110 BPM. 4 bars beats 8 in 18/18 listener variants; 4 vs 2 is a toss-up at 126 BPM (12/18), 2 wins at 100 BPM, 4 wins clearly at 174. 1 bar outruns speedMax and the ear. |
| Height of the big path | ElevationParams `reach` 0.6-0.7 for ORBIT ships | 0.5 (clip's) | sim + research | Lower paths (more azimuth, less zenith) score better, with and without the breath: reach 0.3 → 0.140, 0.5 → 0.186, 0.7 → 0.201 (r15); with the recommended set 0.5 → 0.323, 0.7 → 0.345, mostly for the edges of the floor (r44). Vertical MAMAs are larger (Saberi 1990). |
| Beat pulse | replace the breathing pulse by a gate: gravity acts only during beat 1 of each bar (lab extension `pulseMode = gate`) | 0.3 / 0.6 breathing | sim | The breathing pulse moves a ship < 1° per beat at any depth (20-30° needed). The gate keeps the bends, lands them on the one, and costs a sixth of always-on gravity (−0.009 vs −0.062 against no bodies, breath on, 8 kHz). |
| Beat link: "the breath" | every moving ship stands still for beat 4 of every bar and restarts on the one (both ships together) | none | sim | +0.056 engagement (6/6 seeds) at fatigue +0.025; positive in 18 of 18 listener variants and all 72 of their seeds; works at 100, 126 and 174 BPM. Half-beat stops are too short (under the ~336 ms integration time); stops on 2 and 4 become a stutter. Every 2nd bar is the gentler option (+0.034, fatigue +0.009). |
| Breath, two ships | ship 1 stops on beat 4, ship 2 on beat 2 (call and response) | — | sim (small) | +0.006 over both stopping on 4 (6/6 seeds), fatigue −0.014 (r51); ahead in 14/18 listener variants, 62/72 seeds (r52). An option. Staggering whole bars instead was worse (r28). |
| Stronger moves (optional) | stand still for the last bar of 8, double the lap rate for 2 bars in 8 | none | sim (fragile) | +0.034 against the every-bar breath's +0.056, at three times the fatigue; lost when the floor tires twice as fast (16/18 variants). Only for a floor with stamina. |
| Kicks on the one | none | — | sim | Every kick size tried (0.15-0.8, every 1-8 bars) did worse: more fatigue than interest. |
| Speed changes | ×2 or ×½ only, on a bar line; prefer ×2; none by default once the ships breathe | — | sim + research | Without moves, doubling helped 6/6 seeds and halving hurt. On top of the every-bar breath a doubling cost (0.282 → 0.267, 12 seeds). Smaller changes are not heard as speed (Carlile & Best; Locke 2016). |
| Ships moving at once | 2 | up to 4 | sim (rests on the fatigue guess) | 2 > 1 in 18/18 listener variants, 2 > 4 in 16/18; with the breath 1 → 0.113, 2 → 0.186, 3 → 0.157, 4 → 0.048; with holds and doublings on, 3 and 4 ships tire the floor fast (fatigue 0.39 / 0.68). |
| Counter-rotation | not by default | — | sim | Ships meet head-on twice a lap; no vection to prevent at 1 lap / 4 bars. |
| Escort capture radius | `captureRadius = 0.3`-`0.45` (× √mass) | 0.15 | sim + research | At 0.15 the escort is a small circle near the zenith: parked. Without the breath 0.3 breaks even with patrol (r7); inside the recommended set an escort 4 bars in 16 costs −0.030 at 0.15, −0.014 at 0.3, −0.006 at 0.45 (r47). |
| Escort duty | ≤ 4 bars in 16 per ship; the DJ's gesture, not an automatic routine | — | sim | Every automatic escort rotation tried did worse than patrol. |
| Escort lap | `captureLapBars = 2` (keep) | 2 | sim (weak) | 4 bars was slightly worse. |
| Role of the planets | the DJ's way of saying *where*, not the cure for the circle; light, spread out, gated to beat 1 | the anti-boredom device | sim | Gravity halves boredom without moves, but the breath does that cheaper; with the breath on, every body setup scored below no bodies (r33-r38, 18/18 listener variants). The planets act as brakes: ships 25 % slower and further in. Gated to beat 1 at half mass they cost −0.002 … −0.014 instead of −0.028 … −0.075. |
| Body masses | G 0.5 / C 1 / H 1.5 (half the plan's) | 1 / 2 / 3 | sim | Without moves: same engagement, better for the least served. With the breath on: closed loop 0.270 → 0.300 at half mass (8 kHz), while no bodies at all scored 0.332. The planets cost attention in the model; keep them light. |
| Body placement | few bodies; with always-on gravity spread them rather than one heavy one | — | sim | Always-on, no breath: three spread groups 0.200, one central hotspot 0.159 (r21). Recommended set (gated, half mass, breath): cost vs no bodies −0.004 (one) … −0.015 (eight), rising with the amount of bending (r45). |
| Dead zones | keep as the DJ's tool; no automatic ones | −2 | guess | No group in the sim got tired enough to trigger one. |
| Moving band FREQ | 5-8 kHz at 2-3 oct (any of them), or 3 kHz at 4 oct | — | sim + research | 8 kHz/2 oct beats 3 kHz/2 oct in 18/18 listener variants; 3 kHz/4 oct is nearly as good (0.266 vs 0.282 in the final shootout); inside the recommended set 5, 6 and 8 kHz score the same (r53). The model does not know the track's spectrum: check there is energy up there. |
| Moving band Q | ≥ 2 oct; never under 1 oct | — | sim + research | 1 oct loses ~45 % of the engagement, ½ oct ~90 %. |
| FREQ floor for a path | ≥ 1 kHz centre; nothing under ~250 Hz | — | research (sim agrees) | 1 kHz and 250 Hz bands scored ~0.6 of the 3 kHz band. |
| Wander | `wanderRadius = 0.12` (keep) | 0.12 | research | ~10° per bar: "life", below a heard bend. |
| speedMax | `0.9` (keep) | 0.9 | sim | Caps the path at about one lap per bar, which is also where the ear stops following. |
