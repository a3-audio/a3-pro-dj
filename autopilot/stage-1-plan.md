# a3-prodj stage 1 (the booth inside the sphere) — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A JUCE/OpenGL app, a3-prodj, that stands you at the floor centre inside the sphere at the rig.
- You see every channel as a blob at Motion's azimuth/elevation, with a radar for what is behind you.
- In front of you stands the booth: StemDeck A, the mixer, Motion and StemDeck B, the first three of them live
  screens.
- You can watch, and while *pro-DJ LIVE* is on, you can operate.

**Architecture:**
- **Core.** Core follows the app as a desk of kind `prodj`. It relays Motion's positions only to such desks, tells
  them where Motion and StemDeck run, and holds the single global *pro-DJ LIVE* state. It announces that state as a
  lease, forwards pointer clicks to StemDeck/Motion only while LIVE is on, and refuses a prodj's mixer values while
  it is off.
- **The mixer panel** is a3-desk's own `DeskComponent`, compiled from a3-mixer (pinned submodule) and rendered
  offscreen into a texture.
- **The screens** are the devices' screencasts. They are decoded by an `ffmpeg` child process into PPM frames.
  `a3-screencast` becomes one encoder with a fan-out to several viewers.
- **Pure units** carry every decision: geometry, camera, input, pointer, glow, PPM, LIVE gate. Thin JUCE/GL classes
  sit on top.

