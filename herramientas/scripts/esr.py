import ncnn, numpy as np, cv2, sys, time
def load():
    net=ncnn.Net(); net.opt.use_vulkan_compute=False; net.opt.num_threads=2
    net.load_param("/home/claude/esr/r/models/realesrgan-x4plus.param"); net.load_model("/home/claude/esr/r/models/realesrgan-x4plus.bin"); return net
def run(net,rgb):  # rgb uint8 HxWx3 -> 4x
    x=(rgb.astype(np.float32)/255.).transpose(2,0,1).copy()
    ex=net.create_extractor(); ex.input("data",ncnn.Mat(x)); r,out=ex.extract("output")
    o=np.array(out).transpose(1,2,0); return np.clip(o*255,0,255).round().astype(np.uint8)
def tiled(net,rgb,T=128,P=10):
    h,w=rgb.shape[:2]; out=np.zeros((h*4,w*4,3),np.uint8)
    for y in range(0,h,T):
        for x in range(0,w,T):
            y0,x0=max(y-P,0),max(x-P,0); y1,x1=min(y+T+P,h),min(x+T+P,w)
            o=run(net,np.ascontiguousarray(rgb[y0:y1,x0:x1]))
            cy,cx=(y-y0)*4,(x-x0)*4; hh,ww=min(T,h-y)*4,min(T,w-x)*4
            out[y*4:y*4+hh,x*4:x*4+ww]=o[cy:cy+hh,cx:cx+ww]
    return out
if __name__=="__main__":
    net=load(); im=cv2.imread(sys.argv[1])[:,:,::-1]
    t=time.time(); o=tiled(net,np.ascontiguousarray(im)); print(o.shape,time.time()-t)
    cv2.imwrite(sys.argv[2],o[:,:,::-1])
