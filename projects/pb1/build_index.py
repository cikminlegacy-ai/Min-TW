#!/usr/bin/env python3
"""Build PB1 index.html: camera, two graded talk clips (past/present), scene hosts, captions,
voice, 3 music cues with ducking lanes, ambience + story sounds + edit sounds.  Run: python3 build_index.py"""
import json
from timemap import M, Src   # SFX/cue times authored on the first cut → current cut
cuts = json.load(open("cuts.json")); SCENES = json.load(open("scenes.json"))
TALK_END = cuts["total"]; END = round(TALK_END + 2.48, 2); SPLIT = M(212.74)
holds = [(round(s["t"] + s["dur"], 3), round(s["t"] + s["dur"] + s["hold"], 3)) for s in cuts["segments"] if s.get("hold")]
cards = [(M(9.86), M(11.2)), (M(66.15), M(67.55)), (M(154.91), M(156.3)), (M(212.74), M(214.0)), (TALK_END, END)]
lifts = sorted(holds + cards)

# ---- camera: new framing every >=4 s on a cut (cinematic, funnel 4), slow push during holds
cycle = [1.08, 1.25, 1.0, 1.3, 1.15, 1.28, 1.12]; cam = []; last = -9; k = 0
# measured on this footage: hair top ~513, chin ~1052 (source px). Keep hair >= 400 (under the notes) and chin <= 1150 (above captions).
def cam_y(sc): return round(-8 - 60 * (sc - 1), 1)
for s in cuts["segments"]:
    if s["t"] - last >= 4.0:
        sc = cycle[k % len(cycle)]; k += 1; last = s["t"]
        cam.append((round(s["t"], 3), sc, cam_y(sc)))
cam_js = ", ".join(f"[{t}, {sc}, {y}]" for t, sc, y in cam)
def cam_at(t):
    cur = (1.22, cam_y(1.22))
    for ct, sc, y in cam:
        if ct <= t: cur = (sc, y)
    return cur
hold_js = ", ".join(f"[{a}, {b}, {round(cam_at(a)[0] + 0.05, 3)}, {cam_y(cam_at(a)[0] + 0.05)}]" for a, b in holds)

def lane(base, lift, fade_from=None):
    pts = [(0, base)]
    for a, b in lifts:
        pts += [(a, base), (a + 0.25, lift), (max(b - 0.25, a + 0.3), lift), (b, base)]
    pts = sorted(set(pts))
    j = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": round(t, 3), "v": v} for t, v in pts]}]})
    return j.replace('"', "&quot;")

def music(i, src, start, end, mstart, base, lift):
    # lane times are clip-local: shift lift windows into this clip
    pts = [(0, base)]
    for a, b in lifts:
        if start <= a <= end:
            la, lb = a - start, b - start
            pts += [(la, base), (la + 0.25, lift), (max(lb - 0.25, la + 0.3), lift), (lb, base)]
    j = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": round(t, 3), "v": v} for t, v in sorted(set(pts))]}]}).replace('"', "&quot;")
    return (f'      <audio id="{i}" class="clip" data-start="{start}" data-duration="{round(end - start, 3)}" data-media-start="{mstart}" '
            f'data-track-index="6" src="assets/music/{src}.mp3" data-volume="1" data-fade-in="1.5" data-fade-out="1.5" data-automation="{j}"></audio>')

