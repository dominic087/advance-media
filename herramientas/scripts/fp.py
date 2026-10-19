import sys, numpy as np, cv2
from PIL import Image
sys.path.insert(0,sys.argv[1]); import cutpost
D=sys.argv[1]
cut=np.array(Image.open(D+'/fp1_cut.png'))
rgb=cut[...,:3].copy()
# logo en el cuerpo -> inpaint
m=np.zeros(rgb.shape[:2],np.uint8); m[1838:1912,515:615]=255
rgb=cv2.inpaint(rgb,m,9,cv2.INPAINT_TELEA)
# placa: texto y logo -> blanco liso
cut[...,:3]=rgb
from PIL import ImageDraw
pi=Image.fromarray(cut); dd=ImageDraw.Draw(pi)
dd.rounded_rectangle((394,2150,623,2266),10,fill=(236,237,236,255),outline=(205,205,205,255),width=2)
for cx in (450,570): dd.ellipse((cx-11,2157,cx+11,2179),fill=(30,30,32,255))
lg=Image.open(D+'/logo-white.png'); a=lg.split()[3]
nl=Image.new('RGBA',lg.size,(1,26,93,255)); nl.putalpha(a); lw=180; nl=nl.resize((lw,int(nl.height*lw/nl.width)),Image.LANCZOS)
pi.alpha_composite(nl,(508-lw//2,2188))
cut=np.array(pi)
Image.fromarray(cut).save(D+'/fp1_clean.png')
Image.fromarray(cut[1700:2400,250:850]).save(D+'/fp1_clean_zoom.png')
cutpost.make(D+'/fp1_clean.png',D+'/out/family-plus.jpg','FAMILY PLUS','TRICICLO ELÉCTRICO PARA TODA LA FAMILIA',
  [('800 W','MOTOR'),('40 km/h','VEL. MÁXIMA'),('45 km','AUTONOMÍA'),('1 AÑO','GARANTÍA ELÉCTRICA')])
