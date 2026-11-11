#!/usr/bin/env python3
"""Generate a HyperFrames captions sub-composition (word-by-word, bold white,
keywords yellow) from cuts.json words.
usage: build_captions.py cuts.json OUT.html [--honest-from SEC] [--fix 'a=>b' ...] [--kw WORD ...] [--lower] [--karaoke] [--hl bg,fg] [--kwcolor C] [--css FILE]
- groups of max 3 words, broken at sentence ends / pauses >= 0.15 s
- active word pops (scale) ; after --honest-from the active word gets a yellow highlight box
- tokens like "41" "%" are merged; --fix rewrites a token (case-insensitive) e.g. 'ilan=>iklan'"""
import json, sys, re, html
args = sys.argv[1:]
cuts, out = args[0], args[1]
honest = 1e9; fixes = {}; kws = set(); css_file = None; case = "upper"
hl_bg, hl_fg, kw_color = "#FFC700", "#0A2A7A", "#FFC700"
i = 2
while i < len(args):
    if args[i] == "--honest-from": honest = float(args[i+1]); i += 2
    elif args[i] == "--fix": a, b = args[i+1].split("=>"); fixes[a.lower()] = b; i += 2
    elif args[i] == "--kw": kws.add(args[i+1].upper()); i += 2
    elif args[i] == "--css": css_file = args[i+1]; i += 2
    elif args[i] == "--lower": case = "lower"; i += 1
    elif args[i] == "--karaoke": honest = -1; i += 1
    elif args[i] == "--hl": hl_bg, hl_fg = args[i+1].rsplit(",", 1); i += 2
    elif args[i] == "--kwcolor": kw_color = args[i+1]; i += 2
    else: i += 1
W = json.load(open(cuts))["words"]
# merge split tokens
words = []
for w in W:
    t = w["text"]
    if words and (t in ("%",) or re.match(r"^[,.]?0{3}", t) or t.startswith("-")):
        words[-1]["text"] += t; words[-1]["end"] = w["end"]; continue
    words.append(dict(w))
for w in words:
    raw = w["text"]; end_punct = raw.rstrip()[-1:] if raw.rstrip()[-1:] in ".?!," else ""
    t = re.sub(r"[.,!]+$", "", raw).strip()
    t = fixes.get(t.lower(), t)
    w["disp"] = t.upper() if case == "upper" else t.lower(); w["brk"] = end_punct in (".", "?", "!")
    w["comma"] = end_punct == ","
groups, cur = [], []
for k, w in enumerate(words):
    cur.append(w)
    nxt = words[k+1] if k+1 < len(words) else None
    gap = (nxt["start"] - w["end"]) if nxt else 9
    unit = nxt is not None and nxt["text"].strip(" .,").upper() in ("JUTA", "TAHUN", "RIBU", "%")
    if (len(cur) >= 3 and not unit) or len(cur) >= 4 or w["brk"] or w["comma"] or gap >= 0.15 or nxt is None or \
       (nxt and (nxt["start"] >= honest) != (w["start"] >= honest)):
        groups.append(cur); cur = []
def is_kw(d): return any(d.upper() == k or d.upper().startswith(k) for k in kws)
parts, js = [], []
for gi, g in enumerate(groups):
    gs = max(g[0]["start"] - 0.04, 0.0)
    ge = (groups[gi+1][0]["start"] - 0.04) if gi+1 < len(groups) else g[-1]["end"] + 0.6
    ge = min(ge, g[-1]["end"] + 0.6)
    ge = max(ge, gs + 0.3)   # zero-length word timings would give data-duration 0 (= whole film)
    hon = g[0]["start"] >= honest
    spans = []
    for wi, w in enumerate(g):
        cls = "w" + (" kw" if is_kw(w["disp"]) else "")
        spans.append(f'<span id="c{gi}-{wi}" class="{cls}">{html.escape(w["disp"])}</span>')
        js.append((f"#c{gi}-{wi}", w["start"], w["end"], hon, is_kw(w["disp"])))
    parts.append(f'    <div id="cg{gi}" class="clip cgroup{" honest" if hon else ""}" data-start="{gs:.3f}" '
                 f'data-duration="{ge-gs:.3f}" data-track-index="1">{" ".join(spans)}</div>')
    js.append((f"#cg{gi}", gs, ge, None, None))
tl = []
for sel, s, e, hon, kw in js:
    if hon is None:
        tl.append(f'tl.fromTo("{sel}",{{opacity:0,y:18,scale:0.92}},{{opacity:1,y:0,scale:1,duration:0.14,ease:"back.out(2)"}},{s:.3f});')
        tl.append(f'tl.to("{sel}",{{opacity:0,duration:0.08,ease:"power2.in"}},{e-0.08:.3f});')
    else:
        tl.append(f'tl.fromTo("{sel}",{{opacity:0.0,scale:0.8}},{{opacity:1,scale:1.12,duration:0.1,ease:"power3.out"}},{s:.3f});')
        tl.append(f'tl.to("{sel}",{{scale:1,duration:0.12,ease:"power2.out"}},{s+0.1:.3f});')
        if hon:
            tl.append(f'tl.set("{sel}",{{backgroundColor:"{hl_bg}",color:"{hl_fg}"}},{s:.3f});')
            base = kw_color if kw else "#ffffff"
            tl.append(f'tl.set("{sel}",{{backgroundColor:"rgba(0,0,0,0)",color:"{base}"}},{e:.3f});')
style_override = open(css_file).read() if css_file else None
doc = f'''<template>
  <style>
    #root {{ position:absolute; inset:0; pointer-events:none; }}
    #root .cgroup {{ position:absolute; left:0; right:0; top:1205px; text-align:center; padding:0 70px;
      font-family:"Montserrat", sans-serif; font-weight:900; font-size:84px; line-height:1.05; letter-spacing:-0.01em;
      color:#fff; overflow:visible; opacity:0;
      text-shadow:0 0 2px #000, 0 4px 0 rgba(0,0,0,.85), 0 8px 24px rgba(0,0,0,.55);
      -webkit-text-stroke:3px #000; paint-order:stroke fill; }}
    #root .w {{ display:inline-block; opacity:0; padding:0 6px; border-radius:14px; }}
    #root .w.kw {{ color:#FFC700; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(parts)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join("    "+l for l in tl).strip()}
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
if style_override:
    doc = re.sub(r"<style>.*?</style>", "<style>\n" + style_override.replace("\\", "\\\\") + "\n  </style>", doc, count=1, flags=re.S)
open(out, "w").write(doc)
print(f"{len(groups)} groups, {len(words)} words -> {out}")
