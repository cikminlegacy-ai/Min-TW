#!/usr/bin/env python3
"""Emit CONS1 scene files (kit CSS inlined into each <template>)."""
import os, sys
P = sys.argv[1] if len(sys.argv) > 1 else "."
KIT = open(os.path.join(P, "kit.css")).read()

def scene(cid, css, body, js):
    doc = f'''<template>
  <style>
{KIT}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''
    open(os.path.join(P, f"compositions/{cid}.html"), "w").write(doc)

WHIP_IN = 'tl.fromTo("{s}", {{ x: 260, filter: "blur(18px)" }}, {{ x: 0, filter: "blur(0px)", duration: 0.28, ease: "power3.out" }}, {t});'
def whip(sel, t): return "    " + WHIP_IN.format(s=sel, t=t)
def stamp_in(sel, t, rot=-6):
    return f'    tl.fromTo("{sel}", {{ opacity: 0, scale: 2.4, rotation: {rot*3} }}, {{ opacity: 1, scale: 1, rotation: {rot}, duration: 0.24, ease: "expo.out" }}, {t});'
def pop_in(sel, t):
    return f'    tl.fromTo("{sel}", {{ opacity: 0, scale: 0.4, y: 30 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.32, ease: "back.out(2.2)" }}, {t});'
def out(sel, t):
    return f'    tl.to("{sel}", {{ opacity: 0, scale: 0.85, filter: "blur(6px)", duration: 0.16, ease: "power3.in" }}, {t});'

# 1 HOOK — order ticket above the head
scene("hook", '''
    #hk-t { left:110px; width:820px; top:236px; text-align:center; opacity:0; }
    #hk-t .lab { font-size:30px; color:#E23B2E; }
    #hk-t .h1 { font-family:"Archivo Black", sans-serif; font-size:104px; line-height:.95; color:#E23B2E; letter-spacing:-.01em; }
    #hk-t .h2 { font-size:44px; color:#17140F; }
''', '''
    <div id="hk-t" class="ticket clip" data-start="0" data-duration="3.02">
      <div class="lab mono">ORDER #01 · PASAR PAGI</div>
      <div class="rule"></div>
      <div class="h1">MAKCIK<br/>NASI LEMAK</div>
      <div class="rule"></div>
      <div class="h2 mono">BANGUN 3:00 PAGI?</div>
    </div>''', '''
    tl.fromTo("#hk-t", { opacity: 0, y: -420, rotation: -14 }, { opacity: 1, y: 0, rotation: -3, duration: 0.34, ease: "back.out(1.6)" }, 0.04);
    tl.to("#hk-t", { keyframes: { rotation: [-3, -5, -2, -3] }, duration: 0.3, ease: "none" }, 0.38);
    tl.to("#hk-t", { x: -1200, filter: "blur(16px)", duration: 0.22, ease: "power3.in" }, 2.8);''')

# 2 JAM — clock, 3:00
scene("jam", '''
    #jm-num { left:0; right:140px; top:470px; text-align:center; position:absolute; opacity:0;
      font-family:"Archivo Black", sans-serif; font-size:270px; color:#FFF3DC; line-height:1; text-shadow:0 14px 50px rgba(0,0,0,.6); }
    #jm-pagi { left:330px; top:770px; background:#E23B2E; color:#FFF3DC; font-size:72px; opacity:0; }
''', '''
    <video id="jm-v" class="full clip" data-start="0" data-duration="2.31" data-media-start="6" src="assets/broll/clock.mp4" muted playsinline></video>
    <div class="shade clip" data-start="0" data-duration="2.31"></div>
    <div id="jm-num" class="clip" data-start="0" data-duration="2.31">3:00</div>
    <div id="jm-pagi" class="pill clip" data-start="0" data-duration="2.31">PAGI!</div>''',
whip("#jm-v", 0) + '\n' +
'''    tl.fromTo("#jm-v", { scale: 1.3 }, { scale: 1.08, duration: 2.31, ease: "power1.out" }, 0);
    tl.fromTo("#jm-num", { opacity: 0, scale: 1.6, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.22, ease: "expo.out" }, 0.12);
