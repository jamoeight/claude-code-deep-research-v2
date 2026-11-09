# T6 — Unexplored giant sinkholes, caves and undocumented waterfalls

## Method (what you joined, what you searched; 5-10 lines)
1. **Web research hit hard limits.** The shared WebSearch budget ran out after about 10 queries. WebFetch could not resolve worldwaterfalldatabase.com, en.wikipedia.org or centre-terre.fr. So I could **not** read the WWD "unconfirmed" or "unverified" lists, and novelty checks on the DEM-derived features below are **incomplete** (see each candidate). The lead should run a quick name and coordinate search before promoting any of them.
2. **Calibrated DEM detectors on Copernicus GLO-30** (17 tiles, scripts in the scratchpad, outputs in `data/T6/`):
   - **D1, closed depressions**: sink-fill by morphological reconstruction, then depth = filled − DEM. I report depth, spill (rim) level, equivalent diameter at mid-depth, and wall slope. Calibration: it recovers **Xiaozhai Tiankeng** 0.12 km from its published position (DEM depth 302 m against a true 511–662 m; d/D 0.63; mean wall slope 54°).
   - **D2, "fake lakes"**: deep pits are radar voids, and editors flatten them as lakes (EDM=9). Calibration: **Sima Humboldt and Sima Martel are both stored as flat "lakes" at 1315 m and 1307 m, within 50 m of their published coordinates.** A third flattened patch sits between them.
   - **W1, waterfall finder**: pysheds D8 flow accumulation, then the drop along the channel within 150, 450 and 2000 m. Calibration: **Angel Falls** comes out at 656 m in 450 m and 936 m in 2 km (catchment 37 km²).
3. **Lessons from calibration.** Copernicus underestimates the depth of deep shafts by 2–3× because the floors are radar shadow, filled from ASTER, SRTM or AW3D30. Dashiwei (Leye, 613 m deep) shows only as a breached ASTER-filled hollow about 200 m deep, and D1 misses it. Naré, at its Wondermondo position, is invisible. **Recall for shafts under about 200 m across is poor. Dolines 300 m–1.5 km across are detected reliably.**
4. **Ranking rule.** I ranked candidates by DEM robustness (floor seen by TanDEM-X versus void-filled), size, and remoteness / expedition history, and labelled each candidate's novelty honestly.

## Candidates (ranked)

### C1. Darai Plateau giant closed doline (Gulf/Southern Highlands, PNG) — NOVEL-SYNTHESIS (novelty check incomplete)
- Coordinates: -6.8594, 143.2436 (±0.5 km)
- What it would be / why it matters (significance 6): a round closed depression **262 m deep** (spill at 920 m, floor at 658 m) and **about 670 m across at mid-depth, 1.3 km at the rim** (D1). If it is one collapse doline, it is in the size class of the largest known tiankeng. If it is compound, it is an uvala. Either way, the shaft or cave at its floor would be the target.
- Evidence chain:
  1. D1 output `data/T6/pits_darai.json`. Profiles: E–W 935→658→947 m; N–S 939→658→966 m.
  2. The floor and walls are **real TanDEM-X data** (FLM=2, EDM=1), not void fill, so the 262 m is a minimum. Calibration (Xiaozhai) suggests shaft depths are underestimated.
  3. Tile S07_E143 was chosen to cover the Darai polygonal-karst plateau. The place-name attribution is from general knowledge and was not source-verified in this session. Crop: `data/T6/crop_darai.png`.
- Novelty check: before the budget ran out I searched only Nakanai, Leye and the calibration sites. **I searched nothing on Darai.** Status: not found, but not searched.
- Orbital signature: a near-circular forested bowl about 1.3 km across with a shadowed interior. S2-visible (yes, from relief and shadow) and DEM-visible (yes).
- Biggest reason it could be wrong: it could be a known, mapped cockpit or polje, since the Darai is noted for its large polygonal karst. It may also be a compound depression rather than a single collapse.
- Confidence: 45

