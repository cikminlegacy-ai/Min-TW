"""Find filler + stutter-repeat drops from MMS-aligned words (align.py).
usage: find_drops.py aligned.json cuts.json audio16k.wav drops_out.json [skipStart-skipEnd ...]
  cuts.json = current cut (only words still kept are considered; a repeat is cut only if its 2nd copy is kept)
  skip windows (source s) = deliberate repeats / dialogue to leave alone. Review the printed list!
"""
import json,re,wave,numpy as np
import sys
T=[w for s in json.load(open(sys.argv[1])) for w in s['words']]
seg=json.load(open(sys.argv[2]))['segments']
wf=wave.open(sys.argv[3]);sr=wf.getframerate();A=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
def emin(a,b):
    if b-a<0.03: return (a+b)/2
    i0,i1=int(a*sr),int(b*sr);H=int(0.005*sr)
    e=[np.sqrt((A[i:i+H*2]**2).mean()) for i in range(i0,max(i0+1,i1-2*H),H)]
    return a+np.argmin(e)*0.005+0.005
def kept(a,b): return sum(max(0,min(b,s['src_out'])-max(a,s['src_in'])) for s in seg)
n=lambda w:re.sub(r'[^\w]','',w['w']).lower()
FILL=re.compile(r'^(e+m*|m+|hm+|eh|a+h?|ha+|jadi|okey|okay|ok|so|err+)$')
N=len(T); drops=[]
def pe(i): return T[i-1]['e'] if i>0 else T[i]['s']-0.3
def ns(i): return T[i+1]['s'] if i+1<N else T[i]['e']+0.3
for i,w in enumerate(T):
    t=n(w)
    if not FILL.match(t): continue
    if t in('ha','haa') and w['w'].strip().endswith('?'): continue   # 'ha?' reaction in story
    # CTC marks only the core of a word; filler tails leak ('jadi'->'ni'). Take the whole gap to the next word.
    a=max(pe(i)+0.06, min(w['s']-0.03, pe(i)+0.25)); b=max(a+0.1, ns(i)-0.04)
    drops.append([a,b,'filler:'+t,i])
i=0
while i<N:
    done=False
    for k in (5,4,3,2,1):
        for gap in (0,1,2):
            j=i+k+gap
            if j+k>N: continue
            a_=[n(x) for x in T[i:i+k]]
            if not all(a_): continue
            if not all(FILL.match(n(x)) for x in T[i+k:j]): continue
            if [n(x) for x in T[j:j+k]]!=a_: continue
            if T[j]['w'].strip().startswith('-') or (gap==0 and T[i+k]['w'].strip().startswith('-')): continue
            if any(x0<=T[i]['s']<=x1 for x0,x1 in [tuple(map(float,x.split('-'))) for x in sys.argv[5:]]): continue
            if k==1 and a_[0] in ('kenapa',): continue
            if kept(T[j]['s'],T[j+k-1]['e']) < 0.6*(T[j+k-1]['e']-T[j]['s']): continue   # 2nd copy already cut -> keep 1st
            s=max(pe(i)+0.02, T[i]['s']-0.04); e=max(s+0.05, T[j]['s']-0.04)
            drops.append([s,e,'ulang:'+' '.join(x['w'].strip() for x in T[i:j+k]),i]); done=True; break
        if done: break
    i+=1
drops=[d for d in drops if kept(d[0],d[1])>0.04]
drops.sort()
for d in drops:
    i=d[3]; print(f"{d[0]:7.2f} {d[1]:7.2f} {d[1]-d[0]:4.2f} {d[2][:38]:38s} |{''.join(x['w'] for x in T[max(0,i-4):i+7])}")
json.dump([[round(d[0],3),round(d[1],3),d[2]] for d in drops],open(sys.argv[4],'w'),ensure_ascii=False)
