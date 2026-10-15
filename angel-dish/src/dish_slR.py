"""y-plane sections near the right end.  python3 dish_slR.py out.png y1 y2 y3 y4"""
import sys
import numpy as np
from PIL import Image, ImageDraw
from sdf import Field
import dish
h=0.2; panels=[]
ys=[float(v) for v in sys.argv[2:]] or [-38,-28,-16,-4]
for yv in ys:
    lo,hi=(40,yv-h,-1),(92,yv+h,40)
    F=dish.component(Field(lo,hi,h)); sl=F.G[:,F.G.shape[1]//2]
    img=np.where(sl.T[::-1]<0,0,1); rgb=np.zeros(img.shape+(3,),np.uint8); rgb[img==0]=(230,140,150); rgb[img==1]=(250,250,250)
    im=Image.fromarray(rgb).resize((rgb.shape[1]*2,rgb.shape[0]*2),Image.NEAREST); d=ImageDraw.Draw(im)
    W,H=im.size
    for g in range(40,92,5):
        x=(g-lo[0])/h*2; d.line((x,0,x,H),fill=(120,120,255) if g%10==0 else (200,200,255))
    for z in range(0,40,5):
        y=H-(z-lo[2])/h*2; d.line((0,y,W,y),fill=(120,120,255) if z%10==0 else (200,200,255))
    d.text((5,5),f'y={yv}',fill=(0,0,0)); panels.append(im)
W=max(p.size[0] for p in panels); n=len(panels)
o=Image.new('RGB',(W*2+4,(panels[0].size[1]+4)*((n+1)//2)),'white')
for i,p in enumerate(panels): o.paste(p,((i%2)*(W+4),(i//2)*(p.size[1]+4)))
o.save(sys.argv[1]); print(o.size)
