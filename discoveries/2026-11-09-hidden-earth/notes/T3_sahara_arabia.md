# T3 — Sahara and Arabia: lost oases, lost armies, lost meteorites, lost towns

> **Operating conditions (read first).** WebFetch could not reach arxiv.org or most other hosts in this session. The shared WebSearch budget ran out early, after about 9 searches by this team. As a result:
> (a) Most evidence here comes from my own Copernicus DEM analysis, which is reproducible from `data/T3/`, and from the full text of Warren et al. 2024. I obtained that paper as a PDF from the public arXiv bulk-data bucket on GCS.
> (b) Where I use background knowledge that I could not re-source this session, I tag it **[BK-unverified]**. The lead should verify these claims or remove them.
> (c) Arabia and the trans-Saharan caravan towns could not be researched to the brief's standard. They are listed under *Cannot resolve*, not as candidates.

## Method (what was joined, what was searched)
1. **Chinguetti.** I read Warren, Warren & Protopapa (arXiv:2402.14150, Feb 2024) in full. It is the "route-reconstruction" paper. It is from 2024, not 2021, and it reconstructs **dunes**, not mesas. I then reproduced its high-dune mask on **Copernicus GLO-30**. A pixel is flagged if it stands at least 40 m above any pixel within 800 m to its west, which is their algorithm. I labelled every dune patch in the 10–50 km annulus around Chinguetti and extracted per-dune western-edge coordinates (`data/T3/chinguetti_dune_patches.json`, `chinguetti_highdunes.png`, `zoom_batraz.png`, `zoom_NE.png`). I then joined three things: the per-dune targets, the paper's own constraints (≤50 km straight line, ≥10 km, the eastern Les Boucles already magnetically cleared), and the Linarès blacksmith testimony quoted in that paper.
2. **Zerzura.** From search results I took Wilkinson's directional clue: "five days West of the Farafra–Bahariya track". I turned it into a distance band of 125–220 km at 25–40 km per camel-day. I then ran a closed-depression (fill-difference) search on GLO-90 over the Western Desert (`wd_*`, `westerndesert.png`). For the Gilf Kebir I ran D8 flow accumulation (pysheds) on GLO-90 and ranked wadi catchments (`gilf_wadis.png`).
3. **Cambyses.** I computed great-circle and multi-leg route geometry from Kharga to Siwa (pyproj) against GLO-90 terrain.
4. **Saharan paleolakes.** I ran closed-basin and inflow-channel analysis on GLO-90 over the Ahnet region, 24–28°N, 0–4°E (`ahnet_overview.png`, `ahnet_lowlands.png`).
5. **Nefud.** I ran a flat-floored interdune basin screen on GLO-90 (`nefud_overview.png`). The result was inconclusive; see Dead ends.

## Candidates (ranked)

