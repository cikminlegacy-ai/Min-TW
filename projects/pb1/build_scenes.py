#!/usr/bin/env python3
"""Emit PB1 scene files. Times below are ABSOLUTE (film time); each scene converts to local.
Run from the project dir:  python3 build_scenes.py"""
import os, html
from timemap import M, Src   # times below were authored on the first cut; M() moves them to the current cut
P = "."
KIT = '''
    @font-face { font-family:"Special Elite"; src:url("assets/fonts/special-elite.ttf") format("truetype"); font-weight:400; }
    #root { position:absolute; inset:0; overflow:hidden; }
    .paper { position:absolute; left:110px; width:820px; top:236px; padding:18px 30px 22px; background:#F2E8D5; color:#1B1A17;
      font-family:"Special Elite", monospace; box-shadow:0 14px 40px rgba(0,0,0,.45); opacity:0; border-radius:3px; text-align:center; }
    .paper .k { font-size:28px; color:#B23A2E; letter-spacing:.08em; }
    .paper .t { font-size:56px; line-height:1.08; }
    .paper .t .c { opacity:0; } .wd { white-space:nowrap; display:inline-block; }
    .stamp { position:absolute; font-family:"Special Elite", monospace; color:#B23A2E; border:6px solid #B23A2E; border-radius:10px;
      padding:4px 22px 8px; background:rgba(242,232,213,.9); line-height:1.05; text-align:center; opacity:0; box-shadow:0 10px 30px rgba(0,0,0,.4); }
    .big { position:absolute; left:60px; width:880px; top:236px; text-align:center; font-family:"Special Elite", monospace; color:#F2E8D5;
      font-size:92px; line-height:1.05; text-shadow:0 0 24px rgba(0,0,0,.9), 0 0 60px rgba(0,0,0,.6); opacity:0; }
    .chap { position:absolute; inset:0; background:#0E1726; opacity:0; }
    .chap .lab { position:absolute; left:60px; width:880px; top:780px; text-align:center; font-family:"Montserrat", sans-serif; font-weight:800;
      font-size:30px; letter-spacing:.4em; color:#F3A93C; }
    .chap .ti { position:absolute; left:60px; width:880px; top:830px; text-align:center; font-family:"Special Elite", monospace; font-size:80px; line-height:1.08; color:#F2E8D5; }
    .chap .ti .c { opacity:0; }
    .chap .glow { position:absolute; left:290px; top:500px; width:500px; height:500px; border-radius:50%;
      background:radial-gradient(circle, rgba(243,169,60,.35), rgba(243,169,60,0) 70%); }
    .shot { position:absolute; inset:0; background:#0E1726; opacity:0; }
    .shot .ph { position:absolute; left:90px; top:330px; width:900px; padding:18px 18px 80px; background:#F2E8D5; box-shadow:0 26px 70px rgba(0,0,0,.6); }
    .shot img { display:block; width:864px; height:auto; }
    .shot .cap { position:absolute; left:0; right:0; bottom:20px; text-align:center; font-family:"Special Elite", monospace; font-size:40px; color:#1B1A17; }
    .list { position:absolute; left:110px; width:820px; top:228px; padding:16px 30px 18px; background:#F2E8D5; color:#1B1A17; font-family:"Special Elite", monospace;
      box-shadow:0 14px 40px rgba(0,0,0,.45); opacity:0; border-radius:3px; }
    .list .h { font-size:30px; color:#B23A2E; letter-spacing:.06em; margin-bottom:4px; }
    .list .i { position:relative; font-size:38px; line-height:1.25; opacity:0; }
    .list .i i { position:absolute; left:-6px; top:52%; height:5px; width:0; background:#B23A2E; }
    .rain { position:absolute; left:-60px; top:-200px; width:1200px; height:2400px; opacity:0;
      background-image: repeating-linear-gradient(100deg, rgba(220,230,255,0) 0 22px, rgba(220,230,255,.20) 22px 24px, rgba(220,230,255,0) 24px 61px),
                        repeating-linear-gradient(104deg, rgba(220,230,255,0) 0 40px, rgba(220,230,255,.12) 40px 41px, rgba(220,230,255,0) 41px 97px); }
    .tint { position:absolute; inset:0; opacity:0; }
    .corner { position:absolute; width:120px; height:120px; border-color:#F3A93C; border-style:solid; border-width:0; opacity:0; }
'''

