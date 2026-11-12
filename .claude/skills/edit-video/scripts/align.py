"""Accurate word timings: CTC forced alignment (MMS-300m aligner, HF MahmoudAshraf/mms-300m-1130-forced-aligner)
of a Whisper transcript. Whisper's own word times drift up to ~0.7 s after pauses — too loose for filler cuts.
usage: align.py audio16k.wav transcript.json model_dir out.json
out: same structure, words get refined s/e (+ 'sc' score)."""
import sys, json, re, wave, numpy as np, torch, torchaudio.functional as F
from transformers import Wav2Vec2ForCTC
wav, tj, md, out = sys.argv[1:5]
wf = wave.open(wav); sr = wf.getframerate(); assert sr == 16000
A = torch.from_numpy(np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768)
model = Wav2Vec2ForCTC.from_pretrained(md).eval(); vocab = json.load(open(md + "/vocab.json"))
torch.set_num_threads(4)
# emissions over whole file in 30 s windows with 2 s context each side
FR = 0.02; W = 30; C = 2; em = []
with torch.inference_mode():
    t = 0.0; dur = len(A) / sr
    while t < dur:
        a0 = max(0, t - C); a1 = min(dur, t + W + C)
        x = A[int(a0 * sr):int(a1 * sr)]; x = (x - x.mean()) / (x.std() + 1e-7)
        lp = torch.log_softmax(model(x[None]).logits[0], -1)
        i0 = int(round((t - a0) / FR)); n = int(round(min(W, dur - t) / FR))
        em.append(lp[i0:i0 + n]); t += W
E = torch.cat(em)
NUM = {'0':'kosong','1':'satu','2':'dua','3':'tiga','4':'empat','5':'lima','6':'enam','7':'tujuh','8':'lapan','9':'sembilan'}
def norm(w):
    w = w.lower()
    w = re.sub(r'\d+', lambda m: ' '.join(NUM[c] for c in m.group()), w)
    return ''.join(c for c in w if c in vocab and c not in "'")
segs = json.load(open(tj))
words = [w for s in segs for w in s["words"]]
# align in groups of consecutive segments (~20 s) with margin
groups, cur = [], []
for s in segs:
    cur.append(s)
    if cur[-1]["end"] - cur[0]["start"] > 20: groups.append(cur); cur = []
if cur: groups.append(cur)
for g in groups:
    ws = [w for s in g for w in s["words"]]
    a0 = max(0, g[0]["start"] - 1.5); a1 = min(E.shape[0] * FR, g[-1]["end"] + 1.5)
    f0, f1 = int(a0 / FR), int(a1 / FR)
    toks, owner = [], []
    for k, w in enumerate(ws):
        for c in norm(w["w"]): toks.append(vocab[c]); owner.append(k)
    if not toks: continue
    em_ = E[f0:f1][None]
    try:
        al, sc = F.forced_align(em_, torch.tensor([toks], dtype=torch.int32), blank=0)
    except Exception as e:
        print("skip group", g[0]["start"], e, file=sys.stderr); continue
    al = al[0].tolist(); sc = sc[0].exp().tolist()
    # walk frames: each token occupies a run of its id (repeats separated by blank)
    ti = -1; prev = 0; span = {}
    for fi, tok in enumerate(al):
        if tok != 0 and (tok != prev or prev == 0):
            ti += 1
        if tok != 0 and ti < len(owner):
            k = owner[ti]; s_, e_, ss = span.get(k, (fi, fi, []))
            span[k] = (min(s_, fi), max(e_, fi), ss + [sc[fi]])
        prev = tok
    for k, w in enumerate(ws):
        if k in span:
            s_, e_, ss = span[k]
            w["s"] = round(a0 + s_ * FR, 3); w["e"] = round(a0 + (e_ + 1) * FR, 3); w["sc"] = round(float(np.mean(ss)), 3)
json.dump(segs, open(out, "w"), ensure_ascii=False, indent=1)
print("aligned", len(words), "words")
