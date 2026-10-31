# MJ playbook — how an automatic motion jockey moves sound on the A³ dome

v2, 2026-10-08 (final, 06:10). Written from [motion perception](motion-perception.md) (v1, 02:58), then checked against the MJ Lab simulation
([`report.html`, `log.md`](../../research/mj-lab/)). Where the sim confirmed, refuted or refined a rule, it says so.

Tags: **[R: …]** = from the research note (the row it rests on); **[practice]** = club/stage practice;
**[MJ hypothesis]** = my own rule; **[sim ✓]** = the MJ Lab model supports it across its robustness checks;
**[sim ✗]** = the model contradicts it; **[sim ~]** = the model cannot settle it. The sim is a model, not a
listening test.

The one fact behind every rule: the crowd does not study the motion, it notices it. A move that has to be
listened for is a move that did not happen.

## 1. Speed

1. **Cruise at one lap per 4 bars.** Without stops the best cruise is ~50-75 °/s (2 bars below ~110 BPM); once the ships
   breathe (rule 18), 4 bars at every tempo, because a fast rabbit turns every restart into a sprint. [sim ✓ r43]
   [R: B1, MAMA ~5° front] [sim ✓ against 8 bars and 1 bar in 18/18 listener variants]
2. **One lap per bar is the ceiling for a path**, and only with a wide band above 3 kHz. [R: Roggerone 2019]
   [sim ✓: at 1 bar the ships cannot keep up (speedMax) and the floor gets 4 events a bar]
3. **Faster than one lap per 2 beats is an effect, not a path** — swirl, Leslie, tremolo. Use it for 1-2 bars, never
   as the cruise. [R: Féron 2010] [sim: a swirl costs a little, like every effect]
4. **Slower than one lap per 8 bars is a drift**, not motion. [R: Saberi 1990 + B1] [sim ✓: half the floor misses it]
5. **A speed change must be ×2 to be heard as faster, ×½ as slower.** Double or halve; never nudge.
   [R: Carlile & Best; Locke 2016] [sim ✓ for doubling (6/6 seeds); halving hurt in the model]

## 2. The band (FREQ / Q of the 3D filter)

