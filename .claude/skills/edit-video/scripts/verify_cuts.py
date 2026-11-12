#!/usr/bin/env python3
"""List every transcript word that did NOT make it into the cut (rules.md §6 check).
usage: verify_cuts.py transcript.json cuts.json
A word counts as kept if any part of it (>= 40 ms) lies inside a kept segment.
Read the list: it must contain only what you meant to drop (fillers, repeats, false starts, salam…)."""
import json, sys
T = [w for s in json.load(open(sys.argv[1])) for w in s["words"]]
S = json.load(open(sys.argv[2]))["segments"]
lost, run = [], []
for w in T:
    ov = max((min(w["e"], s["src_out"]) - max(w["s"], s["src_in"]) for s in S), default=0)
    if ov < 0.04:
        run.append(w)
    elif run:
        lost.append(run); run = []
if run: lost.append(run)
n = sum(len(r) for r in lost)
print(f"{n} of {len(T)} words dropped, in {len(lost)} places:")
for r in lost:
    print(f"  {r[0]['s']:7.2f}-{r[-1]['e']:7.2f}  " + " ".join(w["w"].strip() for w in r))
