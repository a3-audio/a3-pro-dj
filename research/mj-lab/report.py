"""Build report.html from results/*.json and figs/*.svg.
    python3 report.py"""

import os
import re
import robust
from report_lib import (page, fig, chart_fig, paired_rows, mean, esc, HERE)
from lab import load, paired

T = lambda kind: {"sim": '<span class="tag sim">supported by sim</span>',
                  "res": '<span class="tag res">research</span>',
                  "guess": '<span class="tag guess">guess</span>',
                  "no": '<span class="tag no">not supported</span>'}[kind]


def m(r, c, k="engagement"):
    return mean(r, c, k)


def pd(r, ref, c, k="engagement"):
    d, se, up, n = paired(load(r), ref, k)[c]
    return "%+.3f ± %.3f, %d of %d seeds" % (d, se, up, n)


def section_header():
    return f"""
<p class="meta">A³ · MJ Lab · 2026-10-08 · a night of simulation</p>
<h1>MJ Lab</h1>
<p class="lede">How should sound fly through the A³ dome so that a dance floor follows it, and does not get bored or
dizzy? A virtual floor, a crowd that listens with a model built from the psychoacoustics literature, and the
FPV gravity flight from the phase-2 plan, run for {RUNS} seeded sets.</p>
<div class="card warn"><strong>This is a model, not evidence.</strong> Every listener in it is a handful of equations
taken from lab studies of single listeners in quiet rooms, plus rules I made up and say so. It can show what
follows from those assumptions and which design choices are fragile. It cannot show what a real floor does.
Section&nbsp;12 lists what only a listening test on the rig can decide.</div>
"""


def section_summary():
    return f"""
<h2>The short version</h2>
<ol class="finds">
<li class="find"><strong>With the plan's start values the planets eat the ships.</strong> A group pulls harder than a ship
can steer back (gravity cap 1.5 against a steering cap of 0.3), so every ship falls into the nearest group and spins a
few centimetres overhead: motion is heard {m('r2_gravity_G','G 0.02','perceived'):.0%} of the time instead of
{m('r5_gravity','no bodies','perceived'):.0%}. Turning G down does not help — there is a cliff, not a slope. The fix is a
ratio: <strong><code>gravityMax ≤ steerMax</code></strong>. Under it the same groups bend the path and let it go. This was
the most robust result of the night: the plan's cap lost in every seed of every listener variant. (Gating gravity to beat 1, finding 5, fixes it
independently: three free beats a bar let every ship climb out.)</li>
<li class="find"><strong>Bending in space halves boredom, but the planets do not buy attention — and once the ships
breathe, they cost.</strong> Under the cap, groups cut "heard but tuned out" from {m('r5_gravity','no bodies','boredom'):.2f} to
{m('r5_gravity','closed loop','boredom'):.2f} (all listener variants), yet engagement stays level and the least-served quarter
usually loses: ships go where the groups already are, and the wells act as brakes — a ship climbing out of one with a
capped steer slows down and is pulled in towards the zenith. With the breath (finding 3) doing the anti-boredom work, a set without bodies scored
{m('r33_breath_gravity','8k/2oct: breath, no bodies'):.3f} against {m('r33_breath_gravity','8k/2oct: breath, closed loop'):.3f} with the
closed loop ({GRAV_HELD}). Keep the groups as the DJ's way of saying <em>where</em>, light and spread out — not as the cure
for the circle.</li>
<li class="find"><strong>Contrast in time works: let the ships breathe.</strong> The cheapest attention in the model
is a ship that stands still for one beat — beat 4 of every bar — and restarts on the one:
{pd('r29_gate','no moves','breath every bar (beat 4)')} engagement for little fatigue
({pd('r29_gate','no moves','breath every bar (beat 4)','fatigue')}), from 100 to 174 BPM. It gained in
{BREATH_HELD} listener variants. Half-beat stops are too short to be integrated by the ear; two stops a bar become a
stutter; long holds plus doublings gain less and tire the floor several times faster. The stops sit on the grid, so
the flight stays in time.</li>
<li class="find"><strong>Two moving ships, a cruise of about 50-75 °/s, a low path, a wide band with energy above
4&nbsp;kHz.</strong> One ship is missed too often; three or four tire the floor. One lap per 4 bars; with the ships breathing
that holds from 100 to 174 BPM (a 2-bar lap then turns every restart into a sprint). A path that comes down towards the horizon is heard better than one near the zenith. 6-8&nbsp;kHz
at 2 octaves or 3&nbsp;kHz at 4 octaves; 1 octave or less, or a centre at 1&nbsp;kHz or below, loses most of the effect.</li>
<li class="find"><strong>The beat pulse is inaudible as a beat.</strong> Breathing gravity +30&nbsp;% / +60&nbsp;% moves a ship by
under one degree per beat ({m('r5_pulse','pulse off','wobbleDeg'):.1f}° → {m('r5_pulse','per beat (plan)','wobbleDeg'):.1f}° of beat
wobble); research puts a heard deviation at 20-30°. Three times the depth changes nothing. The music link the model can
hear is a move that starts on the one: the breath, or gravity switched on only during beat 1, which also makes the
planets six times cheaper (section 8f).</li>
</ol>
{recommended_box()}
<p class="meta">{RUNS} seeded runs of 64-192 bars each in {ROUNDS} rounds, 02:35-06:35 CEST. Recommended defaults: section 11.</p>
"""


def recommended_box():
    if not os.path.exists(os.path.join(HERE, "results", "r39_recommended.json")):
        return ""
    R = "R recommended: cap rule + breath + gated half-mass planets, 8k"
    return f"""<div class="card"><strong>The recommended set</strong>, in one line: the plan's flight with
<code>gravityMax = steerMax</code>, two moving ships, each standing still on beat 4 of every bar, guest groups at half
mass whose gravity acts only during beat 1, and a moving band of 8&nbsp;kHz at 2 octaves (or 3&nbsp;kHz at 4). Final check,
12 seeds × 96 bars: engagement {m('r39_recommended', R):.3f} against {m('r39_recommended', 'P plan as written'):.3f} for the plan as
written and {m('r39_recommended', 'C bare orbit, 8k'):.3f} for a bare circle in the same band; least-served quarter
{m('r39_recommended', R, 'bottomQuarter'):.3f}; fatigue {m('r39_recommended', R, 'fatigue'):.3f}. It beat the bare circle and the
plan as written in all 18 listener variants and every one of their 72 seeds (section 8f).</div>"""


