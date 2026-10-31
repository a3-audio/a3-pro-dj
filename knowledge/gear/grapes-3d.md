# Grapes 3D Audio Control: the reference problem

Grapes (Not a Number GmbH) is a VST3/standalone 3D-audio control application that does what A³
Motion does: it sequences **movement trajectories** for sound objects and sends them over OSC to
someone else's spatial engine (the guide lists, among others, SAD, the IEM plug-ins, L-ISA,
d&b Soundscape, Spat GRIS and ADM-OSC). It produces no audio itself. Facts below are paraphrased from its user
guide (v1.4.0); the guide is not in this repository — get it from the manufacturer, see
[sources](../sources.md#manufacturer-manuals).

The CDJ is the reference *instrument* (what the hands know, see [CDJ-3000](cdj-3000.md)). Grapes is
the reference *problem*: what parameters a trajectory needs, what they are called, what a clip has to
be able to do. It is the mature version of A³ Motion's vocabulary and shows where A³'s terms will have
to go.

## What to take from it: vocabulary and scope

- **Clips sit in a track × row matrix**; a row fires as a scene. A³ Motion has the same shape with four
  channels and a handful of slots.
- **Clip parameters split in two groups.** *Perform*: speed, speed quantise, offset, fade, direction,
  trigger mode, finished action, loop mode. *Transform*: position x/y/z, scale, rotate. A³'s clip
  settings bar is a subset of Perform — speed, fade, direction and end are the same four ideas.
- **Loop mode is explicit**: one shot (plays once, then hands over to the finished action), loop,
  repeat n times. The **finished action** then says where control goes: next, previous, first, last,
  random, jump.
- **Trigger mode is free / bar / beat** — scheduling on the next bar is a named setting, not a hidden
  behaviour. **Every transport action also has an "instantly" variant** that jumps the queue. That
  pairing is the important bit: quantised by default, with an override for when the moment will not
  wait. A³ does the same with SHIFT.
- **Movement presets** are geometric (line, triangle, square, circle, spiral, lissajous, waveshaper)
  plus behaviours (drag, follow, random, swarm, draw, read).

## Where it stops being a model

Grapes is a mouse-and-desktop program built for someone sitting down: modifier-plus-scroll quick
edits, drag-and-drop onto a trash can, alt-drag to duplicate, collapsible tabs, a zoomable canvas,
double-click to type numbers. None of that survives one hand and a touchscreen in the dark.

So take the **vocabulary and the feature scope** from Grapes, and the **interaction** from the CDJ. A
recommendation of a modifier key or a nested tab because Grapes has one has used it wrong.
