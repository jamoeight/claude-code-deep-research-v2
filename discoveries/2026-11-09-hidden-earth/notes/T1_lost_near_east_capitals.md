# T1 — Lost royal cities of the ancient Near East and Egypt

## Method (what you joined, what you searched; 5-10 lines)
- Joined textual geography from web searches (Akkad/Agade proposals, Ur III and OB references, the Bronze Tablet and Hartapu inscriptions, Lisht cores, Irisaĝrig distance data, Musasir finds) with **Pleiades gazetteer coordinates** (CIGS/DARMC/BAtlas points pulled from `raw.githubusercontent.com/isawnyu/pleiades-datasets`, saved in `data/T1/pleiades/`) and **Copernicus GLO-30 DEM** + **ESA WorldCover** analysis run here (scripts in the scratchpad; outputs in `data/T1/*.png|*.csv`).
- DEM work: relief profiles at every candidate tell; regional relief maps of the Baghdad–Samarra corridor (`corridor.png`, `adhaim.png`, `reach.png`, `sinker_area.png`, `south.png`), the Konya plain (`konya.png`, `konya_zoom.png`), Lisht (`lisht.png`, `lisht_flood.png`), and zooms (`zoom2.png`, `belt_targets.png`). Calibration: Çatalhöyük (known, 37.6667, 32.8276) is detected as a 15 m / 14 ha mound, and Tell Sinker as an 8.6 m mound, so the method sees large tells.
- Geodesic distances computed with pyproj (Umma→Irisaĝrig candidates, Sippar→Akkad candidates, Çumra→TKH).
- **Limits:** WebFetch could not reach any site (DNS blocked), so all literature claims rest on search-result summaries. The shared web-search budget ran out mid-run (≈50 searches), so Ekallatum, Kussara, Arinna, Arzashkun, Taidu and Ineb-hedj were not researched, and some novelty checks are incomplete (said so per candidate). An automated DEM tell detector for the Agade corridor failed calibration (276 hits, missed Tell Sinker) and is reported only as a dead end.

## Candidates (ranked)

