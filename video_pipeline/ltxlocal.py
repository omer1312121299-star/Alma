import torch, sys, time, numpy as np
from diffusers import LTXConditionPipeline, LTXVideoTransformer3DModel, AutoencoderKLLTXVideo, FlowMatchEulerDiscreteScheduler
from diffusers.pipelines.ltx.pipeline_ltx_condition import LTXVideoCondition
from diffusers.utils import export_to_video
from PIL import Image
torch.set_num_threads(4)
key,img,out=sys.argv[1],sys.argv[2],sys.argv[3]
H,W,NF=int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]); seed=int(sys.argv[7])
ck='models/ltx/ltxv-2b-0.9.8-distilled.safetensors'
dt=torch.bfloat16
tr=LTXVideoTransformer3DModel.from_single_file(ck,config='models/ltx/transformer',torch_dtype=dt)
vae=AutoencoderKLLTXVideo.from_single_file(ck,config='models/ltx/vae',torch_dtype=dt)
sch=FlowMatchEulerDiscreteScheduler.from_pretrained('models/ltx/scheduler')
pipe=LTXConditionPipeline(scheduler=sch,vae=vae,text_encoder=None,tokenizer=None,transformer=tr)
emb=torch.load('ai/emb.pt')
pe,pm=emb[key]; ne,nm=emb['NEG']
im=Image.open(img).convert('RGB').resize((W,H),Image.LANCZOS)
t=time.time()
def cb(p,i,ts,kw):
    print(f'step {i} {time.time()-t:.0f}s',flush=True); return kw
v=pipe(conditions=[LTXVideoCondition(image=im,frame_index=0)],prompt_embeds=pe.to(dt),prompt_attention_mask=pm,
       negative_prompt_embeds=ne.to(dt),negative_prompt_attention_mask=nm,width=W,height=H,num_frames=NF,
       timesteps=[1000,993,987,981,975,909,725,0.03],guidance_scale=1.0,guidance_rescale=0.7,
       decode_timestep=0.05,decode_noise_scale=0.025,image_cond_noise_scale=0.0,
       generator=torch.Generator().manual_seed(seed),output_type='pil',callback_on_step_end=cb).frames[0]
export_to_video(v,out,fps=24); print('done',out,round(time.time()-t))