**Tech Stack:**
- C++17 + JUCE 9.0.3: `juce_gui_basics`, `juce_opengl`, `juce_osc`, `juce_cryptography`.
- GoogleTest, CMake.
- Python 3 stdlib (a3-core, the screencast fan-out, the umbrella).
- `ffmpeg` as a runtime tool (already a3-core's Depends).
- Sphinx (a3-doc).

**Spec:** `[stage-1-design.md](stage-1-design.md)`.
- "Settled after the builder check" is binding: the maintainer's *pro-DJ LIVE* and calls 1–8.
- Background: the pro-DJ decomposition (see [README](README.md)), the virtual-desk plan
  the workspace planning note `2026-10-17-virtual-desk-plan.md` (its lines 1–298 describe a3-desk's structure) and its ledger
  the workspace planning note `virtual-desk-ledger/progress.md` (rulings that shaped the code this plan builds on).
- Executors read the spec beside this plan.

## Changes against the design (found while planning; read before Task P1)

1. **The screencast shows the whole screen, not a window.**
   - `a3-screencast` grabs the X screen (`x11grab`, `xdpyinfo` size). The design's "pointer at x/y, normalised 0–1
     of the window" would not match the picture the app clicks on.
   - **Resolution:** pointer coordinates are a share of the **screen picture** (0,0 top-left). Each device maps
     them onto its own top-level window (`screenToWindow`) and ignores a point outside it.
   - The stream carries its size anyway: every decoded PPM frame states width and height. Call 8's "the stream must
     carry its size" therefore needs no protocol, and the StemDeck crops are shares of the frame.
2. **The meters already reach every desk.**
   - Since the virtual desk, `core.vu-relay` forwards the analyzer's and StemDeck's `/vu` to every desk on
     `desk.vu`. The app gets the levels as a desk, through `DeskComponent`'s `DeskMeters`.
   - **Only the positions are new.** Core relays them **only to desks of kind `prodj`**. At 60 Hz × 4 channels × 2
     words, a plain desk has no use for them (A³ rule "Desk lag = position flood").
3. **`installer/package.py` exports with `git archive`, which leaves submodules out.**
   - Call 1's pinned submodule would build an empty `external/a3-mixer`.
   - **Resolution:** Task P3 teaches `package.py` to archive submodules at their pinned commits, from the local
     checkout (no network).
4. **One desk per machine.**
   - `DeskLink` binds `desk.osc` exclusively (virtual-desk change #2), and Core keys desks by host. a3-prodj and
     a3-desk therefore cannot both run on one machine.
   - **Resolution:** accepted for stage 1. The app shows the desk's own "another desk runs on this machine" status
     and only watches. The smoke test runs a3-desk and the app on different machines.
5. **"Every device shows the state … the desks."**
   - Covered: StemDeck, Motion, a3-desk (the virtual desks) and the app itself.
   - **Not covered: the hardware A3 Mixer.** Its Python OLED code has no place designed for it, and the DJ's eye
     at the booth is on Motion's and StemDeck's screens. Issue text for the maintainer is at the end of Task M2.
6. **Call 6 (the Motion machine's screencast ships with a3-motion-ui) and DRY.**
   - The script and its fan-out live in a3-core. a3-motion-ui ships a vendored copy, held byte-equal by a test
     that compares with a3-core beside the checkout. This is the same arrangement as the desk's `shared/`.
   - **Resolution:** extract it later, with the a3-osc-cpp extraction. Issue text is in Task P2.
7. **"Core asks, devices answer" vs. a LIVE that must end.**
   - A device that missed the "off" (Core restart, network drop, eno1 flaps) would keep showing LIVE and keep
     accepting pointers.
   - **Resolution:** LIVE is a **lease**. While on, Core repeats `/prodj/live 1` every 5 s to the devices it
     announces to. A device falls back to off 12 s after the last "on".
   - Core never sends LIVE unasked at start-up: it starts off, and it answers hello/recall. It repeats only while a
     human has switched LIVE on.
8. **Video decoding.**
   - The design leaves FFmpeg/libav or GStreamer open. Linking libav would add build dependencies (`libav*-dev`).
   - **Resolution:** an `ffmpeg` child process decoding to PPM on stdout. That adds no build dependency, only the
     runtime `Depends: ffmpeg` that the rig already has.
   - **This is a dependency decision. The executor asks the maintainer before Task J7** (Global Constraints).
9. **`DeskComponent::setLocked` only guards the master pots.**
   - Watching needs "no hands at all".
   - **Resolution:** Task M1 adds `setHandsWithheld(bool)`.
10. **Where the LIVE switch sits (design "Open"):**
    - the app (key `L` and its HUD chip);
    - a3-desk's status line (a tap toggles it);
    - Motion's status-bar badge (a tap switches it **off** only: the safety exit where the DJ's hands are).
    - StemDeck only shows it.
    - Core switches it off by itself when the last prodj desk goes silent.
11. **Crop of StemDeck.**
    - StemDeck's surface is deck A | mixer | deck B under shared waveforms (`SurfaceLayout.h`). "Its two halves" are
      the **left and right halves** of the frame: `{0,0,0.5,1}` and `{0.5,0,0.5,1}`.

**Found while planning, not part of this plan:** none beyond the issue texts in P2 and M2.

## Not in this plan

- Tutorial, lessons, scoring (stage 2); local audio/engine (stage 3); VR/head tracking (stage 4). Only `Orientation`
  is kept in one place for it.
- An installer role for a3-prodj, a3-prodj in the umbrella's submodules, a3-prodj on the LAN builder (the development server).
  These are the maintainer's, after the smoke test.
- macOS/Windows builds.
- StemDeck with two real windows (design "Open").

## Global Constraints

- **TDD:**
  - Every unit gets its failing test first, and the test fails on an assertion. Where an include or import would
    fail, write a stub first.
  - Source-reading wiring tests (a3-core) may go RED by `StopIteration` (virtual-desk ruling P11).
  - Use `superpowers:test-driven-development`.
- **Builds run at `nice -n 19`, `-j2`.** Never build on the Core machine while the rig plays.
- **Git:**
  - Stage files by name, never `git add -A` or `git add .`.
  - Conventional Commits in English, **no trailers** (no Co-Authored-By, no Claude-Session).
  - Work on a branch in a worktree under `wt/<repo>/<branch>`. **Never merge, never push, never tag.**
  - **Never GitHub:** no `gh`, no git against `origin`, no clone or fetch from github.com. The submodule in J1 is
    added from the local checkout.
  - Before branching in any repo, run `git status` there and report uncommitted work. `a3-motion/ui` carries the
    maintainer's `config/config.json` and `config/skins/*` edits: never touch, stage, stash or reset them.
- **Read only, always:** REAPER projects (`*.RPP`), the patchbay, `config/skins/*` and `config/config.json`
  (a3-motion-ui). The channel palette (Task J3) is **copied as four constants**; no skin is read at runtime.
- **Tests never send OSC to a live machine:**
  - Every test runner calls `a3::refuseOscSenders()` (or the repo's equivalent) first.
  - `test.sh` hands an offline truth (`a3-offline-truth`, every named host → 192.0.2.x).
  - Socket tests bind port 0.
  - No test opens a TCP connection to a screencast port.
- **One truth:**
  - Every address, port and host comes from a3-core's `a3-osc.json`.
  - New words: `prodj.live`, `stemdeck.pointer`, `motion.pointer`, `core.device-at` (Task C1).
  - a3-core's `tools/second_truth.py` scans a3-prodj from C1 on. No literal port or our-word address goes in
    a3-prodj, StemDeck or Motion code.
- **Coupled merges:**
  - A truth change merges with a3-doc's re-rendered `src/ressources/osc.md`/`ports.md`, made on a paired branch in
    the same task.
  - The register only counts in the main checkout (`<workspace>/a3-core`, branch checked out detached; workspace rule
    "worktree runs skip the register").
- **The app never runs on the Core machine** (call 5): it refuses to start there (Task J1). It runs on the development server, the Motion machine or a
  laptop at the rig.
- **Core asks, devices answer:**
  - Nothing is sent unasked at start-up, by any party.
  - The only repeat is the LIVE lease while on (change #7).
  - Pointers and mixer values go out only from a human's hand in the app.
- **No new dependency without the maintainer's yes:**
  - Task J7 needs `ffmpeg` at runtime (ask first).
  - a3-motion-ui gains `Depends: ffmpeg` in P2 (ask together).
  - Nothing else is added.
- **JUCE 9.0.3, C++17, CMake** as a3-desk/stemdeck build them: `find_package(JUCE 9.0.3 CONFIG REQUIRED)`,
  `CMAKE_PREFIX_PATH=$HOME/local/juce`, ccache when present, `-Werror=switch`.
- **Every touch arrives twice** (JUCE 9.0.3 + X: `touch#0` and emulated `mouse#0` per finger).
  - The injected remote pointer is its **own** touch source, `remoteTouchIndex = 9`, never index 0.
  - The app itself acts on mouse-type sources only.
- **UI tasks** (P4 badge, P5 badge, M2 chip, J3 palette, J8 scene/HUD): load the `designer`, `dj-pro` and
  `juce-pro` skills before any colour, size or control choice. Sizes are shares of what they hang on, never pixels
  (A³ rule "No pixel design").
- **License headers:**
  - Every new file carries SPDX (`GPL-3.0-or-later` for code, `CC-BY-SA-4.0` for docs, `CC0-1.0` for trivial
    data).
  - Copied files keep their holder line and gain SPDX.
  - a3-prodj gets `.reuse/dep5` and `LICENSES/`.
- **Test commands:**
  - a3-core: `python3 -m unittest discover -s tools/tests` (the venv, never bare `python3`).
  - a3-doc: `~/.venv-docs/bin/sphinx-build src doc` (0 warnings).
  - StemDeck: `nice -n 19 cmake --build build -j2 && ctest --test-dir build --output-on-failure`.
  - Motion UI: `nice -n 19 ./test.sh`; its tools: `python3 -m unittest discover -s tools/tests`.
  - a3-mixer desk: from `app/`, `A3_OSC_TRUTH=<core truth> ./test.sh`.
  - a3-prodj: `A3_OSC_TRUTH=<core truth> ./test.sh`.
  - Umbrella: `python3 -m unittest discover -s tests`.
  - `<core truth>` until C1 merges:
    `<workspace>/wt/a3-core/feat/prodj-in-core/platform-config/debian-x86_64/a3-core/usr/share/a3/a3-osc.json`.
- **"Green" carries a timestamp:** quote the runner's build time from `test.sh`. A CMake configure error is not a
  red test.

## Review Focus

The five failure modes most likely to bite a person, each pinned by a test in the task named:

1. **LIVE ends under a held remote finger** (switched off, Core restarted, network gone): the device must not keep
   a press down.
   - Expected: a release at once on "off", and a release when the lease runs out (12 s).
   - *Pinned in P4/P5* (`RemotePointerGate.GoingOffMidDragReleases`, `RemotePointerGate.TheLeaseRunsOut`) *and J5*
     (`PointerOut.GoingOffWhileHeldSendsUp`).
2. **A lost "up" datagram.** UDP drops one, and StemDeck/Motion would hold a touch forever.
   - Expected: the app sends a keep-alive move every 250 ms while held, and a device releases a pointer silent for
     1 s.
   - *Pinned in P4/P5* (`RemotePointerGate.ASilentHeldPointerIsReleasedAfterOneSecond`) *and J5*
     (`PointerOut.AHeldPressKeepsAliveEvery250ms`).
3. **The real DJ's finger and the remote pointer at once** on Motion's screen.
   - Expected: two grabs, neither steals the other's channel.
   - *Pinned in P5* (`TouchGrabs.ARemotePointerKeepsItsOwnGrab`).
4. **A pro-DJ app while LIVE is off moves the room anyway.** A stale build or a second app on the network sends
   mixer values.
   - Expected: Core refuses a prodj's values and pointers while off, and the panel takes no hand.
   - *Pinned in C2* (`test_a_prodj_moves_nothing_while_off`), *C3* (`test_values_refused_asks_the_live_gate`) *and
     M1* (`DeskComponent.NoHandsWhileWithheld`).
5. **A second screencast viewer, or a slow one** (the app on Wi-Fi), must not stall OBS or the encoder.
   - Expected: one encoder whatever the number of viewers; a viewer that falls 4 MB behind is dropped, never waited
     for.
   - *Pinned in P1* (`test_a_second_viewer_costs_no_second_encoder`, `test_a_slow_viewer_is_dropped_not_waited_for`).

---

## Phases, branches, worktrees

| Phase | Task | Repo | Branch | Worktree | Before the desk merge? |
|---|---|---|---|---|---|
| 0 | — | — | **gate: the virtual desk is merged** | — | — |
| 1 | P1 | a3-core | `feat/screencast-viewers` | `wt/a3-core/feat/screencast-viewers` | **yes** |
| 1 | P2 | a3-motion-ui | `feat/screencast-on-motion` | `wt/a3-motion-ui/feat/screencast-on-motion` | **yes** (after P1's commit) |
| 1 | P3 | a3-system (umbrella) | `feat/package-submodules` | `wt/a3-system/feat/package-submodules` (by hand: `git -C <workspace> worktree add wt/a3-system/feat/package-submodules -b feat/package-submodules`) | **yes** |
| 1 | P4 | stemdeck | `feat/remote-pointer` | `wt/stemdeck/feat/remote-pointer` | **yes** |
| 1 | P5 | a3-motion-ui | `feat/remote-pointer` | `wt/a3-motion-ui/feat/remote-pointer` | **yes** |
| 2 | C1–C3 | a3-core | `feat/prodj-in-core` | `wt/a3-core/feat/prodj-in-core` | no |
| 2 | C1 | a3-doc | `docs/prodj-in-core` | `wt/a3-doc/docs/prodj-in-core` | no |
| 2 | M1–M2 | a3-mixer | `feat/desk-library` | `wt/a3-mixer/feat/desk-library` | no |
| 2 | J1–J9 | a3-prodj | `feat/stage-1` | `wt/a3-prodj/feat/stage-1` | no (J1 needs M1) |
| 3 | D1 | a3-doc | `docs/prodj-stage-1` | `wt/a3-doc/docs/prodj-stage-1` | no |
| 3 | S1 | workspace | — | `smoke-test/prodj-stage-1.md` | no |

Create the worktrees with the workspace's `new-worktree.sh <repo> <branch>`, run from
`<workspace>`. The umbrella is the exception (see the table).

**Phase 0 (gate, no task).** None of Phase 2 starts before the maintainer has passed `smoke-test/virtual-desk.md`
and merged the five desk branches:
- a3-core `feat/desk-followers` with a3-doc `docs/desk-followers`;
- stemdeck `feat/meters-to-the-relay`;
- a3-mixer `feat/virtual-desk`;
- umbrella `feat/desk-role`.

Phase 2 branches from the mains **after** that merge.

Why Phase 1 is independent:
- P1–P3 touch none of the desk's files.
- P4/P5 read the new words as **optional** truth keys, so they work (inertly) against today's truth.
- P5 touches `OscMessageHandler`, which the desk's Phase E later shrinks. Whoever merges second rebases; the
  conflict is local to the listener list.
- Core's LIVE (C2/C3) needs `DeskFollowers` and is therefore Phase 2. Only its pure module would fit before, and it
  is too small to be worth a stacked branch.

**Merge order (the maintainer's):**
1. a3-core `feat/screencast-viewers` (P1), any time. Deploy on the Core machine and check that OBS still gets its picture.
2. a3-motion-ui `feat/screencast-on-motion` (P2), after 1: its vendored copy must equal merged a3-core. Then
   a3-motion pins ui.
3. umbrella `feat/package-submodules` (P3), any time.
4. stemdeck `feat/remote-pointer` (P4) and a3-motion-ui `feat/remote-pointer` (P5), any time. They stay inert
   until 6 gives the words.
5. **Gate: the virtual desk merged** (Phase 0).
6. a3-core `feat/prodj-in-core` **together with** a3-doc `docs/prodj-in-core` (C1–C3; the register and the
   rendered tables).
7. a3-mixer `feat/desk-library` (M1–M2), after 5. M2's chip reads an optional key, so it works before 6 too.
8. a3-prodj `feat/stage-1` (J1–J9), after 7 and 3.
   - **Before merging,** the maintainer moves the submodule pin to the a3-mixer **main** commit that carries M1/M2
     (`git -C external/a3-mixer checkout <main sha>`, commit `chore: pin a3-mixer`).
   - **After merging, the maintainer tags `v03.0` on a3-prodj's main.** `package.py` refuses an untagged repo
     (`debian_version`).
9. a3-doc `docs/prodj-stage-1` (D1), after 8.
10. **Smoke test `smoke-test/prodj-stage-1.md`** on the rig, run by the maintainer (Task S1).

## File map

**a3-core** (`PKG/` = `platform-config/debian-x86_64/a3-core/`, `LOCAL/` = `PKG~/.local/`)
- P1:
  - create `LOCAL/lib/a3_screencast_fanout.py`;
  - modify `LOCAL/bin/a3-screencast` (ffmpeg → stdout → fan-out);
  - tests: create `tools/tests/test_screencast_fanout.py`, modify `tools/tests/test_package_screencast.py`.
- C1:
  - modify `PKG/usr/share/a3/a3-osc.json`, regenerate `LOCAL/share/a3-core/osc-register.json`;
  - modify `tools/second_truth.py`;
  - create `tools/tests/test_prodj_in_the_truth.py`, modify `tools/tests/test_osc_register.py`.
- C2:
  - modify `LOCAL/lib/a3_core_desks.py` (kinds);
  - create `LOCAL/lib/a3_core_prodj_live.py`;
  - tests: modify `test_core_desks.py`, create `test_core_prodj_live.py`.
- C3: modify `LOCAL/bin/a3-core.py`; create `tools/tests/test_core_prodj_wiring.py`.

**a3-doc**
- C1: `src/ressources/osc.md`, `ports.md` (re-rendered).
- D1: create `src/user/prodj.md`, add it to the user toctree.

**umbrella** — P3: modify `installer/package.py`, `tests/test_package.py`.

**stemdeck** — P4:
- create `Source/RemotePointer.h/.cpp` (pure) and `Source/PointerInjector.h/.cpp`;
- modify `Source/Remote.h/.cpp` (`Words` gains `pointer`, `live`), `Source/RemoteLink.h/.cpp`,
  `Source/OscTruthFile.cpp` (optional keys), `Source/MainComponent.h/.cpp` (badge);
- tests: `tests/RemotePointer.cpp`, `tests/Remote.cpp`.

**a3-motion-ui**
- P2:
  - create `platform_config/screencast/a3-screencast`, `platform_config/screencast/a3_screencast_fanout.py`
    (vendored), `platform_config/a3-motion-screencast` (truth → port → exec);
  - create `platform_config/a3-motion-screencast.service`;
  - modify `packaging/stage`, `packaging/DEBIAN/control`;
  - tests: `tools/tests/test_screencast_on_motion.py`.
- P5:
  - create `src/a3-motion-ui/components/RemotePointer.{hh,cc}` and `PointerInjector.{hh,cc}`;
  - modify `src/a3-motion-engine/OscAddresses.{hh,cc}` (optional `prodjLive`, `motionPointer`),
    `src/a3-motion-ui/osc/OscMessageHandler.{hh,cc}`, `A3MotionUIComponent.{hh,cc}`, `StatusBar`/`StatusBarLayout`
    (badge);
  - tests: `unit/RemotePointer.cc`, `unit/TouchGrabs.cc`, `unit/OscMessageHandler*.cc`.

**a3-mixer** (`app/`)
- M1:
  - create `app/cmake/A3DeskSources.cmake`;
  - modify `CMakeLists.txt`, `tests/CMakeLists.txt`, `Source/DeskComponent.h/.cpp`, `Source/DeskWire.h/.cpp`;
  - tests in `DeskComponentTests.cpp`, `DeskWireTests.cpp`.
- M2:
  - modify `Source/DeskOsc.*`, `DeskInbox.*`, `DeskWire.*`, `DeskIndicatorsUi.*` (StatusLine), `DeskComponent.*`;
  - tests alongside.

**a3-prodj** (new tree)

```
.gitmodules                 external/a3-mixer -> https://github.com/a3-audio/a3-mixer
external/a3-mixer           submodule (added from the local checkout)
CMakeLists.txt              A3Prodj app + a3-prodj-tests; a3-mixer's desk sources via A3DeskSources.cmake
test.sh                     nice 19 build, offline truth (external/a3-mixer/app/tools/a3-offline-truth), xvfb ctest
.reuse/dep5, LICENSES/      GPL-3.0-or-later, CC-BY-SA-4.0, CC0-1.0
Source/
  ProdjOsc.h/.cpp           the app's own words from the truth; pointer/live messages
  RunsHere.h/.cpp           refuse to run on Core's machine
  SceneState.h/.cpp         positions, LIVE, device hosts, beat pulse
  ProdjInbox.h/.cpp         desk.osc messages -> SceneState (+ Glow); the rest go to DeskComponent
  Palette.h                 the four channel colours (copied constants)
  Sphere.h/.cpp             direction of az/el, blob radius, radar point, scene model
  Camera.h/.cpp             Orientation (the head tracker's one place), rays, matrices
  ViewInput.h/.cpp          mouse-look state machine
  Booth.h/.cpp              booth layout, ray -> panel hit
  BoothScreens.h/.cpp       panel ids, crops, panel uv -> device picture share
  PointerOut.h/.cpp         hits -> pointer sends (throttle, keep-alive, LIVE)
  PanelPointer.h/.cpp       synthetic mouse into the offscreen DeskComponent
  Glow.h/.cpp               which mixer control glows, and how much
  PpmStream.h/.cpp          PPM frame parser
  FrameMailbox.h/.cpp       latest-frame handover, decoder thread -> GL thread
  ScreencastReader.h/.cpp   ffmpeg child process + thread
  SceneRenderer.h/.cpp      OpenGL: grid, horizon, blobs, booth, textures
  HudComponent.h/.cpp       radar, crosshair, LIVE chip, status (JUCE paint over GL)
  ProdjComponent.h/.cpp     owns everything; input routing
  Main.cpp                  app, window, truth keeper, links, readers
tests/  CMakeLists.txt, TestRunner.cpp, one *Tests.cpp per unit
packaging/stage, packaging/DEBIAN/{control,postinst,prerm,postrm}, packaging/a3-prodj.desktop
```

**workspace** — S1: `smoke-test/prodj-stage-1.md`.

## Shared definitions (used across tasks; implement exactly)

**Pointer on the wire.**
- Messages: `/stemdeck/pointer iff` and `/motion/pointer iff`. Arguments: `phase` (0 down, 1 move, 2 up), `x`,
  `y` (share of the device's **screen picture**, 0..1 from top-left).
- Path: app → Core (`core.osc`) → device. Core forwards only while LIVE is on and only from a desk of kind
  `prodj`.

**LIVE on the wire.**
- Message: `/prodj/live i` (1 on, 0 off).
- Who switches: the app, a3-desk and Motion send it to Core. Motion only ever sends 0.
- Who announces: Core sends it to every followed desk (kind desk or prodj), Motion and StemDeck:
  - on every change;
  - in answer to a hello or recall;
  - every 5 s while on (the lease).
- Devices: off at start; off 12 s after the last "on".

**Device-side gate** (P4 and P5 implement it identically, each in its own namespace: `remote` in StemDeck, `a3` in
Motion):

```cpp
struct PointerEvent { enum class Phase { down, move, up }; Phase phase; float x, y; };
std::optional<PointerEvent> parsePointer (int phase, float x, float y);   // phase 0..2, finite, 0<=x,y<=1, else nullopt
struct Inject { PointerEvent::Phase phase; float x, y; };
class RemotePointerGate
{
public:
    static constexpr double releaseAfterMs = 1000.0, liveLeaseMs = 12000.0;
    std::vector<Inject> live (bool on, double nowMs);                    // off while held -> { up at last x,y }
    std::vector<Inject> pointer (const PointerEvent& e, double nowMs);  // nothing while off; move/up without down -> nothing;
                                                                         // down while held -> { up, down }
    std::vector<Inject> tick (double nowMs);   // lease out -> off (+ up if held); held and silent > 1 s -> up
    bool isLive (double nowMs) const;
    bool held() const;
};
std::optional<juce::Point<float>> screenToWindow (juce::Point<float> share, juce::Rectangle<float> screen,
                                                  juce::Rectangle<float> window);   // window-local point, nullopt outside
constexpr int remoteTouchIndex = 9;
```

Injection: `peer->handleMouseEvent (juce::MouseInputSource::InputSourceType::touch, local, mods, 1.f, 0.f, timeMs,
{}, remoteTouchIndex)`.
- `mods` is `leftButtonModifier` for down and move, none for up.
- The screen is `Desktop::getDisplays().getDisplayForRect (window)->totalArea`.
- The window is the top-level peer's bounds.

---

## Phase 1 — before the desk merge

### Task P1: the screencast serves several viewers from one encoder (a3-core)

**Files:**
- Create: `LOCAL/lib/a3_screencast_fanout.py`
- Modify: `LOCAL/bin/a3-screencast`
- Test: `tools/tests/test_screencast_fanout.py` (new), `tools/tests/test_package_screencast.py` (adapt)

**Interfaces:**
- Produces:
  - `class Fanout(limit_bytes=4*2**20, max_viewers=8)`. Methods:
    - `add(viewer) -> bool` (False when full);
    - `feed(chunk: bytes) -> list[viewer]` (the viewers dropped for falling behind);
    - `pending(viewer) -> bytes` / `sent(viewer, n)`;
    - `remove(viewer)`;
    - `viewers() -> list`.
  - `class EncoderGate(linger=10.0)`: `wanted(viewer_count: int, now: float) -> bool`. True from the first viewer;
    False once there have been none for `linger` s.
  - `serve(listen_socket, start_encoder: Callable[[], subprocess.Popen], clock=time.monotonic)`. A `selectors`
    loop: accept, read the encoder's stdout, write to viewers, start/stop by `EncoderGate`.
  - `main(argv)` reads `A3_SCREENCAST_PORT` and the encoder command from argv.
  - P2 vendors this file byte for byte. Keep it stdlib-only and free of a3-core imports.

- [ ] **Step 1: Write the failing tests** in `test_screencast_fanout.py`:
  - `test_every_viewer_gets_every_chunk`: two viewers, `feed(b"ab")`; `pending` is `b"ab"` for both.
  - `test_a_slow_viewer_is_dropped_not_waited_for`: `Fanout(limit_bytes=10)`, one viewer never `sent`;
    `feed(b"x"*11)` returns that viewer, and `viewers()` no longer has it.
  - `test_a_ninth_viewer_is_refused`: `max_viewers=8`; the 9th `add` is False.
  - `test_the_encoder_starts_with_the_first_viewer_and_lingers`: `EncoderGate(linger=10)` gives:
    - `wanted(0,0)` False;
    - `wanted(1,1)` True;
    - `wanted(0,5)` True;
    - `wanted(0,11.1)` False.
  - `test_a_second_viewer_costs_no_second_encoder`: `serve` on a port-0 socket, `start_encoder` a fake that writes
    `b"TS"` repeatedly (`[sys.executable, "-c", ...]`). Two TCP clients each read `b"TS"`, and the fake was started
    **once**. The loop stops via a stop event the test sets.
  - `test_the_encoder_stops_when_the_last_viewer_has_gone`: as above with `linger=0.2`; after both clients close
    and 0.5 s, the fake process has been terminated.

  In `test_package_screencast.py`:
  - `test_the_script_has_no_port_number_of_its_own` now looks at the fan-out line (`A3_SCREENCAST_PORT` reaches the
    fan-out; no 4–5 digit literal).
  - `test_ffmpeg_writes_to_stdout`: the ffmpeg line ends in `-f mpegts pipe:1`; `listen=1` is gone.
  - `test_the_fanout_runs_niced_on_the_free_core`: `nice -n 19 taskset -c "$CPUS"` precedes the Python call.
  - Keep every existing assertion that still describes the script: no GPU, `-an`, the latency flags, `-g`, core 0.
- [ ] **Step 2: Run them:** `python3 -m unittest tools.tests.test_screencast_fanout tools.tests.test_package_screencast` (from `tools/..` per the suite's discovery). Expected: FAIL (module missing → write a stub module first so RED is an assertion).
- [ ] **Step 3: Implement.**
  - **`a3_screencast_fanout.py`:**
    - Non-blocking sockets, one `selectors.DefaultSelector`.
    - A viewer's pending bytes are a `bytearray`; one over `limit_bytes` is closed and dropped.
    - The encoder is a `Popen(stdout=PIPE)`, read in 64 KiB chunks. When it exits while viewers wait, start it again
      after 2 s.
    - Stop is `terminate()`, then `kill()` after 2 s.
  - **`a3-screencast`:**
    - ffmpeg as today but `-f mpegts pipe:1`, launched by the fan-out:
      `exec nice -n 19 taskset -c "$CPUS" python3 -I "$HOME/.local/lib/a3_screencast_fanout.py" --port "$A3_SCREENCAST_PORT" -- ffmpeg …`.
    - The comment says "several viewers, one encode".
  - Unit text: `Description=` → "The picture of this machine's screen for OBS and the pro-DJ (MPEG-TS, several
    viewers)". `Restart=always` stays.
- [ ] **Step 4: Run the whole a3-core suite** (venv). Expected: all OK, the two new files included.
- [ ] **Step 5: Measure on the workstation, not the rig.**
  - Run the script with `DISPLAY` set and two `ffplay tcp://127.0.0.1:<port>` viewers.
  - Note the ffmpeg CPU with one vs. two viewers in the commit body (expected: equal).
  - The rig measurement on core 0 is S1's.
- [ ] **Step 6: Commit** `feat(screencast): one encoder, several viewers, started by the first and stopped after the last` — files by name.

### Task P2: Motion's screen as a screencast on the Motion machine (a3-motion-ui)

**Files:**
- Create:
  - `platform_config/screencast/a3-screencast` and `platform_config/screencast/a3_screencast_fanout.py` (copies of
    P1's, SPDX kept);
  - `platform_config/a3-motion-screencast` (Python, stdlib);
  - `platform_config/a3-motion-screencast.service`.
- Modify: `packaging/stage` (`files`: install the three scripts to `usr/lib/a3-motion-ui/`, the unit to
  `usr/lib/systemd/user/`), `packaging/DEBIAN/control` (`Depends: … ffmpeg` — maintainer's yes first).
- Test: `tools/tests/test_screencast_on_motion.py`

**Interfaces:**
- Consumes: P1's fan-out (`main(argv)`) and the script's settings (`A3_SCREENCAST_PORT`, `_CPUS`, `_FPS`, `_CRF`).
- Produces: `a3-motion-screencast`, which does three things:
  - finds the truth in the order Motion reads it: `$A3_OSC_TRUTH`, `~/.cache/a3/a3-osc.json`,
    `/usr/share/a3/a3-osc.json`;
  - reads the `screencast`/`stream` listener's port;
  - `exec`s the vendored `a3-screencast` with `A3_SCREENCAST_PORT` set.

  Without a truth it exits 1 with "no a3-osc.json yet — Motion fetches it from Core". The unit then retries.

- [ ] **Step 1: Write the failing tests:**
  - `test_the_vendored_files_equal_a3_cores`: byte-compare both files with
    `../../a3-core/platform-config/.../a3-screencast` and `.../lib/a3_screencast_fanout.py`. `skipTest` when a3-core
    is not beside the checkout.
  - `test_the_port_comes_from_the_truth`: with a temp truth whose `screencast.stream` port is 4321, the function
    `port_from(truth_path)` returns 4321.
  - `test_the_truth_is_found_in_motions_order`: `truth_path(env, home)` prefers `A3_OSC_TRUTH`, then the cache, then
    `/usr/share`.
  - `test_the_unit_is_not_enabled_by_the_package`: postinst does not name `a3-motion-screencast`.
  - `test_the_unit_restarts`: `Restart=always`, `RestartSec=2`, `StartLimitIntervalSec=0`, `Environment=DISPLAY=:0`,
    and `ExecStartPre=/usr/lib/a3-motion-ui/a3-wait-for-the-screen`.
  - `test_stage_ships_the_screencast`: `packaging/stage`'s `files` installs all three under `usr/lib/a3-motion-ui/`
    with mode 755 (two) / 644 (the module).
- [ ] **Step 2: Run** `python3 -m unittest discover -s tools/tests -p 'test_screencast_on_motion.py'` → FAIL.
- [ ] **Step 3: Implement.** `a3-motion-screencast` exposes `truth_path(env, home)` and `port_from(path)`; `main()`
  wires them and `os.execve`s. The unit mirrors a3-core's (opt-in, `WantedBy=default.target`).
- [ ] **Step 4: Run the tools suite and `nice -n 19 ./test.sh`** (packaging only, but the stage is shared). Expected: green, with the runner timestamp.
- [ ] **Step 5: Commit** `feat(packaging): Motion's screen as a screencast on its own machine, opt-in`.

**Issue text for the maintainer (a3-system), file after merge:**
> **Title:** a3-screencast is vendored into a3-motion-ui
> **Symptom:** the script and its fan-out exist twice (a3-core, a3-motion-ui `platform_config/screencast/`).
> **Finding:** the Motion machine has no a3-core (design call 6); a test holds the copies equal when both checkouts sit side by side.
> **Next step:** move it into the shared package that the a3-osc-cpp extraction creates.
> Labels: enhancement.

### Task P3: `package.py` exports submodules at their pins (umbrella)

**Files:** Modify `installer/package.py` (`archive`), `tests/test_package.py`.

**Interfaces:**
- Produces: `archive(repo, commit, dest)`:
  - unchanged for a repo without gitlinks;
  - for every `160000` entry of `git ls-tree -r <commit>` it runs `git -C <repo>/<path> archive <sha>` into
    `dest/<path>`, recursively;
  - raises `BuildError(f"submodule {path} lacks {sha[:10]}: fetch it into {repo/path}")` when the commit is not
    present locally;
  - never fetches.

- [ ] **Step 1: Write the failing tests** (temp repos, `git -c protocol.file.allow=always submodule add <local path>`):
  - `test_a_submodule_is_archived_at_its_pinned_commit`: the outer commit pins sub commit A, and the sub's HEAD
    later moves to B. The archive holds A's file content.
  - `test_a_missing_submodule_commit_is_refused`: the pinned sha is absent in the sub's checkout →
    `BuildError` naming the path.
  - `test_a_repo_without_submodules_archives_as_before`: the existing expectations still hold.
- [ ] **Step 2: Run** `python3 -m unittest tests.test_package -v` → the two new tests FAIL.
- [ ] **Step 3: Implement** (`ls-tree -r -z`, parse mode/sha/path, recurse with the same tar extraction).
- [ ] **Step 4: Run** `python3 -m unittest discover -s tests` → OK.
- [ ] **Step 5: Commit** `feat(package): export submodules at their pinned commits, from the local checkout`.

The LAN builder on the development server must have the a3-mixer objects for a3-prodj's pin. That is the maintainer's builder
setup; say so in the report.

### Task P4: StemDeck takes a remote pointer while pro-DJ LIVE is on, and shows LIVE

**Files:**
- Create: `Source/RemotePointer.h/.cpp`, `Source/PointerInjector.h/.cpp`
- Modify:
  - `Source/Remote.h/.cpp`: `Words` gains `pointer` and `live`, both optional, empty in an older truth.
  - `Source/OscTruthFile.cpp`: reads `stemdeck.pointer` and `prodj.live` as optional.
  - `Source/RemoteLink.h/.cpp`: routes both; a `RemotePointerGate`; `tick` in `timerCallback`.
  - `Source/MainComponent.h/.cpp`: the badge in the top bar.
  - `CMakeLists.txt` / `tests/CMakeLists.txt`.
- Test: `tests/RemotePointer.cpp` (new), `tests/OscTruth.cpp`/`tests/Remote.cpp` (optional words)

**Interfaces:**
- Consumes: "Shared definitions", device-side gate, in `namespace remote`.
- Produces:
  - `void injectPointer (juce::Component& topLevel, const remote::Inject& i, juce::int64 timeMs)`;
  - `RemoteLink::onLiveChanged : std::function<void (bool)>`, which MainComponent uses for the badge.

- [ ] **Step 1: Write the failing tests** (`tests/RemotePointer.cpp`):
  - `RemotePointer.ParseRefusesOutOfRange`:
    - `parsePointer (3, .5f, .5f)` is nullopt;
    - so are `parsePointer (0, 1.5f, .5f)` and `parsePointer (0, NAN, .5f)`;
    - `parsePointer (0, 0.f, 1.f)` has a value.
  - `RemotePointerGate.NothingWhileNotLive`: `pointer ({down,.5,.5}, 0)` is empty.
  - `RemotePointerGate.DownMoveUpPassWhileLive`: after `live (true, 0)`, the injects are exactly one `down`, one
    `move` and one `up`, with their x/y.
  - `RemotePointerGate.GoingOffMidDragReleases`: down at (.2,.3), then `live (false, 10)` returns `{ up, .2, .3 }`.
  - `RemotePointerGate.ASilentHeldPointerIsReleasedAfterOneSecond`: down at t=0, `tick (999)` is empty,
    `tick (1001)` returns `{ up }`.
  - `RemotePointerGate.TheLeaseRunsOut`: `live (true, 0)`, then `isLive (11999)` is true and `isLive (12001)` false.
    `tick (12001)` while held returns `{ up }`.
  - `RemotePointerGate.AMoveWithoutDownIsDropped` and `RemotePointerGate.ASecondDownReleasesTheFirst` (`{ up(old),
    down(new) }`).
  - `RemotePointer.ScreenToWindow`:
    - screen `{0,0,768,1024}`, window `{0,0,768,1024}`: share (.5,.5) → (384,512);
    - window `{100,0,200,200}`: share (.5,.5) → nullopt;
    - share (.2,.1) on window `{100,0,400,400}` → (53.6, 102.4).
  - `Remote.OptionalPointerWords`: a made-up truth without `stemdeck.pointer` still gives the other words, and
    `words.pointer` is empty.
  - `PointerInjector.ArrivesAsTouchNine`: a 200×200 test window on the desktop (the stemdeck tests' xvfb harness).
    The child records `e.source.getType()`/`getIndex()`; `injectPointer` gives `touch`/`9`, at the expected local
    point.
- [ ] **Step 2: Build and run** (`nice -n 19 cmake --build build -j2 && ctest --test-dir build --output-on-failure -R 'RemotePointer|Remote|PointerInjector'`) → FAIL.
- [ ] **Step 3: Implement.**
  - The gate as in "Shared definitions".
  - `RemoteLink::oscMessageReceived`:
    - `live` (`i`) → `gate.live`, `onLiveChanged`;
    - `pointer` (`iff`) → `parsePointer` → `gate.pointer` → `injectPointer` for each inject, onto
      `mixer.getTopLevelComponent()`.
  - `timerCallback` runs `gate.tick`. A change of `isLive` is reported once.
  - Badge: load `designer`/`dj-pro`/`juce-pro`.
    - It reads `PRO-DJ LIVE` in the top bar's `deviceStatus` area while live, in StemDeck's accent/warning colour
      from `Theme`.
    - It is absent while off.
    - No new pixel sizes.
- [ ] **Step 4: Full StemDeck suite.** Expected: all pass, count quoted.
- [ ] **Step 5: Commit** `feat(remote): a remote pointer from the pro-DJ while LIVE, its own touch, and LIVE in the top bar`.

### Task P5: Motion takes a remote pointer while pro-DJ LIVE is on, shows LIVE, and can switch it off

**Files:**
- Create: `src/a3-motion-ui/components/RemotePointer.{hh,cc}`, `PointerInjector.{hh,cc}`
- Modify:
  - `src/a3-motion-engine/OscAddresses.{hh,cc}`: `prodjLive`, `motionPointer` in `optionalOscAddressKeys()` beside
    `stemdeck.ahead`.
  - `src/a3-motion-ui/osc/OscMessageHandler.{hh,cc}`: Listener gains `onProdjLive (bool)` and
    `onRemotePointer (int phase, float x, float y)`.
  - `A3MotionUIComponent.{hh,cc}`: owns the gate, ticks it, injects.
  - `StatusBar`/`StatusBarLayout`: the badge slot and its tap.
  - The test CMake lists.
- Test: `unit/RemotePointer.cc`, `unit/TouchGrabs.cc`, the OscMessageHandler unit file, `unit/NoUnaskedValues.cc`
  (unchanged, must stay green)

**Interfaces:**
- Consumes: "Shared definitions", in `namespace a3`.
- Produces:
  - `OscAddresses::prodjLive`, `OscAddresses::motionPointer` (empty when the truth lacks them);
  - a tap on the badge sends `/prodj/live 0` through the path Motion already uses to send to Core (the one
    `askCoreForItsState()` uses).

- [ ] **Step 1: Write the failing tests:**
  - The gate and `screenToWindow` tests as in P4, under Motion's names (`RemotePointerGate.*`, `RemotePointer.*`).
  - `TouchGrabs.ARemotePointerKeepsItsOwnGrab`:
    - `grabKey (touch, remoteTouchIndex)` differs from `grabKey (touch, 0)` and from `grabKey (mouse, 0)`;
    - `down` with both on channels 1 and 2 gives `isHeld (1)` and `isHeld (2)`;
    - `up (remoteKey)` returns 2 and leaves 1 held.
  - `OscMessageHandler.ProdjLiveReachesTheListener`: a made-up truth with `prodj.live`; `/prodj/live 1` calls
    `onProdjLive (true)`.
  - `OscMessageHandler.APointerReachesTheListener`: `/motion/pointer 0 .25 .75` calls `onRemotePointer (0, .25f,
    .75f)`.
  - `OscAddresses.PointerAndLiveAreOptional`: a truth without them gives no missing key, and both are empty.
  - `PointerInjector.ArrivesAsTouchNine`: as in P4, with Motion's GUI test harness.
  - `StatusBarLayout.TheLiveBadgeHasASlotOnlyWhileLive`: the layout with live=false has no badge rect; with
    live=true it has a non-empty rect inside the bar that overlaps no other key.
- [ ] **Step 2: Run** `nice -n 19 ./test.sh -- -R 'RemotePointer|TouchGrabs|OscMessageHandler|OscAddresses|PointerInjector|StatusBarLayout'` → FAIL.
- [ ] **Step 3: Implement.**
  - The handler routes both words.
  - `A3MotionUIComponent` keeps a `RemotePointerGate`, runs `tick` on its existing UI timer, and injects into its
    top-level peer.
  - Load `designer`/`dj-pro`/`juce-pro` for the badge.
    - It is shown only while live and reads `PRO-DJ LIVE`.
    - A tap sends `/prodj/live 0` (never 1) and shows off at once. Core's next message confirms it.
  - Never touch `config/config.json` or skins.
- [ ] **Step 4: Full suite** `nice -n 19 ./test.sh`. Expected: green, runner time quoted, `NoUnaskedValues` still green.
- [ ] **Step 5: Commit** `feat(ui): a remote pointer from the pro-DJ while LIVE, its own touch index, and a LIVE badge that switches it off`.

---

## Phase 0 — gate (no task)

**The virtual desk is merged** (see "Phases"). Phase 2 starts from the new mains. Re-read
the workspace planning note `virtual-desk-ledger/progress.md` for late rulings, and `git log` the desk files: smoke-test fixes
may have changed `DeskComponent`, `DeskLink` or `a3_core_desks.py` since this plan was written.

## Phase 2 — after the gate

### Task C1: the pro-DJ in the one truth (a3-core + a3-doc)

**Files:**
- Modify (a3-core): `PKG/usr/share/a3/a3-osc.json`, `LOCAL/share/a3-core/osc-register.json` (regenerated by
  `tools/osc_register.py`), `tools/second_truth.py`, `tools/tests/test_osc_register.py`
- Create (a3-core): `tools/tests/test_prodj_in_the_truth.py`
- Modify (a3-doc): `src/ressources/osc.md`, `src/ressources/ports.md` (re-rendered with `tools/render_docs.py` as
  the desk's A5 did)

**Interfaces:**
- Produces, in the truth:
  - `programs` gains `"prodj"`. It has no listener of its own: the app is a desk and listens on `desk.osc`/`desk.vu`.
    The program's description says so.
  - route `{"from": "prodj", "to": "core.osc"}`.
  - `device.hello.from`, `state.recall.from` and `core.here.to` gain `"prodj"`. `device.hello`'s meaning adds:
    "a pro-DJ app says `prodj` and is followed as a desk of that kind".
  - `channel.azimuth`, `channel.elevation`: `"relayed_to": ["prodj"]`. The meaning adds "relayed to the pro-DJ
    apps followed, no one else".
  - `prodj.live`: pattern `/prodj/live`, args `i`, from `["prodj", "desk", "motion"]`, to `["core"]`,
    `announced_to` `["desk", "prodj", "motion", "stemdeck"]`. Meaning: the single global pro-DJ LIVE state,
    1 = a pro-DJ app may operate. Core holds it, starts off, and repeats it every 5 s while on; a device counts it
    off 12 s after the last 1. Motion only ever sends 0.
  - `stemdeck.pointer`: `/stemdeck/pointer`, `iff`, from `["prodj"]`, to `["core"]`, `relayed_to` `["stemdeck"]`.
    Meaning: a click on StemDeck's screen picture. Phase 0 down, 1 move, 2 up; x, y a share of the screen from
    top-left; forwarded only while pro-DJ LIVE.
  - `motion.pointer`: the same for Motion, `relayed_to` `["motion"]`.
  - `core.device-at`: `/core/device/at`, `ss`, from `["core"]`, to `["prodj"]`. Meaning: where a followed device
    runs: device (`motion`, `stemdeck`) and host. Sent to a pro-DJ app when it joins or recalls, and when that
    device moves.
  - `screencast.stream`'s `carries`: "the screen's picture as MPEG-TS, several viewers on one encode (OBS, the
    pro-DJ apps)".
- `second_truth.py`:
  - `OUR_WORDS` gains `prodj` and `motion`;
  - `REPOS` gains `"a3-prodj"`, with `CHECKOUT_PATHS` unchanged (the checkout sits at `<workspace>/a3-prodj`);
  - a missing checkout is skipped as the others are; the implementer verifies that path.

- [ ] **Step 1: Write the failing tests** (`test_prodj_in_the_truth.py`, in the style of `test_desk_in_the_truth.py`):
  - `test_is_a_program_that_listens_as_a_desk`: `"prodj"` in programs; no listener has program `prodj`.
  - `test_talks_to_core`: `("prodj", "core.osc", None)` in routes.
  - `test_says_hello_asks_and_hears_core`: `"prodj"` in `device.hello.from`, `state.recall.from`, `core.here.to`.
  - `test_only_the_prodj_hears_positions`: `relayed_to` of both position words is `["prodj"]`.
  - `test_live_is_switched_by_three_and_announced_to_four`: `prodj.live` has the from/to/announced_to above and
    args `"i"`.
  - `test_pointers_come_only_from_the_prodj`: both pointer words have `from == ["prodj"]`, args `"iff"` and the
    single `relayed_to` above.
  - `test_core_says_where_devices_run`: `core.device-at` has args `"ss"`, from core, to prodj.

  In `test_osc_register.py`: `test_the_position_only_comes_in` becomes `test_the_position_comes_in_and_goes_to_the_prodj`:
  `{("motion","in"), ("prodj","out")}`.
- [ ] **Step 2: Run** the two files (venv) → FAIL.
- [ ] **Step 3: Edit the truth, run `tools/osc_register.py`, edit `second_truth.py`.** In the paired a3-doc
  worktree, re-render the tables.
- [ ] **Step 4: Run the a3-core suite in the worktree, then the register in the main checkout.**
  - Detach `<workspace>/a3-core` on the branch and `<workspace>/a3-doc` on `docs/prodj-in-core`.
  - Run the suite: 0 skipped. Then return both to `main`.
  - Run `sphinx-build src doc` in the a3-doc worktree: 0 warnings.
- [ ] **Step 5: Commit both:**
  - a3-core `feat(truth): the pro-DJ -- positions to it, LIVE, pointers to StemDeck and Motion, where devices run`;
  - a3-doc `docs(osc): the pro-DJ's words and routes, rendered from the truth`.

### Task C2: Core knows desks of kind `prodj`, and holds pro-DJ LIVE (pure)

**Files:**
- Modify: `LOCAL/lib/a3_core_desks.py`, `tools/tests/test_core_desks.py`
- Create: `LOCAL/lib/a3_core_prodj_live.py`, `tools/tests/test_core_prodj_live.py`

**Interfaces:**
- Produces, in `a3_core_desks.py`:
  - `DESK = "desk"`, `PRODJ = "prodj"`;
  - `desk_name(host, kind=DESK) -> f"{kind}@{host}"`;
  - `kind_of(name) -> str | None` (the part before `@`, None without `@`);
  - `DeskFollowers.hello(host, now, kind=DESK)` stores the kind. A known host saying another kind takes the new
    kind, and the result is KNOWN;
  - `name_of(host, port)` returns `desk_name(host, kind)`;
  - `hosts_of_kind(kind) -> list[str]`.
- Produces, in `a3_core_prodj_live.py`:

  ```python
  REPEAT_EVERY = 5.0
  class ProdjLive:
      on: bool                                 # property; False at start
      def set(self, wanted: bool, now) -> bool      # True when it changed
      def nobody_left(self) -> bool                  # off; True when it changed
      def due(self, now) -> bool                     # while on: True once every REPEAT_EVERY s
      def admits(self, kind, key) -> bool            # see the tests
  SWITCHERS = ("desk", "prodj", "motion")
  def may_switch(origin_kind_or_name, wanted) -> bool   # motion only to off
  ```

- [ ] **Step 1: Write the failing tests:**
  - `test_core_desks.py`:
    - `test_a_prodj_is_named_by_its_kind`: hello("h", 0, kind=PRODJ), then `name_of("h", port) == "prodj@h"`.
    - `test_hosts_of_kind`: a desk at a and a prodj at b give `hosts_of_kind(PRODJ) == ["b"]`.
    - `test_kind_of_a_name`: `kind_of("prodj@h") == "prodj"`, and `kind_of("motion")` is None.
    - Every existing test stays as is (the default kind is desk).
  - `test_core_prodj_live.py`:
    - `test_starts_off`;
    - `test_set_reports_a_change_once`: set(True) is True, set(True) again is False;
    - `test_the_last_prodj_leaving_switches_it_off`;
    - `test_repeats_every_five_seconds_while_on`: on at 0, then `due(4.9)` False, `due(5.0)` True, `due(6)` False,
      `due(10.0)` True;
    - `test_never_repeats_while_off`;
    - `test_a_prodj_moves_nothing_while_off`:
      - `admits("prodj","channel.volume")` is False while off;
      - `admits("prodj", k)` is True for `k` in `("device.hello","state.recall","prodj.live")`;
      - after set(True), `admits("prodj","channel.volume")` and `admits("prodj","stemdeck.pointer")` are True;
      - `admits("desk","channel.volume")` and `admits("motion", …)` are always True;
    - `test_pointers_pass_only_from_a_prodj_while_on`: `admits("desk","motion.pointer")` is False even while on;
    - `test_motion_may_only_switch_off`: `may_switch("motion", False)` True, `may_switch("motion", True)` False,
      `may_switch("prodj", True)` True, `may_switch("mixer", True)` False.
- [ ] **Step 2: Run** both files → FAIL (stub module first).
- [ ] **Step 3: Implement** (pure, no I/O, a lock like `DeskFollowers` if read from the vu thread; LIVE is read on
  the serve thread only, so no lock).
- [ ] **Step 4: Run the a3-core suite** (venv) → OK.
- [ ] **Step 5: Commit** `feat(core): desks of kind prodj, and the pro-DJ LIVE state as a pure lease`.

### Task C3: Core wires the pro-DJ in (a3-core.py)

**Files:** Modify `LOCAL/bin/a3-core.py`; create `tools/tests/test_core_prodj_wiring.py` (source-reading, the style
of `test_core_desk_wiring.py`).

**Interfaces:**
- Consumes: C1's keys, C2's API, the desk wiring (`desk_said_hello`, `_desk_clients`, `origin_of`,
  `values_refused`, `notice_desk_silence`, `osc_handler_recall`, `point_motion_at`, `stemdeck_said_hello`,
  `on_tick`).
- Produces, in a3-core.py:
  - `_prodj_live = ProdjLive()`;
  - `prodj_clients() -> list[WatchedClient]` (the `_desk_clients` whose host is of kind prodj);
  - `tell_prodj(client)`, which sends the cached positions (only those not None, clamped), `core.device-at` for
    Motion and StemDeck (when known) and `prodj.live`;
  - `announce_live()`, which sends `prodj.live` to every `_desk_clients` value, `osc_a3motion` and
    `_stemdeck_client` (when there is one), **never** through `broadcast()`, so the hardware mixer is not told;
  - handlers `osc_handler_prodj_live` and `osc_handler_pointer`, mapped from the truth keys as the other handlers
    are.

- [ ] **Step 1: Write the failing tests** (`test_core_prodj_wiring.py`):
  - `test_a_prodj_hello_joins_as_a_desk_of_its_kind`: `osc_handler_device_hello` has `device in ("desk", "prodj")`
    with the hash check, and passes `kind=device` to `desk_said_hello`.
  - `test_a_joining_prodj_is_told_positions_places_and_live`: `desk_said_hello` calls `tell_prodj(` when the kind
    is prodj.
  - `test_positions_reach_the_prodj_after_iem`: in `osc_handler_channel` the azimuth and elevation branches call
    `prodj_clients()` after the IEM loop, with the clamped value.
  - `test_a_recall_answers_the_asker_with_live`: `osc_handler_recall` sends `prodj.live` to the asking desk or
    Motion, and calls `tell_prodj(` for a prodj.
  - `test_motion_and_stemdeck_moving_tell_the_prodj`: `point_motion_at` and `stemdeck_said_hello` (on news) send
    `core.device-at` to `prodj_clients()`.
  - `test_live_is_switched_only_by_who_may`: `osc_handler_prodj_live` asks `may_switch(` with
    `origin_of(client_address)` and `announce_live(` on a change.
  - `test_live_is_repeated_on_the_tick_while_on`: `on_tick` asks `_prodj_live.due(` and calls `announce_live(`.
  - `test_the_last_prodj_leaving_switches_live_off`: `notice_desk_silence` calls `_prodj_live.nobody_left(` when
    `_desks.hosts_of_kind(PRODJ)` is empty, then `announce_live(`.
  - `test_pointers_are_forwarded_only_through_the_gate`: `osc_handler_pointer` asks
    `_prodj_live.admits(kind_of(origin), key)`. It sends to `_stemdeck_client` for `stemdeck.pointer` and to
    `osc_a3motion` for `motion.pointer`, never via `relay(`/`broadcast(`.
  - `test_values_refused_asks_the_live_gate`: `values_refused` returns True when
    `not _prodj_live.admits(kind_of(origin_of(client_address)), key)`.
  - `test_announce_live_never_broadcasts`: `announce_live`'s source has no `broadcast(`.
  - `test_stemdeck_news_tells_it_live`: `stemdeck_said_hello` sends `prodj.live` to the new client after
    `stemdeck.recall`.
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Implement.**
  - Every send goes through `WatchedClient`, as the desk's do.
  - `traffic.seen` taps for the new handlers, using `origin_of`.
  - Journal lines:
    - `prodj: LIVE on (by <origin>)` / `off (by <origin>)`;
    - `prodj: LIVE off, no pro-DJ app left`;
    - a refused pointer is counted, not printed.
- [ ] **Step 4: Run the a3-core suite in the worktree, then the register run in the main checkout as in C1** (with
  a3-doc on `docs/prodj-in-core`). Expected: all OK, 0 skipped.
- [ ] **Step 5: Commit** `feat(core): follow the pro-DJ app -- positions, where devices run, LIVE as a lease, pointers only while LIVE`.

### Task M1: a3-desk's code as a source set other apps compile (a3-mixer)

**Files:**
- Create: `app/cmake/A3DeskSources.cmake`
- Modify:
  - `app/CMakeLists.txt` and `app/tests/CMakeLists.txt` (use it);
  - `Source/DeskWire.h/.cpp` (`hello` takes the device name);
  - `Source/DeskComponent.h/.cpp` (device name, `setHandsWithheld`, `meters()`, `controlFor`).
- Test: `tests/DeskComponentTests.cpp`, `tests/DeskWireTests.cpp`

**Interfaces:**
- Produces:
  - `A3DeskSources.cmake` sets three things, without `find_package` and without any target:
    - `A3DESK_LIBRARY_SOURCES`: absolute paths, everything in today's `A3DESK_SOURCES`;
    - `A3DESK_INCLUDE_DIR`: `app/Source`;
    - `A3DESK_JUCE_MODULES`: `juce::juce_gui_basics;juce::juce_osc;juce::juce_cryptography`.

    Consumers compile the sources into their own targets with their own JUCE modules. A static library linking JUCE
    modules would compile the modules twice (a3-motion-ui's note, 2026-10-03).
  - `DeskWire::hello (const juce::String& truthDigest, const juce::String& device = "desk") const`.
  - `DeskComponent (Send send, juce::String device = "desk")`. The device name reaches every hello.
  - `void DeskComponent::setHandsWithheld (bool)`: while true, `handsAccepted()` is false and every control dims,
    as before Core answers.
  - `const DeskMeters* DeskComponent::meters() const`.
  - `juce::Component* DeskComponent::controlFor (const std::string& key, int channel) const`. It returns the
    knob/fader/key for a truth key such as `"channel.volume"`, `"channel.cue"` or `"master.booth"` (channel 0 for
    none), and nullptr for unknown.

- [ ] **Step 1: Write the failing tests:**
  - `DeskWire.HelloNamesTheDevice`: `wire.hello ("abc", "prodj")` has args `("prodj", "abc")`, and the default is
    still `"desk"`.
  - `DeskComponent.HelloCarriesTheDeviceName`: built with `"prodj"`; the first hello recorded by the `Send`
    recorder (FakePeer path) has `"prodj"`.
  - `DeskComponent.NoHandsWhileWithheld`: a joined desk with `setHandsWithheld (true)` has `handsAccepted() ==
    false`, `touchPot (0, .5f)` sends nothing, and `setHandsWithheld (false)` gives the hands back.
  - `DeskComponent.ControlForFindsTheFaderAndTheCue`: `controlFor ("channel.volume", 2)` is the DeskFader of strip
    2, `controlFor ("channel.cue", 3)` is the CUE key of strip 3, and `controlFor ("nope", 1)` is nullptr.
  - `DeskComponent.MetersAreThere`: after `useTruth`, `meters() != nullptr`.
- [ ] **Step 2: Run** `A3_OSC_TRUTH=<core truth> ./test.sh -- -R 'HelloNamesTheDevice|HelloCarriesTheDeviceName|NoHandsWhileWithheld|ControlFor|MetersAreThere'` → FAIL.
- [ ] **Step 3: Implement.** `CMakeLists.txt` `include(cmake/A3DeskSources.cmake)` and uses
  `A3DESK_LIBRARY_SOURCES` where `A3DESK_SOURCES_ABS` was. The app's and the tests' behaviour is unchanged.
- [ ] **Step 4: Full desk suite** (`./test.sh`). Expected: everything from before plus the five, timestamp quoted.
  Then run `packaging/stage build` into a scratch dir once to confirm the package still builds.
- [ ] **Step 5: Commit** `refactor(desk): its sources as a set other apps compile; the device name in the hello; hands can be withheld`.

### Task M2: pro-DJ LIVE in a3-desk's status line (a3-mixer)

**Files:** Modify `Source/DeskOsc.*` (optional key), `Source/DeskInbox.*` (`Indicators::prodjLive`, lease),
`Source/DeskWire.*` (`prodjLive (bool)`), `Source/DeskIndicatorsUi.*` (StatusLine chip and its tap),
`Source/DeskComponent.*`; tests alongside.

**Interfaces:**
- Consumes: C1's `prodj.live`; M1's DeskComponent.
- Produces:
  - `DeskOsc::hasOptional ("prodj.live")`: `missing()` does not list it;
  - `Outgoing DeskWire::prodjLive (bool on) const` (int32 1/0 to Core);
  - `Indicators::prodjLive`, which counts as off 12 s after the last 1 (`DeskInbox::step (nowMs)`);
  - `StatusLine::onLiveTapped : std::function<void()>`.

- [ ] **Step 1: Write the failing tests:**
  - `DeskOsc.ProdjLiveIsOptional`: a truth without it has no missing key.
  - `DeskWire.ProdjLiveIsAnInt`: `prodjLive (true)` → `/prodj/live` int32 1, to core.
  - `DeskInbox.LiveIsALease`: `/prodj/live 1` at t=0 gives `prodjLive` true at t=11999 and false after
    `step (12001)`.
  - `DeskComponent.TheLiveChipTogglesWithHands`: joined, a tap on the chip sends `/prodj/live 1` (and 0 when lit);
    with hands withheld or not joined it sends nothing.
  - `DeskUi.TheLiveChipPaintsLitAndDark`: the status line snapshot is brighter in the chip's rect when live.
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Implement.** Load `designer`/`dj-pro`/`juce-pro`. The chip sits at the status line's right end and
  reads `PRO-DJ LIVE` lit, `pro-DJ` dark. Its size is a share of the line.
- [ ] **Step 4: Full desk suite** → green, timestamp quoted.
- [ ] **Step 5: Commit** `feat(desk): pro-DJ LIVE in the status line, a tap switches it`.

**Issue text for the maintainer (a3-mixer), file after merge:**
> **Title:** the hardware desk does not show pro-DJ LIVE
> **Symptom:** while a pro-DJ app may operate, StemDeck, Motion and the virtual desks say so; the A3 Mixer's OLEDs do not.
> **Finding:** Core announces `/prodj/live` only to desks, Motion and StemDeck (a3-core `announce_live`); the mixer's Python display code has no place for it.
> **Next step:** decide where on the OLEDs it belongs; then add `mixer` to `prodj.live.announced_to`.
> Labels: enhancement.

### Task J1: a3-prodj scaffold — build, tests, truth words, refusal on Core's machine

**Files:**
- Create: `.gitmodules` and `external/a3-mixer`, `CMakeLists.txt`, `test.sh`, `.reuse/dep5`, `LICENSES/*` (copied
  from a3-mixer), `Source/ProdjOsc.h/.cpp`, `Source/RunsHere.h/.cpp`, `Source/Main.cpp` (stub window),
  `tests/CMakeLists.txt`, `tests/TestRunner.cpp`, `tests/ProdjOscTests.cpp`, `tests/RunsHereTests.cpp`
- Modify: `README.md` (status line: stage 1 in progress; build/test section)

**Interfaces:**
- Consumes: M1's `A3DeskSources.cmake`, a3-mixer's `shared/` (`a3::OscTruth`, `a3::refuseOscSenders`) and
  `desk::Outgoing`.
- Produces:

  ```cpp
  namespace prodj {
  struct Match { std::string key; int number = 0; };
  class ProdjOsc {
  public:
      explicit ProdjOsc (a3::OscTruth truth);
      static juce::StringArray missing (const a3::OscTruth&);   // channel.azimuth, channel.elevation, prodj.live,
                                                                // stemdeck.pointer, motion.pointer, core.device-at,
                                                                // beat; listener screencast/stream
      std::optional<Match> match (const juce::String& address) const;   // the four we hear: positions, live, device-at, beat
      desk::Outgoing live (bool on) const;
      desk::Outgoing pointer (Device device, int phase, float x, float y) const;   // Device from BoothScreens.h (J4)
      int screencastPort() const;
      juce::String coreHost() const;   // the truth's hosts.core
  };
  bool isCoreMachine (const juce::Array<juce::IPAddress>& mine, const juce::String& coreHost);
  }
  ```

  `Device` is declared in J1 as `enum class Device { stemdeck, motion, mixerPanel };` in `BoothScreens.h` (a header
  stub here, filled in J4).
- Build:
  - targets `A3Prodj` (`juce_add_gui_app`, PRODUCT_NAME "A3 ProDJ") and `a3-prodj-tests`;
  - both compile `A3DESK_LIBRARY_SOURCES` and the app's own sources (all but `Main.cpp`);
  - include dirs `Source`, `${A3DESK_INCLUDE_DIR}`, and for the tests also `external/a3-mixer/app/tests` (TestTruth,
    FakePeer);
  - JUCE modules `${A3DESK_JUCE_MODULES}` plus `juce::juce_opengl`;
  - definitions as a3-desk's, `-Werror=switch`, ccache.
- `test.sh`: a3-desk's, with `RUNNER=…/a3-prodj-tests` and the offline truth through
  `external/a3-mixer/app/tools/a3-offline-truth`.

- [ ] **Step 1: Add the submodule from the local checkout** (no GitHub):
  - `git -c protocol.file.allow=always submodule add <workspace>/a3-mixer external/a3-mixer`, then check
    out M1/M2's branch head in it;
  - set `.gitmodules` `url = https://github.com/a3-audio/a3-mixer`, and **do not** run `submodule sync` (the local
    `.git/config` keeps the local URL);
  - `git status` must show `.gitmodules` and the gitlink only.
- [ ] **Step 2: Write the failing tests:**
  - `TestRunner.cpp` = a3-desk's (refuse senders first, GUI initialiser).
  - `ProdjOsc.TheWordsAreAllThere`: `missing (offline truth)` is empty.
  - `ProdjOsc.AMissingWordIsNamed`: a made-up truth without `motion.pointer` → missing contains it.
  - `ProdjOsc.MatchesPositionsAndLive`: `/channel/3/azimuth` gives `{"channel.azimuth",3}`, `/prodj/live` gives
    `{"prodj.live",0}`, `/channel/5/azimuth` (out of range) is nullopt, and `/channel/1/volume` is nullopt (the
    desk's word, not ours).
  - `ProdjOsc.PointerMessage`: `pointer (Device::motion, 1, .25f, .5f)` is `/motion/pointer` int32 1, float .25,
    float .5, `To::core`.
  - `ProdjOsc.LiveMessage`: `live (false)` is `/prodj/live` int32 0.
  - `RunsHere.OnCoresAddressItRefuses`: mine `{10.0.0.5, 192.168.8.10}`, core `192.168.8.10` → true;
    core `192.0.2.1` → false; an empty core host → false.
- [ ] **Step 3: Run** `A3_OSC_TRUTH=<core truth> ./test.sh` → FAIL (stubs compile; the assertions fail).
- [ ] **Step 4: Implement.**
  - `ProdjOsc` follows `DeskOsc`'s pattern: regexes from patterns, ranges from the truth.
  - `Main.cpp` refuses on Core's machine: a message box "A3 ProDJ does not run on Core's machine (the audio
    machine)" and quit, with `juce::IPAddress::getAllAddresses()`.
- [ ] **Step 5: Run** → green, runner time quoted.
- [ ] **Step 6: Commit** `feat: the a3-prodj build, its truth words, and no start on Core's machine` (`.gitmodules`, the gitlink and the new files, by name).

### Task J2: the scene's state and the inbox

**Files:** Create `Source/SceneState.h/.cpp`, `Source/ProdjInbox.h/.cpp`, `tests/SceneStateTests.cpp`,
`tests/ProdjInboxTests.cpp`.

**Interfaces:**
- Consumes: J1's `ProdjOsc::match`.
- Produces:

  ```cpp
  struct ChannelSpot { std::optional<float> azimuthDeg, elevationDeg; bool known() const; };
  class SceneState {
  public:
      void position (int channel /*1-4*/, bool azimuth, float degrees);
      const ChannelSpot& spot (int channel) const;
      void live (bool on, double nowMs);
      bool isLive (double nowMs) const;          // the 12 s lease, like the devices
      void deviceAt (const juce::String& device, const juce::String& host);
      juce::String hostOf (const juce::String& device) const;   // empty when unknown
      void beat (double nowMs);
      float beatPulse (double nowMs) const;      // 1 at the beat, linear to 0 over 150 ms
  };
  class ProdjInbox {
  public:
      ProdjInbox (const ProdjOsc& osc, SceneState& scene);
      bool receive (const juce::OSCMessage& m, double nowMs);   // true when it was ours (the caller still hands
  };                                                             // every message to DeskComponent: /beat is both)
  ```

- [ ] **Step 1: Write the failing tests:**
  - `SceneState.ABlobNeedsBothAngles`: after `position (2, true, 30)` only, `known()` is false; after
    `position (2, false, 10)` it is true.
  - `SceneState.LiveIsALease`: on at 0, live at 11999, not live at 12001.
  - `SceneState.BeatPulseDecays`: beat at 0 gives pulse 1 at 0, 0.5 at 75, 0 at 150 and at 1000.
  - `ProdjInbox.PositionsLand`: `/channel/1/elevation 45.f` gives `spot(1).elevationDeg == 45`.
  - `ProdjInbox.NonFiniteIsDropped`: `/channel/1/azimuth NaN` leaves it unset (virtual-desk ruling: the inbox
    guards network input).
  - `ProdjInbox.WrongTypesAreDropped`: `/prodj/live` with a string → no change, no crash.
  - `ProdjInbox.DeviceAt`: `/core/device/at "motion" "192.0.2.20"` gives `hostOf ("motion") == "192.0.2.20"`.
  - `ProdjInbox.DeskWordsAreNotOurs`: `/channel/1/volume .5` → `receive` false.
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run** → green.
- [ ] **Step 5: Commit** `feat: the scene's state -- positions, LIVE lease, where devices run, the beat`.

### Task J3: sphere, palette, camera, mouse-look

**Files:** Create `Source/Palette.h`, `Source/Sphere.h/.cpp`, `Source/Camera.h/.cpp`, `Source/ViewInput.h/.cpp`;
tests `SphereTests.cpp`, `CameraTests.cpp`, `ViewInputTests.cpp`.

**Interfaces:**
- Produces:

  ```cpp
  struct Vec3 { float x, y, z; };
  // IEM convention: azimuth 0 = front (0,0,-1), +90 = left (-1,0,0); elevation +90 = up (0,1,0).
  Vec3 directionOf (float azimuthDeg, float elevationDeg);
  float blobRadius (float level);              // share of the sphere radius: 0.04 at <= -60 dBFS, 0.12 at 0 dBFS, linear in dB
  juce::Point<float> radarOf (float azimuthDeg, float elevationDeg);   // top-down disc, front up: (-sin az cos el, -cos az cos el)
  struct Blob { Vec3 direction; float radius; juce::Colour colour; float glow; };
  std::vector<Blob> sceneBlobs (const SceneState&, const std::array<float, 4>& levels, double nowMs);  // known spots only; glow = 0.3 + 0.7 * beatPulse
  // Palette.h: the four channel colours, copied once from Motion's default skin quiet-indigo-2 (2026-10-17):
  inline const std::array<juce::Colour, 4> channelColours { juce::Colour (0xffd81159), juce::Colour (0xff4870ec),
                                                            juce::Colour (0xfff7d002), juce::Colour (0xff289e98) };
  struct Orientation { float yawDeg = 0.f, pitchDeg = 0.f; };   // the one place a head tracker will write (stage 4)
  struct Ray { Vec3 origin, direction; };
  class Camera {
  public:
      static constexpr float fovYDeg = 75.f, degreesPerPixel = 0.12f, pitchLimitDeg = 85.f;
      void look (float dxPixels, float dyPixels);   // right = yaw down (turn right), up = pitch up; clamps pitch
      Orientation orientation() const; void setOrientation (Orientation);
      Ray rayThrough (float u, float v, float aspect) const;   // u,v share of the view, (0.5,0.5) = straight ahead
      std::array<float, 16> view() const; std::array<float, 16> projection (float aspect) const;   // column-major for GL
  };
  struct ViewAction { enum class Kind { none, capture, release, look, pointerDown, pointerMove, pointerUp };
                      Kind kind = Kind::none; float dx = 0, dy = 0, u = .5f, v = .5f; };
  class ViewInput {
  public:
      ViewAction mouseDown (float u, float v, bool alt);
      ViewAction mouseMove (float dx, float dy, float u, float v, bool alt);
      ViewAction mouseUp (float u, float v, bool alt);
      ViewAction escape();
      bool captured() const;
  };
  ```

  Yaw follows azimuth: an orientation of yaw = a looks at `directionOf (a, 0)`.

- [ ] **Step 1: Write the failing tests:**
  - `Sphere.FrontLeftUp`:
    - `directionOf (0,0) ≈ (0,0,-1)`, `directionOf (90,0) ≈ (-1,0,0)`, `directionOf (0,90) ≈ (0,1,0)`;
    - `directionOf (180,0) ≈ (0,0,1)` (tolerance 1e-5).
  - `Sphere.BlobRadiusFollowsLevel`: `blobRadius (0.f) == 0.04f`, `blobRadius (1.f) == 0.12f`,
    `blobRadius (0.001f) == 0.04f` (-60 dB), and `blobRadius (0.0316f) ≈ 0.08f` (-30 dB).
  - `Sphere.BehindIsDownOnTheRadar`: `radarOf (180,0).y ≈ 1` and `radarOf (0,0).y ≈ -1`.
  - `Sphere.OnlyKnownSpotsMakeBlobs`: one known spot → one blob in `channelColours[ch-1]`.
  - `Camera.YawFollowsAzimuth`: `setOrientation ({90,0})`, then `rayThrough (.5,.5,1.6).direction ≈
    directionOf (90,0)`.
  - `Camera.PitchIsClamped`: `look (0, -10000)` gives pitch 85.
  - `Camera.LookRightTurnsRight`: `look (100, 0)` gives yaw `-12` (right is negative azimuth).
  - `ViewInput.FirstClickCapturesAndDoesNotPress`.
  - `ViewInput.CapturedMoveLooks`: `look` with dx, dy.
  - `ViewInput.CapturedClickPressesAtTheCrosshair`: `pointerDown` at (.5,.5); a move while down is `pointerMove`
    carrying dx, dy and (.5,.5).
  - `ViewInput.AltFreesThePointer`: captured + alt: a move is `none`, and a down at (.2,.7) is `pointerDown`
    (.2,.7).
  - `ViewInput.EscapeReleases`: `escape()` → `release`, then `captured()` is false.
  - `ViewInput.UpWithoutDownIsNothing`.
- [ ] **Step 2: Run** → FAIL. **Step 3: Implement** (load `designer` and `dj-pro` before fixing the blob sizes and
  the grid's look in J8; the numbers above are the plan's, and the designer may refine them in J8 with the maintainer).
- [ ] **Step 4: Run** → green. **Step 5: Commit** `feat: the sphere, the channel colours, the camera and mouse-look`.

### Task J4: the booth and clicking its screens

**Files:** Create `Source/Booth.h/.cpp`, fill `Source/BoothScreens.h/.cpp`; tests `BoothTests.cpp`,
`BoothScreensTests.cpp`.

**Interfaces:**
- Consumes: J3's `Vec3`, `Ray`.
- Produces:

  ```cpp
  enum class PanelId { stemdeckA, mixer, motion, stemdeckB };   // left to right on the booth
  enum class Device { stemdeck, motion, mixerPanel };
  struct Crop { float x, y, w, h; };   // share of the device's frame
  Crop cropOf (PanelId);               // stemdeckA {0,0,.5,1}, stemdeckB {.5,0,.5,1}, mixer/motion {0,0,1,1}
  Device deviceOf (PanelId);
  juce::Point<float> toFrame (PanelId, float u, float v);   // stemdeckB (0,.3) -> (.5,.3)
  struct Panel { PanelId id; Vec3 topLeft, right, down; };   // right/down: full edge vectors
  struct BoothLayout { std::array<Panel, 4> panels; Vec3 tableTopLeft, tableRight, tableDown; };
  // Panels 0.5 tall, widths = 0.5 * aspect, gaps 0.06, centred; 0.9 in front of the eye, bottom edge at -0.35,
  // tilted 20 degrees back. Aspect = width/height of what the panel shows (frame crop, or the desk's size).
  BoothLayout layOutBooth (const std::array<float, 4>& aspects);
  struct PanelHit { PanelId id; float u, v; };
  std::optional<PanelHit> hitPanel (const BoothLayout&, const Ray&);           // nearest, 0<=u,v<=1, front side
  std::optional<PanelHit> onPanelPlane (const BoothLayout&, PanelId, const Ray&);  // unclamped plane hit, then clamped to 0..1
  ```

- [ ] **Step 1: Write the failing tests:**
  - `BoothScreens.TheHalvesOfStemDeck`: `toFrame (stemdeckA, 1, .5) == (.5, .5)` and
    `toFrame (stemdeckB, 0, .5) == (.5, .5)`.
  - `BoothScreens.DevicesOfPanels`: both StemDeck panels → `Device::stemdeck`, motion → motion, mixer →
    mixerPanel.
  - `Booth.TheOrderIsADeckMixerMotionBDeck`: the panels' centres' x strictly increase in PanelId order.
  - `Booth.ARayThroughAPanelsCentreHitsItInTheMiddle`: for each panel, the ray from the origin to its centre →
    that id, u,v ≈ .5.
  - `Booth.ARayAboveTheBoothMissesIt`: the ray `(0,0.5,-1)` → nullopt.
  - `Booth.AspectSetsTheWidth`: aspect .375 vs .75 → the second panel's `right` length is doubled.
  - `Booth.ADragOffThePanelIsClampedToItsEdge`: `onPanelPlane` for a ray right of the mixer → u == 1.
  - `Booth.TheBoothIsInFront`: every panel's centre z < 0.
- [ ] **Step 2: Run** → FAIL. **Step 3: Implement.** **Step 4: Run** → green.
- [ ] **Step 5: Commit** `feat: the booth's four screens in front of you, and where a ray meets them`.

### Task J5: pointer out — clicks to StemDeck/Motion and into the mixer panel

**Files:** Create `Source/PointerOut.h/.cpp`, `Source/PanelPointer.h/.cpp`; tests `PointerOutTests.cpp`,
`PanelPointerTests.cpp`.

**Interfaces:**
- Consumes: J4's `PanelHit`, `toFrame`, `deviceOf`; M1's `DeskComponent` (offscreen); J1's `ProdjOsc::pointer`.
- Produces:

  ```cpp
  struct PointerSend { Device device; int phase; float x, y; };   // x,y: the device's frame share (mixerPanel: panel uv)
  class PointerOut {
  public:
      static constexpr double keepAliveMs = 250.0, minMoveMs = 16.0;
      std::vector<PointerSend> down (std::optional<PanelHit> hit, bool live, double nowMs);
      std::vector<PointerSend> move (std::optional<PanelHit> onHeldPlane, double nowMs);
      std::vector<PointerSend> up (double nowMs);
      std::vector<PointerSend> tick (double nowMs);
      std::vector<PointerSend> liveChanged (bool live, double nowMs);
      std::optional<PanelId> held() const;
  };
  class PanelPointer {   // a synthetic mouse into a component that is on no screen
  public:
      explicit PanelPointer (juce::Component& panel);
      void down (juce::Point<float> share); void move (juce::Point<float> share); void up (juce::Point<float> share);
  };
  ```

  PanelPointer:
  - The target is `panel.getComponentAt (point)`, deepest. It is kept from down to up.
  - Events are `juce::MouseEvent`s relative to the target, built as the desk's tests build them (`eventAt`):
    source `Desktop::getInstance().getMainMouseSource()`, `mouseDownPos` kept, `mouseWasDragged` after the first
    move.
  - It calls the target's `mouseDown`/`mouseDrag`/`mouseUp`.

- [ ] **Step 1: Write the failing tests:**
  - `PointerOut.NothingGoesOutWhileNotLive`: `down (hit, false, 0)` is empty, and a later `move`/`up` stays empty.
  - `PointerOut.ADownOnStemdeckBLandsInTheRightHalf`: hit `{stemdeckB, .5, .25}` gives
    `{stemdeck, 0, .75, .25}`.
  - `PointerOut.AMoveIsThrottledTo16ms`: moves at 0 and 10 ms give one send, at 20 ms another.
  - `PointerOut.AHeldPressKeepsAliveEvery250ms`: down at 0, `tick (249)` empty, `tick (250)` gives a move at the
    last position.
  - `PointerOut.GoingOffWhileHeldSendsUp`: down, then `liveChanged (false, 5)` gives `{up}` and `held()` is
    nullopt.
  - `PointerOut.ADragStaysOnThePanelItBeganOn`: down on motion, then a move given a clamped hit on motion's plane
    → device motion.
  - `PointerOut.ADownOffEveryPanelSendsNothing`.
  - `PanelPointer.ATapOnACueKeySendsItsEdges`: a joined `DeskComponent` (FakePeer helper from
    `external/a3-mixer/app/tests`), laid out at its minimum size. down/up at the centre share of
    `controlFor ("channel.cue", 1)` records `/channel/1/cue` `"1"` then `"0"`.
  - `PanelPointer.ADragOnAFaderSendsVolume`: down at a fader's cap, a move 20 % of its height up, then up → at least
    one `channel.volume` with a value greater than before.
  - `PanelPointer.WithheldHandsSendNothing`: `setHandsWithheld (true)`, then the same tap → nothing recorded.
- [ ] **Step 2: Run** → FAIL. **Step 3: Implement.** **Step 4: Run** → green.
- [ ] **Step 5: Commit** `feat: clicks on the booth's screens -- to StemDeck and Motion over Core, into the mixer panel here`.

### Task J6: seeing the DJ — controls that glow when someone else moves them

**Files:** Create `Source/Glow.h/.cpp`, `tests/GlowTests.cpp`.

**Interfaces:**
- Consumes: a3-desk's `desk::DeskOsc::match` (`desk::Match`), its `takeover` tolerance (1e-4, `Takeover.h`), and
  M1's `controlFor`.
- Produces:

  ```cpp
  class Glow {
  public:
      static constexpr double holdMs = 600.0;
      // A desk word arrived. `before` is what the panel showed (DeskState), `after` the message's number.
      void heard (const desk::Match& m, float before, float after, double nowMs);
      struct Lit { std::string key; int channel; float strength; };   // strength 1 at once, linear to 0 over holdMs
      std::vector<Lit> lit (double nowMs) const;
  };
  ```

  Only a value that **differs** by more than 1e-4 lights a control (virtual-desk change #8). Whole-state replays
  repeat equal values, and they must not light the whole desk.

- [ ] **Step 1: Write the failing tests:**
  - `Glow.AChangeLightsItsControl`: `heard ({"channel.volume",2}, .3, .6, 0)` makes `lit (0)` one entry with
    strength 1, and `lit (300)` strength .5.
  - `Glow.AnEqualValueLightsNothing`: before .5, after .50005 → empty.
  - `Glow.ItFades`: `lit (600)` is empty.
  - `Glow.LampsGlowTheirKey`: `{"channel.cue.led",3}` going from 0 to 1 lights key `"channel.cue"`, channel 3.
- [ ] **Step 2: Run** → FAIL. **Step 3: Implement.** **Step 4: Run** → green.
- [ ] **Step 5: Commit** `feat: what someone else moves on the desk glows on the booth`.

### Task J7: the screens' pictures — PPM frames from an ffmpeg child

**Before starting: the maintainer has said yes to `Depends: ffmpeg` (Global Constraints).**

**Files:** Create `Source/PpmStream.h/.cpp`, `Source/FrameMailbox.h/.cpp`, `Source/ScreencastReader.h/.cpp`; tests
`PpmStreamTests.cpp`, `FrameMailboxTests.cpp`, `ScreencastReaderTests.cpp`.

**Interfaces:**
- Produces:

  ```cpp
  struct Frame { int width = 0, height = 0; std::vector<std::uint8_t> rgb; };
  class PpmStream {
  public:
      static constexpr int maxSide = 8192;
      void feed (const std::uint8_t* data, std::size_t n);
      std::optional<Frame> next();   // "P6" ws w ws h ws "255" one-ws, then w*h*3 bytes
      bool broken() const;           // bad magic, maxval != 255, a side 0 or > maxSide
  };
  class FrameMailbox {   // the decoder thread posts, the GL thread takes; latest wins
  public:
      void post (Frame&& f);
      std::optional<Frame> take();
  };
  juce::StringArray decoderCommand (const juce::String& host, int port);
  class ScreencastReader : private juce::Thread {
  public:
      ScreencastReader (juce::StringArray command, FrameMailbox& out);   // starts at once; stops in the destructor
      bool receiving() const;   // a frame within the last 2 s
  };
  ```

  `decoderCommand` gives `ffmpeg -hide_banner -loglevel error -nostdin -fflags nobuffer -flags low_delay
  -probesize 32 -analyzeduration 0 -i tcp://<host>:<port> -an -f image2pipe -c:v ppm -`. The reader's loop runs
  the child through `juce::ChildProcess`, reads into `PpmStream` and posts frames. When the child ends or the
  stream breaks, it kills the child, waits 2 s and starts again.

- [ ] **Step 1: Write the failing tests:**
  - `PpmStream.OneFrameInPieces`: a 2×1 frame fed in 3-byte pieces → one frame, width 2, rgb as fed.
  - `PpmStream.TwoFramesInOneFeed`: two frames → `next()` twice, then nullopt.
  - `PpmStream.HeaderWhitespace`: `"P6\n2 1\n255\n"` and `"P6 2\n1 255\n"` both parse.
  - `PpmStream.MaxvalOtherThan255IsBroken`.
  - `PpmStream.AbsurdSizeIsBroken`: `"P6\n9000 10\n255\n"` → broken.
  - `FrameMailbox.LatestWins`: two posts, then one take gives the second; the next take is nullopt.
  - `ScreencastReader.TheCommandIsLowLatency`: `decoderCommand ("192.0.2.1", 1)` contains `-fflags`, `nobuffer`,
    `low_delay`, `tcp://192.0.2.1:1`, `image2pipe`, `ppm` and `-an`, and not `-re`.
  - `ScreencastReader.FramesFromAChild`: command `{"sh","-c","printf 'P6\\n1 1\\n255\\n\\001\\002\\003'; sleep 1"}`
    puts a 1×1 frame with rgb {1,2,3} in the mailbox within 2 s. No network.
- [ ] **Step 2: Run** → FAIL. **Step 3: Implement.** **Step 4: Run** → green.
- [ ] **Step 5: Commit** `feat: the booth screens' pictures, decoded by an ffmpeg child into PPM frames`.

### Task J8: the window — scene, HUD, input, links (load `designer`, `dj-pro`, `juce-pro` first)

**Files:** Create `Source/SceneRenderer.h/.cpp`, `Source/HudComponent.h/.cpp`, `Source/ProdjComponent.h/.cpp`;
complete `Source/Main.cpp`; tests `HudComponentTests.cpp`, `ProdjComponentTests.cpp`.

**Interfaces:**
- Consumes: everything above; a3-desk's `DeskComponent`, `DeskLink`, `a3::TruthKeeperLink`, `nowMs()`.
- Produces:

  ```cpp
  class HudComponent : public juce::Component {   // 2D, painted over the GL scene
  public:
      void show (const std::vector<Blob>& blobs, bool live, bool captured, juce::String status, Orientation o);
  };
  class ProdjComponent : public juce::Component, private juce::Timer {
  public:
      using Send = std::function<bool (const desk::Outgoing&)>;
      explicit ProdjComponent (Send send);
      void useTruth (a3::OscTruth truth);
      void receive (const juce::OSCMessage& m, double nowMs);   // ProdjInbox + Glow first, then DeskComponent
      void announced (const a3::Announcement& a, double nowMs);
      desk::DeskComponent& panel();
      VuInbox* vuInbox();                                       // the panel's, for DeskLink
      void toggleLive();                                        // key L and the HUD chip: sends prodj.live
  };
  ```

  Behaviour:
  - **The panel.** `DeskComponent` is constructed with device `"prodj"`, kept visible but parentless, and sized
    to 1.5× `minimumDeskSize`. Its hands are withheld unless `SceneState::isLive`. It is snapshotted at 20 Hz
    (`createComponentSnapshot`) with the `Glow` overlay drawn on the snapshot (the bounds of `controlFor`).
  - **Screencasts.** One `ScreencastReader` for StemDeck at `hostOf("stemdeck")`, else `ProdjOsc::coreHost()`.
    One for Motion at `hostOf("motion")`, started only once known. A reader is rebuilt when its host changes.
  - **Input.**
    - Mouse-type sources only (every touch arrives twice): `ViewInput` → `Camera::look` / ray → `hitPanel` /
      `onPanelPlane` → `PointerOut`.
    - A `mixerPanel` send goes to `PanelPointer`; the others go to `ProdjOsc::pointer` → `Send`.
    - Captured mode uses `e.source.enableUnboundedMouseMovement (true)` and hides the cursor. Escape releases.
  - **Timer (60 Hz)** runs `PointerOut::tick`, applies `liveChanged` when the lease flips, and repaints.
  - **SceneRenderer** (an `OpenGLRenderer`, `juce::OpenGLContext` attached, `setComponentPaintingEnabled (true)`
    so the HUD paints on top):
    - a lat/long grid every 30°, the horizon brighter;
    - blobs as camera-facing discs (`sceneBlobs`);
    - the booth table and four textured quads: StemDeck A and B crop one texture, the mixer is the snapshot,
      Motion is its texture;
    - a panel with no picture shows "no picture from <device>" (drawn into its texture by the HUD's helper);
    - frames from the `FrameMailbox`es are uploaded on the GL thread with `glTexSubImage2D` when the size is
      unchanged.
  - **HUD:**
    - the radar disc bottom-right (blobs at `radarOf`, front up, the view's yaw as a wedge);
    - a crosshair while captured;
    - the chip `PRO-DJ LIVE` / `watching` top-right;
    - a status line with the desk's status text (it says "another desk runs on this machine" when `DeskLink`
      cannot bind) and which screencasts are receiving.
  - **Main.cpp:** the desk's Main pattern (keeper link, `load()` → `useTruth`), plus `DeskLink` with
    `onMessage = component.receive`. It runs the RunsHere check first. The window is resizable, F11 is full screen,
    and its title is "A3 ProDJ".

- [ ] **Step 1: Write the failing tests:**
  - `HudComponent.TheRadarShowsABlobBehind`: blobs = one at az 180 in channel 1's colour. A 400×300 snapshot has
    a pixel within 3 px of the radar centre + (0, +0.8 × radius) whose colour is channel 1's (tolerance 40 per
    component).
  - `HudComponent.TheChipSaysLive`: `live = true` vs false → the chip rect's mean brightness is higher when live.
  - `HudComponent.PaintsEveryState`: captured/free × live/off × no blobs/four blobs; each snapshot paints without
    throwing (A³ rule "A page test must paint").
  - `ProdjComponent.LiveTogglesThroughCore`: `toggleLive()` sends `/prodj/live 1`, and does not change
    `isLive` until Core says so.
  - `ProdjComponent.APositionReachesTheScene` and `ProdjComponent.TheDeskStillHearsItsWords`: a `/channel/1/volume`
    reaches `panel().state()`.
  - `ProdjComponent.ThePanelIsWithheldWhileNotLive`: after a join (FakePeer answer), `panel().handsAccepted()` is
    false. After `/prodj/live 1` it is true. After 12.1 s without a repeat it is false again.
  - `ProdjComponent.ATouchSourceDoesNothing`: a synthetic touch-type mouseDown leaves `ViewInput` free.
- [ ] **Step 2: Run** → FAIL. **Step 3: Implement.** **Step 4: Run** → green, runner time quoted.
- [ ] **Step 5: Look at it.**
  - Run the app on the workstation against the offline truth (it hears nothing and sends nothing until joined).
  - Take three screenshots (free, captured, an imagined LIVE via a test hook): `xvfb-run` or the local display,
    the way the desk's B12 did.
  - Review with the `designer` skill and fix what it flags, in this task.
- [ ] **Step 6: Commit** `feat: the pro-DJ's view -- sphere, blobs, radar, booth with live screens, mouse-look and LIVE`.

### Task J9: packaging (a3-prodj)

**Files:** Create `packaging/stage`, `packaging/DEBIAN/{control,postinst,prerm,postrm}`,
`packaging/a3-prodj.desktop`; extend `.reuse/dep5` with `packaging/*`.

**Interfaces:**
- `stage build <src> <build> <juce> <jobs> [--test]` configures `<src>` (top level, submodule inside) with
  `-DA3PRODJ_TESTS`. With `--test` it runs `xvfb-run ctest` against an offline truth, the way a3-desk's does.
- `stage files` installs `usr/bin/a3-prodj`, `usr/share/applications/a3-prodj.desktop` and
  `usr/share/doc/a3-prodj/copyright`.
- `control`: `Package: a3-prodj`, `Depends: ${shlibs:Depends}, ffmpeg, libx11-6, libxext6, libxrandr2,
  libxinerama1, libxcursor1, libgl1`.
  - Description: the pro-DJ's view of the A3 rig. You stand inside the sphere at the floor centre, see every
    channel and the booth, and operate StemDeck, the mixer and Motion while pro-DJ LIVE is on.
  - It does not run on Core's machine. No service.
- postinst/prerm/postrm: no-op with SPDX and `exit 0` (`package.py` requires all four; virtual-desk ruling P3).

- [ ] **Step 1: Write the failing check:** `tests/packaging/test_stage.py` (Python, stdlib), with two tests:
  - `test_control_names_its_runtime_tools`: `ffmpeg` and `libgl1` in Depends;
  - `test_files_lays_out_the_binary_desktop_and_copyright`: runs `stage files` with a fake build dir holding an
    empty binary → three files at their paths, binary mode 755.

  The C++ `test.sh` ignores it; `stage build --test` runs it.
- [ ] **Step 2: Run** `python3 -m unittest discover -s tests/packaging` → FAIL.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run it, then `packaging/stage build` into the scratchpad with `--test`, then `stage files`.**
  - `package.py` itself needs the maintainer's `v03.0` tag; it is verified after the merge, in S1.
  - Quote the ctest count.
- [ ] **Step 5: Commit** `build: the a3-prodj package recipe`.

## Phase 3 — documentation and the device check

### Task D1: the pro-DJ in the user manual (a3-doc)

**Files:** Create `src/user/prodj.md` (CC-BY-SA-4.0 header as the other pages); add it to the user toctree.

Hand the writing to a separate agent (A³ rule "Docs by separate agents"), with this content:
- what stage 1 is;
- where it runs (not on Core's machine);
- how to open it;
- mouse-look and the keys (click to capture, Esc, Alt, L);
- what LIVE means and where it shows/switches (app, a3-desk's status line, Motion's badge = off, StemDeck shows);
- the lease (12 s);
- one desk per machine;
- turning on Motion's screencast on the Motion machine (`systemctl --user enable --now a3-motion-screencast`).

No rendered-table hand edits ("docs agents must not hand-edit rendered rows").

- [ ] **Step 1:** Write the page. **Step 2:** `~/.venv-docs/bin/sphinx-build src doc` → 0 warnings. **Step 3: Commit** `docs(user): the pro-DJ view, stage 1`.

### Task S1: the device checklist `smoke-test/prodj-stage-1.md`

**Files:** Create `<workspace>/smoke-test/prodj-stage-1.md` (workspace, not committed).

Write the checklist in the shape of `smoke-test/virtual-desk.md`:
- what changed, per repo with SHAs;
- how to build and install (the packages, which machine);
- a **Verified** section filled with what was checked automatically: suite counts with timestamps, the register
  run, the P1 workstation measurement;
- the items below as **unchecked boxes**;
- an empty `## Result` for the maintainer.

Never tick a box. Never run anything on the rig.

Items (each says what to do and what to see):
1. the Core machine, after installing a3-core: with OBS connected, start the app on the development server. OBS keeps its picture, the app
   shows StemDeck. `top` shows one ffmpeg on core 0, and its CPU is the same before and after the app joins.
2. the Motion machine: `systemctl --user enable --now a3-motion-screencast`. The app's Motion screen shows Motion within 3 s of
   start.
3. The app on the Core machine refuses to start, with the message.
4. Core's window (`/api/devices`) lists `prodj@<host>` with "is Core's". The journal says `desk: <host> joined`.
5. Move a channel on Motion: its blob moves on the sphere in the same direction as on Motion's own sphere (az +90
   is **left**). Behind you it shows on the radar.
6. Play a stem: the blob grows with the level. The beat pulses.
7. LIVE off (start state): clicks on StemDeck's and Motion's screens and on the mixer panel do nothing. Core's
   traffic window counts refused pointers.
8. `L` in the app: `PRO-DJ LIVE` lights in the app, on StemDeck's top bar, on Motion's status bar and on a3-desk's
   status line (a3-desk on another machine).
9. LIVE on: a click on a StemDeck A deck button acts on deck A, on StemDeck B on deck B (crop halves). A drag on
   Motion moves a blob. A fader drag on the mixer panel moves the hardware's REAPER fader, and a3-desk follows.
10. While a remote drag on Motion is held, the DJ drags another blob with a finger. Both move, and neither jumps.
11. Tap Motion's badge: LIVE goes off everywhere within a second. A held remote drag is released.
12. LIVE on, then pull the app machine's cable for 15 s: StemDeck's and Motion's badges go off after ~12 s.
    Reconnect: the app shows watching.
13. LIVE on, then close the app: after a minute Core's journal says `LIVE off, no pro-DJ app left`.
14. The real DJ turns a knob on the hardware desk: the matching knob glows on the 3D booth and moves. A Motion
    recall does not make everything glow.
15. a3-desk and the app on the same machine: the app says "another desk runs on this machine" and only watches.
16. Mouse-look: click captures, Esc frees, Alt clicks where the pointer is. Pitch stops at the poles.
17. `package.py a3-prodj` after the maintainer's `v03.0` tag builds `a3-prodj_03.0+N`. `dpkg -I` shows
    `Depends: … ffmpeg`.
18. Frame rate of the app's screens on the development server (≥ 30 fps target); the Core machine's audio cores untouched (`xruns` in the
    journal unchanged).

---

## Self-review (done while writing)

**Spec coverage:**
- Mouse-look → J3/J8.
- Blobs and radar → J3/J8.
- Booth with four screens → J4/J8.
- Real screens via screencast → P1/P2/J7.
- Control via OSC and clicks on screens → P4/P5/C3/J5.
- The mixer panel from a3-desk's components → M1/J5/J8.
- Seeing the DJ → J6/J8.
- No audio, nothing unasked → Global Constraints and C3.
- Orientation in one place → J3.
- Truth words and a3-doc → C1.
- Calls 1–8 → M1+J1, C1/C3, J3, P1, J1, P2, P4/P5, J4.
- *pro-DJ LIVE* → C2/C3/M2/P4/P5/J8.
- The design's "Open" items: change #10 (where the switch sits) and "Not in this plan" (two StemDeck windows).

**Type consistency:**
- `Device`/`PanelId`/`PanelHit` are defined in J4 (`Device` stubbed in J1).
- `desk::Outgoing` comes from a3-mixer.
- `RemotePointerGate`/`Inject`/`remoteTouchIndex` are identical in P4/P5.
- `prodj.live`'s lease is 12 s in P4/P5/M2/J2 alike, the repeat 5 s in C2.

**Review Focus:** each of the five has a named test in its owning task.

**Proportion:** signatures, test names and values; no bodies beyond the shared gate's declaration.
