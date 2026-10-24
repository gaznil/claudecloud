# fix_text.py in.mp4 art.jpg out.mp4 : re-print the exact small text of the creative onto an AI-generated ad, tracked per frame
import sys, subprocess, numpy as np, cv2
inp, artp, out = sys.argv[1:4]
art = cv2.imread(artp); ah, aw = art.shape[:2]
# text regions in creative coords (x0,y0,x1,y1)
boxes = [(380,215,760,320),(460,555,640,640),(160,1100,640,1160),(1200,1112,1880,1170),(40,30,200,190)]
regm = np.zeros((ah,aw),np.uint8)
for x0,y0,x1,y1 in boxes: regm[y0:y1,x0:x1]=255
regm = cv2.GaussianBlur(regm,(0,0),6)
cap = cv2.VideoCapture(inp); fps = cap.get(5); W=int(cap.get(3)); H=int(cap.get(4))
enc = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-c:v','libx264','-crf','14','-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart',out],stdin=subprocess.PIPE)
sift = cv2.SIFT_create(6000); small = cv2.resize(art,(aw//4,ah//4)); ks,ds = sift.detectAndCompute(cv2.cvtColor(small,cv2.COLOR_BGR2GRAY),None)
bf = cv2.BFMatcher(); Hs=[]; frames=[]
while True:
    ok,f = cap.read()
    if not ok: break
    frames.append(f)
    k,d = sift.detectAndCompute(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),None)
    m=[a for a,b in bf.knnMatch(ds,d,k=2) if a.distance<0.75*b.distance]
    Hm=None
    if len(m)>=15:
        Hm,_=cv2.findHomography(np.float32([ks[x.queryIdx].pt for x in m])*4,np.float32([k[x.trainIdx].pt for x in m]),cv2.RANSAC,2.5)
    Hs.append(Hm)
# fill gaps + temporal smoothing of corner tracks
corn = np.float32([[0,0],[aw,0],[aw,ah],[0,ah]]).reshape(-1,1,2)
C=[cv2.perspectiveTransform(corn,H).reshape(-1) if H is not None else None for H in Hs]
idx=[i for i,c in enumerate(C) if c is not None]
C=np.array([C[min(idx,key=lambda j:abs(j-i))] if C[i] is None else C[i] for i in range(len(C))])
Cs=C.copy()
for i in range(len(C)):
    lo,hi=max(0,i-2),min(len(C),i+3); Cs[i]=C[lo:hi].mean(0)
print('tracked',len(idx),'of',len(C))
for f,c in zip(frames,Cs):
    M=cv2.getPerspectiveTransform(corn.reshape(-1,2),c.reshape(4,2).astype(np.float32))
    wa=cv2.warpPerspective(art,M,(W,H),flags=cv2.INTER_AREA).astype(np.float32)
    wm=cv2.warpPerspective(regm,M,(W,H)).astype(np.float32)/255
    full=cv2.warpPerspective(np.full((ah,aw),255,np.uint8),M,(W,H))>0
    # match tone/blur of the generated ad
    wa=cv2.GaussianBlur(wa,(0,0),0.9)
    ff=f.astype(np.float32); sel=full&(wm>0.5)
    for ch in range(3):
        x=cv2.GaussianBlur(wa[...,ch],(0,0),3)[sel]; y=cv2.GaussianBlur(ff[...,ch],(0,0),3)[sel]
        A=np.vstack([x,np.ones_like(x)]).T; gsl,off=np.linalg.lstsq(A,y,rcond=None)[0]
        wa[...,ch]=wa[...,ch]*gsl+off
    # keep things in front (wires: dark unsaturated thin; palm: green)
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV); g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32)
    bh=cv2.morphologyEx(g,cv2.MORPH_BLACKHAT,np.ones((7,7),np.uint8))
    wire=((bh>18)&(hsv[...,1]<60)&(g<110)).astype(np.uint8)
    wire=cv2.dilate(cv2.morphologyEx(wire,cv2.MORPH_OPEN,np.ones((1,11),np.uint8)),np.ones((2,2),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(wire)
    wire=np.isin(lab,[i for i in range(1,n) if st[i,2]>=150])
    palm=((hsv[...,0]>28)&(hsv[...,0]<95)&(hsv[...,1]>50))
    occ=cv2.GaussianBlur(cv2.dilate((wire|palm).astype(np.uint8),np.ones((3,3),np.uint8)).astype(np.float32),(0,0),0.8)
    a=(wm*(1-occ))[...,None]
    o=(wa*a+ff*(1-a)).clip(0,255).astype(np.uint8)
    enc.stdin.write(o.tobytes())
enc.stdin.close(); enc.wait()
