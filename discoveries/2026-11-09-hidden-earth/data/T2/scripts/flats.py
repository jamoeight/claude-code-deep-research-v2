# Find large low-relief interdune flats ("tati"-type surfaces where Taklamakan ruins are usually exposed)
# inside a candidate circle, from Copernicus GLO-30 (windowed COG reads).
import rasterio, numpy as np, sys, json, math
from rasterio.windows import from_bounds
from scipy.ndimage import maximum_filter, minimum_filter, uniform_filter, label, find_objects
lat0,lon0,rkm,tag=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
dlat=rkm/111.0; dlon=rkm/(111.32*math.cos(math.radians(lat0)))
S,N_,W,E=lat0-dlat,lat0+dlat,lon0-dlon,lon0+dlon
def tiles():
    for la in range(math.floor(S),math.floor(N_)+1):
        for lo in range(math.floor(W),math.floor(E)+1):
            yield la,lo
res=1/3600
H=int(round((N_-S)/res)); Wd=int(round((E-W)/res))
mos=np.full((H,Wd),np.nan,np.float32)
for la,lo in tiles():
    name=f"Copernicus_DSM_COG_10_N{la:02d}_00_E{lo:03d}_00_DEM"
    u=f"https://copernicus-dem-30m.s3.amazonaws.com/{name}/{name}.tif"
    with rasterio.open(u) as ds:
        b=(max(W,lo),max(S,la),min(E,lo+1),min(N_,la+1))
        if b[0]>=b[2] or b[1]>=b[3]: continue
        win=from_bounds(*b,transform=ds.transform).round_offsets().round_lengths()
        a=ds.read(1,window=win)
        r0=int(round((N_-b[3])/res)); c0=int(round((b[0]-W)/res))
        mos[r0:r0+a.shape[0],c0:c0+a.shape[1]]=a[:H-r0,:Wd-c0]
dem=np.nan_to_num(mos,nan=np.nanmean(mos))
k=33  # ~1 km window (lat spacing 30 m; lon ~24 m)
relief=maximum_filter(dem,k)-minimum_filter(dem,k)
# relative height vs 3 km mean: negative = trough/interdune
rel=dem-uniform_filter(dem,101)
flat=(relief<6)&(rel<0)
lab,n=label(flat)
objs=find_objects(lab)
out=[]
yy,xx=np.mgrid[0:H,0:Wd]
for i,sl in enumerate(objs,1):
    m=(lab[sl]==i); npx=m.sum()
    area=npx*30*30*math.cos(math.radians(lat0))/1e6
    if area<1.0: continue
    ry=yy[sl][m].mean(); rx=xx[sl][m].mean()
    la=N_-(ry+0.5)*res; lo=W+(rx+0.5)*res
    dk=math.hypot((la-lat0)*111,(lo-lon0)*111.32*math.cos(math.radians(lat0)))
    if dk>rkm: continue
    out.append(dict(lat=round(la,4),lon=round(lo,4),area_km2=round(area,2),dist_km=round(dk,1),mean_z=round(float(dem[sl][m].mean()),1)))
out.sort(key=lambda d:-d['area_km2'])
print(f"{tag}: box {S:.3f}-{N_:.3f}N {W:.3f}-{E:.3f}E; dem z {np.nanmin(mos):.0f}-{np.nanmax(mos):.0f} m; flats>1km2: {len(out)}; frac flat {flat.mean():.3f}")
for d in out[:12]: print("  ",d)
json.dump(out,open(f"flats_{tag}.json","w"),indent=0)
