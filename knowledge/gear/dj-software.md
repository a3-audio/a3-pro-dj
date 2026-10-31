# DJ software: rekordbox, Serato, Traktor

What the three main DJ software families mean to a DJ arriving at A³, and where A³ meets them. This
page is general DJ knowledge plus A³'s decisions; nothing here comes from a vendor manual, so details
that matter for an implementation must be checked against the vendor's current documentation.

## What they are to a DJ

- **rekordbox** (AlphaTheta / Pioneer DJ) is the library and preparation tool of the CDJ world:
  tracks are analysed at home (beat grid, BPM, key, waveform), hot cues and loops are set and stored,
  and the result is exported to a USB stick that any CDJ on the link can read. Beat sync and quantize on
  a CDJ need a track analysed this way (CDJ-3000X manual, p. 95 and 100). rekordbox can also perform on
  a laptop with a controller, and can be the sync master on a Pro DJ Link network.
- **Serato DJ Pro** is laptop-centred performance software with controllers and DVS (timecode vinyl);
  CDJ-3000-class players can also act as its controllers (the manufacturer publishes a connection
  guide).
- **Traktor Pro** (Native Instruments) is laptop-centred performance software with controllers and
  DVS; its manual is a good model for writing DJ documentation (goal-named tutorials, see
  [writing for DJs](../best-practices/documentation-for-djs.md)).

All three carry the same mental model: a **prepared library** (analysed grid, cues, loops), decks with
**sync and quantize**, loops in **powers of two**, and **hot cues** as instant jumps.

## Where A³ meets them

- **A³ follows the CDJ world over Pro DJ Link**, not the software directly. If a DJ plays rekordbox on
  CDJs, A³ follows the tempo master on the link (see [Pro DJ Link](pro-dj-link.md)).
- **A laptop DJ without a link** reaches A³ through the beat analyser (EXT: tempo from the audio) or tap
  tempo (INT).
- **StemDeck's library** is its own (folders of stems, artist > album > set), not a rekordbox or Serato
  library. Stems are prepared beforehand on the DJ's own computer, the way a rekordbox user analyses at
  home (see [preparation](../best-practices/preparation.md)).
- **No reading of the rekordbox database.** Its export database is encrypted; decrypting it is a legal
  question that needs a lawyer before anyone touches it (A³ decision, 2026-10-04).
- **One stick, every deck** — the rekordbox/CDJ habit A³ wants to copy for its own library (target, see
  [preparation](../best-practices/preparation.md#the-library-travels-on-one-stick)).
