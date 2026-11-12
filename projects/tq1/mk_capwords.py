#!/usr/bin/env python3
"""Caption words from a Whisper transcript of the cut audio (cut2.wav = cuts.json segments at 1.0x, no holds),
mapped to output time and spelling-fixed.  usage: mk_capwords.py cut_transcript.json > cap_words.json"""
import json, sys
c = json.load(open("cuts.json")); SP = c["speed"]; segs = c["segments"]
cum = []; acc = 0.0
for s in segs:
    cum.append(acc); acc += s["src_out"] - s["src_in"]
def seg_of(tau):
    for k, (s, c0) in enumerate(zip(segs, cum)):
        if tau < c0 + s["src_out"] - s["src_in"]: return k
    return len(segs) - 1
def to_out(tau, k):
    s, c0 = segs[k], cum[k]; L = s["src_out"] - s["src_in"]
    return round(s["t"] + min(max(tau - c0, 0), L) / SP, 3)
FIX = {"Talakil": "talaqi", "Tajwid": "tajwid", "Talaqi": "talaqi", "mahrosh,": "makhraj,", "makroshnya,": "makhrajnya,",
       "Enggak": "Sebab", "tajuk": "tajwid", "nakol": "naql", "Nakol": "naql", "Sakta.": "saktah.", "fap,": "faham,", "ok,": "okey,", "ok.": "okey.", "ok": "okey", "sakta.": "saktah.", "practical": "praktikal", "pump,": "faham,",
       "disebab": "sebab", "Okay": "Okey", "Okay,": "Okey,", "Okay.": "Okey."}
out = []
for seg in json.load(open(sys.argv[1])):
    for w in seg["words"]:
        t = w["w"].strip()
        if not t: continue
        if t.startswith("-") and out:
            out[-1]["text"] += t; out[-1]["end"] = to_out(w["e"], seg_of((w["s"] + w["e"]) / 2)); continue
        k = seg_of((w["s"] + w["e"]) / 2)            # a word belongs to the segment holding its midpoint
        out.append({"text": FIX.get(t, t), "start": to_out(w["s"], k), "end": to_out(w["e"], k)})
for i, w in enumerate(out):
    if w["text"] == "kurang" and i and out[i - 1]["text"].lower() == "ilmu": w["text"] = "Quran"
# phrase fixes where Whisper dropped/misheard words (checked against the first verification pass + source)
REPL = [(["Baca", "kan."], ["Kan", "dah", "selesai", "baca", "kan?"]),
        (["apa", "ni", "hukum-hukum", "tajuknya", "dia."], ["benda", "hukum-hukum", "tajwid", "yang", "ada."]),
        (["Dia", "tiga", "group", "kan."], ["Dalam", "kelas", "saya", "ada", "tiga", "group", "kan?"])]
for old, new in REPL:
    for i in range(len(out) - len(old) + 1):
        if [w["text"] for w in out[i:i + len(old)]] == old:
            a, b = out[i]["start"], out[i + len(old) - 1]["end"]
            if i and len(new) > len(old): a = min(a, out[i - 1]["end"] + 0.05)   # Whisper squeezed the dropped words; give them room
            d = (b - a) / len(new)
            out[i:i + len(old)] = [{"text": t, "start": round(a + j * d, 3), "end": round(a + (j + 1) * d, 3)} for j, t in enumerate(new)]
            break
    else:
        print("WARN no match", old, file=sys.stderr)
# split glued "Al-Quran." style tokens are fine; capitalise "Quran"
for w in out:
    if w["text"].lower().startswith("al-quran"): w["text"] = "Al-Quran" + w["text"][8:]
json.dump(out, sys.stdout, ensure_ascii=False, indent=0)