### C1. Chinguetti "iron hill": unsurveyed SW/S Les Boucles megadune fronts — PROPOSED (area, Warren et al. 2024); per-dune targets are new
- **Coordinates:** 20.360, -12.440 (±6 km). The individual targets are listed below.
- **What it would be / why it matters (significance 9/10 if real):** Ripert described an iron mass 40 m high and 100 m long. That would be the largest meteorite on Earth by orders of magnitude, and it would vindicate his 1916 account. The prior probability is low (see "Biggest reason").
- **Evidence chain:**
  1. Ripert said the mass was "nearly covered by sand" in 1916, with a large dune on its NE side. He first said the direction was **SW**, then corrected it to **SE**. The trip was about 10 h at night without a compass. Early searches were visual only. Warren et al. set an upper limit of 50 km and a lower limit of 10 km on the straight-line distance. https://arxiv.org/abs/2402.14150 (full text read via the arXiv GCS bulk-data copy).
  2. The dunes migrate SW at ≤1 m/yr (SRTM vs ALOS). So the front of the mass should now sit about 100 m NE of the western (lee) foot of a dune that is >30–40 m high, at most about 500 m in from the dune foot (same source).
  3. Their December 2022 foot magnetometer survey of the **eastern** Les Boucles (six dunes, readings every ~50 m) found a range of only 46 nT. They say this definitively excludes that area. They recommend surveying the remaining annulus dunes ("green areas") (same source).
  4. My GLO-30 reproduction shows that the unsurveyed Les Boucles dunes above 40 m lie mainly in a **SW lobe at bearings 195–230° and 11–18 km**. This fits Ripert's *original* "SW" statement. A secondary group lies due S/SSE at 10–13 km. The largest patches, with western-edge midpoints (the survey walk line), are:
     - LB-SW1: centroid 20.3480, -12.4533; 112 ha above 40 m; maximum relief 62 m; 15.8 km at 216°. W-edge 20.3471, -12.4549.
     - LB-SW2: 20.3808, -12.4211; 90 ha; 63 m; 10.9 km at 213°. W-edge 20.3804, -12.4238.
     - LB-SW3: 20.3452, -12.4351; 71 ha; 59 m; 15.1 km at 210°. W-edge 20.3451, -12.4374.
     - LB-SW4: 20.3636, -12.4791; 70 ha; 59 m; 16.4 km at 228°. W-edge 20.3640, -12.4824.
     - LB-SW5: 20.3656, -12.4098; 66 ha; 60 m; 11.9 km at 204°. W-edge 20.3654, -12.4110.
     - LB-S1: 20.3907, -12.2857; 30 ha; 58 m; 11.4 km at 135°. This one may fall inside Warren's surveyed area; I inferred that area's boundary as lon > -12.27 because their Fig. 1 could not be read.
  5. Magnetic detectability (my derivation). Treat the mass as a demagnetisation-limited sphere with J ≈ 3B₀/μ₀ ≈ 79 A/m, assuming B₀ ≈ 33,000 nT **[BK-unverified IGRF value]**. A mass equivalent to 100×40×40 m (D ≈ 67 m) then gives about 1,300–2,500 nT at 100 m and 80–160 nT at 250 m. The 2004 PRISM-I survey was flown at 100 m height with 500 m line spacing, so it would detect it unambiguously. Warren et al. say the data exist in the "Chinguetti 2012" block but have not been released to them.
- **Novelty check:** I searched for the arXiv paper, its coverage (phys.org, sciencythoughts, ScienceAlert) and the Monod history. Warren et al. already map these dunes as recommended "green areas". A per-dune target list with coordinates does not appear in what I saw. Label: PROPOSED (area).
- **Orbital signature:** If the mass is buried, which is the hypothesis, it is invisible to optical and DEM sensors. The decisive test is the PRISM-I aeromagnetic grid or a ground walk along the listed W-edges. If any part is exposed, it would be a dark, varnished or rusty mass about 100×40 m on the SW (lee) foot of a pale dune. That is about 10×4 pixels in **Sentinel-2 (visible)** and 3×1 pixels in GLO-30 (marginal). The lead's S2 check should look for dark blocks at the listed W-edges. Warren notes that dark blocky shale diapirs in the area are the known false positive; Gallouédec's 1990s aerial "sighting" was probably one of these.
- **Biggest reason it could be wrong:** Welten et al. (2001) found from radionuclides that the 4.5 kg mesosiderite came from a parent body ≤1.6 m across. Monod concluded in 1989 that Ripert's hill was the sedimentary butte **guelb Aouinet**, with no metal. Zanda doubted that identification. Sources: https://en.wikipedia.org/wiki/Chinguetti_meteorite, https://meteoritestheblog.com/2014/07/25/the-first-post/, https://www.lyellcollection.org/doi/full/10.1144/SP287.16
- **Confidence:** 4

### C2. Chinguetti: NW fringe of the Batraz megadune field — PROPOSED (area); the distance-convergence argument is a NOVEL-SYNTHESIS
- **Coordinates:** 20.190, -12.005 (±4 km)
- **What / why (sig 9):** This is the same object as C1. Here the hypothesis is that the guide took the fast former riverbed "Taiaret Idaouali" south-east to the edge of the Batraz high dunes.
- **Evidence chain:**
  1. Batraz is the only other area of dunes >40 m within reach. Warren et al. place it 40–60 km SE and call reaching it overnight "rather unlikely but cannot be ruled out". https://arxiv.org/abs/2402.14150
  2. Three constraints converge here and nowhere else:
     - Ripert's *corrected* direction was **SE**.
     - In 1934 Captain Linarès reported a blacksmith's account of an iron block "roughly half way between Chinguetti and Ouadane". My computed Chinguetti–Ouadane distance is 92.7 km (Ouadane at 20.929, -11.624 **[BK-unverified gazetteer]**), so half-way is about **46 km**. The account is quoted in Warren et al.
     - The mass needs dunes ≥40 m, and the hard limit is ≤50 km.

     Only the NW Batraz dunes satisfy SE + 46–50 km + ≥40 m together.
  3. GLO-30 targets (all dunes; I checked their shapes on the hillshade):
     - B1: centroid 20.1898, -12.0005; 80 ha above 40 m; maximum relief 61 m; 48.5 km at 129°. W-edge runs 20.1829–20.1974 along lon ≈ -12.0024.
     - B3: 20.1912, -12.0224; 18.6 ha; 50 m; 46.6 km at 130°. W-edge 20.1915, -12.0246.
     - B4: 20.1963, -11.9776; 36 ha; 53 m; 50.0 km at 126°. W-edge 20.1962, -11.9793.
     - Smaller SW patches at 20.12–20.16, -12.09 to -12.11 (43–46 km, 47–54 m relief) sit on a rock-plateau margin and may be cliffs, not dunes. They are flagged for an S2 check.
