# Steepest-descent flow lines on a heavily smoothed Copernicus GLO-30 DEM (overview ~250 m),
# used as a proxy for regional palaeo-drainage axes beyond present river termini.
import numpy as np, sys, json
from scipy.ndimage import gaussian_filter
dem=np.load(sys.argv[1]); LAT1,LON0,N=41,79,450
res=1.0/N
dem=np.where(np.isfinite(dem),dem,np.nanmax(dem))
SIG=float(sys.argv[2]) if len(sys.argv)>2 else 12
S=gaussian_filter(dem.astype(np.float64),SIG)
def rc(lat,lon): return int((LAT1-lat)/res), int((lon-LON0)/res)
def ll(r,c): return LAT1-(r+0.5)*res, LON0+(c+0.5)*res
nb=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
def trace(lat,lon,maxsteps=4000):
    r,c=rc(lat,lon); path=[(r,c)]
    for _ in range(maxsteps):
        z=S[r,c]; best=None; bz=z
        for dr,dc in nb:
            rr,cc=r+dr,c+dc
            if 0<=rr<S.shape[0] and 0<=cc<S.shape[1]:
                # distance-weighted slope (lon spacing ~0.79 of lat spacing at 38N)
                dist=np.hypot(dr, dc*0.79)
                s=(z-S[rr,cc])/dist
                if s>0 and (best is None or s>bs): best=(rr,cc); bs=s
        if best is None: break
        r,c=best; path.append((r,c))
    return [ll(r,c)+(float(dem[r,c]),) for r,c in path]
seeds=json.loads(sys.argv[3])
out={}
for name,(la,lo) in seeds.items():
    p=trace(la,lo); out[name]=p
    pts=p[::max(1,len(p)//12)]+[p[-1]]
    print(f"{name}: {len(p)} steps; end {p[-1][0]:.3f},{p[-1][1]:.3f}")
    print("   "+"; ".join(f"{a:.3f},{b:.3f}({z:.0f}m)" for a,b,z in pts))
json.dump(out,open(sys.argv[4],'w'))
