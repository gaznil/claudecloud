# usage: track_place.py in_video art.jpg out.mp4 x1 y1 x2 y2 x3 y3 x4 y4 [blur] [haze]
import sys, subprocess, numpy as np, cv2, json
inp, artp, out = sys.argv[1:4]
q = np.array(list(map(float, sys.argv[4:12])), np.float32).reshape(4,2)
blur = float(sys.argv[12]) if len(sys.argv)>12 else 0.7
haze = float(sys.argv[13]) if len(sys.argv)>13 else 0.07
pr = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=r_frame_rate','-of','json',inp]))
fps = pr['streams'][0]['r_frame_rate']
# decode with rotation applied
dec = subprocess.Popen(['ffmpeg','-v','error','-i',inp,'-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
_f=subprocess.check_output(['ffmpeg','-v','error','-i',inp,'-frames:v','1','-f','image2pipe','-vcodec','png','-']); _i=cv2.imdecode(np.frombuffer(_f,np.uint8),1); h,w=_i.shape[:2]
enc = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r',fps,'-i','-','-c:v','libx264','-crf','14','-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart',out],stdin=subprocess.PIPE)
art = cv2.imread(artp); ah,aw = art.shape[:2]
A = cv2.getPerspectiveTransform(np.float32([[0,0],[aw,0],[aw,ah],[0,ah]]), q)
sift = cv2.SIFT_create(4000)
ref=None; kp0=des0=None; mask0=None
bf = cv2.BFMatcher()
prevH = np.eye(3)
n=0
while True:
    buf = dec.stdout.read(w*h*3)
    if len(buf)<w*h*3: break
    f = np.frombuffer(buf,np.uint8).reshape(h,w,3).copy()
    g = cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    if ref is None:
        # features on the board plus a margin (rigid structure around it)
        mask0 = np.zeros_like(g); c=q.mean(0); qq=(q-c)*1.35+c
        cv2.fillPoly(mask0,[qq.astype(np.int32)],255)
        kp0,des0 = sift.detectAndCompute(g,mask0); ref=g; H=np.eye(3)
    else:
        kp,des = sift.detectAndCompute(g,None)
        H=prevH
        if des is not None and len(kp)>10:
            m = bf.knnMatch(des0,des,k=2)
            good=[a for a,b in (x for x in m if len(x)==2) if a.distance<0.7*b.distance]
            if len(good)>=12:
                s=np.float32([kp0[a.queryIdx].pt for a in good]); d=np.float32([kp[a.trainIdx].pt for a in good])
                Hn,_=cv2.findHomography(s,d,cv2.RANSAC,3.0)
                if Hn is not None: H=Hn
    prevH=H
    M = H@A
    wa = cv2.warpPerspective(art,M,(w,h),flags=cv2.INTER_CUBIC)
    mk = cv2.warpPerspective(np.full((ah,aw),255,np.uint8),M,(w,h))
    if blur>0: wa=cv2.GaussianBlur(wa,(0,0),blur); mk=cv2.GaussianBlur(mk,(0,0),0.8)
    wa = wa.astype(np.float32)
    mean = wa.mean(axis=2,keepdims=True); wa = mean+(wa-mean)*0.9
    wa = (wa-128)*0.88+128
    wa = wa*(1-haze)+np.array([214,208,205],np.float32)*haze
    a = (mk.astype(np.float32)/255)[...,None]
    o = (wa*a + f.astype(np.float32)*(1-a)).clip(0,255).astype(np.uint8)
    enc.stdin.write(o.tobytes()); n+=1
enc.stdin.close(); enc.wait(); print('frames',n,w,h)