### C2. Lengguru karst giant doline "B" (Kaimana/Bintuni, West Papua) — NOVEL-SYNTHESIS (novelty check incomplete)
- Coordinates: -3.2692, 133.8425 (±0.5 km)
- What it would be / why it matters (significance 6): a closed depression **223 m deep** (spill at 769 m, floor at 546 m), **about 785 m across at mid-depth** and about 1.5 km at the rim. It lies in the poorly speleologised Lengguru fold belt.
- Evidence chain:
  1. D1 output `data/T6/pits_lengguru.json`. Profiles: E–W 828→551→1027 m; N–S 814→552→866 m.
  2. The data are mostly TanDEM-X with some SRTM30 fill (FLM 2/5). Crop: `data/T6/crop_lengguru_B.png`.
  3. No tiankeng-grade steepness (mean wall slope 23°). Treat it as a giant doline or uvala, not a shaft.
- Novelty check: Lengguru was not searched (budget exhausted). I know of no caving literature for this tile, and that knowledge is unverified.
- Orbital signature: a forested bowl about 1.5 km across. S2-visible: yes. DEM-visible: yes.
- Biggest reason it could be wrong: it may be a structural or fluvial basin with a hidden outlet, or a DEM fill artefact on one wall.
- Confidence: 40

### C3. Lengguru giant closed basin "A" (West Papua) — NOVEL-SYNTHESIS (novelty check incomplete)
- Coordinates: -3.3492, 133.9714 (±0.8 km)
- What it would be / why it matters (significance 6): a closed basin **255 m deep** (spill at 555 m, floor at about 300 m), **about 1.5 km across at mid-depth** and 2.5 km overall. The central floor is **AW3D30-filled (FLM=9)**, so TanDEM-X could not see it. That is the radar-shadow signature of steep walls seen at Xiaozhai and Dashiwei. It is a polje or giant-doline candidate with possible ponors.
- Evidence chain:
  1. D1 output `data/T6/pits_lengguru.json`. Profiles: E–W 726→300→700 m; N–S 668→300→575 m.
  2. FLM along the profile: a void-filled core about 1 km across. Crop: `data/T6/crop_lengguru_A.png`.
- Novelty check: as for C2. Not searched.
- Orbital signature: a large bowl or flat floor 1.5–2.5 km across. S2-visible: yes. DEM-visible: yes.
- Biggest reason it could be wrong: a void-filled floor can also mean a lake or swamp. Low coherence would void it, but no EDM lake flag is set.
- Confidence: 35

### C4. Steep "tiankeng-like" pit, Phong Nha–Ke Bang / Hin Nam No border karst — NOVEL-SYNTHESIS (novelty doubtful; heavily expedition-explored region)
- Coordinates: 17.6169, 106.0739 (±0.3 km)
- What it would be / why it matters (significance 5): the steepest non-Chinese pit in my scans. DEM depth **207 m (minimum)**, spill at 508 m, **about 330 m across at mid-depth**, 90th-percentile wall slope 58°, d/D 0.35. The centre is partly ASTER-filled (radar shadow), so the true depth is probably greater.
- Evidence chain:
  1. D1 output `data/T6/pits_khammouane_phongnha.json`. Profiles: E–W 632→301→529 m; N–S 639→312→620 m.
  2. Of the 982 depressions of 60 m or more in N17_E105/E106, only 14 pass d/D ≥0.3 with slope ≥33°. This is the second deepest of them. Crop: `data/T6/crop_hinnamno_pn.png`.
- Novelty check: not searched. British–Vietnamese teams have mapped this area for decades, so it is plausibly already known. I could not determine which side of the Laos–Vietnam border it falls on.
- Orbital signature: a near-round shadowed pit about 400–500 m across at the rim. S2-visible: yes. DEM-visible: yes.
- Biggest reason it could be wrong: it is probably already documented, or it is a doline that feeds a known cave.
- Confidence: 30

