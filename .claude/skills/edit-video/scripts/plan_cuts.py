#!/usr/bin/env python3
"""Turn kept source ranges + silence list into tight jump-cut segments.
usage: [SPEED=1.3] [MAX_GAP=0.3] plan_cuts.py keep.json silences.txt transcript.json > cuts.json
SPEED (user rule 2026-11-12: 1.2-1.3): output plays faster; segment dur = src len / SPEED (holds unscaled).
keep.json: [[src_start, src_end, "label"(, hold_s)], ...]  (ranges to keep, in order; optional hold_s = freeze+silence
           inserted AFTER that range, e.g. 1.2 after a painful line — funnel 4 / funnel 2 pauses)
silences.txt: lines "start end" from ffmpeg silencedetect
Every silence inside a kept range longer than MAX_GAP is removed (jump cut).
Output: segments with src in/out and output timeline position, plus remapped words."""
import json, sys, os
MAX_GAP = float(os.environ.get("MAX_GAP", 0.3))   # user 2026-11-12: thinking pauses cut tight (was 0.5)
SPEED = float(os.environ.get("SPEED", 1.0))
PAD = 0.06       # breathing room either side of speech
MIN_SEG = 0.22   # drop slivers shorter than this
keep = json.load(open(sys.argv[1]))
sil = [tuple(map(float, l.split())) for l in open(sys.argv[2]) if l.strip()]
words = [w for s in json.load(open(sys.argv[3])) for w in s["words"]]
segs = []
for item in keep:
    a, b, label = item[:3]; hold = float(item[3]) if len(item) > 3 else 0.0
    cur = a
    for s, e in sil:
        if e <= a or s >= b: continue
        s2, e2 = max(s, a), min(e, b)
        if e2 - s2 > MAX_GAP:
            if s2 + PAD > cur + 0.05:
                segs.append([cur, min(s2 + PAD, b), label])
            cur = max(e2 - PAD, cur)
    if b - cur > 0.05: segs.append([cur, b, label])
    if hold > 0 and segs: segs[-1] = segs[-1][:3] + [hold]
segs = [sg for sg in segs if sg[1] - sg[0] >= MIN_SEG or len(sg) > 3]
# snap every boundary (and hold) to the 30 fps frame grid: video segments are frame-quantised, audio is not,
# and 170 unsnapped segments drift ~1 s (PB1). Snapped, video and audio lengths match exactly.
FPS = 30
def snap(x): return round(round(x * FPS) / FPS, 4)
def snapseg(a, b):   # output length (b-a)/SPEED must be whole frames
    a = snap(a); n = max(1, round((b - a) / SPEED * FPS)); return a, round(a + n / FPS * SPEED, 4)
segs = [list(snapseg(sg[0], sg[1])) + sg[2:3] + ([snap(sg[3])] if len(sg) > 3 else []) for sg in segs]
segs = [sg for sg in segs if sg[1] > sg[0]]
out, t = [], 0.0
for sg in segs:
    a, b, label = sg[:3]; hold = sg[3] if len(sg) > 3 else 0.0
    o = {"src_in": round(a, 4), "src_out": round(b, 4), "t": round(t, 4), "dur": round((b - a) / SPEED, 4), "label": label}
    if SPEED != 1: o["speed"] = SPEED
    if hold: o["hold"] = hold
    out.append(o)
    t += (b - a) / SPEED + hold
# remap words that fall inside kept segments
mw = []
for w in words:
    mid = (w["s"] + w["e"]) / 2
    for sg in out:
        ov = min(w["e"], sg["src_out"]) - max(w["s"], sg["src_in"])
        if ov > 0.06 or (sg["src_in"] <= mid < sg["src_out"]):
            f = lambda x: sg["t"] + (x - sg["src_in"]) / SPEED
            mw.append({"text": w["w"].strip(), "start": round(f(max(w["s"], sg["src_in"])), 3),
                       "end": round(f(min(w["e"], sg["src_out"])), 3)})
            break
mw.sort(key=lambda w: w["start"])
json.dump({"total": round(t, 3), "speed": SPEED, "segments": out, "words": mw}, sys.stdout, ensure_ascii=False, indent=1)
