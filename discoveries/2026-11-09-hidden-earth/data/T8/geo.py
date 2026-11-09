"""T8 helper: windowed reads of Copernicus GLO-30 DEM and ESA WorldCover 2021 (10 m)
from public S3, plus geodesic helpers. Small windows only (no bulk downloads)."""
import math
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from pyproj import Geod

G = Geod(ellps="WGS84")

def _hemi(v, pos, neg, width):
    return (pos if v >= 0 else neg) + f"{abs(int(v)):0{width}d}"

def dem_url(lat_floor, lon_floor):
    ns = _hemi(lat_floor, "N", "S", 2)
    ew = _hemi(lon_floor, "E", "W", 3)
    name = f"Copernicus_DSM_COG_10_{ns}_00_{ew}_00_DEM"
    return f"/vsicurl/https://copernicus-dem-30m.s3.amazonaws.com/{name}/{name}.tif"

def wc_url(lat3, lon3):
    ns = _hemi(lat3, "N", "S", 2)
    ew = _hemi(lon3, "E", "W", 3)
    return ("/vsicurl/https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/"
            f"ESA_WorldCover_10m_2021_v200_{ns}{ew}_Map.tif")

def _mosaic(bounds, urls_for, res):
    """bounds=(W,S,E,N). Returns array on a regular grid of step res (deg), north-up."""
    W, S, E, N = bounds
    nx = int(round((E - W) / res)); ny = int(round((N - S) / res))
    out = np.full((ny, nx), np.nan, dtype="float32")
    for url, (tw, ts, te, tn) in urls_for(bounds):
        iw, is_, ie, in_ = max(W, tw), max(S, ts), min(E, te), min(N, tn)
        if iw >= ie or is_ >= in_:
            continue
        try:
            with rasterio.open(url) as ds:
                win = from_bounds(iw, is_, ie, in_, ds.transform)
                a = ds.read(1, window=win, boundless=True, fill_value=np.nan if ds.dtypes[0].startswith("float") else 0)
        except Exception as e:  # missing tile (ocean) etc.
            print("tile missing", url, e)
            continue
        c0 = int(round((iw - W) / res)); r0 = int(round((N - in_) / res))
        h = min(a.shape[0], ny - r0); w = min(a.shape[1], nx - c0)
        out[r0:r0 + h, c0:c0 + w] = a[:h, :w]
    return out

def dem(bounds):
    def urls(b):
        W, S, E, N = b
        for la in range(math.floor(S), math.ceil(N)):
            for lo in range(math.floor(W), math.ceil(E)):
                yield dem_url(la, lo), (lo, la, lo + 1, la + 1)
    return _mosaic(bounds, urls, 1 / 3600)

def worldcover(bounds):
    def urls(b):
        W, S, E, N = b
        for la in range(3 * math.floor(S / 3), 3 * math.ceil(N / 3), 3):
            for lo in range(3 * math.floor(W / 3), 3 * math.ceil(E / 3), 3):
                yield wc_url(la, lo), (lo, la, lo + 3, la + 3)
    return _mosaic(bounds, urls, 1 / 12000)

def box(lat, lon, half_km):
    dlat = half_km / 111.32
    dlon = half_km / (111.32 * math.cos(math.radians(lat)))
    return (lon - dlon, lat - dlat, lon + dlon, lat + dlat)

def grid_latlon(bounds, shape):
    W, S, E, N = bounds
    ny, nx = shape
    lats = N - (np.arange(ny) + 0.5) * (N - S) / ny
    lons = W + (np.arange(nx) + 0.5) * (E - W) / nx
    return np.meshgrid(lats, lons, indexing="ij")

def dist_km(lat1, lon1, lat2, lon2):
    _, _, d = G.inv(lon1, lat1, lon2, lat2)
    return d / 1000.0

def inv(lat1, lon1, lat2, lon2):
    az, _, d = G.inv(lon1, lat1, lon2, lat2)
    return (az % 360), d / 1000.0

def fwd(lat, lon, az, km):
    lo, la, _ = G.fwd(lon, lat, az, km * 1000.0)
    return la, lo
