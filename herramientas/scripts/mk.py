import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
NAVY=(1,26,93); DEEP=(0,11,46); CREAM=(243,233,210); BURG=(138,44,69); ROSE=(232,169,186)
W,H=1080,1350
F="/usr/share/fonts/opentype/inter/"
def font(n,s): return ImageFont.truetype(F+n,s)
def make(photo,out,title,sub,items,frac=0.5,tsize=150,xfrac=0.5):
    im=Image.new("RGB",(W,H),NAVY)
    ph=ImageOps.exif_transpose(Image.open(photo)).convert("RGB")
    PH_Y=300; PH_H=H-PH_Y-134
    r=max(W/ph.width,PH_H/ph.height)
    ph=ph.resize((int(ph.width*r),int(ph.height*r)),Image.LANCZOS)
    top=int((ph.height-PH_H)*frac); left=int((ph.width-W)*xfrac)
    im.paste(ph.crop((left,top,left+W,top+PH_H)),(0,PH_Y))
    for i in range(50):
        y=PH_Y+i
        im.paste(Image.blend(im.crop((0,y,W,y+1)),Image.new("RGB",(W,1),NAVY),1-i/50),(0,y))
    if items:
        y0=H-134-150
        im.paste(Image.blend(im.crop((0,y0,W,y0+150)),Image.new("RGB",(W,150),DEEP),0.84),(0,y0))
    d=ImageDraw.Draw(im)
    lg=Image.open("/home/claude/advance-video/public/logo-white.png").convert("RGBA")
    lw=250; lg=lg.resize((lw,int(lg.height*lw/lg.width)),Image.LANCZOS)
    im.paste(lg,(W-60-lw,40),lg)
    while d.textlength(title,font=font("Inter-ExtraBold.otf",tsize))>W-60-250-70: tsize-=4
    d.text((60,36+(150-tsize)//2),title,font=font("Inter-ExtraBold.otf",tsize),fill=CREAM)
    f=font("Inter-Bold.otf",30); tw=d.textlength(sub,font=f)
    d.rounded_rectangle((60,222,60+tw+50,222+56),28,fill=BURG)
    d.text((85,234),sub,font=f,fill=CREAM)
    if items:
        cw=W//len(items); y0=H-134-150
        for i,(b,l) in enumerate(items):
            cx=i*cw+cw//2
            fb=font("Inter-ExtraBold.otf",44); fl=font("Inter-Bold.otf",19)
            d.text((cx-d.textlength(b,font=fb)/2,y0+30),b,font=fb,fill=CREAM)
            d.text((cx-d.textlength(l,font=fl)/2,y0+96),l,font=fl,fill=ROSE)
            if i: d.line((i*cw,y0+30,i*cw,y0+120),fill=BURG,width=3)
    d.rectangle((0,H-134,W,H-130),fill=BURG); d.rectangle((0,H-130,W,H),fill=DEEP)
    d.text((60,H-98),"Guadalajara, Jalisco",font=font("Inter-SemiBold.otf",30),fill=CREAM)
    btn="ESCRÍBENOS POR WHATSAPP"; fb=font("Inter-Bold.otf",28); bw=d.textlength(btn,font=fb)+60
    d.rounded_rectangle((W-60-bw,H-108,W-60,H-38),35,fill=(37,211,102))
    d.text((W-60-bw+30,H-91),btn,font=fb,fill=DEEP)
    im.save(out,quality=92)
