#!/bin/bash
# Rebuild PB1 after a re-cut (cuts.json already planned). Usage: ./rebuild.sh [skip-talk]
set -e
SK=/home/user/Min-TW/.claude/skills/edit-video/scripts
SRC="/tmp/claude-0/-home-user-Min-TW/94a4eb73-a899-5606-9809-9f8ce39fcd34/scratchpad/src4/PB 1/IMG_0547.MOV"
if [ "$1" != skip-talk ]; then
  python3 $SK/build_talk.py "$SRC" cuts.json assets/video/talk.mp4
  ffmpeg -nostdin -v error -y -i assets/video/talk.mp4 -vn -c:a copy assets/video/voice.m4a
fi
python3 $SK/build_captions.py cuts.json compositions/captions.html --lower --karaoke --hl "rgba(243,169,60,0.92),#1B1A17" --kwcolor "#F3A93C" --css captions.css --fix 'Jumat=>Jumaat' --fix 'kuyuk=>kuyup' --fix 'Ilang=>elaun' --fix 'ilang=>elaun' --fix 'pengurusi=>pengerusi' --fix 'allow=>allowance' --fix 'Ujung=>Hujung' --fix 'Kabat=>kabait' --fix 'kabat=>kabait' --fix 'rutin=>dalami' --kw MAYAT --kw 13 --kw BAU --kw 30 --kw HUJAN
python3 build_scenes.py && python3 build_index.py && ./apply_grades.sh
npm run check 2>&1 | grep -E "✗|Check (passed|failed)" | cut -c1-200
