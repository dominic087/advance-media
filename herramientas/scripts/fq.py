import sys, numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0,sys.argv[1]); import cutpost
D=sys.argv[1]
c=np.array(Image.open(D+'/fq2_cut.png')); rgb=np.array(Image.open(D+'/fotos/fq2.jpg').convert('RGB')); a=c[...,3].copy()
a[a<70]=0
n,lab,st,_=cv2.connectedComponentsWithStats((a>0).astype(np.uint8))
big=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); a[lab!=big]=0
m=np.zeros(a.shape,np.uint8); m[698:744,722:780]=255; m[1190:1220,342:418]=255
rgb=cv2.inpaint(rgb,m,7,cv2.INPAINT_TELEA)
rgb=(255*((rgb/255.0)**0.8)*1.04).clip(0,255).astype(np.uint8)
hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV); blu=(hsv[...,0]>95)&(hsv[...,0]<130); hsv[...,1]=np.where(blu,(hsv[...,1]*0.35).astype(np.uint8),hsv[...,1]); rgb=cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)
pi=Image.fromarray(np.dstack([rgb,a])); d=ImageDraw.Draw(pi)
d.rectangle((858,812,1000,868),fill=(236,236,234,255))
d.rectangle((910,786,944,812),fill=(236,236,234,255))
lg=Image.open(D+'/logo-white.png'); al=lg.split()[3]
nl=Image.new('RGBA',lg.size,(1,26,93,255)); nl.putalpha(al); lw=118; nl=nl.resize((lw,int(nl.height*lw/nl.width)),Image.LANCZOS)
pi.alpha_composite(nl,(929-lw//2,818))
pi.save(D+'/fq2_clean.png')
v=Image.new('RGBA',pi.size,(1,26,93,255)); v.alpha_composite(pi); v.convert('RGB').crop((600,600,1100,1000)).save(D+'/z.jpg')
cutpost.make(D+'/fq2_clean.png',D+'/out/family-q.jpg','FAMILY Q','TRICICLO ELÉCTRICO DE 1000 W',
  [('1000 W','MOTOR'),('45 km/h','VEL. MÁXIMA'),('50 km','AUTONOMÍA'),('1 AÑO','GARANTÍA ELÉCTRICA')],maxw=760)
