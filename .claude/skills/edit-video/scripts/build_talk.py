#!/usr/bin/env python3
"""Cut the source talking-head into one jump-cut clip from cuts.json.
usage: build_talk.py SOURCE cuts.json OUT.mp4 [WIDTH HEIGHT]
- HDR (HLG/PQ) sources are tonemapped to SDR bt709 (hable) automatically.
- Output: H.264 30fps, keyframe every 15 frames (seek-safe for HyperFrames),
  AAC 48k, voice cleaned (highpass, light denoise, compression, -14 LUFS).
- 12 ms audio fades on every cut so jump cuts never click."""
import json, subprocess, sys, os, tempfile
src, cuts, out = sys.argv[1], sys.argv[2], sys.argv[3]
W, H = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (1440, 2560)
segs = json.load(open(cuts))["segments"]
trc = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=color_transfer",
                      "-of","csv=p=0",src],capture_output=True,text=True).stdout.strip()
hdr = trc in ("arib-std-b67","smpte2084")
vf = f"scale={W}:{H}:flags=lanczos"
if hdr:
    vf += (",zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv")
vf += ",fps=30,format=yuv420p"
tmp = tempfile.mkdtemp(prefix="talk_")
lst = open(os.path.join(tmp,"list.txt"),"w")
for i,s in enumerate(segs):
    d = s["src_out"]-s["src_in"]; f = os.path.join(tmp,f"s{i:03d}.mp4")
    af = f"afade=t=in:d=0.012,afade=t=out:st={max(d-0.012,0):.3f}:d=0.012"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{s['src_in']:.3f}","-i",src,"-t",f"{d:.3f}",
        "-vf",vf,"-af",af,"-c:v","libx264","-preset","medium","-crf","14","-g","15",
        "-c:a","pcm_s16le","-ar","48000","-ac","2",f.replace(".mp4",".mov")],check=True)
    lst.write(f"file '{f.replace('.mp4','.mov')}'\n"); print(f"seg {i+1}/{len(segs)}",flush=True)
lst.close()
cat = os.path.join(tmp,"cat.mov")
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst.name,"-c","copy",cat],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",cat,"-c:v","libx264","-preset","medium","-crf","16","-g","15",
    "-pix_fmt","yuv420p","-movflags","+faststart",
    "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
    "-bsf:v","h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
    "-af","highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=7",
    "-c:a","aac","-b:a","192k","-ar","48000",out],check=True)
print("wrote",out)
