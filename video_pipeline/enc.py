import torch, sys
from transformers import T5EncoderModel
import sentencepiece as spm
torch.set_num_threads(4)
P="Cinematic architectural film, photorealistic, golden hour warm sunlight, smooth stabilized gimbal camera, sharp details, stable straight architectural lines"
NEG="worst quality, inconsistent motion, blurry, jittery, distorted, warping, morphing, bent lines, melting architecture, deformed building, flicker, text, watermark, people, cars"
sp=spm.SentencePieceProcessor(model_file='models/ltx/tokenizer/spiece.model')
te=T5EncoderModel.from_pretrained('models/ltx/text_encoder',torch_dtype=torch.bfloat16).eval()
items={'NEG':NEG}
for line in open('ai/shots.tsv'):
    k,p=line.rstrip('\n').split('\t'); items[k]=p+'. '+P
items['A']="Cinematic drone shot slowly gliding forward toward a modern residential apartment building, trees in the foreground gently swaying. "+P
out={}
for k,t in items.items():
    ids=sp.encode(t)[:127]+[1]; n=len(ids); ids=ids+[0]*(128-n)
    ii=torch.tensor([ids]); am=torch.zeros(1,128,dtype=torch.long); am[0,:n]=1
    with torch.no_grad(): e=te(ii,attention_mask=am)[0]
    out[k]=(e.to(torch.bfloat16),am); print(k,n,e.shape,flush=True)
torch.save(out,'ai/emb.pt')
