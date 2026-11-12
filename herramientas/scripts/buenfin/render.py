import sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import json
TM=json.load(open(sys.argv[1]+'/timing.json'))
W,H,FPS=1080,1920,30; DUR=TM['dur']; NF=TM['S'][-1]
BEAT=60/104*FPS  # 17.31 frames
NAVY=(1,26,93); DEEP=(0,11,46); CREAM=(243,233,210); VINO=(138,44,69); ROSA=(232,169,186); GREEN=(37,211,102); WHITE=(255,255,255)
FD='/usr/share/fonts/opentype/inter/'
def F(sz,st='BlackItalic'): return ImageFont.truetype(FD+f'Inter-{st}.otf',sz)
D=sys.argv[1]; PF='/mnt/project-files/fotos/'
logo=Image.open(D+'/logo.png').convert('RGBA')
def clamp(x,a=0,b=1): return max(a,min(b,x))
def eo(x): x=clamp(x); return 1-(1-x)**3
def eback(x,s=1.9): x=clamp(x); x-=1; return x*x*((s+1)*x+s)+1
def ebounce(x):
    x=clamp(x); n,d=7.5625,2.75
    if x<1/d: return n*x*x
    if x<2/d: x-=1.5/d; return n*x*x+.75
    if x<2.5/d: x-=2.25/d; return n*x*x+.9375
    x-=2.625/d; return n*x*x+.984375
# background
bg=Image.new('RGB',(W,H)); bd=ImageDraw.Draw(bg)
for y in range(H):
    k=y/H; c=tuple(int(DEEP[i]+(NAVY[i]-DEEP[i])*(1-abs(k-.45)*1.6 if abs(k-.45)<.6 else 0.04)) for i in range(3)); bd.line([(0,y),(W,y)],fill=c)
def background(f):
    im=bg.copy(); ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    off=(f*3)%160
    for i in range(-3,20):
        x=i*160+off
        d.polygon([(x,0),(x+60,0),(x+60-700,H),(x-700,H)],fill=(255,255,255,10))
    im.paste(ov,(0,0),ov); return im
def tsize(txt,font):
    b=font.getbbox(txt); return b[2]-b[0],b[3]-b[1],b
def text_img(txt,font,fill,stroke=0,sfill=None):
    w,h,b=tsize(txt,font); pad=20+stroke
    im=Image.new('RGBA',(w+2*pad,h+2*pad),(0,0,0,0))
    ImageDraw.Draw(im).text((pad-b[0],pad-b[1]),txt,font=font,fill=fill,stroke_width=stroke,stroke_fill=sfill)
    return im
def paste_c(base,im,cx,cy,scale=1.0,alpha=1.0,rot=0):
    if scale<=0.01 or alpha<=0.01: return
    if scale!=1: im=im.resize((max(1,int(im.width*scale)),max(1,int(im.height*scale))),Image.BICUBIC)
    if rot: im=im.rotate(rot,resample=Image.BICUBIC,expand=True)
    if alpha<1:
        a=im.getchannel('A').point(lambda v:int(v*alpha)); im=im.copy(); im.putalpha(a)
    base.paste(im,(int(cx-im.width/2),int(cy-im.height/2)),im)
def fit_text(txt,maxw,size,st='BlackItalic'):
    while size>20:
        f=F(size,st)
        if tsize(txt,f)[0]<=maxw: return f
        size-=4
    return F(size,st)
_cache={}
def T(txt,maxw,size,fill,st='BlackItalic',stroke=0,sfill=None):
    k=(txt,maxw,size,fill,st,stroke,sfill)
    if k not in _cache: _cache[k]=text_img(txt,fit_text(txt,maxw,size,st),fill,stroke,sfill)
    return _cache[k]
def echo(base,txt,cy,f0,f,maxw=980,size=170,col=CREAM):
    """Big word with repeated outline copies above/below that drift."""
    main=T(txt,maxw,size,col)
    ghost=T(txt,maxw,size,(0,0,0,0),stroke=3,sfill=ROSA)
    p=(f-f0)
    h=main.height-30
    for k in (3,2,1):
        sp=eo(p/12)
        for s in (-1,1):
            a=(0.55-0.15*k)*clamp(p/8)
            paste_c(base,ghost,W/2+s*k*6,cy+s*k*h*0.78*sp,1,a)
    pulse=1+0.06*max(0,1-((f%BEAT)/5))
    paste_c(base,main,W/2,cy,eback(p/10)*pulse)
