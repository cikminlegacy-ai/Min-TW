---
name: edit-video
description: Edit a Muhaimin TikTok talking-head video in the saved theme "MUHAIMIN - TIKTOK AWARENESS NAIK FOLLOWERS" (9:16, hook 3 saat, jump cuts, B-roll, subtitle kuning, lo-fi 10%) with HyperFrames. Use when the user types /edit-video followed by a Google Drive link (and optionally a HOOK LOCK, script or per-line edit notes).
---

# /edit-video — Tema Muhaimin (TikTok awareness, naik followers)

The user sends `/edit-video <google drive folder link>` and maybe a hook / script / notes.
Do the whole edit in the theme below and **stop at a preview** — never render the final MP4
until the user approves the preview (theme rule). Reply to the user in Bahasa Melayu (casual, "aku/kau" ok).

Read `theme.md` (in this folder) first: it is the user's rule book, verbatim. Everything below is how to execute it.
The first finished project is `projects/aw1` (see its `EDIT-NOTES.md`) — copy its scene files and look as the starting point.

## 0. Setup (every new session — the container is fresh)

```bash
pip install gdown faster-whisper            # Drive download + Malay transcription
npm i -g hyperframes@0.9.19 || true          # or always use: npx hyperframes@0.9.19
npx hyperframes skills                       # installs /hyperframes, /media-use ... skills (then read /hyperframes SKILL.md)
export HYPERFRAMES_TELEMETRY=0
```
Scripts live in `.claude/skills/edit-video/scripts/` (call them by absolute path).

## 1. Download

```bash
S=<scratchpad>; mkdir -p $S/src && cd $S/src && gdown --folder "<drive link>"
```
Folder convention from the user: the talking-head `*.MOV` at top, `BAHAN/` = B-roll stock clips,
`BG/` = background / extra B-roll. Make a contact sheet of every clip (ffmpeg `fps=4/dur,scale=320:-2,tile=4x1`) and LOOK at it to map clips to script lines.
Note any clip with a stock watermark (iStock `_adpp_is` previews) and tell the user.

## 2. Transcribe + plan cuts

- Audio: `ffmpeg -i TW.MOV -vn -ac 1 -ar 16000 audio.wav`
- `python3 scripts/transcribe.py audio.wav medium` → `transcript.json` (word timestamps, Malay, with a domain prompt — edit the prompt words for the new topic).
- Silences: `ffmpeg -i audio.wav -af silencedetect=n=-38dB:d=0.22 -f null - 2>&1 | grep -oE 'silence_(start|end): [0-9.]+' | awk '{print $2}' | paste - - > silences.txt`
- Write `keep.json` = ordered `[src_start, src_end, "label"]` ranges of sentences to KEEP. Drop: greetings/intro, "sebenarnya macam ni", "jadi", "eh/aa/hmm", repeated words ("Dulu, ... Dulu,"), weakest sentence(s) until total is **45–50 s**. Check exact cut points with an RMS energy scan (find the dB minimum between two words).
- `python3 scripts/plan_cuts.py keep.json silences.txt transcript.json > cuts.json` → removes every pause > 0.18 s inside kept ranges, prints total + remapped words.
- Check frames at segment boundaries for looking down / fiddling with cap or phone → cut those too.

## 3. Build the talking-head clip

`python3 scripts/build_talk.py "<TW.MOV>" cuts.json talk.mp4` (1440x2560, 30 fps, gop 15).
iPhone footage is HDR HLG: the script tonemaps (hable) to SDR and writes bt709 tags — if tags stay bt2020/arib the browser double-tonemaps. Voice is cleaned + loudnorm -14 LUFS.
Extract `voice.m4a` from it (`-vn -c:a copy`) — videos are muted in the composition, voice is its own `<audio>`.

## 4. HyperFrames project

`cd projects && npx hyperframes init <name> --example blank --resolution portrait --non-interactive --skip-skills --skill=hyperframes`
then follow the `projects/aw1` structure:

- `index.html`: `#cam` wrapper (transform-origin on the face) holding `#talk` (0 → start of honest part), `#talk-bg` + `#talk-fg` (honest part; bg blurred via media-treatment `effects.blur 0.7`, fg sharp with a radial CSS mask = "background blur"), `#honest-tint` vignette; one scene host per beat; captions host (z 20); voice, music, SFX `<audio>`s.
- Camera: `tl.set("#cam",{scale,y})` on EVERY jump-cut time (alternate 1.0–1.38) → hides cuts + gives the 2-second pattern interrupt. Hook: `fromTo scale 1.55→1.2` in 0.38 s expo.out, `y` pushed down so the hook card sits ABOVE the head (card must never cover the face/mouth).
- Hook card (compositions/hook.html): yellow `#FFC700` text on royal blue `#0A2A7A`, 10 px yellow border, top ≈190 px, slam-in scale 2.1→1 + shake, white flash, exits at 2.8 s. SFX at 0: whoosh-cinematic + pop (vol 1.6) + impact-bass.
- B-roll beats: landscape stock is low-res → put it in a rounded white-bordered card (1000x562) over a brand-colour ground, with a label chip; only HD clips go full-bleed. Big-number cards: count-up via a proxy object tween + onUpdate text. Keep the band 1150–1330 px free for captions.
- Captions: `python3 scripts/build_captions.py cuts.json compositions/captions.html --honest-from <sec> --fix 'wrong=>right' --kw 41% --kw JUTA ...` (Montserrat 900, 84 px, white + black stroke, keywords yellow, groups ≤3 words, active word pops; after `--honest-from` the active word gets a yellow highlight box). Fix whisper mistakes with `--fix`.
- Grade (premium + lighting) — always through the CLI, never CSS filters:
  `npx hyperframes media-treatment --project . --file index.html --selector '#talk' --grading '{"adjust":{"exposure":0.12,"contrast":0.14,"highlights":-0.12,"shadows":0.1,"blacks":-0.06,"temperature":0.07,"vibrance":0.18,"saturation":0.04},"details":{"vignette":0.22}}' --apply`
  (same for `#talk-fg`; `#talk-bg` adds `"effects":{"blur":0.7}`). Use `grade-compare` if the lighting is different.
- Music: lo-fi bed at `data-volume="0.1"`, start at its strongest bar (`data-media-start`), fades. CC0/CC-BY sources via Openverse (Jamendo works; Freesound previews and Wikimedia return 403/429 here). Current track: "Lofy" by macouno, Jamendo, CC BY 3.0 — credit it in the caption.
- SFX: bundled Pixabay set in `~/.claude/skills/media-use/audio/assets/sfx` (whoosh, whoosh-short, whoosh-cinematic, pop, impact-bass-1/2, riser, sparkle, click-soft). One per visible action, rotate whoosh variants, durations = file length.
- Ending (honest part): no B-roll, close-up, background blur, yellow highlight subs, a small "+ FOLLOW" pill on "follow saya". Never a sales CTA.

## 5. Verify, then PREVIEW (no render)

`npm run check` → 0 errors. `npx hyperframes snapshot --at <every beat> -o <dir>` → read the contact sheets, fix overlaps (face covered, X covering text, pills on captions).
`npx hyperframes preview --background` then `report_preview_port` the port, send the contact sheets to the user, list the edit decisions + timestamps. Commit + push the project (media is git-ignored).
Only after "ok/approve": `npx hyperframes render -q delivery -o out/<name>.mp4`, check `npx hyperframes audio out/<name>.mp4 --json`, send the file.
