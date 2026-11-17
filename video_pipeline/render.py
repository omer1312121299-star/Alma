import numpy as np, cv2, sys, json, subprocess, os
sys.path.insert(0,'.'); from look import grade, smooth
W,H,FPS=1920,1080,30
OW,OH=2576,1912
SRC=os.environ.get('SRC','work/up4.png'); U=float(os.environ.get('U','4'))
big=None
def load():
    global big
    if big is None: big=cv2.imread(SRC)[:,:,::-1]
    return big
disp_full=np.load('work/disp.npy')
def ease(t): return 0.45*t+0.55*(t*t*(3-2*t))
def lerp(a,b,t): return np.array(a,float)*(1-t)+np.array(b,float)*t

def prep(shot):
    # region in orig coords covering all crops + margin
    xs=[];ys=[]
    for c,w in [(shot['c0'],shot['w0']),(shot['c1'],shot['w1'])]:
        h=w*9/16; xs+= [c[0]-w/2,c[0]+w/2]; ys+=[c[1]-h/2,c[1]+h/2]
    wmin=min(shot['w0'],shot['w1']); m=0.12*max(shot['w0'],shot['w1'])
    x0=max(0,int(min(xs)-m)); x1=min(OW,int(max(xs)+m)); y0=max(0,int(min(ys)-m)); y1=min(OH,int(max(ys)+m))
    S=W/wmin*1.0  # tile px per orig px
    b=load()
    sub=b[int(y0*U):int(y1*U),int(x0*U):int(x1*U)]
    tw,th=int((x1-x0)*S),int((y1-y0)*S)
    interp=cv2.INTER_AREA if S<U else cv2.INTER_CUBIC
    tile=cv2.resize(sub,(tw,th),interpolation=interp).astype(np.float32)/255
    d=cv2.resize(disp_full[y0:y1,x0:x1],(tw,th),interpolation=cv2.INTER_LINEAR)
    tile=grade(tile,d,sky_y_off=y0*S,full_h=OH*S,x_off=x0*S,full_w=OW*S,S=S)
    # foliage mask
    hsv=cv2.cvtColor((tile*255).astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32)
    fol=smooth(hsv[...,0],22,32)*(1-smooth(hsv[...,0],88,98))*smooth(hsv[...,1],35,70)*smooth(d,0.30,0.38)
    fol=cv2.GaussianBlur(fol.astype(np.float32),(0,0),6*S/2+1)
    # disparity for warping: dilate foreground so edges stretch background
    r=max(3,int(5*S)); k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*r+1,2*r+1))
    dw=cv2.GaussianBlur(cv2.dilate(d,k),(0,0),r*1.6)
    return dict(tile=tile,d=d,dw=dw,fol=fol,x0=x0,y0=y0,S=S)

def frames(shot,P):
    n=int(round(shot['dur']*FPS)); tile,dw,d,fol,S=P['tile'],P['dw'],P['d'],P['fol'],P['S']
    uu,vv=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
    du=(uu-W/2); dv=(vv-H/2)
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
    vig=1-0.10*(((uu-W/2)/(W*0.62))**2+((vv-H/2)/(H*0.75))**2)
    vig=np.clip(vig,0,1)[...,None]
    for i in range(n):
        t=ease(i/max(n-1,1)); tl=i/FPS
        c=lerp(shot['c0'],shot['c1'],t); w=lerp([shot['w0']],[shot['w1']],t)[0]
        T=lerp(shot.get('T0',[0,0]),shot.get('T1',[0,0]),t)  # orig px per unit disp
        z=lerp([shot.get('z0',0)],[shot.get('z1',0)],t)[0]
        df=shot.get('df',0.4)
        sc=w/W  # orig px per output px
        bx=(c[0]-P['x0'])*S; by=(c[1]-P['y0'])*S
        qx=(bx+du*sc*S).astype(np.float32); qy=(by+dv*sc*S).astype(np.float32)
        for _ in range(5):
            dd=cv2.remap(dw,qx,qy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)-df
            s=1+z*dd
            qx=(bx+du*sc*S/s+T[0]*dd*S).astype(np.float32); qy=(by+dv*sc*S/s+T[1]*dd*S).astype(np.float32)
        if shot.get('sway',True):
            f=cv2.remap(fol,qx,qy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
            amp=1.5*sc*S
            ph=qx/(S*140); pv=qy/(S*180)
            sx=np.sin(2*np.pi*(0.55*tl+ph+0.3*pv))+0.5*np.sin(2*np.pi*(1.3*tl+2.1*ph-pv+0.2))
            sy=0.35*np.sin(2*np.pi*(0.8*tl+1.3*pv+ph))
            qx=(qx+f*sx*amp).astype(np.float32); qy=(qy+f*sy*amp).astype(np.float32)
        fr=cv2.remap(tile,qx,qy,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
        dof=shot.get('dof',0)
        if dof>0:
            fd=lerp([shot.get('f0',df)],[shot.get('f1',df)],t)[0]
            dmap=cv2.remap(d,qx,qy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
            coc=np.clip(np.abs(dmap-fd)*shot.get('dofk',4),0,1)
            coc=cv2.GaussianBlur(coc,(0,0),3)[...,None]
            b1=cv2.GaussianBlur(fr,(0,0),dof*0.45); b2=cv2.GaussianBlur(fr,(0,0),dof)
            fr=np.where(coc<0.5, fr*(1-coc*2)+b1*(coc*2), b1*(2-coc*2)+b2*(coc*2-1))
        g=shot.get('glow')
        if g:
            gx=(g[0]-c[0])/sc+W/2; gy=(g[1]-c[1])/sc+H/2
            r2=((uu-gx)**2+(vv-gy)**2)/(g[2]/sc)**2
            fr=fr+(np.exp(-r2)*g[3])[...,None]*np.array([1.0,0.82,0.55],np.float32)

        fr=np.clip(fr*vig+ (1-vig)*0.0,0,1)
        yield fr

def run(shots,outdir,only=None):
  sel=[s for k,s in enumerate(shots) if only is None or k in only]
  for s in sel:
    out=f"{outdir}/{s['name']}.mp4"
    p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
      '-vf','noise=alls=3:allf=t,format=yuv420p','-c:v','libx264','-preset','slow','-crf','15',out],stdin=subprocess.PIPE)
    P=prep(s)
    for fr in frames(s,P):
        p.stdin.write((fr*255+0.5).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait(); print('done',s['name'],flush=True)

if __name__=='__main__':
    shots=json.load(open(sys.argv[1]))
    only=[int(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else None
    run(shots,sys.argv[2],only)
