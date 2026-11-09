# T7 — Hidden cities in old data: unmined lidar and tropical earthwork gaps

## Method (what you joined, what you searched; 5-10 lines)
1. **Known-earthwork catalogue.** I used the 1,253 "earthwork" points that Walker et al. 2023 (PeerJ 11:e15137) compiled from published sources (`data/T7/gh/walker_submit.csv`, from github.com/RobertSWalker/ancient_amazonia_archaeology). I checked it against independent coordinates: it reproduces Jacó Sá to within 0.36 km, Tequinho to within 0.13 km and Fazenda Colorada to within 0.03 km. Single-link clustering at 0.25° splits it into the Acre–Pando–Abunã mega-cluster (808 points), Baures (54), Rondônia–Guaporé (39 + 18), the Upper Tapajós in Mato Grosso (36 + 35 + 17 + 12), Nova Mamoré (15), Riberalta (14), Casarabe (6 + 6) and the Upper Xingu (16).
2. **Forest loss.** Hansen Global Forest Change v1.12, `lossyear` band for 2001–2024 (GCS bucket `earthenginepartners-hansen`). I aggregated it to 0.025° and then 0.1° cells (`data/T7/sa_cells_0p1deg.csv`). I slid 0.5° × 0.5° windows across the area and kept those with **zero catalogued earthworks**, the known clusters 5–80 km away, the **largest clearing in 2019–2024**, and median elevation inside the range of the known clusters (AWS terrain tiles; known earthworks sit at 132–262 m, 5th–95th percentile).
3. **Surveyed-zone masks.** I excluded the 2024 Pärssinen et al. airborne-lidar corridors (Rio Branco–Lábrea, Carauari–Lábrea, Manoel Urbano–Lábrea, Carauari–Boca do Acre–Rio Branco, Manoel Urbano–Rio Branco; 4,497 km² in total) and the Acre core.
4. **Maya test.** I tried top-hat peak detection on Copernicus GLO-30 elevation (150 m radius disk), keeping only peaks surrounded by ≥97% ESA WorldCover tree cover within 1.5 km. I calibrated it on Calakmul, El Mirador, Nakbé and Tikal.
5. **Lidar inventory.** Built from about 10 web searches, the Amazonian archaeology atlas on GitHub (tadad/amazonian-archaeology-atlas), and the USGS 3DEP boundary index (hobuinc/usgs-lidar).
6. **Limits.** WebFetch could not reach any publisher host, and the shared web-search budget ran out early. Novelty checks for the boxes therefore rest on the Walker catalogue (compiled about 2022) plus the 2026 Pärssinen corridors. Earthworks found after about 2022 are not checked; the lead should spot-check.

## Part A — Inventory: lidar and high-resolution elevation data collected for non-archaeological purposes

