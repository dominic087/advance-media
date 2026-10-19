import sys, numpy as np, cv2
from PIL import Image
sys.path.insert(0,sys.argv[1]); import cutpost
D=sys.argv[1]
c=np.array(Image.open(D+'/fpq1_cut.png')); rgb=np.array(Image.open(D+'/fotos/fpq1.jpg').convert('RGB')); a=c[...,3].copy()
a[:865,:245]=0
a[a<70]=0
a[1000:1036,80:226]=0
n,lab,st,_=cv2.connectedComponentsWithStats((a>0).astype(np.uint8))
big=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); a[lab!=big]=0
m=np.zeros(a.shape,np.uint8); m[970:1004,1018:1118]=255
rgb=cv2.inpaint(rgb,m,7,cv2.INPAINT_TELEA)
out=np.dstack([rgb,a]); Image.fromarray(out).save(D+'/fpq1_clean.png')
cutpost.make(D+'/fpq1_clean.png',D+'/out/family-plus-q.jpg','FAMILY PLUS Q','TRICICLO ELÉCTRICO CON BATERÍA DE 72 V',
  [('1000 W','MOTOR'),('45 km/h','VEL. MÁXIMA'),('50 km','AUTONOMÍA'),('72 V','BATERÍA')])
