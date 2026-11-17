import numpy as np, cv2
def smooth(x,a,b):
    t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
def sky_mask(img, disp):
    # img float RGB 0..1, disp 0..1 (same size)
    hsv=cv2.cvtColor((img*255).astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32)
    lum=img.mean(2)
    m=smooth(-disp,-0.20,-0.12)*smooth(lum,0.62,0.75)*(hsv[...,1]<60)
    m=cv2.GaussianBlur(m.astype(np.float32),(0,0),1.2)
    return np.clip(m,0,1)
def make_sky(h,w,y_off=0,full_h=None):
    full_h=full_h or h
    y=(np.arange(h)[:,None]+y_off)/full_h
    x=np.linspace(0,1,w)[None,:]
    top=np.array([0.56,0.69,0.87]); mid=np.array([0.84,0.88,0.92]); hor=np.array([0.98,0.93,0.84])
    t=np.clip(y/0.62,0,1)[...,None]
    a=np.clip(t/0.55,0,1); b=np.clip((t-0.55)/0.45,0,1)
    sky=np.where(t<0.55, top*(1-a)+mid*a, mid*(1-b)+hor*b)
    sky=np.broadcast_to(sky,(h,w,3)).copy()
    # sun glow upper left behind trees
    g=np.exp(-(((x-0.08)/0.35)**2+((y-0.42)/0.30)**2))[...,None]
    sky=sky*(1-0.45*g)+np.array([1.0,0.95,0.86])*0.45*g
    return sky.astype(np.float32)
def sky_replace(img, disp, sky, S=1.0):
    hard=(sky_mask(img,disp)>0.9).astype(np.uint8)
    lum=img.mean(2); br=img[...,2]-img[...,0]
    k=lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*int(r)+1,2*int(r)+1))
    region=cv2.dilate(hard,k(max(2,18*S))).astype(np.float32)
    region=cv2.GaussianBlur(region,(0,0),4*S+1)*(disp<0.6)
    # local old-sky colour (normalized masked blur)
    sg=max(8,60*S); hf=hard.astype(np.float32)
    num=cv2.GaussianBlur(img*hf[...,None],(0,0),sg); den=cv2.GaussianBlur(hf,(0,0),sg)[...,None]
    old=np.where(den>1e-3,num/np.maximum(den,1e-3),np.array([0.87,0.88,0.93],np.float32))
    skylum=old.mean(2)
    lmin=cv2.erode(lum,k(max(2,6*S)))
    a=np.clip((lum-lmin)/np.maximum(skylum-lmin,0.05),0,1)
    hsv=cv2.cvtColor((img*255).astype(np.uint8),cv2.COLOR_RGB2HSV)
    fol=((hsv[...,0]>=20)&(hsv[...,0]<=95)&(hsv[...,1]>40)&(hsv[...,2]<200)).astype(np.uint8)
    foln=cv2.GaussianBlur(cv2.dilate(fol,k(max(2,10*S))).astype(np.float32),(0,0),2*S+1)
    bld=smooth(disp,0.22,0.28)*(1-np.clip(foln*1.5,0,1))
    a=a*smooth(br,-0.05,0.0)*region*(1-bld)
    a=np.maximum(a,hf)
    return np.clip(img+a[...,None]*(sky-old),0,1)

def grade(img, disp, sky_y_off=0, full_h=None, x_off=0, full_w=None, S=1.0):
    h,w,_=img.shape
    sky=make_sky(h,w,sky_y_off,full_h)
    out=sky_replace(img,disp,sky,S)
    # filmic golden-hour grade
    lum=(out*np.array([0.3,0.59,0.11])).sum(2,keepdims=True)
    hi=smooth(lum,0.35,0.95); sh=1-smooth(lum,0.05,0.45)
    out=out*(1+hi*np.array([0.035,0.012,-0.035]))
    out=out+sh*np.array([-0.012,-0.004,0.008])
    out=np.clip(out,0,1)
    # contrast: lower blacks, s-curve
    out=np.clip((out-0.03)/0.95,0,1)
    out=out+0.18*(out-0.5)*(1-np.abs(2*out-1))
    # vegetation richer & slightly golden
    hsv=cv2.cvtColor((np.clip(out,0,1)*255).astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32)
    veg=(smooth(hsv[...,0],25,35)*(1-smooth(hsv[...,0],85,95))*smooth(hsv[...,1],40,80))[...,None]
    l=out.mean(2,keepdims=True); out=l+(out-l)*(1.08+0.12*veg)
    out=out*(1+veg*np.array([0.03,0.0,-0.04]))
    # directional warm light from left/top (sun wrap)
    full_w=full_w or w; full_h=full_h or h
    xx=(np.arange(w)[None,:]+x_off)/full_w; yy=(np.arange(h)[:,None]+sky_y_off)/full_h
    light=np.clip(1-xx,0,1)**2*0.035+np.clip(1-yy,0,1)*0.015
    out=out+light[...,None]*np.array([1.0,0.75,0.4])
    return np.clip(out,0,1).astype(np.float32)
