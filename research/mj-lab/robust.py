"""Do the core rankings survive changes to the listener model? Reads r8_*."""
import os
from lab import load, paired, RESULTS
from rounds import PERTURB

REF = "ref (2 ships, lap 4, 3k/2oct, loop)"
CLAIMS = [
    # (label, condition, metric, expected sign of (condition - ref))
    ("2 ships beat 4", "4 ships", "engagement", -1),
    ("2 ships beat 1", "1 ship", "engagement", -1),
    ("lap 4 bars beats lap 2", "lap 2 bars", "engagement", -1),
    ("lap 4 bars beats lap 8", "lap 8 bars", "engagement", -1),
    ("8 kHz/2 oct beats 3 kHz/2 oct", "8k/2oct", "engagement", +1),
    ("2 oct beats 1 oct", "3k/1oct", "engagement", -1),
    ("bodies cut boredom", "no bodies", "boredom", +1),
    ("bodies cost the least served", "no bodies", "bottomQuarter", +1),
]


def table():
    rows = []
    for pn in PERTURB:
        name = "r8_" + pn.replace(" ", "_").replace("/", "-")
        if not os.path.exists(os.path.join(RESULTS, name + ".json")):
            continue
        out = load(name)
        cells = []
        for label, cond, key, sign in CLAIMS:
            m, se, up, n = paired(out, REF, key)[cond]
            held = (m * sign > 0)
            cells.append((held, m, se))
        rows.append((pn, cells))
    return rows


if __name__ == "__main__":
    rows = table()
    print("| perturbation | " + " | ".join(c[0] for c in CLAIMS) + " |")
    print("|" + "---|" * (len(CLAIMS) + 1))
    for pn, cells in rows:
        print("| %s | %s |" % (pn, " | ".join(("yes" if h else "**NO**") + " %+.3f" % m for h, m, se in cells)))


CLAIMS24 = [
    ("plan + cap beats plan as written", "D plan + cap rule", "P plan as written"),
    ("lab flight beats plan + cap", "E lab flight", "D plan + cap rule"),
    ("lab flight beats the bare orbit", "E lab flight", "C bare orbit"),
    ("moves beat no moves (lab flight)", "F lab flight + hold/double", "E lab flight"),
    ("lab + moves beats the bare orbit", "F lab flight + hold/double", "C bare orbit"),
]


def table24():
    rows = []
    for pn in PERTURB:
        name = "r24_" + pn.replace(" ", "_").replace("/", "-")
        if not os.path.exists(os.path.join(RESULTS, name + ".json")):
            continue
        out = load(name)
        cells = []
        for label, a, b in CLAIMS24:
            m, se, up, n = paired(out, b, "engagement")[a]
            cells.append((m > 0, m, se))
        rows.append((pn, cells))
    return rows