def typed(text):
    # letters are .c spans (typed one by one); each word is a nowrap .wd span so lines never break mid-word
    words = text.split(" ")
    return " ".join('<span class="wd">' + "".join(f'<span class="c">{html.escape(ch)}</span>' for ch in w) + "</span>" for w in words)

class Scene:
    def __init__(self, cid, t0, t1):
        self.cid, self.t0, self.t1 = cid, (0.0 if t0 == 0 else M(t0)), M(t1)
        self.body, self.js, self.n = [], [], 0
    def L(self, t): return round(t - self.t0, 3)
    def clip(self, cls, a, b, inner="", style="", extra=""):
        self.n += 1; i = f"{self.cid}-{self.n}"
        oa, ob = a, b
        a = max(M(a), self.t0); b = min(M(b), self.t1)
        if b - a < 0.6:
            print(f"WARN {self.cid}: element at {oa}-{ob} collapsed to {a}-{b} (its words were cut) — re-anchor with Src()")
            b = a + 1.2
        self.body.append(f'    <div id="{i}" class="{cls} clip" data-start="{self.L(a)}" data-duration="{round(b - a, 3)}"{(" style=\"" + style + "\"") if style else ""}{extra}>{inner}</div>')
        return i, self.L(a), self.L(b)
    # --- element kinds ---
    def paper(self, a, b, kicker, text, rot=-1.5):
        i, la, lb = self.clip("paper", a, b, f'<div class="k">{html.escape(kicker)}</div><div class="t">{typed(text)}</div>' if kicker else f'<div class="t">{typed(text)}</div>')
        self.js.append(f'tl.fromTo("#{i}", {{ opacity: 0, y: -30, rotation: {rot*3} }}, {{ opacity: 1, y: 0, rotation: {rot}, duration: 0.28, ease: "power3.out" }}, {la});')
        self.js.append(f'tl.fromTo("#{i} .t .c", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01, stagger: {min(0.035, 0.9/max(len(text),1)):.3f} }}, {la + 0.12});')
        self.js.append(f'tl.to("#{i}", {{ opacity: 0, y: -16, duration: 0.18, ease: "power2.in" }}, {round(lb - 0.2, 3)});')
    def stamp(self, a, b, text, left=180, top=300, size=70, rot=-6):
        i, la, lb = self.clip("stamp", a, b, html.escape(text), f"left:{left}px; top:{top}px; font-size:{size}px;")
        self.js.append(f'tl.fromTo("#{i}", {{ opacity: 0, scale: 2.2, rotation: {rot*2.5} }}, {{ opacity: 1, scale: 1, rotation: {rot}, duration: 0.2, ease: "expo.out" }}, {la});')
        self.js.append(f'tl.to("#{i}", {{ opacity: 0, duration: 0.16 }}, {round(lb - 0.17, 3)});')
    def big(self, a, b, text, color="#F2E8D5", size=92, top=236):
        i, la, lb = self.clip("big", a, b, typed(text), f"color:{color}; font-size:{size}px; top:{top}px;")
        self.js.append(f'tl.set("#{i}", {{ opacity: 1 }}, {la});')
        self.js.append(f'tl.fromTo("#{i} .c", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.12, stagger: {min(0.05, 1.0/max(len(text),1)):.3f} }}, {la});')
        self.js.append(f'tl.to("#{i}", {{ opacity: 0, filter: "blur(6px)", duration: 0.25 }}, {round(lb - 0.26, 3)});')
    def chapter(self, a, b, lab, title, warm=False):
        bg = "#2A1C10" if warm else "#0E1726"
        i, la, lb = self.clip("chap", a, b, f'<div class="glow"></div><div class="lab">{html.escape(lab)}</div><div class="ti">{typed(title)}</div>', f"background:{bg};")
        self.js.append(f'tl.fromTo("#{i}", {{ opacity: 0 }}, {{ keyframes: {{ opacity: [0, 1, 0.3, 1] }}, duration: 0.22, ease: "none" }}, {la});')
        self.js.append(f'tl.fromTo("#{i} .ti .c", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01, stagger: {min(0.045, 0.7/max(len(title),1)):.3f} }}, {la + 0.15});')
        self.js.append(f'tl.fromTo("#{i} .glow", {{ scale: 0.8, opacity: 0.6 }}, {{ keyframes: {{ scale: [0.8, 1.05, 0.95, 1.0], opacity: [0.6, 1, 0.7, 1] }}, duration: {round(lb - la, 3)}, ease: "none" }}, {la});')
        self.js.append(f'tl.to("#{i}", {{ opacity: 0, duration: 0.2 }}, {round(lb - 0.21, 3)});')
    def shot(self, a, b, src, cap, rot=-2):
        i, la, lb = self.clip("shot", a, b, f'<div class="ph"><img src="{src}" alt="{html.escape(cap)}"/><div class="cap">{html.escape(cap)}</div></div>', "background:rgba(14,23,38,.92);")
        self.js.append(f'tl.fromTo("#{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {la});')
        self.js.append(f'tl.fromTo("#{i} .ph", {{ y: 120, rotation: {rot*3}, scale: 0.9 }}, {{ y: 0, rotation: {rot}, scale: 1, duration: 0.45, ease: "expo.out" }}, {la});')
        self.js.append(f'tl.fromTo("#{i} .ph", {{ scale: 1 }}, {{ scale: 1.04, duration: {round(lb - la - 0.5, 3)}, ease: "none" }}, {la + 0.45});')
        self.js.append(f'tl.to("#{i}", {{ opacity: 0, duration: 0.22 }}, {round(lb - 0.23, 3)});')
    def checklist(self, a, b, head, items):
        """items: [(text, t_show, t_strike or None)]"""
        inner = f'<div class="h">{html.escape(head)}</div>' + "".join(f'<div class="i">{html.escape(t)}<i></i></div>' for t, _, _ in items)
        i, la, lb = self.clip("list", a, b, inner)
        self.js.append(f'tl.fromTo("#{i}", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, {la});')
        for k, (t, ts, tx) in enumerate(items):
            self.js.append(f'tl.fromTo("#{i} .i:nth-of-type({k + 2})", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.25 }}, {self.L(M(ts))});')
            if tx: self.js.append(f'tl.fromTo("#{i} .i:nth-of-type({k + 2}) i", {{ width: 0 }}, {{ width: "102%", duration: 0.3, ease: "power2.out" }}, {self.L(M(tx))});')
        self.js.append(f'tl.to("#{i}", {{ opacity: 0, duration: 0.2 }}, {round(lb - 0.21, 3)});')
    def rain(self, a, b):
        i, la, lb = self.clip("rain", a, b, "", extra=" data-layout-ignore")
        self.js.append(f'tl.fromTo("#{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, {la});')
        self.js.append(f'tl.fromTo("#{i}", {{ y: -600, x: 0 }}, {{ y: 0, x: -110, duration: {round(lb - la, 3)}, ease: "none" }}, {la});')
        self.js.append(f'tl.to("#{i}", {{ opacity: 0, duration: 0.8 }}, {round(lb - 0.8, 3)});')
    def tint(self, a, b, css, peak=1.0):
        i, la, lb = self.clip("tint", a, b, "", f"background:{css};", " data-layout-ignore")
        self.js.append(f'tl.fromTo("#{i}", {{ opacity: 0 }}, {{ opacity: {peak}, duration: 0.5 }}, {la});')
        self.js.append(f'tl.to("#{i}", {{ opacity: 0, duration: 0.5 }}, {round(lb - 0.5, 3)});')
    def corners(self, a, b):
        pos = [("left:70px;top:230px;", "border-top-width:6px;border-left-width:6px;"), ("right:70px;top:230px;", "border-top-width:6px;border-right-width:6px;"),
               ("left:70px;bottom:620px;", "border-bottom-width:6px;border-left-width:6px;"), ("right:70px;bottom:620px;", "border-bottom-width:6px;border-right-width:6px;")]
        for k, (p, bd) in enumerate(pos):
            i, la, lb = self.clip("corner", a, b, "", p + bd, " data-layout-ignore")
            self.js.append(f'tl.fromTo("#{i}", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, {la + k * 0.18});')
            self.js.append(f'tl.to("#{i}", {{ opacity: 0, duration: 0.2 }}, {round(lb - 0.21, 3)});')
    def write(self):
        js = "\n    ".join(self.js)
        open(os.path.join(P, f"compositions/{self.cid}.html"), "w").write(f'''<template>
  <style>
{KIT}
  </style>
  <div id="root" data-composition-id="{self.cid}" data-width="1080" data-height="1920">
{chr(10).join(self.body)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {js}
    window.__timelines["{self.cid}"] = tl;
  </script>
</template>
''')
        return (self.cid, self.t0, round(self.t1 - self.t0, 3))

