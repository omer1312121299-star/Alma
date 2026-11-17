import numpy as np, cv2, sys
sys.path.insert(0,'.'); from look import grade
big=cv2.imread('work/up4b.png')[:,:,::-1]; d=np.load('work/disp.npy')
OW,OH=2576,1912
shots={'B':(1240,860,1300),'C':(1500,880,640),'D':(1255,1500,1150),'E':(1250,520,1500),'F':(2010,940,1150),'G':(700,1560,1250)}
for k,(cx,cy,w) in shots.items():
    h=w*704/1248; x0=int(cx-w/2); y0=int(cy-h/2); x0=max(0,min(x0,OW-w)); y0=max(0,min(int(y0),int(OH-h)))
    S=1248/w; sub=big[int(y0*4):int((y0+h)*4),int(x0*4):int((x0+w)*4)]
    t=cv2.resize(sub,(1248,704),interpolation=cv2.INTER_AREA).astype(np.float32)/255
    dd=cv2.resize(d[y0:int(y0+h),x0:x0+w],(1248,704))
    g=grade(t,dd,sky_y_off=y0*S,full_h=OH*S,x_off=x0*S,full_w=OW*S,S=S)
    cv2.imwrite(f'ai/in_{k}.png',(g[:,:,::-1]*255+.5).astype(np.uint8)); print(k)
