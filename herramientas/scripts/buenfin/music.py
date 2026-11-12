import numpy as np, wave
SR=44100; BPM=104; B=60/BPM; DUR=20.8
N=int(SR*DUR); out=np.zeros((N,2))
t_all=np.arange(N)/SR
def add(sig,start,pan=0.0,g=1.0):
    i=int(start*SR); n=min(len(sig),N-i)
    if n<=0: return
    out[i:i+n,0]+=sig[:n]*g*(1-pan); out[i:i+n,1]+=sig[:n]*g*(1+pan)
def kick():
    t=np.arange(int(.35*SR))/SR; f=50+90*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)
def clap():
    t=np.arange(int(.25*SR))/SR; n=np.random.randn(len(t))
    env=np.exp(-t*18)+0.5*np.exp(-((t-.012)*300)**2)
    return n*env*0.5
def hat(o=False):
    t=np.arange(int((.18 if o else .05)*SR))/SR; n=np.random.randn(len(t)); n=np.diff(n,prepend=0)
    return n*np.exp(-t*(15 if o else 80))*0.25
def note(m): return 440*2**((m-69)/12)
def saw(f,d,amp=.2):
    t=np.arange(int(d*SR))/SR; s=sum(np.sin(2*np.pi*f*k*t)/k for k in range(1,9))
    env=np.minimum(1,t/.01)*np.exp(-t*2.5); return s*env*amp
def pluck(f,d):
    t=np.arange(int(d*SR))/SR; s=np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*2*f*t)+.25*np.sin(2*np.pi*3*f*t)
    return s*np.exp(-t*9)*0.18
np.random.seed(3)
# progression per bar (4 beats): Am F C G  (bass midi roots)
prog=[(45,[57,60,64]),(41,[57,60,65]),(48,[55,60,64]),(43,[55,59,62])]
melody=[76,72,74,76, 77,76,72,69, 72,74,76,79, 79,77,74,71]
beats=int(DUR/B)+1
for b in range(beats):
    tb=b*B; bar=(b//4)%4; root,ch=prog[bar]
    intro = b<2
    add(kick(),tb,g=0.9 if not intro else 0.6)
    if b%2==1 and not intro: add(clap(),tb,g=0.8)
    for h in (0,.5):
        add(hat(h==.5),tb+h*B,pan=.3,g=1)
    if not intro:
        # bass offbeat pump
        add(saw(note(root),B*0.45,.22),tb); add(saw(note(root+12),B*0.4,.12),tb+B/2)
        for m in ch: add(pluck(note(m+12),B*.9),tb+B/2,pan=-.2,g=.8)
        add(pluck(note(melody[b%16]),B*.8),tb,pan=.2,g=1.1)
    else:
        for m in ch: add(pluck(note(m+12),B*.9),tb,g=.6)
# riser into each scene? small sweep at start
out/=np.max(np.abs(out))*1.05
fade=np.ones(N); fs=int(2.3*SR); fade[-fs:]=np.linspace(1,0,fs)**1.5
fi=int(.05*SR); fade[:fi]=np.linspace(0,1,fi)
out*=fade[:,None]
pcm=(out*32767).astype(np.int16)
w=wave.open(__import__('sys').argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
