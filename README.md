# a3-pro-dj — the A³ pro-DJ

The DJ's side of [A³ Audio](https://github.com/a3-audio/a3-system), a system for playing DJ and live
sets in 3D sound. This repository holds two things:

1. **Everything A³ knows about DJing** — best practices for DJs, knowledge about other DJ gear, being
   live on stage, and playing on 3D systems, with the research behind it.
2. **The pro-DJ application** (later) — the set seen from the floor centre, inside the sphere, with
   every sound moving around; in time an autopilot, a co-pilot beside a human DJ, and a school. It
   reads what A³ Core and A³ Motion send over OSC and produces no audio. Its code is on the branch
   `feat/stage-1` until merged.

**User documentation of the whole system: <https://a3-audio.github.io/a3-doc/>**

## How it is organised

```
knowledge/              what a DJ needs to know, as rules — the part to read
  best-practices/       the booth, set structure, preparation, live on stage, writing for DJs
  gear/                 CDJ-3000, Pro DJ Link, DJ software, mixers, Grapes 3D, and A³ itself
  spatial/              playing in 3D, motion perception research, the MJ playbook, spatial FX
  sources.md            every outside source, with a link (manufacturer manuals as links only)
research/               the work behind the rules: the MJ Lab simulation (code, log, results,
                        figures, report) and the defaults audit
autopilot/              the pro-DJ application: stages, the stage-1 design and plan
```

Start with [the booth](knowledge/best-practices/the-booth.md) — the five facts every other page
follows from — then [playing in 3D](knowledge/spatial/playing-in-3d.md).

| Page | What it answers |
|---|---|
| [the booth](knowledge/best-practices/the-booth.md) | what a performer's hands and eyes can do; how to argue a design question |
| [live on stage](knowledge/best-practices/live-on-stage.md) | before the gig, during the set, panic, troubleshooting, the clock |
| [preparation](knowledge/best-practices/preparation.md) | library, stems, levels and meters |
| [set structure](knowledge/best-practices/set-structure.md) | the phases of a night, mood, build/drop/breakdown, one panel layout |
| [writing for DJs](knowledge/best-practices/documentation-for-djs.md) | docs, names, the buyer's question |
| [CDJ-3000](knowledge/gear/cdj-3000.md) | the reference instrument: tempo, cue, loops, hot cues, quantize, sync |
| [Pro DJ Link](knowledge/gear/pro-dj-link.md) | the players' network, how A³ joins it, wording rules |
| [DJ software](knowledge/gear/dj-software.md) | rekordbox, Serato, Traktor and A³ |
| [mixers](knowledge/gear/mixers.md) | what a DJM user expects; how the A³ Mixer differs |
| [Grapes 3D](knowledge/gear/grapes-3d.md) | the reference for trajectory vocabulary |
| [the A³ instrument](knowledge/gear/a3-system.md) | A³'s parts and how sound moves, from the booth |
| [playing in 3D](knowledge/spatial/playing-in-3d.md) | the rules in short |
| [motion perception](knowledge/spatial/motion-perception.md) | the research, A³'s starting values, a listening test |
| [MJ playbook](knowledge/spatial/mj-playbook.md) | rules for moving sound, checked against the lab |
| [spatial FX](knowledge/spatial/spatial-fx.md) | stereo DJ effects in 3D, whole-field effects |

Every page tags what is knowledge and what is a guess. Where a rule is A³'s own decision, it carries
the date it was made.

## How the `dj-pro` skill uses it

A³ is developed with Claude Code. Its `dj-pro` skill — the DJ's advocate in the room while the
interface is designed — is a short entry point that points into `knowledge/` of this checkout, so the
knowledge exists once, here, and the skill and the people read the same pages. The manufacturer
manuals the skill consults are kept locally beside it and are **not** in this repository; see
[sources](knowledge/sources.md#manufacturer-manuals) for where to get them.

## Trademarks

Pro DJ Link and rekordbox are trademarks of AlphaTheta Corporation. Pioneer DJ is a trademark of
Pioneer Corporation. CDJ is a product name of theirs. Serato, Traktor and Grapes are trademarks of
their owners. Where these pages use the names, they only say what A³ works with or is compared to.
**A³ is not affiliated with, endorsed or certified by AlphaTheta, Pioneer or any other manufacturer
named here.** See the [trademark page of the A³ documentation](https://a3-audio.github.io/a3-doc/ressources/trademarks.html).

## Licence

[REUSE](https://reuse.software/)-compliant; see `.reuse/dep5` and `LICENSES/`. Documents, figures and
research data CC-BY-SA-4.0; code GPL-3.0-or-later.