| Dataset | Collected for | Coverage | Access | Archaeological screening status | Promising sub-area (box) |
|---|---|---|---|---|---|
| 2013 forest-carbon lidar, Campeche (the Valeriana source) | Forest carbon monitoring | About 122–129 km² in east-central Campeche | Collector reported as The Nature Conservancy Mexico in Spanish-language coverage (URL not captured; LiveScience says only "a survey to measure and monitor carbon in Mexico's forests"); obtain via the authors | Screened by Auld-Thomas et al. 2024 (Antiquity 98:1340): 6,764 structures, Valeriana second only to Calakmul in density | Any other blocks from the same 2013 campaign are **unverified**. Ask Auld-Thomas or Canuto whether other polygons exist. |
| NASA G-LiHT Mexico/Yucatán transects (LAZ files and visualisations) | Forest structure and carbon | Long transects across southern Mexico. Regions: South, North2, Centro, Norte, Out, Chiapas, Campeche | Open: scholar.uc.edu collections w9505239h (LAZ) and j6731563k (GeoTIFF) | **Mined.** Golden et al. 2016 screened a sample; Schroder et al. 2020 did a full annotation | Re-screen with automated detectors. Detection value is mostly per transect. |
| INEGI lidar (5 m elevation model and canopy height) | National mapping and flood work | Tabasco, southern Veracruz, parts of Campeche, Chiapas and Oaxaca | Public (INEGI) | **Mined for formal ceremonial complexes** (Inomata et al. 2021: 478 complexes). The paper says dense vegetation hampered detection in the Campeche hills and the Palenque–Chinikihá zone | Palenque–Chinikihá zone: re-mine with modern ground classification. Box from memory, unverified: 17.3–17.6 N, −92.1 to −91.6 W. |
| EBA (INPE) plus Sustainable Landscapes Brazil transects, 2008–2018 | Biomass and forest research | 5,315 km² (0.08% of Amazonia) | Open (ORNL DAAC / INPE) | **Screened once.** Peripato et al. 2023 found 24 new and 9 known earthworks; only about half of the flagged features were confirmed | Re-screen with the Wagner et al. 2022 fast terrain-anomaly method. Priority: transects in southern Amazonas, Rondônia and northern Mato Grosso. |
| Colombian forest-carbon airborne lidar (Asner et al. 2012, Biogeosciences 9:2683) | Forest carbon (Carnegie Airborne Observatory with IDEAM) | 465,622 ha in 38 blocks, 2011, about 1.6 returns/m² | Status unknown; request from the Global Airborne Observatory / IDEAM | **Unscreened.** The atlas record finds no archaeological screen in English or Spanish | Block locations are in the paper's figures, which I could not fetch. **This is the best unmined archive found.** |
| USGS 3DEP Puerto Rico, 2015 (LAS 2018) and 2016 (LAS 2017) | Post-hurricane topography and flood mapping | Whole island, bbox −67.963, 17.869, −65.214, 18.527; 89.5 billion + 27.2 billion points | **Open** on S3 (usgs-lidar-public, entwine point tiles: `USGS_LPC_PR_PuertoRico_2015_LAS_2018/ept.json`) | Unknown; could not be searched | Forested karst and the Cordillera Central, for Taíno plazas and ball courts. Sub-box (unverified): 18.20–18.40 N, −66.95 to −66.55 W. |
| G-LiHT Puerto Rico, March 2017 (NGEE-Tropics) | Ecology field sites | Targeted at field sites | OSTI 1582600; ngt-data.lbl.gov NGT0070 | Unknown | Small; 3DEP supersedes it. |
| GEDI spaceborne lidar (25 m footprints) | Global forest structure | Global but sparse | NASA LP DAAC | **Tested for Maya buildings** (Kokalj & Mast, github.com/JohMast/GEDI_Yucatan) | Too sparse for 11 m ditches. At most a screening layer for large mounds such as the Casarabe platforms. |
| Unverified leads from memory (no source this session) | — | NASA LVIS AfriSAR 2016 over Gabon (Lopé, Mondah, Pongara, Rabi, Mabounié); Indonesian peat-restoration lidar 2018–19 (Sumatra, Kalimantan); Carnegie Sabah 2016; Carnegie Peru carbon mapping | Varies | Unknown | Only the Gabon data is likely public. Southern Sumatra coastal peat (Srivijaya-era, heavily looted) would be looting-sensitive. |

For context: Pärssinen et al. 2026 (Nature, doi 10.1038/s41586-026-10835-7) is *archaeological* lidar, not environmental. It covers 4,497 km² in 10 lines, with 6 parallel 1 km swaths about 10 km apart between Rio Branco and Lábrea. It found 432 earthworks, 396 of them new, with density falling toward Lábrea (320 toward Rio Branco against 27 toward Lábrea). Lidar found about five times more than satellite imagery, and satellites mostly find sites in cleared land. **This is why the boxes below target recent clearing.**

