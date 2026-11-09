# T4 — Hidden impact craters

## Method (what you joined, what you searched; 5-10 lines)
- I ran about 20 WebSearch queries on the Australasian tektite (AAT) source debate, Libyan Desert Glass (LDG), the new ananguite strewn field and the crater databases. WebFetch could not reach en.wikipedia.org, wikiwand or ncbi, and the shared web-search budget ran out partway through. Claims marked **[BK]** come from background knowledge and were **not verified in this session**.
- **Data join 1:** I compiled 42 deep-sea microtektite abundances (Glass 1994, Table 1) and 263 tektite find localities, including Muong Nong-type (MN) finds and the Sieh et al. 2020 Dataset S1. They came from the public repository github.com/yicolas/2024_Laos_Australasian_Impactor, an unpublished paleomagnetic study of Bolaven dated Nov 2026. The data are saved in `data/T4/aa_*.csv`.
- **Analysis A:** I re-ran the Glass & Pizzuto (1994) source-location inversion, fitting log abundance against log distance on a 0.25° grid, with 500 bootstrap resamples and an optional downrange-asymmetry term (`data/T4/mt_fit.py`, `mt_boot.py`). Then I scored each published candidate site against the fit.
- **Analysis B:** I took the geometric median of literature MN-type finds and kept the collection-biased Sieh S1 finds separate.
- **Analysis C:** I checked the unpublished paleomagnetic sites against the digitised Sieh 2020 crater outlines (point-in-polygon), and drew a Copernicus GLO-30 radial profile over Bolaven.
- **Data deliverable:** `data/T4/known_impact_structures.csv` has 372 rows with the columns name, lat, lon, diameter_km and status:
  - 189 `confirmed` (Earth Impact Database scrape)
  - 9 `confirmed_post_eid`
  - 153 `proposed`
  - 21 `discarded`
  - Row-by-row sources are in `known_impact_structures_provenance.csv`, and the build script is `build_csv.py`.

## Candidates (ranked)

### C1. Bolaven Plateau buried crater, S Laos (AAT source) — PROPOSED
- Coordinates: 15.203, 106.271 (±10 km). This centre comes from inverting the "distance from crater" column of Sieh 2020 Dataset S1, with a median misfit of about 1.4 km. The digitised gravity outline centroid is 15.222N, 106.245E and the geologic outline centroid is 15.198N, 106.289E. The outlines measure about 13.5×16 km and 13.8×13.6 km.
- What it would be / why it matters (significance 10): this would be the source of the largest young strewn field, 788 ka, which covers about 10–15% of Earth's surface. The crater has been missing for about 100 years.
- Evidence chain:
  1. Sieh et al. 2020 give four lines of evidence: lava ages, tektite geochemistry, a 404-station gravity survey showing a buried crater of about 17×13 km, and a bouldery breccia 10–20 km from the centre. https://www.pnas.org/doi/10.1073/pnas.1904368116
  2. Melosh's commentary called it the "best candidate yet" but flagged the small size. https://www.pnas.org/doi/10.1073/pnas.1920576117
  3. Sieh et al. 2023 describe the Bolaven diamicton as proximal ejecta, with tektites at its top. https://www.pnas.org/doi/10.1073/pnas.2310351120
  4. Carling et al. 2024 logged more than 100 sections in 5 countries and describe an ejecta blanket of at least 300,000 km² dated 788–785 ka. This is the same research group, so it is not independent. https://progearthplanetsci.springeropen.com/articles/10.1186/s40645-024-00660-9
  5. My microtektite fit gives Bolaven r²=0.794 against a best fit of 0.803 (F(2,38)=1.74, not significantly worse). With an asymmetry term the fit is r²=0.802, and the downrange maximum points at an azimuth of 205° (SSW). That direction agrees with the southward oblique impact inferred from the null results in Chinese loess and Beijing boreholes. https://www.nature.com/articles/s44453-025-00017-6
  6. The literature MN-type finds have a geometric median at 16.22N 106.39E, about 115 km NNE of Bolaven (`data/T4/aa_tektite_localities.csv`).