- **Novelty check:** As for C1. The convergence argument and the per-dune list did not appear in anything I saw.
- **Orbital signature:** As C1. The megadunes are 1–3 km long and 50–60 m high, so they show clearly in GLO-30 and S2. A buried iron mass would only show magnetically.
- **Biggest reason wrong:** Warren et al. repeated the route in reverse and it took three days with loaded camels, so 46–50 km overnight is at the edge of what is feasible. The "half way" in the blacksmith's account may refer to a different, smaller object (see C3). The base rate is also low (C1).
- **Confidence:** 3

### C3. The Linarès blacksmiths' "block as big as my house": Chinguetti–Ouadane midpoint and an unexamined 60 m linear ridge 54 km ENE — NOVEL-SYNTHESIS
- **Coordinates:** 20.680, -11.940 (±12 km). This circle covers both the computed midpoint (20.697, -11.994) and the centre of the ridge (20.66, -11.89).
- **What / why (sig 7):** The blacksmiths of Chinguetti said they "recovered iron" from a block E or SE of town, roughly half way to Ouadane. Workable native iron in a house-sized block would itself be a giant iron meteorite (≫100 t), whether or not Ripert's hill exists.
- **Evidence chain:**
  1. The testimony is in Warren et al. They assumed it described the same object as Ripert's hill and tested it only in the eastern Les Boucles, 12–22 km E, with a null result. They also state that "there are no further large dunes to the E within our 50 km limit". https://arxiv.org/abs/2402.14150
  2. **Contradiction:** their 50 km limit comes from Ripert's 10-hour ride. The blacksmiths' account has no time limit, and the literal midpoint is 46 km ENE (my geodesic calculation, azimuth 56°). That ground has not been surveyed in any work I saw.
  3. GLO-30 shows a straight ridge about 20 km long running NNW–SSE from about 20.75, -11.93 to 20.57, -11.83. It stands about 50–60 m above the plain and is about 600 m wide (profiles at 20.72, 20.66 and 20.60 N), with 40 m+ patches along it. Its centre is 54 km from Chinguetti at bearing about 66° ("E") and 41 km from Ouadane, which matches "roughly half way". If it is sand, it is a hiding place just outside Warren's search radius. If it is rock (dyke or hogback), it may itself be the "house" landmark. (`data/T3/zoom_NE.png`)
  4. Detectability (my derivation, same assumptions as C1): a 10 m iron sphere gives only about 4–8 nT at 100 m and about 1 nT at 250 m. PRISM-I, with 500 m line spacing, has roughly a 50% chance of catching it. A foot magnetometer would see it easily (≈500 nT at 20 m). The coverage edge is ≈11°56′W, about 0.05° east of the midpoint, so the midpoint is just inside PRISM-I coverage (Warren et al.).
- **Novelty check:** Searched under the Chinguetti queries above. No source places the blacksmiths' block at the true midpoint, and none mentions this ridge. The search budget prevented any further checks.
- **Orbital signature:** The block is about 5–10 m across, dark, possibly with blacksmith spoil (slag or charcoal hearths) around it. That is 1 pixel in S2 and **needs sub-metre imagery (Maxar or Google Earth)**. The ridge is **S2- and DEM-visible**. The lead's S2 check is the tone of the ridge: pale, smooth sand versus dark, varnished, gullied rock.
- **Biggest reason wrong:** The block may be a lateritic or haematitic ironstone that the smiths smelted, rather than meteoritic iron. The testimony is second-hand (1934). The direction "E or SE" sits awkwardly with an ENE midpoint.
- **Confidence:** 3