## Part B — Geoglyph calibration targets (KNOWN; use these to tune the 10 m Sentinel-2 look)
| Site | Lat, Lon | Source | Notes |
|---|---|---|---|
| Jacó Sá (two geoglyphs) | −9.9606, −67.4975 | 9°57′38″S 67°29′51″W per FAPESP and ecycle; Walker points −9.9638, −67.498 and −9.9639, −67.491 | About 50 km from Rio Branco along the BR-317 |
| Tequinho | −9.897, −67.422 | XRONOS site 37619; Walker −9.8977, −67.423 | Square main enclosure 210 m across, triple ditch, connected roads |
| Fazenda Colorada (Wikipedia label) | −10.6020, −67.9177 | en.wikipedia.org/wiki/Acre_geoglyphs; Walker −10.6021, −67.918 | FAPESP places a "Fazenda Colorada" within 20 km of Jacó Sá, so there may be two sites with this name. Treat the label with caution; the point itself is a catalogued earthwork. |
| Local calibration points (Walker catalogue, unnamed) | −9.372, −65.734 (west edge of A1); −10.153, −64.969 (south of A2); −9.724, −57.173 (south-west of A3); −11.301, −69.127 (Pando, east of A6); −14.283, −64.201 (Mojos, M1) | walker_submit.csv | Use these to see the local version of the signature in each box |

Typical geometry: figures 10–385 m across, ditches about 11 m wide and 1.4 m deep (UNESCO tentative list 5999). At 10 m resolution a ditch is about one pixel wide. Look for closed geometric rings, squares or U-shapes 100–350 m across, as a thin line of greener or darker pasture in the dry season (July–September). The line shows up as NIR/SWIR contrast against browned pasture. Sites are often paired, or joined by parallel embanked roads. Newly cleared ground with slash and burn scars hides ditches for 1–2 years, so compare the 2025 and 2026 dry seasons.

## Candidates (ranked)
All box statistics are in `data/T7/box_stats.csv`, reproducible with `data/T7/box_stats.py`. Each box is 0.5° × 0.5° (about 3,050 km²).

### C1. A1 "North of the Abunã" geoglyph gap box (frontier where Amazonas, Acre and Rondônia meet) — NOVEL-SYNTHESIS
- Coordinates: −9.25, −65.45 (±35 km). Box N −9.0, S −9.5, W −65.7, E −65.2.
- What it would be / why it matters (significance 6): unrecorded ditched enclosures on the east flank of the Acre–Abunã geoglyph cluster, on land cleared since 2019.
- Evidence chain:
  1. No catalogued earthworks inside the box. There are 6 within 50 km and 45 within 100 km; the nearest group (−9.372 to −9.434, −65.734 to −65.816) sits just west of the box edge (Walker 2023, github.com/RobertSWalker/ancient_amazonia_archaeology).
  2. Hansen GFC v1.12: 1,418 km² of forest lost 2001–2024 (46% of the box), including **700 km² in 2019–2024**. That is a large area of new exposure (storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12/).
  3. Median elevation 154 m (10th–90th percentile 124–210 m), the same as the adjacent Abunã cluster (144–189 m).
  4. The box lies about 170 km east of the Pärssinen 2026 Rio Branco–Lábrea transect block (natureasia press release 9397; atlas record).
  5. Peripato et al. 2023 predict the highest earthwork probability in south-western Amazonia (research-portal.uu.nl record; EurekAlert 1003406).
- Novelty check: Walker catalogue plus the 2026 lidar corridors only. Post-2022 or grey-literature finds from IPHAN Rondônia may exist.
- Orbital signature: rings and squares 100–350 m across with ~11 m ditches in pasture. Visible in Sentinel-2 when dry; not visible in 30 m elevation data.
- Biggest reason it could be wrong: the east edge of the cluster may be a real boundary of the earthwork culture, or amateurs scanning Google Earth may already have found sites there.
- Confidence that it holds ≥1 new geoglyph: 45.

