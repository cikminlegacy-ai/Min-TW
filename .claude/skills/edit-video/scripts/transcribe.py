import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2] if len(sys.argv)>2 else "small", device="cpu", compute_type="int8")
import numpy as np, wave
wf=wave.open(sys.argv[1]); a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
segs, info = m.transcribe(a, language="ms", word_timestamps=True, vad_filter=False,
  initial_prompt=sys.argv[3] if len(sys.argv)>3 else "Abang akak, saya nak cerita.")
out=[]
for s in segs:
    out.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"w":w.word,"s":w.start,"e":w.end} for w in s.words]})
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}", flush=True)
json.dump(out, open("transcript.json","w"), ensure_ascii=False, indent=1)
