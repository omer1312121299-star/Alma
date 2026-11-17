import sys, shutil, time
from gradio_client import Client, handle_file
img,prompt,out=sys.argv[1],sys.argv[2],sys.argv[3]
h,w=int(sys.argv[4]),int(sys.argv[5]); seed=int(sys.argv[6]); dur=float(sys.argv[7]) if len(sys.argv)>7 else 5
neg="worst quality, inconsistent motion, blurry, jittery, distorted, warping, morphing, bent lines, melting architecture, deformed building, flicker, text, watermark, people, cars"
c=Client('Lightricks/ltx-video-distilled',verbose=False)
t=time.time()
r=c.predict(prompt,neg,handle_file(img),None,h,w,'image-to-video',dur,9,seed,False,1,True,api_name='/image_to_video')
v=r[0]['video'] if isinstance(r[0],dict) else r[0]; shutil.copy(v,out); print('ok',out,round(time.time()-t))