### C2. A3 Upper Tapajós / Paranaíta box (northern Mato Grosso) — NOVEL-SYNTHESIS
- Coordinates: −9.45, −56.95 (±35 km). Box N −9.2, S −9.7, W −57.2, E −56.7.
- Significance 6: extends the de Souza et al. 2018 belt of ditched fortified villages (1250–1500 CE), which they modelled over about 400,000 km² of southern Amazonia (pmc.ncbi.nlm.nih.gov/articles/PMC5871619; mongabay 2018).
- Evidence chain:
  1. No catalogued earthworks inside; 3 within 50 km and 18 within 100 km. The nearest are at −9.724, −57.173 (39 km) and −9.424, −57.37 (46 km), and the −9.58, −57.95 cluster (36 sites) lies to the west (Walker).
  2. 1,341 km² cleared 2001–2024, 398 km² of it in 2019–2024 (Hansen).
  3. Median elevation 256 m, inside the Upper Tapajós cluster range of 132–291 m.
- Novelty check: Walker catalogue only. Fieldwork after de Souza 2018 is unchecked.
- Orbital signature: ditched enclosures (often D-shaped or circular, 100–300 m) with sunken roads. Visible in Sentinel-2 in pasture.
- Biggest reason it could be wrong: the de Souza team may already have surveyed east of the Teles Pires.
- Confidence: 40.

### C3. A2 Jaci-Paraná / Nova Mamoré box (Rondônia) — NOVEL-SYNTHESIS
- Coordinates: −9.85, −64.95 (±35 km). Box N −9.6, S −10.1, W −65.2, E −64.7.
- Significance 5: sits between the Abunã cluster (−9.07, −66.07) and the Nova Mamoré cluster (−10.39, −65.23), in heavily cleared land.
- Evidence chain:
  1. No catalogued earthworks inside; nearest at −10.153, −64.969 (34 km); 26 within 100 km (Walker).
  2. **1,928 km² cleared 2001–2024 (63% of the box)**, 496 km² of it in 2019–2024 (Hansen).
  3. Median elevation 146 m, matching the Nova Mamoré cluster (111–169 m).
- Novelty check: Walker only. Most clearing predates 2019, so Google Earth users may have looked already.
- Orbital signature: as C1. Visible in Sentinel-2.
- Biggest reason it could be wrong: decades of exposure without published sites could mean genuine absence.
- Confidence: 40.

### C4. A6 Iñapari–Iberia tri-border box (Peru, Bolivia and Brazil) — NOVEL-SYNTHESIS
- Coordinates: −11.45, −69.45 (±35 km). Box N −11.2, S −11.7, W −69.7, E −69.2.
- Significance 6: a political-border survey gap. Brazilian catalogues stop at the Acre River, but the same plateau continues into Madre de Dios (Peru) and Pando (Bolivia).
- Evidence chain:
  1. No catalogued earthworks inside; nearest Pando cluster at −11.30, −69.13 (39 km); 15 within 100 km (Walker).
  2. 746 km² cleared 2001–2024, 432 km² of it in 2019–2024, along the corridor (Hansen).
  3. Median elevation 310 m, in line with western Acre.
- Novelty check: Walker only. Peruvian national (Ministerio de Cultura) records are unchecked.
- Orbital signature: as C1.
- Biggest reason it could be wrong: some of the loss may be gold mining rather than pasture, and the Acre culture may not have crossed the river.
- Confidence: 30.

### C5. A4 Rondônia–Amazonas–Mato Grosso tri-border box (between Machadinho and Colniza) — NOVEL-SYNTHESIS
- Coordinates: −9.25, −60.65 (±35 km). Box N −9.0, S −9.5, W −60.9, E −60.4.
- Significance 5: bridges the Madeira-side clusters and the north-west Mato Grosso clusters (−9.47, −59.79 and −9.93, −59.91).
- Evidence: no catalogued earthworks within 50 km; nearest at −9.614, −60.201 (64 km); 9 within 100 km. 1,008 km² cleared, 454 km² of it in 2019–2024. Median elevation 142 m (Walker; Hansen).
- Novelty check: Walker only.
- Orbital signature: as C1 and C2.
- Biggest reason it could be wrong: this is an interpolation across about 130 km with no anchor site.
- Confidence: 25.

