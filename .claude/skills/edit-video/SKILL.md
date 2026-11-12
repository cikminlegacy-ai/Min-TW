---
name: edit-video
description: Editor + script doctor + strategist for Muhaimin (B40 KL audience, 4-funnel playbook). Edit Muhaimin's talking-head videos for TikTok / Instagram Reels / YouTube Shorts (9:16, 1080x1920) with HyperFrames, following his saved 9-point structure (transcribe first, animation that never covers the face, premium SFX, TikTok+IG safe zone, ducked background music, cut repeats/pauses, strongest hook, preview before render, a NEW design every video). Use when the user types /edit-video followed by a Google Drive / video link (optionally a HOOK LOCK, script or notes).
---

# /edit-video — Muhaimin short-form editor

The user sends `/edit-video <link>` (+ maybe hook / script / notes). Do the whole edit and **stop at a preview**.
Never render until the user says "render"/"ok". Reply in Bahasa Melayu (casual, "aku/kau").
Do not ask the user to repeat their requirements — they are saved here. Do not ask many questions: make the most logical assumption and continue.
Input can be footage (do the full edit), or only a script/idea (then deliver the funnels.md written output — detect funnel, 3 hooks, second-by-second timeline, exact on-screen text, music/SFX/B-roll, caption + 5 hashtags, What's Next CTA — no build).

**Read first, every time (all in this folder):**
0. `funnels.md` — Muhaimin's strategy playbook (role, B40 KL audience, 2026 algorithm, golden rules, 4 funnels, CTA & analogy banks, the 9 required outputs). **Highest priority**: the detected funnel decides duration, structure, pacing, music, text tone and CTA, and overrides the generic durations/pacing in rules.md and theme.md.
1. `rules.md` — the user's structure (§1–14; §12 subtitles, §13 reference/pro style, §14 Quran are newest). Binding for every video.
2. `design-log.md` — what past videos looked like. Rule 9: the new design must differ (≥5 of 8 dimensions vs the last video, no repeated combination). Add an entry after rendering.
3. `theme.md` — the "TikTok awareness / naik followers" series brief (45–50 s, educate only, never sell, honest close-up ending). Apply when the video is that kind of content or the user mentions it. Its blue/yellow palette was AW1's design — do NOT reuse it by default (rule 9 wins).

**DEFAULT STYLE (user approved 2026-11-12): `projects/tq1`** — copy its build_index.py system for every new video (rules.md §13). What changes per video is ONLY music, SFX, colour grade and transitions, chosen per emotion beat from the mood map (rules.md §15). Older reference build: `projects/aw1` (+ `EDIT-NOTES.md`) — reuse its *mechanics* (camera punch per jump cut, scene-per-beat, caption generator, honest blur), not its look.

## 0. Tools (installed by the Default environment's setup script)

Check, and install anything missing: `node -v` (22+), `ffmpeg`, `ffprobe`, `yt-dlp`, `gdown`, `python3 -c "import faster_whisper"`,
`ls ~/.claude/skills/{hyperframes,media-use,video-use}`, `ls ~/Developer/remotion-starter`. Missing → run the same steps manually:
`pip install gdown faster-whisper yt-dlp`; `git clone https://github.com/browser-use/video-use ~/Developer/video-use && (cd ~/Developer/video-use && uv sync) && ln -sfn ~/Developer/video-use ~/.claude/skills/video-use`;
`npx -y hyperframes@0.9.19 skills`; `npx hyperframes browser ensure`. Always `export HYPERFRAMES_TELEMETRY=0`.
Read the `/hyperframes` skill (contract) before writing compositions. Remotion (`~/Developer/remotion-starter`) is available but HyperFrames is the default engine.

## 1. Download

- Drive: `cd <scratchpad>/src && gdown --folder "<link>"` (single file: `gdown "https://drive.google.com/uc?id=<FILE_ID>"` — this gdown has no --fuzzy).
- YouTube/TikTok/IG reference: `yt-dlp -o "<scratchpad>/ref/%(id)s.%(ext)s" "<url>"`.
- Folder convention: talking-head `*.MOV` at top, `BAHAN/` = B-roll, `BG/` = backgrounds/extra B-roll.
- Contact-sheet every clip (`fps=4/dur,scale=320:-2,tile=4x1`) and LOOK at it. Flag stock watermarks (iStock `_adpp_is` previews).

## 2. Transcribe FIRST (rule 1)

- ElevenLabs if a key is configured (proxy injects it; `~/Developer/video-use/.env` holds a placeholder):
  `cd ~/Developer/video-use && uv run python helpers/transcribe.py <video> --edit-dir <scratchpad>/edit --language ms` then `pack_transcripts.py`. It costs credits — fine, the user asked for transcription. On 401/no key → fall back.
- Whisper fallback: `ffmpeg -i <video> -vn -ac 1 -ar 16000 audio.wav && python3 scripts/transcribe.py audio.wav medium` → `transcript.json` (edit the domain prompt words in the script for the topic).
- Noisy room (fan/AC) and ffmpeg silencedetect misses pauses → `python3 scripts/silences.py audio.wav > silences.txt` (energy-based).
- Footage may contain the user talking TO YOU ("Claude, …", "cuba zoom in", "okay tu information yang lepas"): those are directions, not content — follow them, cut them out, and list what you cut in the preview message.
- **Detect the funnel** (funnels.md) from the transcript before cutting; it sets the target duration and what to keep (e.g. funnel 2 keeps 1 s pauses after key points; funnel 4 keeps a 1.5 s silence after the most painful line).
- Read the whole transcript; mark hook candidates, numbers/facts, brands, comparisons, CTA, repeats.

## 3. Cut (rule 6) and hook (rule 7)

- Silences: `ffmpeg -i audio.wav -af silencedetect=n=-38dB:d=0.22 -f null - 2>&1 | grep -oE 'silence_(start|end): [0-9.]+' | awk '{print $2}' | paste - - > silences.txt`
- **Cut policy (rules.md §6, user 2026-11-12): KEEP all story content.** Build keep.json as the WHOLE recording minus only: fillers (eh/aa/hmm/ok so/okey/sebenarnya kan), sentences said twice, false starts, salam intro, looking-down/fiddling, editor-directed talk, and a clearly weak part. Never drop content to hit a funnel duration. Hook line may be copied to the front (cold open). Exact cut points via an RMS dB-minimum scan between words.
- After planning, diff transcript vs cuts.json words: the only missing words must be the ones you meant to drop. List every drop in the preview message.
- Fillers & repeats (rules.md §6): disfluency-prompt Whisper → `scripts/align.py audio.wav transcript.json <mms model dir> aligned.json` (MMS forced aligner from HF MahmoudAshraf/mms-300m-1130-forced-aligner; needs torch/torchaudio CPU + transformers) → `scripts/find_drops.py` + `scripts/fillers.py` → review list.
- `SPEED=1.1 python3 scripts/plan_cuts.py keep.json silences.txt transcript.json > cuts.json` (speed 1.1–1.2 per rules.md §6B, never above 1.2; jump-cuts pauses > 0.3 s; no holds). Then rebuild the cut audio and re-transcribe it to verify (rules.md §6).
- **No scene delays** (user 2026-11-12): holds (4th keep value → freeze+silence) only if the user asks; dramatic beats ≤ 0.4 s.
- Long source (10 min): build_talk takes ~20–40 min on CPU (4K HDR decode). Start it early in the background and write design/scenes meanwhile.
- **Disk is limited** (per-session allowance): segment files are big (PB1: 7 GB). build_talk now encodes straight from the concat list and deletes its temp dir. Before a new video, delete old `/tmp/talk_*` dirs and old source downloads from the scratchpad (re-downloadable from Drive); `df -h /tmp` when anything fails with exit 228 / no space.
- `python3 scripts/build_talk.py "<src>" cuts.json talk.mp4` → 1440x2560/30fps, HDR→SDR tonemap + bt709 tags, voice cleaned + −14 LUFS. Extract `voice.m4a` (`-vn -c:a copy`); videos stay muted, voice is its own `<audio>`.

## 4. Design (rule 9) — decide before building

Write a short `DESIGN.md` in the project: palette, fonts, subtitle style, hook card, transitions, grade, music genre, SFX style — checked against `design-log.md`.
**Fonts (rule 10, updated 2026-11-12): chosen by the story's vibe every time** (table in rules.md §10; Nunito + Montserrat is the default for neutral/educational videos). Subtitles stay easy to read. State vibe + reason in DESIGN.md. Browse `npx hyperframes catalog --tag caption-style --json`, `--tag transition`, and the frame presets in `~/.claude/skills/hyperframes/assets/frame-presets/`.

## 5. Build (HyperFrames)

`cd projects && npx hyperframes init <name> --example blank --resolution portrait --non-interactive --skip-skills --skill=hyperframes`
- Camera: `#cam` wrapper with transform-origin on the face (measure hair-top/chin on the real footage); a framing change on jump cuts, and a pattern interrupt (zoom / pop text / B-roll) on **every main story point**.
- Animations only where they add meaning (rule 2). **Never cover the face**: snapshot each beat; put graphics above the head (push `#cam` y down), on the opposite side, or as full-screen cutaways.
- Safe zone (rule 4): all text inside x 60–940, y 220–1330; captions ~1150–1300.
- Captions: **rules.md §12 (2026-11-12) overrides everything older**: black/white only, small (~46 px), ONE line of 3–5 words, fixed at chest/belly level, calm fade — no karaoke colours, no pops. `python3 scripts/build_captions.py ... --words 3-5 --one-line` style output (write a fresh generator if needed).
- **Reference video given → copy its style (rules.md §13)**; Quran verses → Rasm Uthmani from Quran.com/Tanzil + KFGQPC HAFS / Amiri Quran font (rules.md §14).
- Grade via `npx hyperframes media-treatment ... --grading '<json>' --apply` (never CSS filters); `grade-compare` 3–4 candidates first.
- Music (rule 5): new genre each video (Openverse → Jamendo works; Freesound/Wikimedia blocked). Duck under voice with a volume lane, e.g. `data-automation='{"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":0.14},{"t":0.3,"v":0.05},...]}]}'` built from word timings (0.05 while speaking, ~0.14 in gaps/cutaways), then optionally `node ~/.claude/skills/media-use/audio/scripts/carve.mjs --comp index.html`. Credit CC-BY tracks.
- SFX (rule 3 + **rule 3B story sound design**): build a sound map from the transcript — ambience per place/time, a story sound on every word that has a sound (pintu, air, malam, ular, tapak kaki, jantung…), edit sounds for text/transitions, a story sound or ambience change every 4–6 s, total silence 0.5–1.5 s before the scariest/most painful line. Source story sounds from `sfx/google-sound-library.txt` (CC BY 4.0; `curl -o x.ogg <url>` then convert to mp3; a few index entries return 404 — check the HTTP code and pick a neighbour), edit sounds from bundled Pixabay. Peak 1 frame after the word; `data-duration` = file length; everything ducked under the voice.

## 6. Verify → PREVIEW (rule 8)

`npm run check` → 0 errors. `npx hyperframes snapshot --at <every beat> -o /home/user/Min-TW/preview/<name>` → read the sheets; fix any face overlap, safe-zone breach, text collisions.
`npx hyperframes preview --background` → `report_preview_port`; send contact sheets (SendUserFile) + the funnels.md output in Malay rojak: "Aku detect ni funnel X, betul tak?", what was cut to fit the funnel duration, 3 new hook options (isu Malaysia + sakit B40 + ingin tahu), the second-by-second timeline as built, exact on-screen text, music/SFX/B-roll used, caption + 5 hashtags, the What's Next CTA, and a short "skrip tambah rakam" when the footage lacks a line the funnel needs (never fake his voice). Plus anything to decide (watermarks, music credit). Commit + push.

## 7. Render (only after approval)

`HYPERFRAMES_RENDER_DETACHED=1 npx hyperframes render -q delivery -w 4 -o out/<name>.mp4` in the background (CPU-only: ~50 min for 48 s with blur layers — warn the user). Then `ffmpeg -af ebur128=peak=true` (target −14 LUFS, ≤ −1 dBTP; compare with voice.m4a alone — mix ≈ voice means the bed sits well under the voice). Long videos: the delivery render is huge (PB1 4:45 = 839 MB) → also make an upload copy: `-c:v libx264 -crf 20 -maxrate 8M -bufsize 16M -af loudnorm=I=-14:TP=-1.5:LRA=11` (PB1 → 262 MB), spot-check frames, then **rule 11: `scripts/deliver.sh out/<render>.mp4 out/<name>-final-1080p.mp4`** (1080x1920, 90–100 MB, HEVC 2-pass max quality — rules.md §11) and send ONLY that file (copy to `/home/user/Min-TW/preview/`, SendUserFile display "attach"), add the `design-log.md` entry, commit + push.
