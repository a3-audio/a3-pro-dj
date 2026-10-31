# The booth: what a performer's hands and eyes can do

A³ is built for DJs and live acts of all kinds. It is not a studio tool, an installation controller
or a mixing desk. Whatever it does, it does while somebody is playing to a room. Every rule in this
knowledge base comes back to that, and this page is where it starts.

## Five facts about the booth

A desk at midday is nothing like a booth at 2am. Designs that forget it look fine in a screenshot and
fail in front of a crowd.

- **Nobody reads.** Not labels, not menus, not values. They glance. If something has to be read to be
  understood, it will be got wrong.
- **One hand is busy.** The other one is on this. Anything needing two hands competes with the mix.
- **There is no undo in front of an audience.** A control that can ruin the moment needs to be hard to
  hit by accident, and a way back needs to exist.
- **It is dark and it moves.** Contrast beats subtlety; a target the size of a fingertip beats a target
  the size of a cursor.
- **Timing is the medium.** A control that responds late has responded wrong. If something has to land
  on a beat, the interface must let it.

Argue from these. "It would look cleaner" is not an argument; "you cannot find that in the dark without
looking away from the deck" is.

## Meet the expectation the DJ already has

A DJ arriving at A³ is not a beginner. They have thousands of hours on CDJs and a mixer, and they carry
expectations that were shaped there (see [gear](../gear/)). The strongest design move is usually **to
meet an expectation they already have** rather than to teach them a new one. Before proposing
anything, ask: *what does this person already do for this?*

- **Loop lengths are beats and bars in powers of two**, because that is what a loop control on a deck
  offers. A length in seconds would be correct and useless. Below a bar, count beats; from a bar up,
  count bars. "64 beats" means nothing in a booth; "16 bars" does.
- **Tempo is a number you can see at all times, and sync is a state you can see at all times.** Both
  belong where the eye already goes.
- **A hot cue is instant and unforgiving. A loop is a thing you sit inside.** Those are different mental
  models, and a control that blurs them feels wrong for reasons the user cannot name.
- **Colour identifies a channel.** That is not decoration; it is how a deck is found without reading.
- **Quantised by default, with an override for when the moment will not wait.** Starting on the next
  downbeat is what the DJ expects; a "now" variant (A³ uses SHIFT) is what saves a moment.
- **State is shown by light, not by text.** A loop that is on is a lit LOOP key, not the words
  "LOOP OFF" when it is off (A³ decision, 2026-10-28, after the CDJ).

## How to argue a design question

- **Derive, don't decorate.** The question is rarely "which of these looks better". It is "which of
  these matches something the performer already does". Trace a recommendation back to a habit, a
  constraint, or a moment in a set. If you cannot, say that you are guessing.
- **Name the moment.** Put a recommendation in a scene: *"mid-transition, one hand on the crossfader,
  needing to arm a take on the next downbeat"* tells a developer more than "improve discoverability".
- **Say what it costs.** A bigger button takes room from something else, a confirmation step costs a
  beat, a mode saves space and costs certainty. An argument with no cost in it is a sales pitch.
- **Prefer removing.** A booth interface gets better mostly by having less on it. Before adding, check
  whether something can carry two meanings or go away.
- **Distinguish knowledge from hunch.** "DJs expect loop lengths in powers of two" is knowledge. "A swipe
  would feel better here" is a hunch. Label them differently: a hunch presented as knowledge wastes a
  build cycle.
- **Disagree once, with the reason.** If a change is elegant in code and wrong on stage, say so plainly,
  once — then let the decision be made.

## A rule that holds in one configuration only is not a rule

A performer may see only one device (a StemDeck, say) and expect its record key to record. A feature
that is right in the full rig but silently stops working in a smaller one fails in front of an
audience, and nobody in the booth will know why. So A³'s behaviour has to work in **every**
configuration it can be set up in, without hand-wiring — recording works whatever is connected, Pro DJ
Link behaves like a CDJ-3000 whatever network it is on. (A³ decision, 2026-10-28.)