### C1. Agade/Akkad at Tell Sinker, on a relict Tigris meander belt NW of Baghdad — PROPOSED
- Coordinates: 33.7981, 44.3244 (±1 km) (DEM peak; published point 33.79723, 44.32385)
- What it would be / why it matters (significance 10): the capital of the first territorial empire (Sargon, Naram-Sin), the only unlocated Mesopotamian imperial capital.
- Evidence chain:
  1. Tell Sinker has been proposed for Agade on the basis of the Early Dynastic List of Geographical Names. It lies "on the ancient bed of the Tigris river northwest of Baghdad". It is Akkad Survey site 16 (primarily Early Dynastic; 600 × 300 m, with a 250 × 100 × 10 m central mound). https://en.wikipedia.org/wiki/Akshak (seen in search results; HandWiki mirror https://handwiki.org/wiki/History:Akshak)
  2. N. Kawakami, "Searching for the Location of the Ancient City of Akkade in Relation to the Ancient Course of the Tigris Using Historical Geographical and GIS Analyses", Akkadica 143 (2022) 101–135, plus earlier GIS reconstructions of the Ur III Tigris. https://jglobal.jst.go.jp/en/detail?JGLOBAL_ID=202101003038834773 ; https://researchmap.jp/naokawa?lang=en
  3. Active fieldwork: a JSPS-funded Japan–Iraq joint survey of Akkade (2024–2028). The first surface survey at Tell Sinker ran 14 Mar–2 Apr 2025 and collected diagnostic sherds around the mound margins to estimate site extent. Talks followed in Dec 2025 and Mar 2026. https://kaken.nii.ac.jp/en/grant/KAKENHI-PROJECT-24K21175/ ; https://www1.niu.ac.jp/topics/study/2025/7009.html ; https://www.tokyo-np.co.jp/article/403940 ; report PDF (not reachable here): http://jswaa.org/wp/wp-content/uploads/2026/03/report06-kawakami.pdf
  4. Textual constraints that fit a Tigris-side site north of Baghdad: Steinkeller (2001) argued Akkade must lie off the Tigris rather than the Euphrates, north of Adab, and a city list places Akkade off the Tigris between Eshnunna and Ashur (summarized in https://en.wikipedia.org/wiki/Irisa%C4%9Drig). Agade is generally placed along or east of the Tigris between Samarra and Baghdad (Pleiades https://pleiades.stoa.org/places/63806066 ; https://archaeology.org/issues/may-june-2024/collection/capital-of-the-worlds-first-empire/lost-cities/).
  5. **New DEM evidence (this run):** GLO-30 shows a relict meander belt with loops 1–2 km across. It diverges from the modern Tigris near Balad (≈33.98 N, 44.15 E) and rejoins it near 33.55 N, 44.33 E, so it is a ≈50 km cutoff (`data/T1/sinker_area.png`, `reach.png`). Tell Sinker sits on the east bank of a relict loop at mid-reach. Its DEM peak is 8.6 m above the 1.2 km background (`dem.py` profile). This physically confirms the "ancient bed of the Tigris" setting.
- Novelty check: I searched "Tell Sinker Agade", "Kawakami Akkadica 2022", and "テル・シンカー遺跡 アッカド". The site is published and under active survey, so it is PROPOSED. The DEM delineation of the cutoff is my own work; Kawakami's GIS paper (not readable here) may already contain it.
- Orbital signature: a 600 × 300 m light-toned bare mound within irrigated fields, with a 250 × 100 m central rise of ~10 m. Visible in S2 and in the DEM (8.6 m relief at 30 m). Relict channel scars and ponds lie immediately west.
- Biggest reason it could be wrong: the surface survey called it "primarily Early Dynastic", and nothing Sargonic has been reported. An OB itinerary reportedly places Akkad between Sippar and Khafajah, but Tell Sinker is 82 km N of Sippar and 54 km from Khafajah, a 3× detour on a 43 km route (https://en.wikipedia.org/wiki/Akkad_(city), as summarized in search results).
- Confidence (0-100): 15

### C2. Agade in the paleo-Adhaim / relict-Tigris junction zone between Balad and Ad-Dujayl — NOVEL-SYNTHESIS
- Coordinates: 33.97, 44.23 (±8 km)
- What it would be / why it matters (significance 10): this zone reconciles the two strongest north-of-Baghdad proposals: Ziegler's "near the Adhaim–Tigris confluence" and Kawakami's "on the ancient Tigris bed (Tell Sinker)".
- Evidence chain:
  1. Nele Ziegler (CNRS) favours a spot near the Adhaim–Tigris confluence, ~50 miles N of Baghdad. https://archaeology.org/issues/may-june-2024/collection/capital-of-the-worlds-first-empire/lost-cities/ . The Sargon article likewise says "the region of the confluence of the Tigris and the Adhem … or further down towards Baghdad". https://en.wikipedia.org/wiki/Sargon_of_Akkad
  2. DEM derivation (`adhaim.png`, `reach.png`): today the Adhaim leaves its incised valley onto the floodplain at ≈34.03 N, 44.30 E (BAtlas point A007, 34.0297, 44.2976, lies there). The relict Tigris belt of C1 diverges from the modern river at ≈33.98 N, 44.15 E, 14.9 km away on azimuth 248°. When the Tigris used the relict belt, the Adhaim must have crossed the floodplain to join it. That paleo-junction falls in the 33.93–34.00 N, 44.15–44.30 E box, ~21 km NNW of Tell Sinker along the same belt.
  3. BAtlas/DARMC lists Tulul al-Hibir (33.9722, 44.2498) inside this box (Pleiades https://pleiades.stoa.org/places/894163). The DEM shows only a 4.3 m local peak there (33.9745, 44.2514), because orchards and buildings degrade a 30 m DSM.
  4. A Tigris quay is required: Agade is a Tigris-side port city in the Ur III/OB tradition (Steinkeller via https://en.wikipedia.org/wiki/Irisa%C4%9Drig). A junction city would control both the Tigris and the Adhaim route to the Zagros piedmont.
- Novelty check: I searched "Adhaim confluence Agade" and "Tell Sinker" and found Ziegler (confluence) and Kawakami (ancient bed), but nothing that joins them through the DEM-traced divergence point. Kawakami 2022 was unreadable here and could overlap. The search budget was exhausted before a final check.
- Orbital signature: a tell of 30–100 ha, perhaps 5–15 m high, at the inner margin of relict meander scars. It would need S2 and sub-metre imagery to separate it from the Balad/Ad-Dujayl orchards and villages. In the DEM, only a large (>8 m) mound would stand out.
- Biggest reason it could be wrong: the dates of the relict belt and of the Adhaim's ancient outlet are unknown. Either could post-date the 3rd millennium, and the area is heavily built up.
- Confidence (0-100): 6

### C3. Irisaĝrig (Ur III royal-estate city, heavily looted archive) — PROPOSED
- Coordinates: 32.1529, 45.3689 (±5 km), with Tall Warīsh 32.1834, 45.3421 as the alternative inside the radius
- What it would be / why it matters (significance 6): the source of the looted Irisaĝrig tablets (~450 in the U.S.). Thousands of objects were returned to Iraq in 2018, and the city has never been excavated scientifically.
- Evidence chain:
  1. Molina: the looters found the site around 2003. "Site 1056" of Adams' survey, 76 km upstream of Umma, is the leading candidate, with #1032 as the alternative. Satellite images show heavy looting from 2003 to 2009. https://www.livescience.com/62688-lost-city-of-irisagrig-ancient-tablets.html ; https://explorersweb.com/the-race-to-find-a-lost-iraqi-city-before-looters-strip-it-bare/ ; https://www.academia.edu/10126837/
  2. Pleiades/CIGS gives Irisaĝrig a "certain" point at 32.1529, 45.3689, described as "on the Tigris river near Nippur, about 60–80 km north of Umma; heavily looted". https://pleiades.stoa.org/places/237830124
  3. Derivation (pyproj): the CIGS point is **72.8 km** from Umma (Tall Jūka 31.6669, 45.8860; az 318°) and 13.4 km ENE of Nippur. Tall Warīsh (CIGS 32.1834, 45.3421) is **77.0 km** from Umma, which matches Molina's 76 km. An Arabic study proposes "Tell Warsh" for Irisaĝrig (https://search.emarefa.net/detail/BIM-1320445).
  4. DEM: both points sit on the same NW–SE relict levee ridge, 2–3 m high, scattered with small spoil-like mounds (`zoom2.png`). That fits a city on a Tigris branch. The CIGS point shows 3.1 m relief.
  5. Competitors are weaker. Tell al-Wilayah lies 45 km from Nippur, and Steinkeller says it is "definitely not Irisaĝrig" (possibly Anzagar). Umm al-Ḥafriyāt is only 64 km from Umma. (https://en.wikipedia.org/wiki/Irisa%C4%9Drig ; https://www.journals.uchicago.edu/doi/full/10.1086/703852 Viano 2019)
- Novelty check: the location is published in Pleiades/CIGS and by Molina. My only additions are the distance match to Tall Warīsh and the observation that both points lie on one levee.
- Orbital signature: a low mound field (2–4 m) of several tens of ha, pock-marked by looting pits. Pits need sub-metre imagery; the mound is marginal in S2 as a light mottled patch, and the levee is visible in the DEM.
- Biggest reason it could be wrong: CIGS may simply have adopted site 1056 by assumption, and road distances are not straight lines. Only excavated, provenanced tablets would settle it.
- Confidence (0-100): 45

### C4. Itj-tawy (Amenemhat-itj-tawy), Middle Kingdom capital, in the floodplain east of the Lisht pyramids — PROPOSED
- Coordinates: 29.572, 31.236 (±2 km)
- What it would be / why it matters (significance 9): the residence city of the 12th–13th Dynasties.
- Evidence chain:
  1. The city is unlocated and thought to lie near Lisht, buried in the floodplain. Wikidata/Wikipedia give 29°34′13″N 31°13′52″E, i.e. 29.5703, 31.2311. https://en.wikipedia.org/wiki/Itjtawy ; https://www.wikidata.org/wiki/Q389285
  2. Shallow cores found Late Middle Kingdom settlement ≈300 m NE of Amenemhat I's pyramid, interpreted as a suburb. https://www.researchgate.net/publication/320498553 . Using the pyramid's DEM position (29.5799, 31.2268, found by top-hat detection), that point is 29.5818, 31.2290.
  3. Arnold: by the mid-13th Dynasty a dense suburb "of the nearby city – possibly Jtj-t3wj" covered the S and E cemetery. Desert-edge koms include the Kom el-ʿAgil faience site. https://en.wikipedia.org/wiki/Lisht
  4. Hawass (2024): "the town centre lies deep beneath the cultivation". https://english.ahram.org.eg/News/519298.aspx
  5. Parcak: a spot chosen from NASA topography and then cored showed a Middle Kingdom occupation layer ~5 m down, with jeweller's waste (carnelian, agate). https://www.lingq.com/de/englisch-lernen-online/courses/58847/sarah-parcak-archeology-from-space-238930/ ; https://www.asor.org/news/2023/1/parcak-webinar-middle-kingdom/
  6. DEM (`lisht_flood.png`, detrended fields only): a western flood basin lies 0.5–1 m low at 31.225–31.24 E, with slightly higher ground at 31.245–31.255 E. My candidate centre sits between the pyramids' latitudes, 1–2 km east of the desert edge.
- Novelty check: the area is published (Wikidata, Arnold, Hawass, Parcak). I add only the explicit derivations.
- Orbital signature: none. The city is buried about 5 m under alluvium and modern fields and villages. Finding it needs coring transects or ERT; possible subtle crop marks would need sub-metre imagery. It is not visible in S2 or the DEM.
- Biggest reason it could be wrong: the town core may lie farther north or south along the desert edge, under the modern villages.
- Confidence (0-100): 50

### C5. Tarḫuntašša at Türkmen-Karahöyük (Konya plain) — PROPOSED
- Coordinates: 37.5710, 32.7421 (±5 km). This is a DEM-derived mound and must be verified as TKH; see below.
- What it would be / why it matters (significance 9): Muwatalli II's capital, where the Hittite court and the gods of Hatti moved before Kadesh.
- Evidence chain:
  1. Massa, Osborne and Bachhuber suggest TKH is Tarḫuntašša. The 2019 Hartapu inscription was found in a canal by the mound. https://arkeo.bilkent.edu.tr/?page_id=994 ; https://www.cambridge.org/core/blog/?p=36159 ; https://archaeology.org/issues/january-february-2021/collection/turkey-luwian-inscription/top-10-discoveries-of-2020/
  2. Size: the upper mound is ≈30 ha and 35 m high (https://www.asor.org/wp-content/uploads/2020/10/Osborne-et-al_ASOR_VAM2020_Abstract.pdf). The lower town is ≥80 ha (https://isac.uchicago.edu/research/projects/turkmen-karahoyuk-intensive-survey-project). The LBA settlement "at least doubled in size to 60–80 ha" (2024 season: https://isac.uchicago.edu/sites/default/files/uploads/shared/docs/Publications/Annual-Reports/2024-2025/AR2024-25_Turkmen-Karahoyuk.pdf).
  3. 2025: a Luwian seal of the official Kurunti-ziti points to bureaucracy at the site. https://www.anatolianarchaeology.net/3500-year-old-luwian-seal-naming-bronze-age-official-found-at-turkmen-karahoyuk/
  4. Counter-evidence: Hawkins & Weeden (2021) place TKH in the Hulaya River Land (perhaps the Çarşamba/Hotamış system), which the Bronze Tablet treats as the Hatti–Tarḫuntašša frontier. They also argue for two Hartapus. https://discovery.ucl.ac.uk/id/eprint/10155520/1/10.1515_aofo-2021-0015.pdf ; Bronze Tablet text: https://lrc.la.utexas.edu/eieol/hitol/70
  5. DEM (`konya_tophat.csv`, `konya_zoom.png`): the only isolated mound within 15 km of Çumra that matches TKH's published dimensions is at 37.5710, 32.7421. It stands ~30 m above the plain (1041 vs 1011 m), covers ≈24 ha above 2 m, is round, and lies 2.9 km W of Çumra (GeoNames 37.5732, 32.7745). Çatalhöyük, as calibration, comes out at 15 m / 14 ha. Another 30 m feature at 37.5213, 32.9138 sits on an alluvial-fan edge, and its own mound is only ~6–8 m.
- Novelty check: the TKH identification is published and contested. I found no published coordinate for TKH in my sources, so the lead should confirm that the DEM mound is TKH, for example against a Google Earth label or the project maps.
- Orbital signature: an upper mound ~550 m across and ~30–35 m high, surrounded by a low lower-town halo of ≥80 ha. Clearly visible in S2 and the DEM.
- Biggest reason it could be wrong: under the Hawkins–Weeden reading, TKH is the frontier Hulaya land, not the capital. Even the 60–80 ha LBA settlement has yielded no text naming Tarḫuntašša.
- Confidence (0-100): 25

### C6. Muṣaṣir/Ardini (Urartian holy city of Ḫaldi) at Mudjesir (Mdjeser) near Sidakan — PROPOSED
- Coordinates: 36.80, 44.67 (±15 km). This is an approximate Sidakan-district position from model knowledge, anchored on Soran town (GeoNames 36.6556, 44.5422); the exact village coordinates were not available. Replace with Mdjeser village.
- What it would be / why it matters (significance 7): the temple city of Ḫaldi sacked by Sargon II in 714 BC.
- Evidence chain:
  1. Thureau-Dangin located it tentatively at Mudjesir, 10 km W of Topzawa. https://en.wikipedia.org/wiki/Musasir . The Sidekan article places Ardini 5 km from Sidekan. https://en.wikipedia.org/wiki/Sidekan
  2. D. Marf Zamua reports 17 column bases, life-size funerary statues of the 7th–6th c. BC, a seal impression, and vessels at "Mdjeser"; reports describe column bases dedicated to Ḫaldi. https://www.cbsnews.com/news/remains-of-long-lost-temple-guarded-by-life-size-statues-discovered-in-iraq/ ; https://historyofarmenia.org/2017/06/11/remains-long-lost-temple-musasir-discovered-iraq/
  3. Penn Museum surveys found signs of a monumental structure at Mudjesir, and early Iron Age terraced buildings at Gund-i Topzawa that were destroyed while still in use. https://www.penn.museum/sites/expedition/searching-for-the-kingdom-of-musasir/
- Novelty check: published (Zamua, Penn). I could not verify the "2023 finds" named in the brief; my searches surfaced only the 2005–2017 reports.
- Orbital signature: a village-scale terrace with temple foundations a few hundred metres across in a mountain valley. It needs sub-metre imagery and is not visible in the DEM.
- Biggest reason it could be wrong: the evidence is statues and column bases, with no inscription naming Muṣaṣir. Wikipedia even states the hypotheses cluster at "36°N 46°E", which is inconsistent with Mudjesir.
- Confidence (0-100): 45 (that Muṣaṣir lies within the radius)

### C7. Thinis (Tjeny), First Dynasty capital — PROPOSED
- Coordinates: 26.3372, 31.8930 (±6 km) (Girga town, GeoNames)
- What it would be / why it matters (significance 9): the seat of the Thinite kings whose tombs are at Abydos.
- Evidence chain:
  1. Mainstream consensus places Thinis at or near Girga or el-Birba. A statue fragment naming Thinis is said to come from el-Birba, and as of 2025 the question is inconclusive. https://en.wikipedia.org/wiki/Thinis ; https://en.wikipedia.org/wiki/Girga
  2. Mariette's Kom el-Sultan and the el-Kherbeh / el-Tineh proposals have lost favour. https://en.wikipedia.org/wiki/Kom_El_Sultan ; https://www.ancient-origins.net/ancient-places-africa/lost-city-thinis-first-capital-united-egypt-009807
  3. Girga is 17.0 km from the Abydos necropolis (Pleiades 26.1851, 31.9176; https://pleiades.stoa.org/places/756512), a plausible capital–necropolis spacing.
- Novelty check: published. I found no 2018–2025 coring or survey project in my searches.
- Orbital signature: buried under Girga or el-Birba and floodplain silt. Not visible in S2 or the DEM; needs coring.
- Biggest reason it could be wrong: the Nile has migrated across this reach, so the city may have been eroded or lie on the opposite bank.
- Confidence (0-100): 40

### C8. Waššukanni (Mittani capital) at Tell Fekheriye / Ras al-Ain — PROPOSED (contested)
- Coordinates: 36.8415, 40.0701 (±3 km) (DEM peak; Pleiades 36.8426, 40.0710)
- What it would be / why it matters (significance 8): the capital of the Mittani empire; its archive would rival Amarna.
- Evidence chain:
  1. Opitz proposed the largely unexcavated Tell Fekheriye. De Martino, Novák and Bonatz support it after German excavations (2006–2010), but no document naming the capital has been found. https://en.wikipedia.org/wiki/Wa%C5%A1%C5%A1ukanni ; https://vici.org/vici/21237/?lang=en
  2. Against it: an NAA comparison with clay from the Mittani Amarna letters appeared to rule out Fekheriye, and Lipiński rejects the identification. The site is securely Iron Age Sikkan. (same sources; https://pleiades.stoa.org/places/413537087 ; petrography: https://journals.librarypublishing.arizona.edu/jaei/article/875/galley/870/download/)
  3. DEM: a 13.9 m relief peak, partly under the Ras al-Ain town fabric (`zoom2.png`).
  4. Related: the other Mittani royal city, Taʾidu, is tentatively placed at Tell Hamidi (BAtlas 36.8165, 41.1668; https://pleiades.stoa.org/places/874740). The DEM shows a 34 m mound there.
- Novelty check: published and contested.
- Orbital signature: a ~1 km mound complex, partly urbanised. Visible in S2 and the DEM.
- Biggest reason it could be wrong: the clay provenance result and the absence of texts.
- Confidence (0-100): 35

### C9. Tarḫuntašša, southern alternative: the Karaman–Karadağ–Kızıldağ zone, with the Göksu valley as a tail — PROPOSED
- Coordinates: 37.40, 33.15 (±25 km) (Karadağ, Pleiades https://pleiades.stoa.org/places/648588); Karaman/Laranda is at 37.18, 33.22
- What it would be / why it matters (significance 9): the same city as C5, under the Hawkins–Weeden reading that TKH is the Hulaya frontier and the capital lies beyond it.
- Evidence chain:
  1. An academic paper argues for the Karadağ volcano, with Kızıldağ less likely. https://www.academia.edu/12856389
  2. The Hartapu inscriptions at Kızıldağ and Karadağ are dated to the 12th c. by Hawkins & Weeden. https://discovery.ucl.ac.uk/id/eprint/10155520/1/10.1515_aofo-2021-0015.pdf
  3. Other published options include the Göksu valley, Kilise Tepe near Mut, Meydancıkkale (Pleiades 36.2733, 33.4411) and Sirkeli. https://en.wikipedia.org/wiki/Tar%E1%B8%ABunta%C5%A1%C5%A1a ; Jones's 2019 GIS thesis "challenges the consensus". https://etheses.bham.ac.uk/id/eprint/8793/
- Novelty check: published. I did not screen the Karaman plain for large unnamed LBA-size mounds; the DEM showed volcanic outliers only. That screen is the obvious next step.
- Orbital signature: a capital-size mound (>20 ha) on the Karaman plain, or an acropolis site on the volcanic flanks. A mound would show in S2 and the DEM.
- Biggest reason it could be wrong: no large LBA site in the Karaman area has been reported in my sources.
- Confidence (0-100): 15

### C10. Agade in the Samarra / Qadisiyya area (Reade 2002) — PROPOSED
- Coordinates: 34.2001, 43.8767 (±15 km) (Samarra, Pleiades https://pleiades.stoa.org/places/894082)
- What it would be / why it matters (significance 10): Agade.
- Evidence chain:
  1. Reade (ZA 92, 2002) suggests Agade lay on the Tigris near Qadisiyah, and a later summary says he argued it is "most probably buried under the Abbasid residential city of Samarra". https://www.researchgate.net/publication/249937745 ; https://keibi.uni-tuebingen.de/Record/KEI00000965
  2. A colossal black-stone statue fragment (possibly Rimush) from "El Sanam" was cited for this area. https://www.labrujulaverde.com/en/2025/09/akkad-the-city-that-was-the-capital-of-the-first-empire-in-history-has-still-not-been-found/
- Novelty check: published.
- Orbital signature: it would lie under or among the 9th-century Abbasid ruin field, so it is not separable in S2 or the DEM.
- Biggest reason it could be wrong: Samarra is 61 km NW of Tell Sinker and farther still from Sippar, Kish and the Diyala, so it is weak against the OB itinerary.
- Confidence (0-100): 5

## Dead ends (things you checked that did not pan out, 1 line each)
- Tell Muhammad (Wall-Romana 1990's Agade; 33.3008, 44.4682): Pleiades now reads it as probably **Diniktum** from OB diplomatic letters, and no Akkadian remains were found (https://pleiades.stoa.org/places/249999668 ; https://openbible.info/geo/modern/m310ad8/tell-muhammad). Its relief is 9 m, inside Baghdad.
- Ishan Mizyad (Weiss 1975; 32.5932, 44.5561): Ur III remains and Akkadian administrative texts, but no capital-scale evidence; only 3 m in the DEM (https://pleiades.stoa.org/places/215156343).
- Tell ed-Der / Sippar-Amnanum (Ménant 1875): rejected because later texts distinguish Akkad from Sippar.
- Tall Ghaḍaiyrīfah (34.1818, 44.2649), a CIGS "large mound" with an inscribed door socket near the Adhaim: the DEM shows ≤2.4 m and the site is off the floodplain; I could not identify the inscription (https://pleiades.stoa.org/places/830124755). The lead is unresolved, not dead.
- Opis/Upi at Tell Mujeiliʿ (33.1844, 44.7015): context for Agade only; 76.6 km from Tell Sinker.
- Automated DEM tell detection (top-hat / percentile relief + WorldCover mask) along the Agade corridor: 276 hits, dominated by levees, fishponds and terraces, and it missed Tell Sinker. Not reliable without imagery. Weak residual targets 2 km SW of Tell Sinker (33.7829, 44.3093, ≈40 ha low rise) and at 33.8265, 44.2965 are listed in `data/T1/belt_targets.png` for the lead only.
- Tell al-Wilayah for Irisaĝrig: rejected by Steinkeller; 45 km from Nippur.
- Umm al-Ḥafriyāt for Irisaĝrig (Frayne 1992): 64 km from Umma, short of 76 km.
- Kilise Tepe for Tarḫuntašša: a small site; the Çağdın inscription's reading of the name is doubtful.
- Ekallatum, Kuššara, Arinna, Arzaškun, Ḫamazi, Awan, Ineb-hedj: not researched because the search budget ran out.

## Sources
- Akkad: https://en.wikipedia.org/wiki/Akkad_(city) ; https://en.wikipedia.org/wiki/Akshak ; https://en.wikipedia.org/wiki/Sargon_of_Akkad ; https://en.wikipedia.org/wiki/Tell_Muhammad ; https://en.wikipedia.org/wiki/Opis ; https://archaeology.org/issues/may-june-2024/collection/capital-of-the-worlds-first-empire/lost-cities/ ; https://jglobal.jst.go.jp/en/detail?JGLOBAL_ID=202101003038834773 ; https://researchmap.jp/naokawa?lang=en ; https://kaken.nii.ac.jp/en/grant/KAKENHI-PROJECT-24K21175/ ; https://www1.niu.ac.jp/topics/study/2025/7009.html ; https://www.tokyo-np.co.jp/article/403940 ; https://cir.nii.ac.jp/crid/1050296354142797056 ; https://www.researchgate.net/publication/249937745 ; https://keibi.uni-tuebingen.de/Record/KEI00000965 ; https://zenon.dainst.org/Record/000517219/Description ; https://openbible.info/geo/modern/m310ad8/tell-muhammad ; https://www.labrujulaverde.com/en/2025/09/akkad-the-city-that-was-the-capital-of-the-first-empire-in-history-has-still-not-been-found/ ; https://www.academia.edu/2466098/Kish_Akkad_and_Agade
- Irisaĝrig: https://en.wikipedia.org/wiki/Irisa%C4%9Drig ; https://www.journals.uchicago.edu/doi/full/10.1086/703852 ; https://www.academia.edu/10126837/ ; https://www.livescience.com/62688-lost-city-of-irisagrig-ancient-tablets.html ; https://explorersweb.com/the-race-to-find-a-lost-iraqi-city-before-looters-strip-it-bare/ ; https://search.emarefa.net/detail/BIM-1320445
- Tarḫuntašša: https://en.wikipedia.org/wiki/Tar%E1%B8%ABunta%C5%A1%C5%A1a ; https://etheses.bham.ac.uk/id/eprint/8793/ ; https://discovery.ucl.ac.uk/id/eprint/10155520/1/10.1515_aofo-2021-0015.pdf ; https://lrc.la.utexas.edu/eieol/hitol/70 ; https://arkeo.bilkent.edu.tr/?page_id=994 ; https://www.asor.org/wp-content/uploads/2020/10/Osborne-et-al_ASOR_VAM2020_Abstract.pdf ; https://isac.uchicago.edu/research/projects/turkmen-karahoyuk-intensive-survey-project ; https://isac.uchicago.edu/sites/default/files/uploads/shared/docs/Publications/Annual-Reports/2024-2025/AR2024-25_Turkmen-Karahoyuk.pdf ; https://biaa.ac.uk/wp-content/uploads/2024/12/BIAA-e-magazine-2024-16.pdf ; https://www.anatolianarchaeology.net/3500-year-old-luwian-seal-naming-bronze-age-official-found-at-turkmen-karahoyuk/ ; https://www.cambridge.org/core/blog/?p=36159 ; https://archaeology.org/issues/may-june-2024/collection/the-storm-gods-city/lost-cities/ ; https://www.academia.edu/12856389
- Itj-tawy: https://en.wikipedia.org/wiki/Itjtawy ; https://www.wikidata.org/wiki/Q389285 ; https://www.researchgate.net/publication/320498553 ; https://en.wikipedia.org/wiki/Lisht ; https://english.ahram.org.eg/News/519298.aspx ; https://www.lingq.com/de/englisch-lernen-online/courses/58847/sarah-parcak-archeology-from-space-238930/ ; https://www.asor.org/news/2023/1/parcak-webinar-middle-kingdom/ ; https://www.nationalgeographic.com/science/article/news-800-egyptian-tombs-lisht-middle-kingdom-parcak-archaeology
- Thinis: https://en.wikipedia.org/wiki/Thinis ; https://en.wikipedia.org/wiki/Girga ; https://en.wikipedia.org/wiki/Kom_El_Sultan
- Waššukanni: https://en.wikipedia.org/wiki/Wa%C5%A1%C5%A1ukanni ; https://vici.org/vici/21237/?lang=en ; https://journals.librarypublishing.arizona.edu/jaei/article/875/galley/870/download/
- Muṣaṣir: https://en.wikipedia.org/wiki/Musasir ; https://en.wikipedia.org/wiki/Sidekan ; https://www.cbsnews.com/news/remains-of-long-lost-temple-guarded-by-life-size-statues-discovered-in-iraq/ ; https://www.penn.museum/sites/expedition/searching-for-the-kingdom-of-musasir/
- Data: Pleiades datasets https://github.com/isawnyu/pleiades-datasets (places/location_points CSV, CIGS/DARMC points); GeoNames-derived towns https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json ; Copernicus DEM GLO-30 (s3://copernicus-dem-30m); ESA WorldCover 2021 (s3://esa-worldcover). Outputs are in `data/T1/`.

```json
[
{"id":"T1-C1","name":"Agade/Akkad at Tell Sinker (relict Tigris belt)","lat":33.7981,"lon":44.3244,"radius_km":1,"feature_size_m":600,"signature":"600x300 m light mound, 250x100x10 m central rise on E bank of relict Tigris meander loop; DEM 8.6 m relief","s2_visible":true,"dem_visible":true,"significance":10,"novelty":"PROPOSED","confidence":15,"looting_sensitive":true,"category":"lost capital","one_line":"Kawakami's Agade candidate under 2025 Japan-Iraq survey; GLO-30 shows it on a ~50 km relict Tigris cutoff (Balad-Taji)"},
{"id":"T1-C2","name":"Agade at paleo-Adhaim/relict-Tigris junction (Balad-Ad Dujayl)","lat":33.97,"lon":44.23,"radius_km":8,"feature_size_m":800,"signature":"30-100 ha tell 5-15 m high at relict meander scars; orchards/villages obscure; needs S2 + sub-m","s2_visible":true,"dem_visible":false,"significance":10,"novelty":"NOVEL-SYNTHESIS","confidence":6,"looting_sensitive":true,"category":"lost capital","one_line":"DEM-traced divergence of the relict Tigris belt sits 15 km from the Adhaim outlet, joining Ziegler's confluence and Kawakami's ancient-bed proposals"},
{"id":"T1-C3","name":"Irisagrig (CIGS point / Tall Warish)","lat":32.1529,"lon":45.3689,"radius_km":5,"feature_size_m":500,"signature":"low 2-4 m mound field pock-marked by looting pits on NW-SE relict levee","s2_visible":true,"dem_visible":true,"significance":6,"novelty":"PROPOSED","confidence":45,"looting_sensitive":true,"category":"lost royal city","one_line":"Looted Ur III city; CIGS point 72.8 km and Tall Warish 77.0 km from Umma vs Molina's 76 km; both on one levee"},
{"id":"T1-C4","name":"Itj-tawy, floodplain E of Lisht pyramids","lat":29.572,"lon":31.236,"radius_km":2,"feature_size_m":1500,"signature":"buried ~5 m under Nile alluvium; no surface expression; needs coring/ERT","s2_visible":false,"dem_visible":false,"significance":9,"novelty":"PROPOSED","confidence":50,"looting_sensitive":false,"category":"lost capital","one_line":"12th Dynasty capital: town centre beneath cultivation E of Amenemhat I and Senusret I pyramids; MK layer at 5 m in cores"},
{"id":"T1-C5","name":"Tarhuntassa at Turkmen-Karahoyuk (DEM-derived mound, verify identity)","lat":37.5710,"lon":32.7421,"radius_km":5,"feature_size_m":550,"signature":"round tell ~550 m, ~30 m high (24 ha >2 m), lower town >=80 ha, 2.9 km W of Cumra","s2_visible":true,"dem_visible":true,"significance":9,"novelty":"PROPOSED","confidence":25,"looting_sensitive":false,"category":"lost capital","one_line":"Massa/Osborne candidate (Hartapu inscription, LBA 60-80 ha, Kurunti-ziti seal); contested by Hawkins-Weeden (Hulaya frontier)"},
{"id":"T1-C6","name":"Musasir/Ardini at Mudjesir (Mdjeser) near Sidakan","lat":36.80,"lon":44.67,"radius_km":15,"feature_size_m":200,"signature":"temple terrace with column bases in mountain valley village; needs sub-metre imagery","s2_visible":false,"dem_visible":false,"significance":7,"novelty":"PROPOSED","confidence":45,"looting_sensitive":true,"category":"lost royal/temple city","one_line":"Haldi column bases and life-size statues reported at Mdjeser; approximate coordinate, replace with village point"},
{"id":"T1-C7","name":"Thinis at Girga / el-Birba","lat":26.3372,"lon":31.8930,"radius_km":6,"feature_size_m":1000,"signature":"buried under modern town and floodplain silt; no orbital signature","s2_visible":false,"dem_visible":false,"significance":9,"novelty":"PROPOSED","confidence":40,"looting_sensitive":false,"category":"lost capital","one_line":"First Dynasty capital; consensus Girga/el-Birba, 17 km from Abydos royal tombs"},
{"id":"T1-C8","name":"Wassukanni at Tell Fekheriye (Ras al-Ain)","lat":36.8415,"lon":40.0701,"radius_km":3,"feature_size_m":1000,"signature":"~1 km mound complex partly under Ras al-Ain town; DEM ~14 m","s2_visible":true,"dem_visible":true,"significance":8,"novelty":"PROPOSED","confidence":35,"looting_sensitive":true,"category":"lost capital","one_line":"Mittani capital candidate backed by Bonatz/Novak; NAA clay result and no texts argue against"},
{"id":"T1-C9","name":"Tarhuntassa southern alternative (Karaman-Karadag-Kizildag)","lat":37.40,"lon":33.15,"radius_km":25,"feature_size_m":600,"signature":"capital-size LBA mound (>20 ha) on Karaman plain or acropolis on volcanic flank","s2_visible":true,"dem_visible":true,"significance":9,"novelty":"PROPOSED","confidence":15,"looting_sensitive":false,"category":"lost capital","one_line":"If TKH is the Hulaya frontier, the capital lies south: Karadag/Kizildag Hartapu zone or Goksu valley"},
{"id":"T1-C10","name":"Agade at Samarra/Qadisiyya (Reade 2002)","lat":34.2001,"lon":43.8767,"radius_km":15,"feature_size_m":800,"signature":"buried beneath Abbasid Samarra ruin field; not separable","s2_visible":false,"dem_visible":false,"significance":10,"novelty":"PROPOSED","confidence":5,"looting_sensitive":true,"category":"lost capital","one_line":"Reade's Tigris-near-Qadisiyah/Samarra proposal; weak against Sippar-Khafajah itinerary"}
]
```
