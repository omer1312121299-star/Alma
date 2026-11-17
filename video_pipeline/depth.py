import torch, numpy as np, cv2, sys
from transformers import AutoImageProcessor, AutoModelForDepthEstimation
from PIL import Image
img=Image.open(sys.argv[1]).convert("RGB")
name="models/da2"
p=AutoImageProcessor.from_pretrained(name); m=AutoModelForDepthEstimation.from_pretrained(name).eval()
torch.set_num_threads(4)
outs=[]
for flip in [False,True]:
    im=img.transpose(Image.FLIP_LEFT_RIGHT) if flip else img
    inp=p(images=im,return_tensors="pt",size={"height":1036,"width":1386})
    with torch.no_grad(): d=m(**inp).predicted_depth[0].numpy()
    d=cv2.resize(d,img.size,interpolation=cv2.INTER_CUBIC)
    outs.append(d[:,::-1] if flip else d)
d=np.mean(outs,0); d=(d-d.min())/(d.max()-d.min())
np.save(sys.argv[2],d.astype(np.float32)); cv2.imwrite(sys.argv[2]+".png",(d*255).astype(np.uint8))