### C6. A5 north-of-Cujubim box (north-east Rondônia) — NOVEL-SYNTHESIS
- Coordinates: −8.65, −62.65 (±35 km). Box N −8.4, S −8.9, W −62.9, E −62.4.
- Significance 5: **the most land cleared in 2019–2024 of any Brazilian box without known earthworks (942 km², 31% of the box in six years)**.
- Evidence: one catalogued earthwork within 100 km (−9.11, −62.635, 51 km away). Median elevation 99 m, which is **below** the 5th percentile of known sites. An alternative box with a better elevation fit is N −8.9, S −9.4, W −62.6, E −62.1 (median 126 m, nearest known 10 km, 349 km² cleared recently).
- Orbital signature: as C1.
- Biggest reason it could be wrong: low terraces outside the known environmental range, and possibly protected areas.
- Confidence: 20.

### C7. M1 Baures–Casarabe gap box (Llanos de Mojos, Bolivia) — NOVEL-SYNTHESIS
- Coordinates: −14.45, −64.25 (±35 km). Box N −14.2, S −14.7, W −64.5, E −64.0.
- Significance 6: the forested interfluve between the Baures ring-ditch cluster (54 points, centroid −13.52, −63.64) and the Casarabe cluster (around −14.8 to −15.3, −64.3 to −64.9). The Prümers et al. 2022 lidar covered only the Cotoca and Landívar areas (atlas field guide).
- Evidence: one catalogued point inside the box (−14.283, −64.201) and 30 within 100 km. Forest loss totals 474 km², 231 km² of it in 2019–2024, concentrated in cells around −14.45, −64.25 (103 km² in one 0.1° cell) (Walker; Hansen).
- Orbital signature: ring ditches 100–300 m across, and Casarabe-style straight causeways and canals, several km long and about 5–10 m wide, in cleared ground and savanna. Sentinel-2 can see them; 30 m elevation data cannot.
- Biggest reason it could be wrong: savanna has no forest-loss signal, and Bolivian 2022–2024 loss may be fire.
- Looting-sensitive: yes.
- Confidence: 25.

### C8. M2 eastern Mojos frontier box (Beni / Santa Cruz) — NOVEL-SYNTHESIS
- Coordinates: −15.05, −63.45 (±35 km). Box N −14.8, S −15.3, W −63.7, E −63.2.
- Significance 5: **880 km² lost in 2022–2024 alone (29% of the box)**. Nearest catalogued points are −14.733, −63.524 (36 km) and −15.126, −63.806 (39 km).
- Biggest reason it could be wrong: the loss is probably burn scars rather than mechanised clearing. Check Sentinel-2: in bare ploughed fields ditches show well; in burned standing forest they barely show.
- Confidence: 15.

### C9. COP-DEM "giant-mound" anomaly in the Calakmul–Río Bec gap — NOVEL-SYNTHESIS (novelty UNCHECKED)
- Coordinates: 18.30194, −89.58750 (±1 km).
- Significance 4.
- Evidence chain:
  1. A top-hat filter on GLO-30 elevation (150 m disk) gives Calakmul 27.4 m at 18.10472, −89.81056, with a second peak of 24.8 m at 18.10306, −89.80833. La Danta at El Mirador gives 29.9 m at 17.75611, −89.92111, and Nakbé 31.3 m. Tikal gives 19–23 m. Becán and Naachtún, at 12–14 m, cannot be separated from noise. So **30 m elevation data reliably shows only pyramids taller than about 35 m**.
  2. After keeping only flat ground (background standard deviation <6 m), ≥97% tree cover and compact peaks (≤12 pixels, ≥22 m), 69 peaks remain across 17–20 N, −91 to −89 W (`data/T7/maya_cop_dem_forest_peaks.csv`).
  3. P3 has the most Calakmul-like profile: a compact peak +29 m above the 1.5 km 20th percentile, about 20 m above the plain right around it, on gentle terrain.
  4. Other peaks to check: 18.40667, −89.6725 (+33 m); 18.24556, −89.64111 (on a ridge, probably natural); 18.17639, −89.60806.