''' + pop_in("#jm-pagi", 1.2))

# 3 MASAK — 4-shot montage with stamps
shots = [("rice", 0.0, 1.03, "MASAK NASI", 0), ("sambal", 1.03, 1.04, "MASAK SAMBAL", 1), ("egg", 2.07, 1.22, "GORENG TELUR", 0), ("cucumber", 3.29, 1.27, "POTONG TIMUN", 0)]
body, js = [], []
for i, (v, s, d, lab, ms) in enumerate(shots):
    body.append(f'    <video id="ms-v{i}" class="full clip" data-start="{s}" data-duration="{d}" data-media-start="{ms}" src="assets/broll/{v}.mp4" muted playsinline></video>')
    body.append(f'    <div id="ms-s{i}" class="stamp clip" data-start="{s}" data-duration="{d}" style="left:{100 if i%2==0 else 150}px; top:{300 if i%2==0 else 340}px; font-size:76px;">{lab}</div>')
    body.append(f'    <div id="ms-n{i}" class="pill mono clip" data-start="{s}" data-duration="{d}" style="left:90px; top:1040px; background:#17140F; color:#FFB547; font-size:34px;">0{i+1} / 04</div>')
    js.append(whip(f"#ms-v{i}", s))
    js.append(stamp_in(f"#ms-s{i}", s + 0.08, -5 if i % 2 == 0 else 4))
scene("masak", '', "\n".join(body), "\n".join(js))

# 4 PENAT
scene("penat", '''
    #pn-s { left:180px; top:420px; font-size:150px; opacity:0; }
''', '''
    <video id="pn-v" class="full clip" data-start="0" data-duration="1.22" data-media-start="3" src="assets/broll/tired.mp4" muted playsinline></video>
    <div class="shade clip" data-start="0" data-duration="1.22"></div>
    <div id="pn-s" class="stamp clip" data-start="0" data-duration="1.22">PENAT!</div>''',
whip("#pn-v", 0) + '\n' + stamp_in("#pn-s", 0.06, -8) +
'\n    tl.to("#pn-s", { keyframes: { x: [0, -12, 10, -6, 0] }, duration: 0.25, ease: "none" }, 0.3);')

# 5 CEDUK — polaroid stack on pandan ground
scene("ceduk", '''
    #cd-p1 { left:90px; top:380px; width:840px; height:560px; opacity:0; }
    #cd-p2 { left:110px; top:560px; width:840px; height:560px; opacity:0; }
    #cd-sen { z-index:5; left:400px; top:236px; background:#FFB547; color:#17140F; font-family:"Archivo Black", sans-serif; font-size:66px; opacity:0; }
''', '''
    <div id="cd-ground" class="ground clip" data-start="0" data-duration="2.72"></div>
    <div id="cd-p1" class="pol"><div class="ph"><video id="cd-v1" class="clip" data-start="0" data-duration="2.72" data-media-start="2" src="assets/broll/stall.mp4" muted playsinline></video></div><div class="cap">LAUK DAH SIAP</div></div>
    <div id="cd-p2" class="pol"><div class="ph"><video id="cd-v2" class="clip" data-start="0.94" data-duration="1.78" data-media-start="0.5" src="assets/broll/scoop.mp4" muted playsinline></video></div><div class="cap">TINGGAL CEDOK JE</div></div>
    <div id="cd-sen" data-layout-allow-occlusion class="pill clip" data-start="2.1" data-duration="0.6">SENANG KAN?</div>''', '''
    tl.fromTo("#cd-p1", { opacity: 0, y: 500, rotation: 10 }, { opacity: 1, y: 0, rotation: -4, duration: 0.4, ease: "expo.out" }, 0.0);
    tl.fromTo("#cd-p2", { opacity: 0, x: 900, rotation: 14 }, { opacity: 1, x: 0, rotation: 3, duration: 0.36, ease: "expo.out" }, 0.94);
    tl.fromTo("#cd-sen", { opacity: 0, scale: 0.3, rotation: -20 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.3, ease: "back.out(2.6)" }, 2.14);''')

# 6 TOOLS — chili colour flood + 9 TOOLS
scene("tools", '''
    #tl-flood { position:absolute; inset:0; background:#E23B2E; transform-origin:50% 100%; }
    #tl-9 { position:absolute; left:0; right:140px; top:250px; text-align:center; font-family:"Archivo Black", sans-serif; font-size:560px; line-height:1; color:#FFF3DC; opacity:0;
      text-shadow:0 20px 0 rgba(23,20,15,.25); }
    #tl-w { position:absolute; left:0; right:140px; top:800px; text-align:center; font-family:"Archivo Black", sans-serif; font-size:170px; line-height:1; color:#17140F; opacity:0; }
    #tl-sub { left:250px; top:1010px; background:#17140F; color:#FFB547; font-size:36px; opacity:0; }
