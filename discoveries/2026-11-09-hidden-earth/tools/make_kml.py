"""Build a Google Earth KML from findings.json (list of dicts with id,name,lat,lon,radius_km,category,tier,one_line)."""
import json, sys, html
from xml.sax.saxutils import escape

COL = {"A": "ff0000ff", "B": "ff00a5ff", "C": "ff00ffff", "calib": "ffaaaaaa"}

def main(inp, outp):
    F = json.load(open(inp))
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
           '<name>Operation Hidden Earth - 2026-11-09</name>']
    for t, c in COL.items():
        out.append(f'<Style id="t{t}"><IconStyle><color>{c}</color><scale>1.2</scale>'
                   '<Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon></IconStyle>'
                   f'<LineStyle><color>{c}</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style>')
    cats = {}
    for f in F:
        cats.setdefault(f.get("category", "other"), []).append(f)
    import math
    for cat, items in sorted(cats.items()):
        out.append(f"<Folder><name>{escape(cat)}</name>")
        for f in items:
            tier = f.get("tier", "C")
            desc = escape(f.get("one_line", "")) + "<br/>" + escape(f.get("novelty", "")) + f" | radius {f.get('radius_km','?')} km"
            out.append(f'<Placemark><name>{escape(f["id"] + " " + f["name"])}</name><styleUrl>#t{tier}</styleUrl>'
                       f'<description><![CDATA[{desc}]]></description>'
                       f'<LookAt><longitude>{f["lon"]}</longitude><latitude>{f["lat"]}</latitude><altitude>0</altitude>'
                       f'<range>{max(1500, float(f.get("view_m", 4000)))}</range><tilt>30</tilt><heading>0</heading></LookAt>'
                       f'<Point><coordinates>{f["lon"]},{f["lat"]},0</coordinates></Point></Placemark>')
            r = float(f.get("radius_km") or 0)
            if r >= 0.5:
                pts = []
                for k in range(0, 361, 10):
                    a = math.radians(k)
                    pts.append(f'{f["lon"] + r/111.32/math.cos(math.radians(f["lat"]))*math.sin(a):.5f},{f["lat"] + r/110.57*math.cos(a):.5f},0')
                out.append(f'<Placemark><name>{escape(f["id"])} uncertainty</name><styleUrl>#t{tier}</styleUrl>'
                           f'<LineString><tessellate>1</tessellate><coordinates>{" ".join(pts)}</coordinates></LineString></Placemark>')
        out.append("</Folder>")
    out.append("</Document></kml>")
    open(outp, "w").write("\n".join(out))
    print("wrote", outp, len(F))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
