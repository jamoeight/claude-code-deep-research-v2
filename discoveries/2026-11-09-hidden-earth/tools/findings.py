"""Curated findings for Operation Hidden Earth -> findings.json + hidden_earth.kml.

Tiers:  A = strongest new leads from our own analysis (look first)
        B = refined classic mysteries (others' proposals sharpened, or new tests)
        C = survey-gap boxes to browse in Google Earth at sub-metre resolution
        calib = known features used to prove the methods work
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))

def ge(lat, lon, dist=4000, tilt=45):
    return f"https://earth.google.com/web/@{lat:.5f},{lon:.5f},0a,{dist:.0f}d,35y,0h,{tilt}t,0r"

def gm(lat, lon, z=15):
    return f"https://www.google.com/maps/@{lat:.5f},{lon:.5f},{z}z/data=!3m1!1e3"

F = [
# ---------------- Tier A: new leads from our own analysis ----------------
dict(id="A1", tier="A", category="Karst", name="Giant round doline, Darai Plateau (PNG)",
     lat=-6.8594, lon=143.2436, radius_km=0.5, view_m=5000, novelty="NOVEL-SYNTHESIS", confidence=45,
     one_line="A near-perfect closed sinkhole about 1.3 km across and about 260 m deep in the Copernicus DEM, inside the Darai polygonal karst.",
     look_for="A round, forest-lined pit far larger than the cockpit hollows around it. Tilt the 3D view to see the wall depth. A 30 m DEM under-reads deep pits, so the real depth may be larger.",
     evidence=["T6 closed-depression detector, calibrated on Xiaozhai tiankeng and on Sima Humboldt and Sima Martel",
               "The floor elevation is measured TanDEM-X data, not void fill (checked in the DEM)",
               "Lead's 3 km DEM/S2 view: the feature dwarfs every neighbouring doline (figure)"],
     fig="darai_doline.jpg", team="T6 + lead"),
dict(id="A2", tier="A", category="Karst", name="Twin giant closed basins, Lengguru fold belt (West Papua)",
     lat=-3.2692, lon=133.8425, radius_km=0.8, view_m=8000, novelty="NOVEL-SYNTHESIS", confidence=40,
     one_line="Two closed karst depressions about 220 m and 255 m deep (sister basin at -3.3492, 133.9714), in a fold belt that cavers have barely visited.",
     look_for="Forested elongated pits or uvalas with steep walls. The sister basin's floor was a radar void, which often means a very deep shaft.",
     evidence=["T6 DEM depression detector", "Lengguru has very few caving expeditions on record (T6 literature sweep)"],
     fig="lengguru_B.jpg", team="T6"),
dict(id="A3", tier="A", category="Biodiversity", name="Unsurveyed forest massif 20 km east of Mount Mabu (Mozambique)",
     lat=-16.304, lon=36.586, radius_km=3, view_m=14000, novelty="NOVEL-SYNTHESIS", confidence=40,
     one_line="After Mabu itself, this is the strongest tall-canopy (>20 m) signal in northern Mozambique: about 11 km² on a ridge with about 940 m of relief. It may be the next 'Google Earth forest'.",
     look_for="A closed, dark-green canopy on the ridge crest that stands out from the miombo and farmland around it. Compare it with Mabu's forest 20 km to the west. Rule out tea or eucalyptus plantations, which grow in neat blocks.",
     evidence=["T5 isolated-summit scan over 11-18°S, 33-41°E, with tall-canopy fraction from the Meta 1 m canopy-height map (Mabu core 16.6%, miombo 0.6%)",
               "Mabu was found exactly this way, from imagery, by Bayliss in 2005, and was then shown to hold many new species",
               "A second, weaker massif sits at -16.354, 36.734",
               "Lead's search found no published survey of a massif east of Mabu (Mabu literature only)"],
     fig="mabu_east.jpg", team="T5 + lead"),
dict(id="A4", tier="A", category="Waterfalls", name="Gorge-head waterfall candidate, Ethiopian highlands",
     lat=7.88242, lon=39.80336, radius_km=0.5, view_m=4000, novelty="NOVEL-SYNTHESIS", confidence=25,
     one_line="The DEM knickpoint scan found a river leaving the farmed plateau and dropping at least 170 m into a box canyon. Its catchment is very large (the DEM figure is about 10,600 km²).",
     look_for="A plunge or cascade at the head of the canyon. Look in the wet season (Jul-Sep): in the dry season it may be a dry lip.",
     evidence=["Lead's waterfall finder found Angel Falls and Kaieteur blind",
               "Knickpoint test: the step is 5x steeper than the reaches above and below, so it is a discrete step, not a steady gorge"],
     fig="ethiopia_fall.jpg", team="lead"),
dict(id="A5", tier="A", category="Waterfalls", name="Star Mountains escarpment fall, east of Tabubil (PNG)",
     lat=-5.2633, lon=141.3469, radius_km=0.5, view_m=4000, novelty="NOVEL-SYNTHESIS", confidence=30,
     one_line="A 42 km² channel drops about 600 m over about 450 m horizontally, the same DEM shape as Angel Falls. Sentinel-2 shows white water in a slot gorge.",
     look_for="White water threading down the escarpment slot. On karst it could be a dry hanging valley outside storms.",
     evidence=["T6 DEM fall detector, which measured Angel Falls at 936 m to within 2 km", "Lead's Sentinel-2 close-up (figure)"],
     fig="star_mtns_fall.jpg", team="T6 + lead"),
dict(id="A6", tier="A", category="Geology", name="Field of rimmed bowl craters, Amadror/Tefedest (Algeria)",
     lat=25.26, lon=6.13, radius_km=20, view_m=40000, novelty="NOVEL-SYNTHESIS", confidence=20,
     one_line="The global crater scan found at least 7 rimmed bowls 0.45-1.35 km wide and 30-135 m deep in dark rock. Their clustering points to a volcanic maar or tuff-ring field, not an impact.",
     look_for="Round craters with raised rims and pale clay floors. Check whether this is a catalogued Hoggar volcanic district. If not, it is an undocumented maar field.",
     evidence=["Global DEM crater scan (2,887 tiles) found Tenoumer, Talemzane, Amguid, Wolfe Creek and Barringer blind",
               "Not in the scan's volcanic exclusion list. A second cluster sits at 25.09N 8.00E (3 craters, white floors)"],
     fig="alg_cluster_A.jpg", team="lead"),
# ---------------- Tier B: classic mysteries sharpened ----------------
dict(id="B1", tier="B", category="Lost cities", name="Akkad (Agade): relict-Tigris / paleo-Adhaim junction",
     lat=33.97, lon=44.23, radius_km=8, view_m=25000, novelty="NOVEL-SYNTHESIS", confidence=6, looting_sensitive=True,
     one_line="Akkad is the only Mesopotamian imperial capital never found. A DEM-traced relict Tigris belt splits from today's river 15 km from where the Adhaim reaches the floodplain, which joins Ziegler's confluence idea to Kawakami's ancient-riverbed idea.",
     look_for="Tells (low mounds of a few hundred metres) along the dry channel belt between Balad and Ad-Dujayl.",
     evidence=["T1 DEM channel tracing", "Kawakami's candidate, Tell Sinker (33.798, 44.324), has been under Japan-Iraq survey since 2025 (PROPOSED). The DEM shows an 8.6 m mound on the same ~50 km cutoff"],
     fig="akkad_junction.jpg", team="T1"),
dict(id="B2", tier="B", category="Lost cities", name="Tell Sinker, Kawakami's Akkad candidate",
     lat=33.7981, lon=44.3244, radius_km=1, view_m=4000, novelty="PROPOSED", confidence=15, looting_sensitive=True,
     one_line="An 8.6 m mound sitting on a dry, roughly 50 km cutoff of the Tigris (Balad to Taji).",
     look_for="A mound rising above the fields.", evidence=["T1"], fig="akkad_sinker.jpg", team="T1"),
dict(id="B3", tier="B", category="Meteorites", name="Chinguetti meteorite: the never-searched midpoint",
     lat=20.68, lon=-11.94, radius_km=12, view_m=40000, novelty="NOVEL-SYNTHESIS", confidence=3,
     one_line="In 1916 Ripert reported a 100 m iron 'hill'. The blacksmiths' account puts a house-sized iron block halfway to Ouadane (about 46 km). The 2024 route paper searched only 12-22 km out. A straight ridge about 60 m high and 20 km long here has never been examined.",
     look_for="A dark, smooth, isolated mass among the dunes. Check whether the ridge is sand or rock.",
     evidence=["T3 reading of arXiv:2402.14150 (Warren et al. 2024)", "Unsurveyed tall dunes in SW Les Boucles (20.36, -12.44) and the NW Batraz megadunes (20.19, -12.005) also fit the bearings"],
     fig="chinguetti_mid.jpg", team="T3"),
dict(id="B4", tier="B", category="Lost cities", name="Ho-lao-lo-kia, Xuanzang's sand-buried city",
     lat=37.55, lon=80.58, radius_km=30, view_m=60000, novelty="NOVEL-SYNTHESIS", confidence=20,
     one_line="Xuanzang places it north of Khotan, with a survivor who fled east to Pi-mo (Uzun-tati), and says it was already a sand mound in 644. That rules out Dandan Oilik, Karadong and Yuansha. The DEM puts the dry downstream end of Pi-mo's streams here.",
     look_for="Rectilinear walls, dark wood/rammed-earth scatters and old canal lines between dunes.",
     evidence=["T2 geodesy on the Da Tang Xiyu Ji", "Calibrated li length 282 m. Xuanzang's 'old Tukhara' town is refined to 37.78, 83.67, 12 km west of the later Endere fort"],
     fig=None, team="T2"),
dict(id="B5", tier="B", category="Lost cities", name="al-Ghaba, the royal town of ancient Ghana",
     lat=15.846, lon=-8.017, radius_km=7, view_m=25000, novelty="NOVEL-SYNTHESIS", confidence=10,
     one_line="al-Bakri (1068) puts the king's town 6 miles from the Muslim town (Koumbi Saleh). That distance meets a low plain with seasonal ponds north-west to north of Koumbi Saleh, and two unexplained 'built-up' land-cover pixels.",
     look_for="Stone house mounds and enclosure walls on the low plain, especially near 15.8239, -7.9902.",
     evidence=["T8 itinerary math + DEM + ESA WorldCover"], fig="ghaba.jpg", team="T8"),
dict(id="B6", tier="B", category="Impact craters", name="Australasian tektite crater: a falsifiable test of Bolaven",
     lat=15.203, lon=106.271, radius_km=10, view_m=40000, novelty="PROPOSED", confidence=35,
     one_line="This is the source of the largest young strewn field (788 ka), still missing. Two lava flows inside Sieh et al.'s proposed outline are magnetically reversed. If they date to more than 788 ka, Bolaven is falsified; if they date to 773-788 ka, it is strongly supported.",
     look_for="Nothing visible from orbit: the crater is buried under basalt. This is a fieldwork test.",
     evidence=["T4: post-2020 critiques (Mizera 2022, Mizera & Strunga 2024, Seydoux-Guillaume 2024)", "A re-run microtektite fit favours about 12°N 106°E and argues against Badain Jaran"],
     fig="bolaven.jpg", team="T4"),
dict(id="B7", tier="B", category="Lost cities", name="Njimi, first capital of Kanem = Tié?",
     lat=14.121, lon=15.729, radius_km=8, view_m=20000, novelty="PROPOSED", confidence=60,
     one_line="DAI/Frobenius identification: a 3.2 ha fired-brick enclosure locally called 'Njimi-ye', dated to the 11th-14th centuries, about 45 km east of Mao.",
     look_for="A rectangular brick enclosure among the dunes.", evidence=["T8"], fig="njimi_tie.jpg", team="T8"),
dict(id="B8", tier="B", category="Dynamic Earth", name="Lhende Khola 2026 landslide-dam site (Nepal-Tibet)",
     lat=28.334, lon=85.484, radius_km=1, view_m=6000, novelty="NOVEL-SYNTHESIS", confidence=70,
     one_line="The barrier lake reported by Chinese state TV (2,950 m, more than 10 km from Gyirong Port) is pinned here by debris in Sentinel-2 and by DEM elevation. The lake had drained by late September 2026.",
     look_for="Fresh debris fan at the junction with the main valley. Compare 2025-10-21 with 2026-10-26.", evidence=["T9"], fig="lhende_dam.jpg", team="T9"),
dict(id="B9", tier="B", category="Lost cities", name="Tarhuntassa (lost Hittite capital) at Türkmen-Karahöyük",
     lat=37.571, lon=32.7421, radius_km=5, view_m=8000, novelty="PROPOSED", confidence=25,
     one_line="This is the Massa/Osborne candidate (Hartapu inscription). The DEM shows a 30 m mound of the right size. The candidate is contested by the Hulaya-frontier reading, whose alternative is the Karadağ/Kızıldağ zone.",
     look_for="A large round höyük in the Konya plain.", evidence=["T1"], fig="tarhuntassa_tkh.jpg", team="T1"),
dict(id="B10", tier="B", category="Lost cities", name="Itj-tawy, Middle Kingdom capital of Egypt",
     lat=29.572, lon=31.236, radius_km=2, view_m=8000, novelty="PROPOSED", confidence=50,
     one_line="The town centre lies beneath fields east of the Lisht pyramids. Cores reach a Middle Kingdom layer at 5 m.",
     look_for="Nothing visible: it is buried under cultivation.", evidence=["T1"], fig=None, team="T1"),
dict(id="B11", tier="B", category="Lost colonial sites", name="La Navidad (Columbus, 1492) at En Bas Saline",
     lat=19.725, lon=-72.125, radius_km=2.5, view_m=8000, novelty="PROPOSED", confidence=55,
     one_line="Three diary distances fit together. They also put the Santa María wreck offshore near 19.80, -72.143.",
     look_for="Reef flats offshore; the site itself needs geophysics.", evidence=["T8"], fig=None, team="T8"),
dict(id="B12", tier="B", category="Lost colonial sites", name="Fort Caroline (1564), St Johns Bluff vicinity",
     lat=30.384, lon=-81.497, radius_km=3, view_m=8000, novelty="PROPOSED", confidence=40,
     one_line="'South side, six miles from the mouth' measures 10.0 km, which lands on the bluff forest. The Altamaha and St Marys alternatives are untested.",
     look_for="Bluff-top clearings.", evidence=["T8"], fig=None, team="T8"),
dict(id="B13", tier="B", category="Lost colonial sites", name="Roanoke Lost Colony: Site X",
     lat=36.003, lon=-76.71, radius_km=4, view_m=8000, novelty="PROPOSED", confidence=35,
     one_line="The fort symbol on the Virginea Pars map patch, plus Border-ware finds on the western Albemarle shore.",
     look_for="Shoreline fields.", evidence=["T8"], fig=None, team="T8"),
# ---------------- Tier C: survey-gap boxes for Google Earth browsing ----------------
dict(id="C1", tier="C", category="Earthworks", name="Amazon geoglyph gap: north of the Abunã",
     lat=-9.25, lon=-65.45, radius_km=28, view_m=60000, novelty="NOVEL-SYNTHESIS", confidence=45,
     one_line="About 700 km² was cleared in 2019-24. There are no catalogued earthworks against Walker et al. 2023, though a known cluster lies just west.",
     look_for="Geometric ditched squares and circles, 100-350 m across, in pasture. Sentinel-2 at 10 m does NOT show known geoglyphs (we tested), so use Google Earth's sub-metre imagery.",
     evidence=["T7"], fig=None, team="T7"),
dict(id="C2", tier="C", category="Earthworks", name="Amazon geoglyph gap: Upper Tapajós / Paranaíta",
     lat=-9.45, lon=-56.95, radius_km=28, view_m=60000, novelty="NOVEL-SYNTHESIS", confidence=40,
     one_line="Extends de Souza's 2018 belt of ditched villages. 1,341 km² cleared, none catalogued.", look_for="Ring ditches and village mounds.", evidence=["T7"], fig=None, team="T7"),
dict(id="C3", tier="C", category="Earthworks", name="Amazon geoglyph gap: Jaci-Paraná / Nova Mamoré",
     lat=-9.85, lon=-64.95, radius_km=28, view_m=60000, novelty="NOVEL-SYNTHESIS", confidence=40,
     one_line="63% cleared, sitting between two known clusters.", look_for="Ditched enclosures.", evidence=["T7"], fig=None, team="T7"),
dict(id="C4", tier="C", category="Earthworks", name="Geoglyph plateau across the Peru-Bolivia border (Iñapari)",
     lat=-11.45, lon=-69.45, radius_km=28, view_m=60000, novelty="NOVEL-SYNTHESIS", confidence=30,
     one_line="The Acre geoglyph plateau continues across the border, where survey effort drops.", look_for="Ditched enclosures.", evidence=["T7"], fig=None, team="T7"),
dict(id="C5", tier="C", category="Stone structures", name="Desert kites: Jebel as-Sawda rim (Libya)",
     lat=28.9, lon=15.15, radius_km=17, view_m=40000, novelty="NOVEL-SYNTHESIS", confidence=30, looting_sensitive=True,
     one_line="A basalt rim adjoining the 330+ known Hamada al-Hamra kites. The Globalkites survey stops at Arabia.",
     look_for="Arrowhead-shaped stone-wall funnels hundreds of metres long. Needs sub-metre imagery.", evidence=["T10"], fig=None, team="T10"),
dict(id="C6", tier="C", category="Stone structures", name="Turgai-type geoglyphs: Ubagan valley (Kazakhstan)",
     lat=51.7, lon=64.5, radius_km=17, view_m=40000, novelty="NOVEL-SYNTHESIS", confidence=25,
     one_line="81% unploughed lake-terrace grassland, the same setting as Ushtogay Square, lying between the Turgai core and the Kostanay Tetragon.",
     look_for="Squares, crosses and swastika shapes made of small mounds, 100-400 m across.", evidence=["T10"], fig=None, team="T10"),
dict(id="C7", tier="C", category="Stone structures", name="Desert kites: Betpak-Dala escarpment (Kazakhstan)",
     lat=45.7, lon=67.45, radius_km=17, view_m=40000, novelty="NOVEL-SYNTHESIS", confidence=20,
     one_line="An 80 m escarpment like the kite-bearing chinks of the Ustyurt, about 110 km east of the dataset's kite limit.", look_for="Kite funnels at the scarp edge.", evidence=["T10"], fig=None, team="T10"),
dict(id="C8", tier="C", category="Stone structures", name="Mustatils: Hisma basin NW of Tabuk (Saudi Arabia)",
     lat=29.3, lon=35.75, radius_km=17, view_m=40000, novelty="NOVEL-SYNTHESIS", confidence=15,
     one_line="A corridor between the AlUla/Tayma mustatil core and the southern Jordan rectangles.", look_for="Long rectangular stone enclosures, 20-600 m.", evidence=["T10"], fig=None, team="T10"),
dict(id="C9", tier="C", category="Dynamic Earth", name="Next Yamal gas-blowout crater: search box",
     lat=70.06, lon=68.7, radius_km=25, view_m=60000, novelty="PROPOSED", confidence=55,
     one_line="4-5 of the roughly 8 known giant craters cluster here near the Bovanenkovo pipeline. Our 2025-26 Sentinel-2 change scan found none new.",
     look_for="A new dark pit 20-40 m wide with an ejecta ring of thrown-out debris. Compare summers.", evidence=["T9"], fig=None, team="T9"),
dict(id="C10", tier="C", category="Dynamic Earth", name="New unnamed islands, NE Greenland (Storstrømmen/Zachariae)",
     lat=77.2, lon=-22.5, radius_km=30, view_m=80000, novelty="PROPOSED", confidence=35,
     one_line="The island inventory stops at 2020, and Pelto notes islands released by retreating ice since then.", look_for="Rock islands appearing out of the ice front.", evidence=["T9"], fig=None, team="T9"),
dict(id="C11", tier="C", category="Paleolakes", name="Ahnet-Tidikelt Holocene megalake basin (Algeria)",
     lat=25.66, lon=1.54, radius_km=15, view_m=50000, novelty="NOVEL-SYNTHESIS", confidence=25,
     one_line="A DEM-derived highstand lake basin of about 9,000 km². Its inflow deltas are the best targets for Holocene shoreline sites.", look_for="Old shorelines, grinding stones and hearths on delta fans.", evidence=["T3"], fig=None, team="T3"),
# ---------------- calibration ----------------
dict(id="K1", tier="calib", category="Calibration", name="Meteor Crater (crater-scan check)", lat=35.0275, lon=-111.0225, radius_km=0, view_m=3000,
     novelty="KNOWN", confidence=100, one_line="Found blind by the DEM crater scan.", look_for="", evidence=[], fig="meteor_calib.jpg", team="lead"),
dict(id="K2", tier="calib", category="Calibration", name="Tenoumer crater (crater-scan check)", lat=22.918, lon=-10.408, radius_km=0, view_m=4000,
     novelty="KNOWN", confidence=100, one_line="The only candidate the scan returned in its 1°×1° tile.", look_for="", evidence=[], fig=None, team="lead"),
dict(id="K3", tier="calib", category="Calibration", name="Kaieteur Falls (waterfall-scan check)", lat=5.175, lon=-59.48, radius_km=0, view_m=4000,
     novelty="KNOWN", confidence=100, one_line="Found blind by the waterfall scan and passed the knickpoint (discrete-step) test.", look_for="", evidence=[], fig="kaieteur_calib.jpg", team="lead"),
dict(id="K4", tier="calib", category="Calibration", name="Angel Falls (waterfall-scan check)", lat=5.9675, lon=-62.5356, radius_km=0, view_m=4000,
     novelty="KNOWN", confidence=100, one_line="Top-ranked of 102 candidates in its tile.", look_for="", evidence=[], fig=None, team="lead"),
dict(id="K5", tier="calib", category="Calibration", name="Mount Mabu forest (sky-island check)", lat=-16.29, lon=36.40, radius_km=0, view_m=14000,
     novelty="KNOWN", confidence=100, one_line="The 2005 Google-Earth discovery that A3 is modelled on.", look_for="", evidence=[], fig="mabu_ref.jpg", team="T5"),
dict(id="K6", tier="calib", category="Calibration", name="Ushtogay Square geoglyph", lat=50.8329, lon=65.3263, radius_km=0, view_m=2500,
     novelty="KNOWN", confidence=95, one_line="Shows what Turgai geoglyphs look like (sub-metre imagery needed).", look_for="", evidence=[], fig=None, team="T10"),
]

# re-rank tier A after the skeptic pass: unsurveyed / unrecorded first
_REMAP = {"A3": "A1", "A6": "A2", "A1": "A3", "A2": "A4", "A5": "A5", "A4": "A6"}
for f in F:
    if f["id"] in _REMAP:
        f["id"] = _REMAP[f["id"]]
for f in F:
    if f["id"] == "B8":
        f["novelty"] = "KNOWN"; f["confidence"] = 90
        f["one_line"] = "The 2026 barrier lake reported by Chinese state TV and Nepal's NDRRMA/ICIMOD. The team pinned its location independently from Sentinel-2 debris and DEM elevation, which matched the published reports. It drained by late September 2026."
    if f["id"] in ("A3", "A4", "B1", "B4", "B6"):
        f["novelty"] = "PARTLY-KNOWN"
F.sort(key=lambda f: ({"A": 0, "B": 1, "C": 2, "W": 3, "calib": 4}[f["tier"]], int(f["id"][1:]) if f["id"][1:].isdigit() else 0))

# waterfall-scan shortlist (discrete-step knickpoints, artifacts filtered), excluding Kaieteur (calib) and A4
_wf = os.path.join(os.path.dirname(__file__), "..", "data", "waterfalls", "falls_ranked.json")
if os.path.exists(_wf):
    k = 0
    for r in json.load(open(_wf))[:16]:
        if abs(r["lat"] - 5.175) < 0.05 or abs(r["lat"] - 7.88242) < 0.01:
            continue
        k += 1
        F.append(dict(id=f"W{k}", tier="W", category="Waterfall shortlist",
                      name=f"Waterfall candidate ({r['reg']})", lat=r["lat"], lon=r["lon"], radius_km=0.3, view_m=3500,
                      novelty="UNCHECKED", confidence=15,
                      one_line=f"DEM step of {r['step_drop']:.0f} m over {r['step_len']:.0f} m; knickpoint ratio {r['knick_ratio']:.1f}; catchment about {r['catch_km2']:.0f} km²; lip at {r['lip_elev']:.0f} m.",
                      look_for="White water or a plunge at the step. The DEM under-reads tall falls.", evidence=["lead waterfall scan"], fig=None, team="lead"))
        if k >= 10:
            break

for f in F:
    f["earth"] = ge(f["lat"], f["lon"], f.get("view_m", 4000))
    f["maps"] = gm(f["lat"], f["lon"], 15 if f.get("view_m", 4000) < 10000 else 12)
    f.setdefault("looting_sensitive", False)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "findings.json")
    json.dump(F, open(out, "w"), indent=1, ensure_ascii=False)
    print(len(F), "findings ->", out)
