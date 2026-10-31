# Writing for DJs: documentation, names, and the buyer's question

How A³ talks to a DJ — in its docs, on its website, in its interface labels. Collected from two DJ
reviews of the A³ documentation (2026-09-29 and 2026-10-30), the go-live structure (2026-10-04), and
the maintainer's naming decisions.

## The question behind every page

> How does the DJ who wants to buy this find his happiness?

Every page of the docs and the website is written for a DJ who is considering A³ and wants to know how
it works. Lead with the moment in a set it helps with, what you need, what you do first, what you hear;
technical depth goes below. (Maintainer, 2026-10-30.)

A working club DJ arriving at A³ asks, in this order:
1. **What is it, and what does the room hear?** Something to hear (a binaural recording works on any
   headphones) and a picture of a crowd inside a ring of speakers beat any amount of text.
2. **What do I need?** Computer, audio interface, speakers, network, which parts are optional. A³'s
   minimum: **four speakers, or just headphones**. Say plainly what runs without hardware.
3. **What do I touch on the one?** A first set that ends on something he hears.
4. **What happens when it goes wrong?** A pre-gig card and a panic card (see
   [live on stage](live-on-stage.md)).

## How other DJ and performance manuals are built

| Source | Pattern |
| :--- | :--- |
| Traktor Pro manual, basic usage tutorials | tutorials named after a **goal** ("Mixing Your First Two Tracks"), prerequisites → numbered steps → a closing line saying what you achieved; the reference comes after |
| Ableton Live, *Live Concepts* | one short chapter defines the few nouns everything rests on, with concrete examples, and asks to be read early |
| Ableton Live, *Launching Clips* | **one line per mode** ("Gate: *down* starts the clip; *up* stops the clip"); launch quantisation is a named setting with its own section |
| Ableton Live, *First Steps* | "make sure it's installed and working" before any concept |
| Pioneer DJ quick-start guides | a separate quick start for connecting and first playback; the part-by-part reference is another document, built on a numbered panel diagram |
| Serato hardware quickstarts | one per piece of hardware, only how *this* box maps to the software |
| Elektron Digitakt quick start | gets you **playing the factory presets** before you make anything; hardware keys in brackets ([BANK]), so a key is never confused with a screen word |
| teenage engineering OP-1 field guide | short and imperative; safety lines blunt, one sentence each |

The common order: **quick start → concepts → performance features with one-line behaviour →
reference → troubleshooting**. Links are in [sources](../sources.md#documentation-and-manuals).

## Rules for A³'s pages

- **One page = one level.** Website: what A³ is, in one scroll. User overview: one screen per device —
  what it does, 3–5 features, a typical moment in a set. Reference: every function, by topic. An
  overview holds no details; a reference page holds no marketing.
- **Readers in this order:** DJs and live acts, then venues and promoters, then makers and developers.
  The main story speaks to DJs; the others each get one door.
- **Borrow the DJ's words.** *Quantise, sync, master, hot cue, loop*, bar and beat counts in powers of
  two. Don't invent new ones.
- **Say what the DJ hears, not what the machine does.** Not "crossfades the channel between its stereo
  and its multichannel encoder" but "3d: how much of the channel lives in the room. Fully down, it's
  plain stereo like any mixer. Turn it up, and the channel follows its blob."
- **Count loops in bars.** "64 beats" means nothing in a booth.
- **Warnings go at the top of their section, not in bullet seven.** "This changes the action
  everywhere" is a box, not a side clause.
- **A GIF earns its place when it shows time or space** — waiting for the downbeat, a rise and fall, a
  take, where the sound goes. A tap a sentence can describe needs no GIF; each one costs maintenance
  every time the look changes.
- **No changelog phrases in the manual** ("the newest eleven", "sets saved before …"): they are wrong
  at the next release.
- **Developer content leaves the user page**: OSC addresses, script syntax, port tables, design
  rationale.
- **Tone:** factual, second person, short sentences, at most one dry joke per section. Plain about
  danger. ("Delete removes the file, not the music. Whatever is loaded keeps playing, so you can't
  delete your way into silence.")

## One name per thing

The 2026-10-30 review found the same control under several names; a DJ cannot tell whether two names
are two things. The maintainer's names (2026-10-30/31):

| Thing | Name |
|---|---|
| the box everything plugs into | **A³ Core** |
| the program running on it (audio included) | **a3-core** (not "Engine" in user-visible text) |
| the stereo analog input | **ST** (not AN or A; A is deck A) |
| the send | **AUX-Send** |
| the 3D control | **3d** |
| the hardware mixer / the app | **A³ Mixer** / the virtual desk |
| the return of the sends | **FX Return** (always B-format plus analog, whatever feeds it) |

## A translation table for CDJ/DJM users

Proposed in the 2026-10-30 review, to be checked against the current system before publishing:

| On a CDJ/DJM | On A³ |
|---|---|
| Master Tempo | KEY on StemDeck |
| Beat Sync | SYNC on StemDeck; PIO on Motion |
| the Pro DJ Link tempo master | the master player; A³ follows it in PIO |
| Color FX (one knob, per channel) | one shared filter with an FX key per channel |
| Beat FX echo | AUX-Send into the delay, delay tempo from the beat |
| isolator EQ | EQ HIGH/MID/LOW, −inf … 0 dB (a kill with no boost — say it in those words) |
| CUE held + PLAY | the same on StemDeck: plays on without a gap |
