"""Historia semanal "Entregas Advance" (1080x1920, 30 fps) con fotos de clientes.
Uso: python3 historia_entregas.py salida.mp4 [--preview carpeta]
Editar SHOTS para cada semana: (foto, texto, foco_x, foco_y)."""
import os, sys, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
NAVY=(1,26,93); DEEP=(0,11,46); CREAM=(243,233,210); BURG=(138,44,69); ROSE=(232,169,186); GREEN=(37,211,102)
W,H,FPS=1080,1920,30
F="/usr/share/fonts/opentype/inter/"
HERE=os.path.dirname(os.path.abspath(__file__))
LOGO=os.path.join(HERE,"..","logo-white.png")
FOT="/mnt/project-files/fotos/entregas/"
SHOTS=[  # (foto, texto, foco x, foco y)  foco = parte de la foto que se queda al centro
    ("20260516_195723.jpg", None, 0.55, 0.0),
    ("20260610_121950.jpg", "Un cliente más estrenando su triciclo", 0.6, 0.6),
    ("20260509_100328.jpg", "Unidades listas para entregar", 0.5, 0.55),
    ("WA0080.jpg", "¡Felicidades por su nueva unidad!", 0.5, 0.6),
    ("20260711_141926.jpg", "Gracias por elegirnos", 0.45, 0.55),
]
SEG=2.5; FADE=0.4; OUTRO=3.0
def font(n,s): return ImageFont.truetype(F+n,s)

def load(name, fx, fy, zoom=1.12):
    ph=ImageOps.exif_transpose(Image.open(FOT+name)).convert("RGB")
    r=max(W*zoom/ph.width,H*zoom/ph.height)
    ph=ph.resize((int(ph.width*r),int(ph.height*r)),Image.LANCZOS)
    return ph,fx,fy