### C5. Tall waterfall at the lip of the Star Mountains southern escarpment, E of Tabubil (W. Province, PNG) — NOVEL-SYNTHESIS (WWD not checkable)
- Coordinates: -5.2633, 141.3469 (±0.5 km); top of the drop at about 1,830 m.
- What it would be / why it matters (significance 7): a channel with a **42 km² catchment** reaches a cliff and drops **608 m in 450 m horizontal** (295 m in 150 m) and **897 m in 2 km**. That is the same DEM signature as Angel Falls (656 m in 450 m, 37 km²). The tile covers the Star Mountains and Hindenburg Range escarpment; that attribution was not source-verified.
- Evidence chain:
  1. W1 output `data/T6/falls_hindenburg.json`. Path: 1827→1134 m in 538 m.
  2. The steep segment is ASTER-filled (FLM=3), which is a layover/shadow void, as expected on a near-vertical wall.
  3. Upstream, the plateau holds a **185 m deep, 2.6 km closed depression** centred at -5.2311, 141.3306 (D1), so it is karst.
  4. Second candidate on the same escarpment: -5.2647, 141.5678 (75.5 km², 244 m in 150 m). That step coincides with an FLM 3→2 seam, so it may be an artefact. Crop: `data/T6/crop_hindenburg_fall1.png`.
- Novelty check: the WWD was unreachable and nothing was searched. Status unknown.
- Orbital signature: a south-facing cliff of about 600 m. Watch for white water or a spray zone at the lip; it may be visible in S2 after rain. DEM-visible: yes. Whether water actually falls needs S2 time series or sub-metre imagery.
- Biggest reason it could be wrong: in karst the surface catchment may sink before the lip, giving a dry hanging valley with the water resurging at the foot. It may also be a steep cascade rather than a free fall.
- Confidence: 30

### C6. Deep closed doline in tile S06_E142 (Hela/Southern Highlands, N of the Muller Range area) — NOVEL-SYNTHESIS (novelty check incomplete)
- Coordinates: -5.3711, 142.3350 (±0.3 km)
- What it would be / why it matters (significance 5): **138 m deep** (spill at 1,065 m), **about 260 m across at mid-depth**, about 450 m at the rim, d/D 0.32. The floor is seen by TanDEM-X (FLM=2), so it is robust. It sits in the karst highlands of the Atea Kananda region (attribution unverified).
- Evidence chain:
  1. D1 output `data/T6/pits_muller.json`. Profiles: E–W 1115→929→1110 m; N–S 1082→933→1300 m.
  2. A D2 "lake" patch sits 5 km ENE at -5.3910, 142.3765 (shallow, 1,139 m).
  3. Crop: `data/T6/crop_muller_pit.png`.
- Novelty check: not searched.
- Orbital signature: a round forested pit about 450 m across. S2: marginal (shadow). DEM-visible: yes.
- Biggest reason it could be wrong: it could be an ordinary large cockpit doline among thousands, or one already known to PNG cavers.
- Confidence: 30

### C7. Void-filled steep pit, northern Nakanai plateau (East New Britain, PNG) — NOVEL-SYNTHESIS, but may be KNOWN (Minyé?)
- Coordinates: -5.1908, 151.6664 (±0.3 km)
- What it would be / why it matters (significance 5): **143 m DEM depth** (spill at 1,003 m, floor at 860 m), about 300–420 m across, d/D 0.29. The **centre is void-filled** (FLM 3/1, EDM 2–4), which is the radar-shadow signature of a deep shaft. The true depth could be 2–3× the DEM value.
- Evidence chain:
  1. D1 output `data/T6/pits_nakanai.json`. Crop: `data/T6/crop_nakanai_pit.png`.
  2. The Nakanai holds known giant dolines: Minyé is 350×350 m and 510 m deep, and its coordinates were not found (showcaves.com tiankeng table; wondermondo).
  3. Naré is listed at 5.2940 S, 151.6399 E (±2 km). The DEM shows **no pit there**, which is a detector miss.
  4. French expeditions (1984, 1988, 2016, 2018, 2026) have worked this range from helicopter and aerial photographs (Petzl Black Hole and Ghost Rivers pages; Centre Terre 2026 brochure).