6. **Move the top of the mix: 6-8 kHz at 2 oct, or 3 kHz at 4 oct.** [R: B4, Yost & Zhong, Langendijk & Bronkhorst]
   [sim ✓: 8 kHz/2 oct > 3 kHz/2 oct in 18/18 listener variants; caveat: the sim does not know the track's spectrum]
7. **Never narrower than 1 octave** for a move that should be followed. [R: Yost & Zhong 2014, Roggerone 2019]
   [sim ✓ 18/18: 1 oct loses ~45 % of the engagement, ½ oct ~90 %]
8. **Never move anything below ~250 Hz as a path; avoid centres at or below 1 kHz.** [practice: 4DSOUND, Rex Club]
   [sim ✓: 250 Hz and 1 kHz bands scored ~0.6 of 3 kHz]
9. **Elevation moves need 6-12 kHz in the band.** When gravity takes a ship over the crowd, the band needs that
   energy or the dive is silent. [R: Langendijk & Bronkhorst 2002] [sim ~: built into the model, but r35 showed it is not what makes the planets
   cost; the 8 kHz band wins for front/back and width, not for elevation alone]
10. **Pick a high or wide band and keep it**; switching FREQ up only while a ship is over a group buys little.
    [sim ✓, MJ hypothesis refuted in its strong form]
11. **A narrow high band sits at its own height** — do not try to move it vertically. [R: Middlebrooks 1992]
12. **The narrower or lower the band, the slower the ship.** [R: B1/B4 coupling]

## 3. How much moves at once

13. **Two ships move; the rest wait.** [practice: 4DSOUND "less becomes far more"] [sim ✓ again with the breath: 3 ships fatigue 0.41]
    [sim ✓: 2 > 1 in 18/18 variants, 2 > 4 in 16/18; with holds and doublings on, a third ship already tires the floor]
14. **Never turn several ships the same way at the same speed** (vection). [R: Väljamäe 2009]
    [sim ~: no vection at 1 lap / 4 bars; counter-rotation itself cost a little because ships meet head-on]
15. **No more than one audible event per ship per 2 beats.** [MJ hypothesis — it is built into the model's fatigue,
    so the sim cannot test it; it is the main thing a listening test must check]

## 4. When to bend, when to hold still

16. **A bend that should be heard must leave the path by ≥ 30°** as seen from the floor. [R: Grantham 1986; B2]
17. **The beat link is a move on the one, not gravity breathing.** If gravity is on, gate it to beat 1 of the bar:
    the bends then land on the one and cost a sixth as much. [sim ✓ r37] The plan's pulse moves a ship by < 1° per beat;
    20-30° is needed. [R: B5] [sim ✓: no effect at any depth or rhythm tried]
18. **Breathe: every moving ship stands still for beat 4 of every bar and restarts on the one.** A short stop on
    the grid makes the restart an event for the whole floor. One whole beat (it must outlast the ~336 ms the ear
    integrates over), once a bar (twice is a stutter), both ships together. [MJ hypothesis; practice: L-ISA "random
    throws that stop"; R: Chandler & Grantham for the length] [sim ✓, the most robust move of the night: positive in
    18/18 listener variants and all 72 of their seeds, 100-174 BPM; every 2nd bar is the gentler variant]
18a. **Two ships: call and response.** Ship 1 breathes on beat 4, ship 2 on beat 2. [sim ✓, small: +0.006, 6/6 seeds, less fatigue]
18b. **For a floor with stamina: hold the last bar of 8 and double for 2 bars in 8.** Less gain than the every-bar breath
    (+0.034 vs +0.056), three times the fatigue. [sim ✓ on 16/18 variants; lost when the floor tires twice as fast]
19. **Do not circle for more than a few laps unchanged.** A steady orbit is heard and then tuned out.
    [MJ hypothesis — the maintainer's fear] [sim ✓: bare orbit boredom ~0.7, the highest of any condition]
20. **Ease off when the floor tires.** [MJ hypothesis] [sim ~: a fixed fatigue threshold cannot serve floors that tire
    at different rates; an MJ that learns (moves on/off per 8 bars, keep what scores) is a hedge, never the best.
    The breath made this rule mostly unnecessary: it is cheap enough to leave on.]
21. **No kicks on the one.** A velocity impulse towards a group adds events and fatigue faster than interest.
    [sim ✗ for the MJ hypothesis "kick on the downbeat"; every size tried did worse]

## 5. Bodies (guest groups) and escort

22. **Gravity must bend, never park.** The pull of the groups is never stronger than the ship's steering back:
    `gravityMax ≤ steerMax`, best right at it. [sim ✓, the most robust result: the plan's cap 1.5 loses in every
    seed of every listener variant]
23. **Bending halves boredom but does not, on its own, win the floor — and with the breath on, it costs.** Use the
    groups to say *where* the sound goes, keep them light (half the plan's masses) and spread; let the breath do the
    anti-boredom work. [sim ✓ r33-r38, 18/18 listener variants; not caused by the ears (r35-r36) but by the paths: the
    wells brake the ships and pull them in. Gated to beat 1 at half mass, the planets cost ~2 % (r42)]
24. **Escort wide or not at all**: the escort orbit must subtend ≥ 30° from the people escorted. At the plan's radius
    (0.15·√m) the ship parks overhead. [R: B2] [sim ✓: 0.3·√m breaks even, 0.15 loses]
25. **Escort is a DJ gesture, not a routine.** [sim ✓: every automatic escort rotation did worse than patrol]
25b. **Few planets.** With the recommended gate, each extra body adds bends and costs a little: one costs −0.004, eight −0.015 (r45). [sim ✓]
26. **Do not feed the biggest group forever.** Groups pull ships, ships serve groups, the least-served quarter
    loses (13/18 variants). Lighter masses (×0.5) give the edges back at the price of some boredom. [sim ✓]
27. **Dead zones are for steering around, not for punishing.** [MJ hypothesis; the sim never produced one]
28. **Fly the big path low** (elevation reach 0.6-0.7): azimuth is heard better than height. [R: Saberi 1990] [sim ✓, weak]

## 6. Stereo DJ effects, translated

29. **Auto-pan L↔R → a step between two opposite points**, ½-2 beats per side. A step reads better than a glide.
    [R: B6, Chandler & Grantham] [sim ✓ step > glide; but every effect cost a little: accents, not routines]
30. **Auto-pan circle → rotation**, 1 lap per 1-4 bars; 1 lap per beat only as a swirl. [R: B1]
31. **Filter sweep → FREQ sweep of the moving band while it orbits** (the band climbs). 4-16 bars. [R: Lee 2015; G]
32. **Riser → elevation climb + doubled rotation every 4 bars + high FREQ**, 8-16 bars; **drop → snap to front or
    static on the 1.** [R + G; the hold-and-restart result (18) supports the "snap on the 1" half]
33. **Echo throw → throw the return to the opposite side and let it drift back over 1-2 bars.** Needs its own path.
    [G; not in today's routing]
