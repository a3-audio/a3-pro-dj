# Preparation: library, stems, levels, meters

What is done before a set, at home or at soundcheck, so that nothing has to be done during it. The
on-stage checklist is in [live on stage](live-on-stage.md).

## The library travels on one stick

In the Pioneer world one USB stick in any player is enough: every other player on the Pro DJ Link
network sees and loads from it. DJs expect exactly that, and it is A³'s target too (decided
2026-10-29, not built yet):

- one stick at **any** deck host serves the library to every deck on the network;
- A³ Core can also serve a library from its own disk;
- a deck loads a track whole into memory, so the network is only read at load time, never during
  playback.

Until then each deck host needs its own copy of the library.

## Stems are made beforehand

Stem separation (drums, bass, other, vocals) without a GPU takes hours per track: a measurement in
2026-10 found demucs.cpp on a desktop CPU 6× slower than real time for `htdemucs` and about 25×
slower for the finer `htdemucs_ft`. On the machine that plays the set it would compete with the audio.
So **stems are made on the DJ's own computer before the gig** and copied into the library, the way a
rekordbox user analyses tracks at home. (A³ decision, 2026-10-26; the tool lives in its own
repository.) Any text promising "it splits tracks itself" on the rig over-promises.

## Prepare the track, not the moment

- **Beat grids** are checked at home. A deck aligns to the beat; where the "one" is, a DJ sets by hand
  on the jog, as on a CDJ.
- **Tempo range**: a deck's pitch range should offer the CDJ's steps (see [CDJ-3000](../gear/cdj-3000.md)).
- **Key lock** (Master Tempo on a CDJ, KEY on StemDeck): the high-quality time-stretch costs more CPU;
  a change of engine is applied only where nobody hears it — when the deck is stopped or at the next
  load.

## Levels and meters

- **Gain staging is set at soundcheck**, with the room as loud as it may ever get at the top of the
  trim, and set up quietly first ("start quiet").
- **One meter behaviour everywhere** (A³ decision, 2026-10-07). Every display in the booth — deck
  screens, desk displays, channel LEDs, the main meter — shows the same peak with the same ballistics,
  so two meters never disagree about one signal:
  - attack immediate;
  - release 20 dB/s;
  - peak hold 1.5 s, then falling at 20 dB/s;
  - the shared LED scale −36, −24, −18, −12, −9, −6, −3, 0 dBFS.

  That is a little livelier than IEC 60268-18 (20 dB in 1.7 s, about 12 dB/s), which is right for a
  booth.
- A clip indicator must never disappear before its hold mark: give it the same 1.5 s as the peak hold.

## The clock

Who is tempo master is agreed before the doors open, not discovered at the drop. See
[Pro DJ Link](../gear/pro-dj-link.md) and the clock card in [live on stage](live-on-stage.md).

## Rehearse in headphones

A drag on the sphere and a recorded take are heard by the room as they happen, so a movement is
rehearsed in the headphones first. A³ decodes the cue as B-format to binaural headphones (one HRTF for
everything), so a movement can be heard in the phones. Which channel setting keeps a rehearsal out of
the room while it still moves in the phones is an open question in the documentation (2026-09-29:
"3d down, cue on" was proposed and is to be confirmed).
