import torch, numpy as np, cv2, sys, time
from spandrel import ModelLoader
torch.set_num_threads(4)
m=ModelLoader().load_from_file(sys.argv[1]).model.eval()
img=cv2.imread(sys.argv[2])[:,:,::-1].astype(np.float32)/255
H,W,_=img.shape; s=4; T=256; P=16
out=np.zeros((H*s,W*s,3),np.float32)
t0=time.time()
for y in range(0,H,T):
  for x in range(0,W,T):
    y0,x0=max(y-P,0),max(x-P,0); y1,x1=min(y+T+P,H),min(x+T+P,W)
    t=torch.from_numpy(img[y0:y1,x0:x1].transpose(2,0,1).copy())[None]
    with torch.no_grad(): o=m(t)[0].numpy().transpose(1,2,0)
    ty,tx=(y-y0)*s,(x-x0)*s; h,w=min(T,H-y)*s,min(T,W-x)*s
    out[y*s:y*s+h,x*s:x*s+w]=o[ty:ty+h,tx:tx+w]
  print(y,time.time()-t0,flush=True)
cv2.imwrite(sys.argv[3],(np.clip(out,0,1)[:,:,::-1]*255+.5).astype(np.uint8))
