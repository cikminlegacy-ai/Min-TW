#!/usr/bin/env python3
"""Energy-based pause finder for noisy rooms (fans, AC) where ffmpeg silencedetect misses pauses.
usage: silences.py audio.wav [speech_db] > silences.txt   (16 kHz mono wav; lines "start end")
A 20 ms frame is "quiet" when RMS < speech_db (default: noise floor + 9 dB, max -24).
Very quiet rooms (noise floor below -50 dB): pass about floor+13 (e.g. -46). Check soft/whispered lines survive (RMS scan) — -40 cut a quiet "kau faham-faham je lah" in PB1.
Single loud frames inside a pause are tolerated (median filter), pauses >= 0.22 s are printed."""
import sys, wave, numpy as np
wf = wave.open(sys.argv[1]); sr = wf.getframerate()
a = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768
hop = int(0.02 * sr); n = len(a) // hop
db = np.array([20 * np.log10(np.sqrt((a[i*hop:(i+1)*hop] ** 2).mean()) + 1e-9) for i in range(n)])
floor = np.percentile(db, 10)
thr = float(sys.argv[2]) if len(sys.argv) > 2 else min(floor + 9, -24)
q = (db < thr).astype(int)
k = 5; pad = np.pad(q, k // 2, mode="edge")
q = np.array([int(np.median(pad[i:i+k])) for i in range(n)])
out, start = [], None
for i, v in enumerate(list(q) + [0]):
    if v and start is None: start = i
    if not v and start is not None:
        if (i - start) * 0.02 >= 0.22: out.append((start * 0.02, i * 0.02))
        start = None
sys.stderr.write(f"noise floor {floor:.1f} dB, threshold {thr:.1f} dB, {len(out)} pauses\n")
for s, e in out: print(f"{s:.3f}\t{e:.3f}")
