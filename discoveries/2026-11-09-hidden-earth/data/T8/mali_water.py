import sys, numpy as np, rasterio
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from scipy import ndimage as ndi
sys.path.insert(0,'.')
import geo
# region: 11.2-13.6N, 8.8W-6.0W, at ~50 m (1/2400 deg) using nearest from 10 m WorldCover
W,S,E,N=-8.9,11.2,-6.0,13.7
res=1/2400
nx=int((E-W)/res); ny=int((N-S)/res)
out=np.zeros((ny,nx),np.uint8)
for la in (9,12):
  for lo in (-9,-6):
    u=geo.wc_url(la,lo)
    iw,is_,ie,in_=max(W,lo),max(S,la),min(E,lo+3),min(N,la+3)
    if iw>=ie or is_>=in_: continue
    with rasterio.open(u) as ds:
        win=from_bounds(iw,is_,ie,in_,ds.transform)
        h=int(round((in_-is_)/res)); w=int(round((ie-iw)/res))
        a=ds.read(1,window=win,out_shape=(h,w),resampling=Resampling.nearest)
    r0=int(round((N-in_)/res)); c0=int(round((iw-W)/res))
    out[r0:r0+h,c0:c0+w]=a
np.save('mali_wc50.npy',out)
water=(out==80)
lab,n=ndi.label(water)
sizes=ndi.sum(water,lab,range(1,n+1))
big=np.argsort(sizes)[::-1][:6]
for i in big:
    m=lab==(i+1); rr,cc=np.argwhere(m).T
    print('comp',i+1,'px',int(sizes[i]),'lat %.3f-%.3f lon %.3f-%.3f'%(N-rr.max()*res,N-rr.min()*res,W+cc.min()*res,W+cc.max()*res))
