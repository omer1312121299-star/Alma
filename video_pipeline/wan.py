import sys, shutil, time
from gradio_client import Client, handle_file
img,prompt,out=sys.argv[1],sys.argv[2],sys.argv[3]
dur=float(sys.argv[4]) if len(sys.argv)>4 else 5
seed=int(sys.argv[5]) if len(sys.argv)>5 else 42
space=sys.argv[6] if len(sys.argv)>6 else 'zerogpu-aoti/wan2-2-fp8da-aoti-faster'
neg="morphing, warping, distorted architecture, bent lines, melting, flicker, blurry, low quality, text, watermark, people, cars appearing, static, jpeg artifacts, oversaturated"
c=Client(space)
t=time.time()
r=c.predict(input_image=handle_file(img),prompt=prompt,steps=6,negative_prompt=neg,duration_seconds=dur,guidance_scale=1,guidance_scale_2=1,seed=seed,randomize_seed=False,api_name="/generate_video")
v=r[0]['video'] if isinstance(r[0],dict) else r[0]
shutil.copy(v,out); print('ok',out,round(time.time()-t),'s')
