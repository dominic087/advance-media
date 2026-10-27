"""Historia de una sola foto "Entregas Advance" (1080x1920, imagen).
Uso: python3 historia_foto.py
Editar FOTOS: (foto, recorte x0,y0,x1,y1 en fracción, lugar de entrega, salida).
El recorte deja fuera las caras de los clientes."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
NAVY=(1,26,93); DEEP=(0,11,46); CREAM=(243,233,210); BURG=(138,44,69); ROSE=(232,169,186); GREEN=(37,211,102)
W,H=1080,1920
F="/usr/share/fonts/opentype/inter/"
HERE=os.path.dirname(os.path.abspath(__file__))
LOGO=os.path.join(HERE,"..","logo-white.png")
FOT="/mnt/project-files/fotos/entregas/"
OUT="/mnt/project-files/piezas/entregas/"
FOTOS=[
    ("20260516_195723.jpg",(0,0.25,1,1),"Tesistán","entrega-1.jpg"),
    ("20260610_121950.jpg",(0,0.29,1,1),"Huentitán","entrega-2.jpg"),
    ("20260509_100328.jpg",(0,0,1,1),"...","entrega-3.jpg"),
    ("WA0080.jpg",(0,0.42,0.8,1),"...","entrega-4.jpg"),
    ("20260711_141926.jpg",(0,0.12,1,1),"...","entrega-5.jpg"),
]
def font(n,s): return ImageFont.truetype(F+n,s)

def make(name,box,lugar,out):
    ph=ImageOps.exif_transpose(Image.open(FOT+name)).convert("RGB")
    x0,y0,x1,y1=box; ph=ph.crop((int(x0*ph.width),int(y0*ph.height),int(x1*ph.width),int(y1*ph.height)))
    r=max(W/ph.width,H/ph.height)
    bg=ph.resize((int(ph.width*r)+1,int(ph.height*r)+1)).filter(ImageFilter.GaussianBlur(40))
    bg=bg.crop(((bg.width-W)//2,(bg.height-H)//2,(bg.width-W)//2+W,(bg.height-H)//2+H))
    im=Image.blend(bg,Image.new("RGB",(W,H),NAVY),0.55)
    fg=ph.resize((W,int(ph.height*W/ph.width)),Image.LANCZOS)
    MAXH=1000  # la foto va entre el logo y el texto
    if fg.height>MAXH: fg=fg.crop((0,(fg.height-MAXH)//2,W,(fg.height-MAXH)//2+MAXH))
    top=440+(MAXH-fg.height)//2; im.paste(fg,(0,top))
    d=ImageDraw.Draw(im)
    lg=Image.open(LOGO).convert("RGBA"); LW=420; lg=lg.resize((LW,int(lg.height*LW/lg.width)),Image.LANCZOS)
    im.paste(lg,((W-LW)//2,200),lg)
    f=font("Inter-Bold.otf",30); tag="ENTREGAS ADVANCE"; tw=d.textlength(tag,font=f)
    d.rounded_rectangle(((W-tw)//2-30,350,(W+tw)//2+30,404),27,fill=BURG); d.text(((W-tw)//2,360),tag,font=f,fill=CREAM)
    yb=1480
    fl=font("Inter-BlackItalic.otf",76); txt=("ENTREGA EN "+lugar.upper()) if not lugar.lower().startswith("entrega") else lugar.upper()
    while d.textlength(txt,font=fl)>W-120: fl=font("Inter-BlackItalic.otf",fl.size-4)
    d.text(((W-d.textlength(txt,font=fl))/2,yb),txt,font=fl,fill=CREAM)
    s="Gracias por su confianza"; fs=font("Inter-SemiBold.otf",38)
    d.text(((W-d.textlength(s,font=fs))/2,yb+fl.size+24),s,font=fs,fill=ROSE)
    btn="ESCRÍBENOS POR WHATSAPP"; fb=font("Inter-ExtraBold.otf",36); bw=d.textlength(btn,font=fb)+80
    yw=1650
    d.rounded_rectangle(((W-bw)/2,yw,(W+bw)/2,yw+86),43,fill=GREEN); d.text(((W-bw)/2+40,yw+22),btn,font=fb,fill=DEEP)
    os.makedirs(OUT,exist_ok=True); im.save(OUT+out,quality=92)  # sin EXIF/GPS
    return im
if __name__=="__main__":
    import sys
    for f in FOTOS:
        if len(sys.argv)<2 or f[3] in sys.argv[1:]: make(*f); print("ok",f[3])
