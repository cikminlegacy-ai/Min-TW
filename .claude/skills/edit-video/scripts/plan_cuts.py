#!/usr/bin/env python3
"""Turn kept source ranges + silence list into tight jump-cut segments.
usage: plan_cuts.py keep.json silences.txt transcript.json > cuts.json
keep.json: [[src_start, src_end, "label"(, hold_s)], ...]  (ranges to keep, in order; optional hold_s = freeze+silence
           inserted AFTER that range, e.g. 1.2 after a painful line — funnel 4 / funnel 2 pauses)
silences.txt: lines "start end" from ffmpeg silencedetect
Every silence inside a kept range longer than MAX_GAP is removed (jump cut).
Output: segments with src in/out and output timeline position, plus remapped words."""
import json, sys
MAX_GAP = 0.18   # keep at most this much of any pause
PAD = 0.07       # breathing room either side of speech
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
out, t = [], 0.0
for sg in segs:
    a, b, label = sg[:3]; hold = sg[3] if len(sg) > 3 else 0.0
    o = {"src_in": round(a, 3), "src_out": round(b, 3), "t": round(t, 3), "dur": round(b - a, 3), "label": label}
    if hold: o["hold"] = hold
    out.append(o)
    t += b - a + hold
# remap words that fall inside kept segments
mw = []
for w in words:
    mid = (w["s"] + w["e"]) / 2
    for sg in out:
        ov = min(w["e"], sg["src_out"]) - max(w["s"], sg["src_in"])
        if ov > 0.06 or (sg["src_in"] <= mid < sg["src_out"]):
            off = sg["t"] - sg["src_in"]
            mw.append({"text": w["w"].strip(), "start": round(max(w["s"], sg["src_in"]) + off, 3),
                       "end": round(min(w["e"], sg["src_out"]) + off, 3)})
            break
mw.sort(key=lambda w: w["start"])
json.dump({"total": round(t, 3), "segments": out, "words": mw}, sys.stdout, ensure_ascii=False, indent=1)
