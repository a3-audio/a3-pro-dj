# Auditory motion: what research says, and starting values for A³

What a listener on a dance floor can and cannot hear of a moving sound, and the values A³ starts from
because of it. Written 2026-10-08 as the research base for A³ Motion's flight (the "ships"), its clips,
and the 3D band filter (FREQ/Q); the [MJ playbook](mj-playbook.md) and the
[movement lab](../../research/mj-lab/) build on it.

Part A is sources, part B is derived values, part C is a one-evening listening test. Every claim in
part A has a source. Strength tags: **[solid]** means peer-reviewed and replicated, or a standard
textbook. **[single]** means one peer-reviewed study. **[practice]** means practitioner or press
reports, so anecdotal.

Arithmetic used throughout. One bar is 4 beats, so
`deg/s = 360 × laps_per_bar × BPM / 240 = 1.5 × BPM × laps_per_bar`.
That is 180 °/s per lap-per-bar at 120 BPM and 195 °/s at 130 BPM.

**How A³ moves a sound (the context for part B):**
- In stereo mode the 3D control pulls a filtered band (an Airwindows Isolator3 band, chosen by FREQ
  and Q) out of the channel and sends it into the room; the rest stays put as the steady bed. So the
  band moves and the rest does not. With stems, a whole stem moves instead.
- FREQ and Q arrive as 0…1 and are mapped linearly onto the Isolator's parameter range. How that
  parameter relates to **Hz and octaves had not been measured** when this was written (see C0), so
  part B talks in Hz and octaves, not in A³ control values.
- Encoding and decoding are IEM plug-ins (3rd-order Ambisonics). Motion steers azimuth and elevation
  only; there is no distance.

---

## A. What the research says

### A1. Motion perception limits