- **Adversarial (published since 2020):**
  - Mizera 2022 (MAPS 57:1973) ran a two-component mixing model on oxides and Sr-Nd. Tektite composition does not match a mix of weathered basalt and Mesozoic sandstone. Mizera also disputes the crater size, the gravity interpretation, the burial and the ejecta. https://onlinelibrary.wiley.com/doi/full/10.1111/maps.13912
  - Mizera & Strunga 2024 argue the diamicton is too thin and lacks megablocks, suevite and polymict breccia. https://www.pnas.org/doi/10.1073/pnas.2400122121 Sieh et al. replied that drilling is still the definitive test. https://www.pnas.org/doi/10.1073/pnas.2401580121
  - Seydoux-Guillaume et al. 2024 studied the only monazite inclusion found in an MN tektite. It places the source in a triangle formed by the Philippines, coastal S China and N Vietnam, and favours the Palawan or South China blocks over Indochina. A comment and reply followed in Geology 2025. https://pubs.geoscienceworld.org/gsa/geology/article/52/12/865/648099/Clues-on-the-Australasian-impact-crater-site
  - Size: Glass & Pizzuto 1994 estimate 32–114 km and Whymark 2021 estimates about 43 km, against 13–17 km for Bolaven.
  - Karimi et al. 2023 propose a rival site.
- **NEW (T4): a falsification test from the unpublished repository.**
  - Two in-situ basalt flows, PKS-J at 15.2431, 106.2581 and PKS-K at 15.2419, 106.2585, lie **inside both** digitised crater outlines, 2.7–6 km from the centre.
  - Their Ar/Ar ages are 407–601 ka, but both carry well-defined **reversed** (Matuyama) magnetisation, so they are probably older than 773 ka.
  - If re-dating gives more than 788 ka, pre-impact lava survives intact over the crater centre, and that falsifies this crater outline.
  - If it gives 773–788 ka, these would be the first dated post-impact crater fill, which strongly supports the crater.
  - The repository's "conglomerate test" results disagree between its own files, so I give them no weight. The same repository's rjMCMC mixing model returns only about 5% basalt in the tektites, which agrees with Mizera's point about the basalt.
- Novelty check: the crater location is PROPOSED (Sieh 2020). I searched "Bolaven" together with the paleomagnetism and reversed-polarity terms and found no publication on the in-crater polarity contradiction. That test is NOVEL-SYNTHESIS.
- Orbital signature: none. In GLO-30 the site is a convex summit dome at about 1,250–1,275 m, with at most a 20 m low within 3 km of the centre and no rim at 6.5–8.5 km (`data/T4/scan_box_stats.json`). The crater is not visible in S2 or the DEM; finding it needs gravity data or a drill hole.
- Biggest reason it could be wrong: the geochemistry and monazite evidence point away from a basalt-and-sandstone target on the Indochina block, and the crater looks too small for the volume of ejecta.
- Confidence (that the AAT crater is within ±10 km): 35

### C2. Central Laos MN-type cluster (Savannakhet–Xepon), DEM falsification target — PROPOSED (region) / derived centroid new
- Coordinates: 16.22, 106.39 (±60 km). This is the geometric median of 28 unique MN-type find sites from the literature, excluding the Sieh S1 set. Including S1 gives 15.63N, 106.19E.
- Significance 9. MN-type (layered, proximal) tektites are found mainly in Laos and Thailand (Boschi et al. 2025, https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024GC012133). The asymmetric microtektite fit here gives r²=0.801, downrange at 202°.
- Evidence chain:
  1. MN distribution: `data/T4/aa_tektite_localities.csv`.
  2. Microtektite fit: `mt_fit.py`.
  3. The impact was oblique toward the south (Beijing boreholes, above), so the crater should lie uprange (north) of the symmetric best fit at 12N, which places it at or north of about 15N.
- Novelty check: "central Indochina" is a long-standing generic proposal. I found no published crater site at this centroid.
- Orbital signature: there is no young lava cover here. A 15–45 km crater in Khorat sandstone, 788 ka old, should still show as a basin or partial ring with 100–300 m of relief, which would be **DEM-visible**. If the lead's DEM shows no such basin, the result supports burial (C1) or an offshore site (C3).
- Biggest reason it could be wrong: MN finds cluster where people have collected, and tropical erosion or alluvium could hide the rim.
- Confidence: 12