def section_question():
    return """
<h2>1. The question</h2>
<p>The maintainer, on the gravity flight: ships that only go round their path sound boring, so the guest groups on
the floor should act as planets that bend, fling and capture them. The question for this night was the MJ's: <em>which
movements actually pull listeners in, which ones go unnoticed, and which ones wear a floor out?</em> And, under it, the
fear: does a gravity field really stop the circling, or does it just move the circle?</p>
<p>What I could do without touching the rig: build the floor in software, port the flight model from the plan exactly,
give each simulated guest the hearing limits the literature reports, let them walk towards what they like and away
from what tires them, let their groups become the planets, and run it many times with different seeds.</p>
"""


def section_model():
    return f"""
<h2>2. The model</h2>
<h3>The room and the flight</h3>
<p>A round floor under a dome; 8 speakers on a ring at ear height and 4 above at 45°; room edge at 6&nbsp;m
(radius 1 in floor units). Guests stand inside 85&nbsp;% of the radius. Up to four ships fly the phase-2 gravity model:
<code>FlightTuning</code>, <code>gravityAt</code>, <code>gravityPulse</code> and <code>rabbitAt</code> are ported line for
line from the C++ in <code>feat/fpv-gravity</code>; the ship step, wander, separation and escort follow the plan's text
(they were not written yet). Fixed step of 1/64 beat (1/128 checked: same results), time in beats, 126 BPM, all
randomness seeded. A ship's floor point becomes a direction exactly as <code>HeightMap::mapTo3D</code> does with
default elevation (room edge at 26°, centre at the zenith).</p>
<h3>How one guest hears a moving band</h3>
<div class="tablewrap"><table>
<tr><th>Piece</th><th>In the model</th><th>Source</th></tr>
<tr><td>Is it moving?</td><td>Angle travelled in 336&nbsp;ms and in 1&nbsp;s windows, against the minimum audible movement
angle for that speed (1.7° at 2°/s … 8.3° at 90°/s … 21° at 360°/s)</td><td>{T('res')} Perrott &amp; Musicant 1977; Saberi &amp; Perrott 1990;
Chandler &amp; Grantham 1992; Locke 2016</td></tr>
<tr><td>Where is it?</td><td>Threshold × (1 + 5·sin²) away from where the guest faces (the DJ); ×1.8 for vertical motion</td>
<td>{T('res')} Grantham 1986 (5° → 30°); Saberi 1990</td></tr>
<tr><td>Which band?</td><td>Localisation blur by width and centre (narrow and 1.5-2&nbsp;kHz worst); elevation needs
6-12&nbsp;kHz; front/back confusion without 8-16&nbsp;kHz; an upper limit of rotation that falls for low and narrow bands</td>
<td>{T('res')} Yost &amp; Zhong 2014; Mills 1958; Langendijk &amp; Bronkhorst 2002; Roggerone 2019; Féron 2010</td></tr>
<tr><td>Off centre</td><td>Blur grows with distance from centre; the precedence effect pulls the band towards the nearest speaker</td>
<td>{T('res')} Zotter &amp; Frank; Stitt 2017 — the shape and size are {T('guess')}</td></tr>
<tr><td>Habituation</td><td>A steady motion keeps 20&nbsp;% of its interest. An <em>event</em> — a turn of ≥ 45°, a speed-up ≥ 2×,
a slow-down ≥ 1.5×, a start — restores it, decaying over a bar; an event off the beat is worth 70&nbsp;%</td>
<td>{T('guess')} (the speed ratios are {T('res')} Carlile &amp; Best 2002)</td></tr>
<tr><td>Attention</td><td>The strongest moving source counts fully, the next 0.4, then 0.15, 0.05</td><td>{T('guess')}; practice: "few moving elements"</td></tr>
<tr><td>Fatigue</td><td>Rises with total moving salience above about one source, with more than one event every 2 beats,
with coherent rotation (vection) and with blur; recovers over 16 beats</td><td>{T('guess')} — no published threshold exists (Väljamäe 2009 for vection)</td></tr>
</table></div>
<p>Per sample (every 1/16 note) each guest gets <strong>engagement</strong> = attended interest × (1 − fatigue) − blur −
0.3·fatigue. That is the headline metric. Next to it: <strong>bottom quarter</strong> (mean engagement of the 25&nbsp;%
least-served guests), <strong>perceived</strong> (share of time any motion is above threshold), <strong>boredom</strong>
(share of heard time with no recent event), <strong>fatigue</strong>.</p>
<h3>How the crowd moves, and the closed loop</h3>
<p>72 guests start in three clumps plus scattered people. Each walks slowly (at most ~5&nbsp;cm/s) towards ships whose
motion it finds salient and pleasant and away from blur and fatigue, explores at random while dissatisfied, looks for
company when alone and keeps 36&nbsp;cm personal space. Every bar the automatic MJ clusters the floor (people within
0.7&nbsp;m of each other) and turns groups of 4+ into gravity bodies: 4-7 people mass 1, 8-14 mass 2, 15+ mass 3. The
ships bend towards them, the guests walk towards the ships: that is the closed loop the plan asks for.
{T('guess')} for every number in this paragraph.</p>
<div class="figs two">
{fig('map_perceived', 'A single ship on a bare 4-bar orbit, guests frozen on a grid: share of time each spot hears motion. The sides and the rim hear less (Grantham, precedence).')}
{fig('map_bored', 'The same orbit: share of heard time that is habituated. The centre hears a steady circle best — and tunes it out most.')}
</div>
<h3>Limits I know of</h3>
<ul>
<li>No real music: one band per ship with a fixed level. The model prefers high, wide bands because they localise
best; whether a track has enough energy up there is a track question.</li>
<li>No room acoustics beyond the precedence pull; no subwoofers; no visual cue from the DJ.</li>
<li>The crowd's walking and fatigue rules are invented. Section 9 changes them and checks which conclusions survive.</li>
<li>Engagement is a single number built from my own weights. Rankings matter here, not values.</li>
<li>Over long sets the model's crowd walks itself into one big group whatever the ships do; a real floor has walls,
a bar and friends. Crowd-shape results are the weakest part of the model.</li>
</ul>
"""


