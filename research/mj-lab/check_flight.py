"""Sanity checks of the flight port against the plan's Task 4-7 behaviours."""
import math
from flight import *

def fly(bodies, bars, tun=None, orders=None, seed=1, n=1, dt=1/128):
    t = tun or FlightTuning()
    w = FlightWorld(seed, t, n)
    for ch in range(n):
        x, y, _, _ = rabbit_at(0, ch, 4, t); w.launch(ch, (x, y), 0, 4)
    o = orders or [Orders(flying=ch < n) for ch in range(4)]
    path = []; steps = int(bars * 4 / dt)
    for i in range(steps):
        tb = i * dt
        w.step(o, bodies, tb, 4, gravity_pulse(tb, 4, t), dt)
        r = rabbit_at(tb + dt, 0, 4, t, w.phase_offset[0])
        path.append((tb, w.p[0], w.v[0], r[:2]))
    return path

p = fly([], 12)
d = [math.dist(q, r) for tb, q, v, r in p if tb > 16]
print("empty: max dist to rabbit after 4 bars %.3f (plan <0.1 w/o wander)" % max(d))
t0 = FlightTuning(wanderRadius=0)
d = [math.dist(q, r) for tb, q, v, r in fly([], 12, t0) if tb > 16]
print("empty, no wander: max %.3f mean %.3f" % (max(d), sum(d)/len(d)))
body = [(0.25, 0.0, 2.0)]
e = min(math.dist(q, body[0][:2]) for tb, q, v, r in fly([], 8, t0))
g = min(math.dist(q, body[0][:2]) for tb, q, v, r in fly(body, 8, t0))
print("group bends: closest approach empty %.3f with group %.3f" % (e, g))
dz = [(0.7*1.2, 0.0, -2.0)]
print("dead zone min dist %.3f" % min(math.dist(q, dz[0][:2]) for tb, q, v, r in fly(dz, 8, t0)))
o = [Orders(True, ESCORT, 0)] + [Orders(False) for _ in range(3)]
pe = fly([(0.3, -0.2, 2.0)], 8, t0, o)
ds = [math.dist(q, (0.3, -0.2)) for tb, q, v, r in pe if tb > 12]
print("escort: dist range %.3f..%.3f target %.3f" % (min(ds), max(ds), 0.15*math.sqrt(2)))
sp = [math.hypot(*v) for tb, q, v, r in pe]
print("escort speed range %.3f..%.3f" % (min(sp), max(sp)))
