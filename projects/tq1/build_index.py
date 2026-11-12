#!/usr/bin/env python3
"""TQ1 — 5 Cara Belajar Tajwid & Talaqi. Builds index.html (one composition, everything inline).
Style copies BAHAN/REFERENCE.mov (rules.md §13); subtitles per rules.md §12; Quran per §14.
Run: python3 build_index.py"""
import json, html, re

cuts = json.load(open("cuts.json"))
SEGS = cuts["segments"]; SP = cuts["speed"]; END = round(cuts["total"], 3)

def M(src):
    """source time -> output time"""
    for s in SEGS:
        if s["src_in"] - 0.02 <= src <= s["src_out"] + 0.02:
            return round(s["t"] + (min(max(src, s["src_in"]), s["src_out"]) - s["src_in"]) / SP, 3)
    for s in SEGS:
        if s["src_in"] > src: return round(s["t"], 3)
    return END

HOLDS = [(round(s["t"] + s["dur"], 3), s["hold"]) for s in SEGS if s.get("hold")]
(TQ_T, TQ_D), (TE_T, TE_D), (PR_T, PR_D) = HOLDS          # talaqi, teori, praktikal
BROLL_AUDIO = [("talaqi", TQ_T, TQ_D), ("teori", TE_T, TE_D), ("praktikal", PR_T, PR_D)]

# ---------------- Quran text (Quran.com API, QPC Hafs = KFGQPC Uthmanic Script HAFS v18 encoding)
def qpc(key):
    if key.startswith("67:"):
        for v in json.load(open("data/mulk2.json"))["verses"]:
            if v["verse_key"] == key: return v["text_qpc_hafs"]
    return json.load(open(f"data/v_{key.replace(':', '_')}.json"))["verse"]["text_qpc_hafs"]

def gold(text, frag):
    """colour the whole WORD(s) containing frag (never a lone combining mark: it would break Arabic shaping)"""
    assert frag in text, (frag, text)
    i = text.index(frag); a = text.rfind(" ", 0, i) + 1; b = text.find(" ", i + len(frag)); b = len(text) if b < 0 else b
    return html.escape(text[:a]) + '<span class="g">' + html.escape(text[a:b]) + '</span>' + html.escape(text[b:])

A_6714 = html.escape(qpc("67:14"))
v181 = qpc("18:1"); A_181 = gold(v181[v181.index("وَلَمۡ"):], "ۜ")                 # ... عِوَجَاۜ ١
v4911 = qpc("49:11"); i = v4911.index("بِئۡسَ"); A_4911 = gold(v4911[i:v4911.index("وَمَن", i)].strip(), "ٱلِٱسۡمُ")
v3652 = qpc("36:52"); A_3652 = gold(v3652, "ۜ")

# ---------------- camera: subtle punch on jump cuts, >= 4 s apart (no shake)
cycle = [1.0, 1.07, 1.0, 1.12, 1.04, 1.1]; cam = []; last = -9; k = 0
for s in SEGS:
    if s["t"] - last >= 4.0:
        cam.append((round(s["t"], 3), cycle[k % len(cycle)])); k += 1; last = s["t"]

# ---------------- overlays (times = source seconds unless noted; converted with M)
# section chips (top): (src_time, label)
CHIPS = [(0.0, "5 cara belajar tajwid & talaqi"), (18.9, "Video simulasi · kelas dewasa"),
         (33.9, "01 · Modul kelas"), (52.38, "02 · Guru yang mahir"), (81.7, "03 · Berani baca depan guru"),
         (141.7, "04 · Sesi teori"), (173.85, "05 · Praktikal yang kreatif"), (221.25, "Kelima-lima mesti berkait"),
         (255.05, "Ada soalan? Tanya saya")]