def section_hypotheses():
    rb = {c[0]: sum(1 for _, cells in robust.table() if cells[i][0]) for i, c in enumerate(robust.CLAIMS)}
    n = ROBUST_N
    rows = [
        ("H1", "Guest groups as gravity bodies make the motion more varied <em>and</em> more engaging than the bare orbit",
         f"More varied: yes under a cap (boredom halves, {rb['bodies cut boredom']}/{n} variants). More engaging: no, level overall; the least served lose in {rb['bodies cost the least served']}/{n}.", "no"),
        ("H1b", "With the breath on, the planets still add engagement", "No: a set without bodies scored highest in both bands; lighter, spread groups cost least", "no"),
        ("H2", "The plan's start values bend the path without capturing ships", "No: capture at G 0.02 with cap 1.5; a cliff between G 0.004 and 0.008", "no"),
        ("H2b", "Capping gravity at the steering limit gives bends without capture", "Yes, and the rule is the ratio: with stiffer steering the best cap moves with steerMax", "sim"),
        ("H3", "One lap per 4 bars beats one per 8", f"Yes ({rb['lap 4 bars beats lap 8']}/{n})", "sim"),
        ("H3b", "One lap per 4 bars beats one per 2", f"Toss-up ({rb['lap 4 bars beats lap 2']}/{n}); depends on tempo: 2 bars better at 100 BPM, far worse at 174", "guess"),
        ("H4", "Gravity breathing on every beat is heard as a beat", "No: < 1° of beat wobble at any depth tried", "no"),
        ("H5", "Pulsing on the bar or half bar is better than every beat", "No difference — none is audible", "no"),
        ("H6", "Two moving ships are better than one or four", f"2 > 1 in {rb['2 ships beat 1']}/{n}; 2 > 4 in {rb['2 ships beat 4']}/{n}; with moves on, 2 is clearly best", "sim"),
        ("H7", "A wide band (≥ 2 oct) with energy above 4 kHz moves best", f"8 kHz > 3 kHz in {rb['8 kHz/2 oct beats 3 kHz/2 oct']}/{n}; 2 oct > 1 oct in {rb['2 oct beats 1 oct']}/{n}", "sim"),
        ("H8", "Escorting a group attracts listeners", "No at the plan's radius (parks overhead); neutral when twice as wide", "no"),
        ("H9", "Stillness before the one makes the next move audible", "Yes — and shorter is better: one beat on beat 4 of every bar beats a bar-long hold (see H13)", "sim"),
        ("H10", "Speed changes help only when ≥ 2×", "Doubling helps in 6/6 seeds; halving hurts", "sim"),
        ("H11", "Closing the loop makes the floor collapse into one blob", "Slowly: over 128 bars the largest group reaches ~0.9 of the floor with bodies vs ~0.75 without; walking towards the sound does most of it", "guess"),
        ("H12", "Stereo effects translate: a ping-pong step reads better than a glide", "Step beats glide, but every effect cost a little: accents, not routines", "guess"),
        ("H13", "Short, frequent stops on the grid (the breath) beat long holds", f"Yes: one beat on beat 4 of every bar gains more than hold + double at a third of the fatigue; positive in {BREATH_HELD} listener variants", "sim"),
        ("H14", "A learning MJ (tries moves on/off, keeps what the floor rewards) is the safe default", "It is the hedge with the smallest worst case, but never the best on any one floor; the breath made it unnecessary", "guess"),
    ]
    tr = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{T(d)}</td></tr>" for a, b, c, d in rows)
    return f"""
<h2>3. Hypotheses and verdicts</h2>
<div class="tablewrap"><table><tr><th></th><th>Hypothesis</th><th>What the sim said</th><th></th></tr>{tr}</table></div>
<p class="meta">"Supported by sim" means: the predicted sign in most seeds, and it survives the listener variations of
section 9. It does not mean a floor will do it. "Not supported" means the model says no; "guess" means the model
cannot settle it.</p>
"""


def section_results():
    s = []
    s.append(f"""
<h2>4. Gravity: from capture to bend</h2>
<p>With the plan's start values the pull of a group of mass 1 is stronger than the ship's steering inside about
0.25 of the room's radius, and a crowd of mass 3 reaches 0.4 — which, with the big path at 0.56-0.84, is everywhere.
Every ship ends up on a group and circles in the softening core. Seen from the floor that is a sound parked overhead.</p>
<div class="figs two">
{fig('traj_bare', 'No bodies: two ships circle the precessing ellipse. Heard, then tuned out.')}
{fig('traj_plan', 'Plan start values with the crowd as bodies: both ships sit on group G1.')}
{fig('traj_lab', 'Lab tuning (gravityMax = steerMax = 0.3): the same crowd bends the laps and lets go.')}
{fig('traj_escort', 'Lab tuning + escort rotation: ship 1 circles the crowd for 8 bars, then patrols.')}
{fig('traj_labdef', 'Lab defaults (stiff steering, cap = steering) with hold + double: bends, stops and sprints.')}
{fig('traj_plan4', 'The plan as written with four ships: all four parked on the crowd.')}
</div>
<div class="figs one">
{chart_fig('r2_gravity_G', 'perceived', 'Share of time motion is heard, by G', 'Plan steering and cap. Between G 0.004 and 0.008 the ships go from untouched to captured.')}
{chart_fig('r3_cap', 'boredom', 'Boredom by gravity cap (G 0.02)', 'Lower is better. The cap is a smooth lever up to the steering limit (0.3); past it (0.4) capture returns.', better='lower')}
</div>
{chart_fig('r3_cap', 'perceived', 'Share of time motion is heard, by gravity cap', 'What the cap costs: the more the path bends towards the crowd, the more of it happens overhead, where a 3 kHz band is poorly heard.')}
{section_scenes()}
{chart_fig('r9_steer', 'engagement', 'The rule is a ratio: cap against steering', 'Stiffer steering (steerMax 0.6) with the cap at 0.5, 0.75, 1 and 1.33 times steerMax. Best right at 1; above it the ships are captured again.')}
""")
    s.append(f"""
<h2>5. Speed, ship count, band</h2>
<div class="figs one">
{chart_fig('r5_speed', 'engagement', 'Engagement by lap length', 'Lap 1 bar asks 1.1 floor units per beat, more than speedMax (0.9): the ships cut inside and the ear gets 4 events a bar.')}
{chart_fig('r5_ships', 'engagement', 'Engagement by ships moving at once', 'Four ships: fatigue {0:.2f}, and the least-served quarter goes negative.'.format(m('r5_ships','4 ships','fatigue')))}
{chart_fig('r5_band', 'engagement', 'Engagement by moving band (FREQ / width)', 'Width matters more than centre; energy above 4 kHz buys front/back and elevation.')}
{chart_fig('r9_ships_moves', 'engagement', 'Ship count again, with the best moves on', 'With holds and doublings the optimum stays at two ships.')}
</div>
{fig('frames_four', 'Four ships at once (lab tuning): tired guests in red. Not dizziness from speed but from too much moving at once.')}
""")
    s.append(f"""
<h2>6. The beat pulse</h2>
<p>The plan's pulse multiplies gravity by up to 1.3 on each beat and 1.6 on the one. The audible quantity is how far a
ship moves off its smooth path within a beat. Measured as the RMS of a ship's azimuth minus its one-beat moving
average: {m('r5_pulse','pulse off','wobbleDeg'):.1f}° with the pulse off, {m('r5_pulse','per beat (plan)','wobbleDeg'):.1f}° with the
plan's pulse, {m('r5_pulse','per beat x3 depth','wobbleDeg'):.1f}° at three times the depth. Research puts the threshold for a heard
deviation at 20-30° (Grantham; the research note's B2/B5). The pulse makes the bends happen a little earlier in the
beat, but nobody will hear it as a beat.</p>
{chart_fig('r5_pulse', 'engagement', 'Engagement by pulse mode', 'All within noise of each other.')}
""")
    s.append(f"""
<h2>7. MJ moves</h2>
<p>Moves the plan does not have, added to the lab's flight as switches on bar lines: a <strong>hold</strong> (the ship
stands still for the last bar of a phrase while its rabbit runs on, so it restarts on the one with a burst), a
<strong>speed move</strong> (double or halve the lap rate for 2 bars in 8), <strong>counter-rotation</strong>, a
<strong>kick</strong> (a velocity impulse towards the heaviest group on the one), and the plan's <strong>escort</strong>
in variants. Paired by seed against the lab baseline (2 ships, lap 4 bars, 3&nbsp;kHz / 2&nbsp;oct, closed loop):</p>
{paired_rows('r6_moves', 'lab baseline')}
{paired_rows('r7_combo', 'lab baseline')}
<p>Moves in time beat moves in space. A hold makes the next start an event for everyone at once, and a doubling is
the smallest speed change the ear reliably hears (Carlile &amp; Best; Locke 2016). The later cadence rounds (below)
found that the stop does not need to be long: one beat is enough. Kicks add events too, but they move
the band over the crowd and add more fatigue than interest. Halving makes motion drop below threshold at the sides.</p>
{section_cadence()}
<h3>Escort</h3>
{paired_rows('r7_escort', 'lab baseline')}
<p>The plan's capture radius (0.15·√mass) gives an orbit that, from inside the escorted group, is a small circle near
the zenith: elevation motion of a 3&nbsp;kHz band, hardly heard, and a stream of small events that tires. Doubling the
radius brings it level with patrol. Escort is a gesture for the DJ, not a free win.</p>
{fig('frames_lab', 'Four frames of a set with escort rotation (lab tuning): trails of the last 2 bars, groups as discs, tired guests in red.')}
""")
    s.append(f"""
<h2>8. The closed loop and the crowd</h2>
<p>Guests who follow the sound concentrate: with silence {m('r4_control','0 ships (silence moves nothing)','grouped'):.0%}
of the floor stands in groups of 4+, with ships they ignore {m('r4_control','2 ships, crowd ignores sound','grouped'):.0%},
with ships they follow {m('r4_control','2 ships, default','grouped'):.0%}, and when they walk three times as fast
{m('r4_control','2 ships, walk x3','grouped'):.0%} (largest group {m('r4_control','2 ships, walk x3','largest'):.0%}).
Bodies add little to this; the walking does it. Fairness is where bodies cost: the least-served quarter drops from
{m('r5_gravity','no bodies','bottomQuarter'):.3f} to {m('r5_gravity','closed loop','bottomQuarter'):.3f}, because the ships spend their time
over the groups. Halving all masses gives some of it back ({m('r7_mass','mass x0.5','bottomQuarter'):.3f}) at the price of boredom.</p>
<div class="figs two">
{fig('heat_loop', 'Crowd density every 8 bars, closed loop. Discs: the bodies the MJ derives from the groups.')}
{fig('heat_none', 'The same seed with no bodies.')}
</div>
""")
    return "".join(s)