### C4. Ahnet–Tidikelt terminal basin: Holocene highstand shoreline at the southern inflow delta — NOVEL-SYNTHESIS (novelty check NOT completed)
- **Coordinates:** 25.66, 1.54 (±15 km). Secondary target: the NE inflow at 26.68, 1.94 (±15 km).
- **What / why (sig 5):** The lowest closed basin of the Ahnet region is a candidate humid-period lake. Wadi deltas at the highstand contour are prime places for Holocene (and older) settlement.
- **Evidence chain (all my own derivation from GLO-90 open data):**
  1. A fill-difference analysis gives a closed basin about 8,200 km² in area. Its floor is **116 m** (deepest at 26.402, 1.502) and its spill is about **174 m**, probably westward toward the Reggane low (26.58, 0.44), where the filled-flow outlet carries the basin's whole catchment.
  2. Hypsometry within the window: 1,025 km² lies below 125 m and 9,495 km² below 175 m. That is a flat floor of sebkha scale, consistent with a lake of up to about 9,000 km² at highstand.
  3. D8 inflows crossing the 175 m contour, by catchment: 28,542 km² entering at 26.678, 1.935 (NE); 17,213 km² at 25.661, 1.540 (S, draining the Ahnet uplands); 13,680 km² at 26.111, 0.955 (SW); 7,285 km² at 25.698, 1.282.
  4. Name: I believe the low is the sebkha usually mapped as **Sebkha Mekerrhane**, south-west of In Salah **[BK-unverified]**.
- **Novelty check:** Not possible; the search budget was exhausted. The lead should search "Mekerrhane Holocene lake", "Ahnet paleolake" and "sebkha Mekerrhane archaeology". If published, downgrade to KNOWN or PROPOSED.
- **Orbital signature:** Possible paleoshoreline benches and tone bands near the 160–175 m contour, white diatomite or lacustrine carbonate, and delta lobes. These are **S2-visible**, km scale. In GLO-30, benches of 1–3 m are only marginal. Sites themselves (lithic scatters, hearths, stone circles) **need sub-metre imagery**.
- **Biggest reason wrong:** Part of the closed basin may be a DEM artefact of dune damming. The highstand may predate the Holocene. The area may already be well known to Algerian or French Quaternary work.
- **Confidence:** 25 (that a Holocene lake margin with sites exists at these deltas)
- looting_sensitive: true

### C5. Zerzura "as Wilkinson located it": the sub-sea-level lake-depression chain 170–220 km W/NW of the Farafra–Bahariya track — PROPOSED (sector); contradiction-mined
- **Coordinates:** 28.770, 26.950 (±30 km). The two depressions inside this circle are listed below.
- **What / why (sig 5):** Wilkinson's original 1835 clue places Zerzura about 500 km north of the Gilf Kebir wadis that later explorers settled on. Following the original clue leads to real, spring-fed but uninhabited depressions rather than rain-fed Gilf wadis.
- **Evidence chain:**
  1. Wilkinson placed the oasis "five days West of the track connecting the oases of Farafra and Bahariya", based on an Arab who found it while searching for a lost camel. https://www.heritagedaily.com/2023/04/the-search-for-the-lost-city-of-zerzura/146743 ; https://explorersweb.com/exploration-mysteries-zerzura/ ; http://geoffrey-kolbe.com/C-Nav/zerzura.htm
  2. The Gilf identification comes from Almásy's later reasoning, which placed Zerzura near the end of the Dakhla–Kufra route (explorersweb), and from his 1932–33 finds (https://en.wikipedia.org/wiki/Zerzura). These are different informants and a different geography, so the identification does not follow from Wilkinson.
  3. My calculation: five camel-days at 25–40 km/day is 125–220 km. In GLO-90, the only closed depressions in that band with floors low enough to intersect the regional aquifer (spring oases) are a chain of sub-sea-level basins:
     - 28.715, 26.753: floor -9 m, 307 km², 197 km from the track
     - 28.830, 27.155: floor -33 m, 602 km², 170 km
     - 28.973, 26.686: floor -69 m, 194 km², 218 km
     - 28.613, 27.562: floor +38 m, 214 km², 124 km

     These are presumably the known uninhabited lake oases between Bahariya and Siwa (Sitra, Bahrein, Nuwamisa, El Areg) **[BK-unverified names; match to a gazetteer]**.
  4. A non-peer-reviewed draft also restricts the Zerzura search to the area west of the Farafra–Bahariya line. https://www.researchgate.net/publication/373200968_TLBR_-_The_Lost_City_of_Zerzura_-_Draft_001
  5. The Kitab al-Kanuz city "white as a dove" is literary. The earliest mention, a mid-13th-century al-Nabulsi list of deserted *Fayyum* villages, suggests a northern rather than a Gilf locus. https://en.wikipedia.org/wiki/Zerzura ; https://en.wikipedia.org/wiki/Kitab_al-Kanuz