- Novelty check: searched for "Nakanai unexplored dolines helicopter" and for Minyé/Naré coordinates. I found no coordinates for Minyé or Kavakuna. **Cannot resolve** whether this is Minyé or Kavakuna (KNOWN) or an unvisited shaft. Its width matches Minyé's 350 m.
- Orbital signature: a round black hole of 300–400 m in rainforest. S2-visible: yes.
- Biggest reason it could be wrong: it is very likely a known Nakanai doline.
- Confidence: 25 (as a *new* feature)

### C8. Escarpment waterfall, tile S06_E142 (Hela/Southern Highlands, PNG) — NOVEL-SYNTHESIS (WWD not checkable)
- Coordinates: -5.7114, 142.3908 (±0.5 km); top of the drop at about 2,140 m.
- What it would be / why it matters (significance 5): with a 21.5 km² catchment, the channel drops **536 m in 450 m** (195 m in 150 m) and **955 m in 2 km**. The steep segment is in **real TanDEM-X data** (FLM=2), not fill.
- Evidence chain:
  1. W1 output `data/T6/falls_muller.json`. Path: 2138→1577 m in 470 m.
  2. Also in this tile: -5.2281, 142.2811, a **153 km²** river dropping 341 m in 450 m and 947 m in 2 km. That looks like a gorge or cascade, a "big-river" candidate.
- Novelty check: none possible (WWD blocked).
- Orbital signature: a steep stream on a scarp of about 550 m. DEM-visible: yes. A free fall needs high-resolution imagery.
- Biggest reason it could be wrong: it is probably a steep cascade series rather than a single fall.
- Confidence: 20

### C9. Alpine pit at ~2,560 m, tile S06_E142 (Hela, PNG) — NOVEL-SYNTHESIS (novelty check incomplete)
- Coordinates: -5.5644, 142.4961 (±0.3 km)
- What it would be / why it matters (significance 4): **116 m deep** (spill at 2,559 m), about 210 m across at mid-depth, d/D 0.31, 90th-percentile wall slope 49°. TanDEM-X data. This would be a high-altitude shaft entrance in montane karst.
- Evidence chain: D1 output `data/T6/pits_muller.json`. Profiles: E–W 2662→2443→2575 m; N–S 2621→2443→2591 m.
- Novelty check: not searched.
- Orbital signature: a pit about 380 m across at the rim. S2: marginal (cloud). DEM: yes.
- Biggest reason it could be wrong: it may be a glacial or periglacial hollow, or an ordinary doline.
- Confidence: 20

### C10 (calibration). Sarisariñama sima cluster, Venezuela — KNOWN
- Coordinates: 4.6806, -64.2252 (±0.3 km). This is the third "fake-lake" patch, 3.6 ha, eq. diameter 214 m, flattened at 1,303 m, between Humboldt (4.6856, -64.2186) and Martel (4.6775, -64.2222).
- What it would be / why it matters (significance 3): it validates detector D2. Both Sima Humboldt (314 m deep) and Sima Martel (248 m deep) are stored as EDM "lakes" at their published coordinates. The third patch is probably one of the other known simas, but I **cannot resolve** which.
- Evidence chain: `data/T6/lakes_sarisarinama.json`; Wikipedia's Sima Humboldt and Sima Martel coordinates. A fourth D2 patch on the Jaua massif (4.8822, -64.5356) turned out to be a 40 m bog hollow, so I rejected it.
- Novelty check: Humboldt and Martel are KNOWN. The third patch is unresolved.
- Orbital signature: round shafts 150–350 m across on the tepui top. S2-visible: yes.
- Biggest reason it could be wrong: none for the calibration use.
- Confidence: 90 (that it is a real sima)