def section_more():
    return f"""
<h2>8b. Tempo, height, band switching, programmes</h2>
<div class="figs one">
{chart_fig('r14_bpm', 'engagement', 'Engagement by tempo and lap length', 'At 174 BPM a 2-bar lap is 4.7 events a bar and tires the floor; at 100 BPM it is the better cruise. The target is an angular speed of roughly 50-75 °/s, not a bar count.')}
{chart_fig('r15_reach', 'engagement', 'Engagement by the path\'s elevation reach', 'HeightMap reach: 0.3 keeps the path high (near the zenith), 0.7 brings the rim down to the horizon. Lower paths are heard better: more azimuth, less overhead.')}
{chart_fig('r13_dive', 'engagement', 'Engagement by band strategy (with hold + double)', 'Switching to 8 kHz only while over a group buys little; a high or a wide band all the time buys a lot.')}
{chart_fig('r10_program', 'engagement', 'Engagement by set programme (136 bars)', 'The model has no song structure, so a dramaturgy (intro, groove, peak, break) cannot score here; what it measures is steady state.')}
</div>
{fig('azimuth_zoom', 'The breath close up: a ship that stops on beat 4 of every bar (the flat steps), restarts on the one and catches up with its rabbit.')}
{fig('azimuth_time', 'How the moves look in time: degrees a ship has travelled round the room. The bare orbit is a straight ramp; gravity bends it; hold + double gives flat steps (holds) and steep stretches (doublings).')}
"""


def section_effects():
    return f"""
<h2>8c. Stereo DJ effects in the dome</h2>
<p>An effect takes the second ship for the last 2 bars of every 16 and then hands it back to the flight. Paired against
the same set without effect (both with hold + double):</p>
{paired_rows('r16_effects', 'no effect')}
<p>Every effect costs a little here: an effect is a burst of events on top of a set that already has its moves, and the
model counts that as load. Two readings survive. A <strong>step reads better than a glide</strong> (ping-pong every 2
beats: step −0.017, full glide −0.028), as the research note predicted from the 336&nbsp;ms integration time. And the
<strong>shortest, sharpest effect costs least</strong>. Use effects as accents in a breakdown, not as a routine. (A
1/16-bar glide equals a step at the model's 1/16-note sample rate, hence the identical row.)</p>
"""


def section_scenes():
    if not os.path.exists(os.path.join(HERE, "results", "r21_scenes.json")):
        return ""
    out = load("r21_scenes")
    scenes = []
    for n in out:
        sc = n.split(": ")[0]
        if sc not in scenes:
            scenes.append(sc)
    tunings = ["plan (cap 1.5)", "cap = steer (0.3)", "stiff, cap = steer (0.6)"]
    head = "<tr><th>bodies placed by the DJ</th>" + "".join(f"<th>{esc(t)}</th>" for t in tunings) + "</tr>"
    rows = []
    for sc in scenes:
        cells = []
        for t in tunings:
            runs = out[f"{sc}: {t}"]
            pe = sum(r["perceived"] for r in runs) / len(runs)
            en = sum(r["engagement"] for r in runs) / len(runs)
            bo = sum(r["boredom"] for r in runs) / len(runs)
            cells.append(f"<td>{en:.3f} <span class=\"meta\">heard {pe:.0%} · bored {bo:.2f}</span></td>")
        rows.append(f"<tr><td>{esc(sc)}</td>{''.join(cells)}</tr>")
    return f"""
<h3>Does the cap rule hold for bodies the DJ places by hand?</h3>
<p>The closed loop above derives the bodies from the crowd. Here they are fixed scenes, as a DJ would tap them in
(with the crowd still listening and walking). Mean engagement, with the share of time motion is heard and the boredom:</p>
<div class="tablewrap"><table>{head}{"".join(rows)}</table></div>
<p>The plan's cap captures in every scene. Under the cap, <strong>several modest groups spread over the floor</strong>
did best: the path is bent from several sides in turn, instead of always towards one heavy centre. A hotspot in the
middle of the room mostly pulls the ships overhead. Stiffer steering scored a little lower with hand-placed groups:
it brings the ship back to the big path sooner.</p>
"""