SCENES = []
# ---------------- HOOK + BABAK 1 (0 – 66.15) ----------------
s = Scene("bab1", 0, 66.15)
s.paper(0.05, 3.5, "catatan · hari ke-7", "bau macam-macam.")
s.paper(3.6, 4.75, "", "13 tahun tak diguna", rot=1.2)
s.stamp(4.8, 9.8, "BILIK MAYAT", left=250, top=270, size=88, rot=-5)
s.chapter(9.86, 11.2, "BAB 1", "kenapa kami sanggup")
s.paper(11.25, 14.4, "", "aku + 2 kawan", rot=1)
s.paper(14.46, 17.05, "masa tu", "pelajar tahun akhir")
s.checklist(17.11, 25.5, "cari duit tambahan untuk:", [("bayar motor", 22.6, None), ("duit makan", 25.0, None)])
s.big(25.56, 29.5, "bukan dari keluarga yang mampu.", size=64)
s.tint(29.55, 38.7, "radial-gradient(ellipse at 50% 35%, rgba(14,23,38,0) 30%, rgba(14,23,38,.55) 100%)")
s.paper(34.71, 35.7, "", "malam jumaat")
s.paper(35.75, 38.7, "pengerusi surau", "kami panggil “cikgu”", rot=1)
s.rain(40.0, 51.7)
s.paper(38.8, 46.9, "setiap kali hujan", "subuh · zohor · asar · maghrib · isyak", rot=-1)
s.stamp(47.25, 48.8, "BASAH KUYUP", left=230, top=280, size=72, rot=4)
s.paper(48.85, 51.7, "", "tak mampu beli baju hujan.", rot=-1)
s.stamp(54.2, 56.0, "ELAUN DIPOTONG", left=150, top=280, size=70, rot=-5)
s.paper(56.05, 57.15, "", "tugas: imam surau", rot=1)
s.paper(59.44, 63.6, "cikgu", "“boleh sediakan bilik…”", rot=-1)
s.paper(63.65, 66.1, "", "“sanggup ke tak?”", rot=1.5)
SCENES.append(s.write())

