"""T8 itinerary / text math. All inputs printed; see notes file for sources."""
import sys, math
sys.path.insert(0, '.')
import geo
from pyproj import Geod
P = lambda *a: print(*a)

P("=== C1 Ghana royal town (al-Ghaba) ring around Koumbi Saleh ===")
KS = (15.765684, -7.968710)
for name, mile_km in [("Roman mile 1.48 km", 1.48), ("Arab mile 1.85 km (low)", 1.85), ("Arab mile 1.97 km", 1.97)]:
    P("  6 x %-24s = %.1f km" % (name, 6 * mile_km))
# plain-floor arc from DEM profiles: az 300-010, d 8.9-11.8 km, floor 233-238 m
c = geo.fwd(*KS, 330, 10.3)
P("  arc centroid (az 330, 10.3 km): %.4f, %.4f" % c)
for az in (300, 330, 0):
    for d in (8.9, 11.8):
        P("   arc corner az %3d d %.1f -> %.4f, %.4f" % ((az, d) + geo.fwd(*KS, az, d)))
for nm, p in [("DEM depression A (137 ha, 7 m)", (15.85467, -8.00786)), ("DEM depression B (112 ha, 2.2 m)", (15.85273, -7.96288)),
              ("WorldCover built px cluster", (15.8246, -7.9920)), ("modern pond+trees NE", (15.883, -7.866))]:
    az, d = geo.inv(*KS, *p); P("  %-34s %.4f,%.4f  az %3.0f  d %.1f km" % (nm, p[0], p[1], az, d))

P("\n=== C4/C5 Mali capital: Walata -> candidates, 24 days 'travelling rapidly' ===")
WAL = (17.2996, -7.0249)
cands = {"Niani (Guinea)": (11.37, -8.39), "Kangaba": (11.9404, -8.4175), "Niger/Sankarani wedge (S of confluence)": (11.88, -8.38),
         "Bamako": (12.6524, -7.9993), "Koulikoro (Hunwick corridor W)": (12.8549, -7.5742),
         "Hunwick corridor mid (left bank)": (13.10, -7.05), "Segou": (13.4287, -6.2544)}
for k, p in cands.items():
    az, d = geo.inv(*WAL, *p)
    P("  %-40s bearing %3.0f  gc %4.0f km  route(x1.25) %4.0f km  -> %4.1f km/day over 24 d; Zaghari at day 10 = %3.0f km route" % (k, az, d, d*1.25, d*1.25/24, d*1.25*10/24))
CONF = (12.01, -8.33)
P("  Niger-Sankarani confluence (WorldCover water trace) ~ %.2f, %.2f" % CONF)
for k in ("Bamako", "Koulikoro (Hunwick corridor W)", "Hunwick corridor mid (left bank)", "Segou", "Kangaba", "Niani (Guinea)"):
    az, d = geo.inv(*CONF, *cands[k]); P("   confluence -> %-34s %3.0f km" % (k, d))
P("  10 miles = %.1f km (Roman) .. %.1f km (Arab 1.97)" % (14.8, 19.7))
# locus: capital 15-20 km beyond a Sankarani crossing near the confluence, inside the wedge (heading SW)
for az in (200, 215, 230):
    for d in (14.8, 19.7):
        P("   wedge locus az %d d %.1f -> %.3f, %.3f" % ((az, d) + geo.fwd(*CONF, az, d)))

P("\n=== C2 Njimi = Tie: 'about 45 km east of Mao' ===")
MAO = (14.1215, 15.3122)
for d in (40, 45, 50):
    P("  Mao + %d km @ 90 -> %.4f, %.4f" % ((d,) + geo.fwd(*MAO, 90, d)))

P("\n=== C3 La Navidad: Diario geometry ===")
PIC = (19.783, -72.195)   # NE tip of Cap-Haitien headland from WorldCover land/water
EBS = (19.725, -72.125)   # approx. En Bas Saline (Bord de Mer de Limonade area)
az, d = geo.inv(*PIC, *EBS); P("  Picolet -> EBS: az %.0f, %.2f km" % (az, d))
g = Geod(ellps="WGS84")
def circle_intersections(p1, r1, p2, r2):
    # local planar (equirectangular) intersection, km
    lat0 = (p1[0] + p2[0]) / 2; kx = 111.32 * math.cos(math.radians(lat0)); ky = 110.6
    x2 = (p2[1] - p1[1]) * kx; y2 = (p2[0] - p1[0]) * ky
    d = math.hypot(x2, y2)
    if d > r1 + r2 or d < abs(r1 - r2): return []
    a = (r1**2 - r2**2 + d**2) / (2 * d); h = math.sqrt(max(r1**2 - a**2, 0))
    xm, ym = a * x2 / d, a * y2 / d
    out = []
    for s in (1, -1):
        x = xm + s * h * (-y2) / d; y = ym + s * h * x2 / d
        out.append((p1[0] + y / ky, p1[1] + x / kx))
    return out
for lg in (5.56, 5.92):
    sol = circle_intersections(PIC, 1.0 * lg, EBS, 1.5 * lg)
    P("  league %.2f km: wreck = 1 lg from Picolet AND 1.5 lg from EBS ->" % lg, ["%.4f,%.4f" % s for s in sol])

P("\n=== C6 Fort Caroline: '6 miles from the mouth' on south side ===")
MOUTH = (30.400, -81.395); BLUFF = (30.384, -81.497)
az, d = geo.inv(*MOUTH, *BLUFF); P("  mouth -> St Johns Bluff tree block: az %.0f, %.1f km = %.1f statute mi (straight)" % (az, d, d / 1.609))

P("\n=== C7 Roanoke Site X ===")
FR = (35.938, -75.712); SX = (36.003, -76.710)
az, d = geo.inv(*FR, *SX); P("  Fort Raleigh area -> Salmon Creek mouth (approx): az %.0f, %.1f km = %.1f statute mi" % (az, d, d / 1.609))

P("\n=== C8 Mabila ===")
FORKS = (31.15, -87.95); MAR = (32.25, -87.80); SELMA = (32.407, -87.021)
for nm, p in [("Forks (southern Clarke Co.)", FORKS), ("Marengo Co. centre", MAR)]:
    az, d = geo.inv(*SELMA, *p); P("  Selma -> %-28s az %.0f  %.0f km" % (nm, az, d))
az, d = geo.inv(*FORKS, *MAR); P("  Forks <-> Marengo: %.0f km" % d)