def tempo_breath_table():
    out = load("r31_breath_tempo")
    arms = ["1-beat breath every bar", "half-beat breath every bar", "2-beat breath every 2nd bar"]
    head = "<tr><th>tempo</th>" + "".join(f"<th>{esc(a)}</th>" for a in arms) + "</tr>"
    rows = []
    for bpm in (100, 126, 174):
        sub = {k: v for k, v in out.items() if k.startswith(f"{bpm} BPM")}
        p = paired(sub, f"{bpm} BPM: no moves")
        f = paired(sub, f"{bpm} BPM: no moves", "fatigue")
        tds = "".join(f'<td style="white-space:nowrap">{p[f"{bpm} BPM: {a}"][0]:+.3f} <span class="meta">fatigue {f[f"{bpm} BPM: {a}"][0]:+.3f}</span></td>' for a in arms)
        rows.append(f"<tr><td>{bpm} BPM</td>{tds}</tr>")
    return f'<div class="tablewrap"><table>{head}{"".join(rows)}</table></div>'


def section_cadence():
    if not os.path.exists(os.path.join(HERE, "results", "r23_cadence.json")):
        return ""
    return f"""
<h3>How often should the MJ do something?</h3>
<p>Holds and doublings at different rates (2 ships, lap 4 bars, closed loop, 6 seeds), paired against no moves:</p>
{paired_rows('r23_cadence', 'no moves')}
<p>A short stop is worth more than a long one: <strong>standing still for the last 2 beats of every 4 bars</strong>
gave the largest single gain at a third of the fatigue of the hold-plus-double combination. A stop once in 16 bars is
too rare to matter. Doublings help at any rate tried, but each costs fatigue.</p>
{paired_rows('r25_cadence2', 'no moves') if os.path.exists(os.path.join(HERE, "results", "r25_cadence2.json")) else ""}
<h3>The breath</h3>
<p>That led to the night's best move. Every moving ship stands still for one beat — beat 4 — and restarts on the one.
Its rabbit runs on, so the restart is a little sprint. Variations, paired against no moves:</p>
{paired_rows('r28_breath_shape', 'no moves')}
{paired_rows('r29_gate', 'no moves')}
<p>Once a bar, for one whole beat, is the sweet spot. Half a beat (238&nbsp;ms at 126 BPM) is shorter than the ear's
~336&nbsp;ms integration time and loses half the effect; two stops a bar become a regular stutter that habituates like
the circle did. Both ships breathing together beats taking turns. Across tempo:</p>
{tempo_breath_table()}
<p>With two ships, letting them answer each other — ship 1 stops on beat 4, ship 2 on beat 2 — adds a little more and
tires less (round 51, inside the recommended set):</p>
{paired_rows('r51_call_response', 'both stop on 4')}
<p class="meta">Across the 18 listener variants (round 52): ahead in 14 of 18, 62 of 72 seeds. An option, not a rule.</p>
{fig('frames_final', 'Four frames of the recommended set: cap rule, breath every bar, closed loop. No tired guests.')}
"""


def floor_table(round_name, floors, arms, labels):
    out = load(round_name)
    head = "<tr><th>floor (listener variant)</th>" + "".join(f"<th>{esc(l)}</th>" for l in labels) + "</tr>"
    rows = []
    for f in floors:
        vals = [sum(r["engagement"] for r in out[f + ": " + a]) / len(out[f + ": " + a]) for a in arms]
        best = max(vals)
        tds = "".join(f'<td>{"<strong>" if v == best else ""}{v:.3f}{"</strong>" if v == best else ""}</td>' for v in vals)
        rows.append(f"<tr><td>{esc(f)}</td>{tds}</tr>")
    return f'<div class="tablewrap"><table>{head}{"".join(rows)}</table></div>'


def section_adaptive():
    floors = ["default", "fatigue x2", "fatigue x0.5", "habituation weak", "habituation strong"]
    t19 = floor_table("r19_bandit", floors, ["baseline", "hold+double", "learning MJ"],
                      ["no moves", "hold + double always", "learning MJ"])
    long = ""
    if os.path.exists(os.path.join(HERE, "results", "r20_bandit_long.json")):
        long = "<h3>Longer sets (192 bars)</h3>" + floor_table(
            "r20_bandit_long", ["default", "fatigue x2", "habituation strong"],
            ["baseline", "hold+double", "learning, 8-bar blocks", "learning, 4-bar blocks, explore .15"],
            ["no moves", "always", "learning, 8-bar blocks", "learning, 4-bar blocks"])
    return f"""
<h2>8d. A closed-loop MJ</h2>
<p>The moves lose when the floor tires twice as fast as the model assumes (section 9), and nobody knows how fast a
real floor tires. Two ways for the MJ to hedge were tried.</p>
<p><strong>A fatigue threshold</strong> (pause the moves while the floor's mean fatigue is above a line, resume
below a lower one) cannot do both jobs: a low line (0.12/0.06) protects the fast-tiring floor but throws away the
gain on the default one; a higher line (0.25/0.15) keeps the gain and no longer protects. Floors differ in their
resting fatigue, and the MJ does not know which floor it has.</p>
{paired_rows('r18b_adaptive', 'default: baseline')}
<p><strong>A learning MJ</strong> does know, after a while: every 8 bars it switches the moves on or off, scores the
floor's mean engagement over the second half of the block, keeps whichever has scored better and still tries the
other one a quarter of the time. Mean engagement, 96-bar sets, 6 seeds:</p>
{t19}
<p>Against the best choice for each floor, the worst case is −0.064 for "no moves", −0.028 for "always", and
−0.019 for the learning MJ. Always-on wins on average; the learning MJ is the safer default for a floor that has
not been measured — which is every floor, so far.</p>
{long}
"""


