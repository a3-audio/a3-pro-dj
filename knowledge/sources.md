# Sources

Every outside source this knowledge base rests on, with a link. **Manufacturer manuals are linked,
never copied**: get them from the manufacturer. Short paraphrases with page numbers appear in the
pages that use them; nothing longer.

A³'s own sources (its decisions, reviews and measurements) are named on the page where they are used,
with a date.

## Manufacturer manuals

| Document | Where to get it | Used in |
|---|---|---|
| AlphaTheta / Pioneer DJ **CDJ-3000X** instruction manual | product support page: <https://support.alphatheta.com/en-US/products/48245720355353> · online manual: <https://www.pioneerdj.com/support/manuals/player/cdj-3000x/en/index.html> · product page: <https://alphatheta.com/en/product/player/cdj-3000x/> | [CDJ-3000](gear/cdj-3000.md), [Pro DJ Link](gear/pro-dj-link.md) |
| Pioneer DJ **DJM-900NXS2** operating instructions (Beat FX values) | Pioneer DJ manuals: <https://support.pioneerdj.com/hc/en-us/articles/11949532807193-Manuals> | [mixers](gear/mixers.md), [motion perception](spatial/motion-perception.md) |
| Not a Number **Grapes 3D Audio Control** user guide (A³ read v1.4.0; current is v2.0.0) | download page: <https://grapes-3d.com/download/> · user guide v2.0.0: <https://grapes-3d.com/wp-content/uploads/2026/10/Grapes-3D-Audio-Control-User-Guide_v2.0.0.pdf> · tutorials: <https://grapes-3d.com/tutorials/> | [Grapes 3D](gear/grapes-3d.md) |
| Roland **SPD-SX PRO** reference (auto-pan rates) | <https://static.roland.com/manuals/SPD-SX_PRO_reference_v200/en-US/560965643.html> | [motion perception](spatial/motion-perception.md) |

## Pro DJ Link

- Deep Symmetry, **DJ Link Ecosystem Analysis** — the public protocol documentation A³'s
  implementations are written from: <https://djl-analysis.deepsymmetry.org/>
- **prolink-connect** (protocol documentation and implementation): <https://github.com/EvanPurkhiser/prolink-connect>
- beat-link (EPL-2.0) and dysentery (EPL-1.0) are reference implementations; A³ reads their
  documentation and never ports their code.
- A³'s trademark notice: <https://a3-audio.github.io/a3-doc/ressources/trademarks.html>

## Motion perception and spatial audio

Full citations with strength tags are in [motion perception](spatial/motion-perception.md), part A.

