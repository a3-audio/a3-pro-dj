"""Run named rounds from rounds.py and print their summary tables.
    nice -n 19 python3 -u go.py [--seeds N] <round> [<round> ...]
A round name ending in * runs every round with that prefix."""
import sys
from rounds import R
from lab import sweep, summary

if __name__ == "__main__":
    args = sys.argv[1:]
    seeds = (1, 2, 3, 4, 5, 6)
    if args and args[0] == "--seeds":
        seeds = tuple(range(1, int(args[1]) + 1))
        args = args[2:]
    names = []
    for a in args:
        names += [k for k in R if k.startswith(a[:-1])] if a.endswith("*") else [a]
    for name in names:
        out = sweep(name, R[name], seeds=seeds)
        print(summary(out))
        print(flush=True)
