#!/usr/bin/env python3
"""Emit SERAM1 scene files (kit.css inlined into each <template>). Run from the project dir."""
import os, sys
P = sys.argv[1] if len(sys.argv) > 1 else "."
KIT = open(os.path.join(P, "kit.css")).read()

def scene(cid, css, body, js):
    open(os.path.join(P, f"compositions/{cid}.html"), "w").write(f'''<template>
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
''')

def flicker(sel, t):
    """light flicker: dip to black for a few frames, twice"""
    return (f'    tl.fromTo("{sel}", {{ opacity: 0 }}, {{ keyframes: {{ opacity: [0, 0.92, 0.15, 0.85, 0] }}, duration: 0.26, ease: "none" }}, {t});')

def letters(text, cls_id):
    return "".join(f'<span class="{cls_id}">{c if c != " " else "&nbsp;"}</span>' for c in text)

# 1 HOOK (0–3.65): flicker, kicker, BILIK MAYAT letter by letter, 13 TAHUN
scene("hook", '''
    #hk-k { top:228px; font-size:32px; }
    #hk-t { top:262px; font-size:100px; letter-spacing:.03em; white-space:nowrap; }
    #hk-t .L { display:inline-block; opacity:0; }
    #hk-y { top:222px; font-size:32px; font-family:"Cinzel", serif; font-weight:700; letter-spacing:.2em; }
    #hk-l1 { left:250px; width:580px; top:374px; }
''', f'''
    <div id="hk-k" class="kick clip" data-start="0" data-duration="2.74">AKU PERNAH TIDUR DI</div>
    <div id="hk-t" class="ttl clip" data-start="1.8" data-duration="1.85" style="opacity:1">{letters("BILIK MAYAT", "L")}</div>
    <div id="hk-l1" class="line clip" data-start="1.8" data-duration="1.85"></div>
    <div id="hk-y" class="kick rust clip" data-start="2.74" data-duration="0.91">13 TAHUN TAK DIGUNA</div>
    <div id="hk-fl" class="black clip" data-start="0" data-duration="0.3" data-layout-ignore></div>''', '''
''' + flicker("#hk-fl", 0) + '''
    tl.fromTo("#hk-k", { opacity: 0, scaleX: 1.25 }, { opacity: 1, scaleX: 1, duration: 0.5, ease: "power3.out" }, 0.08);
    tl.fromTo("#hk-t .L", { opacity: 0, y: 14, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.16, ease: "power2.out", stagger: 0.045 }, 1.82);
    tl.fromTo("#hk-l1", { opacity: 0, scaleX: 0 }, { opacity: 0.8, scaleX: 1, duration: 0.4, ease: "power3.out" }, 2.2);
    tl.to("#hk-k", { opacity: 0, duration: 0.12 }, 2.62);
    tl.fromTo("#hk-y", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.2, ease: "power3.out" }, 2.78);
    tl.to(["#hk-t", "#hk-l1", "#hk-y"], { opacity: 0, filter: "blur(6px)", duration: 0.18, ease: "power2.in" }, 3.45);''')

# 2 SURAU (3.65–4.81): zoom out, small label
scene("surau", '''
    #su-t { top:250px; font-size:64px; font-weight:700; letter-spacing:.12em; }
''', '''
    <div id="su-t" class="ttl clip" data-start="0.2" data-duration="0.96">DI SURAU</div>
    <div id="su-fl" class="black clip" data-start="0" data-duration="0.12" data-layout-ignore></div>''',
flicker("#su-fl", 0).replace("0.26", "0.12") + '''
    tl.fromTo("#su-t", { opacity: 0, filter: "blur(10px)" }, { opacity: 0.95, filter: "blur(0px)", duration: 0.3, ease: "power2.out" }, 0.24);''')

# 3 EMOSI (4.81–7.87)
scene("emosi", '''
    #em-k { top:228px; font-size:30px; }
    #em-t { top:270px; font-size:100px; }
''', '''
    <div id="em-k" class="kick clip" data-start="0.2" data-duration="2.86">SEBUAH KISAH</div>
    <div id="em-t" class="ttl clip" data-start="2.2" data-duration="0.86">PENUH EMOSI</div>''', '''
    tl.fromTo("#em-k", { opacity: 0 }, { opacity: 0.85, duration: 0.6, ease: "power1.out" }, 0.25);
    tl.fromTo("#em-t", { opacity: 0, scale: 1.12, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: "power3.out" }, 2.24);''')