- Perrott & Musicant 1977, JASA 62(6) 1463 — minimum audible movement angle vs speed ([summary](https://publications.aston.ac.uk/id/document/57808))
- Saberi & Perrott 1990, JASA 88(6) 2639 — MAMA over speed, horizontal and vertical ([pdf](https://sites.socsci.uci.edu/~saberi/saberiandperrott1990a.pdf))
- Grantham 1986, JASA 79(6) 1939 — MAMA by source position
- Chandler & Grantham 1992, JASA 91(3) 1624 — temporal integration (~336 ms)
- Féron, Frissen, Boissinot, Guastavino 2010, JASA 128(6) 3703 — upper limit of rotation
- Roggerone, Vacher, Tarlao, Guastavino 2019, Sci Rep 9:16437 — the limit depends on spectrum ([open](https://doi.org/10.1038/s41598-019-52742-0))
- Carlile & Best 2002, JASA 111(2) 1026; Locke, Leung, Carlile 2016, Sci Rep 6:27725 — speed discrimination ([open](https://doi.org/10.1038/srep27725))
- Carlile & Leung 2016, Trends in Hearing 20 — review ([open](https://doi.org/10.1177/2331216516644254))
- Mills 1958, JASA 30(4) 237 — minimum audible angle by frequency
- Zotter & Frank 2019, *Ambisonics*, Springer, open access ([book](https://doi.org/10.1007/978-3-030-17207-7))
- Stitt, Bertet, van Walstijn 2017, JAES 65(3) 188 — off-centre listening, 3rd order ([abstract](https://pure.qub.ac.uk/en/publications/off-center-listening-with-third-order-ambisonics-dependence-of-pe/))
- Marentakis et al., ICAD 2008 — trajectory identification in a hall ([record](https://repository.gatech.edu/entities/publication/9a712595-a009-44d7-a305-cbd864a32f2f))
- Langendijk & Bronkhorst 2002, JASA 112(4) 1583 — spectral cues for elevation and front/back ([summary](https://sonicfield.org/library/contribution-of-spectral-cues-to-human-sound-localization))
- Yost & Zhong 2014, JASA — bandwidth dependence ([summary](https://labs.sonicfield.org/library/sound-source-localization-identification-accuracy-bandwidth-dependencies))
- Middlebrooks 1992, JASA 92(5) 2607; Blauert, *Spatial Hearing* — directional bands ([context](https://acris.aalto.fi/ws/portalfiles/portal/91320765/Directional_Band_ICA2022.pdf))
- Lee, ICSA 2015 — pitch-height effect ([pdf](https://eprints.hud.ac.uk/25887/1/ICSA2015_LEE_AuthorManuscript.pdf))
- Normandeau 2009, Organised Sound 14(3) — timbre spatialisation ([CUP](https://resolve.cambridge.org/core/journals/organised-sound/article/timbre-spatialisation-the-medium-is-the-space/0FC76C4A3E8EA33261DC0B95AABAC6E1)); Kim-Boyle 2008, ICMC — spectral spatialisation
- Chowning 1971, JAES 19(1) 2 — simulation of moving sources ([CCRMA](https://ccrma.stanford.edu/papers/simulation-of-moving-sound-sources))
- Kendall 2010, Organised Sound 15(3) — spatial schemata ([QUB](https://pure.qub.ac.uk/en/publications/spatial-perception-and-cognition-in-multichannel-audio-for-electr/))
- Wilson & Harrison 2010, Organised Sound 15(3) 239 — BEAST ([Wikipedia](https://en.wikipedia.org/wiki/Birmingham_ElectroAcoustic_Sound_Theatre))
- Väljamäe 2009, Brain Res. Rev. 61(2) 240 — auditory vection ([Chalmers](https://research.chalmers.se/en/publication/114917))
- Zahorik, Brungart, Bronkhorst 2005, Acta Acustica 91, 409 — distance perception
- Costa 2025, P.Porto, MSc thesis — DJ spatialisation with REAPER and IEM ([record](https://recipp.ipp.pt/entities/publication/51a8214f-a439-48a4-9a0a-bac306c0d43f))
- Stockhausen, *Kontakte* ([Wikipedia](https://en.wikipedia.org/wiki/Kontakte), [eContact](https://econtact.ca/12_4/kontakte/index.php)); Leslie speaker ([Wikipedia](https://en.wikipedia.org/wiki/Leslie_speaker))

## Club practice in 3D

- 4DSOUND, *Techno is Space — A Review* (Spatial Sound Institute): <https://spatialsoundinstitute.com/P_Techno-is-Space-A-Review>
- Molécule at the Rex Club with L-ISA (ProSoundWeb): <https://www.prosoundweb.com/molecule-brings-immersive-soundscape-to-the-rex-club-in-paris-with-l-isa/>

## Set structure and mood

- Russell's circumplex model: <https://psu.pb.unizin.org/psych425/chapter/circumplex-models/>; Mood Meter (RULER): <https://unhconnect.unh.edu/s/1518/images/gid4/editor_documents/moodmeter-2020.pdf>
- Approaching and receding sound sources (PubMed): <https://pubmed.ncbi.nlm.nih.gov/20364898/>
- Perception of objects that move in depth (ScienceDirect): <https://www.sciencedirect.com/science/article/abs/pii/S0003682X17307843>
- Looming sounds as warning signals: <https://www.researchgate.net/publication/26679267_Looming_sounds_as_warning_signals_The_function_of_motion_cues>
- The vertical symphony — pitch and spatial/affective mapping: <https://link.springer.com/article/10.1007/s10339-026-01364-2>
- Berklee, immersive audio mixing techniques: <https://online.berklee.edu/takenote/immersive-audio-mixing-techniques-how-to-create-spatial-mixes-in-dolby-atmos-and-3d-music/>
- Spatialization of Stockhausen's *Cosmic Pulses* (studio report): <https://info.ggkarman.de/sites/default/files/pdf/Garcia_Karman_COSMICPULSES.pdf>
- Smalley, *Spectromorphology: explaining sound-shapes*: <http://www.yorku.ca/vannort/smalley-spectromorphology.pdf>; OREMA on spectromorphology: <http://www.orema.dmu.ac.uk/analytical_toolbox/spectromorphology>
- The 3–2 son clave: <https://musictheory.pugetsound.edu/mt21c/ThreeTwoClave.html>; Tresillo: <https://en.wikipedia.org/wiki/Tresillo_(rhythm)>
- Dub filter sweeps and movement (Bass Culture): <https://bassculture.substack.com/p/the-heart-of-dub-filter-sweeps-and>; King Tubby: <https://en.wikipedia.org/wiki/King_Tubby>; Dub techno: <https://en.wikipedia.org/wiki/Dub_techno>
- Tension and release in EDM (Point Blank): <https://www.pointblankmusicschool.com/blog/creating-tension-and-release-in-electronic-dance-music/>
- 20 defining techniques of electronic music production: <https://soundand.design/20-defining-techniques-of-contemporary-electronic-music-production-d5ebd501d1ec>
- Panning in club tracks (Aulart): <https://www.aulart.com/blog/8-tips-for-using-panning-in-your-track/>; auto-pan (Icon Collective): <https://www.iconcollective.edu/ableton-live-auto-pan-tips>

## Documentation and manuals

How other DJ and performance manuals are built (see [writing for DJs](best-practices/documentation-for-djs.md)):

- Traktor Pro manual, basic usage tutorials: <https://docs.native-instruments.com/ni-tech-manuals/traktor-pro-manual/en/basic-usage-tutorials>
- Ableton Live manual: *Live Concepts* <https://www.ableton.com/en/manual/live-concepts/>, *Launching Clips* <https://www.ableton.com/en/manual/launching-clips/>, *First Steps* <https://www.ableton.com/en/manual/first-steps/>
- Serato hardware quickstart guides: <https://support.serato.com/hc/en-us/sections/360000031815-Quickstart-Guides>
- Pioneer DJ quick-start guides and manuals: <https://support.pioneerdj.com/hc/en-us/articles/11949532807193-Manuals>
- Elektron Digitakt quick guide: <https://www.elektron.se/wp-content/uploads/2024/09/Digitakt_Quick_Guide_ENG_230308.pdf>
- teenage engineering OP-1 field guide: <https://teenage.engineering/guides/op-1>

## Legal orientation (Pro DJ Link, 2026-10-04)

Named in the orientation that found Pro DJ Link support fine to offer under EU/German law: CJEU
*SAS Institute v World Programming* (C-406/10); §§ 69d and 69g UrhG; § 3 GeschGehG. This is a
record of what the decision rested on, not legal advice.
