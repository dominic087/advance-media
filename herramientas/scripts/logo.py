from PIL import Image
import numpy as np
im=np.asarray(Image.open('/home/user/advance-media/2026-10/family-golovolt.jpg').convert('RGB')).astype(float)
c=im[0:250,1500:2160]
a=np.clip((c[...,0]-25)/(230-25),0,1)
ys,xs=np.where(a>0.1); c=c[max(0,ys.min()-4):ys.max()+5, max(0,xs.min()-4):xs.max()+5]; a=a[max(0,ys.min()-4):ys.max()+5, max(0,xs.min()-4):xs.max()+5]
out=np.zeros(a.shape+(4,),np.uint8); out[...,:3]=255; out[...,3]=(a*255).astype(np.uint8)
Image.fromarray(out).save('logo-white.png'); print(out.shape)