# ---------------- BABAK 2 (66.15 – 154.91) ----------------
s = Scene("bab2", 66.15, 154.91)
s.chapter(66.15, 67.55, "BAB 2", "bilik di belakang surau")
s.tint(67.55, 86.8, "radial-gradient(ellipse at 50% 38%, rgba(14,23,38,0) 25%, rgba(5,8,14,.6) 100%)")
s.paper(69.7, 71.6, "", "ada satu bilik…", rot=-1)
s.stamp(72.7, 75.6, "BILIK MAYAT?!", left=200, top=270, size=90, rot=-4)
s.paper(Src(167.3), Src(172.1), "", "baru 3 kali diguna", rot=1)
s.paper(Src(178.1), Src(189.2), "cikgu", "barang dalam bilik pun jarang diguna", rot=-1)
s.paper(77.5, 79.8, "", "hampir 13 tahun kosong", rot=-1)
s.paper(Src(209.3), Src(219.0), "selama ni mayat", "dimandikan di masjid sri putra", rot=1)
s.shot(Src(207.3), Src(209.25), "assets/img/meja-mandi.jpg", "untuk mandikan mayat")
s.big(82.2, 86.75, "pandang atas bawah… fikir.", size=70)
s.paper(87.6, 89.9, "kawan aku", "“min, tak ada pilihan.”", rot=1)
s.paper(89.95, 94.8, "kalau tak ambil", "elaun kurang = komitmen tak terbayar", rot=-1)
s.paper(94.9, 100.2, "hujung minggu", "kemas bilik", rot=1)
s.paper(100.29, 102.5, "", "jemaah datang tolong", rot=-1)
s.checklist(102.56, 124.6, "buang “vibe” bilik mayat:", [("paip mandi mayat", 105.4, 112.42), ("lorong air mandi mayat", 115.68, 118.74), ("apa-apa yang nampak macam bilik mayat", 121.3, 124.31)])
s.paper(127.0, 132.6, "kawan aku", "“ayah kau buat perubatan islam kan?”", rot=1)
s.paper(137.6, 142.05, "untuk", "pagar bilik · halau benda halus", rot=-1)
s.paper(Src(342.3), Src(351.0), "kau pakar perubatan islam?", "share kat komen", rot=-1)
s.paper(145.07, 148.5, "bahan", "daun bidara", rot=1)
s.paper(148.56, 153.7, "baca pada air daun", "yasin · ayat 1–9", rot=-1)
s.corners(153.72, 154.9)
SCENES.append(s.write())