# big title cards (chest): (src_in, src_out, label, title_html)
CARDS = [(0.35, 6.4, "BELAJAR TAJWID &amp; TALAQI", '5 Cara <i>berkesan</i>'),
         (10.4, 13.3, "UMUR", '50an <span class="dot">·</span> 60an'),
         (34.0, 37.4, "CARA 01", 'Modul <i>Kelas</i>'),
         (52.5, 56.0, "CARA 02", 'Guru <i>Mahir</i>'),
         (81.75, 83.6, "CARA 03", 'Pelajar <i>Baca</i>'),
         (94.0, 96.1, "UMUR", '50 <span class="dot">·</span> 60 <span class="dot">·</span> 70an'),
         (141.75, 145.5, "CARA 04", 'Sesi <i>Teori</i>'),
         (157.85, 159.65, "TOPIK SIMULASI", 'Saktah <span class="amp">&amp;</span> <i>Naql</i>'),
         (173.9, 177.6, "CARA 05", 'Praktikal <i>Kreatif</i>'),
         (200.5, 201.45, "DALAM KELAS SAYA", '3 <i>Group</i>'),
         (204.4, 205.6, "GROUP PERTAMA BACA", '3 <span class="dot">·</span> 2 <span class="dot">·</span> 1'),
         (222.3, 224.15, "KESIMPULAN", 'Mesti <i>berkait</i>'),
         (255.1, 260.25, "NAK TAHU LAGI DETAIL?", 'Tanya di <i>komen</i>'),
         (272.0, 275.0, "JANGAN LUPA", '<i>Follow</i> saya')]
# stacked point pills (left, chest): groups; each (src_time, text, mark) ; group cleared at end src
PILLS = [
    ((6.62, 9.4), [(6.95, "Nombor 3", ""), (7.95, "Nombor 5", "")]),
    ((14.0, 17.75), [(16.1, "Rasa kerdil dalam kelas", "")]),
    ((39.3, 44.1), [(39.4, "Tanpa modul", "x"), (40.4, "Kelas kurang teratur", "x")]),
    ((57.5, 72.2), [(61.1, "Makhraj · tempat keluar huruf", ""), (65.8, "Sifat huruf", ""), (69.5, "Bunyi panjang · pendek", "")]),
    ((86.1, 90.3), [(86.15, "Guru baca dulu", ""), (89.2, "Lepas tu pelajar baca", "")]),
    ((96.75, 101.0), [(96.8, "Takut nak baca", "x"), (98.7, "Takut ditegur", "x")]),
    ((101.5, 115.0), [(107.2, "Ilmu dari guru", "v"), (112.3, "Support kawan sekelas", "v")]),
    ((128.9, 141.2), [(134.0, "Jarang datang", "x"), (135.2, "Malu kawan dah ke depan", "x")]),
    ((146.85, 151.3), [(147.5, "Rungkai hukum tajwid", "")]),
    ((184.9, 199.95), [(189.1, "Terlalu fakta", "x"), (191.7, "Terikat dengan buku", "x"), (199.4, "Buat ikut group", "v")]),
    ((228.95, 242.85), [(228.2, "Kelas", ""), (229.5, "Praktik di rumah", ""), (235.5, "Ilmu melekat", "v"), (241.85, "Ilmu lain pun boleh", "v")]),
    ((245.15, 254.0), [(245.2, "Cara penyampaian", ""), (250.4, "Tiru style ni", "v")]),
]
# muted B-roll cutaways over the talk: (src_in, src_out, file, media_start, mode)  mode: full | card
CUTS = [(19.0, 27.3, "opening", 2.0, "full"),
        (27.7, 32.5, "dewasa", 0.0, "full"),
        (44.2, 49.45, "modul", 0.0, "card"),
        (86.1, 90.3, "perbetul", 1.0, "full"),
        (112.25, 115.0, "sesama", 0.0, "full"),
        (131.3, 136.7, "teliti", 2.0, "full"),
        (146.85, 151.3, "msurat", 0.0, "full"),
        (209.58, 214.7, "simulasi", 0.0, "full"),
        (228.95, 233.0, "cekhukum", 0.0, "full")]
# emotion beats (rules.md §3C, subtle): (src_time, kind)
EMO = [(16.6, "surprise"), (113.0, "happy"), (135.3, "surprise"), (235.5, "happy"), (242.2, "happy"), (250.5, "happy")]