| Finding | Numbers | Source | Strength |
|---|---|---|---|
| The minimum audible movement angle (MAMA) grows with speed | 8.3° at 90 °/s up to 21.2° at 360 °/s | Perrott & Musicant 1977, JASA 62(6) 1463 ([summary](https://publications.aston.ac.uk/id/document/57808)) | solid |
| MAMA is U-shaped over speed; the best resolution is at slow speeds | horizontal 1.7° at 1.8 °/s, about 10° at 320 °/s; optimum about 2 °/s horizontally and 7–11 °/s vertically; **vertical MAMAs are larger at every speed (often > 8°)** | Saberi & Perrott 1990, JASA 88(6) 2639 ([pdf](https://sites.socsci.uci.edu/~saberi/saberiandperrott1990a.pdf)) | solid |
| MAMA depends on where the source is | about 5° straight ahead, **> 30° at ±90°** (500 Hz tones) | Grantham 1986, JASA 79(6) 1939 | solid |
| The ear integrates over time | minimum integration time about 336 ms (500 Hz); MAMA rises steeply below 100–150 ms duration | Chandler & Grantham 1992, JASA 91(3) 1624 ([via](https://publications.aston.ac.uk/id/document/57808)) | solid |
| Upper limit of rotation (UL): above it, listeners cannot tell CW from CCW | **white noise about 2.5 rot/s (900 °/s)**; band-limited noise equals white noise in an anechoic room; harmonic tones fall lower as f0 rises | Féron, Frissen, Boissinot, Guastavino 2010, JASA 128(6) 3703 | single+ (replicated by the next row) |
| The UL depends on spectrum and comes from front/back confusion | UL rises with centre frequency **and** bandwidth; **250 Hz bands fall below 0.5 rot/s** (cannot be measured, ITD only); 4 kHz at ½–1 oct is clearly below white noise; 4 kHz at 4 oct is about the same as white noise. Above the UL, people hear "left-right alternation", "half circles, figure eights, jumps". 24-speaker ring, r = 1.8 m. | Roggerone, Vacher, Tarlao, Guastavino 2019, Sci Rep 9:16437 ([open](https://doi.org/10.1038/s41598-019-52742-0)) | single, strong |
| Speed discrimination is coarse | **20–70 % speed difference** needed (Weber fraction roughly constant); a sudden **speed-up during motion needs about 3× more** than a slow-down; the velocity integration window is about 1 s; listeners have a "slow prior" | Carlile & Best 2002, JASA 111(2) 1026; Locke, Leung, Carlile 2016, Sci Rep 6:27725 ([open](https://doi.org/10.1038/srep27725)) | solid |
| Overview of all the above | the "snapshot" theory: motion is largely successive localisations | Carlile & Leung 2016, Trends in Hearing 20 ([open](https://doi.org/10.1177/2331216516644254)) | review |
| Static acuity also varies with frequency | MAA about 1° in front below 1 kHz, **worst around 1.5–2 kHz** (the ITD/ILD hand-over) | Mills 1958, JASA 30(4) 237 | solid |

**Ambisonics, listener position, and a crowd:**
- The sweet area grows with order. Zotter & Frank define it as the region with localisation uncertainty
  < 30°. At 1st order it reaches halfway to the speakers; **at 3rd order it covers almost the whole
  array**. Ambisonics with max-rE keeps width and loudness constant while panning. VBAP does not: its
  width changes as the source passes a speaker. Source: Zotter & Frank 2019, *Ambisonics*, Springer, open access
  ([book](https://doi.org/10.1007/978-3-030-17207-7)). [solid]
- Off centre, the **precedence effect pulls transients towards the nearest speaker** more than steady
  noise. The source direction depends on signal type. Source: Stitt, Bertet, van Walstijn 2017, JAES 65(3) 188
  ([abstract](https://pure.qub.ac.uk/en/publications/off-center-listening-with-third-order-ambisonics-dependence-of-pe/)). [single]
  For a club this means a moving hi-hat band is heard by most of the crowd as "which speaker near
  me gets louder", not as an angle.
- In a hall, how well listeners identify trajectories depends on **seat, trajectory and scene complexity**. A
  visible, synchronous performer gesture partly offsets the off-centre loss. Source: Marentakis et al., ICAD
  2008 ([record](https://repository.gatech.edu/entities/publication/9a712595-a009-44d7-a305-cbd864a32f2f)). [single]

### A2. Frequency: what moves well

| Band | Cue | What it means for motion | Source |
|---|---|---|---|
| < about 150 Hz | in-room, mode-dominated; subs usually shared | does not localise or move in a club; practice keeps it static or distributed | [practice]: 4DSOUND keeps bass a "steady pulse" ([review](https://spatialsoundinstitute.com/P_Techno-is-Space-A-Review)); Rex Club L-ISA with distributed subs ([PSW](https://www.prosoundweb.com/molecule-brings-immersive-soundscape-to-the-rex-club-in-paris-with-l-isa/)) |
| about 150 Hz – 1 kHz | ITD | azimuth is fine, **front/back ambiguous**, so rotation direction is lost early (250 Hz UL < 0.5 rot/s) | Roggerone 2019; Yost & Zhong 2014 |
| about 1.5–3 kHz | ITD/ILD gap | worst static acuity for narrow signals | Mills 1958; Yost & Zhong 2014 |
| 4–16 kHz | ILD + pinna | **up/down cues 6–12 kHz, front/back 8–16 kHz**; needed for elevation and for unambiguous circles | Langendijk & Bronkhorst 2002, JASA 112(4) 1583 ([summary](https://sonicfield.org/library/contribution-of-spectral-cues-to-human-sound-localization)) [solid] |

- **Bandwidth matters more than centre frequency.** Noise wider than 1 octave localises best (about 6–7° rms) and
  **does not depend on CF**. Narrower bands are worse, especially at 1–4 kHz. Source: Yost & Zhong 2014, JASA,
  "Sound source localization identification accuracy: bandwidth dependencies"
  ([summary](https://labs.sonicfield.org/library/sound-source-localization-identification-accuracy-bandwidth-dependencies)). [solid]
  The UL work above shows the same for motion.
- **Narrow bands have their own elevation.** For 1/6-octave noise, perceived elevation and front/back follow the
  **centre frequency, not the source position**: Blauert's "directional bands". Source: Middlebrooks 1992, JASA
  92(5) 2607; Blauert, *Spatial Hearing* ([context](https://acris.aalto.fi/ws/portalfiles/portal/91320765/Directional_Band_ICA2022.pdf)). [solid]
  A narrow, high band moving in elevation will sit at "its" height whatever Core sends.
- **Pitch-height effect:** higher bands are heard higher, and phantom images from wide speaker pairs rise
  (500 Hz and 8 kHz the most). Source: Lee, ICSA 2015 ([pdf](https://eprints.hud.ac.uk/25887/1/ICSA2015_LEE_AuthorManuscript.pdf)). [single]
- **Moving a filtered band instead of full band:** there is no listening study of "extract one band and move it" on
  a dance floor. The closest practice is **timbre or spectral spatialisation**, where 4–16 bandpass bands are spread
  and moved separately. Sources: Normandeau 2009, Organised Sound 14(3)
  ([CUP](https://resolve.cambridge.org/core/journals/organised-sound/article/timbre-spatialisation-the-medium-is-the-space/0FC76C4A3E8EA33261DC0B95AABAC6E1)) [practice/aesthetic];
  Kim-Boyle 2008, ICMC, "Spectral spatialization – an overview" [practice]. The psychophysical consequence follows
  directly from Roggerone 2019 and Yost & Zhong 2014: **the moving band must be wide, about 2 octaves or more,
  and contain energy above 2–4 kHz**, or direction and front/back collapse at moderate speeds.

### A3. Trajectory shape and timing in practice

- Rotation speeds in practice:
  - Stockhausen's rotation table (Kontakte 1958–60, manual) and the electric version for *Sirius*
    went **up to 25 rot/s**. Far above the UL, that becomes a timbre or "flutter", not a path
    ([Wikipedia, Kontakte](https://en.wikipedia.org/wiki/Kontakte); [eContact](https://econtact.ca/12_4/kontakte/index.php)). [practice]
  - Leslie speaker: slow at 40–50 rpm (about 0.7–0.8 rot/s), fast at 340–400 rpm (about 6–7 rot/s), which is heard as
    tremolo or vibrato. This matches the UL ([Wikipedia](https://en.wikipedia.org/wiki/Leslie_speaker)). [practice]
- Chowning 1971 simulated moving sources with **angle + direct/reverb ratio (distance) + Doppler (speed)** and argued that motion
  reads as motion only when distance and speed cues come with it. Source: JAES 19(1) 2
  ([CCRMA](https://ccrma.stanford.edu/papers/simulation-of-moving-sound-sources)). [practice/classic]
- Listeners find spatial gesture meaningful, but at the level of **schemata such as "approach", "encircle" and
  "fly-over"**, not exact geometry. Source: Kendall 2010, Organised Sound 15(3)
  ([QUB](https://pure.qub.ac.uk/en/publications/spatial-perception-and-cognition-in-multichannel-audio-for-electr/)). [review/theory]
- BEAST, the large diffusion orchestra, uses n-channel stems and diffusion as performance. Source: Wilson & Harrison 2010,
  Organised Sound 15(3) 239 ([BEAST](https://en.wikipedia.org/wiki/Birmingham_ElectroAcoustic_Sound_Theatre)). [practice]
- Club practice from 4DSOUND's "Techno is Space":
  - hi-hats and kicks "hitting you at different heights and angles" worked;
  - **few moving elements**: "less becomes far more";
  - spatial complexity asks for attention a club does not always give;
  - stereo habits produced a "3D-ised version of what we know".

  [practice] ([review](https://spatialsoundinstitute.com/P_Techno-is-Space-A-Review))
- L-ISA at the Rex Club (Molécule): a snare circling, ping-pong between virtual walls, random throws that stop and
  fade ([PSW](https://www.prosoundweb.com/molecule-brings-immersive-soundscape-to-the-rex-club-in-paris-with-l-isa/)). [practice]
- DJ spatialisation with REAPER and IEM on 7.1.4: the MSc thesis reports that stability and real-time feasibility dominated. It has no speed
  data. Source: Costa 2025, P.Porto ([record](https://recipp.ipp.pt/entities/publication/51a8214f-a439-48a4-9a0a-bac306c0d43f)). [practice]
- **Disorientation:** a rotating sound field can induce illusory self-rotation (auditory vection), especially with
  several sources turning together. It is weaker than visual vection. Source: Väljamäe 2009, Brain Res. Rev. 61(2) 240
  ([Chalmers](https://research.chalmers.se/en/publication/114917)). [review] There is **no published threshold for
  "tiring" on a dance floor**. The practitioner consensus is "few elements, not all moving".

### A4. Stereo DJ effects and their note values

- Pioneer DJ DJM-900NXS2 Beat FX (operating instructions): delay and echo at **1/16–16 beats**; filter, flanger and phaser cycles
  at **1/16–64 beats**. There is no dedicated auto-pan, but PING PONG and TRANS exist
  ([manuals](https://support.pioneerdj.com/hc/en-us/articles/11949532807193-Manuals)). [manufacturer]
- Generic auto-pan: 0.05–10 Hz free, or note values in sync
  ([Roland SPD-SX PRO](https://static.roland.com/manuals/SPD-SX_PRO_reference_v200/en-US/560965643.html)). [manufacturer]
- **No published mapping from stereo DJ effects to 3D was found.** What follows in B is derived.

### A5. Distance and size (brief)

Distance is cued by level, direct-to-reverberant ratio and spectrum (air absorption). Doppler cues speed. Source:
Zahorik, Brungart, Bronkhorst 2005, Acta Acustica 91, 409. [review] Chowning 1971. A³ steers azimuth and elevation only. A
velocity-dependent level or HF change ("closer when faster") would be the cheapest add-on, but it is out of scope.

---

## B. Starting values for A³ (derived, not sourced)

Tags: **R** = from research (with the A-row it rests on). **G** = guess, test it.

### B1. Speed

| laps/bar | lap every | °/s at 120 | °/s at 130 | Reading | Tag |
|---|---|---|---|---|---|
| 1/32 | 32 bars (a slow precession) | 5.6 | 6.1 | not heard as motion on its own; "the room drifts" | R (Saberi: optimum resolution, but too slow to notice without a reference) + G |
| 1/8 | 8 bars | 22.5 | 24 | slow, clear for wide bands | R (MAMA about 5° front) |
| **1/4** | **4 bars (the base orbit)** | **45** | **49** | **clear path, readable in the crowd: keep as the default** | R |
| 1/2 | 2 bars | 90 | 98 | energetic; side MAMA > 20° | R |
| 1 | 1 bar | 180 | 195 | direction still clear for wide high bands, ambiguous for low bands | R (Roggerone: 250 Hz UL < 0.5 rot/s = 180 °/s) |
| 2 | 2 beats | 360 | 390 | "swirl"; direction only for broadband or ≥ 2 oct at 4 kHz | R |
| 4 | 1 beat | 720 | 780 | at the UL (2.5 rot/s = 900 °/s): turns into a texture, tremolo-like | R (Féron 2010) |

- **`speedMax`:** 1 lap per 2 beats (≈ 360–400 °/s) for full band or wide bands, and **1 lap per bar for a band with FREQ below about 1 kHz**.
  Faster than that is an effect (Leslie, flutter), not a path. **R + G**
- **`speedMin` for a captured ship:** ≥ 1 lap per 2 bars (the escort lap). Its radius is small, though, so check the *angular*
  speed seen from the room: a small orbit around a group at the rim sweeps only a few degrees, and that is below the MAMA. **G**
- **Speed changes must be ≥ 1.5×, and ≥ 2× when speeding up, to be heard as "faster".** A slingshot that adds 20 % is
  inaudible as speed. It is only audible as a change of path. **R** (Carlile & Best; Locke 2016)

### B2. Excursion, meaning how far a bend must go

| Item | Value | Tag |
|---|---|---|
| Smallest deviation from the orbit that counts as "it bent" | ≥ 20° azimuth front, ≥ 30° to the sides; **use 30° as the design minimum for the crowd** | R (Grantham MAMA 5°→30°; sweet-area criterion 30°) |
| A body's capture orbit seen from the centre | must subtend ≥ 30°, otherwise ESCORT sounds like "parked" | G (derived from the row above) |
| Wander per bar | ≤ 10° is inaudible, so it is safe as "life"; 20–30° is heard as a wobble | R + G |

### B3. Elevation

| Item | Value | Tag |
|---|---|---|
| Use elevation for | bands with energy at **6–12 kHz** (hats, air, claps); otherwise it is mostly not heard | R (Langendijk & Bronkhorst) |
| Smallest elevation step | ≥ 15–20° (vertical MAMA > 8° in the lab; worse with a dome and a crowd) | R + G |
| Vertical speed | slower than azimuth: ≤ 1/2 of the azimuth speed | R (vertical optimum is slower; G for the factor) |
| Narrow high band (Q > about 1 oct) | **elevation will be fixed by its frequency** (directional bands), so do not rely on elevation movement there | R (Middlebrooks 1992) |

### B4. The 3D filter (FREQ, Q)

Hz and octave values. Mapping them onto Isolator3's 0.05…0.9 needs C0 first.

| Item | Value | Tag |
|---|---|---|
| FREQ default (centre) | **about 3 kHz**, roughly 1.5–6 kHz at 2 oct: hats, claps and vocal presence, inside the best UL region (4 kHz, ≥ 2 oct) | R (Roggerone, Yost & Zhong) + G (club content) |
| FREQ useful range | **about 250 Hz – 10 kHz**. Below about 250 Hz it moves "something", but the crowd hears no path (ITD only, front/back gone, room modes) | R + practice |
| FREQ below about 150 Hz | not useful for motion; a test point at most | practice |
| Q (bandwidth) default | **2 octaves** | R |
| Q range | **4 oct (wide) to 1 oct (narrow)**. Narrower than 1 oct is a "colour that wobbles", and narrower than ½ oct moves almost nothing audible | R (Yost & Zhong: > 1 oct needed; Roggerone: 4 kHz ½–1 oct UL drops sharply) |
| Coupling | the narrower Q or the lower FREQ, the lower the usable speed (B1 caps) | R |
| Energy | a 2-oct band at 3 kHz in club music carries roughly −10 to −15 dB relative to full band (genre-dependent). The 3D gain should make it audible against the steady bed, so measure it on the system's meters | G |

FREQ and Q only act in 3D, yet they sit on the motion controller. That is consistent with B4: they
choose **what** moves, which is a motion decision and not a tone control. A label such as "MOVE BAND" with
a Hz/oct readout would make that explicit. **G** (UI suggestion, not decided).

### B5. Gravity pulse

| Item | Value | Tag |
|---|---|---|
| A gravity pulse on the beat | it acts on acceleration. The audible quantity is the **positional deviation per beat** near a body, and it must reach ≥ 20–30° (B2) to be heard as "pulled on the beat". It is probably inaudible with small pulse depths (0.3 / 0.6 of the acceleration) unless a ship passes close to a body | R (MAMA) + G (needs a log of the deviation in the unit tests: max angle change per beat at 120 BPM) |
| Rhythm resolution | a beat at 120 BPM lasts 500 ms, just above the 336 ms integration time, so a **per-beat** spatial accent is near the limit and a per-1/8 one (250 ms) is below it | R (Chandler & Grantham) |
| Suggestion | pulse on **half bars or bars**, not on every beat; keep the downbeat accent | G |

### B6. Stereo DJ effects translated to 3D (proposals)

| Stereo effect | 3D translation | Rate (note value) | Tag |
|---|---|---|---|
| Auto-pan L↔R | ping-pong between two opposite points, a step or a fast glide (≤ 1/16 bar) | 1/2–2 beats per side | G; a step reads better than a glide, because short glides fall below integration time (R) |
| Auto-pan circle | rotation | 1 lap per 1–4 bars; 1 lap per beat only as "swirl" | R (B1) |
| Filter sweep | **FREQ sweep of the moving band while it orbits**: the band "climbs" (pitch-height) | 4–16 bars | R (Lee) + G |
| Echo throw | throw the delay return to a point opposite the source and let it drift back over 1–2 bars | 1/4–1 bar delay | G (needs the delay on its own movable path, so out of the current routing) |
| Riser | elevation sweep from 0° to the top + faster rotation (×2 per 4 bars), high FREQ | 8–16 bars | R (elevation needs HF) + G |
| Drop | snap the band back to front or static on the 1 (contrast) | 1 beat | G |

---

## C. Listening test: one evening at the system

**Safety first:** a PA set up for a club is loud. **No signal goes to the speakers until the person
responsible for the PA says so**, and that person sets the level and the amps. Music only (the DJ's own
tracks), no test tones on the PA.

**C0. Before the evening (no PA):** measure the band filter's Hz and octaves for the parameters 0.05 /
0.25 / 0.5 / 0.75 / 0.9 (offline, or on the headphone bus) so that FREQ and Q can be talked about in
Hz and octaves.

**Who and where:** 3–5 listeners: whoever runs the system, the DJ, and 1–3 others. **Three positions:**
centre, halfway to the ring, and about 1 m from a speaker. Listeners rotate between blocks, and each
listener answers on a sheet.

**Method:** the DJ plays one loop-friendly track (and a second, darker one). The operator switches the
settings in a random order without naming them. Each trial lasts 8 bars. Listeners answer:
1. direction (CW / CCW / unclear), which is an objective check;
2. "motion clear" on a 1–5 scale;
3. "comfortable / musical" on a 1–5 scale.

| Block | Compare | Settings | Time |
|---|---|---|---|
| 1 Speed | full band vs default band | 1 lap per 8 / 4 / 2 / 1 bars, and per 2 beats | 20 min |
| 2 FREQ | at Q 2 oct, 1 lap per 4 bars | 250 Hz, 1 kHz, 3 kHz, 8 kHz | 15 min |
| 3 Q | at the best FREQ | 4 / 2 / 1 / ½ oct | 15 min |
| 4 Elevation | high band, azimuth fixed | elevation 0↔45° on vs off, A/B | 10 min |
| 5 Gravity | one orbiting ship, one heavy group | pulse depth 0 / small / 2× small | 15 min |
| 6 Load | 1 vs 2 vs 4 ships moving at once | for comfort and vection | 10 min |

About 90 minutes with changes of position. **Decide from the results:** the speed caps (B1), the FREQ
and Q defaults and range limits (B4), whether elevation is worth a control (B3), the pulse depth (B5),
and how many simultaneous movers are pleasant (B6/A3). The measured values then go into Motion's
flight tuning and clip defaults, with a reference to this page.

**Status:** no record of it having been run as of 2026-10-31. Until it is, every **G** above is a guess and every **R** is
a reading of the literature, not of this system.
