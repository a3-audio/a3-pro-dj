# DJ mixers: what a DJM user expects, and how the A³ Mixer differs

A club DJ's mixer is a Pioneer DJ DJM or something laid out like one. This page records the mixer
habits A³ has to meet or explain, and where the A³ Mixer (hardware panel and virtual desk) does it
differently. "Verify" marks a fact taken from memory, not from a manual.

## What a DJM user expects

- **Channel strip**: trim (gain), a three-band EQ, a channel fader, a cue (PFL) key; a crossfader.
- **The EQ is an isolator**: each band can kill its range completely. A DJ needs to know whether an EQ
  kills, and whether it boosts.
- **Color FX**: one knob shared by all channels, applied per channel by its own key — filter, noise,
  echo and similar.
- **Beat FX**, tempo-synced, set in beats. On the DJM-900NXS2: delay and echo from **1/16 to 16
  beats**; filter, flanger and phaser cycles from **1/16 to 64 beats**; no dedicated auto-pan, but
  PING PONG and TRANS exist (DJM-900NXS2 manual).
- **Tap tempo** for the effects' BPM when no clock is there (several taps averaged — verify).
- **Meters** on every channel and the master, with a clear clip indication.
- **Booth and headphone (cue) outputs** with their own levels.

## The A³ Mixer, against that

- **Channel strip**: gain, EQ HIGH / MID / LOW, volume, PFL (cue), an FX key, **AUX-Send**, and **3d**
  (how much of the channel goes into the room — the control a DJM does not have).
- **EQ**: −inf … 0 dB per band, i.e. a kill with no boost. Say it in those words for a DJM user.
- **One shared filter with an FX key per channel** — closer to a DJM's Color FX knob than to a filter
  per channel. One sentence in the docs prevents a DJ looking for a per-channel filter.
- **AUX-Send into a delay** whose tempo follows the music (live clock, then the MASTER deck, then the
  playing deck, then the last value). The sends come back on the **FX Return**, which is always
  B-format plus the analog return; it has its own level, meter and cue.
- **Inputs**: decks A–D (StemDeck) and **ST**, the stereo analog input, chosen on an input ring per
  channel.
- **No motor faders.** A value changed elsewhere leaves the hardware fader where it is; touching it
  takes over (soft takeover, "a physical turn wins"). A ring on the desk shows where the hardware knob
  stands elsewhere. See [live on stage](../best-practices/live-on-stage.md#the-hardware-fader-that-does-not-move).
- **LOCK** on master, booth and phones keeps a set from being wrecked by a stray hand.
- **No reset gesture on the master** — deliberately, because it would make the whole room loud at once.
- **Meters**: the same ballistics on every display in the system (see
  [preparation](../best-practices/preparation.md#levels-and-meters)).
- **Cue**: each deck's cue reaches the headphones as binaural (decoded from B-format, one HRTF for
  everything), so the movement can be heard in the phones.

## Stereo DJ effects in 3D

A DJ's Beat FX vocabulary translates into movement in the room; the translations are in
[spatial FX](../spatial/spatial-fx.md).