### C3. Gulf of Tonkin / Yinggehai (Song Hong) basin floor — PROPOSED
- Coordinates: 19.0, 107.8 (±120 km). I derived this from Whymark's verbal location, "floor of the Yinggehai/Beibu Gulf", not from a figure.
- Significance 10. Evidence chain:
  1. Whymark 2021 (Thai Geosci. J.) reviews the case for a Gulf of Tonkin site and a single crater of about 43 km. https://ph03.tci-thaijo.org/index.php/TGJ/article/view/1782
  2. Glass & Koeberl 2006 (as cited later) place the source in S China–N Vietnam–Gulf of Tonkin, with a crater of about 50 km. https://www.academia.edu/45122493/Constraints_on_the_Location_of_the_Australasian_Tektite_Impact_Crater
  3. The monazite triangle includes N Vietnam and S China (C1, item 3 of the adversarial list).
  4. South China MN-type tektites exist (Boschi 2025).
- Against: in the symmetric microtektite fit, r²=0.761 (F=8.0, p≈0.001). With asymmetry it rises to 0.797. [Reasoning] The Yinggehai basin is a petroleum province covered by heavy seismic surveys, so a 40 km crater should already have been reported.
- Orbital signature: submerged and buried in sediment; not visible in S2 or the DEM. Only seismic data can test it.
- Confidence: 15