- Novelty check: **not performed** (search budget exhausted). It could well be a registered site, for example in the Hormiguero/Río Bec zone, or a karst hill.
- Orbital signature: a 3×3-pixel bump of about 20 m in GLO-30; invisible in Sentinel-2 under forest; lidar or a sub-metre canopy shadow needed.
- Looting-sensitive: yes.
- Confidence: 12.

### C10. M3 Beni south of Riberalta box — NOVEL-SYNTHESIS
- Coordinates: −12.05, −65.95 (±35 km). Box N −11.8, S −12.3, W −66.2, E −65.7.
- Significance 4: 552 km² lost in 2022–2024; nearest catalogued point −12.485, −65.554 (65 km); the Riberalta ring-ditch cluster (−11.10, −66.15) lies 90–100 km north.
- Biggest reason it could be wrong: fire-driven loss, and it is far from any anchor site.
- Confidence: 15.

## Dead ends
- WebFetch was blocked for every publisher (Cambridge, Nature, LiveScience, Factum and others), so the exact Valeriana coordinates and the Peripato probability map could not be read.
- The web-search budget (shared across teams) ran out after about 10 queries. Novelty checks in Rondônia and southern Amazonas and the Khmer site catalogues were **not done**.
- A COP-DEM peak scan of the Maya karst without a flatness filter gave 94,624 raw detections (46,793 after a stricter compactness threshold). Karst hills and forest remnants beside clearings swamp it, so the method only works on flat forested ground.
- Khmer outliers: **cannot resolve**. Hansen shows strong 2015–2024 clearing in northern Cambodia: 13.0–13.5 N, 104.5–105.0 E (666 km²); 13.5–14.0 N, 104.0–104.5 E (629 km²); 12.5–13.0 N, 105.5–106.0 E (1,072 km²). These lie near Preah Khan of Kompong Svay and Koh Ker, but I had no verifiable site catalogue or lidar footprint to separate known sites from gaps.
- The southern-Amazonas box south of Humaitá (−7.5 to −8.0, −63.7 to −63.2; 470 km² cleared recently) was dropped: it is 135 km from any known earthwork, and at 72–88 m elevation it falls outside the known environmental range.
- Pará boxes along the BR-163 (around −8.2 to −8.7, −55.0 to −54.5) were dropped: probable Indigenous-land and gold-mining clearing, and no nearby anchor sites.