# ---------------- BABAK 3 (154.91 – 212.74) ----------------
s = Scene("bab3", 154.91, 212.74)
s.chapter(154.91, 156.3, "BAB 3", "30 hari pertama")
s.paper(157.8, 160.3, "hari 1–7", "bau.", rot=-1)
s.paper(160.34, 162.6, "", "nyamuk? takde.", rot=1)
s.paper(162.67, 167.4, "", "bilik dah kedap", rot=-1)
s.shot(168.8, 173.6, "assets/img/sulfur-ular.jpg", "sulfur keliling bilik — halau ular", rot=2)
s.paper(173.66, 178.2, "", "cara tradisional + perubatan islam", rot=1)
s.big(179.4, 183.85, "makhluk halus… tak boleh elak.", size=66)
s.tint(178.2, 212.7, "radial-gradient(ellipse at 50% 38%, rgba(14,23,38,0) 22%, rgba(3,5,10,.68) 100%)")
s.big(183.92, 185.4, "hari 7", size=110, color="#F3A93C")
s.big(185.45, 186.4, "hari 14", size=110, color="#F3A93C")
s.big(186.42, 189.7, "hari 30", size=110, color="#F3A93C")
s.paper(189.78, 193.8, "", "bau pelik.", rot=-1)
s.paper(193.9, 195.5, "", "pagi-pagi…", rot=1)
s.paper(195.57, 197.45, "", "azim (bukan nama sebenar)", rot=-1)
s.big(197.6, 199.8, "“ada bau pelik tak?”", size=74)
s.paper(201.3, 206.85, "kawan aku", "“dia dah lama duduk sini.”", rot=1)
s.big(207.2, 212.7, "“kalau dia usik kaki kita… lalu je lah.”", size=58)
SCENES.append(s.write())

# ---------------- PESAN (212.74 – 274.52) ----------------
s = Scene("pesan", 212.74, 274.52)
s.chapter(212.74, 214.0, "PESAN", "apa aku belajar", warm=True)
s.paper(214.05, 218.5, "nasihat orang perubatan islam", "masuk tempat baru?", rot=-1)
s.paper(218.55, 227.7, "7 hari berturut-turut", "baca al-baqarah penuh", rot=1)
s.paper(227.72, 232.9, "", "jangan pernah miss", rot=-1)
s.paper(232.95, 238.8, "dalam bilik tu", "quran · solat · amalan", rot=1)
s.paper(238.89, 242.0, "", "biar dia keluar sikit-sikit", rot=-1)
s.big(242.1, 244.65, "kepada kau…", size=80, color="#F3A93C")
s.paper(244.71, 250.9, "", "yang tengah struggle", rot=1)
s.paper(250.97, 257.5, "", "“kerja ni tak kena dengan sijil…”", rot=-1)
s.paper(257.53, 260.95, "", "apa peluang yang ada?", rot=1)
s.paper(261.0, 265.55, "boleh bayar komitmen", "walaupun sikit-sikit", rot=-1)
s.paper(265.6, 272.5, "", "tak ganggu kerja & keluarga?", rot=1)
s.big(272.6, 274.5, "better ambil.", size=110, color="#F3A93C")
SCENES.append(s.write())

# ---------------- CTA + END (274.52 – 285.2) ----------------
s = Scene("cta", 274.52, 285.28)
s.paper(277.5, 282.78, "komen kat bawah", "apa kau belajar dari kisah ni?", rot=-1)
s.chapter(282.8, 285.28, "SAVE VIDEO NI", "bila kau tengah struggle, tengok balik.", warm=True)
SCENES.append(s.write())

open("scenes.json", "w").write(__import__("json").dumps(SCENES))
print("scenes:", SCENES)