- **Novelty check:** The search budget ran out before I could check "Zerzura Sitra" or "Zerzura Bahrein". The sector was proposed by the TLBR draft. Treat it as PROPOSED.
- **Orbital signature:** Salt-lake and palm or reed patches are dark green in S2 and **S2-visible**. Depressions 100–600 km² across are **DEM-visible**. Ruins or tombs at lake margins **need sub-metre imagery**.
- **Biggest reason wrong:** "Five days" is vague, and Wilkinson's informant may have been describing a known oasis. Zerzura may be a composite legend with no single location.
- **Confidence:** 10
- looting_sensitive: true

### C6. Zerzura, Gilf Kebir consensus wadis (Abd el Melik / Hamra / Talh), with a DEM runoff ranking — KNOWN (calibration)
- **Coordinates:** 24.300, 25.231 (±15 km). This is the main N–S trunk wadi of the northern (Abu Ras) plateau.
- **Why:** This is the calibration case. By common consent the three Zerzura wadis are Talh, Abd el Melik and Hamra. Almásy and Clayton found them in 1932–33. Their "oasis" is rain-fed pools with acacia rather than springs. http://geoffrey-kolbe.com/C-Nav/zerzura.htm ; https://historynet.com/the-quest-for-zerzura/ ; https://en.wikipedia.org/wiki/Zerzura
- **DEM contribution (GLO-90 D8):** Fit to Zerzura, meaning pools and trees, scales with catchment.
  - The largest single drainage in the Gilf is the N–S trunk on the northern plateau. Its catchment grows from 360 km² at 23.95 N (lon 25.30) to **2,269 km² at 24.50 N (lon 25.22)**. I *tentatively* identify it as Wadi Abd el Melik **[BK-unverified]**.
  - The main plateau's largest north-draining system leaves the plateau at **24.124, 25.998 (1,587 km²)**.
  - The largest east- and south-draining wadi mouths are at 23.033, 26.107 (722 km²), 23.488, 26.485 (583 km²) and 23.315, 26.363 (483 km²). These are the systems I would check against gazetteer names (Wadi Wassa, Firaq, el Bakht and others **[BK-unverified]**).
  - Under-examined candidate: if the 24.124, 25.998 system is *not* one of the named three, it is the best-watered wadi of the main plateau and lacks the Zerzura literature attention I saw.
- **Orbital signature:** Acacia lines in the wadi floors (S2-visible as dark dots and lines); wadi floors 0.2–1 km wide; DEM-visible.
- **Confidence:** 30 (that the 2,269 km² trunk is Abd el Melik; the KNOWN status itself is not in doubt)

## Cannot resolve (evidence too thin this session)
- **Cambyses' lost army.** I could not source the competing claims this session. These include Herodotus 3.26 ("midway" between Oasis and Ammon, buried by a south wind), the Castiglioni brothers' 2009 claim, and Kaper's revolt hypothesis. All of these are **[BK-unverified]**. My geometry shows the following:
  - The direct Kharga (Hibis) to Siwa line is 645 km; its midpoint is 27.37, 28.08.
  - Via Farafra the route is 649 km; midpoint 27.12, 27.90.
  - Via Dakhla and Farafra it is 696 km; midpoint 26.97, 28.03.
  - Via Bahariya it is 698 km; midpoint 28.26, 28.91.

  Every "midway" falls in or on the rim of the **Farafra or Bahariya depressions**, which are oases and limestone plateau, not the Great Sand Sea. A sand burial "midway" is therefore geomorphically inconsistent unless the army left the oasis chain westward into the Sand Sea. That reading favours the non-sandstorm explanations. Any search corridor would be the Sand Sea tongue W/NW of Farafra (about 27.1–27.6 N, 26.6–27.4 E), where GLO-90 shows NNW–SSE seif corridors entering the depression. My confidence that the army lies there is below 2%, so this is not ranked.