## Sources
- Walker et al. 2023 data: https://github.com/RobertSWalker/ancient_amazonia_archaeology (PeerJ 11:e15137, https://peerj.com/articles/15137/)
- Hansen GFC v1.12: https://storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12/
- Pärssinen et al. 2026: https://www.natureasia.com/en/info/press-releases/detail/9397 ; https://archaeology.org/news/2026/07/31/hundreds-of-geoglyphs-discovered-in-amazon-rainforest/ ; atlas record https://github.com/tadad/amazonian-archaeology-atlas (vault/LiDAR Scans/2026-acre-amazonas-als-campaign.md)
- Colombian forest-carbon archive: atlas vault/LiDAR Scans/2011-colombia-ecological-als.md ; https://bg.copernicus.org/articles/9/2683/2012/
- Peripato et al. 2023: https://research-portal.uu.nl/en/publications/more-than-10000-pre-columbian-earthworks-are-still-hidden-through/ ; https://www.scribd.com/document/699527388/Science-ade2541-Sm ; https://www.eurekalert.org/news-releases/1003406
- de Souza et al. 2018: https://pmc.ncbi.nlm.nih.gov/articles/PMC5871619 ; https://news.mongabay.com/2018/04/new-study-discovers-81-lost-human-settlements-in-the-amazon-rainforest/
- Valeriana: https://hyperallergic.com/961787/ancient-maya-city-discovered-in-southeastern-mexico/ ; https://livescience.com/archaeology/lasers-reveal-maya-city-including-thousands-of-structures-hidden-in-mexico ; https://bigthink.com/strange-maps/lidar-finds-valeriana/
- G-LiHT: https://pure.psu.edu/en/publications/reanalyzing-environmental-lidar-data-for-archaeology-mesoamerican/ ; https://pure.psu.edu/en/publications/the-lowland-maya-settlement-landscape-environmental-lidar-and-eco/ ; https://scholar.uc.edu/collections/w9505239h?locale=en ; https://www.osti.gov/biblio/1582600 ; https://ngt-data.lbl.gov/dois/NGT0070/
- INEGI / Inomata 2021: https://par.nsf.gov/servlets/purl/10332671 ; https://www.sflorg.com/2021/11/laser-mapping-in-southern-mexico.html
- GEDI for Maya: https://github.com/JohMast/GEDI_Yucatan
- USGS 3DEP Puerto Rico: https://raw.githubusercontent.com/hobuinc/usgs-lidar/master/boundaries/resources.geojson
- Calibration: https://agencia.fapesp.br/un-estudio-con-geoglifos-indica-que-la-amazonia-tuvo-un-uso-sostenible/25020 ; https://revistapesquisa.fapesp.br/a-cultura-dos-geoglifos/ ; https://xronos.ch/sites/37619 ; https://whc.unesco.org/en/tentativelists/5999 ; https://en.wikipedia.org/wiki/Acre_geoglyphs
- Brazilian municipal seats (for place names): https://github.com/kelvins/municipios-brasileiros ; Copernicus GLO-30 elevation and ESA WorldCover 2021 (AWS S3)

