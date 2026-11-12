"""Detect filled pauses (mmm / eee / hmm / aaa) acoustically.
A filled pause = voiced, loud enough, spectrally STATIONARY for >= MIN s.
usage: fillers.py audio.wav [t0 t1] [--min 0.35]  -> prints 'start end dur flux' (source seconds)"""
import sys, wave, numpy as np
args=[a for a in sys.argv[1:]]
MIN=0.35; FLUX=0.45
if '--min' in args: i=args.index('--min'); MIN=float(args[i+1]); del args[i:i+2]
wf=wave.open(args[0]); sr=wf.getframerate()
a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
t0,t1=(float(args[1]),float(args[2])) if len(args)>2 else (0,len(a)/sr)
H=int(sr*0.01); N=int(sr*0.032); win=np.hanning(N)
nb=40; f=np.fft.rfftfreq(N,1/sr)
mel=lambda x:2595*np.log10(1+x/700); edges=np.linspace(mel(80),mel(4000),nb+2); hz=700*(10**(edges/2595)-1)
fb=np.zeros((nb,len(f)))
for i in range(nb):
    l,c,r=hz[i],hz[i+1],hz[i+2]; fb[i]=np.clip(np.minimum((f-l)/(c-l),(r-f)/(r-c)),0,None)
st=int(t0*sr); en=int(t1*sr)
fr=np.lib.stride_tricks.sliding_window_view(a[st:en],N)[::H]*win
P=np.abs(np.fft.rfft(fr))**2
db=10*np.log10(P.sum(1)+1e-10)
L=np.log(fb@P.T+1e-9).T; L=L-L.mean(1,keepdims=True)
# zero crossing -> voicing proxy (low zcr = voiced)
zcr=(np.abs(np.diff(np.sign(fr),axis=1))>0).mean(1)
flux=np.r_[0,np.sqrt(((L[1:]-L[:-1])**2).mean(1))]
k=7; fl=np.convolve(flux,np.ones(k)/k,'same')
thr=np.percentile(db,60)-12
ok=(db>thr)&(fl<FLUX)&(zcr<0.15)
out=[];i=0;n=len(ok)
while i<n:
    if ok[i]:
        j=i
        while j<n and ok[j]: j+=1
        if (j-i)*0.01>=MIN: out.append((t0+i*0.01+0.016,t0+j*0.01+0.016,float(fl[i:j].mean())))
        i=j
    else: i+=1
for s,e,m in out: print(f"{s:.2f} {e:.2f} {e-s:.2f} {m:.3f}")
