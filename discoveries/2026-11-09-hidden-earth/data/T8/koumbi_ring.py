"""Ghana royal town (al-Ghaba) search ring around Koumbi Saleh.
al-Bakri (1068): two towns on a plain, king's town 6 miles from the Muslim town, continuous
habitation between.  6 miles = 8.9 km (Roman mile 1.48 km) .. 11.8 km (Arab mile ~1.97 km).
We map: (a) DEM mound signature, calibrated on Koumbi Saleh itself; (b) closed depressions
(seasonal ponds = water for a town); (c) WorldCover tree cover ("al-ghaba" = the grove)."""
import sys, json
import numpy as np
from scipy import ndimage as ndi
from skimage.morphology import reconstruction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import geo

KS = (15.765684, -7.968710)  # Pleiades 41177950
b = geo.box(*KS, 17.0)
z = geo.dem(b)
print("DEM", z.shape, np.nanmin(z), np.nanmax(z))
lat, lon = geo.grid_latlon(b, z.shape)
d = np.vectorize(lambda a, o: 0)(0, 0)
# distance grid (fast approx, local equirectangular)
kx = 111.32 * np.cos(np.radians(KS[0])); ky = 110.57
D = np.hypot((lon - KS[1]) * kx, (lat - KS[0]) * ky)
az = (np.degrees(np.arctan2((lon - KS[1]) * kx, (lat - KS[0]) * ky)) + 360) % 360

# residual relief: DEM minus 1.5 km median (removes dune/plain trend)
med = ndi.median_filter(z, size=51)
res = z - med
r0, c0 = np.unravel_index(np.argmin(D), D.shape)
win = res[r0-12:r0+13, c0-12:c0+13]
print("Koumbi Saleh residual relief within +-360 m: max %.2f m, mean %.2f m" % (np.nanmax(win), np.nanmean(win)))
print("KS DEM elev %.1f, local 1.5km median %.1f" % (z[r0, c0], med[r0, c0]))

# closed depressions
seed = z.copy(); seed[1:-1, 1:-1] = np.nanmax(z)
filled = reconstruction(seed, z, method="erosion")
depth = filled - z

# D8 flow accumulation on filled+tiny gradient
zz = filled + 1e-4 * D  # tiny tilt to route flats outward-ish (diagnostic only)
ny, nx = zz.shape
order = np.argsort(zz, axis=None)[::-1]
acc = np.ones(ny * nx, dtype=np.float64)
flat = zz.ravel()
nbr = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
for idx in order:
    r, c = divmod(idx, nx)
    best = None; bz = flat[idx]
    for dr, dc in nbr:
        rr, cc = r+dr, c+dc
        if 0 <= rr < ny and 0 <= cc < nx:
            v = flat[rr*nx+cc]
            dz = (bz - v) / (1.414 if dr and dc else 1.0)
            if dz > 0 and (best is None or dz > best[0]):
                best = (dz, rr*nx+cc)
    if best: acc[best[1]] += acc[idx]
acc = acc.reshape(ny, nx)
cell_km2 = (30.8 * 30.8 * np.cos(np.radians(KS[0]))) / 1e6

ring = (D >= 8.5) & (D <= 12.5)
out = {"koumbi": {"elev": float(z[r0, c0]), "res_max": float(np.nanmax(win))}}

# (a) mound components in ring with residual > 1.5 m
lab, n = ndi.label((res > 1.5) & ring)
mounds = []
for i in range(1, n+1):
    m = lab == i
    a_ha = m.sum() * cell_km2 * 100
    if a_ha < 3: continue
    rr, cc = np.argwhere(m).mean(0).astype(int)
    mounds.append(dict(lat=round(float(lat[rr, cc]),5), lon=round(float(lon[rr, cc]),5), area_ha=round(a_ha,1),
                       peak_res=round(float(res[m].max()),2), dist_km=round(float(D[rr, cc]),2), az=round(float(az[rr, cc]))))
mounds.sort(key=lambda x: -x["peak_res"] * x["area_ha"])
out["mounds_top"] = mounds[:15]
print("mound comps in ring:", len(mounds))

# (b) closed depressions > 0.8 m deep & > 5 ha anywhere within 14 km
lab, n = ndi.label((depth > 0.8) & (D <= 14))
deps = []
for i in range(1, n+1):
    m = lab == i
    a_ha = m.sum() * cell_km2 * 100
    if a_ha < 5: continue
    rr, cc = np.unravel_index(np.argmax(np.where(m, depth, -1)), m.shape)
    deps.append(dict(lat=round(float(lat[rr, cc]),5), lon=round(float(lon[rr, cc]),5), area_ha=round(a_ha,1),
                     max_depth=round(float(depth[m].max()),2), dist_km=round(float(D[rr, cc]),2), az=round(float(az[rr, cc]))))
deps.sort(key=lambda x: -x["area_ha"])
out["depressions"] = deps[:20]

# (c) main drainage lines: cells with acc > 20 km2, report where they cross the ring
ch = (acc * cell_km2 > 20)
out["channel_cells_in_ring"] = int((ch & ring).sum())
chring = np.argwhere(ch & ring)
pts = []
for rr, cc in chring[:: max(1, len(chring)//25)]:
    pts.append(dict(lat=round(float(lat[rr, cc]),4), lon=round(float(lon[rr, cc]),4), acc_km2=round(float(acc[rr, cc]*cell_km2),1), az=round(float(az[rr, cc]))))
out["channel_samples_ring"] = pts
# channel near KS?
near = ch & (D < 3)
out["channel_within_3km_of_KS"] = int(near.sum())
if near.any():
    rr, cc = np.unravel_index(np.argmax(np.where(near, acc, 0)), acc.shape)
    out["ks_channel_max"] = dict(lat=float(lat[rr, cc]), lon=float(lon[rr, cc]), acc_km2=float(acc[rr, cc]*cell_km2), dist=float(D[rr, cc]))

# elevation profile by azimuth sector in ring (mean elev) -> which way is "down-valley"
sect = {}
for s in range(0, 360, 30):
    m = ring & (az >= s) & (az < s+30)
    sect[s] = round(float(np.nanmean(z[m])), 1)
out["ring_mean_elev_by_sector"] = sect
np.save(__file__.rsplit("/",1)[0] + "/koumbi_acc.npy", acc.astype("float32"))
json.dump(out, open(__file__.rsplit("/",1)[0] + "/koumbi_ring_dem.json", "w"), indent=1)
print(json.dumps(out, indent=1)[:6000])
