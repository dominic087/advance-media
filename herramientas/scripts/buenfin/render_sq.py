import sys, types, subprocess
from PIL import Image, ImageDraw
D=sys.argv[1]
src=open(D+'/render.py').read()
rep=[("im=background(f).convert('RGBA')","im=Image.new('RGBA',(W,H),(0,0,0,0))"),
     ("if sc!=7: paste_c(im,LOGO_S,W/2,150,1)","pass"),
     ("if showbar: paste_c(im,DATEBAR,W/2,1560,1)","pass"),
     ("paste_c(im,FINE,W/2,1655,1,0.95)","pass"),
     ("    if p<3 and f>0:","    if False:"),
     ("return im.convert('RGB')","return im"),
     ("    base.paste(im,(int(cx-im.width/2),int(cy-im.height/2)),im)","    L=Image.new('RGBA',base.size,(0,0,0,0)); L.paste(im,(int(cx-im.width/2),int(cy-im.height/2))); base.alpha_composite(L)")]
for a,b in rep:
    assert a in src, a; src=src.replace(a,b)
m=types.ModuleType('r'); sys.argv=[sys.argv[0],D]+sys.argv[2:]
exec(compile(src.split("if __name__=='__main__':")[0],'render_mod','exec'),m.__dict__)
NW,NH=1080,1350
TOP,BOT=250,1490          # content band of the 9:16 layout
ZT,ZB=150,1170            # where it goes in 4:5
sc_=(ZB-ZT)/(BOT-TOP); CW=int(1080*sc_); CH=ZB-ZT
fade=Image.new('L',(CW,CH),255); d=ImageDraw.Draw(fade)
for i in range(30):
    v=int(255*i/30); d.line([(0,i),(CW,i)],fill=v); d.line([(0,CH-1-i),(CW,CH-1-i)],fill=v)
LOGO=m.logo.resize((330,int(146*330/584)),Image.LANCZOS)
BAR=m.pill('DEL 12 AL 16 DE NOVIEMBRE',m.F(46),m.CREAM,m.VINO,48,24)
FINE=m.text_img('Promoción válida del 12 al 16 de noviembre o hasta agotar existencias.',m.F(26,'SemiBold'),m.CREAM)
def frame(f):
    bg=m.background(f).resize((NW,NH),Image.BILINEAR).convert('RGBA')
    sc=max(i for i in range(8) if f>=m.S[i]); p=f-m.S[sc]
    lay=m.frame(f).crop((0,TOP,1080,BOT)).resize((CW,CH),Image.LANCZOS)
    a=Image.composite(lay.getchannel('A'),Image.new('L',(CW,CH),0),fade); lay.putalpha(a)
    bg.alpha_composite(lay,((NW-CW)//2,ZT))
    if sc!=7: m.paste_c(bg,LOGO,NW/2,78,1)
    if sc!=2: m.paste_c(bg,BAR,NW/2,1222,1)
    m.paste_c(bg,FINE,NW/2,1300,1,0.95)
    if p<3 and f>0:
        bg.alpha_composite(Image.new('RGBA',(NW,NH),(255,255,255,int(110*(1-p/3)))))
    return bg.convert('RGB')
if len(sys.argv)>2 and sys.argv[2]=='stills':
    for f in map(int,sys.argv[3].split(',')): frame(f).save(f'{D}/sq_{f:03d}.jpg',quality=90)
    sys.exit()
out=sys.argv[2]; aud=sys.argv[3]
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{NW}x{NH}','-r','30','-i','-','-i',aud,
  '-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-profile:v','high','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],stdin=subprocess.PIPE)
for f in range(m.NF): p.stdin.write(frame(f).tobytes())
p.stdin.close(); p.wait()
