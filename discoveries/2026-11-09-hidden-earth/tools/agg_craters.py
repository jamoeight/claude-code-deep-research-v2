import json, glob, os, sys, math, csv
D = os.path.join(os.path.dirname(__file__), "..", "data")
rows = []
for f in glob.glob(f"{D}/scan/tiles/*.json"):
    r = json.load(open(f))
    if isinstance(r, list): rows += r
known = []
kp = f"{D}/T4/known_impact_structures.csv"
if os.path.exists(kp):
    for k in csv.DictReader(open(kp)):
        try: known.append((float(k["lat"]), float(k["lon"]), k["name"], float(k.get("diameter_km") or 1)))
        except Exception: pass
def hav(a, b, c, d):
    p = math.pi / 180
    return 6371 * 2 * math.asin(math.sqrt(math.sin((c - a) * p / 2) ** 2 + math.cos(a * p) * math.cos(c * p) * math.sin((d - b) * p / 2) ** 2))
smin = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
# isolation: real craters rarely sit in fields of similar depressions (dunes, karst, thermokarst)
import numpy as np
LL = np.array([[r["lat"], r["lon"]] for r in rows]) if rows else np.zeros((0, 2))
for r in rows:
    d = np.hypot(LL[:, 0] - r["lat"], (LL[:, 1] - r["lon"]) * math.cos(math.radians(r["lat"]))) * 111
    r["nbr5km"] = int((d < 5).sum() - 1)
sel = [r for r in rows if r["nbr5km"] <= 2 and r["score"] >= smin and r["frac_rim_raised"] >= 0.67 and r["circ"] >= 0.75]
for r in sel:
    r["known"] = ""
    for la, lo, n, dk in known:
        if hav(r["lat"], r["lon"], la, lo) < max(2.0, dk):
            r["known"] = n; break
sel.sort(key=lambda r: -r["score"])
print(len(rows), "raw;", len(sel), "pass;", sum(1 for r in sel if r["known"]), "match known;", len(known), "known list")
json.dump(sel, open(f"{D}/scan/candidates.json", "w"), indent=0)
for r in sel[:40]:
    print(r["lat"], r["lon"], r["nbr5km"], r["diam_m"], r["depth_m"], r["circ"], r["frac_rim_raised"], r["rim_relief_m"], r["score"], r["known"])
