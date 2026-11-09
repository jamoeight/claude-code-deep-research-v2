# T10 — Steppe and desert stone megastructures: survey gaps

## Method (what you joined, what you searched; 5-10 lines)
- About 45 WebSearch queries in English, Russian and French covering published distributions and survey extents for desert kites, mustatils, gates and wheels, Turgai/steppe geoglyphs, khirigsuurs, and Saharan keyhole and V-antenna monuments. **Limits:** WebFetch was refused for every scholarly host tried (wikipedia, reference-global, metajnl, PLOS). curl was refused for Zenodo, Mendeley, ResearchGate and HAL. The shared web-search budget ran out partway through the task. As a result, the actual distribution datasets (Globalkites on Zenodo, the Sparavigna keyhole KMLs on Mendeley) could **not** be downloaded. All literature evidence below comes from search-result abstracts and snippets, plus three open GitHub repos.
- Gap logic: (a) a survey edge that follows a *project or administrative* boundary or a dataset bounding box rather than a landscape boundary; (b) the same landform continues past that edge (basalt rim, plateau chink/escarpment, lake-terrace grassland); (c) at least one example of the type is already known beyond the core.
- I derived the landforms myself from Copernicus GLO-30 DEM (escarpment profiles), ESA WorldCover 2021 (grassland vs cropland vs water) and coarse 160 m Sentinel-2 L2A mosaics (dark basalt fraction). Scripts are in the scratchpad. PNG and NPY outputs are in `data/T10/`.
- **Imagery test:** at the Ushtogay Square and Turgay triradial coordinates, and at two published kite coordinates, the structures are **not resolvable** in 10 m S2 (`data/T10/cal_*.png`). The mounds are 6–12 m and kite walls are about 1 m wide. Every box below therefore needs Google Earth or Bing sub-metre imagery. S2 and the DEM are useful only for checking the landform.

