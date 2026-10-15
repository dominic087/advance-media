from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
S=2
F="/usr/share/fonts/opentype/inter/"
def f(w,s): return ImageFont.truetype(F+f"Inter-{w}.otf",s*S)
W,H=1080,1350
class Dr:
    def __init__(s,im): s.d=ImageDraw.Draw(im)
    def _b(s,xy): return tuple(v*S for v in xy)
    def text(s,xy,t,font=None,fill=None,anchor=None): s.d.text(s._b(xy),t,font=font,fill=fill,anchor=anchor)
    def textlength(s,t,font=None): return s.d.textlength(t,font=font)/S
    def rounded_rectangle(s,xy,r,fill=None,outline=None,width=1): s.d.rounded_rectangle(s._b(xy),r*S,fill=fill,outline=outline,width=width*S)
    def ellipse(s,xy,fill=None,outline=None,width=1): s.d.ellipse(s._b(xy),fill=fill,outline=outline,width=width*S)
    def rectangle(s,xy,fill=None): s.d.rectangle(s._b(xy),fill=fill)
NAVY=(1,26,93); DEEP=(0,11,46); CREAM=(243,233,210); BUR=(138,44,69); GREEN=(37,211,102)
cut={k:Image.open(f"up_{k}.png") for k in ["hero","rojo","verde","negro"]}
logo=Image.open("/home/claude/advance-video/public/logo-white.png").convert("RGBA")
def bg(glow=(0.5,0.45)):
    g=Image.new("RGB",(W*S,H*S),DEEP)
    top=Image.linear_gradient("L").resize((W*S,H*S))
    nv=Image.new("RGB",(W*S,H*S),NAVY)
    g=Image.composite(g,nv,top)
    gl=Image.new("L",(W*S,H*S),0); d=ImageDraw.Draw(gl)
    cx,cy=int(W*glow[0])*S,int(H*glow[1])*S; d.ellipse((cx-480*S,cy-420*S,cx+480*S,cy+420*S),fill=120)
    gl=gl.filter(ImageFilter.GaussianBlur(150*S))
    g.paste(Image.new("RGB",(W*S,H*S),(30,70,170)),(0,0),gl)
    return g
def shadow(im,xy,w,h):
    s=Image.new("L",(W*S,H*S),0); ImageDraw.Draw(s).ellipse((xy[0]*S,xy[1]*S,(xy[0]+w)*S,(xy[1]+h)*S),fill=170)
    s=s.filter(ImageFilter.GaussianBlur(18*S)); im.paste(Image.new("RGB",(W*S,H*S),(0,4,25)),(0,0),s)
def put(im,c,x,y,w):
    ch=int(c.height*w/c.width)
    shadow(im,(x+int(w*.1),y+ch-int(w*.07)),int(w*.8),int(w*.1))
    c=c.resize((w*S,ch*S),Image.LANCZOS)
    al=c.getchannel("A"); c=c.convert("RGB").filter(ImageFilter.UnsharpMask(1.6,70,2)); c.putalpha(al)
    im.paste(c,(x*S,y*S),c); return ch
def lg(im,w=300,x=None,y=36):
    l=logo.resize((w*S,int(logo.height*w/logo.width)*S),Image.LANCZOS); im.paste(l,(((W-w-50) if x is None else x)*S,y*S),l)

def title(im,y,size,x=50):
    Dr(im).text((x,y),"FAMILY",font=f("BlackItalic",size),fill=(255,255,255))
A=bg((0.68,0.42)); d=Dr(A)
lg(A,300); title(A,60,170)
d.rounded_rectangle((50,270,420,340),20,outline=(255,255,255),width=2)
d.text((75,305),"Bocina Bluetooth",font=f("SemiBold",28),fill=(255,255,255),anchor="lm")
d.text((50,390),"CARACTERÍSTICAS",font=f("ExtraBold",34),fill=(255,255,255))
specs=["Velocidad máxima 45 km/h","Motor 850 W","Baterías 48V-20AH","Autonomía 60 km","Rodada 8\"","Inclinación 15°","Frenos de tambor","Peso máx. soportado 200 kg"]
for i,s in enumerate(specs):
    y=445+i*66; d.rounded_rectangle((50,y,440,y+54),14,outline=(120,150,220),width=2,fill=(6,36,110))
    d.ellipse((66,y+19,82,y+35),fill=CREAM); d.text((98,y+27),s,font=f("Medium",24),fill=(255,255,255),anchor="lm")
put(A,cut["hero"],480,240,540)
d.text((W//2,1002),"COLORES DISPONIBLES",font=f("ExtraBold",38),fill=(255,255,255),anchor="mm")
xs=[60,405,750]
for (k,lab),x in zip([("rojo","ROJO"),("verde","VERDE"),("negro","NEGRO")],xs):
    h=put(A,cut[k],x,1030,262); d.rounded_rectangle((x+36,1295,x+226,1337),21,outline=(255,255,255),width=2); d.text((x+131,1316),lab,font=f("Bold",24),fill=(255,255,255),anchor="mm")
A.save("/home/claude/fotos/salida/family-opcion-A-HD.jpg",quality=95,subsampling=0)
# ---------- B: propuesta
B=bg((0.5,0.4)); d=Dr(B)
lg(B,280,x=(W-280)//2,y=40)
d.text((W//2,230),"FAMILY",font=f("BlackItalic",190),fill=(255,255,255),anchor="mm")
pw=d.textlength("TRICICLO ELÉCTRICO · BOCINA BLUETOOTH",font=f("Bold",26))+60
d.rounded_rectangle(((W-pw)/2,330,(W+pw)/2,386),28,fill=BUR); d.text((W//2,358),"TRICICLO ELÉCTRICO · BOCINA BLUETOOTH",font=f("Bold",26),fill=CREAM,anchor="mm")
h=put(B,cut["hero"],(W-500)//2+20,385,500)
badges=[("45","km/h"),("850","W"),("60","km"),("200","kg")]
bw=230
for i,(n,u) in enumerate(badges):
    x=60+i*(bw+13); y=1030
    d.rounded_rectangle((x,y,x+bw,y+112),22,fill=(6,36,110),outline=(120,150,220),width=2)
    d.text((x+bw//2,y+48),n,font=f("ExtraBold",56),fill=CREAM,anchor="mm"); d.text((x+bw//2,y+90),u+("  máx." if i==0 else "  motor" if i==1 else "  autonomía" if i==2 else "  carga"),font=f("Medium",20),fill=(200,215,245),anchor="mm")
d.text((50,1190),"Disponible en:",font=f("SemiBold",26),fill=(255,255,255),anchor="lm")
for j,(c,col) in enumerate([("Rojo",(214,40,40)),("Verde",(130,190,140)),("Negro",(25,25,30))]):
    x=270+j*190; d.ellipse((x,1172,x+36,1208),fill=col,outline=(255,255,255),width=2); d.text((x+48,1190),c,font=f("SemiBold",26),fill=(255,255,255),anchor="lm")
d.rectangle((0,1240,W,H),fill=DEEP)
d.text((50,1295),"Guadalajara, Jalisco",font=f("SemiBold",26),fill=CREAM,anchor="lm")
bt="ESCRÍBENOS POR WHATSAPP"; bf=f("ExtraBold",24); tw=d.textlength(bt,font=bf)+60
d.rounded_rectangle((W-50-tw,1262,W-50,1332),35,fill=GREEN); d.text((W-50-tw/2,1297),bt,font=bf,fill=(255,255,255),anchor="mm")
B.save("/home/claude/fotos/salida/family-opcion-B-HD.jpg",quality=95,subsampling=0)