# ---------------- captions (rules.md §12): 3-5 words, ONE line, B/W, fixed at belly height
# text = Whisper re-transcription of the final cut audio (cap_words.json, already mapped to output time + fixed)
words = json.load(open("cap_words.json"))
T = json.load(open("broll_plan.json"))["teori"]; off = 0.0; tw = []
for a, b in T:                       # teacher speech inside the teori insert
    for seg in json.load(open("teori_words.json")):
        for w in seg["words"]:
            m = (w["s"] + w["e"]) / 2
            if a <= m < b: tw.append({"text": w["w"].strip(), "start": round(TE_T + off + w["s"] - a, 3), "end": round(TE_T + off + w["e"] - a, 3)})
    off += b - a
for w in tw:
    w["text"] = {"hujurat": "Hujurat"}.get(w["text"], w["text"])
words = sorted(words + tw, key=lambda w: w["start"])
words = [w for w in words if not (TQ_T <= w["start"] < TQ_T + TQ_D or PR_T <= w["start"] < PR_T + PR_D)]

MAXC = 30
def L(ws): return len(" ".join(x["text"] for x in ws))
phr, cur = [], []
for w in words:
    if cur and w["start"] - cur[-1]["end"] > 0.5: phr.append(cur); cur = []
    cur.append(w)
    if re.search(r"[.?!,]$", w["text"]): phr.append(cur); cur = []
if cur: phr.append(cur)
# glue tiny phrases (1-2 words) to a neighbour when the result still fits one line of <=5 words
g = []
for p in phr:
    if g and (len(p) < 3 or len(g[-1]) < 3) and len(g[-1]) + len(p) <= 5 and L(g[-1] + p) <= MAXC and p[0]["start"] - g[-1][-1]["end"] < 0.7:
        g[-1] = g[-1] + p
    else:
        g.append(p)