def section_breath_gravity():
    if not os.path.exists(os.path.join(HERE, "results", "r33_breath_gravity.json")):
        return ""
    return f"""
<h2>8f. With the breath on, do the planets still matter?</h2>
<p class="meta">Rounds 33-38, 42 and 45-49.</p>
<p>The question the night started with, asked again at the end. 2 ships, breath on every bar, 6 seeds:</p>
{chart_fig('r33_breath_gravity', 'engagement', 'Engagement with the breath, by bodies and band', 'In both bands the set without bodies scores highest; lighter or hand-placed spread groups cost least; an escort costs most.')}
<p>In this model the planets were never the source of attention; they were a cure for boredom, and the breath is a
cheaper one. What gravity still does — pull ships over the crowd and serve the groups before the loners — is then pure
cost. My first suspect was the model's assumption that overhead motion of a mid band is hard to hear; it is not the cause
(below). And the groups may matter for reasons the model does not score: the DJ telling the room where the sound goes is a performance gesture, not a perception metric.</p>
{robust_grav_html()}
<h3>Why: the planets act as brakes</h3>
<p>Switching off, one at a time, every listener effect that could explain it — precedence and off-centre blur,
proximity loudness, fatigue, and the poor hearing of overhead motion, then all of them at once — leaves no bodies ahead
in every seed ({pd('r36_why', 'ideal: all three off + overhead like azimuth: closed loop', 'ideal: all three off + overhead like azimuth: no bodies')} with
ideal ears). The cost is in the paths: with groups as bodies the ships fly slower (median 0.35 against 0.47 floor
units per beat) and further in (median radius 0.69 against 0.85). A ship that climbs out of a well with a capped steer
loses speed, and the wells pull the path in towards the zenith. Less angle per second for most of the floor.</p>
<h3>Making the planets cheap</h3>
{chart_fig('r37_useful_planets', 'engagement', 'Breath on, 8 kHz: forms of gravity', 'Gravity that acts only during beat 1 of each bar, at half mass, comes within 0.01 of no bodies, keeps the bends, and lands them on the one.')}
<div class="figs two">
{fig('traj_gate', 'Breath on every bar, gravity gated to beat 1 at half mass: the groups still bend the laps, on the one.')}
{fig('traj_final', 'For comparison, the breath with always-on gravity (cap rule): pulled further in.')}
</div>
{gate_robust_html()}
<p>With 24 seeds the price of gated half-mass planets against none is {pd('r42_gate_cost', 'breath, no bodies, 8k', 'R recommended, 8k')}
— about 2&nbsp;% of the engagement, every seed. That is the price of keeping the planets as the DJ's gesture.</p>
<p>Hand-placed scenes with the gate and half masses, against no bodies:</p>
{paired_rows('r45_scenes_rec', 'no bodies', keys=("engagement", "bottomQuarter", "boredom", "turnStd"))}
<p>With the gate, the cost simply follows how much the bodies bend the path: one hotspot is nearly free, eight bodies
are not.</p>
{rec_robust_html()}
<p>The gate also makes the cap rule a second line of defence rather than the only one: with gravity on beat 1 only,
even the plan's cap of 1.5 at full mass no longer captures ({m('r48_gate_cap', 'gate, cap 1.5, full mass, no breath'):.3f}
against {m('r48_gate_cap', 'plan as written'):.3f} as written) — three free beats a bar let every ship climb out. Across the 18 listener variants the gate alone, added to the plan as
written, gained +0.10 to +0.30 in all 72 seeds (round 49).</p>
<p>An escort as the DJ's gesture (4 bars in 16) inside the recommended set, by capture radius:</p>
{paired_rows('r47_escort_rec', 'R')}
<h3>Longer sets and other rooms</h3>
<p>Over 192 bars the recommended set holds ({m('r40_long', '192 bars: R recommended, 8k'):.3f}, fatigue
{m('r40_long', '192 bars: R recommended, 8k', 'fatigue'):.3f}, no drift). Its order over the bare circle and the plan as written
holds at 100 and 174 BPM, with 40 or 120 guests and with a uniform start (round 41); at 174 BPM the margin shrinks.</p>
"""


def rec_robust_html():
    f = os.path.join(HERE, "results", "r46_rec_robust.json")
    if not os.path.exists(f):
        return ""
    out = load("r46_rec_robust")
    perts = []
    for n in out:
        p = n.split(": ")[0]
        if p not in perts:
            perts.append(p)
    rows = []
    for pn in perts:
        sub = {k: v for k, v in out.items() if k.startswith(pn + ": ")}
        a = paired(sub, pn + ": bare orbit, 8k")[pn + ": recommended, 8k"]
        b = paired(sub, pn + ": plan as written")[pn + ": recommended, 8k"]
        rows.append(f'<tr><td>{esc(pn)}</td><td class="{"yes" if a[0] > 0 else "nope"}">{a[0]:+.3f} <span class="meta">({a[2]}/{a[3]})</span></td><td class="{"yes" if b[0] > 0 else "nope"}">{b[0]:+.3f} <span class="meta">({b[2]}/{b[3]})</span></td></tr>')
    return f"""<h3>The recommended set across the 18 listener variants</h3>
<p>Paired engagement of the recommended set (8 kHz) against a bare circle in the same band and against the plan as
written, 4 seeds per variant:</p>
<div class="tablewrap"><table><tr><th>listener model</th><th>vs bare orbit</th><th>vs plan as written</th></tr>{"".join(rows)}</table></div>"""


def gate_robust_html():
    f = os.path.join(HERE, "results", "r38_gate_robust.json")
    if not os.path.exists(f):
        return ""
    out = load("r38_gate_robust")
    perts = []
    for n in out:
        p = n.split(": ")[0]
        if p not in perts:
            perts.append(p)
    rows = []
    for pn in perts:
        sub = {k: v for k, v in out.items() if k.startswith(pn + ": ")}
        pr = paired(sub, pn + ": closed loop")
        g = pr[pn + ": gravity on beat 1, mass x0.5"]
        n0 = pr[pn + ": no bodies"]
        rows.append(f'<tr><td>{esc(pn)}</td><td class="{"yes" if g[0] > 0 else "nope"}">{g[0]:+.3f} <span class="meta">({g[2]}/{g[3]})</span></td><td>{n0[0]:+.3f} <span class="meta">({n0[2]}/{n0[3]})</span></td></tr>')
    return f"""<p>Across the listener variants, paired against the always-on closed loop (4 seeds each):</p>
<div class="tablewrap"><table><tr><th>listener model</th><th>gravity on beat 1, half mass</th><th>no bodies</th></tr>{"".join(rows)}</table></div>"""


def robust_grav_html():
    f = os.path.join(HERE, "results", "r34_breath_gravity_robust.json")
    if not os.path.exists(f):
        return ""
    out = load("r34_breath_gravity_robust")
    perts = []
    for n in out:
        p = n.split(": ")[0]
        if p not in perts:
            perts.append(p)
    rows = []
    for pn in perts:
        sub = {k: v for k, v in out.items() if k.startswith(pn + ": ")}
        pr = paired(sub, pn + ": breath, closed loop")
        a = pr[pn + ": breath, no bodies"]
        b = pr[pn + ": breath, loop, mass x0.5"]
        rows.append(f'<tr><td>{esc(pn)}</td><td class="{"yes" if a[0] > 0 else "nope"}">{a[0]:+.3f} <span class="meta">({a[2]}/{a[3]})</span></td><td>{b[0]:+.3f} <span class="meta">({b[2]}/{b[3]})</span></td></tr>')
    return f"""<h3>Across the listener variants (4 seeds each)</h3>
<p>Paired against "breath, closed loop":</p>
<div class="tablewrap"><table><tr><th>listener model</th><th>no bodies</th><th>closed loop, masses ×0.5</th></tr>{"".join(rows)}</table></div>"""


