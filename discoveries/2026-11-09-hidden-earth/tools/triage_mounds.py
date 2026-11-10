"""Rank mound-scan output per zone; tag ones near a Pleiades-located place; emit contact-sheet jsons."""
import json, csv, math, sys, os, glob
D = os.path.join(os.path.dirname(__file__), "..")
csv.field_size_limit(10**9)
P = []
for r in csv.DictReader(open(f"{D}/data/T1/pleiades/places.csv", encoding="utf-8-sig")):
    try:
        la, lo = float(r["representative_latitude"]), float(r["representative_longitude"])
    except Exception:
        continue
    P.append((la, lo, r["title"]))
import numpy as np
PA = np.array([[a, b] for a, b, _ in P])
def near_pleiades(la, lo, km=1.5):
    d = np.hypot(PA[:, 0] - la, (PA[:, 1] - lo) * math.cos(math.radians(la))) * 111
    i = int(np.argmin(d))
    return (P[i][2], round(float(d[i]), 2)) if d[i] < km else ("", round(float(d[i]), 1))
zone = sys.argv[1]; topn = int(sys.argv[2]) if len(sys.argv) > 2 else 20
rows = json.load(open(f"{D}/data/private/mounds/{zone}.json"))
for r in rows:
    r["size"] = r["area_ha"] * min(r["rel_m"], 30)
    r["pleiades"], r["pl_km"] = near_pleiades(r["lat"], r["lon"])
sel = [r for r in rows if r["rel_m"] >= 4 and r["nbr3km"] <= 4]
sel.sort(key=lambda r: -r["size"])
print(zone, len(rows), "mounds;", len(sel), "pass;", sum(1 for r in sel if r["pleiades"]), "near Pleiades")
for i, r in enumerate(sel[:topn]):
    print(f"{zone[:4]}{i:02d}", r["lat"], r["lon"], r["area_ha"], "ha", r["rel_m"], "m", "nbr", r["nbr3km"], "|", r["pleiades"][:40], r["pl_km"])
json.dump([{"id": f"M-{zone[:6]}-{i:02d}", "lat": r["lat"], "lon": r["lon"], "half_km": max(0.8, math.sqrt(r["area_ha"] / 100) * 2.5)} for i, r in enumerate(sel[:topn])],
          open(f"{D}/data/private/mounds/{zone}_sheet.json", "w"))
json.dump(sel, open(f"{D}/data/private/mounds/{zone}_ranked.json", "w"))
