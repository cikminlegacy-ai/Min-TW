#!/bin/bash
# Phone delivery copy (user rule 2026-11-11): 1080x1920, 100–150 MB (target 125 MB), -14 LUFS, saves on a phone.
# usage: deliver.sh <rendered.mp4> <out.mp4> [target_MB]
set -e
IN="$1"; OUT="$2"; MB="${3:-125}"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
A=192   # audio kbps
# total kbit = MB*8*1000 (decimal MB, ~4% container headroom)
V=$(python3 -c "d=float('$DUR'); v=int($MB*8000*0.96/d - $A); print(max(1500, min(v, 40000)))")
echo "duration ${DUR}s → video ${V} kbps (target ${MB} MB)"
P=$(mktemp -d)
ffmpeg -nostdin -v error -y -i "$IN" -vf "scale=1080:1920:flags=lanczos" -c:v libx264 -preset slow -b:v ${V}k -pass 1 -passlogfile "$P/x" -an -f mp4 /dev/null
ffmpeg -nostdin -v error -y -i "$IN" -vf "scale=1080:1920:flags=lanczos" -c:v libx264 -preset slow -b:v ${V}k -maxrate $((V*2))k -bufsize $((V*4))k -pass 2 -passlogfile "$P/x" \
  -pix_fmt yuv420p -movflags +faststart -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a ${A}k -ar 48000 "$OUT"
rm -rf "$P"
ls -la "$OUT" | awk '{printf "%s  %.1f MB\n", $9, $5/1000000}'
