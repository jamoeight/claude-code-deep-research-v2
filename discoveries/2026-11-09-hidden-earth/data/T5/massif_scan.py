#!/usr/bin/env python3
"""Find isolated massifs (inselbergs / sky islands) from Copernicus GLO-30 DEM
read at a coarse overview. A massif = local maximum whose summit stands
> MIN_RELIEF m above the 10th-percentile elevation of a ~RING km window.
Usage: python3 -I massif_scan.py S N W E [min_relief_m] [ring_km]
Outputs CSV lines: lat,lon,summit_m,base_m,relief_m
"""
import math, os, sys
os.environ.setdefault("AWS_NO_SIGN_REQUEST", "YES")
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
import numpy as np
import rasterio
from scipy import ndimage

S, N, W, E = map(float, sys.argv[1:5])
MIN_RELIEF = float(sys.argv[5]) if len(sys.argv) > 5 else 700
RING_KM = float(sys.argv[6]) if len(sys.argv) > 6 else 20
STEP = 1 / 400.0  # ~ 280 m grid

ny = int(round((N - S) / STEP)); nx = int(round((E - W) / STEP))
grid = np.full((ny, nx), np.nan, dtype=np.float32)
for la in range(int(math.floor(S)), int(math.ceil(N))):
    for lo in range(int(math.floor(W)), int(math.ceil(E))):
        ns = ("N%02d" % la) if la >= 0 else ("S%02d" % -la)
        ew = ("E%03d" % lo) if lo >= 0 else ("W%03d" % -lo)
        name = f"Copernicus_DSM_COG_10_{ns}_00_{ew}_00_DEM"
        p = f"s3://copernicus-dem-30m/{name}/{name}.tif"
        try:
            with rasterio.open(p) as ds:
                a = ds.read(1, out_shape=(400, 400)).astype(np.float32)
        except Exception:
            continue  # ocean
        r0 = int(round((N - (la + 1)) / STEP)); c0 = int(round((lo - W) / STEP))
        rs, cs = max(r0, 0), max(c0, 0)
        re_, ce = min(r0 + 400, ny), min(c0 + 400, nx)
        if rs < re_ and cs < ce:
            grid[rs:re_, cs:ce] = a[rs - r0:re_ - r0, cs - c0:ce - c0]

g = np.nan_to_num(grid, nan=0.0)
k = max(3, int(RING_KM / 0.28))
loc_max = (g == ndimage.maximum_filter(g, size=int(8 / 0.28)))  # summit dominant within ~8 km
base = ndimage.percentile_filter(g, 10, size=k)
relief = g - base
cand = np.argwhere(loc_max & (relief > MIN_RELIEF))
for r, c in cand:
    lat = N - (r + 0.5) * STEP; lon = W + (c + 0.5) * STEP
    print(f"{lat:.3f},{lon:.3f},{int(g[r, c])},{int(base[r, c])},{int(relief[r, c])}")
