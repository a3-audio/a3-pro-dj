# Spatial effects for DJs

Two kinds of effect: a DJ's **stereo effects translated into movement**, and **whole-field effects**
that only a 3D system can do. Neither has a published reference mapping; everything here is derived
(from [motion perception](motion-perception.md) and the [MJ playbook](mj-playbook.md)) or an idea
waiting for a design. Tags: **R** = rests on research, **G** = a guess to test, **sim** = checked in the
movement lab's simulation.

## Stereo DJ effects, translated

A DJM's Beat FX are set in note values (delay and echo 1/16–16 beats; filter, flanger, phaser cycles
1/16–64 beats). A DJ thinks in those values; a 3D effect should too.

| Stereo effect | In 3D | Rate | Tag |
|---|---|---|---|
| Auto-pan L↔R | a **step** between two opposite points (a fast glide at most) | ½–2 beats per side | G; step > glide (short glides fall under the ear's integration time) — R, sim |
| Auto-pan circle | rotation | 1 lap per 1–4 bars; 1 lap per beat only as a swirl | R |
| Filter sweep | sweep the moving band's FREQ while it orbits: the band "climbs" (higher is heard higher) | 4–16 bars | R (Lee 2015) + G |
| Echo throw | throw the delay return to the side opposite the source and let it drift back | over 1–2 bars, delay ¼–1 bar | G; needs the delay on its own movable path |
| Riser | climb in elevation, double the rotation every 4 bars, high FREQ | 8–16 bars | R (elevation needs HF) + G |
| Drop | snap the band to the front, or freeze it, on the one | 1 beat | G; the "stop and restart on the one" result supports it (sim) |

In the simulation every effect cost a little attention when used as a routine: **effects are
accents, not the main course.**

## Whole-field effects on a deck's B-format (ideas, 2026-10-30)

StemDeck's decks deliver their stems as a 3rd-order Ambisonics field (B-format). On that field, the
whole room can move rather than one source — the effect no stereo setup has. The maintainer: "note the
fx. we will need them." Not designed or scheduled; each would be an IEM plug-in in the engine, per deck
input.

| Effect | Tool (IEM suite) | What the room hears | CPU |
|---|---|---|---|
| **Spin** | SceneRotator | the whole deck turns around the room, beat-synced (e.g. one turn per bar), or tilts overhead; hold to speed up, release to land home on the downbeat | almost none |
| **Tunnel / zoom** | AmbisonicWarp (ToolBox) | the field pulled together towards one direction during the build, snapping open to the full room on the drop: a spatial riser | low |
| **Explode** | GranularEncoder | one stem (hats, a vocal chop) scattered as grains over all speakers, then pulled back | medium |
| **Throw / freeze** | FdnReverb (ambisonic) | a 3D echo-out: send a stem, freeze, the tail stands everywhere while the beat runs on; pairs with the delay | medium |
| **Directional ducking** | DirectionalCompressor | sidechain pumping from one direction only: the kick pushes the pads backwards | low–medium |
| **Doppler room** | RoomEncoder | a stem as a source in a virtual room with reflections and Doppler: a fast orbit gets a real swoosh | high, per source |

Start with **spin and tunnel**: cheap, whole-field, and the hardest hit (build → tunnel, drop → spin).

## How they are operated (DJ view, not decided)

- **One pad per effect, momentary**: hold = on, release = back. There is no undo in front of a room.
- **Beat-quantised start and end** (next downbeat or bar), with a "now" override — the same pairing as
  quantised transport with an instant variant.
- **One knob per effect** for intensity (spin speed, tunnel width, grain spread).
- **Per deck**, wherever the deck runs.

## Movement and stems: how much of a stem goes into 3D

A stem at rest is steady. An action raises the stem's 3D to full over its first beat and lowers it
over its last (the effective 3D is the deck's 3d × the action's envelope). A separate per-stem 3D knob
was tried and dropped (2026-10-29): with stems, the action *is* the gesture.