def section_shootout():
    return f"""
<h2>8e. Shootout: the plan as written against the lab's defaults</h2>
<p>The final round, 12 seeds, 96 bars each, everything else equal: the plan as written (P), the bare orbit (C), the
plan with the cap rule (D), and D with the breath, with a high or wide band, and with a doubling on top.</p>
{chart_fig('r39_recommended', 'engagement', 'The recommended set, 12 seeds', 'R: cap rule, breath every bar, planets gated to beat 1 at half mass, 8 kHz / 2 oct. Without planets it scores a little higher (section 8f); with three ships it tires.') if os.path.exists(os.path.join(HERE, "results", "r39_recommended.json")) else ""}
{chart_fig('r32_final', 'engagement', 'Final shootout: engagement', 'Recommended: D + breath every bar with 8 kHz / 2 oct (or 3 kHz / 4 oct). Plain plan steering is enough.')}
<div class="figs one">
{chart_fig('r32_final', 'bottomQuarter', 'Final shootout: the least-served quarter', '')}
{chart_fig('r32_final', 'boredom', 'Final shootout: boredom', '', better='lower')}
{chart_fig('r32_final', 'fatigue', 'Final shootout: fatigue', '', better='lower')}
</div>

<h3>The earlier shootout, with stiff steering</h3>
<p>12 seeds, 96 bars each.</p>
{chart_fig('r17_shootout', 'engagement', 'Engagement, plan vs lab defaults', 'A/B: plan start values (gravity cap 1.5). D: only the cap rule. E: stiff steering with the cap equal to it (the wider escort radius is set but unused: no escorts here). F: E + hold/double. G: F + 8 kHz/2 oct band.')}
<div class="figs one">
{chart_fig('r17_shootout', 'perceived', 'Share of time motion is heard', '')}
{chart_fig('r17_shootout', 'bottomQuarter', 'The least-served quarter', '')}
{chart_fig('r17_shootout', 'boredom', 'Boredom', '', better='lower')}
{chart_fig('r17_shootout', 'fatigue', 'Fatigue', '', better='lower')}
</div>
"""


def section_robust():
    rows = robust.table()
    head = "<tr><th>Listener model</th>" + "".join(f"<th>{esc(c[0])}</th>" for c in robust.CLAIMS) + "</tr>"
    body = []
    for pn, cells in rows:
        tds = "".join(f'<td class="{"yes" if h else "nope"}">{"✓" if h else "✗"} <span class="meta">{mm:+.3f}</span></td>' for h, mm, se in cells)
        body.append(f"<tr><td>{esc(pn)}</td>{tds}</tr>")
    held = [sum(1 for _, cells in rows if cells[i][0]) for i in range(len(robust.CLAIMS))]
    summary = ", ".join(f"{c[0]}: {h}/{len(rows)}" for c, h in zip(robust.CLAIMS, held))
    return f"""
<h2>9. Robustness: change the listener, keep the verdict?</h2>
<p>Each row re-runs eight core conditions (4 seeds each) with one assumption changed: hearing thresholds ×0.7 and
×1.4, the side penalty halved or raised, habituation strong or weak, fatigue halved or doubled, crowd size 40 and 120,
140 BPM, a uniform start, the plan's own 1/128-beat step, a ring of 8 speakers only or 16 + 8, and listeners who face
the centre or any direction instead of the DJ. A tick means the paired difference to the reference
(2 ships, lap 4 bars, 3&nbsp;kHz / 2&nbsp;oct, closed loop) has the claimed sign.</p>
<div class="tablewrap"><table>{head}{"".join(body)}</table></div>
<p class="meta">Held: {esc(summary)}.</p>
{robust24_html()}
"""


def robust24_html():
    rows = robust.table24()
    if not rows:
        return ""
    head = "<tr><th>Listener model</th>" + "".join(f"<th>{esc(c[0])}</th>" for c in robust.CLAIMS24) + "</tr>"
    body = []
    for pn, cells in rows:
        tds = "".join(f'<td class="{"yes" if h else "nope"}">{"✓" if h else "✗"} <span class="meta">{mm:+.3f}</span></td>' for h, mm, se in cells)
        body.append(f"<tr><td>{esc(pn)}</td>{tds}</tr>")
    held = [sum(1 for _, cells in rows if cells[i][0]) for i in range(len(robust.CLAIMS24))]
    summary = ", ".join(f"{c[0]}: {h}/{len(rows)}" for c, h in zip(robust.CLAIMS24, held))
    return f"""
<h3>And the shootout's order?</h3>
<p>The plan as written (P), the plan with the cap rule (D), the lab flight (E: stiff steering, cap = steering), E with
hold + double (F), and the bare orbit (C), under the same listener variants (64 bars, 4 seeds):</p>
<div class="tablewrap"><table>{head}{"".join(body)}</table></div>
<p class="meta">Held: {esc(summary)}.</p>
"""


def section_conclusions():
    return """
<h2>10. What the MJ concludes</h2>
<ol>
<li><strong>Gravity is a bending tool with a hard ceiling.</strong> Never let the pull exceed what the ship can steer back
with. Above that line the sound parks; below it the path bends and recovers. Make it a rule in <code>FlightTuning</code>,
not a tuning value: <code>gravityMax = steerMax</code>. Stiffer steering fixes the plan's tracking error (0.19 behind the
rabbit) but is not a gain in itself.</li>
<li><strong>The circle is not the enemy; an unbroken circle is.</strong> What un-bores a floor in this model is a change it
can hear: a short stop and a restart on the one — the breath, one beat every second bar — or a doubling. Bending towards groups changes the geometry, but from the floor it
mostly turns azimuth motion into overhead motion.</li>
<li><strong>Put the moves on bar lines, not the beat into the physics.</strong> The pulse is harmless, but it is not the music
link. A move that starts on the one is.</li>
<li><strong>Two ships move; the rest wait.</strong> With moves on, a third moving ship already costs more than it gives.</li>
<li><strong>Cruise at one lap per 4 bars.</strong> Without stops the best cruise is an angle per second (50-75 °/s, so 2 bars
below ~110 BPM); with the breath, 4 bars at every tempo tried. Fly the big path low.</li>
<li><strong>Move the top of the mix.</strong> 6-8&nbsp;kHz at 2 octaves, or 3&nbsp;kHz at 4. Never narrower than an octave, never
centred at 1&nbsp;kHz or below, if the path should be followed.</li>
<li><strong>Let the planets say where, not fight the boredom.</strong> Once the ships breathe, groups as gravity cost
attention in this model. Keep them light (half the plan's masses) and spread, and let the DJ use them to point the
sound at a part of the room.</li>
<li><strong>Escort wide or not at all, and only as a gesture.</strong> At the plan's radius it parks the ship over the group.</li>
<li><strong>Watch who is left out, and watch the floor tire.</strong> Groups pull ships and ships serve groups; lighter masses
keep the edges in. The moves are worth it only while the floor has the stamina, so an MJ that eases off when the floor
tires is the safe default (section 8d).</li>
</ol>
"""


