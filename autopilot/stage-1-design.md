# a3-prodj, stage 1: the booth inside the sphere (design)

Written 2026-10-17 after a brainstorm with the maintainer. Repo: `a3-prodj` (GitHub a3-audio/a3-prodj, now a3-pro-dj;
checkout `<workspace>/a3-prodj`, one README commit). Background:
the pro-DJ decomposition of 2026-10-16 (see [README](README.md)), the virtual desk
(a3-mixer `feat/virtual-desk`, app a3-desk), FPV in a3-motion-ui (the workspace planning note `fpv-motion-ui.md`).
Mockups: the workspace planning note `prodj-brainstorm/` (layout A chosen).

## Intent

The maintainer, in his words: in the DJ booth, headphones on (main and booth optional), seeing the
sphere around him; "see where every sound is around me at a glance"; the mixer UI, two StemDecks and
Motion on the booth in front of him; "seeing the DJ touching faders, buttons, screens"; **watch and
operate** the booth from the pro-DJ view. And: **it is the DJ-learning tutorial for the A³ suite** — a
newcomer's first lesson ends with them able to **load a track, mix two decks, move a sound**; learners
sit **at the rig and at home on a laptop**. Linux first; macOS and Windows later.

The pro-DJ is, in the long run, a teacher and a player (autopilot / co-pilot / training, from the
decomposition). This document covers **stage 1 only**.

## Stages (decided: build in stages, rig view first)

1. **Rig view** — this document: at the rig, watch and operate the booth from inside the sphere.
2. Tutorial at the rig — the first lesson (load, mix, move) guided inside the app.
3. Laptop variant — the app brings a small local A³ (decks, mixer, Motion, binaural engine) for home.
4. Later: VR headset with head tracking (OSC, IEM SceneRotator convention); autopilot/co-pilot/training.

## Goals (stage 1)

- A first-person 3D view from the floor centre, inside the sphere; **mouse-look like an ego-shooter**
  on an ordinary screen (decided). You stand; no walking is needed (my call).
- **Every sound at a glance**: each of Motion's channels as a blob on the sphere at its azimuth/elevation,
  plus a small **radar** (top-down) for what is behind you (layout A, decided).
- **The booth as a 3D desk in the room in front of you** (layout A, decided) with four screens: StemDeck A,
  mixer, Motion, StemDeck B.
- **Real screens via screencast** (decided): StemDeck's and Motion's screens are the real devices' screens,
  live, from the MPEG-TS screencast (`a3-screencast`, TCP listener, port 9930 on the Core machine since a3-core
  b4af579; picture only, ~33 ms sender latency).
- **Control via OSC** (decided), and for StemDeck and Motion by **clicking on the screen image**
  (decided): the app sends the click's position to the device over OSC.
- **Seeing the DJ**: what the real DJ touches lights up on the 3D booth (my call for how — see below).

## Non-goals (stage 1)

- No tutorial logic, no lessons, no scoring (stage 2).
- No local audio, no engine, no running without the rig (stage 3). The app produces no audio.
- No VR/head tracking yet (stage 4) — but keep the camera's orientation in one place so an OSC head
  tracker can drive it later.
- No autopilot/co-pilot: the app never acts on a deck by itself.

## Anti-goals

