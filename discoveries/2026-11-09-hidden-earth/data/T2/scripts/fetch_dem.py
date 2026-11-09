# Fetch Copernicus GLO-30 DEM tiles at overview level 8 (~250 m) and mosaic.
import rasterio, numpy as np, sys
from rasterio.enums import Resampling
from concurrent.futures import ThreadPoolExecutor
LAT0,LAT1,LON0,LON1 = 36,41,79,87   # tile lower-left corners lat in [36,40], lon in [79,86]
N=450
def tile(lat,lon):
    name=f"Copernicus_DSM_COG_10_N{lat:02d}_00_E{lon:03d}_00_DEM"
    u=f"https://copernicus-dem-30m.s3.amazonaws.com/{name}/{name}.tif"
    try:
        with rasterio.open(u) as ds:
            a=ds.read(1,out_shape=(N,N),resampling=Resampling.average)
        return lat,lon,a
    except Exception as e:
        print("miss",lat,lon,e,file=sys.stderr); return lat,lon,None
jobs=[(la,lo) for la in range(LAT0,LAT1) for lo in range(LON0,LON1)]
mos=np.full(((LAT1-LAT0)*N,(LON1-LON0)*N),np.nan,dtype=np.float32)
with ThreadPoolExecutor(8) as ex:
    for la,lo,a in ex.map(lambda j: tile(*j), jobs):
        if a is None: continue
        r=(LAT1-1-la)*N; c=(lo-LON0)*N
        mos[r:r+N,c:c+N]=a
np.save(sys.argv[1],mos)
print(mos.shape, np.nanmin(mos), np.nanmax(mos))