## Calibration: known examples to look at in Google Earth
| ID | Type | Coordinates | Size | Source | S2 10 m? |
|---|---|---|---|---|---|
| K1 | Ushtogay Square, mound geoglyph (Turgai) | 50.832933, 65.326276 | ~274–287 m per side, 101 mounds | Wikipedia-derived coordinates in search results ([Steppe Geoglyphs](https://en.wikipedia.org/wiki/Steppe_Geoglyphs)); 287 m and 101 mounds ([Kazinform](https://www.inform.kz/ru/uchenye-obnaruzhili-na-territorii-kazahstana-beloe-pyatno_a2275126)) | Marginal or no (checked Sep 2023 and May 2023 scenes) |
| K2 | Turgay triradial ("swastika") | 50.102778, 65.360833 | ~100 m (about 800 m from Urpek) | [Steppe Geoglyphs](https://en.wikipedia.org/wiki/Steppe_Geoglyphs); Kazinform reports a 104 m triradial | No |
| K3 | Desert kite, Harrat al-Harrah (Saudi part of Harrat ash-Sham) | 31.483472, 38.368028 | hundreds of m | Example coordinates hard-coded in the open kite-detector app [eyepop-ai/SDSUDesertKites](https://github.com/eyepop-ai/SDSUDesertKites) (app.py l.756). **Not independently verified.** | No (S2 chip noisy) |
| K4 | Desert kites, Khaybar | 25.742162, 39.292586 and 25.867377, 39.240912 | hundreds of m | same repo (app.py l.746, 751). Khaybar holds about 917 kites ([aawsat](https://english.aawsat.com/home/article/1088441/close-mysteries-made-stone-saudi-arabia%E2%80%99s-desert?page=4)). **Unverified** | No |
| K5 | "Kostanay Tetragon", trapezoid of mound geoglyphs | ≈53.20, 63.68 (±3 km) | not given | Dey, reported in the press: 1.9 km from Zatobolsk along the M36, about 10 km from Kostanay ([Kazinform](https://www.inform.kz/ru/sensacionnaya-nahodka-otkryt-geoglif-kostanayskiy-tetragon_a2965579), [Informburo](https://informburo.kz/novosti/geoglif-vnushitelnyh-razmerov-sluchayno-obnaruzhen-v-stepi-kostanaya.html)). The Zatobolsk position is from my background knowledge, so treat it as approximate. | No |
| K6 | Zuratkul "Elk", stone-strip geoglyph (Chelyabinsk, Russia) | not obtained | 218 × 195 m, strips 3–5 m | [znanierussia](https://znanierussia.ru/articles/%D0%9B%D0%BE%D1%81%D1%8C_(%D0%B3%D0%B5%D0%BE%D0%B3%D0%BB%D0%B8%D1%84)) | maybe |

**Types still missing precise calibration coordinates** (search budget exhausted). Search windows that are sourced:
- **Gates:** "almost all in or just north of Harrat Khaybar", 13–518 m long ([Arab News](https://www.arabnews.pk/node/1181146), [Live Science](https://www.livescience.com/60698-mysterious-stone-structures-discovered-saudi-arabia.html)).
- **Mustatils:** densest in AlUla and Khaybar counties, up to about 600 m long ([Thomas et al. 2021](https://cambridge.org/core/services/aop-cambridge-core/content/view/S0003598X2100051X)).
- **Wheels:** Wisad Pools in Jordan's Black Desert; diameters 25–70 m ([cyberleninka](https://cyberleninka.ru/article/n/desert-kites-and-stone-circles-of-the-syrian-desert-in-satellite-images)).
- **Big Circles:** Jordan, about 400 m across ([Archaeology](https://archaeology.org/news/2014/10/31/141031-big-circle-aerial-photographs/)).
- **Khirigsuur:** Urt Bulagyn in the Khanuy valley, Mongolia ([Bonn](https://www.for5438.uni-bonn.de/research/locations)).
- **Keyhole monuments:** Aïr and Ténéré in Niger, Ahaggar, Tassili, Messak ([Gauthier 2008b](https://ressources.ingall-niger.org/documents/livres/lectures/Gauthier-2008b-aars12-MO.pdf)).

## Distribution facts used (each seen in search results)
- **Kites:** 6,721 identified as of 1 Nov 2024, mainly on Bing imagery ([JOAD data paper](https://openarchaeologydata.metajnl.com/articles/150/files/67c039e4a1a44.pdf)). The Globalkites range runs "from the Aralo-Caspian zone to central-western Arabia" (Bouzid & Barge 2022 abstract, read from [mathias-bellat/ML_archaeology_review](https://github.com/mathias-bellat/ML_archaeology_review) `data/Metadata.csv`). So **North Africa sits outside the systematic Globalkites survey**.
- **Dataset edge:** a search-result summary of the dataset gives an eastern boundary value of **65.996°E** (low certainty, snippet only). A Ustyurt paper says kites run west to the Caspian shore and "almost 1000 km eastward until the Sarysu River basin" ([ResearchGate](https://www.researchgate.net/publication/280446641_The_'desert_kites'_of_the_Ustyurt_plateau)).
- **Aralo-Caspian:** holds one ninth of all kites; 143 were recorded on the SW Ustyurt ([HAL](https://hal.archives-ouvertes.fr/hal-01224967)). The "arans" sit mainly along the cliffs of the Ustyurt and Mangyshlak ([UNESCO TL 6571](https://whc.unesco.org/en/tentativelists/6571)). Kites follow saiga routes ([Saiga RC](https://saigaresourcecentre.com/node/2358)).
- **Libya:** at least 330 kite-like structures on and around the Hamada al-Hamra ([Antiquity 2018](https://www.cambridge.org/core/product/63DC3D3D72A3BA696AA09904C4F06B85)), plus a second set in Tripolitania ([Antiquity 2019](https://core-prod.cambridgecore.org/core/services/aop-cambridge-core/content/view/747A1B038737B0BAA222B61D116401C7/S0003598X19001546a.pdf/desert-kites-in-the-tripolitania-region-new-evidence-from-satellite-imagery.pdf)). Yemeni kites lie between Ma'rib and Sirwah (Brunner 2008; Skorupka 2010, cited ibid.).
- **Arabia:** more than 300 kites, about 500 km further south than previously thought ([Groucutt & Carleton 2021](https://www.sciencedirect.com/science/article/pii/S2352409X21002078)). Kites are also known on Harrat Rahat, Harrat Kishb, at Tabuk and in the Nafud ([aawsat](https://english.aawsat.com/home/article/1088441/close-mysteries-made-stone-saudi-arabia%E2%80%99s-desert?page=4) / [Esquire ME](https://www.esquireme.com/culture/the-mystery-of-the-desert-kites-in-the-saudi-wilderness)), and on Harrat Nawasif east of Turbah ([Popular Archaeology](https://popular-archaeology.com/article/massive-late-neolithic-animal-traps-in-arabia-have-archaeologists-mobilized/)). The RCU found 207 new kites in AlUla ([RCU](https://www.rcu.gov.sa/en/media-gallery/news/kites/)). Jordan has at least 550 ([Jordan Times](https://jordantimes.com/news/local/how-satellite-images-are-transforming-our-understanding-desert-kites-jordan)).
- **Mustatils:**
  - 1,072 identified, 276 photographed from the air, 39 surveyed on the ground ([sciencythoughts summary of Thomas et al.](https://sciencythoughts.blogspot.com/2021/07/interpretting-neolithic-mustatils-of.html)). The same summary notes that similar rectangles occur in southern Jordan, relationship unclear.
  - About 1,600 identified by satellite ([Arab News](https://www.arabnews.pk/node/2141631/saudi-arabia)).
  - 104 in the southern Nefud between Ha'il and Tayma ([Groucutt 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7575307)).
  - 169 in Ha'il; their locations are predicted by water proximity, east-facing slopes and nearby rocky outcrops ([Arab News](https://www.arabnews.pk/node/2572047/art-culture)). Hatton's study-area code is in [amyhatton/mustatils_spatial_analysis_redo](https://github.com/amyhatton/mustatils_spatial_analysis_redo).
  - Survey programmes are organised by county (AAKSAU covers AlUla, AAKSAK covers Khaybar) or by the Nefud margin.
- **Turgai geoglyphs:**
  - About 260 known (Dey) ([CSM](https://www.csmonitor.com/Science/2015/1115/What-s-with-those-mysterious-shapes-NASA-photographed-in-Kazakhstan)), 90–400 m across ([Live Science](https://livescience.com/47954-geoglyphs-discovered-in-kazakhstan.html)).
  - Built from mounds 6–12 m wide in soft chernozem; the Turgai, Ubagan and Tobol all run through the same trough ([Tengrinews](https://tengrinews.kz/my-country/zagadki-turgaiskix-geoglifov-369134/), [Tengrinews 2](https://tengrinews.kz/my-country/zagadochnyie-geoglifyi-turgaya-pochemu-dolinu-severe-402027/)).
- **Saharan monuments:**
  - The Gauthiers have registered 6–7k monuments ([CAC2008](https://meetings.iac.es/cac2008/pages/view_abstractc75f.html?aid=95)).
  - The ranges of keyhole and V-antenna types are delimited, and some types run "from the Atlantic to the eastern edge of the Ténéré in Niger" ([Gauthier 2008b](https://ressources.ingall-niger.org/documents/livres/lectures/Gauthier-2008b-aars12-MO.pdf)).
  - Keyhole KMLs exist ([Mendeley](https://data.mendeley.com/datasets/gjgj4hzpgc/2)) but could not be downloaded.
  - I found no Chad or Sudan keyhole record.

## Candidates (ranked): survey-gap boxes and hints

### C1. Western rim of Jebel as-Sawda basalt, next to the Hamada al-Hamra kites (Libya) — NOVEL-SYNTHESIS
- Coordinates: 28.90, 15.15 (±17 km). **Box 28.75–29.05 N, 15.00–15.30 E**
- What / why (significance 6): desert kites on a basalt rim contiguous with the only known North African kite field.
- Evidence chain:
  1. At least 330 kites "on and around" the Hamada al-Hamra, and a second set in Tripolitania (Antiquity 2018/2019).
  2. Globalkites stops at "central-western Arabia" (Bouzid & Barge 2022), so no systematic survey covers Libya.
  3. Levantine kites concentrate on basalt-harra rims (at least 550 on the Jordanian Harrat; Jordan Times).
  4. My S2 mosaic (`data/T10/libya_sawda.png`) shows the red hamada surface running east to about 15.0°E and abutting a dark lava plateau at 28.65–29.15 N, 15.0–16.0 E. I am identifying that plateau as Jebel as-Sawda from background knowledge.
  5. I scanned 0.3° windows along the edge; this box is a rim box, with 26% of pixels below TCI brightness 150 against 0% on the reference hamada.
- Novelty check: no search hit on kites at Jebel as-Sawda. I could not read the full 2018 paper, so "around the plateau" may already include it.
- Orbital signature: walls 300 m–2 km long, about 1 m wide, converging antennae; Libyan kites lack the apex enclosure. Sub-metre imagery needed; not visible in S2 or DEM.
- Biggest reason it could be wrong: the Italian team may already have scanned it, or the Libyan kites may be tied to hamada limestone rather than basalt.
- Confidence: 30

### C2. Ubagan-valley grassland and lake chain, between the Turgai core and the Kostanay Tetragon (Kazakhstan) — NOVEL-SYNTHESIS
- Coordinates: 51.70, 64.50 (±17 km). **Box 51.55–51.85 N, 64.35–64.65 E**
- What / why (significance 6): Turgai-type mound geoglyphs (squares, rings, crosses, lines) on the northern half of the same trough.
- Evidence chain:
  1. About 260 geoglyphs are known, concentrated in the Turgai core (Amangeldy area).
  2. The Turgai, Ubagan and Tobol share one trough with lake chains (Tengrinews).
  3. The Kostanay Tetragon, found by chance about 300 km north (K5), shows the type exists outside the core.
  4. In WorldCover (`data/T10/turgai_worldcover.png`), this box is 81% grassland, 2% cropland and 14% water or wetland. That matches the Ushtogay reference window (81% grassland), so unplowed steppe should preserve the mounds. The boxes further north (51.85–52.45 N) are 20–35% cropland.
- Novelty check: no search hit for geoglyphs in the Ubagan valley; Dey's survey extent is unpublished.
- Orbital signature: figures 90–400 m made of mounds 6–12 m wide, showing as faint tonal dots or crop/soil marks. Google Earth needed; not visible in S2 (tested at K1 and K2).
- Biggest reason it could be wrong: Dey, who lives in Kostanay, has probably already browsed the whole trough.
- Confidence: 25

### C3. Western escarpment of the Betpak-Dala plateau, east of the known kite limit (Kazakhstan) — NOVEL-SYNTHESIS
- Coordinates: 45.70, 67.45 (±17 km). **Box 45.55–45.85 N, 67.30–67.60 E**
- What / why (significance 7): it would extend the Central Asian kite range by about 100 km east, into a second saiga range.
- Evidence chain:
  1. Kites reportedly reach the Sarysu basin (ResearchGate Ustyurt paper).
  2. The dataset's east edge is about 66.0°E (snippet).
  3. Ustyurt kites sit on chink cliffs along saiga routes (UNESCO, Saiga RC).
  4. My DEM profiles show a chink-like scarp: 154→240 m between 67.3 and 67.4°E at 45.6°N, and 165→239 m between 67.6 and 67.7°E at 45.8°N. Spurs and re-entrants are visible in `data/T10/betpakdala_scarp_dem.png`.
  5. From my derivation, 67.45°E is about 1.45° × 78 km ≈ 113 km east of 66.0°E.
- Novelty check: searches in English and Russian ("араны Бетпак-Дала", "Sarysu kites") returned nothing.
- Orbital signature: V- or arrow-shaped walls 0.5–2 km long ending at the scarp edge. Sub-metre imagery needed. The scarp itself is visible in the DEM.
- Biggest reason it could be wrong: the 65.996°E edge may be real, if the Betpak-Dala saiga routes did not cross scarps.
- Confidence: 20

### C4. Older lava surfaces of Harrat Kishb (Saudi Arabia) — PROPOSED (kites already reported; box new)
- Coordinates: 23.20, 41.50 (±17 km). **Box 23.05–23.35 N, 41.35–41.65 E**
- What / why (significance 5): pendants, wheels and possibly gates on a southern harrat, compared with the gate core at Khaybar.
- Evidence chain:
  1. Gates are "almost all in or just north of Harrat Khaybar" (Arab News 2017). Kennedy calls the harrats from Syria to Yemen "especially rich".
  2. Kites are already reported on Kishb and Rahat (aawsat / Esquire ME).
  3. My S2 mosaic (`data/T10/harrats_rahat_kishb.png`) places Kishb at about 22.65–23.5 N, 41.0–41.75 E. The two very dark young flows (about 23.15–23.35 N, 41.08–41.28 E and 22.8–22.96 N, 41.14–41.40 E) are excluded. The box covers brown, weathered older flows of the kind that carry the Khaybar gates.
- Novelty check: no search hit for gates, wheels or pendants on Harrat Kishb.
- Orbital signature: wheels 25–70 m, pendants and tails 50–200 m, gates 13–518 m. Sub-metre imagery needed.
- Biggest reason it could be wrong: amateur explorers (the "Desert Team") may already have browsed it, and the gate concentration at Khaybar may be real.
- Confidence: 30 for any pendant or wheel; 10 for a gate
- looting_sensitive: true (pendant tombs)

### C5. Western Tibesti piedmont near Wour (Chad) — NOVEL-SYNTHESIS
- Coordinates: 21.35, 15.90 (±17 km). **Box 21.20–21.50 N, 15.75–16.05 E**
- What / why (significance 5): keyhole and V-antenna monuments east of their published limit at the eastern edge of the Ténéré.
- Evidence chain:
  1. Gauthier 2008b says the ranges of these types are delimited and that pan-Saharan types reach the "eastern edge of the Ténéré".
  2. A Collège de France corpus covers stone monuments "from Niger to Chad" without types.
  3. In my S2 mosaic (`data/T10/chad_tibesti_west.png`), the massif front runs at about 15.8–16.0 E. Tarso Toussidé at about 21.05 N, 16.45 E confirms the georeferencing. Wadis leave the massif onto sandstone pediments here, the setting where Aïr and Tassili monuments cluster (analogy).
- Novelty check: no Chad keyhole record found.
- Orbital signature: keyholes and V-antennas 10–60 m, dark stone on pale ground. Sub-metre imagery needed.
- Biggest reason it could be wrong: the published limit may be real, since types are regionally restricted.
- Confidence: 25 for keyhole or V types; above 60 that some unrecorded tumulus would appear
- Notes: looting_sensitive true. The Tibesti has war-era minefields, so this is remote-only.

### C6. Hisma basin north-west of Tabuk (Saudi Arabia) — NOVEL-SYNTHESIS
- Coordinates: 29.30, 35.75 (±17 km). **Box 29.15–29.45 N, 35.60–35.90 E**
- What / why (significance 6): mustatils in the corridor between the AlUla/Tayma core and the similar rectangles reported in southern Jordan.
- Evidence chain:
  1. Survey projects follow county or Nefud boundaries (AAKSAU, AAKSAK, Groucutt/Hatton), and none is Tabuk-based.
  2. Similar rectangles are reported in southern Jordan (sciencythoughts).
  3. Hatton's predictors are water, rocky outcrops and east-facing slopes.
  4. My S2 mosaic (`data/T10/hisma_tabuk.png`) shows sandstone inselbergs cut by dendritic wadis here, away from the Tabuk centre-pivot farms at about 28.3–28.6 N, 36.4–36.9 E.
- Novelty check: no search hit on mustatils at Hisma or Tabuk. The "200,000 km²" extent in Thomas et al. may already include it.
- Orbital signature: two parallel walls 20–600 m long with end platforms. Possibly faint lines in S2; sub-metre imagery preferred.
- Biggest reason it could be wrong: Kennedy's Google Earth surveys may already have covered it.
- Confidence: 15
- looting_sensitive: true

### C7. Atyrau region "geoglyphs" (Kazakhstan) — PROPOSED (reported, unstudied)
- Coordinates: 47.10, 51.90 (±250 km). Region centroid only; no coordinates were published.
- What / why (significance 4): Kazinform reports several large geoglyphs in Atyrau oblast, visible only from the air and never systematically studied. One figure is described as edged by a 6 m-wide track ([Kazinform](https://www.inform.kz/ru/geoglifi-obnaruzhennie-v-atirauskoy-oblasti-eshe-ne-izucheni-5355c3)).
- Novelty check: this is the only source found.
- **Warning:** the "geoglyphs" at Airakty-Shomanai in neighbouring Mangystau were made in 2017 for tourism, according to the same search summary. Treat these as possibly modern until shown otherwise.
- Orbital signature: unknown; "large".
- Biggest reason it could be wrong: modern or Soviet-era features.
- Confidence: 15

### C8. "Arans" of Zangezur (Armenia–Nakhchivan uplands) — PROPOSED (amateur posts)
- Coordinates: 39.50, 46.00 (±40 km). Approximate Syunik/Zangezur upland; no coordinates were given.
- What / why (significance 4): amateur essays describe Turkic-named stone game corrals ("arans", "goshundashi") in Zangezur ([proza.ru 1](https://proza.ru/2022/10/15/820), [proza.ru 2](https://proza.ru/2023/03/07/304)). Armenia is inside Globalkites, but the Nakhchivan side may not be.
- Note: a militarised border region. Do not target border installations.
- Confidence: 15

## Dead ends (1 line each)
- **Iran and Afghanistan kites:** 4 searches found no published kite; this cannot be resolved without the Globalkites dataset. No box proposed. Iran's NW basalt next to the Armenian kites is the only plausible lead.
- **Yemen kite gap** (between about 21.5 N Nawasif and about 15.5 N Ma'rib–Sirwah): left out on ethics grounds, because it is an active Saudi–Yemen/Houthi front.
- **Sudan** (Wadi Howar, Darfur): left out because of the active war; no distribution data was obtained either.
- **Mongolian khirigsuurs:** there are tens of thousands and no complete inventory, so a new one is near-certain anywhere and of low significance. Not a meaningful gap.
- **Turkmen Ustyurt (Kaplankyr chink):** plausible, but I had no evidence about whether Globalkites covered it; not boxed.
- Hatton's mustatil R workspace (.RDataTmp, about 3 GB uncompressed) could not be parsed without R.
- GitHub code search found no public kite, mustatil or khirigsuur coordinate datasets.
- S2 10 m cannot resolve the Turgai mounds or kite walls (tested); sub-metre imagery is mandatory.
- Turgai count conflict: about 260 (Dey) versus 73 in the state protection list. These are probably different selections.

## Sources
All URLs are cited inline above. Search-result summaries only; WebFetch was blocked. GitHub repos cloned to `data/T10/repos/`. Imagery and DEM products are in `data/T10/` (libya_sawda, turgai_worldcover, betpakdala_scarp_dem, harrats_rahat_kishb, chad_tibesti_west, hisma_tabuk, cal_*).

```json
[
{"id":"T10-C1","name":"Jebel as-Sawda W rim kites gap (Libya)","lat":28.90,"lon":15.15,"radius_km":17,"feature_size_m":1000,"signature":"converging 1 m stone walls 0.3-2 km on basalt/hamada rim","s2_visible":false,"dem_visible":false,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":30,"looting_sensitive":true,"category":"desert kite survey gap","one_line":"Box 28.75-29.05N 15.00-15.30E: basalt rim contiguous with the 330+ Hamada al-Hamra kites, outside Globalkites coverage"},
{"id":"T10-C2","name":"Ubagan valley grassland lake chain (Turgai-type geoglyphs)","lat":51.70,"lon":64.50,"radius_km":17,"feature_size_m":250,"signature":"squares/rings/crosses/lines of 6-12 m mounds on unplowed steppe","s2_visible":false,"dem_visible":false,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":25,"looting_sensitive":false,"category":"steppe geoglyph survey gap","one_line":"Box 51.55-51.85N 64.35-64.65E: 81% grassland lake terraces between the Turgai core and the Kostanay Tetragon"},
{"id":"T10-C3","name":"Betpak-Dala W escarpment kites (Kazakhstan)","lat":45.70,"lon":67.45,"radius_km":17,"feature_size_m":1000,"signature":"arrow/V stone walls ending at ~80 m chink scarp","s2_visible":false,"dem_visible":false,"significance":7,"novelty":"NOVEL-SYNTHESIS","confidence":20,"looting_sensitive":false,"category":"desert kite survey gap","one_line":"Box 45.55-45.85N 67.30-67.60E: chink-like scarp ~110 km east of the dataset's 66.0E kite limit"},
{"id":"T10-C4","name":"Harrat Kishb older flows: pendants/wheels/gates","lat":23.20,"lon":41.50,"radius_km":17,"feature_size_m":200,"signature":"wheels 25-70 m, pendants, possible gates up to 518 m on weathered basalt","s2_visible":false,"dem_visible":false,"significance":5,"novelty":"PROPOSED","confidence":30,"looting_sensitive":true,"category":"harrat structures survey gap","one_line":"Box 23.05-23.35N 41.35-41.65E: southern harrat with kites reported but no gate/wheel record found"},
{"id":"T10-C5","name":"W Tibesti piedmont near Wour: keyhole/V-antenna monuments","lat":21.35,"lon":15.90,"radius_km":17,"feature_size_m":40,"signature":"dark-stone keyhole/V-antenna tumuli 10-60 m on wadi terraces","s2_visible":false,"dem_visible":false,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":25,"looting_sensitive":true,"category":"Saharan monument survey gap","one_line":"Box 21.20-21.50N 15.75-16.05E: just east of the published 'eastern Tenere' limit of the monument types"},
{"id":"T10-C6","name":"Hisma basin NW of Tabuk: mustatils","lat":29.30,"lon":35.75,"radius_km":17,"feature_size_m":300,"signature":"paired parallel walls 20-600 m with end platforms near sandstone outcrops","s2_visible":false,"dem_visible":false,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":15,"looting_sensitive":true,"category":"mustatil survey gap","one_line":"Box 29.15-29.45N 35.60-35.90E: corridor between the AlUla/Tayma core and the southern Jordan rectangles"},
{"id":"T10-C7","name":"Atyrau oblast unstudied geoglyphs","lat":47.10,"lon":51.90,"radius_km":250,"feature_size_m":200,"signature":"unknown large figures; one edged by a 6 m track","s2_visible":false,"dem_visible":false,"significance":4,"novelty":"PROPOSED","confidence":15,"looting_sensitive":false,"category":"hint","one_line":"Kazinform report of several large, never-studied geoglyphs; beware modern fakes as in Mangystau"},
{"id":"T10-C8","name":"Zangezur 'arans' (game corrals)","lat":39.50,"lon":46.00,"radius_km":40,"feature_size_m":500,"signature":"stone drive walls/corrals on upland basalt","s2_visible":false,"dem_visible":false,"significance":4,"novelty":"PROPOSED","confidence":15,"looting_sensitive":false,"category":"hint","one_line":"Amateur proza.ru essays describe kites in Zangezur; Nakhchivan side possibly unsurveyed; border zone"},
{"id":"T10-K1","name":"Ushtogay Square (calibration)","lat":50.832933,"lon":65.326276,"radius_km":0.3,"feature_size_m":280,"signature":"square of 101 mounds with diagonals","s2_visible":false,"dem_visible":false,"significance":8,"novelty":"KNOWN","confidence":95,"looting_sensitive":false,"category":"calibration","one_line":"Largest Turgai geoglyph"},
{"id":"T10-K2","name":"Turgay triradial (calibration)","lat":50.102778,"lon":65.360833,"radius_km":0.3,"feature_size_m":100,"signature":"three-armed mound swastika","s2_visible":false,"dem_visible":false,"significance":7,"novelty":"KNOWN","confidence":90,"looting_sensitive":false,"category":"calibration","one_line":"About 800 m from Urpek"},
{"id":"T10-K3","name":"Kite, Harrat al-Harrah (calibration, unverified)","lat":31.483472,"lon":38.368028,"radius_km":1,"feature_size_m":500,"signature":"kite walls on basalt","s2_visible":false,"dem_visible":false,"significance":5,"novelty":"KNOWN","confidence":60,"looting_sensitive":false,"category":"calibration","one_line":"Example coordinates from an open kite-detection app"},
{"id":"T10-K4","name":"Kite, Khaybar (calibration, unverified)","lat":25.867377,"lon":39.240912,"radius_km":1,"feature_size_m":500,"signature":"kite walls on basalt","s2_visible":false,"dem_visible":false,"significance":5,"novelty":"KNOWN","confidence":55,"looting_sensitive":false,"category":"calibration","one_line":"Second app example; also 25.742162,39.292586"},
{"id":"T10-K5","name":"Kostanay Tetragon (calibration, approx)","lat":53.20,"lon":63.68,"radius_km":3,"feature_size_m":200,"signature":"trapezoid of eroded mounds in chernozem","s2_visible":false,"dem_visible":false,"significance":5,"novelty":"KNOWN","confidence":50,"looting_sensitive":false,"category":"calibration","one_line":"Dey, reported in press: 1.9 km from Zatobolsk along the M36"}
]
```