- **Trans-Saharan caravan towns (al-Bakri, al-Idrisi, Ibn Battuta) and the Mali capital.** I had no searches left. I report no candidates rather than restating legends from memory.
- **Arabia (Iram/Ubar beyond Shisr, Green Arabia coverage gaps, Rub' al-Khali).** Not sourced. A GLO-90 flat-floored interdune screen of the Nefud ran (`nefud_overview.png`). Its top flat basins lie mostly *outside* the dune sea (27.0–27.9 N, 42.4–43.6 E). Inside the sand sea it flagged 27.634, 41.340 and 28.107, 39.286 as possible paleolake basins. Without Green Arabia's site list I cannot call either a gap, so neither is ranked.

## Dead ends
- The premise of a "2021 arXiv paper reconstructing candidate mesas" is wrong. The paper is arXiv:2402.14150 (2024), and it reconstructs dunes. The "mesa" answer is Monod's guelb Aouinet (1989), which is KNOWN and has no metal.
- West Farafra lobe (floor 52.7 m at 27.172, 27.032): a good spring setting, but it is only 94 km (about 3 days) from the Farafra–Bahariya track, so it fails Wilkinson's "five days". Rejected for C5.
- A 780 m contour threshold for Gilf wadi mouths missed the lower northern plateau (~650–750 m). I replaced it with direct channel tracing.
- Dune-texture route analysis (Kharga–Siwa): the texture index does not separate dunes from escarpments. I used it only qualitatively.
- PALSAR/Landsat-thermal searches for Chinguetti were already done by Warren et al., with nothing of interest. Not repeated.
- arxiv.org and other hosts were unreachable by WebFetch; the WebSearch budget was exhausted after about 9 queries.

## Sources
- Warren, R., Warren, S., Protopapa, E. (2024). New evidence on the lost giant Chinguetti meteorite. https://arxiv.org/abs/2402.14150 (PDF read via https://storage.googleapis.com/arxiv-dataset/arxiv/arxiv/pdf/2402/2402.14150v1.pdf ; text in `data/T3/chinguetti.txt`)
- https://en.wikipedia.org/wiki/Chinguetti_meteorite
- Marvin 2007, https://www.lyellcollection.org/doi/full/10.1144/SP287.16
- https://meteoritestheblog.com/2014/07/25/the-first-post/
- https://phys.org/news/2024-03-physicists-deny-chinguetti-meteorite.html
- http://sciencythoughts.blogspot.com/2024/02/looking-for-chinguetti-meteorite.html
- https://www.sciencealert.com/the-worlds-largest-meteorite-seemed-to-vanish-in-1916-why-cant-we-find-it
- https://grokipedia.com/page/chinguetti_meteorite (low reliability; used only for the PRISM access status)
- https://en.wikipedia.org/wiki/Zerzura ; https://en.wikipedia.org/wiki/Kitab_al-Kanuz
- https://www.heritagedaily.com/2023/04/the-search-for-the-lost-city-of-zerzura/146743
- https://historynet.com/the-quest-for-zerzura/
- http://geoffrey-kolbe.com/C-Nav/zerzura.htm
- https://explorersweb.com/exploration-mysteries-zerzura/
- https://www.researchgate.net/publication/373200968_TLBR_-_The_Lost_City_of_Zerzura_-_Draft_001
- Copernicus DEM GLO-30 / GLO-90 (AWS open data): https://copernicus-dem-30m.s3.amazonaws.com , https://copernicus-dem-90m.s3.amazonaws.com
- Derived files: `discoveries/2026-11-09-hidden-earth/data/T3/` (chinguetti_dune_patches.json, *.png maps, *_z.npy DEM mosaics, gk_acc.npy flow accumulation)

```json
[
 {"id":"T3-C1","name":"Chinguetti iron hill: unsurveyed SW/S Les Boucles megadune fronts","lat":20.360,"lon":-12.440,"radius_km":6,"feature_size_m":100,"signature":"Buried iron mass ~100x40 m at SW (lee) foot of >40 m dunes; targets LB-SW1..5 W-edges (e.g. 20.3471,-12.4549; 20.3804,-12.4238). If exposed: dark block on pale dune foot. Decisive test: PRISM-I aeromag or foot magnetometer.","s2_visible":false,"dem_visible":false,"significance":9,"novelty":"PROPOSED","confidence":4,"looting_sensitive":false,"category":"lost meteorite","one_line":"Per-dune walk lines for the unsurveyed Les Boucles dunes that Warren et al. 2024 left open; matches Ripert's original 'SW'."},
 {"id":"T3-C2","name":"Chinguetti iron hill: NW Batraz megadunes","lat":20.190,"lon":-12.005,"radius_km":4,"feature_size_m":100,"signature":"Buried iron mass at W foot of 50-61 m megadunes B1 (W-edge 20.183-20.197,-12.0024), B3 (20.1915,-12.0246), B4 (20.1962,-11.9793).","s2_visible":false,"dem_visible":false,"significance":9,"novelty":"PROPOSED","confidence":3,"looting_sensitive":false,"category":"lost meteorite","one_line":"Only high-dune ground that fits Ripert's corrected SE bearing, the blacksmith's ~46 km 'half-way' distance and the 50 km camel limit together."},
 {"id":"T3-C3","name":"Linares blacksmiths' house-sized iron block near Chinguetti-Ouadane midpoint / 60 m ENE ridge","lat":20.680,"lon":-11.940,"radius_km":12,"feature_size_m":10,"signature":"5-10 m dark block, possible slag/hearth spoil (sub-metre needed); nearby 20 km NNW-SSE ridge 50-60 m high (20.75,-11.93 to 20.57,-11.83): S2 tone check sand vs rock.","s2_visible":false,"dem_visible":false,"significance":7,"novelty":"NOVEL-SYNTHESIS","confidence":3,"looting_sensitive":true,"category":"lost meteorite","one_line":"Warren et al. tested the blacksmiths' account 12-22 km E; the literal midpoint (46 km ENE) and an unexamined 60 m ridge 54 km ENE were never surveyed."},
 {"id":"T3-C4","name":"Ahnet-Tidikelt terminal basin (Sebkha Mekerrhane?) southern inflow delta highstand shoreline","lat":25.66,"lon":1.54,"radius_km":15,"feature_size_m":5000,"signature":"Closed basin floor 116 m, spill ~174 m (~9,500 km2 at highstand); 17,213 km2 wadi enters at 175 m contour; shoreline tone bands/diatomite S2-visible, sites need sub-metre. Secondary NE inflow 26.68,1.94.","s2_visible":true,"dem_visible":true,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":25,"looting_sensitive":true,"category":"paleolake / Holocene settlement","one_line":"DEM-derived 9,000 km2 highstand basin in the Ahnet region; its main inflow deltas are the best Holocene shoreline-site targets (novelty check not completed)."},
 {"id":"T3-C5","name":"Zerzura per Wilkinson: sub-sea-level lake depressions 170-220 km W/NW of the Farafra-Bahariya track","lat":28.770,"lon":26.950,"radius_km":30,"feature_size_m":20000,"signature":"Closed depressions floor -9 to -69 m, 194-602 km2 (28.715,26.753; 28.830,27.155; 28.973,26.686); salt lakes and palm/reed patches S2-visible; ruins need sub-metre.","s2_visible":true,"dem_visible":true,"significance":5,"novelty":"PROPOSED","confidence":10,"looting_sensitive":true,"category":"lost oasis","one_line":"Wilkinson's original 'five days west of the Farafra-Bahariya track' points ~500 km north of the Gilf, at the spring-fed lake-oasis chain between Bahariya and Siwa."},
 {"id":"T3-C6","name":"Zerzura consensus wadis, Gilf Kebir (calibration); largest DEM catchment trunk","lat":24.300,"lon":25.231,"radius_km":15,"feature_size_m":800,"signature":"N-S trunk wadi, 2,269 km2 catchment at 24.50N; acacia lines in 0.2-1 km wide floor; main-plateau N system exits at 24.124,25.998 (1,587 km2).","s2_visible":true,"dem_visible":true,"significance":4,"novelty":"KNOWN","confidence":30,"looting_sensitive":false,"category":"lost oasis (calibration)","one_line":"KNOWN Zerzura wadis; DEM runoff ranking says the northern-plateau trunk (likely Abd el Melik) and the 24.12N/26.00E system are the best-watered."}
]
```