## Dead ends (things you checked that did not pan out, 1 line each)
- WWD "unconfirmed" and "unverified" lists: host unreachable from WebFetch, so they were not read.
- Nakanai 1988 "enormous doline between the Galowe and Wunung gorges" (a bowl with no river): it is reported, and the 2016 Black Hole was found near it. I could not locate the gorges without a map. Large bowls in the DEM at -5.4697, 151.4108 (205 m deep, 1.6 km) and -5.6603, 151.2272 (265 m deep, 2.3 km) are possible matches. Unresolved.
- Naré (5.294 S, 151.640 E, wondermondo): no pit in the DEM within 4 km. Either the coordinates are wrong or the shaft is too narrow for radar.
- Dashiwei (24.808 N, 106.444 E): only an ASTER-filled, breached hollow about 200 m deep. D1 misses it.
- 2022 Leye tiankeng near Ping'e village (306×150×192 m): no published coordinates found, so I could not match it.
- "Fake-lake" detector on PNG highlands and Khammouane: dozens of EDM=9 patches (real ponds, swamps and cloud voids). Not specific enough without imagery.
- Nakanai -5.12, 151.758 (143 m deep pit): entirely ASTER-filled, with a probable cloud artefact.
- Jaua 4.99, -64.45 (110 m D1 pit): it is an open valley, not a closed depression.
- Auyantepui 5.864, -62.517 (384 m "pit"): an SRTM30+ fill artefact inside the Devil's Canyon.
- Mulu tile: only 6 depressions of 60 m or more; nothing new.

## Sources
- Petzl, BLACK HOLE expedition (1988 helicopter flight; "enormous doline" between Galowe and Wunung; black hole about 100 m wide): https://www.petzl.com/SE/en/Sport/News/2017-4-12/BLACK-HOLE--exploring-a-world-without-light
- Petzl, GHOST RIVERS expedition (Wunung resurgence): https://www.petzl.com/INT/en/Sport/News/2018-6-6/GHOST-RIVERS-expedition
- Centre Terre, PNG 2026 Mayang brochure (Mayang resurgence found 1984 on a helicopter survey of the Galowe gorges): https://www.centre-terre.fr/mayang2026/plaquette/CT-PNG-2026-en.pdf
- Petzl, 2026 PNG expedition: https://www.petzl.com/be/en/sport/we-are-petzl/caving/inside-a-2026-expedition-to-papua-new-guinea/-NEWS--SPORT--Recit-d-une-expedition-en-Papouasie-_SPO_a7CbK0000000hplUAA.html
- Minyé 350×350×510 m: https://showcaves.com/english/explain/Karst/Tiankeng.html ; https://wondermondo.com/minye-sinkhole-and-cave
- Naré coordinates: https://wondermondo.com/nare-sinkhole
- JCU Nakanai booklet: https://researchonline.jcu.edu.au/74406/1/Nakanai_Mountains_ENB_FINAL_V.2_June%202022.pdf
- Sima Humboldt and Sima Martel coordinates and depths: https://en.wikipedia.org/wiki/Sima_Humboldt ; https://en.wikipedia.org/wiki/Sima_Martel
- Xiaozhai coordinates: https://en.wikipedia.org/wiki/Xiaozhai_Tiankeng
- Dashiwei coordinates: https://wondermondo.com/dashiwei-tiankeng
- 2022 Leye tiankeng: https://ukranews.com/en/news/855624-giant-karst-sinkhole-discovered-in-china-s-guangxi ; https://regional.chinadaily.com.cn/guangxi/2022-05/09/c_749580.htm
- Copernicus FLM/EDM codes: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_DEM_GLO30
- DEM data: s3://copernicus-dem-30m (tiles listed in `data/T6/*.json`)

