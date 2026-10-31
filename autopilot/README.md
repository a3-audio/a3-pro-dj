# The pro-DJ application: autopilot, co-pilot, school

The pro-DJ is A³'s DJ as software: an application of its own that stands at the floor centre, inside
the sphere, and sees every sound moving around it. In the long run it **plays** (autopilot for a whole
set), **plays along** (co-pilot beside a human DJ), and **teaches** (a training game, and the
tutorial for the A³ suite). This folder holds its design documents; the code lives on the branch
`feat/stage-1` of this repository until it is merged.

Its knowledge — how a DJ plays, what the room can hear, what a set looks like — is the
[knowledge base](../knowledge/) next to this folder. The autopilot is meant to act on it.

## Decided (2026-10-16 and 2026-10-17)

- **All three roles** — autopilot, co-pilot, training (like/dislike, a score) — in **one separate
  application**, seen from the pro-DJ's point of view: inside the sphere at floor centre, the movement
  all around.
- **Head tracking over OSC** (yaw/pitch/roll, the IEM SceneRotator convention), usable later for
  binaural listening from the same position.
- **Never a second brain on a deck.** The pro-DJ conducts StemDeck's Auto DJ and A³ Motion's pilots
  *through A³ Core*; it never drives a deck behind the deck's back, and the app only sends what a human
  does in it.
- **Nothing unasked at start-up** (Core asks, devices answer).
- **One global switch, "pro-DJ LIVE".** While it is on, any pro-DJ app on the network may operate the
  booth; while it is off, devices ignore it and it only watches. Every device shows the state where
  the eye already goes, so nobody is surprised by a remote hand.
- **Taking over is instant, handing back is deliberate.** For A³ Motion's automatic motion jockey the
  levels are OFF / HINT / FLY (mockups in [research/mj-lab/mockups](../research/mj-lab/mockups/)).
- **Known trap:** the physical desk has no motor faders, so anything the pro-DJ moves leaves the knobs
  disagreeing; the rule is "a physical turn wins", with a visible state.

## Stages

| # | Stage | Status (2026-10-31) |
|---|---|---|
| 1 | **The booth inside the sphere** — at the rig, watch and operate the booth from the floor centre: every channel as a blob on the sphere, a radar for what is behind you, the booth (StemDeck A, the mixer, Motion, StemDeck B) as a 3D desk with the devices' live screens; operate it while pro-DJ LIVE is on | built and reviewed on `feat/stage-1`, not merged; [design](stage-1-design.md), [plan](stage-1-plan.md) |
| 2 | **Tutorial at the system** — the first lesson guided inside the app: load a track, mix two decks, move a sound | not started |
| 3 | **Laptop variant** — the app brings a small local A³ (decks, mixer, Motion, binaural output) for learning at home | not started |
| 4 | **VR and the brain** — a VR headset with head tracking; autopilot, co-pilot and training | not started |

The order of the earlier decomposition (2026-10-16): the virtual desk first (an A³ Mixer replica,
now in a3-mixer), then the pro-DJ view (stage 1), then its brain, then hearing it binaurally.

## Later ideas

- StemDeck's stem groups (drums, bass, other, vocals) as their own sounds on the sphere, each with its
  own position, in the pro-DJ view and in A³ Motion (2026-10-17: "a good idea, we do that later").

## The documents

- [stage-1-design.md](stage-1-design.md) — the design of stage 1, with the maintainer's decisions and
  the calls left to the builder.
- [stage-1-plan.md](stage-1-plan.md) — the implementation plan it was built from, task by task. It is
  a working document of 2026-10-17: paths are relative to the A³ development workspace, machine names
  are replaced by their roles, and later changes (in the branch's commits and the A³ docs) supersede
  it.
