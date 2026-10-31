# The A³ instrument, from the booth

Advice that does not fit the instrument is noise. This is the shape of A³ as of 2026-10-31, seen from
the performer's side; the full user documentation is at <https://a3-audio.github.io/a3-doc/>.

## The parts

Devices sit on one PoE Ethernet switch and talk OSC over UDP.

- **A³ Core** — the computer everything plugs into, with a multichannel audio interface. Its program,
  **a3-core**, does the audio and computes the 3D (Ambisonics) sound field for the speakers, the
  booth and binaural headphones. It has a portrait touch screen for setup; during a set nobody needs to
  touch it.
- **A³ Mixer** — a 4-channel DJ mixer panel (gain, EQ, volume, PFL, FX key, AUX-Send, 3d per channel)
  that remote-controls Core. The same desk exists as an app, the virtual desk.
- **A³ Motion** — the device with the screen. Records and plays back *movement* per channel and sends
  it to Core, so a sound moves through the room in time with the music. Per channel: two encoders, one
  pot and a row of pads; global keys; and a **touchscreen**, which is how the whole interface is
  operated (the encoders do one fixed job each).
- **StemDeck** — up to four decks (A–D) that play tracks split into stems (drums, bass, other, vocals)
  and place each stem in the room themselves. Behaves like a CDJ-3000 on Pro DJ Link.
- **beat-analyzer** — follows the music's beat from the audio, or from Pro DJ Link, and gives the
  system its clock.

## The two ways sound moves

- **Stereo channel (CDJ, turntable, any ST input):** the 3d control pulls a filtered band (chosen by
  FREQ and Q) out of the stereo signal and moves it through the room, while the rest stays put.
  0 = plain stereo; 0.5 = the band in 3D and the rest steady (the sum is the original); 1 = only the
  filtered band, in 3D.
- **Stems (StemDeck):** a whole stem moves; no band filter is needed, because the stems are already
  separate. A stem at rest is steady; an action raises its 3D to full over its first beat and back over
  its last.

## What a performer does with Motion

Picks a clip, records a movement by dragging a blob across a sphere for a set number of bars (a quarter
bar up to 32), and plays it back in time; fires actions (momentary pads) for accents; loads a set that
puts a clip and six actions on each of four channels. Playback follows a beat clock: **INT** (tap
tempo), **EXT** (the beat-analyzer), or **PIO** (Pro DJ Link).

## Things worth remembering when proposing a change

- **Motion runs standalone.** A plain build is the full interface with mouse and touch and no panel
  attached. That is the default, not a degraded mode, and it is how the interface is tried and
  demoed. A proposal that only makes sense with a knob under the hand ignores most of its users.
- **The minimum room is four speakers, or just headphones** (maintainer, 2026-10-30).
- **Clips carry movement, not sound.** 3d, FREQ and Q are never recorded into clips; only actions
  (and later the pro-DJ's pilot) move them (A³ decision, 2026-10-07).
- **Core asks, devices answer.** Nothing is sent unasked at start-up; a device comes up by asking Core
  what the room is doing.
- **Cost** is to be published with a crowdfunding campaign; the docs carry no prices yet.
