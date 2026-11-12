#!/bin/bash
# Phone delivery copy — user rules 2026-11-11/12: 1080x1920, 90–100 MB (target 95), "kualiti kayangan".
# Phone could not save 120 MB; ≤100 MB works. Max quality inside that budget:
#   HEVC (x265) 2-pass, preset slow, aq-mode 3, psy-rd, light deblock, hvc1 tag (iPhone/Android/TikTok/IG play it),
#   -14 LUFS audio (AAC 256k). Size is checked and the encode redone if it lands outside 90–100 MB.
# usage: deliver.sh <rendered.mp4> <out.mp4> [target_MB=95] [hevc|h264]
set -e
IN="$1"; OUT="$2"; MB="${3:-95}"; CODEC="${4:-hevc}"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
A=256
P=$(mktemp -d); trap 'rm -rf "$P"' EXIT
enc() { # $1 = target MB
  V=$(python3 -c "d=float('$DUR'); print(max(1200, int($1*8000*0.975/d - $A)))")
  echo "duration ${DUR}s → video ${V} kbps ($CODEC, target $1 MB)"
  VF="scale=1080:1920:flags=lanczos,format=yuv420p"
  COMMON=(-color_primaries bt709 -color_trc bt709 -colorspace bt709)
  if [ "$CODEC" = "hevc" ]; then
    XP="log-level=error:aq-mode=3:psy-rd=2.0:psy-rdoq=1.0:deblock=-1,-1:rc-lookahead=40:bframes=6:colorprim=bt709:transfer=bt709:colormatrix=bt709"
    ffmpeg -nostdin -v error -y -i "$IN" -vf "$VF" -c:v libx265 -preset slow -b:v ${V}k -x265-params "$XP:pass=1:stats=$P/x265.log" -an -f mp4 /dev/null
    ffmpeg -nostdin -v error -y -i "$IN" -vf "$VF" -c:v libx265 -preset slow -b:v ${V}k -x265-params "$XP:pass=2:stats=$P/x265.log:vbv-maxrate=$((V*2)):vbv-bufsize=$((V*4))" \
      -tag:v hvc1 "${COMMON[@]}" -movflags +faststart -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a ${A}k -ar 48000 "$OUT"
  else
    ffmpeg -nostdin -v error -y -i "$IN" -vf "$VF" -c:v libx264 -preset veryslow -tune film -b:v ${V}k -pass 1 -passlogfile "$P/x" -an -f mp4 /dev/null
    ffmpeg -nostdin -v error -y -i "$IN" -vf "$VF" -c:v libx264 -preset veryslow -tune film -profile:v high -b:v ${V}k -maxrate $((V*2))k -bufsize $((V*4))k -pass 2 -passlogfile "$P/x" \
      "${COMMON[@]}" -movflags +faststart -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a ${A}k -ar 48000 "$OUT"
  fi
}
enc "$MB"
SZ=$(python3 -c "import os;print(round(os.path.getsize('$OUT')/1e6,1))")
if python3 -c "import sys; sys.exit(0 if 90<=$SZ<=100 else 1)"; then :; else
  NEW=$(python3 -c "print(round($MB*$MB/$SZ, 1))"); echo "size ${SZ} MB outside 90–100 → re-encode at ${NEW} MB"; enc "$NEW"
  SZ=$(python3 -c "import os;print(round(os.path.getsize('$OUT')/1e6,1))")
fi
echo "$OUT  ${SZ} MB  ($(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height -of csv=p=0 "$OUT"))"
