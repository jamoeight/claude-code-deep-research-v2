"""Render findings.json (+ optional skeptic verdicts) into the report page index.html."""
import json, os, html, re

ROOT = os.path.join(os.path.dirname(__file__), "..")
F = json.load(open(os.path.join(ROOT, "findings.json")))
PRIVATE = os.environ.get("PRIVATE") == "1"
_r2 = os.path.join(ROOT, "data", "private", "findings_r2.json") if PRIVATE else os.path.join(ROOT, "findings_r2_public.json")
if os.path.exists(_r2):
    F = F + json.load(open(_r2))
V = {}
vp = os.path.join(ROOT, "data", "skeptic_verdicts.json")
if os.path.exists(vp):
    V = json.load(open(vp))
e = html.escape

NOV = {"NOVEL-SYNTHESIS": ("New synthesis", "nov"), "PROPOSED": ("Proposed by others", "pro"),
       "KNOWN": ("Known", "kno"), "UNCHECKED": ("Unchecked", "unc"), "PARTLY-KNOWN": ("Region known, spot unconfirmed", "par")}


def coord(f):
    ns = "N" if f["lat"] >= 0 else "S"
    ew = "E" if f["lon"] >= 0 else "W"
    return f"{abs(f['lat']):.4f}° {ns}, {abs(f['lon']):.4f}° {ew}"


def chip(f):
    lab, cls = NOV.get(f["novelty"], (f["novelty"], "unc"))
    return f'<span class="chip {cls}">{e(lab)}</span>'


def verdict(f):
    v = V.get(f["id"])
    if not v:
        return ""
    return f'<p class="verdict"><span class="vlab">Skeptic check</span> <b>{e(v["verdict"])}</b>. {e(v["note"])}</p>'


def links(f):
    dec = f"{f['lat']:.5f}, {f['lon']:.5f}"
    return (f'<div class="links"><a href="{e(f["earth"])}" target="_blank" rel="noopener">Open in Google Earth</a>'
            f'<a href="{e(f["maps"])}" target="_blank" rel="noopener">Google Maps satellite</a>'
            f'<button type="button" class="copy" data-c="{dec}">Copy {dec}</button></div>')


def conf(f):
    c = int(f.get("confidence", 0))
    return (f'<div class="conf" title="Team confidence {c}/100"><span class="clab">Confidence</span>'
            f'<span class="bar"><i style="width:{c}%"></i></span><span class="cnum">{c}</span></div>')


def card(f, big=True):
    fig = ""
    if f.get("fig"):
        fdir = f.get("figdir", "figures")
        fig = (f'<figure><img src="{fdir}/{e(f["fig"])}" alt="Sentinel-2 true colour (left) and Copernicus DEM hillshade (right) for {e(f["name"])}" loading="lazy">'
               f'<figcaption>Left: Sentinel-2 true colour, 10 m. Right: Copernicus GLO-30 elevation, hillshaded. Red cross = coordinate.</figcaption></figure>')
    ev = "".join(f"<li>{e(x)}</li>" for x in f.get("evidence", []))
    loot = '<span class="chip loot">Looting-sensitive region</span>' if f.get("looting_sensitive") else ""
    rad = f" · ±{f['radius_km']:g} km" if f.get("radius_km") else ""
    return f"""
<article class="card {'big' if big else ''}" id="{e(f['id'])}">
  <header><span class="fid">{e(f['id'])}</span><span class="cat">{e(f['category'])}</span>{chip(f)}{loot}</header>
  <h3>{e(f['name'])}</h3>
  <p class="coord">{coord(f)}{rad}</p>
  {fig}
  <p class="lede">{e(f['one_line'])}</p>
  {'<p class="look"><span class="vlab">What to look for</span> ' + e(f['look_for']) + '</p>' if f.get('look_for') else ''}
  {verdict(f)}
  {'<details><summary>Evidence chain</summary><ul>' + ev + '</ul><p class="team">Source: ' + e(f.get('team','')) + '</p></details>' if ev else ''}
  {conf(f)}
  {links(f)}
</article>"""


def row(f):
    return (f"<tr><td class='mono'>{e(f['id'])}</td><td>{e(f['name'])}<div class='sub'>{e(f['one_line'])}</div>{verdict(f)}</td>"
            f"<td class='mono'>{f['lat']:.4f}, {f['lon']:.4f}</td>"
            f"<td><a href='{e(f['earth'])}' target='_blank' rel='noopener'>Earth</a> · <a href='{e(f['maps'])}' target='_blank' rel='noopener'>Maps</a></td></tr>")


A = [f for f in F if f["tier"] == "A"]
B = [f for f in F if f["tier"] == "B"]
C = [f for f in F if f["tier"] == "C"]
W = [f for f in F if f["tier"] == "W"]
K = [f for f in F if f["tier"] == "calib"]
HM = [f for f in F if f["tier"] == "H"]
HINTRO_PRIVATE = ("You asked for human-made things. Three new teams and a new elevation-model tell finder went after lost capitals, missing road stations and ruined desert towns. "
                  "Every lead here was looked at in Sentinel-2 and the DEM. This private page carries exact coordinates. The public repo shows them rounded to about 10 km, because several sites sit in regions where looting is active.")
HINTRO_PUBLIC = ("Round 2 focused on human-made sites. Coordinates of possibly unrecorded archaeological sites are rounded to about 10 km here to avoid helping looters; "
                 "exact positions are in the owner's private report.")

tpl = open(os.path.join(os.path.dirname(__file__), "page_template.html")).read()
out = (tpl.replace("{{A}}", "".join(card(f) for f in A))
          .replace("{{B}}", "".join(card(f, big=False) for f in B))
          .replace("{{C}}", "".join(row(f) for f in C))
          .replace("{{W}}", "".join(row(f) for f in W))
          .replace("{{K}}", "".join(row(f) for f in K))
          .replace("{{H}}", "".join(card(f, big=True) for f in HM))
          .replace("{{HINTRO}}", (HINTRO_PRIVATE if PRIVATE else HINTRO_PUBLIC))
          .replace("{{NA}}", str(len(A))).replace("{{NB}}", str(len(B))).replace("{{NC}}", str(len(C)))
          .replace("{{NW}}", str(len(W))).replace("{{NTOT}}", str(len(F))))
outp = os.path.join(ROOT, "data", "private", "index_private.html") if PRIVATE else os.path.join(ROOT, "index.html")
open(outp, "w").write(out)
print(outp, len(out) // 1024, "KB")
