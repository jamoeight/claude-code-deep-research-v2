"""Resumable multi-region crater scan driver. Writes data/scan/tiles/<la>_<lo>.json per tile."""
import sys, os, json, math, time
sys.path.insert(0, os.path.dirname(__file__))
from concurrent.futures import ThreadPoolExecutor, as_completed
import scan_craters as sc

REGIONS = {
    "W_Sahara":   (15, 27, -17, -3),
    "C_Sahara":   (15, 32, -3, 25),
    "E_Sahara":   (15, 30, 25, 37),
    "Arabia":     (15, 32, 36, 56),
    "Australia":  (-32, -18, 115, 140),
    "Atacama":    (-28, -18, -71, -66),
    "Namib_Kalahari": (-28, -17, 12, 26),
    "Iran_Afghan": (25, 37, 52, 70),
    "C_Asia":     (37, 48, 50, 75),
    "Gobi_Tarim": (36, 46, 75, 112),
    "Patagonia":  (-50, -38, -72, -64),
    "US_SW_Mex":  (25, 40, -120, -103),
}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "scan", "tiles")
os.makedirs(OUT, exist_ok=True)

def job(t):
    la, lo = t
    fn = os.path.join(OUT, f"{la}_{lo}.json")
    if os.path.exists(fn):
        return t, None
    for attempt in range(3):
        try:
            res = sc.scan_tile(la, lo)
            json.dump(res, open(fn, "w"))
            return t, len(res)
        except Exception as e:
            err = repr(e)
            time.sleep(3)
    json.dump({"error": err}, open(fn + ".err", "w"))
    return t, -1

order = sys.argv[1:] or list(REGIONS)
for name in order:
    a0, a1, o0, o1 = REGIONS[name]
    tiles = [(la, lo) for la in range(a0, a1) for lo in range(o0, o1)]
    t0 = time.time(); n = 0
    with ThreadPoolExecutor(int(os.environ.get("NTH", "6"))) as ex:
        for f in as_completed([ex.submit(job, t) for t in tiles]):
            n += 1
    print(f"{name}: {len(tiles)} tiles in {time.time()-t0:.0f}s", flush=True)