# 4 SERAM (7.87–8.93)
scene("seram", '''
    #sr-t { top:228px; font-size:150px; letter-spacing:.06em; color:#E0605C; z-index:2; }
    #sr-red { position:absolute; inset:0; background:radial-gradient(ellipse at 50% 50%, rgba(158,42,43,0) 40%, rgba(110,10,12,.55) 100%); opacity:0; }
''', '''
    <div id="sr-red" class="clip" data-start="0" data-duration="1.06" data-layout-ignore></div>
    <div id="sr-t" class="ttl rust clip" data-start="0.08" data-duration="0.98">SERAM</div>
    <div id="sr-fl" class="black clip" data-start="0" data-duration="0.26" data-layout-ignore></div>''',
flicker("#sr-fl", 0) + '''
    tl.fromTo("#sr-red", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, 0.05);
    tl.fromTo("#sr-t", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.14, ease: "expo.out" }, 0.1);
    tl.to("#sr-t", { keyframes: { x: [0, -6, 5, -4, 3, 0], y: [0, 3, -2, 2, -1, 0] }, duration: 0.5, ease: "none" }, 0.26);''')

# 5 INSPIRASI (8.93–10.12): gold light flood
scene("inspirasi", '''
    #in-glow { position:absolute; inset:0; background:radial-gradient(ellipse 900px 700px at 50% 20%, rgba(224,168,75,.55), rgba(224,168,75,0) 70%); mix-blend-mode:screen; opacity:0; }
    #in-k { top:228px; font-size:30px; color:#E0A84B; }
    #in-t { top:266px; font-size:108px; color:#E0A84B; text-shadow:0 0 40px rgba(224,168,75,.55), 0 0 80px rgba(0,0,0,.6); }
''', '''
    <div id="in-glow" class="clip" data-start="0" data-duration="1.19" data-layout-ignore></div>
    <div id="in-k" class="kick clip" data-start="0" data-duration="1.19">TAPI ADA</div>
    <div id="in-t" class="ttl clip" data-start="0.15" data-duration="1.04">INSPIRASI</div>''', '''
    tl.fromTo("#in-glow", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.inOut" }, 0.0);
    tl.fromTo("#in-k", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 0.02);
    tl.fromTo("#in-t", { opacity: 0, y: 24, filter: "blur(12px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }, 0.2);''')

# 6 NEXT (10.12–13.44)
scene("next", '''
    #nx-k { top:228px; font-size:30px; color:#E0A84B; }
    #nx-t { top:268px; font-size:92px; }
''', '''
    <div id="nx-k" class="kick clip" data-start="2.3" data-duration="1.02">KISAH PENUH</div>
    <div id="nx-t" class="ttl clip" data-start="2.4" data-duration="0.92">NEXT VIDEO</div>''', '''
    tl.fromTo("#nx-k", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 2.32);
    tl.fromTo("#nx-t", { opacity: 0, scaleX: 1.2, filter: "blur(8px)" }, { opacity: 1, scaleX: 1, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }, 2.42);''')

# 7 END CARD (13.44–16.4)
scene("end", '''
    #ed-bg { position:absolute; inset:0; z-index:0; background:radial-gradient(ellipse at 50% 45%, #1a1410 0%, #07080A 70%); }
    #ed-t { z-index:2; top:640px; font-size:104px; letter-spacing:.06em; }
    #ed-p { top:800px; font-size:50px; color:#E0A84B; font-family:"Cinzel", serif; font-weight:700; letter-spacing:.4em; }
    #ed-l { left:300px; width:480px; top:770px; background:#E0A84B; }
    #ed-f { position:absolute; left:350px; top:930px; padding:16px 40px 18px; border-radius:999px; background:#E9E4D8; color:#07080A;
      font-family:"Nunito", sans-serif; font-weight:900; font-size:46px; opacity:0; }
''', '''
    <div id="ed-bg" class="clip" data-start="0" data-duration="2.96"></div>
    <div id="ed-t" data-layout-allow-occlusion class="ttl clip" data-start="0.1" data-duration="2.86">BERSAMBUNG…</div>
    <div id="ed-l" class="line clip" data-start="0.1" data-duration="2.86"></div>
    <div id="ed-p" class="kick clip" data-start="0.5" data-duration="2.46">PART 2</div>
    <div id="ed-f" class="clip" data-start="0.9" data-duration="2.06">+ FOLLOW</div>''', '''
    tl.fromTo("#ed-bg", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.inOut" }, 0);
    tl.fromTo("#ed-t", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.5, ease: "power2.out" }, 0.12);
    tl.fromTo("#ed-l", { opacity: 0, scaleX: 0 }, { opacity: 0.9, scaleX: 1, duration: 0.5, ease: "power3.out" }, 0.35);
    tl.fromTo("#ed-p", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.55);
    tl.fromTo("#ed-f", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.32, ease: "back.out(2.2)" }, 0.92);''')
print("scenes written")
