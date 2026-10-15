import numpy as np, cv2
from PIL import Image
m=np.load("mask2.npy").astype(np.uint8)
src=np.array(Image.open('/root/.claude/uploads/9d59e278-dfdb-58bd-863e-a6b91bb90443/c9bc7382-image.jpg').convert("RGB"))
hsv=cv2.cvtColor(src,cv2.COLOR_RGB2HSV).astype(np.float32)
h=hsv[...,0]*2; s=hsv[...,1]/255; v=hsv[...,2]/255
bggreen=(h>60)&(h<175)&(s>0.15)
boxes={"rojo":(48,1479,434,1859),"negro":(954,1476,1380,1863),"verde":(503,1464,905,1861),"hero":(600,419,1407,1410)}
for k,(x0,y0,x1,y1) in boxes.items():
    M=m[y0:y1,x0:x1].copy()
    n,l,st,_=cv2.connectedComponentsWithStats(M); keep=np.zeros_like(M)
    for i in range(1,n):
        if st[i,4]>3000: keep[l==i]=1
    M=keep
    G=bggreen[y0:y1,x0:x1]; V=v[y0:y1,x0:x1]
    if True:
        R=61 if k=="hero" else 121
        near=cv2.dilate(M,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(R,R)))
        # don't extend downward into the floor: limit to rows above the lowest 12% of the vehicle
        ys=np.where(M.any(1))[0]; cut=int(ys.min()+0.80*(ys.max()-ys.min()))
        near[cut:]=0
        Gb=G&(V<0.6); add=((~Gb)&(near>0)).astype(np.uint8)
        add=cv2.morphologyEx(add,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
        U=np.maximum(M,add)
        n,l,st,_=cv2.connectedComponentsWithStats(U); lab=np.unique(l[M>0]); lab=lab[lab>0]
        U=np.isin(l,lab).astype(np.uint8)
        # holes: visible green wall inside the vehicle (not dark tyres)
        hole=(G&(V>0.40)&(V<0.6)&(U>0)).astype(np.uint8)
        n,l,st,_=cv2.connectedComponentsWithStats(hole); hb=np.zeros_like(hole)
        for i in range(1,n):
            if st[i,4]>120: hb[l==i]=1
        U[cv2.dilate(hb,np.ones((3,3),np.uint8))>0]=0
    if False:
        hole=(G&(V<0.45)&(V>0.24)&(s[y0:y1,x0:x1]>0.25)&(U>0)).astype(np.uint8)
        n,l,st,_=cv2.connectedComponentsWithStats(hole); hb=np.zeros_like(hole)
        for i in range(1,n):
            if st[i,4]>200: hb[l==i]=1
        U[cv2.dilate(hb,np.ones((3,3),np.uint8))>0]=0
    # fill tiny pinholes, remove specks
    U=cv2.morphologyEx(U,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    n,l,st,_=cv2.connectedComponentsWithStats(U); out=np.zeros_like(U)
    for i in range(1,n):
        if st[i,4]>60: out[l==i]=1
    np.save(f"m3_{k}.npy",out)
# preview
prev=Image.new("RGB",(1700,1000),(0,0,60)); xo=0
for k in ["rojo","negro","verde"]:
    x0,y0,x1,y1=boxes[k]; c=Image.fromarray(src[y0:y1,x0:x1]); a=Image.fromarray(np.load(f"m3_{k}.npy")*255)
    bg=Image.new("RGB",c.size,(255,0,255)); bg.paste(c,(0,0),a); prev.paste(bg,(xo,0)); xo+=c.width+20
x0,y0,x1,y1=boxes["hero"]; c=Image.fromarray(src[y0:y1,x0:x1]); a=Image.fromarray(np.load("m3_hero.npy")*255)
bg=Image.new("RGB",c.size,(255,0,255)); bg.paste(c,(0,0),a); bg=bg.resize((c.width*580//c.height,580)); prev.paste(bg,(0,410))
prev.save("/tmp/claude-0/-home-claude-advance-media/9d59e278-dfdb-58bd-863e-a6b91bb90443/scratchpad/m3.png")
