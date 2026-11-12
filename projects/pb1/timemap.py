"""Map times authored against the OLD cut (cuts_old.json) to the NEW cut (cuts.json) via source time.
M(t): old output time -> source time -> new output time. Used by build_scenes.py and build_index.py."""
import json, os
_old = json.load(open("cuts_old.json"))["segments"] if os.path.exists("cuts_old.json") else None
_new = json.load(open("cuts.json"))["segments"]
def _to_src(t):
    for s in _old:
        a = s["t"]; b = a + s["dur"] + s.get("hold", 0)
        if a - 1e-6 <= t < b:
            return s["src_in"] + min(t - a, s["dur"]) * s.get("speed", 1)
    return _old[-1]["src_out"] + (t - (_old[-1]["t"] + _old[-1]["dur"] + _old[-1].get("hold", 0)))
def _to_new(src):
    best = None
    for s in _new:
        if s["src_in"] - 1e-6 <= src <= s["src_out"] + 1e-6:
            return round(s["t"] + (src - s["src_in"]) / s.get("speed", 1), 3)
        if s["src_in"] > src:   # src fell in a removed pause: snap to the next kept segment start
            return round(s["t"], 3)
    last = _new[-1]
    return round(last["t"] + last["dur"] + last.get("hold", 0) + (src - last["src_out"]), 3)
class Src(float):
    """A time given in SOURCE seconds (for notes added after the first cut)."""
def M(t):
    if isinstance(t, Src): return _to_new(float(t))
    if _old is None: return t
    return _to_new(_to_src(t))
NEW_TOTAL = json.load(open("cuts.json"))["total"]