- Never a second brain on a deck: the app only sends what a human does in it (a click, a fader move).
- Never send anything unasked at start-up (A³ rule: "Core asks, devices answer").
- Nothing that disturbs the live set: the screencast and OSC traffic must not load the audio machine
  (the Core machine's audio cores 1–3; the screencast runs niced on core 0).

## Constraints

- JUCE 9.0.3 + OpenGL, C++17, CMake, built and packaged like the other A³ apps (`installer/package.py`,
  `packaging/stage`, a `v*` tag before the first package); REUSE licensing like the other repos.
- Linux first (the rig's Debian, X11); keep platform-specific code thin for the later ports.
- OSC addresses come from Core's truth (`a3-osc.json`), never hard-coded — the way a3-desk and Motion
  read it (offline truth for tests; senders refuse live machines in tests).
- Relevant OSC in today's truth: `/channel/{ch}/azimuth f`, `/channel/{ch}/elevation f` (Motion → Core),
  `/vu/{n} ff` (beat-analyzer/StemDeck → Motion/mixer/radla), `/beat iif`, `/core/here sss` (Core's
  broadcast: where Core is), the desk's channel controls and `/channel/{ch}/stem/*`.
- TDD for all code (workspace rule).

## How it works (stage 1)

**Inputs the app needs** (the builder works out the exact subscription path — see "Left to the builder"):
- Motion's channel positions (azimuth, elevation) and colours; levels for blob size; the beat for a pulse.
- The mixer's state — the app is a **desk** in Core's sense: it reuses a3-desk's code (DeskState, the
  takeover ring, the wire to Core, the truth reader) and joins Core like a desk does (Core serves up to 4
  desks since the virtual-desk work).
- The two screencasts: the Core machine's (StemDeck) exists; **the Motion machine needs one for Motion** (same `a3-screencast`
  script/unit; whether a3-core or the a3-motion package ships it on the Motion machine is the builder's call).

**StemDeck A and B:** today StemDeck is one window with both decks. The two booth screens show its two
halves (crop of the one stream), or StemDeck gets two windows — my call: **crop the one stream** for
stage 1; a clicked point is mapped back to the full window's coordinates.

**Click → OSC (my call for the mechanism):** StemDeck and Motion each get a small OSC input "pointer at
x/y (normalised 0–1 of the window), down/up" that the app feeds into its own UI as a touch/mouse event
(JUCE: synthesise a MouseEvent on the top-level component). The 3D app raycasts the click onto the screen
panel, converts to the window's normalised coordinates, sends down/up (and drag moves while held). The
device stays the one that decides what the click means. New OSC addresses go into Core's truth and
a3-doc's OSC reference (the register test couples a3-core and a3-doc).

**The mixer panel:** rendered natively in the 3D booth from a3-desk's components (not a video), operated
directly — faders, pots, keys, the INPUT encoder — exactly like a3-desk.

**Seeing the DJ (my call):** whatever the real DJ moves shows in the OSC the app already receives (desk
values; Motion/StemDeck state echoed through Core); the matching control on the 3D booth glows briefly.
For touches on StemDeck's or Motion's own screens, the screencast shows them anyway. No camera, no hand
tracking.

**The sphere:** blobs in Motion's channel colours, size by level, a faint grid and horizon (floor level);
the beat as a pulse; the radar as a small top-down disc in a corner of the view (layout A). Look and feel
follow the `designer` skill (A³'s dark design language) and `dj-pro` (what a performer must see at a
glance).

## Settled after the builder check (2026-10-17)

**Decided by the maintainer:**
- **Remote clicks — any pro-DJ app, under one global state "pro-DJ LIVE".** Core holds a single global
  state, *pro-DJ LIVE*. While it is on, any pro-DJ app on the rig network may operate (pointer clicks into
  StemDeck/Motion, the mixer panel); while it is off, the devices ignore pro-DJ pointer input and the app
  only watches. Every device shows the state where the eye already goes (StemDeck, Motion, the desks), so
  nobody is surprised by a remote hand. No per-device or per-app arming. Who switches it, and where the
  switch sits, is for the plan (proposal: on the pro-DJ app and on the desk; Core is the one truth, devices
  answer Core — "Core asks, devices answer").

**My calls (the maintainer may overrule):**
1. **The mixer code is shared, not copied.** a3-prodj starts after the virtual desk (`a3-mixer
   feat/virtual-desk`) is merged; the desk's non-UI core (truth reader, DeskState with grab and the
   takeover ring, the wire to Core, meters) becomes a library in a3-mixer that a3-prodj consumes as a
   pinned submodule. The app takes one of Core's four desk slots.
2. **Positions and levels reach the app through Core.** Today `/channel/{ch}/azimuth|elevation` go Motion
   → Core only, and `/vu` only to Motion/mixer/radla. Stage 1 therefore includes an a3-core change: Core
   announces Motion's positions and the meters to its followers through its existing follower model (no
   second, parallel relay). Truth change → a3-doc's OSC reference in the same merge (register test).
3. **Channel colours:** a fixed palette like Motion's default skin (quiet-indigo-2); the maintainer's skins
   are never read or written.
4. **The screencast serves several viewers.** Today each listener takes one viewer (OBS holds StemDeck's);
   stage 1 changes `a3-screencast` so a second viewer (the app) costs no second encode (e.g. one encoder,
   several outputs/multicast) — the builder picks the mechanism, measured on the Core machine core 0.
5. **The app never runs on the Core machine** (the audio machine): the development server, the Motion machine or a laptop at the rig.
6. **Motion's screencast on the Motion machine is part of stage 1**, shipped with the a3-motion-ui package (a3-core is
   not installed on the Motion machine).
7. **Remote pointer input** in StemDeck and Motion is its own input source (its own index), separate from
   the touchscreen's touch and emulated mouse (JUCE + X sends every touch twice; A³ rule), and only active
   while *pro-DJ LIVE* is on.
8. **StemDeck crop:** StemDeck's window is fixed (768×1024 portrait panel); the two deck halves are fixed
   regions of that frame. If the window size ever changes, the stream must carry its size.

## Left to the builder

- The exact way the app receives Motion's positions and the levels (Core relays them to followers? a
  subscription like the desk's? listening on Motion's port?) — pick the one that fits Core's follower
  model; do not add a second relay.
- Video decoding (FFmpeg/libav through JUCE or GStreamer) and the texture upload path; target ≥ 30 fps
  on the rig's NUC-class machine without touching the audio cores.
- Mouse-look feel (sensitivity, invert, pointer capture), field of view, how to "click a screen" while in
  mouse-look (e.g. a crosshair click, or holding a key to free the pointer).
- Window/full-screen handling, where the app runs (the development server, the Motion machine, a laptop at the rig).
- Packaging details and the installer role (if any).

## Open (to settle in planning, not blocking the design)

- Where the *pro-DJ LIVE* switch sits and how each device shows it.
- Whether StemDeck later gets two real windows instead of the cropped stream.
