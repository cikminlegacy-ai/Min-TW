#!/usr/bin/env python3
"""Caption words from a Whisper transcript of the cut audio (cut2.wav = cuts.json segments at 1.0x, no holds),
mapped to output time and spelling-fixed.  usage: mk_capwords.py cut_transcript.json > cap_words.json"""
import json, sys
c = json.load(open("cuts.json")); SP = c["speed"]; segs = c["segments"]
cum = []; acc = 0.0
for s in segs:
    cum.append(acc); acc += s["src_out"] - s["src_in"]
def to_out(tau):
    for s, c0 in zip(segs, cum):
        L = s["src_out"] - s["src_in"]
        if tau < c0 + L: return round(s["t"] + max(tau - c0, 0) / SP, 3)
    return round(segs[-1]["t"] + segs[-1]["dur"], 3)
FIX = {"Talakil": "talaqi", "Tajwid": "tajwid", "Talaqi": "talaqi", "mahrosh,": "makhraj,", "makroshnya,": "makhrajnya,",
       "Enggak": "Sebab", "tajuk": "tajwid", "nakol": "naql", "sakta.": "saktah.", "practical": "praktikal", "pump,": "faham,",
       "disebab": "sebab", "Okay": "Okey", "Okay,": "Okey,", "Okay.": "Okey."}
out = []
for seg in json.load(open(sys.argv[1])):
    for w in seg["words"]:
        t = w["w"].strip()
        if not t: continue
        if t.startswith("-") and out:
            out[-1]["text"] += t; out[-1]["end"] = to_out(w["e"]); continue
        out.append({"text": FIX.get(t, t), "start": to_out(w["s"]), "end": to_out(w["e"])})
for i, w in enumerate(out):
    if w["text"] == "kurang" and i and out[i - 1]["text"].lower() == "ilmu": w["text"] = "Quran"
# split glued "Al-Quran." style tokens are fine; capitalise "Quran"
for w in out:
    if w["text"].lower().startswith("al-quran"): w["text"] = "Al-Quran" + w["text"][8:]
json.dump(out, sys.stdout, ensure_ascii=False, indent=0)
