import cv2, numpy as np, sys
sys.path.insert(0,"/home/claude/esr"); from esr import load, tiled
net=load()
for k in ["col_gris","col_rojo","hero_clean","tilt_clean"]:
    im=cv2.imread(f"/home/claude/fotos/cargo180/{k}.png")[:,:,::-1]
    o=tiled(net,np.ascontiguousarray(im)); cv2.imwrite(f"/home/claude/fotos/cargo180/{k}_x4.png",o[:,:,::-1]); print("done",k,flush=True)
