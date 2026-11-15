# Reel "Conoce nuestras bicimotos" 1080x1920 30fps. Uso: python3 render.py <salida_dir> [audio.wav] [timing.json]
import sys, os, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance
W,H,FPS=1080,1920,30
NAVY=(1,26,93); DEEP=(0,11,46); CREAM=(243,233,210); VINO=(138,44,69); ROSA=(232,169,186); GREEN=(37,211,102)
FD='/usr/share/fonts/opentype/inter/'
def F(sz,st='BlackItalic'): return ImageFont.truetype(FD+f'Inter-{st}.otf',sz)
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=sys.argv[1]; os.makedirs(OUT+'/fr',exist_ok=True)
logo=Image.open(HERE+'/../logo-white.png').convert('RGBA')
P='/mnt/project-files/'
def ld(p): return ImageOps.exif_transpose(Image.open(p)).convert('RGB')
ag=Image.open(P+'piezas/semana3/aguila-post.jpg').convert('RGB'); ag=ag.crop((0,330,1080,1060))
MOTOS=[  # (nombre, foto, centro x/y de recorte, datos)
 ('ALPHA', ld(P+'fotos/semana4/alpha/120806.jpg'), (0.35,0.62), ['500 W','30 km/h','35 km']),
 ('BETA',  ld(P+'fotos/semana6/beta1.jpg'), (0.5,0.55), ['500 W','30 km/h','35 km']),
 ('LUNA',  ld(P+'fotos/semana4/luna/184650.jpg'), (0.45,0.6), ['700 W','35 km/h','40 km']),
 ('AUDI',  ld(P+'fotos/semana6/audi2.jpg'), (0.45,0.62), ['850 W','40 km/h','45 km']),
 ('ÁGUILA',ag, (0.5,0.5), ['950 W','45 km/h','50 km']),
]
CW,CH=960,940
def card(im,c):
    r=max(CW/im.width,CH/im.height)*1.12; im=im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS)
    return im
CARDS=[card(m[1],m[2]) for m in MOTOS]
TM=json.load(open(sys.argv[3])) if len(sys.argv)>3 else {'starts':[0,3,6,9,12,15,18],'dur':23}
ST=TM['starts']+[TM['dur']]; NF=int(TM['dur']*FPS)
bg=Image.new('RGB',(W,H)); bd=ImageDraw.Draw(bg)
for y in range(H):
    k=y/H; t=max(0,1-abs(k-.42)*1.7); bd.line([(0,y),(W,y)],fill=tuple(int(DEEP[i]+(NAVY[i]-DEEP[i])*t) for i in range(3)))
def eo(x): x=max(0,min(1,x)); return 1-(1-x)**3
def ctext(d,y,txt,f,fill):
    d.text(((W-d.textlength(txt,font=f))/2,y),txt,font=f,fill=fill)
def pill(d,cx,y,txt,f,fg,bgc,px=34,h=70):
    tw=d.textlength(txt,font=f); d.rounded_rectangle((cx-tw/2-px,y,cx+tw/2+px,y+h),h//2,fill=bgc)
    d.text((cx-tw/2,y+h/2),txt,font=f,fill=fg,anchor='lm')
def put_logo(im,y=110,w=440):
    lg=logo.resize((w,int(logo.height*w/logo.width)),Image.LANCZOS); im.paste(lg,((W-w)//2,y),lg)
def frame(f):
    t=f/FPS; s=max(i for i in range(len(ST)-1) if ST[i]<=t); p=(t-ST[s]); L=ST[s+1]-ST[s]
    im=bg.copy(); d=ImageDraw.Draw(im)
    put_logo(im)
    if s==0:
        a=eo(p/0.6)
        pill(d,W/2,620,'NUEVA TEMPORADA' if False else 'MOVILIDAD ELÉCTRICA',F(34,'Bold'),CREAM,VINO)
        f1=F(150); y=760+int((1-a)*80)
        ctext(d,y,'CONOCE',f1,CREAM); ctext(d,y+170,'NUESTRAS',F(118),ROSA); ctext(d,y+320,'BICIMOTOS',f1,CREAM)
        ctext(d,1400,'5 modelos para moverte por la ciudad',F(40,'SemiBold'),CREAM)
    elif s<=5:
        n,_,c,dat=MOTOS[s-1]; ph=CARDS[s-1]
        z=1+0.06*p/L; ph2=ph.resize((int(ph.width*z),int(ph.height*z)),Image.BILINEAR)
        cx=int((ph2.width-CW)*c[0]); cy=int((ph2.height-CH)*c[1])
        crop=ph2.crop((cx,cy,cx+CW,cy+CH)); m=Image.new('L',(CW,CH),0); ImageDraw.Draw(m).rounded_rectangle((0,0,CW-1,CH-1),40,fill=255)
        x0=(W-CW)//2+int((1-eo(p/0.45))*W*0.6); im.paste(crop,(x0,330),m)
        a=eo((p-0.15)/0.5)
        f1=F(160); tw=d.textlength(n,font=f1)
        d.text(((W-tw)/2,1300+int((1-a)*60)),n,font=f1,fill=CREAM)
        cw=W//3
        for i,v in enumerate(dat):
            if p>0.35+i*0.15:
                pill(d,cw*i+cw/2,1560,v,F(44,'ExtraBold'),DEEP if i==1 else CREAM,ROSA if i==1 else VINO,px=30,h=84)
        for i,l in enumerate(['MOTOR','VEL. MÁXIMA','AUTONOMÍA']):
            ctx=cw*i+cw/2; fl=F(24,'Bold'); d.text((ctx-d.textlength(l,font=fl)/2,1660),l,font=fl,fill=ROSA)
        # puntos de progreso
        for i in range(5): d.ellipse((W/2-90+i*40-9,1760-9,W/2-90+i*40+9,1760+9),fill=CREAM if i==s-1 else (60,70,120))
    else:
        a=eo(p/0.6)
        ctext(d,560,'TODAS CON',F(90),ROSA); ctext(d,670,'1 AÑO DE',F(140),CREAM); ctext(d,830,'GARANTÍA',F(140),CREAM)
        ctext(d,990,'en todo lo eléctrico',F(46,'SemiBold'),CREAM)
        ctext(d,1080,'Refacciones y asistencia telefónica',F(40,'SemiBold'),ROSA)
        sc=1+0.04*abs(((f%30)/15)-1)
        btn='ESCRÍBENOS POR WHATSAPP'; fb=F(int(44*sc),'ExtraBold'); bw=d.textlength(btn,font=fb)+90; hh=int(110*sc)
        d.rounded_rectangle(((W-bw)/2,1300,(W+bw)/2,1300+hh),hh//2,fill=GREEN); d.text((W/2,1300+hh/2),btn,font=fb,fill=DEEP,anchor='mm')
        ctext(d,1480,'Guadalajara, Jalisco',F(46,'SemiBold'),CREAM)
    return im
for f in range(NF): frame(f).save(f'{OUT}/fr/{f:04d}.jpg',quality=92)
cmd=['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{OUT}/fr/%04d.jpg']
if len(sys.argv)>2 and sys.argv[2]!='-': cmd+=['-i',sys.argv[2],'-c:a','aac','-b:a','160k','-shortest']
cmd+=['-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-movflags','+faststart',f'{OUT}/bicimotos.mp4']
subprocess.run(cmd,check=True)