```json
[
{"id":"T7-C1","name":"A1 North-of-Abunã geoglyph gap box (AM/AC/RO frontier)","lat":-9.25,"lon":-65.45,"radius_km":35,"feature_size_m":250,"signature":"Geometric ring/square ditches 100-350 m, ~11 m wide, greener line in dry-season pasture; box N-9.0 S-9.5 W-65.7 E-65.2","s2_visible":true,"dem_visible":false,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":45,"looting_sensitive":false,"category":"earthwork-gap","one_line":"700 km2 cleared 2019-24, zero catalogued earthworks, known cluster just west; outside 2026 lidar corridors"},
{"id":"T7-C2","name":"A3 Upper Tapajós / Paranaíta box (MT)","lat":-9.45,"lon":-56.95,"radius_km":35,"feature_size_m":200,"signature":"Ditched enclosures (circular/D-shaped) 100-300 m with sunken roads; box N-9.2 S-9.7 W-57.2 E-56.7","s2_visible":true,"dem_visible":false,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":40,"looting_sensitive":false,"category":"earthwork-gap","one_line":"Extension of de Souza 2018 fortified-village belt; 1341 km2 cleared, 0 catalogued, elevation in range"},
{"id":"T7-C3","name":"A2 Jaci-Paraná / Nova Mamoré box (RO)","lat":-9.85,"lon":-64.95,"radius_km":35,"feature_size_m":250,"signature":"Geometric ditches in pasture; box N-9.6 S-10.1 W-65.2 E-64.7","s2_visible":true,"dem_visible":false,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":40,"looting_sensitive":false,"category":"earthwork-gap","one_line":"63% cleared box between two known clusters with no catalogued earthworks"},
{"id":"T7-C4","name":"A6 Iñapari–Iberia tri-border box (PE/BO/BR)","lat":-11.45,"lon":-69.45,"radius_km":35,"feature_size_m":250,"signature":"Geometric ditches in pasture along the Interoceanic corridor; box N-11.2 S-11.7 W-69.7 E-69.2","s2_visible":true,"dem_visible":false,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":30,"looting_sensitive":false,"category":"earthwork-gap","one_line":"Political-border gap: Acre geoglyph plateau continues into Peru/Pando; 432 km2 cleared 2019-24"},
{"id":"T7-C5","name":"A4 RO–AM–MT tri-border box (Machadinho–Colniza)","lat":-9.25,"lon":-60.65,"radius_km":35,"feature_size_m":200,"signature":"Ditched enclosures in pasture; box N-9.0 S-9.5 W-60.9 E-60.4","s2_visible":true,"dem_visible":false,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":25,"looting_sensitive":false,"category":"earthwork-gap","one_line":"Bridges Madeira and NW-MT clusters; 454 km2 cleared 2019-24, nearest known 64 km"},
{"id":"T7-C6","name":"A5 north-of-Cujubim box (RO)","lat":-8.65,"lon":-62.65,"radius_km":35,"feature_size_m":200,"signature":"Ditched enclosures in fresh clearings; box N-8.4 S-8.9 W-62.9 E-62.4","s2_visible":true,"dem_visible":false,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":20,"looting_sensitive":false,"category":"earthwork-gap","one_line":"Largest 2019-24 clearing (942 km2) of any Brazilian box without known earthworks, but low terrain"},
{"id":"T7-C7","name":"M1 Baures–Casarabe gap box (Llanos de Mojos)","lat":-14.45,"lon":-64.25,"radius_km":35,"feature_size_m":300,"signature":"Ring ditches 100-300 m and km-long straight causeways/canals; box N-14.2 S-14.7 W-64.5 E-64.0","s2_visible":true,"dem_visible":false,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":25,"looting_sensitive":true,"category":"earthwork-gap","one_line":"Interstitial forest between Baures ring-ditch and Casarabe clusters, outside 2022 lidar"},
{"id":"T7-C8","name":"M2 eastern Mojos frontier box (Beni/Santa Cruz)","lat":-15.05,"lon":-63.45,"radius_km":35,"feature_size_m":250,"signature":"Ring ditches in mechanized clearings (check fire vs clearing); box N-14.8 S-15.3 W-63.7 E-63.2","s2_visible":true,"dem_visible":false,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":15,"looting_sensitive":true,"category":"earthwork-gap","one_line":"880 km2 forest loss 2022-24, nearest known earthworks 36-39 km"},
{"id":"T7-C9","name":"COP-DEM giant-mound anomaly P3, Calakmul–Río Bec gap","lat":18.30194,"lon":-89.5875,"radius_km":1,"feature_size_m":90,"signature":"Compact 3x3-px ~20 m bump in GLO-30 DSM under continuous forest, Calakmul-like profile","s2_visible":false,"dem_visible":true,"significance":4,"novelty":"NOVEL-SYNTHESIS","confidence":12,"looting_sensitive":true,"category":"maya-structure","one_line":"DSM top-hat calibrated on Calakmul/Mirador/Nakbé; novelty UNCHECKED, may be a registered site or karst hill"},
{"id":"T7-C10","name":"M3 Beni south of Riberalta box","lat":-12.05,"lon":-65.95,"radius_km":35,"feature_size_m":250,"signature":"Ring ditches in cleared/burned forest; box N-11.8 S-12.3 W-66.2 E-65.7","s2_visible":true,"dem_visible":false,"significance":4,"novelty":"NOVEL-SYNTHESIS","confidence":15,"looting_sensitive":true,"category":"earthwork-gap","one_line":"552 km2 loss 2022-24, 90-100 km south of Riberalta ring-ditch cluster"}
]
```
