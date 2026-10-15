import numpy as np, cv2, sys, os
from PIL import Image, ImageFilter
from rembg import new_session, remove
P="/home/claude/advance-video/public/"; D="/home/claude/fotos/cargo180/"
s=new_session("isnet-general-use")
def best(k): return D+f"{k}_x4.png" if os.path.exists(D+f"{k}_x4.png") else D+f"{k}.png"
def sharpen(im): return im.filter(ImageFilter.UnsharpMask(1.4,60,2))
for k,out,H in [("hero_clean","c180_hero.jpg",1700),("tilt_clean","c180_tilt.jpg",1600)]:
    im=Image.open(best(k)).convert("RGB"); im=im.resize((int(im.width*H/im.height),H),Image.LANCZOS); sharpen(im).save(P+out,quality=93); print(out,im.size,best(k))
# vehicle cutout from hero
im=Image.open(best("hero_clean")).convert("RGB")
m=remove(im,session=s,only_mask=True); a=np.array(m).astype(np.float32)/255
a=np.clip((a-0.3)/0.5,0,1); b=(a>0.5).astype(np.uint8); n,l,st,_=cv2.connectedComponentsWithStats(b)
keep=np.isin(l,[1+np.argmax(st[1:,4])]).astype(np.uint8); keep=cv2.dilate(keep,np.ones((9,9),np.uint8)); a=a*keep
rgba=np.dstack([np.array(im),(a*255).astype(np.uint8)]); ys,xs=np.where(a>0.05)
c=Image.fromarray(rgba).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); c.thumbnail((1800,1800),Image.LANCZOS); c.save(P+"c180_cut.png"); print("cut",c.size)
for col in ["azul","gris","rojo"]:
    im=Image.open(best("col_"+col)).convert("RGB")
    if im.width<800: im=im.resize((im.width*4,im.height*4),Image.LANCZOS)
    m=np.array(remove(im,session=s,only_mask=True)).astype(np.float32)/255
    # white background key as extra safety
    g=np.array(im).astype(np.float32); white=(g.min(2)>235)
    a=np.where(white,0,m); a=np.clip((a-0.3)/0.5,0,1)
    b=(a>0.5).astype(np.uint8); n,l,st,_=cv2.connectedComponentsWithStats(b)
    keep=np.zeros_like(b)
    for i in range(1,n):
        if st[i,4]>0.02*b.sum(): keep[l==i]=1
    a=a*cv2.dilate(keep,np.ones((7,7),np.uint8))
    rgba=np.dstack([np.array(im),(a*255).astype(np.uint8)]); ys,xs=np.where(a>0.05)
    c=Image.fromarray(rgba).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); c=c.resize((c.width,c.height)); 
    al=c.getchannel("A"); c2=sharpen(c.convert("RGB")); c2.putalpha(al); c2.save(P+f"c180_{col}.png"); print(col,c2.size,best("col_"+col))
