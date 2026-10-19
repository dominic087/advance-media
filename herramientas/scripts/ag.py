import sys, numpy as np, cv2
from PIL import Image
D=sys.argv[1]
src=np.array(Image.open(D+'/fotos/ag1.jpg').convert('RGB'))
cut=np.array(Image.open(D+'/ag1_cut.png'))
a=cut[...,3].copy()
# mantener sólo el componente principal (quita la línea negra de la anotación)
n,lab,st,_=cv2.connectedComponentsWithStats((a>40).astype(np.uint8))
big=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); a[lab!=big]=0
# quitar la mitad superior derecha donde estaba la línea (por si quedó pegada)
a[300:520,830:870]=np.where(np.arange(830,870)[None,:]>=840,0,a[300:520,830:870]) if False else a[300:520,830:870]
rgb=src.copy()
hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV)
orange=((hsv[...,0]>5)&(hsv[...,0]<25)&(hsv[...,1]>120)&(hsv[...,2]>120)).astype(np.uint8)
m=np.zeros(a.shape,np.uint8)
# línea + punto "posapies"
box=np.zeros_like(m); box[700:870,662:692]=1; m|=orange&box
# punto + línea "sliders"
box=np.zeros_like(m); box[790:960,200:302]=1; m|=orange&box
m=cv2.dilate(m*255,np.ones((7,7),np.uint8))
# logos del proveedor
m[803:847,408:527]=255   # PIALLI en el piso
m[595:700,620:718]=np.maximum(m[595:700,620:718],255*(cv2.cvtColor(rgb[595:700,620:718],cv2.COLOR_RGB2GRAY)>60).astype(np.uint8))  # calcomanía PIA
m[500:560,236:274]=np.maximum(m[500:560,236:274],255*(cv2.cvtColor(rgb[500:560,236:274],cv2.COLOR_RGB2GRAY)>120).astype(np.uint8))
m=cv2.dilate(m,np.ones((3,3),np.uint8))
rgb=cv2.inpaint(rgb,m,7,cv2.INPAINT_TELEA)
# donde la anotación salía fuera de la moto, quitar alfa
gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
sl=np.zeros_like(m); sl[818:965,195:290]=1
a[(m>0)&(sl>0)]=0
sl2=np.zeros_like(m); sl2[780:820,240:300]=1; a[(m>0)&(sl2>0)&(gray>80)]=0
ps=np.zeros_like(m); ps[690:880,655:700]=1
a[(m>0)&(ps>0)&(gray>95)]=0
# piso: color oscuro liso
a[805:845,410:525]=255
bx2=np.zeros_like(m); bx2[592:702,618:720]=1
hs=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV)
sel=(bx2>0)&((hs[...,1]>70)&(hs[...,2]>60)|(cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)>55))
rgb[sel]=(26,26,29)
# calcomanía trasera: cerrar huecos de alfa
cl=cv2.morphologyEx((a>128).astype(np.uint8),cv2.MORPH_CLOSE,np.ones((25,25),np.uint8))
bx=np.zeros_like(m); bx[590:705,615:722]=1
a[(bx>0)&(cl>0)]=255
out=np.dstack([rgb,a])
Image.fromarray(out).save(D+'/ag1_clean.png')
v=Image.new('RGBA',(960,1280),(1,26,93,255)); v.alpha_composite(Image.fromarray(out)); v.convert('RGB').crop((0,400,960,1000)).save(D+'/ag1_clean_v.jpg')
Image.fromarray(m).crop((0,400,960,1000)).save(D+'/ag1_mask.png')
