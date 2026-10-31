"""Experiment runner: seeded sweeps, 2 worker processes under nice."""
import json, math, os, sys, time, copy
from multiprocessing import Pool
from dataclasses import replace
from sim import Config, run

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(RESULTS, exist_ok=True)


def _one(args):
    name, cfg = args
    os.nice(0)
    r = run(cfg)
    r.pop("trace", None)
    return name, cfg.seed, r


def sweep(round_name, conditions, seeds=(1, 2, 3, 4, 5, 6), workers=2):
    """conditions: dict name -> function(seed) -> Config."""
    jobs = [(n, f(s)) for n, f in conditions.items() for s in seeds]
    t0 = time.time()
    out = {n: [] for n in conditions}
    with Pool(workers) as pool:
        for name, seed, r in pool.imap_unordered(_one, jobs):
            out[name].append(dict(seed=seed, **r))
    for n in out:
        out[n].sort(key=lambda d: d["seed"])
    with open(os.path.join(RESULTS, round_name + ".json"), "w") as f:
        json.dump(out, f, indent=0)
    print("# %s: %d runs in %.0f s" % (round_name, len(jobs), time.time() - t0))
    return out


def summary(out, keys=("engagement", "bottomQuarter", "perceived", "boredom", "fatigue", "eventsPerBar",
                       "grouped", "largest", "turnStd", "onPath", "clarity")):
    rows = []
    head = "| condition | " + " | ".join(keys) + " |"
    rows.append(head)
    rows.append("|" + "---|" * (len(keys) + 1))
    for n, runs in out.items():
        cells = []
        for k in keys:
            v = [r[k] for r in runs]
            m = sum(v) / len(v)
            sd = math.sqrt(sum((x - m) ** 2 for x in v) / max(1, len(v) - 1))
            cells.append("%.3f±%.3f" % (m, sd))
        rows.append("| %s | %s |" % (n, " | ".join(cells)))
    return "\n".join(rows)


def load(round_name):
    with open(os.path.join(RESULTS, round_name + ".json")) as f:
        return json.load(f)


def paired(out, ref, key="engagement"):
    """Per condition: mean of (condition - ref) over shared seeds, its standard
    error, and how many seeds went the same way."""
    refd = {r["seed"]: r[key] for r in out[ref]}
    res = {}
    for n, runs in out.items():
        d = [r[key] - refd[r["seed"]] for r in runs if r["seed"] in refd]
        m = sum(d) / len(d)
        sd = math.sqrt(sum((x - m) ** 2 for x in d) / max(1, len(d) - 1))
        res[n] = (m, sd / math.sqrt(len(d)), sum(1 for x in d if x > 0), len(d))
    return res


def paired_table(out, ref, keys=("engagement", "bottomQuarter", "boredom", "fatigue")):
    rows = ["| vs %s | " % ref + " | ".join("Δ " + k for k in keys) + " |", "|" + "---|" * (len(keys) + 1)]
    ps = {k: paired(out, ref, k) for k in keys}
    for n in out:
        if n == ref:
            continue
        rows.append("| %s | %s |" % (n, " | ".join("%+.3f ± %.3f (%d/%d up)" % ps[k][n] for k in keys)))
    return "\n".join(rows)