# id, start, file, duration, volume, media_start, fade
SFX = [
 # ambience
 ("amb-hook", 0.0, "room_tone_wind_blowing_long", 9.8, 0.30, 0, 1.0),
 ("amb-malam", 29.5, "july_night", 9.3, 0.40, 5, 1.0),
 ("amb-hujan", 39.9, "rain_on_roof", 13.0, 0.50, 3, 1.2),
 ("amb-owl", 66.1, "owl_hooting", 4.2, 0.35, 2, 0.8),
 ("amb-ataswah", 82.2, "hallow_wind", 4.6, 0.25, 0, 1.0),
 ("amb-makhluk", 179.3, "hallow_wind", 4.6, 0.40, 8, 1.0),
 ("amb-seram", 199.8, "wind_quiet_creaks", 12.9, 0.22, 10, 1.5),
 ("amb-pagi", 193.8, "june_songbirds", 3.7, 0.35, 4, 0.8),
 # story sounds
 ("sniff-1", 2.7, "human_nose_sniffing", 1.2, 0.50, 1, 0.3),
 ("thunder", 40.2, "distant_thunder", 6.0, 0.55, 0, 1.5),
 ("tapak", 66.2, "distant_footsteps_on_wood", 3.4, 0.60, 0, 0.6),
 ("pintu", 70.3, "creaking_wooden_door", 2.6, 0.60, 0, 0.6),
 ("jantung-1", 72.6, "heartbeat-4", 3.0, 0.85, 0, 0.6),
 ("air-dulang", Src(207.4), "water_pour_into_surgical_tray", 2.3, 0.50, 1, 0.5),
 ("sapu", 96.6, "sweeping_wooden_porch", 3.0, 0.45, 2, 0.6),
 ("gosok", 101.8, "scrubbing_metal", 2.0, 0.40, 0, 0.5),
 ("air-paip", 108.3, "water_drains_in_pipe", 2.5, 0.45, 0, 0.6),
 ("logam", 112.4, "metal_scrap_rattling", 1.5, 0.50, 0, 0.4),
 ("longkang", 118.7, "water_drains_in_pipe", 2.0, 0.40, 6, 0.6),
 ("daun", 145.0, "leaves_russle_on_tree", 2.5, 0.45, 2, 0.6),
 ("baldi", 148.5, "pour_into_metal_bucket", 2.2, 0.50, 0, 0.5),
 ("jam-1", 154.9, "clock_ticking", 1.4, 0.50, 0, 0.3),
 ("nyamuk", 159.9, "flies_buzzing_and_circling", 1.1, 0.40, 0, 0.15),
 ("ular", 171.7, "animal_hiss_and_rattle", 2.0, 0.50, 0, 0.5),
 ("jam-2", 183.9, "clock_ticking", 5.8, 0.45, 1, 0.6),
 ("sniff-2", 189.7, "human_nose_sniffing", 1.2, 0.40, 4, 0.3),
 ("jantung-2", 198.0, "heartbeat-4", 2.0, 0.85, 0, 0.3),
 ("nafas", 207.2, "breathing_echo_space", 5.4, 0.30, 0, 1.2),
 # edit sounds
 ("taip-1", 9.9, "typing", 1.2, 0.35, 0, 0.3),
 ("taip-2", 66.2, "typing", 1.2, 0.30, 0, 0.3),
 ("taip-3", 154.95, "typing", 1.2, 0.35, 0, 0.3),
 ("taip-4", 212.8, "typing", 1.2, 0.35, 0, 0.3),
 ("taip-5", 282.8, "typing", 1.4, 0.35, 0, 0.3),
 ("cop-1", 4.8, "impact-bass-2", 1.5, 0.35, 0, 0.6),
 ("cop-2", 47.25, "click-soft", 0.37, 0.50, 0, 0),
 ("cop-3", 54.2, "click-soft", 0.37, 0.50, 0, 0),
 ("whoosh-1", Src(207.25), "whoosh-short", 0.57, 0.30, 0, 0),
 ("whoosh-2", 168.75, "whoosh-short", 0.57, 0.30, 0, 0),
 ("riser", 271.2, "riser", 1.4, 0.25, 8.6, 0.3),
 # quiet "Pesan" section: soft key taps on each new note (story sound every 4-6 s)
 ("key-1", 214.1, "key-press", 0.43, 0.35, 0, 0), ("key-2", 218.6, "key-press", 0.43, 0.35, 0, 0),
 ("key-3", 227.8, "key-press", 0.43, 0.35, 0, 0), ("key-4", 233.0, "key-press", 0.43, 0.35, 0, 0),
 ("key-5", 238.95, "key-press", 0.43, 0.35, 0, 0), ("key-6", 244.8, "key-press", 0.43, 0.35, 0, 0),
 ("key-7", 251.0, "key-press", 0.43, 0.35, 0, 0), ("key-8", 257.6, "key-press", 0.43, 0.35, 0, 0),
 ("key-9", 261.05, "key-press", 0.43, 0.35, 0, 0), ("key-10", 265.65, "key-press", 0.43, 0.35, 0, 0),
 ("key-11", 277.55, "key-press", 0.43, 0.35, 0, 0),
]
# ---- rules.md §3C: emotion moment = transition + matching SFX, together (source times, mapped to the current cut)
# kind: scare (flash + shake + punch + stinger), surprise (whip zoom-snap + whoosh/impact), happy (warm glow + bounce + chime/sparkle)
EMO = [
 (Src(173.94), "scare",    "Mayat.",                      [("glitch-2", 1.2, 0.40, 0), ("impact-bass-2", 1.5, 0.55, 0)]),
 (Src(174.90), "surprise", "Biar betul Cikgu?",           [("whoosh-cinematic", 1.0, 0.35, 0)]),
 (Src(176.42), "scare",    "Bilik mayat.",                [("heartbeat-single", 1.2, 0.90, 0), ("impact-bass-1", 1.2, 0.45, 0)]),
 (Src(233.96), "surprise", "Min, tak ada pilihan",        [("whoosh-short", 0.57, 0.35, 0), ("impact-bass-1", 1.2, 0.30, 0)]),
 (Src(247.24), "happy",    "Alhamdulillah, jemaah tolong", [("chime", 2.0, 0.30, 0)]),
 (Src(305.92), "happy",    "Settle, tiga benda",          [("ping", 1.3, 0.35, 0), ("pop", 0.72, 0.30, 0)]),
 (Src(317.70), "surprise", "Ayah kau reti perubatan Islam?", [("whoosh", 0.57, 0.35, 0), ("pop", 0.72, 0.25, 0)]),
 (Src(452.54), "scare",    "Terbangun",                   [("heartbeat-single", 1.2, 0.80, 0)]),
 (Src(464.32), "scare",    "Ada bau pelik tak?",          [("glitch-3", 1.2, 0.35, 0), ("impact-bass-2", 1.5, 0.45, 0)]),
 (Src(478.84), "scare",    "Kalau dia usik kaki kita",    [("glitch-1", 1.0, 0.30, 0)]),
 (Src(516.50), "happy",    "Al-Baqarah, penuh",           [("sparkle", 1.8, 0.30, 0)]),
 (Src(542.48), "happy",    "Tips",                        [("chime", 2.0, 0.28, 0)]),
 (Src(576.22), "happy",    "Kurangkan beban",             [("sparkle", 1.8, 0.28, 0)]),
 (Src(585.98), "happy",    "Better ambil",                [("ping", 1.3, 0.35, 0), ("pop", 0.72, 0.30, 0)]),
]
EMO = [(M(t), k, lab, sf) for t, k, lab, sf in EMO]
emo_js = ", ".join(f'[{t}, "{k}"]' for t, k, lab, sf in EMO)
for n, (t, k, lab, sf) in enumerate(EMO):
    for m, (f, d, v, ms) in enumerate(sf):
        SFX.append((f"emo{n}-{m}", Src(-1), f, d, v, ms, 0.05))