''', '''
    <div id="tl-flood" class="clip" data-start="0" data-duration="1.71"></div>
    <div id="tl-9" class="clip" data-start="0" data-duration="1.71">9</div>
    <div id="tl-w" class="clip" data-start="0" data-duration="1.71">TOOLS</div>
    <div id="tl-sub" class="pill mono clip" data-start="0" data-duration="1.71">UNTUK TEAM SAYA</div>''', '''
    tl.fromTo("#tl-flood", { scaleY: 0 }, { scaleY: 1, duration: 0.24, ease: "power2.inOut" }, 0);
    tl.fromTo("#tl-9", { opacity: 0, scale: 2.2, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "expo.out" }, 0.16);
    tl.fromTo("#tl-w", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out" }, 0.38);''' + '\n' + pop_in("#tl-sub", 0.6))

# 7 MENU — split: face panel top, 9-tools board below
items = ["KONTEN SIAP", "BLUEPRINT 31K", "40 HARI STORY", "40 HARI WALL POST", "HANDLE REJECTION", "Q&amp;A", "TESTIMONI", "LIVE", "POSTER"]
ticks = [0.05, 1.08, 2.75, 4.6, 6.83, 7.96]
rows = "\n".join(f'        <div class="it" id="mn-i{i}"><span class="tick" id="mn-k{i}">✓</span><span class="tx">{t}</span></div>' for i, t in enumerate(items))
js = ['''    tl.fromTo("#mn-board", { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 0.34, ease: "expo.out" }, 0);
    tl.fromTo("#mn-cam", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0);
    tl.set(["#mn-k6", "#mn-k7", "#mn-k8"], { scale: 0 }, 0);''']
for i, t in enumerate(ticks):
    js.append(f'    tl.fromTo("#mn-k{i}", {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.25, ease: "back.out(3)" }}, {t});')
    js.append(f'    tl.fromTo("#mn-i{i} .tx", {{ color: "#9a9182" }}, {{ color: "#17140F", duration: 0.12 }}, {t});')
    js.append(f'    tl.set("#mn-cnt", {{ textContent: "{i+1}/9" }}, {t});' if False else '')
scene("menu", '''
    #mn-bg { position:absolute; inset:0; background:#1E7A46; }
    #mn-cam { position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:hidden; clip-path: inset(0 0 1150px 0 round 0 0 40px 40px); }
    #mn-cam video { position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; transform-origin:430px 690px; }
    #mn-board { position:absolute; left:60px; width:880px; top:790px; height:375px; background:#FFF3DC; border-radius:26px; padding:22px 30px; opacity:0;
      box-shadow:0 20px 60px rgba(0,0,0,.45); }
    #mn-head { display:flex; justify-content:space-between; align-items:center; font-family:"Archivo Black", sans-serif; font-size:40px; color:#E23B2E; }
    #mn-head .mono { font-size:28px; color:#17140F; }
    #mn-grid { display:grid; grid-template-columns: 1fr 1fr; grid-auto-flow: column; grid-template-rows: repeat(5, 54px); column-gap:24px; margin-top:12px; }
    #mn-grid .it { display:flex; align-items:center; gap:12px; font-weight:800; font-size:27px; color:#9a9182; }
    #mn-grid .tick { width:40px; height:40px; font-size:24px; flex:none; }
''', f'''
    <div id="mn-bg" class="clip" data-start="0" data-duration="8.7"></div>
    <div id="mn-cam"><video id="mn-talk" class="clip" data-start="0" data-duration="8.7" data-media-start="21.01" src="assets/video/talk.mp4" muted playsinline style="transform: translate(-20px, -110px) scale(1.42);"></video></div>
    <div id="mn-board">
      <div id="mn-head"><span>MENU · 9 TOOLS</span><span class="mono">DAH SIAP ✓</span></div>
      <div id="mn-grid">
{rows}
      </div>
    </div>''', "\n".join(j for j in js if j))

# 8 TESTI
scene("testi", '''
    #ts-s { left:200px; top:360px; font-size:96px; opacity:0; }
''', '''
    <video id="ts-v" class="full clip" data-start="0" data-duration="1.5" data-media-start="4" src="assets/broll/clap.mp4" muted playsinline></video>
    <div class="shade clip" data-start="0" data-duration="1.5"></div>
    <div id="ts-s" class="stamp clip" data-start="0" data-duration="1.5">TESTIMONI ✓</div>''',
whip("#ts-v", 0) + '\n' + stamp_in("#ts-s", 0.2, -5))

# 9 TAK NIAGA — chips above the head
scene("taknia", '''
    #tn-a, #tn-b { left:120px; width:800px; top:250px; text-align:center; opacity:0; }
    #tn-a .m, #tn-b .m { font-size:28px; color:#E23B2E; }
    #tn-a .h, #tn-b .h { font-family:"Archivo Black", sans-serif; font-size:66px; line-height:1.05; }
''', '''
    <div id="tn-a" class="ticket clip" data-start="0.85" data-duration="1.7"><div class="m mono">SAHABAT SAYA</div><div class="h">TAK PERNAH BERNIAGA</div></div>
    <div id="tn-b" class="ticket clip" data-start="2.5" data-duration="2.47"><div class="m mono">BUKAN DARI</div><div class="h">KETURUNAN PENIAGA</div></div>''',
'''    tl.fromTo("#tn-a", { opacity: 0, y: -200, rotation: 6 }, { opacity: 1, y: 0, rotation: 2, duration: 0.32, ease: "back.out(1.7)" }, 0.88);
    tl.to("#tn-a", { x: -1100, filter: "blur(14px)", duration: 0.2, ease: "power3.in" }, 2.32);
    tl.fromTo("#tn-b", { opacity: 0, x: 1100, rotation: -6 }, { opacity: 1, x: 0, rotation: -2, duration: 0.3, ease: "expo.out" }, 2.52);
''' + out("#tn-b", 4.78))

# 10 JAWAPAN
scene("jawapan", '''
    #jw-t { left:140px; width:760px; top:520px; text-align:center; opacity:0; }
    #jw-t .m { font-size:30px; color:#E23B2E; }
    #jw-t .h { font-family:"Archivo Black", sans-serif; font-size:96px; line-height:1; }
''', '''
    <video id="jw-v" class="full clip" data-start="0" data-duration="2.3" data-media-start="2" src="assets/broll/question.mp4" muted playsinline></video>
    <div id="jw-t" class="ticket clip" data-start="0.6" data-duration="1.7"><div class="m mono">ORANG TANYA?</div><div class="rule"></div><div class="h">JAWAPAN<br/>DAH ADA <span class="tick" style="width:80px;height:80px;font-size:52px;vertical-align:middle">✓</span></div></div>''',
whip("#jw-v", 0) + '\n' + pop_in("#jw-t", 0.62))

# 11 SENJATA — boxing, live, poster, full board all ticked
rows_all = "\n".join(f'        <div class="it"><span class="tick">✓</span><span class="tx">{t}</span></div>' for t in items)
scene("senjata", '''
    #sj-s1 { left:150px; top:360px; font-size:92px; opacity:0; }
    #sj-s2 { left:220px; top:360px; font-size:92px; opacity:0; }
    #sj-s3 { left:200px; top:360px; font-size:92px; opacity:0; }
    #sj-bg { position:absolute; inset:0; background:#1E7A46; }
    #sj-board { position:absolute; left:60px; width:880px; top:240px; background:#FFF3DC; border-radius:26px; padding:34px 40px; opacity:0; box-shadow:0 20px 60px rgba(0,0,0,.45); }
    #sj-board .hd { font-family:"Archivo Black", sans-serif; font-size:56px; color:#E23B2E; }
    #sj-board .it { display:flex; align-items:center; gap:18px; font-weight:800; font-size:44px; color:#17140F; height:76px; }
    #sj-big { left:150px; top:640px; font-size:118px; opacity:0; }
''', f'''
    <video id="sj-v1" class="full clip" data-start="0" data-duration="1.04" data-media-start="3" src="assets/broll/boxing.mp4" muted playsinline></video>
    <div id="sj-s1" class="stamp clip" data-start="0" data-duration="1.04">SENJATA SIAP</div>
    <video id="sj-v2" class="full clip" data-start="1.04" data-duration="0.75" data-media-start="2" src="assets/broll/live.mp4" muted playsinline></video>
    <div id="sj-s2" class="stamp clip" data-start="1.04" data-duration="0.75">LIVE ✓</div>
    <video id="sj-v3" class="full clip" data-start="1.79" data-duration="0.85" data-media-start="1" src="assets/broll/megaphone.mp4" muted playsinline></video>
    <div id="sj-s3" class="stamp clip" data-start="1.79" data-duration="0.85">POSTER ✓</div>
    <div id="sj-bg" class="clip" data-start="2.64" data-duration="1.23"></div>
    <div id="sj-board" class="clip" data-start="2.64" data-duration="1.23">
      <div class="hd">9/9 TOOLS</div>
{rows_all}
    </div>
    <div id="sj-big" data-layout-allow-overlap class="stamp clip" data-start="3.15" data-duration="0.72">SEMUA DAH ADA</div>''',
"\n".join([whip("#sj-v1", 0), stamp_in("#sj-s1", 0.05, -5), whip("#sj-v2", 1.04), stamp_in("#sj-s2", 1.08, 5), whip("#sj-v3", 1.79), stamp_in("#sj-s3", 1.83, -4),
 '    tl.fromTo("#sj-board", { opacity: 0, y: 400, rotation: 4 }, { opacity: 1, y: 0, rotation: -1, duration: 0.34, ease: "expo.out" }, 2.64);',
 stamp_in("#sj-big", 3.18, -8)]))

# 12 JALAN
scene("jalan", '''
    #jl-a { left:170px; width:700px; top:260px; text-align:center; opacity:0; }
    #jl-a .m { font-size:28px; color:#E23B2E; } #jl-a .h { font-family:"Archivo Black", sans-serif; font-size:72px; line-height:1.05; }
    #jl-go { left:240px; top:300px; background:#1E7A46; color:#FFF3DC; font-family:"Archivo Black", sans-serif; font-size:80px; opacity:0; }
''', '''
    <div id="jl-a" class="ticket clip" data-start="0.55" data-duration="1.85"><div class="m mono">SEBAB TU</div><div class="h">TEAM BARU JOIN</div></div>
    <div id="jl-go" class="pill clip" data-start="2.44" data-duration="1.32">TERUS JALAN →</div>''',
pop_in("#jl-a", 0.6) + '\n' + out("#jl-a", 2.24) +
'\n    tl.fromTo("#jl-go", { opacity: 0, x: -700 }, { opacity: 1, x: 0, duration: 0.3, ease: "expo.out" }, 2.46);\n    tl.to("#jl-go", { x: 900, filter: "blur(14px)", duration: 0.2, ease: "power3.in" }, 3.56);')

# 13 SOLO — alone + search typing
scene("solo", '''
    #so-s { left:80px; top:360px; font-size:68px; opacity:0; }
    #so-bar { position:absolute; left:80px; width:840px; top:330px; height:110px; background:#fff; border-radius:60px; display:flex; align-items:center; gap:22px; padding:0 34px;
      box-shadow:0 20px 50px rgba(0,0,0,.45); opacity:0; }
    #so-ico { width:46px; height:46px; border:7px solid #17140F; border-radius:50%; position:relative; flex:none; }
    #so-ico::after { content:""; position:absolute; width:8px; height:26px; background:#17140F; right:-14px; bottom:-20px; transform:rotate(-45deg); border-radius:4px; }
    #so-tx { font-weight:700; font-size:44px; color:#17140F; white-space:nowrap; overflow:hidden; }
    #so-cnt { left:330px; top:500px; background:#E23B2E; color:#FFF3DC; font-family:"Archivo Black", sans-serif; font-size:60px; opacity:0; }
''', '''
    <video id="so-v1" class="full clip" data-start="0" data-duration="2.3" data-media-start="3" src="assets/broll/alone.mp4" muted playsinline></video>
    <div class="shade clip" data-start="0" data-duration="2.3"></div>
    <div id="so-s" class="stamp clip" data-start="0" data-duration="2.3">SORANG-SORANG?</div>
    <video id="so-v2" class="full clip" data-start="2.3" data-duration="2.53" data-media-start="1" src="assets/broll/laptop.mp4" muted playsinline></video>
    <div class="shade clip" data-start="2.3" data-duration="2.53"></div>
    <div id="so-bar" class="clip" data-start="2.3" data-duration="2.53"><div id="so-ico"></div><div id="so-tx">|</div></div>
    <div id="so-cnt" class="pill clip" data-start="3.3" data-duration="1.53">0/9 TOOLS</div>''',
"\n".join([whip("#so-v1", 0), stamp_in("#so-s", 0.12, -5), whip("#so-v2", 2.3),
 pop_in("#so-bar", 2.34),
 '''    const ty = { n: 0 }; const full = "cari tools satu-satu...";
    tl.fromTo(ty, { n: 0 }, { n: full.length, duration: 1.4, ease: "none",
      onUpdate: () => { document.querySelector("#so-tx").textContent = full.slice(0, Math.round(ty.n)) + "|"; } }, 2.4);''',
 pop_in("#so-cnt", 3.32)]))

# 14 PENAT2 — callback ticket above the head
scene("penat2", '''
    #p2-t { left:150px; width:740px; top:240px; text-align:center; opacity:0; }
    #p2-t .m { font-size:28px; color:#E23B2E; } #p2-t .h { font-family:"Archivo Black", sans-serif; font-size:50px; white-space:nowrap; line-height:1; color:#E23B2E; }
    #p2-s { left:590px; top:420px; font-size:60px; opacity:0; }
''', '''
    <div id="p2-t" class="ticket clip" data-start="0.05" data-duration="2.47"><div class="m mono">ORDER #01 · TADI</div><div class="h">MAKCIK NASI LEMAK</div></div>
    <div id="p2-s" class="stamp clip" data-start="0.9" data-duration="1.62">PENAT!</div>''',
'    tl.fromTo("#p2-t", { opacity: 0, y: -300, rotation: -10 }, { opacity: 1, y: 0, rotation: -3, duration: 0.32, ease: "back.out(1.6)" }, 0.06);\n' + stamp_in("#p2-s", 0.95, 8) + '\n' + out("#p2-t", 2.34) + '\n' + out("#p2-s", 2.34))

# 15 SIAP
scene("siap", '''
    #sp-c { left:120px; top:290px; background:#1E7A46; color:#FFF3DC; font-family:"Archivo Black", sans-serif; font-size:70px; opacity:0; }
''', '''
    <div id="sp-c" class="pill clip" data-start="1.15" data-duration="1.98">9/9 TOOLS ✓ SIAP</div>''',
pop_in("#sp-c", 1.18) + '\n' + out("#sp-c", 2.95))

# 16 CTA — comment bubble + follow card
scene("cta", '''
    #ct-b { position:absolute; left:80px; width:820px; top:236px; background:#fff; border-radius:28px; padding:22px 28px; display:flex; gap:22px; align-items:center;
      box-shadow:0 20px 50px rgba(0,0,0,.45); opacity:0; }
    #ct-av { width:96px; height:96px; border-radius:50%; background:#FFB547; color:#17140F; font-family:"Archivo Black", sans-serif; font-size:50px; display:flex; align-items:center; justify-content:center; flex:none; }
    #ct-b .nm { font-size:30px; color:#7a746a; font-weight:700; }
    #ct-b .tx { font-family:"Archivo Black", sans-serif; font-size:96px; line-height:1; color:#E23B2E; }
    #ct-f { position:absolute; left:150px; width:620px; top:470px; height:150px; background:#fff; border-radius:24px; overflow:hidden; opacity:0;
      box-shadow:0 20px 50px rgba(0,0,0,.45); }
    #ct-img { position:absolute; left:-40px; top:-10px; width:908px; height:223px; transform: scale(0.75); transform-origin:0 0; }
    #ct-fb { position:absolute; left:368px; top:4px; width:230px; text-align:center; background:#E23B2E; color:#fff; font-weight:800; font-size:36px; border-radius:16px; padding:10px 22px; }
''', '''
    <div id="ct-b" class="clip" data-start="0.03" data-duration="2.98"><div id="ct-av">A</div><div><div class="nm">abang_akak · baru je</div><div class="tx">SENANG</div></div></div>
    <div id="ct-f" class="clip" data-start="0.88" data-duration="2.13"><img id="ct-img" src="assets/img/follow.png" alt="CikMin @cikmin9508" /><div id="ct-fb">+ Follow</div></div>''',
'''    tl.fromTo("#ct-b", { opacity: 0, y: -60, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.34, ease: "back.out(2)" }, 0.04);
    tl.fromTo("#ct-b .tx", { scale: 1.4 }, { scale: 1, duration: 0.3, ease: "expo.out" }, 0.2);
    tl.fromTo("#ct-f", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, 0.9);
    tl.fromTo("#ct-fb", { scale: 1 }, { scale: 1.12, duration: 0.14, yoyo: true, repeat: 1, ease: "power2.out" }, 1.6);''')
print("scenes written")
