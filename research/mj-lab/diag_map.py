"""Perception map: frozen listeners on a grid, one ship, no bodies."""
import sys, math
from sim import Config, run
from flight import FlightTuning
from crowd import CrowdTuning
from mj import MJPolicy
lap = float(sys.argv[1]) if len(sys.argv) > 1 else 4
cfg = Config(ships=1, bars=24, flight=FlightTuning(wanderRadius=0, orbitLapBars=lap),
             crowd=CrowdTuning(start="grid", frozen=True), mj=MJPolicy(bodies="none"), trace=False)
import crowd
res = run(cfg)
print({k: round(v,3) for k,v in res.items()})
