# Pro DJ Link: the players' network, and how A³ joins it

Pro DJ Link is the Ethernet link between Pioneer DJ / AlphaTheta players and mixers. Through it the
players share one beat clock (the tempo master), share libraries (a USB stick in one player is
browsable from all), and tell the mixer and each other what they are doing. A DJ who plays CDJs
expects it to just work, and expects anything else on the link to behave like a player.

> Pro DJ Link and rekordbox are trademarks of AlphaTheta Corporation. Pioneer DJ is a trademark of
> Pioneer Corporation. CDJ is a product name of theirs. A³ is not affiliated with, endorsed or
> certified by AlphaTheta or Pioneer. A³'s Pro DJ Link support is an independent implementation for
> interoperability, built from public documentation of the protocol. See the
> [trademark notice in the A³ documentation](https://a3-audio.github.io/a3-doc/ressources/trademarks.html).

## What a DJ expects from the link

- **One tempo master.** One player is master (its MASTER key lit); every player with BEAT SYNC on
  follows its tempo and beat position. Master moves when the master's track changes or it pauses, when
  its MASTER key is pressed, or when another player's MASTER key is pressed (CDJ-3000X manual, p. 101).
- **Player numbers** 1–6 on a CDJ-3000, set to Auto or fixed; the mixer channel matches the player.
- **A USB stick in any player serves every player.**
- **The link is plug-in.** A player has one network port and works on whatever network it is plugged
  into; nobody configures a subnet in the booth.
- **On someone else's network, ask first.** Joining a venue's link is at your own risk; ask the venue
  before connecting.

## How A³ uses it

- **A³ Motion's PIO clock mode** follows the link's tempo master: Motion's clips play in time with the
  CDJs. (Via the beat-analyzer, which joins the link as player 7 in its clock mode 2.)
- **StemDeck follows or leads the link.** With the sync source set to PIO, SYNC on a deck follows the
  link's tempo master (BPM including pitch) and lands its beats on the master's beats. StemDeck can
  also be master. Its decks claim player numbers like a player: **A = 6, B = 5, C = 4, D = 3**
  (decided 2026-10-28; deck B was 8 before, outside the CDJ-3000's 1–6).
- **StemDeck behaves like a CDJ-3000 on the link** (maintainer, 2026-10-28: "it must behave like
  pioneer dj cdj 3000"): it announces itself, claims its number in stages, gives a taken number up and
  says so ("player N is taken by …"), sends a keep-alive every 2 s, and sends no beat or status before
  its claim is done. It picks the network the machine is plugged into for the outside world (the
  default route), not a pinned subnet, with an override for odd hosts.
- **Beat, not bar.** A deck that follows the link aligns to the beat. Where the "one" is, the DJ sets
  by hand on the jog, as on a CDJ.
- **When the master falls silent** (paused, loading): the last tempo holds, no phase correction runs,
  and the display says "held" — the same rule as A³ Motion's external clocks (see
  [live on stage](../best-practices/live-on-stage.md#clock-follow-smoothly-never-trust-the-source)).
- **The delay follows the music.** The delay's tempo comes from the live beat clock, else the MASTER
  deck's BPM, else the playing deck's, else the last value (A³ decision, 2026-10-28) — so an echo is
  never at the wrong tempo just because nobody pressed MASTER.

### Known gaps against a real CDJ-3000 (2026-10-28)

Found while checking StemDeck against the public protocol analysis; each needs a real CDJ to settle:
- StemDeck's status packets use the older (nexus-2-class) layout, not the CDJ-3000's larger one.
- StemDeck sends status only while one of its decks is master; a CDJ sends status all the time, so a
  mixer sees StemDeck present but not its state while it follows.
- No tempo-master handoff: with a real CDJ on the link two masters can show, and pressing MASTER on a
  CDJ does not take it from StemDeck.
- To be accepted as master, the status claims an analysed USB track; a CDJ that then tries to browse
  that "USB" finds nothing.
- Mixer-assigned player numbers (on a DJM channel port) are not answered.
- Status and beats are broadcast (so every A³ listener on one host hears them); a CDJ sends status
  unicast. Whether a CDJ accepts broadcast status is unverified.

## The library, Pro DJ Link style (target)

Like the Pioneer world: one USB stick at any deck host serves every deck on the network, and A³ Core
can serve a library too. Decided 2026-10-29 as the target; not built. See
[preparation](../best-practices/preparation.md#the-library-travels-on-one-stick).

## Wording and legal rules (A³, 2026-10-04)

A legal orientation concluded that offering Pro DJ Link support is fine: A³'s implementation is its
own code, written from public documentation, and exchanges unencrypted UDP only. The risk is implied
endorsement, so:

- say **"works with Pro DJ Link"** and **"player 6"**; never "virtual CDJ" or "StemDeck is the CDJ";
- no logos; never "certified" or "official";
- **never port code** from beat-link (EPL-2.0) or dysentery (EPL-1.0) — writing from their
  documentation is fine;
- stay away from **rekordbox database decryption**; that needs a lawyer first;
- the trademark notice lives once in the A³ documentation; other places link to it.

## The protocol in one paragraph

UDP broadcast on ports 50000 (announce and keep-alive), 50001 (beats, and tempo-master takeover) and
50002 (status). Every packet starts with a fixed ten-byte magic and a type byte. A beat packet carries
the player number, the pitch, the track BPM and the beat within the bar (1–4); the effective BPM is
track BPM × pitch. A status packet carries, among much else, a "tempo master" flag and the BPM. The
byte layouts are documented in Deep Symmetry's DJ Link analysis (link in
[sources](../sources.md#pro-dj-link)); A³'s implementations are in the StemDeck and beat-analyzer
repositories.