### C4. Tonle Sap, Cambodia — PROPOSED
- Coordinates: 12.9, 104.1 (±40 km), my estimate of the lake centre. Source: Hartung & Koeberl 1994. https://www.researchgate.net/publication/234408269_A_POSSIBLE_SOURCE_IN_CAMBODIA_FOR_AUSTRALASIAN_TEKTITES
- Significance 10. For: in my replication the symmetric best fit is 12.0N 105.75E, which matches Glass & Pizzuto 1994 (12N 106E; https://agupubs.onlinelibrary.wiley.com/doi/10.1029/94JE01866). Tonle Sap scores r²=0.798.
- Against: the symmetric fit is biased downrange (south), and the median MN find lies 444 km away.
- Orbital: alluvial lake basin, flat, not visible in the DEM.
- Confidence: 5

### C5. Leizhou Peninsula–N Hainan young basalt field (a "Bolaven analogue") — NOVEL-SYNTHESIS (weak)
- Coordinates: 20.3, 110.0 (±80 km).
- Evidence chain: it lies inside the monazite triangle (C1) and near South China MN-type tektites (Boschi 2025). It is about 200 km from Whymark's Yinggehai site and uprange of the SSW-directed asymmetry. [BK] The Leiqiong Quaternary basalt field could bury a crater, as at Bolaven.
- Against: symmetric r²=0.717 (F=16.6); asymmetric r²=0.790 needs a 0.63 log-unit asymmetry. The field also contains maars, which would look like circular false positives.
- Novelty: none of my roughly 20 AAT-source searches surfaced this area; I could not run a dedicated search.
- Orbital: buried; a test needs a public gravity model to look for a circular Bouguer low.
- Confidence: 5

### C6. Badain Jaran megadune-lake area, NW China — PROPOSED (disfavoured)
- Coordinates: 39.75, 102.4 (±50 km), APPROXIMATE, from the paper's verbal description.
- Source: Karimi et al. 2023 report annular gravity highs around a low and a magnetic anomaly. https://www.nature.com/articles/s41598-023-40177-7
- Against:
  - No AA microtektites in 19 Chinese Loess Plateau sections. https://www.sciencedirect.com/science/article/abs/pii/S003101822100506X
  - None in Beijing Plain boreholes (above).
  - My fit: r²=0.617; the site was **never selected in 500 bootstraps** (F=35.8). Even with asymmetry it needs a 68× N–S abundance asymmetry and still reaches only r²=0.747.
  - MN finds lie about 2,500 km away.
- Orbital: buried under megadunes; not visible in the DEM.
- Confidence: 2

### C7. Libyan Desert Glass source — PROPOSED (structure link) / origin unresolved
- Coordinates: 25.4, 25.0 (±80 km). This spans the [BK] LDG field at about 25.5N 25.5E and the EID structures BP (25.317, 24.333; 2 km) and Oasis (24.583, 24.4; 18 km), which lie roughly 117 and 151 km west of the field. The EID gives both only a "<120 Ma" age.
- Significance 8. Evidence chain:
  1. Reidite in LDG zircons shows an impact origin, not an airburst (Cavosie & Koeberl). https://theconversation.com/how-we-solved-the-mystery-of-libyan-desert-glass-117253
  2. High-pressure ZrO₂ phases (2023). https://www.researchgate.net/publication/370143218
  3. Magnani 2026 finds that dendritic zircon cannot distinguish the formation models and gives a liquidus of at least about 2250 °C. https://onlinelibrary.wiley.com/doi/10.1111/maps.70094
  4. Kebira (31 km) was proposed from satellite data only, and field visits found no evidence. https://en.wikipedia.org/wiki/Kebira_Crater Reimold & Koeberl 2014 list it as discarded.
  5. The Gilf Kebir "crater field" is non-impact. https://www.researchgate.net/publication/249502283
- Test: date the BP and Oasis melt or breccia. An age near [BK] 29 Ma would identify the source.
- Orbital: BP and Oasis are DEM-visible ring structures. A buried LDG crater under the Great Sand Sea would not be visible.
- Biggest risk: [BK] earlier work may already have dated these structures or ruled them out (I could not check), and the glass and its source may differ in composition.
- Confidence: 10

### C8. Al Madafi, Tabuk, Saudi Arabia — PROPOSED (most testable untested structure)
- Coordinates: 28.67, 37.18 (±3 km); diameter 6 km. Source: the Wikipedia possible-structures list, via the astrobleme catalogue (`provenance.csv`).
- Significance 4. It is arid, the rock is exposed and the site is reachable by road [BK]. A test needs only sampling for shatter cones and PDFs.
- Orbital: should be DEM-visible at 6 km.
- Biggest risk: its status may have changed after mid-2026.
- Confidence (impact origin): 25

## Other strewn fields and glasses with unknown sources
- **Ananguites** (Musolino et al. 2025, EPSL): a new strewn field dated 10.76±0.05 Ma, about 900 km long, mainly in South Australia. The crater has not been found. Their isotopes match a volcanic arc (Luzon, Sulawesi or Bismarck, PNG); a crater within Australia is favoured if the crater-to-field distance is under 2,000 km, and the New England paleo-arc is not excluded. https://www.sciencedirect.com/science/article/pii/S0012821X2500398X ; https://phys.org/news/2025-09-evidence-distinct-australian-tektite-groups.html. This is the best new crater-hunt target after the AAT, but it is a job for gravity data, not a small-bowl DEM search.
- **Irghizites** come from Zhamanshin (KNOWN), which was once proposed as the AAT source (Geology 1979). https://pubs.geoscienceworld.org/gsa/geology/article-abstract/7/7/351/188232
- **Darwin glass:** Darwin Crater (-42.317, 145.667; 1.2 km) is still listed as "possible".
- **Belize tektites → Pantasma** (13.37, -85.95), now in the confirmed class.
- Newer AA-field work:
  - Organic residues from biomass in an MN tektite (Zanetta 2026) imply a vegetated target. https://onlinelibrary.wiley.com/doi/10.1111/maps.70116
  - A microkrystite (Del Rio 2026). https://onlinelibrary.wiley.com/doi/10.1111/maps.70238
  - Whymark proposes "uprange" tektites (MetSoc 2025). https://www.hou.usra.edu/meetings/metsoc2025/pdf/5080.pdf

## Proposed structures ranked by testability (status from Wikipedia possible list and Reimold & Koeberl 2014; all in the CSV)
1. Al Madafi, SA (28.67, 37.18; 6 km)
2. El Mrayer, Mauritania (22.5, -7.2; 2 km)
3. Temimichat, Mauritania (24.25, -9.65; 0.7 km)
4. Jeptha Knob, KY (38.18, -85.12) and Howell, TN (35.23, -86.61): drill cores exist
5. Bajada del Diablo, AR (-42.82, -67.47): contested crater field
6. Bukit Bunuh, MY (5.08, 100.98)
7. Bolaven: a 300–600 m drill hole would settle it
8. Sudan Bayuda (18.06, 33.50) and Mahas (20.03, 30.23): remote-sensing only, access blocked by the war
9. Libya: Garet El Lefet (25.0, 16.5), Ibn-Batutah (21.57, 20.84), Jebel Hadid (20.87, 22.71); Niger: Arlit (21.35, 9.15). All remote-sensing only, with poor security.
10. Offshore, testable only by drilling: Nadir (9.4, -17.1), Silverpit (54.23, 1.85), Velingara (13.04, -14.13)

## DEM-scan boxes (item 5; the lead has already run a global scan, so these are kept short)
These are computed metrics (`data/T4/scan_box_stats.json`): median local relief within 1 km, and the share of WorldCover class "bare/sparse".

| Box | Lat range | Lon range | Median 1 km relief | Bare/sparse | Note |
|---|---|---|---|---|---|
| Nullarbor WA | -31.5 to -29.5 | 126.5–128.5 | 3.9 m | 0% | 94% grass; dolines are false positives |
| Jiddat al-Harasis, Oman | 19–21 | 55.5–57.5 | 3.8 m | 100% | |
| Tanezrouft | 21–23 | -1–1 | 4.5 m | 100% | |
| Atacama Central Depression | -21.9 to -19.9 | -70.1 to -69.1 | | 98.7% | Mine pits and salars are false positives |
| Beishan | 41–43 | 96–98 | 20.6 m | | Rough |

None of these boxes contains a structure from the CSV.

Expected yield [BK rate, order of magnitude]: about 0.1–0.5 new 0.3–5 km craters per 2°×2° box.

## Dead ends
- en.wikipedia.org, wikiwand and ncbi were blocked for WebFetch; I recovered the Wikipedia lists from the astrobleme repository instead.
- impactearth.com is unreachable, and I found no bulk export.
- The GitHub repository GT-IMPACT/ImpactStructures is a Minecraft mod.
- With an asymmetry term the microtektite fit cannot constrain location: it puts the best fit at 9N 109E with r² flat across the region.
- I could not obtain the ODP 1144A and other South China Sea abundances, so the northern constraint is weak.
- The coordinates for Badain Jaran and Yinggehai could not be taken from the papers' figures.

## Sources
- https://www.pnas.org/doi/10.1073/pnas.1904368116 ; https://www.pnas.org/doi/10.1073/pnas.1920576117 ; https://www.pnas.org/doi/10.1073/pnas.2310351120 ; https://www.pnas.org/doi/10.1073/pnas.2400122121 ; https://www.pnas.org/doi/10.1073/pnas.2401580121
- https://onlinelibrary.wiley.com/doi/full/10.1111/maps.13912 ; https://www.nature.com/articles/s41598-023-40177-7 ; https://www.sciencedirect.com/science/article/abs/pii/S003101822100506X ; https://www.nature.com/articles/s44453-025-00017-6
- https://agupubs.onlinelibrary.wiley.com/doi/10.1029/94JE01866 ; https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2006JE002857 ; https://www.researchgate.net/publication/253605707
- https://pubs.geoscienceworld.org/gsa/geology/article/52/12/865/648099/Clues-on-the-Australasian-impact-crater-site ; https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024GC012133 ; https://ph03.tci-thaijo.org/index.php/TGJ/article/view/1782 ; https://progearthplanetsci.springeropen.com/articles/10.1186/s40645-024-00660-9
- https://www.sciencedirect.com/science/article/pii/S0012821X2500398X ; https://theconversation.com/how-we-solved-the-mystery-of-libyan-desert-glass-117253 ; https://onlinelibrary.wiley.com/doi/10.1111/maps.70094 ; https://en.wikipedia.org/wiki/Kebira_Crater
- https://ui.adsabs.harvard.edu/abs/2022ESRv..23204112O (Impact Earth)
- Data: https://raw.githubusercontent.com/cjwinchester/earth-impact-data/main/earth-impact-craters.csv ; https://github.com/nobulart/astrobleme ; https://github.com/yicolas/2024_Laos_Australasian_Impactor (unpublished, Nov 2026) ; s3 copernicus-dem-30m ; esa-worldcover

```json
[
{"id":"T4-C1","name":"Bolaven buried crater (AAT source)","lat":15.203,"lon":106.271,"radius_km":10,"feature_size_m":15000,"signature":"buried under <0.8 Ma basalt; convex summit dome in DEM, no rim; gravity low","s2_visible":false,"dem_visible":false,"significance":10,"novelty":"PROPOSED","confidence":35,"looting_sensitive":false,"category":"impact_crater","one_line":"Sieh 2020 site; new test: reversed-polarity in-situ flows inside outline must date 773-788 ka or crater is falsified"},
{"id":"T4-C2","name":"Central Laos Muong Nong cluster","lat":16.22,"lon":106.39,"radius_km":60,"feature_size_m":30000,"signature":"if unburied: eroded 15-45 km basin/partial ring, 100-300 m relief in Khorat sandstone","s2_visible":false,"dem_visible":true,"significance":9,"novelty":"PROPOSED","confidence":12,"looting_sensitive":false,"category":"impact_crater","one_line":"Geometric median of literature MN-type tektite finds; a DEM check can falsify an exposed crater here"},
{"id":"T4-C3","name":"Gulf of Tonkin / Yinggehai basin floor","lat":19.0,"lon":107.8,"radius_km":120,"feature_size_m":43000,"signature":"submerged, sediment-buried; seismic only","s2_visible":false,"dem_visible":false,"significance":10,"novelty":"PROPOSED","confidence":15,"looting_sensitive":false,"category":"impact_crater","one_line":"Whymark 2021 site; fits microtektites only with SSW asymmetry"},
{"id":"T4-C4","name":"Tonle Sap","lat":12.9,"lon":104.1,"radius_km":40,"feature_size_m":40000,"signature":"alluvial lake basin, no DEM expression","s2_visible":false,"dem_visible":false,"significance":10,"novelty":"PROPOSED","confidence":5,"looting_sensitive":false,"category":"impact_crater","one_line":"Hartung & Koeberl 1994; matches symmetric microtektite best fit (12N 105.75E) but far from MN tektites"},
{"id":"T4-C5","name":"Leizhou-N Hainan basalt field","lat":20.3,"lon":110.0,"radius_km":80,"feature_size_m":30000,"signature":"buried under Quaternary basalt; test with gravity","s2_visible":false,"dem_visible":false,"significance":10,"novelty":"NOVEL-SYNTHESIS","confidence":5,"looting_sensitive":false,"category":"impact_crater","one_line":"Bolaven analogue inside the monazite triangle near S China MN tektites; weak"},
{"id":"T4-C6","name":"Badain Jaran megadune-lake area","lat":39.75,"lon":102.4,"radius_km":50,"feature_size_m":null,"signature":"buried under megadunes; gravity/magnetic anomaly","s2_visible":false,"dem_visible":false,"significance":10,"novelty":"PROPOSED","confidence":2,"looting_sensitive":false,"category":"impact_crater","one_line":"Karimi 2023; contradicted by loess and Beijing nulls and microtektite fit (never selected in 500 bootstraps)"},
{"id":"T4-C7","name":"LDG source: BP/Oasis dating test","lat":25.4,"lon":25.0,"radius_km":80,"feature_size_m":18000,"signature":"BP 2 km and Oasis 18 km ring structures 117-151 km W of LDG field","s2_visible":true,"dem_visible":true,"significance":8,"novelty":"PROPOSED","confidence":10,"looting_sensitive":false,"category":"impact_crater","one_line":"Reidite shows impact origin; date BP/Oasis (<120 Ma) to test a ~29 Ma link"},
{"id":"T4-C8","name":"Al Madafi structure","lat":28.67,"lon":37.18,"radius_km":3,"feature_size_m":6000,"signature":"6 km circular structure in arid exposed rock","s2_visible":true,"dem_visible":true,"significance":4,"novelty":"PROPOSED","confidence":25,"looting_sensitive":false,"category":"impact_crater","one_line":"Most field-testable untested proposed structure (shatter cones / PDF sampling)"}
]
```