```json
[
{"id":"T6-C1","name":"Darai Plateau giant closed doline","lat":-6.8594,"lon":143.2436,"radius_km":0.5,"feature_size_m":1300,"signature":"round closed depression 262 m deep (DEM, TanDEM-X floor), ~670 m wide at mid-depth, 1.3 km rim","s2_visible":true,"dem_visible":true,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":45,"looting_sensitive":false,"category":"giant doline","one_line":"262 m deep, 1.3 km closed doline in Darai karst; floor seen by TanDEM-X; novelty search not run"},
{"id":"T6-C2","name":"Lengguru giant doline B","lat":-3.2692,"lon":133.8425,"radius_km":0.5,"feature_size_m":1500,"signature":"closed depression 223 m deep, ~785 m at mid-depth","s2_visible":true,"dem_visible":true,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":40,"looting_sensitive":false,"category":"giant doline","one_line":"223 m deep giant doline/uvala in little-caved Lengguru fold belt, West Papua"},
{"id":"T6-C3","name":"Lengguru closed basin A","lat":-3.3492,"lon":133.9714,"radius_km":0.8,"feature_size_m":2500,"signature":"255 m deep closed basin, ~1.5 km at mid-depth, floor AW3D30-filled (radar shadow)","s2_visible":true,"dem_visible":true,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":35,"looting_sensitive":false,"category":"giant doline/polje","one_line":"2.5 km, 255 m deep closed karst basin with void-filled floor, West Papua"},
{"id":"T6-C4","name":"Phong Nha/Hin Nam No steep pit","lat":17.6169,"lon":106.0739,"radius_km":0.3,"feature_size_m":500,"signature":"steep pit >=207 m deep, ~330 m mid-depth, p90 wall slope 58 deg, partly void-filled","s2_visible":true,"dem_visible":true,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":30,"looting_sensitive":false,"category":"tiankeng candidate","one_line":"Tiankeng-like pit on the Laos-Vietnam karst border; region heavily explored, may be known"},
{"id":"T6-C5","name":"Star Mountains escarpment waterfall E of Tabubil","lat":-5.2633,"lon":141.3469,"radius_km":0.5,"feature_size_m":600,"signature":"42 km2 channel reaches cliff lip, 608 m drop in 450 m, 897 m in 2 km (Angel Falls-like DEM signature)","s2_visible":false,"dem_visible":true,"significance":7,"novelty":"NOVEL-SYNTHESIS","confidence":30,"looting_sensitive":false,"category":"waterfall","one_line":"Possible ~600 m escarpment fall on karst plateau edge; may be dry hanging valley"},
{"id":"T6-C6","name":"S06E142 deep doline (Hela)","lat":-5.3711,"lon":142.3350,"radius_km":0.3,"feature_size_m":450,"signature":"138 m deep, ~260 m mid-depth, TanDEM-X floor","s2_visible":false,"dem_visible":true,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":30,"looting_sensitive":false,"category":"doline","one_line":"Robust 138 m deep round doline in PNG highland karst"},
{"id":"T6-C7","name":"Northern Nakanai void-filled pit","lat":-5.1908,"lon":151.6664,"radius_km":0.3,"feature_size_m":400,"signature":"143 m DEM depth with void-filled centre (radar shadow), 300-420 m wide","s2_visible":true,"dem_visible":true,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":25,"looting_sensitive":false,"category":"giant doline/shaft","one_line":"Deep shaft signature in Nakanai; may be known Minye/Kavakuna, cannot resolve"},
{"id":"T6-C8","name":"S06E142 escarpment waterfall","lat":-5.7114,"lon":142.3908,"radius_km":0.5,"feature_size_m":550,"signature":"21.5 km2 channel, 536 m drop in 450 m in real TanDEM-X data","s2_visible":false,"dem_visible":true,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":20,"looting_sensitive":false,"category":"waterfall","one_line":"Steep ~540 m scarp stream, likely tiered fall/cascade"},
{"id":"T6-C9","name":"Alpine pit at 2560 m (Hela)","lat":-5.5644,"lon":142.4961,"radius_km":0.3,"feature_size_m":380,"signature":"116 m deep, ~210 m mid-depth, steep walls","s2_visible":false,"dem_visible":true,"significance":4,"novelty":"NOVEL-SYNTHESIS","confidence":20,"looting_sensitive":false,"category":"doline/shaft","one_line":"High-altitude steep pit, possible montane shaft entrance"},
{"id":"T6-C10","name":"Sarisarinama third flattened sima (calibration)","lat":4.6806,"lon":-64.2252,"radius_km":0.3,"feature_size_m":214,"signature":"EDM 'lake' flattened patch between Sima Humboldt and Sima Martel","s2_visible":true,"dem_visible":true,"significance":3,"novelty":"KNOWN","confidence":90,"looting_sensitive":false,"category":"calibration sinkhole","one_line":"Detector D2 recovers Humboldt and Martel exactly; third patch probably a known sima"}
]
```