def pulse_scale(f): return 1+0.05*max(0,1-((f%BEAT)/5))
def rrect_mask(w,h,r):
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],r,fill=255); return m
def pill(txt,font,fg,bgc,padx=50,pady=26):
    w,h,b=tsize(txt,font); im=Image.new('RGBA',(w+2*padx,h+2*pady),(0,0,0,0))
    d=ImageDraw.Draw(im); d.rounded_rectangle([0,0,im.width-1,im.height-1],im.height//2,fill=bgc)
    d.text((padx-b[0],pady-b[1]),txt,font=font,fill=fg); return im
# ---- photos
def photo_card(path,crop_box_frac=None,cw=900,ch=1000):
    im=ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    r=cw/ch; w,h=im.size
    if crop_box_frac: 
        l,t,rr,bb=crop_box_frac; im=im.crop((int(l*w),int(t*h),int(rr*w),int(bb*h))); w,h=im.size
    if w/h>r: nw=int(h*r); im=im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
    else: nh=int(w/r); im=im.crop((0,(h-nh)//2,w,(h-nh)//2+nh))
    return im.resize((int(cw*1.15),int(ch*1.15)),Image.LANCZOS)
cards={
 'FAMILY':photo_card(PF+'buenfin/family/2.jpg'),
 'FAMILY PRO':photo_card(PF+'semana2/fq1.jpg'),
 'FAMILY PLUS CON TOLDO':photo_card(PF+'semana3/toldo/181032.jpg'),
}
CW,CH=900,1000
def draw_card(base,src,p,fl):
    # p progress frames into scene; ken burns zoom
    z=1.0+0.08*clamp(fl)  # 1.0->1.08 of crop
    sw,sh=src.size; cw,ch=int(sw/1.15/z*1.0),int(sh/1.15/z)
    cw=int(CW*1.15/ (1.0+0.15*(1-clamp(fl)))); ch=int(cw*CH/CW)
    x=(sw-cw)//2; y=(sh-ch)//2
    im=src.crop((x,y,x+cw,y+ch)).resize((CW,CH),Image.BILINEAR)
    card=Image.new('RGBA',(CW+24,CH+24),(0,0,0,0))
    ImageDraw.Draw(card).rounded_rectangle([0,0,CW+23,CH+23],46,fill=CREAM)
    card.paste(im,(12,12),rrect_mask(CW,CH,36))
    sl=eback(p/11,1.4)
    cx=W/2+(1-sl)*900
    rot=(1-eo(p/14))*-6
    paste_c(base,card,cx,860,1.0,1.0,rot)
# ---- icons
def icon_helmet(sz):
    im=Image.new('RGBA',(sz,sz),(0,0,0,0)); d=ImageDraw.Draw(im); s=sz/100
    d.pieslice([12*s,18*s,88*s,94*s],180,360,fill=NAVY)
    d.rectangle([12*s,55*s,88*s,64*s],fill=NAVY)
    d.rounded_rectangle([46*s,46*s,92*s,60*s],5*s,fill=VINO)  # visor
    d.line([(30*s,30*s),(30*s,52*s)],fill=CREAM,width=int(4*s)); d.line([(50*s,22*s),(50*s,42*s)],fill=CREAM,width=int(4*s))
    d.line([(14*s,64*s),(28*s,80*s)],fill=NAVY,width=int(5*s))
    return im
def icon_cover(sz):
    im=Image.new('RGBA',(sz,sz),(0,0,0,0)); d=ImageDraw.Draw(im); s=sz/100
    d.ellipse([66*s,4*s,90*s,28*s],fill=(240,170,40))  # sun
    for a in range(0,360,45):
        r=math.radians(a); d.line([(78*s+15*s*math.cos(r),16*s+15*s*math.sin(r)),(78*s+20*s*math.cos(r),16*s+20*s*math.sin(r))],fill=(240,170,40),width=int(3*s))
    for x,y in ((14,8),(26,16),(38,6),(50,14)): d.line([(x*s,y*s),((x-3)*s,(y+9)*s)],fill=(70,140,230),width=int(3.5*s))
    # cover draped over a tricycle silhouette
    d.chord([12*s,34*s,88*s,104*s],180,360,fill=NAVY)
    d.rectangle([12*s,68*s,88*s,78*s],fill=NAVY)
    d.polygon([(12*s,78*s),(18*s,84*s),(26*s,78*s),(34*s,84*s),(42*s,78*s),(50*s,84*s),(58*s,78*s),(66*s,84*s),(74*s,78*s),(82*s,84*s),(88*s,78*s)],fill=NAVY)
    for cx in (24,76): d.ellipse([(cx-8)*s,82*s,(cx+8)*s,98*s],fill=(30,30,30)); d.ellipse([(cx-3)*s,87*s,(cx+3)*s,93*s],fill=CREAM)
    return im
def icon_gift(sz):
    im=Image.new('RGBA',(sz,sz),(0,0,0,0)); d=ImageDraw.Draw(im); s=sz/100
    d.rounded_rectangle([14*s,40*s,86*s,92*s],6*s,fill=VINO); d.rounded_rectangle([8*s,28*s,92*s,44*s],5*s,fill=ROSA)
    d.rectangle([45*s,28*s,55*s,92*s],fill=CREAM)
    d.ellipse([26*s,8*s,50*s,30*s],outline=CREAM,width=int(6*s)); d.ellipse([50*s,8*s,74*s,30*s],outline=CREAM,width=int(6*s))
    return im
def circle_icon(icon,sz):
    im=Image.new('RGBA',(sz,sz),(0,0,0,0)); ImageDraw.Draw(im).ellipse([0,0,sz-1,sz-1],fill=CREAM)
    ic=icon(int(sz*.68)); im.paste(ic,((sz-ic.width)//2,(sz-ic.height)//2),ic); return im
HELM=circle_icon(icon_helmet,330); COVER=circle_icon(icon_cover,330); GIFT=icon_gift(260)
def wa_icon(sz):
    im=Image.new('RGBA',(sz,sz),(0,0,0,0)); d=ImageDraw.Draw(im); s=sz/100
    d.ellipse([6*s,6*s,94*s,94*s],outline=WHITE,width=int(8*s)); d.polygon([(10*s,96*s),(18*s,70*s),(34*s,86*s)],fill=WHITE)
    d.rounded_rectangle([34*s,28*s,48*s,44*s],4*s,fill=WHITE); d.rounded_rectangle([54*s,58*s,72*s,72*s],4*s,fill=WHITE)
    d.line([(40*s,40*s),(62*s,64*s)],fill=WHITE,width=int(10*s)); return im
# ---- calendar
def calendar(sz_w=760):
    w=sz_w; h=int(w*0.86); im=Image.new('RGBA',(w,h+30),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,30,w-1,h+29],48,fill=CREAM)
    d.rounded_rectangle([0,30,w-1,210],48,fill=VINO); d.rectangle([0,150,w-1,210],fill=VINO)
    for x in (w*.25,w*.75): d.rounded_rectangle([x-18,0,x+18,90],18,fill=ROSA)
    f=F(70); tw,th,b=tsize('NOVIEMBRE',f); d.text(((w-tw)/2-b[0],120-th/2-b[1]),'NOVIEMBRE',font=f,fill=CREAM)
    f=fit_text('BUEN FIN',w-80,190); tw,th,b=tsize('BUEN FIN',f); d.text(((w-tw)/2-b[0],330-th/2-b[1]),'BUEN FIN',font=f,fill=NAVY)
    fd=F(54,'Black'); n=5; cw=(w-80)/n
    for i,day in enumerate(range(12,17)):
        cx=40+cw*i+cw/2; cy=h-90
        d.ellipse([cx-58,cy-58,cx+58,cy+58],fill=NAVY)
        s=str(day); tw,th,b=tsize(s,fd); d.text((cx-tw/2-b[0],cy-th/2-b[1]),s,font=fd,fill=CREAM)
    return im
_bf=Image.open(D+'/buenfin_cal.png').convert('RGBA'); CAL=_bf.resize((780,int(_bf.height*780/_bf.width)),Image.LANCZOS)
# ---- fixed elements
LOGO_S=logo.resize((420,int(146*420/584)),Image.LANCZOS)
DATEBAR=pill('DEL 12 AL 16 DE NOVIEMBRE',F(54),CREAM,VINO,56,28)
FINE=text_img('Promoción válida del 12 al 16 de noviembre o hasta agotar existencias.',F(28,'SemiBold'),CREAM)
# scene boundaries (frames)
S=TM['S']
def frame(f):
    im=background(f).convert('RGBA')
    sc=max(i for i in range(8) if f>=S[i]); p=f-S[sc]; L=S[sc+1]-S[sc]
    showbar=sc not in (2,)
    if sc==0:
        cp=ebounce(p/22); paste_c(im,CAL,W/2,-500+(800+500)*cp,1,1,(1-eo(p/22))*8)
        if p>=26: echo(im,'PREPÁRATE',1330,26,f,size=180)
    elif sc==1:
        a=eback(p/10,1.5); paste_c(im,T('COMPRA',980,190,CREAM),W/2-(1-a)*1100,560,pulse_scale(f))
        a=eback((p-5)/10,1.5); paste_c(im,T('TU UNIDAD',980,170,ROSA),W/2+(1-a)*1100,760,pulse_scale(f))
        if p>=BEAT*2-4:
            q=p-(BEAT*2-4)
            paste_c(im,T('Y LLÉVATE',980,130,CREAM),W/2,960,eback(q/9))
            paste_c(im,T('UN REGALO',980,170,CREAM,stroke=0),W/2,1110,eback((q-3)/9)*pulse_scale(f))
            paste_c(im,GIFT,W/2,1340,eback((q-6)/10)*(1+0.08*math.sin(p/3)),1,6*math.sin(p/4))
    elif sc==2:
        echo(im,'¡APROVECHA!',640,S[2],f,size=170)
        q=p-8; a=eback(q/10)
        paste_c(im,T('DEL 12 AL 16',980,170,CREAM),W/2,1000,a*pulse_scale(f))
        paste_c(im,T('DE NOVIEMBRE',980,140,ROSA),W/2,1190,eback((q-4)/10))
    elif sc in (3,4,5):
        name=['FAMILY','FAMILY PRO','FAMILY PLUS CON TOLDO'][sc-3]
        # echo name behind card
        g=T(name,1000,220 if sc<5 else 150,(0,0,0,0),stroke=3,sfill=ROSA)
        for k in range(-3,4):
            paste_c(im,g,W/2+((f*4)%120)-60+k*0,860+k*300,1,0.25*clamp(p/6))
        draw_card(im,cards[name],p,p/L)
        paste_c(im,T('NUESTROS MODELOS',900,64,ROSA),W/2,300,eo(p/8) if sc==3 else 1)
        spd={'FAMILY':'35 KM/H','FAMILY PRO':'40 KM/H','FAMILY PLUS CON TOLDO':'45 KM/H'}[name]
        paste_c(im,pill(spd,F(58),CREAM,VINO,36,20),W/2+300,420,eback((p-10)/9),1,-6)
        lab=pill(name,fit_text(name,860,92),NAVY,CREAM,48,22)
        paste_c(im,lab,W/2,1415,eback((p-6)/9)*pulse_scale(f))
    elif sc==6:
        paste_c(im,T('TE REGALAMOS:',980,140,CREAM),W/2,400,eback(p/9)*pulse_scale(f))
        a=eback((p-5)/11); paste_c(im,HELM,W/2-250,700,a)
        b=eback((p-10)/11); paste_c(im,COVER,W/2+250,700,b)
        paste_c(im,T('o',200,110,ROSA),W/2,700,eback((p-8)/8))
        paste_c(im,T('CASCO DE',480,62,CREAM),W/2-250,925,a); paste_c(im,T('PROTECCIÓN',480,62,CREAM),W/2-250,995,a)
        paste_c(im,T('FUNDA PARA',480,62,CREAM),W/2+250,925,b); paste_c(im,T('LLUVIA Y SOL',480,62,CREAM),W/2+250,995,b)
        if p>=BEAT*2: paste_c(im,pill('ELIGE EL QUE PREFIERAS',F(60),NAVY,ROSA,48,24),W/2,1200,eback((p-BEAT*2)/9)*pulse_scale(f))
    elif sc==7:
        lg=logo.resize((760,int(146*760/584)),Image.LANCZOS) if 'LG' not in _cache else _cache['LG']; _cache['LG']=lg
        paste_c(im,lg,W/2,430,eback(p/10))
        wa=Image.new('RGBA',(880,170),(0,0,0,0)); d=ImageDraw.Draw(wa); d.rounded_rectangle([0,0,879,169],85,fill=GREEN)
        ic=wa_icon(96); wa.paste(ic,(48,37),ic)
        fn=F(56,'Black'); d.text((170,26),'WHATSAPP',font=F(40,'Bold'),fill=WHITE); d.text((168,68),'+52 33 3027 1430',font=fn,fill=WHITE)
        paste_c(im,wa,W/2,740,eback((p-5)/10)*pulse_scale(f))
        echo(im,'¡CORRE POR EL TUYO!',1040,S[7]+10,f,size=120) if p>=10 else None
        paste_c(im,T('Guadalajara, Jalisco',700,52,ROSA,'Bold'),W/2,1240,eo((p-14)/8))
    # fixed overlays
    if sc!=7: paste_c(im,LOGO_S,W/2,150,1)
    if showbar: paste_c(im,DATEBAR,W/2,1560,1)
    paste_c(im,FINE,W/2,1655,1,0.95)
    # flash on cut
    if p<3 and f>0:
        fl=Image.new('RGBA',(W,H),(255,255,255,int(110*(1-p/3)))); im.alpha_composite(fl)
    return im.convert('RGB')
if __name__=='__main__':
    if len(sys.argv)>2 and sys.argv[2]=='stills':
        for f in map(int,sys.argv[3].split(',')): frame(f).save(f'{D}/still_{f:03d}.jpg',quality=88)
        sys.exit()
    out=sys.argv[2]
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',D+'/mix3.wav',
        '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],stdin=subprocess.PIPE)
    for f in range(NF): p.stdin.write(frame(f).tobytes())
    p.stdin.close(); p.wait()
