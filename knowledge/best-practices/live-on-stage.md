# Live on stage: before the gig, during the set, when it goes wrong

What a performer needs to know about a live set on A³, as rules and checklists. Collected from the
DJ reviews of the A³ documentation (2026-09-29 and 2026-10-30) and from the maintainer's decisions.
Where the rule is A³-specific, it says so; the rest holds for any booth.

## The one rule behind all of them

**One dropout, one crackle, one wrong jump at a gig, and the room's trust is gone at once.** Every
safety rule below exists because a booth has no undo (see [the booth](the-booth.md)).

## When does it land? (quantised versus instant)

A performer has to know, without reading, which presses wait for the beat and which do not. On A³
Motion:

| You press | It happens |
| :--- | :--- |
| Play\|Pause on a clip | on the next downbeat (the "one") |
| SHIFT + Play\|Pause | now |
| ■ (stop) | now |
| an action pad | now, for as long as you hold it |
| load a set | on the next downbeat, all four channels together |
| drag a blob on the sphere | now, continuously — the room hears every centimetre |
| record a take | the room hears what you draw while you draw it |

Two consequences:
- **Pause lands on the downbeat** (A³ decision, 2026-09-25). Stopping "at the end of the figure" felt
  like a dead key once figures got long (up to 16 bars); the next downbeat is what a DJ expects, SHIFT
  makes it immediate, and stop is the instant way out.
- **A drag is live.** Rehearse a movement in headphones first (3d down for the room, cue on).

## Before the gig

A short card, in the order a soundcheck runs:

1. **Agree on the clock.** Who is tempo master tonight? CDJs on Pro DJ Link → A³ follows the link
   (PIO). StemDeck only → a StemDeck deck is master, A³ Motion follows. Vinyl or a lone laptop → the
   beat analyser (EXT) or tap tempo (INT). The clock is not stored in sets, because every venue's booth
   is wired differently: check it at soundcheck, not at the drop.
2. **Check that the BPM shown matches the decks.** A beat analyser that counts a 150 track at 75 is
   right for movement (a half-time grid) but disagrees with the CDJ display the DJ reads.
3. **Room set up and saved before the doors open.** Speaker calibration, front direction, levels.
   Saving a room setup restarts the audio with a fade — not something to do with a crowd in.
4. **Everything visible on the desk.** Decks show up on the desk's input ring, meters move.
5. **Recording is on**, if the set is being recorded.
6. **Developer and edit modes off.** Anything that can overwrite factory content mid-set stays off.
7. **Know what loading a set does**: it stops all four movements and starts the new ones together on
   the next downbeat.

## During the set: do not

- **Do not restart a deck application mid-set.**
- **Do not save the room/engine setup mid-set** (it restarts the audio).
- **Do not load a Motion set in the middle of a track** unless the jump is the point.
- **Do not edit an action mid-set to suit one track.** On A³ Motion an action edited on the ACTION page
  is changed everywhere it is used, in every set. Save a copy first.
- **Do not double-tap the master.** A³ deliberately has no reset gesture on the master fader: it is the
  one gesture that would make the whole room loud at once.

## Reassurances worth knowing before the gig

- **A restart does not move the room.** If A³ Motion restarts, the sounds stay where they were; the
  devices come back knowing what the room is doing (Total Recall).
- **A³ starts silent.** The outputs stay silent until every device has told the system its settings, so
  a reboot never blasts the room at a default level.
- **Delete removes the file, not the music.** Whatever is loaded keeps playing; you cannot delete your
  way into silence.

## Get me out of here (panic)

- **Freeze all movement now:** stop all clips (on A³ Motion: Stop all, or ■ per channel).
- **Back to plain stereo:** 3d down on a channel puts it back to plain stereo, like any mixer.
- After a stop the sound stays where it stopped.

A single "all 3D off" control for the whole system does not exist yet (open as of 2026-10-30).

## The hardware fader that does not move

The A³ Mixer has **no motor faders**. When a value changes elsewhere (on screen, in a recalled set, by
the pro-DJ), the physical fader stays where it is. DJs know the answer from controllers: **soft
takeover / pickup** — the physical control takes over when touched. Say it plainly in any interface
that can move a desk value: "The physical fader doesn't move. Touch it and it takes over from wherever
it sits." A³'s rule: **a physical turn wins**, and the desk shows a ring where the hardware knob stands
elsewhere. For the per-stem AUX pot on the A³ Motion panel the decision went the other way: absolute,
the deck wins, no pickup.

## Clock: follow smoothly, never trust the source

A beat clock from outside (an analyser, a network) will report the wrong octave and the occasional
stray beat. A measurement on 140 BPM music (2026-09-27) found 17 % of beats reported at the right tempo
and the rest at half, and 14 % more than 20 ms off. The performer must never hear that:

- treat half and double tempo as **the same tempo**;
- need several beats (A³: 4) before accepting a real tempo change, more (16) for an octave change, and
  glide to it;
- never jump the phase; catch up gently, and ignore a single stray beat;
- if the clock goes silent, **hold the last tempo** rather than stopping.

## One clock for the audio

Audio that travels between machines (decks on other hosts) must run on **one clock**. Two crystals and
an adaptive resampler in between give occasional crackle, and crackle at a gig is exactly the trust
loss above. A³'s rule since 2026-10-30: the Core's audio interface is the only clock, every device
follows it, no software clock, and a host whose network clock is not stable plays no deck at a gig.
A multi-hour soak with zero dropouts is the release gate. (The engineering lives in a3-core.)

## Troubleshooting, symptom first

| Symptom | Likely cause | Do |
| :--- | :--- | :--- |
| Play blinks and never starts | no beat clock arriving | check the clock source; switch to INT and tap |
| The blob moves, the sound doesn't | 3d is down, or Core is not reached | raise 3d; check that meters move |
| Screen knob and desk fader disagree | no motor faders | touch the fader: it takes over |
| An action does nothing | the pad is empty | assign an action |
| The action sounds different from yesterday | someone edited it | restore it from the library |
| The desk can't select a stem of the other deck | StemDeck's AUTO DJ owns the stem buses while it is on (intended) | switch AUTO DJ off |
| Screen frozen | the application hung | restart it; the room keeps its positions |