def kb(ph,fx,fy,t,W=W,H=H):  # Ken Burns: zoom lento hacia dentro
    s=1.0-0.10*t
    cw=int(ph.width*s); ch=int(cw*H/W)
    if ch>ph.height: ch=ph.height; cw=int(ch*W/H)
    cx=int(fx*ph.width); cy=int(fy*ph.height)
    l=min(max(cx-cw//2,0),ph.width-cw); tp=min(max(cy-ch//2,0),ph.height-ch)
    return ph.crop((l,tp,l+cw,tp+ch)).resize((W,H),Image.BILINEAR)

def grad(im, top=True, h=520, a=0.85):
    ov=Image.new("RGB",(W,h),DEEP)
    m=Image.linear_gradient("L").resize((W,h))
    if top: m=m.transpose(Image.FLIP_TOP_BOTTOM)
    m=m.point(lambda v:int(v*a))
    y=0 if top else H-h
    im.paste(ov,(0,y),m)

logo=Image.open(LOGO).convert("RGBA"); LW=420
logo=logo.resize((LW,int(logo.height*LW/logo.width)),Image.LANCZOS)

def chrome(im):
    grad(im,True,560,0.8); grad(im,False,820,0.93)
    im.paste(logo,((W-LW)//2,215),logo)
    d=ImageDraw.Draw(im)
    f=font("Inter-Bold.otf",30); tag="ENTREGAS ADVANCE"; tw=d.textlength(tag,font=f)
    d.rounded_rectangle(((W-tw)//2-30,360,(W+tw)//2+30,414),27,fill=BURG)
    d.text(((W-tw)//2,370),tag,font=f,fill=CREAM)
    return d

def wrap(d,text,f,maxw):
    words=text.split(); lines=[""]
    for w in words:
        t=(lines[-1]+" "+w).strip()
        if d.textlength(t,font=f)<=maxw: lines[-1]=t
        else: lines.append(w)
    return lines

def caption(im,text):
    d=ImageDraw.Draw(im); f=font("Inter-ExtraBold.otf",72)
    lines=wrap(d,text,f,W-160); y=1500-len(lines)*88
    for ln in lines:
        d.text(((W-d.textlength(ln,font=f))/2,y),ln,font=f,fill=CREAM); y+=88

def intro_text(im):
    d=ImageDraw.Draw(im)
    f=font("Inter-BlackItalic.otf",132)
    for i,ln in enumerate(["ENTREGAS","DE LA SEMANA"]):
        ff=f if i==0 else font("Inter-BlackItalic.otf",88)
        d.text(((W-d.textlength(ln,font=ff))/2,1230+i*150),ln,font=ff,fill=CREAM)
    s="Clientes que ya ruedan con Advance"; fs=font("Inter-SemiBold.otf",40)
    d.text(((W-d.textlength(s,font=fs))/2,1500),s,font=fs,fill=ROSE)

def outro(bgph):
    im=bgph.filter(ImageFilter.GaussianBlur(24))
    im=Image.blend(im,Image.new("RGB",(W,H),NAVY),0.82)
    im.paste(logo,((W-LW)//2,300),logo)
    d=ImageDraw.Draw(im)
    for i,(ln,sz) in enumerate([("GRACIAS POR",104),("SU CONFIANZA",104)]):
        ff=font("Inter-BlackItalic.otf",sz); d.text(((W-d.textlength(ln,font=ff))/2,700+i*130),ln,font=ff,fill=CREAM)
    s="¿El siguiente eres tú?"; fs=font("Inter-Bold.otf",54)
    d.text(((W-d.textlength(s,font=fs))/2,1010),s,font=fs,fill=ROSE)
    btn="ESCRÍBENOS POR WHATSAPP"; fb=font("Inter-ExtraBold.otf",44); bw=d.textlength(btn,font=fb)+100
    d.rounded_rectangle(((W-bw)/2,1180,(W+bw)/2,1290),55,fill=GREEN)
    d.text(((W-bw)/2+50,1210),btn,font=fb,fill=DEEP)
    s="Guadalajara, Jalisco"; fs=font("Inter-SemiBold.otf",40)
    d.text(((W-d.textlength(s,font=fs))/2,1340),s,font=fs,fill=CREAM)
    return im

def main(out, prev=None):
    shots=[load(n,fx,fy) for n,_,fx,fy in SHOTS]
    texts=[t for _,t,_,_ in SHOTS]
    out_frame=outro(kb(*shots[0],0.5))
    n_main=int(SEG*FPS*len(SHOTS)); n_out=int(OUTRO*FPS); N=n_main+n_out; nf=int(FADE*FPS); seg=int(SEG*FPS)
    def shot_frame(i,k):
        if texts[i] is None:  # portada: foto debajo del logo para no tapar caras
            im=Image.new("RGB",(W,H),NAVY); PY=440
            ph=kb(*shots[i],k/(seg+nf),W=W,H=H-PY); im.paste(ph,(0,PY))
            band=Image.new("RGB",(W,120),NAVY); m=Image.linear_gradient("L").resize((W,120)).transpose(Image.FLIP_TOP_BOTTOM)
            im.paste(band,(0,PY),m); chrome(im); intro_text(im); return im
        im=kb(*shots[i],k/(seg+nf)); chrome(im)
        if False: pass
        else: caption(im,texts[i])
        return im
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
        "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","128k","-movflags","+faststart","-map_metadata","-1",out],stdin=subprocess.PIPE)
    for f in range(N):
        if f<n_main:
            i,k=divmod(f,seg); im=shot_frame(i,k)
            if k>=seg-nf:
                nxt=shot_frame(i+1,k-(seg-nf)) if i+1<len(SHOTS) else out_frame
                im=Image.blend(im,nxt,(k-(seg-nf)+1)/nf)
        else: im=out_frame
        if prev and (f%seg==seg//2 or f==N-1): im.save(f"{prev}/f{f:04d}.jpg",quality=85)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait(); print("ok",out,N/FPS,"s")
if __name__=="__main__":
    a=sys.argv; main(a[1], a[3] if len(a)>3 and a[2]=="--preview" else None)
