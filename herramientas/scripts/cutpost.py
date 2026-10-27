# Plantilla de post con vehículo recortado sobre fondo azul (2160x2700)
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
NAVY=(1,26,93); DEEP=(0,11,46); CREAM=(243,233,210); BURG=(138,44,69); ROSE=(232,169,186); WA=(37,211,102)
K=2; W,H=1080*K,1350*K
F="/usr/share/fonts/opentype/inter/"
LOGO=sys.path[0]+"/logo-white.png"
def font(n,s): return ImageFont.truetype(F+n,int(s*K))

def background():
    y,x=np.mgrid[0:H,0:W].astype(float)
    r=np.sqrt(((x-W/2)/(W*0.75))**2+((y-H*0.52)/(H*0.42))**2)
    t=np.clip(r,0,1)[...,None]
    c0=np.array([16,52,150.]); c1=np.array(NAVY,float); c2=np.array(DEEP,float)
    col=np.where(t<0.55, c0+(c1-c0)*(t/0.55), c1+(c2-c1)*((t-0.55)/0.45))
    return Image.fromarray(col.astype(np.uint8))

def make(cut,out,title,sub,items,area=(350,1060),maxw=980,dy=0):
    im=background().convert("RGBA")
    car=Image.open(cut).convert("RGBA")
    a=np.asarray(car)[...,3]; ys,xs=np.where(a>20)
    car=car.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    top,bot=area[0]*K,area[1]*K
    s=min(maxw*K/car.width,(bot-top)/car.height)
    car=car.resize((int(car.width*s),int(car.height*s)),Image.LANCZOS)
    x=(W-car.width)//2; y=bot-car.height+dy*K
    # sombra
    sh=Image.new("L",(W,H),0); d=ImageDraw.Draw(sh)
    d.ellipse((x+car.width*0.06,y+car.height-40*K,x+car.width*0.94,y+car.height+18*K),fill=150)
    sh=sh.filter(ImageFilter.GaussianBlur(22*K))
    im.paste(Image.new("RGBA",(W,H),(0,0,0,255)),(0,0),sh)
    im.alpha_composite(car,(x,y))
    d=ImageDraw.Draw(im)
    lg=Image.open(LOGO); lw=250*K; lg=lg.resize((lw,int(lg.height*lw/lg.width)),Image.LANCZOS)
    im.alpha_composite(lg,(W-60*K-lw,44*K))
    ts=150
    while d.textlength(title,font=font("Inter-BlackItalic.otf",ts))>W-130*K or ts>128: ts-=4
    d.text((56*K,232*K),title,font=font("Inter-BlackItalic.otf",ts),fill=CREAM,anchor="ls")
    f=font("Inter-Bold.otf",30); tw=d.textlength(sub,font=f)
    d.rounded_rectangle((60*K,258*K,60*K+tw+50*K,314*K),28*K,fill=BURG)
    d.text((85*K,286*K),sub,font=f,fill=CREAM,anchor="lm")
    y0=H-134*K-150*K
    band=Image.new("RGBA",(W,150*K),DEEP+(215,)); im.alpha_composite(band,(0,y0))
    d=ImageDraw.Draw(im)
    cw=W//len(items)
    for i,(b,l) in enumerate(items):
        cx=i*cw+cw//2
        d.text((cx,y0+58*K),b,font=font("Inter-ExtraBold.otf",44),fill=CREAM,anchor="mm")
        d.text((cx,y0+108*K),l,font=font("Inter-Bold.otf",19),fill=ROSE,anchor="mm")
        if i: d.line((i*cw,y0+30*K,i*cw,y0+120*K),fill=BURG,width=3*K)
    d.rectangle((0,H-134*K,W,H-130*K),fill=BURG); d.rectangle((0,H-130*K,W,H),fill=DEEP)
    d.text((60*K,H-73*K),"Guadalajara, Jalisco",font=font("Inter-SemiBold.otf",30),fill=CREAM,anchor="lm")
    btn="ESCRÍBENOS POR WHATSAPP"; fb=font("Inter-Bold.otf",28); bw=d.textlength(btn,font=fb)+60*K
    d.rounded_rectangle((W-60*K-bw,H-108*K,W-60*K,H-38*K),35*K,fill=WA)
    d.text((W-60*K-bw/2,H-73*K),btn,font=fb,fill=DEEP,anchor="mm")
    im=im.convert("RGB"); im.save(out,quality=93)
    im.resize((1080,1350),Image.LANCZOS).save(out.replace(".jpg","_prev.jpg"),quality=90)