aud = []
emo_iter = iter([(t, f) for t, k, lab, sf in EMO for (f, d, v, ms) in sf])
for n, (i, t, f, d, v, ms, fade) in enumerate(SFX):
    t = next(emo_iter)[0] if i.startswith("emo") else M(t)
    aud.append(f'      <audio id="sfx-{i}" class="clip" data-start="{t}" data-duration="{d}"' + (f' data-media-start="{ms}"' if ms else "") +
               f' data-track-index="{7 + n % 3}" src="assets/sfx/{f}.mp3" data-volume="{v}"' + (f' data-fade-in="{min(fade, d/3):.2f}" data-fade-out="{min(fade, d/3):.2f}"' if fade else "") + '></audio>')

hosts = "\n".join(f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{s}" data-duration="{d}" data-track-index="{2 + k % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:10"></div>' for k, (c, s, d) in enumerate(SCENES))

html = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>PB1 - 30 Hari Bilik Mayat (Part 2)</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      /* PB1: see DESIGN.md (funnel 4 storytelling) */
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0E1726; }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; }}
      #ground {{ position:absolute; inset:0; background:#0E1726; }}
      #cam {{ position:absolute; inset:0; z-index:1; transform-origin:520px 730px; }}
      #cam video {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
      #shake {{ position:absolute; inset:0; transform-origin:520px 730px; }}
      #fx-flash, #fx-red, #fx-glow {{ position:absolute; inset:0; z-index:30; pointer-events:none; opacity:0; }}
      #fx-flash {{ background:#FFF6E8; }}
      #fx-red {{ background:radial-gradient(ellipse at 50% 45%, rgba(178,58,46,0) 30%, rgba(120,20,14,.85) 100%); }}
      #fx-glow {{ z-index:16; mix-blend-mode:screen; background:radial-gradient(ellipse at 50% 38%, rgba(255,200,120,.55) 0%, rgba(243,169,60,.18) 45%, rgba(243,169,60,0) 75%); }}
      #scrim {{ position:absolute; left:0; right:0; top:1100px; height:400px; z-index:15; pointer-events:none;
        background:linear-gradient(180deg, rgba(14,23,38,0) 0%, rgba(14,23,38,.62) 42%, rgba(14,23,38,.62) 72%, rgba(14,23,38,0) 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
      <div id="ground"></div>
      <div id="cam"><div id="shake">
        <video id="talk-past" class="clip" data-start="0" data-duration="{SPLIT}" data-track-index="0" src="assets/video/talk.mp4" muted playsinline></video>
        <video id="talk-now" class="clip" data-start="{SPLIT}" data-duration="{round(TALK_END - SPLIT, 3)}" data-media-start="{SPLIT}" data-track-index="0" src="assets/video/talk.mp4" muted playsinline></video>
      </div></div>
      <div id="fx-glow" data-layout-ignore></div>
      <div id="fx-red" data-layout-ignore></div>
      <div id="fx-flash" data-layout-ignore></div>

{hosts}

      <div id="scrim" data-layout-ignore></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TALK_END}" data-track-index="1" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:20"></div>

      <audio id="voice" class="clip" data-start="0" data-duration="{TALK_END}" data-track-index="5" src="assets/video/voice.m4a" data-volume="1"></audio>
{music("music-susah", "sad-piano", 0, M(73.2), 0, 0.18, 0.36)}
{music("music-seram", "universal-drone", M(70.2), M(214.2), 40, 0.5, 0.9)}
{music("music-bangkit", "heart-strings", M(211.7), END, 0, 0.17, 0.36)}
{chr(10).join(aud)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // Cinematic framing (funnel 4): new framing on a cut at most every ~4 s; y keeps the head in the band under the notes.
      const CAM = [{cam_js}];
      tl.fromTo("#cam", {{ scale: 1.5, y: -38 }}, {{ scale: 1.22, y: -21, duration: 0.6, ease: "expo.out" }}, 0);
      for (const [t, s, y] of CAM) if (t > 0) tl.set("#cam", {{ scale: s, y: y }}, t);
      // Silences after heavy lines: slow push-in while the frame holds.
      const HOLDS = [{hold_js}];
      for (const [a, b, s, y] of HOLDS) tl.to("#cam", {{ scale: s, y: y, duration: b - a, ease: "sine.inOut" }}, a);
      // rules.md §3C emotion transitions (paired with SFX in the audio list)
      const EMO = [{emo_js}];
      for (const [t, k] of EMO) {{
        if (k === "scare") {{
          tl.set("#fx-flash", {{ opacity: 0.9 }}, t).to("#fx-flash", {{ opacity: 0, duration: 0.16, ease: "power2.out" }}, t + 0.033);
          tl.set("#fx-red", {{ opacity: 0.75 }}, t).to("#fx-red", {{ opacity: 0, duration: 0.9, ease: "power2.out" }}, t + 0.1);
          tl.fromTo("#shake", {{ scale: 1.14 }}, {{ scale: 1, duration: 0.5, ease: "expo.out", immediateRender: false }}, t);
          const X = [18, -15, 12, -9, 6, -3, 0];
          X.forEach((x, i) => tl.set("#shake", {{ x: x, y: (i % 2 ? -1 : 1) * x * 0.5 }}, t + i * 0.033));
        }} else if (k === "surprise") {{
          tl.fromTo("#shake", {{ scale: 1.1, rotation: -1.2 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2)", immediateRender: false }}, t);
          tl.set("#fx-flash", {{ opacity: 0.35 }}, t).to("#fx-flash", {{ opacity: 0, duration: 0.12 }}, t + 0.033);
        }} else {{
          tl.fromTo("#fx-glow", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: "sine.out", immediateRender: false }}, t)
            .to("#fx-glow", {{ opacity: 0, duration: 1.1, ease: "sine.in" }}, t + 0.9);
          tl.fromTo("#shake", {{ scale: 1.045 }}, {{ scale: 1, duration: 0.6, ease: "elastic.out(1, 0.5)", immediateRender: false }}, t);
        }}
      }}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(html)
print("index.html written; cam keys", len(cam), "holds", len(holds), "sfx", len(SFX), "end", END)
