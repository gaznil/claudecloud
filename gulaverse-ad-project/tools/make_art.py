# make_art.py poster out aspect  -> pads poster top with navy to reach W/H = aspect
import sys, numpy as np
from PIL import Image
p=Image.open(sys.argv[1]).convert('RGB'); out=sys.argv[2]; r=float(sys.argv[3])
W=p.width; H=max(p.height,int(W/r)); ex=H-p.height
pc=p.copy(); pc.paste(p.crop((220,30,380,190)),(40,30))
row=np.array(pc.crop((0,2,W,20)).resize((W,1),Image.BOX)).astype(float)
a=np.zeros((H,W,3)); a[:ex]=np.repeat(row,ex,0); a[ex:]=np.array(pc)
art=Image.fromarray(a.clip(0,255).astype('uint8')); art.paste(p.crop((40,30,200,190)),(40,40 if ex else 30)); art.save(out,quality=97)