def section_defaults():
    with open(os.path.join(HERE, "mj-defaults-from-lab.md")) as f:
        md = f.read()
    rows = []
    for line in md.splitlines():
        if line.startswith("|") and not line.startswith("|---") and "Setting" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 5:
                tag = cells[3].lower()
                kinds = [k for k, w in (("sim", "sim"), ("res", "research")) if w in tag] or ["guess"]
                code = lambda t: re.sub(r"`([^`]*)`", r"<code>\1</code>", esc(t))
                tags = " ".join(T(k) for k in kinds) + (' <span class="meta">(weak)</span>' if "weak" in tag else "")
                rows.append(f"<tr><td>{esc(cells[0])}</td><td>{code(cells[1])}</td><td>{code(cells[2])}</td><td>{tags}</td><td>{code(cells[4])}</td></tr>")
    return f"""
<h2>11. Recommended defaults</h2>
<p>Also as a plain table for the defaults owner: <code>mj-defaults-from-lab.md</code>.</p>
<div class="tablewrap"><table><tr><th>Setting</th><th>Value</th><th>Plan / today</th><th></th><th>Why</th></tr>{"".join(rows)}</table></div>
"""


def section_listening():
    return """
<h2>12. What only a listening test can decide</h2>
<ul>
<li><strong>Whether "boredom" exists the way the model says.</strong> The 20&nbsp;% interest a steady circle keeps is my
number (section 9 shows the rankings survive 0.05 and 0.5, but the size of every gain depends on it). Test: 16 bars of
bare orbit, ask "still interesting?" at bars 4, 8, 12 and 16.</li>
<li><strong>Fatigue and dizziness.</strong> No published threshold exists. The ship-count result rests on it. Block 6 of
the research note's listening test (1 vs 2 vs 4 ships) decides it.</li>
<li><strong>Whether diving over the crowd is heard.</strong> The model says a 3&nbsp;kHz band overhead is nearly static to
the people under it. Test: one ship patrolling vs pulled over a group, 3&nbsp;kHz vs 8&nbsp;kHz.</li>
<li><strong>Energy in the band.</strong> The sim prefers 6-8&nbsp;kHz because it localises best; a dark track may have
nothing there. C0 (measure Isolator3 in Hz) comes first.</li>
<li><strong>The breath.</strong> Whether a ship that stops for one beat every bar reads as groove or as a dropout. The
model's whole case for it is that a stop and a restart on the grid are events; a real ear may hear a glitch. Test: 16
bars of plain orbit against 16 bars with the breath, same band, same level, listeners not told which.</li>
<li><strong>Off-centre listening.</strong> The precedence pull is modelled crudely; the rim of the floor may hear far less
than the model says.</li>
<li><strong>How a crowd actually moves.</strong> Nothing in the walking rules is measured. Watch the floor.</li>
</ul>
"""


def section_repro():
    return """
<h2>13. Reproduce</h2>
<p>Everything is in <code>research/mj-lab/</code> of the a3-pro-dj repository, Python standard library only:
<code>flight.py</code> (the plan's model), <code>hearing.py</code> (perception), <code>crowd.py</code> (guests),
<code>mj.py</code> (the automatic MJ), <code>sim.py</code> (one run), <code>rounds.py</code> (every condition),
<code>go.py</code> (sweeps), <code>robust.py</code>, <code>figs.py</code>, <code>report.py</code>. The night's log with
timestamps is <code>log.md</code>.</p>
<p><code>nice -n 19 python3 -u go.py r5_ships</code> re-runs one round (6 seeds, 2 workers);
<code>python3 figs.py all &amp;&amp; python3 report.py</code> rebuilds this page.</p>
"""


def breath_held(round_name="r30_breath1_robust", arm="breath every bar"):
    f = os.path.join(HERE, "results", round_name + ".json")
    if not os.path.exists(f):
        return "(pending)"
    out = load(round_name)
    perts = sorted({n.split(": ")[0] for n in out})
    held = 0
    for pn in perts:
        held += paired({k: v for k, v in out.items() if k.startswith(pn + ": ")}, pn + ": baseline")[pn + ": " + arm][0] > 0
    return f"{held} of {len(perts)}"


def grav_held():
    f = os.path.join(HERE, "results", "r34_breath_gravity_robust.json")
    if not os.path.exists(f):
        return "robustness pending"
    out = load("r34_breath_gravity_robust")
    perts = sorted({n.split(": ")[0] for n in out})
    held = 0
    for pn in perts:
        sub = {k: v for k, v in out.items() if k.startswith(pn + ": ")}
        held += paired(sub, pn + ": breath, closed loop")[pn + ": breath, no bodies"][0] > 0
    return f"no bodies ahead in {held} of {len(perts)} listener variants"


def count_runs():
    import glob, json
    n = 0
    for f in glob.glob(os.path.join(HERE, "results", "*.json")):
        with open(f) as fh:
            n += sum(len(v) for v in json.load(fh).values())
    return n


if __name__ == "__main__":
    global RUNS, ROBUST_N, BREATH_HELD, GRAV_HELD, ROUNDS
    RUNS = count_runs()
    ROBUST_N = len(robust.table())
    BREATH_HELD = breath_held()
    GRAV_HELD = grav_held()
    import glob, re as _re
    ROUNDS = len({_re.match(r"r(\d+)", os.path.basename(f)).group(1) for f in glob.glob(os.path.join(HERE, "results", "r*.json"))})
    body = (section_header() + section_summary() + section_question() + section_model() + section_hypotheses()
            + section_results() + section_more() + section_effects() + section_adaptive() + section_shootout() + section_breath_gravity()
            + section_robust() + section_conclusions() + section_defaults()
            + section_listening() + section_repro())
    html = page("MJ Lab", "A night of simulated dance floors under the A³ dome: which sound movements attract listeners, and what the gravity flight should default to.", body)
    with open(os.path.join(HERE, "report.html"), "w") as f:
        f.write(html)
    print("report.html", len(html) // 1024, "KiB")