chunks = []
for p in g:
    k = 1
    while True:
        n = len(p); size = [n // k + (1 if i < n % k else 0) for i in range(k)]
        parts, i0 = [], 0
        for sz in size: parts.append(p[i0:i0 + sz]); i0 += sz
        if all(len(x) <= 5 and L(x) <= MAXC for x in parts) or k >= n: break
        k += 1
    chunks += parts
CAP = []
for i, c in enumerate(chunks):
    a = c[0]["start"]; nxt = chunks[i + 1][0]["start"] if i + 1 < len(chunks) else END
    b = min(nxt, c[-1]["end"] + 0.6)
    CAP.append((round(a, 3), round(max(b, a + 0.4), 3), " ".join(x["text"] for x in c)))

# ---------------- helpers to emit HTML
def chip_html():
    out = []
    times = [M(t) if t else 0.0 for t, _ in CHIPS]
    for n, ((t, lab), a) in enumerate(zip(CHIPS, times)):
        b = times[n + 1] if n + 1 < len(times) else END
        out.append((f'<div class="chip" id="chip{n}"><span class="ic"></span>{html.escape(lab)}</div>', a, b))
    return out
chips = chip_html()
cards = [(f'<div class="card" id="card{n}"><div class="lab">{lab}</div><div class="ttl">{ttl}</div></div>', M(a), M(b))
         for n, (a, b, lab, ttl) in enumerate(CARDS)]
pills = []
for g, ((ga, gb), items) in enumerate(PILLS):
    end = M(gb) + 0.35
    for j, (t, txt, mk) in enumerate(items):
        mark = {"x": '<span class="mk x">✕</span>', "v": '<span class="mk v">✓</span>', "": ""}[mk]
        pills.append((f'<div class="pill" id="pill{g}_{j}" style="top:{1010 + j * 74}px">{html.escape(txt)}{mark}</div>', M(t), end, mk))

body, js = [], []
# cutaways
for n, (a, b, f, ms, mode) in enumerate(CUTS):
    s, e = M(a), M(b); d = round(e - s, 3)
    if mode == "full":
        body.append(f'<div class="cut clip" id="cut{n}" data-start="{s}" data-duration="{d}" data-track-index="3">'
                    f'<video id="cutv{n}" class="clip" data-start="{s}" data-duration="{d}" data-media-start="{ms}" data-track-index="4" src="assets/video/{f}.mp4" muted playsinline></video><div class="shade"></div></div>')
        js.append(f'tl.fromTo("#cut{n}", {{opacity:0}}, {{opacity:1, duration:0.25, ease:"power2.out"}}, {s});')
        js.append(f'tl.fromTo("#cutv{n}", {{scale:1.06}}, {{scale:1.0, duration:{d}, ease:"none"}}, {s});')
        js.append(f'tl.to("#cut{n}", {{opacity:0, duration:0.2, ease:"power2.in"}}, {round(e - 0.2, 3)});')
    else:
        body.append(f'<div class="cut clip" id="cut{n}" data-start="{s}" data-duration="{d}" data-track-index="3">'
                    f'<video id="cutb{n}" class="clip bg" data-start="{s}" data-duration="{d}" data-media-start="{ms}" data-track-index="4" src="assets/video/{f}_blur.mp4" muted playsinline></video>'
                    f'<div class="vcard" id="vcard{n}"><video id="cutv{n}" class="clip" data-start="{s}" data-duration="{d}" data-media-start="{ms}" data-track-index="5" src="assets/video/{f}.mp4" muted playsinline></video></div></div>')
        js.append(f'tl.fromTo("#cut{n}", {{opacity:0}}, {{opacity:1, duration:0.3, ease:"power2.out"}}, {s});')
        js.append(f'tl.fromTo("#vcard{n}", {{y:60, scale:0.94}}, {{y:0, scale:1, duration:0.45, ease:"power3.out"}}, {s});')
        js.append(f'tl.to("#cut{n}", {{opacity:0, duration:0.25, ease:"power2.in"}}, {round(e - 0.25, 3)});')

# b-roll inserts WITH their own audio (talk is frozen+silent underneath)
for f, t, d in BROLL_AUDIO:
    body.append(f'<div class="cut clip" id="ins-{f}" data-start="{t}" data-duration="{d}" data-track-index="3">'
                f'<video id="insv-{f}" class="clip" data-start="{t}" data-duration="{d}" data-track-index="6" src="assets/video/{f}.mp4" data-has-audio="true" data-volume="1" playsinline></video><div class="shade"></div></div>')
    js.append(f'tl.fromTo("#ins-{f}", {{opacity:0}}, {{opacity:1, duration:0.3, ease:"power2.out"}}, {t});')
    js.append(f'tl.to("#ins-{f}", {{opacity:0, duration:0.25, ease:"power2.in"}}, {round(t + d - 0.25, 3)});')

# ayat cards (inside the inserts): (id, start, end, chip, ref, arabic_html, note, top)
AYAT = [("a6714", TQ_T + 0.4, TQ_T + TQ_D - 0.3, "Talaqi · guru baca, pelajar ikut", "AL-MULK · 67:14", A_6714, "Guru baca dulu, kemudian pelajar ikut bacaan yang sama.", 900),
        ("a181", TE_T + 5.4, TE_T + 15.5, "Saktah · sin kecil ( ۜ )", "AL-KAHF · 18:1", A_181, "Berhenti seketika pada ۜ tanpa ambil nafas baru.", 820),
        ("a4911", TE_T + 15.6, TE_T + TE_D - 0.3, "Naql · pindah baris", "AL-HUJURAT · 49:11", A_4911, "Satu-satunya tempat naql dalam riwayat Hafs.", 820),
        ("a3652", PR_T + 1.7, PR_T + PR_D - 0.3, "Praktikal · baca ikut group", "YĀ SĪN · 36:52", A_3652, "Saktah pada مَّرۡقَدِنَاۜ — berhenti seketika, tanpa nafas.", 860)]
for aid, a, b, chip, ref, ar, note, top in AYAT:
    a, b = round(a, 3), round(b, 3)
    body.append(f'<div class="ayat clip" id="{aid}" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="7" style="top:{top}px">'
                f'<div class="aref">{ref}</div><div class="ar" dir="rtl" lang="ar">{ar}</div><div class="anote">{html.escape(note)}</div></div>')
    js.append(f'tl.fromTo("#{aid}", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {a});')
    js.append(f'tl.to("#{aid}", {{opacity:0, y:-12, duration:0.25, ease:"power2.in"}}, {round(b - 0.25, 3)});')
    chips.append((f'<div class="chip" id="c{aid}"><span class="ic"></span>{html.escape(chip)}</div>', a, b))

# chips (top) — cross-fade
for n, (h, a, b) in enumerate(chips):
    a, b = round(a, 3), round(b, 3)
    body.append(h.replace('class="chip"', f'class="chip clip" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="8"', 1))
    cid = re.search(r'id="([^"]+)"', h).group(1)
    js.append(f'tl.fromTo("#{cid}", {{opacity:0, y:-14}}, {{opacity:1, y:0, duration:0.35, ease:"power3.out"}}, {a});')
for n, (h, a, b) in enumerate(cards):
    body.append(h.replace('class="card"', f'class="card clip" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="9"', 1))
    js.append(f'tl.fromTo("#card{n}", {{opacity:0, y:30, scale:0.97}}, {{opacity:1, y:0, scale:1, duration:0.4, ease:"power3.out"}}, {a});')
    js.append(f'tl.fromTo("#card{n} i", {{opacity:0, x:-10}}, {{opacity:1, x:0, duration:0.4, ease:"power2.out"}}, {round(a + 0.25, 3)});')
    js.append(f'tl.to("#card{n}", {{opacity:0, y:-10, duration:0.25, ease:"power2.in"}}, {round(b - 0.25, 3)});')
for h, a, b, mk in pills:
    pid = re.search(r'id="([^"]+)"', h).group(1)
    body.append(h.replace('class="pill"', f'class="pill clip" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="10"', 1))
    js.append(f'tl.fromTo("#{pid}", {{opacity:0, x:-24}}, {{opacity:1, x:0, duration:0.3, ease:"power3.out"}}, {a});')
    js.append(f'tl.to("#{pid}", {{opacity:0, duration:0.2}}, {round(b - 0.2, 3)});')
# captions
for n, (a, b, txt) in enumerate(CAP):
    body.append(f'<div class="cap clip" id="cap{n}" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="11">{html.escape(txt)}</div>')
    js.append(f'tl.fromTo("#cap{n}", {{opacity:0, y:6}}, {{opacity:1, y:0, duration:0.1, ease:"power1.out"}}, {a});')

# emotion beats (subtle)
emo_js = []
for t, kind in EMO:
    t = M(t)
    if kind == "happy":
        emo_js.append(f'tl.fromTo("#fx-glow", {{opacity:0}}, {{opacity:0.8, duration:0.4, ease:"sine.out", immediateRender:false}}, {t}).to("#fx-glow", {{opacity:0, duration:1.2, ease:"sine.in"}}, {t + 0.9});')
    else:
        emo_js.append(f'tl.fromTo("#punch", {{scale:1.06}}, {{scale:1, duration:0.4, ease:"power3.out", immediateRender:false}}, {t});')

# ---------------- audio
AUD = []
def sfx(i, t, f, d, v, ms=0, fade=0):
    AUD.append(f'<audio id="sfx-{i}" class="clip" data-start="{round(t, 3)}" data-duration="{d}"' + (f' data-media-start="{ms}"' if ms else "") +
               f' data-track-index="{20 + len(AUD) % 3}" src="assets/sfx/{f}.mp3" data-volume="{v}"' +
               (f' data-fade-in="{fade}" data-fade-out="{fade}"' if fade else "") + '></audio>')
REC = [(TQ_T, TQ_T + TQ_D), (PR_T, PR_T + PR_D)]           # Quran recitation: no music, no sfx
def free(t): return not any(a - 0.4 <= t <= b + 0.2 for a, b in REC)
for n, (h, a, b) in enumerate(chips):
    if n and free(a): sfx(f"chip{n}", a, "whoosh-short", 0.57, 0.16)
for n, (h, a, b) in enumerate(cards):
    if free(a): sfx(f"card{n}", a, "pop", 0.72, 0.14)
sfx("hook", 0.3, "impact-bass-1", 2.1, 0.22)
for h, a, b, mk in pills:
    if free(a): sfx(f"pill{a}", a, "click-soft", 0.37, 0.32)
for n, (a, b, f, ms, mode) in enumerate(CUTS):
    sfx(f"cut{n}", M(a), "whoosh", 0.57, 0.14)
for t, kind in EMO:
    sfx(f"emo{t}", M(t), "chime" if kind == "happy" else "whoosh-cinematic", 2.5 if kind == "happy" else 1.2, 0.16 if kind == "happy" else 0.14)
sfx("modul-paper", M(38.2), "using_thick_paper", 1.6, 0.35, 3.0, 0.2)
sfx("buku-paper", M(191.7), "using_thick_paper", 1.4, 0.30, 8.0, 0.2)
sfx("rungkai-pen", M(147.5), "drawing_on_paper_with_pencil", 2.2, 0.30, 4.0, 0.3)
sfx("teori-pen", TE_T + 0.2, "drawing_on_paper_with_pencil", 1.6, 0.18, 10.0, 0.3)

# music lane: duck under voice, silent during recitation, a bit up on the teori insert (teacher voice is roomy)
pts = [(0, 0.0), (0.6, 0.10)]
for a, b in REC:
    pts += [(a - 0.5, 0.10), (a, 0.0), (b, 0.0), (b + 0.8, 0.10)]
pts += [(END - 1.5, 0.10), (END, 0.0)]
lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": round(t, 3), "v": v} for t, v in sorted(pts)]}]}).replace('"', "&quot;")

cam_js = ", ".join(f"[{t}, {s}]" for t, s in cam)
NL = "\n      "
html_out = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>TQ1 - 5 Cara Belajar Tajwid &amp; Talaqi</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family:"Inter"; src:url("assets/fonts/inter.woff2") format("woff2"); font-weight:100 900; }}
      @font-face {{ font-family:"Playfair Display"; src:url("assets/fonts/playfair.woff2") format("woff2"); font-weight:400 900; }}
      @font-face {{ font-family:"Playfair Display"; src:url("assets/fonts/playfair-italic.woff2") format("woff2"); font-weight:400 900; font-style:italic; }}
      @font-face {{ font-family:"UthmanicHafs"; src:url("assets/fonts/UthmanicHafs1Ver18.woff2") format("woff2"); }}
      :root {{ --glass: rgba(18,18,20,.66); --line: rgba(255,255,255,.14); --gold: #D7B46A; }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#101012; }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:"Inter", sans-serif; }}
      #cam {{ position:absolute; inset:0; z-index:1; transform-origin:540px 640px; }}
      #punch {{ position:absolute; inset:0; transform-origin:540px 640px; }}
      #cam video {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
      #fx-glow {{ position:absolute; inset:0; z-index:2; pointer-events:none; opacity:0; mix-blend-mode:soft-light;
        background:radial-gradient(ellipse at 50% 35%, rgba(255,214,150,.75) 0%, rgba(215,180,106,.25) 45%, rgba(215,180,106,0) 75%); }}
      #bottomshade {{ position:absolute; left:0; right:0; top:1120px; height:420px; z-index:3; pointer-events:none;
        background:linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,.28) 45%, rgba(0,0,0,.28) 70%, rgba(0,0,0,0) 100%); }}
      .cut {{ position:absolute; inset:0; z-index:4; overflow:hidden; background:#101012; }}
      .cut video {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
      .cut .shade {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,.35) 0%, rgba(0,0,0,0) 22%, rgba(0,0,0,0) 52%, rgba(0,0,0,.55) 78%, rgba(0,0,0,.35) 100%); }}
      .cut video.bg {{ opacity:.9; }}
      .vcard {{ position:absolute; left:190px; top:330px; width:700px; height:1244px; border-radius:30px; overflow:hidden;
        box-shadow:0 30px 80px rgba(0,0,0,.55); border:1px solid var(--line); }}
      .vcard video {{ width:700px; height:1244px; }}
      .chip {{ position:absolute; left:50%; top:228px; transform:translateX(-50%); z-index:12; white-space:nowrap;
        display:flex; align-items:center; gap:12px; padding:13px 26px 13px 18px; border-radius:999px;
        background:var(--glass); border:1px solid var(--line); color:#fff; font-weight:600; font-size:28px; letter-spacing:.2px;
        backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px); }}
      .chip .ic {{ width:14px; height:14px; border-radius:50%; background:var(--gold); box-shadow:0 0 0 4px rgba(215,180,106,.22); }}
      .card {{ position:absolute; left:50%; top:930px; transform:translateX(-50%); z-index:13; text-align:center; white-space:nowrap;
        padding:26px 56px 30px; border-radius:26px; background:var(--glass); border:1px solid var(--line);
        backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px); }}
      .card .lab {{ color:var(--gold); font-weight:700; font-size:22px; letter-spacing:7px; margin-bottom:6px; }}
      .card .ttl {{ color:#fff; font-family:"Playfair Display", serif; font-weight:700; font-size:84px; line-height:1.05; }}
      .card .ttl i {{ display:inline-block; color:var(--gold); font-style:italic; font-weight:600; }}
      .card .dot, .card .amp {{ color:rgba(255,255,255,.55); }}
      .pill {{ position:absolute; left:64px; z-index:13; white-space:nowrap; display:flex; align-items:center; gap:14px;
        padding:14px 24px; border-radius:16px; background:var(--glass); border:1px solid var(--line); color:#fff;
        font-weight:600; font-size:30px; backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px); }}
      .pill .mk {{ font-size:24px; font-weight:800; width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; }}
      .pill .mk.v {{ color:#101012; background:var(--gold); }}
      .pill .mk.x {{ color:#fff; background:rgba(255,255,255,.18); }}
      .ayat {{ position:absolute; left:60px; width:960px; z-index:14; padding:30px 40px 30px; border-radius:28px; text-align:center;
        background:rgba(14,14,16,.78); border:1px solid rgba(215,180,106,.35); backdrop-filter:blur(18px); -webkit-backdrop-filter:blur(18px); }}
      .ayat .aref {{ color:var(--gold); font-weight:700; font-size:22px; letter-spacing:6px; }}
      .ayat .ar {{ font-family:"UthmanicHafs", serif; color:#fff; font-size:60px; line-height:1.85; margin:10px 0 8px; }}
      .ayat .ar .g {{ color:var(--gold); }}
      .ayat .anote {{ color:rgba(255,255,255,.78); font-weight:500; font-size:26px; }}
      .cap {{ position:absolute; left:0; right:0; top:1268px; z-index:15; text-align:center; white-space:nowrap;
        color:#fff; font-weight:800; font-size:46px; letter-spacing:.2px;
        text-shadow:0 2px 10px rgba(0,0,0,.65), 0 0 2px rgba(0,0,0,.9); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
      <div id="cam"><div id="punch">
        <video id="talk" class="clip" data-start="0" data-duration="{END}" data-track-index="0" src="assets/video/talk.mp4" muted playsinline></video>
      </div></div>
      <div id="fx-glow" data-layout-ignore></div>
      <div id="bottomshade" data-layout-ignore></div>
      {NL.join(body)}
      <audio id="voice" class="clip" data-start="0" data-duration="{END}" data-track-index="1" src="assets/video/voice.m4a" data-volume="1"></audio>
      <audio id="music" class="clip" data-start="0" data-duration="{END}" data-track-index="2" src="assets/music/ambient-blu.mp3" data-volume="1" data-fade-in="1.5" data-fade-out="1.5" data-automation="{lane}"></audio>
      {NL.join(AUD)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const CAM = [{cam_js}];
      for (const [t, s] of CAM) tl.set("#cam", {{ scale: s }}, t);
      {NL.join(js)}
      {NL.join(emo_js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(html_out)
print("index.html: end", END, "| holds", HOLDS, "| captions", len(CAP), "| cuts", len(CUTS), "| sfx", len(AUD))
bad = [c for c in CAP if not (1 <= len(c[2].split()) <= 5)]
print("caption word counts:", {n: sum(1 for c in CAP if len(c[2].split()) == n) for n in range(1, 8)}, "max chars", max(len(c[2]) for c in CAP))
