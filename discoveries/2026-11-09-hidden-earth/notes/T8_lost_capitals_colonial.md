# T8 — Lost capitals of Africa, Asia and the Americas, and lost early-colonial sites

## Method (what you joined, what you searched; 5-10 lines)
- **Limits on this run (read first):** WebFetch could not resolve any host I tried (en.wikipedia.org, persee.fr), so every literature claim below comes from **WebSearch result pages and their snippets** (about 21 queries). The shared WebSearch budget then ran out. The Southeast Asian, Norse, Coronado/Quivira, Charlesfort, Takedda and Aksum leads were **not researched**; see Dead ends. I did not fill those gaps from memory.
- **Texts joined:** al-Bakri's two-town description of Ghana (1068); Ibn Battuta's Walata–Mali stages (24 days; Zaghari; Karsakhu; the Sansara river "about ten miles" from Mali); Columbus's *Diario* distances as quoted in secondary sources; the French account that puts Fort Caroline "six miles" from the river mouth; the DAI and Frobenius reports on Tié; Florida Museum work at En Bas Saline; First Colony Foundation reports on Site X; and Mabila proposals.
- **Physical geography (computed here, scripts in `data/T8/`):** Copernicus GLO-30 DEM and ESA WorldCover 2021 (10 m), read in small windows from public S3. I used them for radial terrain profiles, closed depressions, crude D8 flow accumulation, river and coastline traces, and built-up clusters (to check town coordinates). Distances and bearings use pyproj on WGS84 (`t8_math.py` → `t8_math_output.txt`).
- **Calibration:** the Koumbi Saleh coordinate comes from Pleiades 41177950 (repo copy `data/T1/pleiades/places.csv`). I checked the coordinates of Mao, Kangaba, Bamako, Ségou, Koulikoro, Oualata and Edenton against WorldCover built-up clusters; all matched within 1–2 km.
- **Leagues and miles used:** Roman mile 1.48 km; Arab mile 1.85–1.97 km; Columbus's league tested at both 5.56 and 5.92 km. These are my assumptions and are not sourced in this session.

## Candidates (ranked)

### C1. Ghana Empire royal town "al-Ghaba": low-plain sector 9–12 km NNW of Koumbi Saleh — NOVEL-SYNTHESIS
- Coordinates: **15.846, -8.017 (±7 km)**. This is the centre of an arc at bearings 300°–010° and distances 8.9–11.8 km from Koumbi Saleh (15.7657, -7.9687).
- What it would be / why it matters (significance **8**): the king's town of ancient Ghana, with palace and royal burial mounds. It has never been found.
- Evidence chain:
  1. al-Bakri (1068): "The city of Ghāna consists of two towns situated on a plain. The king's town is six miles distant from this one and bears the name of Al-Ghāba. Between these two towns are continuous habitations." https://en.wikipedia.org/wiki/Koumbi_Saleh ; translation in https://my.aui.ma/ICS/icsfs/Arab_Sources_on_Medieval_West_Africa.pdf?target=b1046592-a60d-4640-b35a-661239617e49
  2. The royal town, "with its large palace and burial mounds", has not been located: https://jwsr.pitt.edu/ojs/jwsr/article/download/286/298/371 ; https://kids.kiddle.co/Koumbi_Saleh
  3. Koumbi Saleh is the usual identification of the (Muslim) town of Ghana. Pleiades gives 15.765684, -7.968710: https://pleiades.stoa.org/places/41177950/osm-location-of-koumbi-saleh . Its western necropolis covers about 170 ha below the Columns Tomb (Capel et al. 2015): https://halshs.archives-ouvertes.fr/halshs-01454893v1/file/C.CAPEL%20et%20al%20%282015%29%20-%20THE%20END%20OF%20A%20HUNDRED-YEAR-OLD%20ARCHAEOLOGICAL%20RIDDLE.%20FIRST%20DATING%20OF%20THE%20COLUMNS%20TOMB%20OF%20KUMBI%20SALEH%20%28MAURITANIA%29.pdf
  4. **Text math:** 6 miles = 8.9 km (Roman mile) to 11.1–11.8 km (Arab mile). That gives a ring 8.9–11.8 km from Koumbi Saleh.
  5. **DEM (GLO-30, my analysis):** Koumbi Saleh sits on a low rise (about 258–260 m). Radial profiles show a lower plain at 233–245 m to the W–NW–N–NNE, out to 10–11 km, closed by dune ridges at 10–13 km. Mean ring elevation by sector is 237–242 m from W through N to NNE, and 279–294 m to the E and S. al-Bakri says "two towns on a plain" with continuous habitation between them. On this terrain, the royal town most plausibly lies on the same low plain, at bearings 300°–010° (possibly 270°–030°) inside the 8.9–11.8 km ring. Source: `data/T8/koumbi_ring.py`, `koumbi_prof.py`, `koumbi_ring_dem.json`.
  6. **Water (DEM closed depressions)** inside that sector: 137 ha, 7 m deep at 15.855, -8.008 (10.7 km, 337°); 112 ha, 2.2 m deep at 15.853, -7.963 (9.7 km, 4°); and a string of 46–92 ha depressions at 11–13.7 km, 331°–336° and 356°–7°. These are candidate seasonal ponds that could have supplied a town.
  7. **WorldCover 2021 "built-up" pixels** sit in a landscape that is about 89% grassland: 1.66 ha at 15.8239, -7.9902 (6.8 km, 340°, on the same plain) and tiny 0.1 ha clusters at 15.846, -8.019 (10.3 km, 329°), right at the arc centroid. For calibration, the largest built cluster near the site is 2.3 ha, 1.1 km SSW of the Pleiades point. Any of these may be modern hamlets; sub-metre imagery would settle it.
- Novelty check: I searched "al-Bakri Ghana two towns six miles royal town al-Ghaba location unknown Koumbi Saleh" and "Koumbi Saleh surroundings tumuli survey satellite imagery royal town". Results say the royal town has not been found. One low-reliability source (https://grokipedia.com/page/Koumbi_Saleh) reports a view that Koumbi Saleh itself is al-Ghaba. Another thread moves the capital to the Mema or Lakes region (El Oualadji tumuli; https://link.springer.com/article/10.1007/s10814-024-09201-w per the search summary). I found no published direction or sector for al-Ghaba. The label is **provisional**: I could not read Berthier's monograph or Thomassey & Mauny 1951.
- Orbital signature: a ruin field of perhaps tens of hectares made of low (1–3 m) mud-brick or stone-rubble mounds, lighter in tone than the surrounding grass, with burial mounds perhaps 10–30 m across (sizes are my analogy, not sourced). **S2: marginal at best. DEM: no.** Dune relief in the 30 m DEM reaches 27 m above the 1.5 km median, and Koumbi Saleh itself (+11 m) does not stand out from the dunes. The site needs **sub-metre imagery**. There is no canopy, so lidar is not required.
- Biggest reason it could be wrong: the identification of Koumbi Saleh as Ghana is disputed. Kritzinger argues it is Awdaghost (https://en.wikipedia.org/wiki/Koumbi_Saleh). Al-Bakri's "6 miles" may also refer to a different twin site. And al-Idrisi reports a new palace built in 510 AH, which implies the royal seat moved.
- Confidence: **10**

### C2. Njimi, first capital of Kanem = Tié, about 45 km east of Mao, Chad — PROPOSED
- Coordinates: **14.121, 15.729 (±8 km)**. This is my own derivation: Mao, checked against its WorldCover built cluster at 14.1215, 15.3122, plus 45 km on bearing 090°. The 40–50 km range spans 15.683–15.775 E.
- What it would be / why it matters (significance **8**): the Sefuwa royal seat of Kanem from the 11th to the 14th century, unlocated since the 18th century.
- Evidence chain:
  1. Tié/Ndjimi is the largest fired-brick site in Kanem, "about 45 km east of Mao" (Frobenius Institute exhibition brochure): https://frobenius-institut.de/images/stories/Ausstellungen/Kanem-Bornou/Broschure%20Tschad%20DS_web.pdf
  2. It is a fired-brick enclosure of about 3.2 ha at the centre of a compact cluster of eleven smaller sites in central Kanem, "most probably the long-sought Kanem capital Njimi". Lebeuf's Njimié likely corresponds to both Urvoy's Njimi and Bivar's Tié. https://www.tandfonline.com/doi/abs/10.1080/0067270X.2020.1868752 ; https://www.researchgate.net/publication/338039885_The_Lake_Chad_region_as_a_crossroads_an_archaeological_and_oral_historical_research_project_on_early_Kanem-Borno_and_its_intra-African_connections
  3. Local informants say the Tié area was once called **Cimi-Ye / Njimi-ye**. This toponym evidence is independent of the archaeology: https://www.researchgate.net/publication/347483517_Archaeological_research_at_Tie_Kanem_Chad_excavations_on_Mound_1Recherches_archeologiques_a_Tie_Kanem_Tchad_fouilles_du_monticule_1
  4. Luminescence and radiocarbon dates place the fired-brick elite sites in the 11th–14th centuries, the Njimi period: https://link.springer.com/article/10.1007/s10437-025-09611-1 ; DAI exhibition report: https://www.dainst.blog/entangled-africa/en/report_2025_01/
  5. A secondary source reports more than 50 fired-brick sites within 25 km of Tié, none larger than 3 ha: http://thedreamvariation.blogspot.com/2025/11/searching-for-njimi-and-medieval-kanem.html
  6. **Text check (tension):** Ibn Sa'id puts Matan "at an angle of the lake, 51° longitude" with Djimi, the capital, south of it (https://www.africanhistoryextra.com/p/a-forgotten-african-empire-the-history). Tié lies east of the lake's northern basin, not south of a lake-shore town. I cannot convert Ibn Sa'id's longitude system without more anchor points, so this is unresolved rather than a refutation.
- Novelty check: I searched "Njimi capital of Kanem location", "Tié Kanem Njimi", and "Tié km from Mao". The DAI and Frobenius team (Magnavita, Bouimon and others) have already proposed Tié. The evidence converges on their site. My only addition is the coordinate derivation from "45 km east of Mao".
- Orbital signature: a 3.2 ha enclosure (about 180 m on a side if square) with reddish fired-brick rubble mounds on pale sandy grassland. **S2: marginal yes** (about 18×18 pixels). **DEM: no.** Sub-metre imagery would pin down the enclosure walls, and the 11 satellite sites around it make a recognisable cluster.
- Biggest reason it could be wrong: my coordinate is "about 45 km" at an assumed due-east bearing, so the enclosure could be up to about 8 km away. Njimi may also have been one of several successive royal sites.
- Confidence: **60** that Tié is Njimi; the position radius stays at 8 km.

### C3. La Navidad (Columbus's fort, 1492) at En Bas Saline, Limonade, Haiti — PROPOSED
- Coordinates: **19.725, -72.125 (±2.5 km)**. I could not read a published coordinate for En Bas Saline. I placed it on the land strip behind the coastal settlement of Bord de Mer de Limonade, which I traced in WorldCover, because a local source puts En Bas Saline in Bord de Mer.
- What it would be / why it matters (significance **8**): the first European settlement in the Americas.
- Evidence chain:
  1. En Bas Saline is thought to be the main town of the cacique Guacanagarí, where La Navidad was set up. A large burned structure on a central mound yielded nearly all the European finds (a lead musket ball, Spanish pottery, rat and pig bones), and radiocarbon dates show it stood in 1492. The Florida Museum calls it "the most likely candidate": https://www.floridamuseum.ufl.edu/histarch/research/haiti/en-bas-saline/ ; https://ufdcimages.uflib.ufl.edu/AA/00/06/19/61/00363/11-41.pdf
  2. No conclusive evidence fixes the fort, and none of its timber has been securely identified: https://www.yahoo.com/news/world/articles/mystery-la-navidad-first-spanish-071002700.html
  3. The local source placing En Bas Saline in the Bord de Mer district of Limonade: https://haiti.fandom.com/wiki/Ville_de_Limonade
  4. **Text math:** the *Diario* puts the village 1.5 leagues from the wreck (as quoted in https://archaeologymysteries.com/2019/02/13/where-is-the-santa-maria-the-ship-of-columbus/ ; https://eathealthy365.com/the-final-voyage-what-really-happened-to-the-santa-maria/). The ship lay about 1 league from Picolet Point (https://www.history.com/articles/christopher-columbus-ships). Diario position fixes put the grounding a few km east of Cap-Haïtien (https://en.wikipedia.org/wiki/Santa_Mar%C3%ADa_(ship)).
  5. **Geometry (mine):** Picolet Point, the NE tip of the Cap-Haïtien headland in WorldCover, is at about 19.783, -72.195. It lies 9.75 km at 131° from En Bas Saline. A circle of 1 league around Picolet (5.56–5.92 km) and a circle of 1.5 leagues around En Bas Saline (8.3–8.9 km) meet offshore at **19.798–19.804, -72.143**. That point is about 5.5 km east of Picolet and about 5 km off the Limonade coast, which fits "a few km east of Cap-Haïtien" on the outer reef. The other intersection falls on land and is rejected. So the three independent distance statements agree with En Bas Saline being the village. A by-product is a **Santa María search box at 19.80, -72.143 (±2 km)**. It is underwater and has no orbital signature.
- Novelty check: I searched "La Navidad fort location unknown En Bas Saline", "Deagan ... burned structure ... league and a half" and the Diario distances. William Hodges proposed En Bas Saline in 1977, followed by Deagan; Morison's reef identification did not come up. A 2014 wreck claim by Barry Clifford, about 4 km from En Bas Saline, appears only in https://grokipedia.com/page/La_Navidad and is unverified. The distance geometry converges on the already-proposed site.
- Orbital signature: a large Taíno town of low middens and mounds around a central mound. The fort is a small structure of unknown size. **S2: no. DEM: no.** The site needs lidar or GPR and excavation. It is under pressure from looting and building: https://www.mdpi.com/2571-9408/3/3/41
- Biggest reason it could be wrong: the fort may have stood on the shore, apart from the village. The mangrove coast has moved since 1492. Columbus's league is uncertain, and my En Bas Saline coordinate is approximate.
- Confidence: **55**

### C4. Mali Empire capital, "Sansara = Sankarani" reading: the Niger–Sankarani wedge opposite Kangaba — PROPOSED
- Coordinates: **11.88, -8.41 (±12 km)**. The wider band extends south to about 11.4 N if the river was crossed further upstream; that case needs ±30 km.
- What it would be / why it matters (significance **9**): the city Ibn Battuta visited in 1352–53, the political centre of the Mali Empire.
- Evidence chain:
  1. Ibn Battuta reached a river called the Sansara, "about ten miles from Malli", and crossed it by ferry. The whole journey from Iwalatan took 24 days "travelling rapidly", with Zaghari 10 days out: https://orias.berkeley.edu/node/176 ; http://faculty.buffalostate.edu/oroszkj/Global%20I/Ibn%20Batuta%20on%20Mali.pdf ; http://www.the153club.org/battuta.html
  2. Dunn's index equates the Sansara with the Sankarani: https://bookreadfree.com/527778/12960368.amp . Since the 1920s, attention has focused on the area near the Sankarani: https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/midfourteenth-century-capital-of-mali/ACD0593AB1E1771CA663A7D4D76C529E
  3. Niani (Guinea) lies on the Sankarani's left bank (https://www.britannica.com/place/Niani) and has been rejected as the capital ("Niani Redux": https://www.academia.edu/3442795/Niani_redux_a_final_rejection_of_the_identification_of_the_site_of_Niani_Republic_of_Guinea_with_the_capital_of_the_kingdom_of_Mali). Dakadjalan, Niani and Kangaba are the three main candidates: https://fr.wikipedia.org/wiki/Empire_du_Mali ; Conrad treats Dakadjalan as the first capital: https://fr.wikipedia.org/wiki/Dakadjalan
  4. **Geography (mine, WorldCover water trace):** the Sankarani, flowing north through Sélingué, joins the Niger at about **12.01, -8.33**. Kangaba (built cluster 11.940, -8.418) is 12 km from the confluence.
  5. **Text math:** 10 miles is 14.8 km (Roman) to 19.7 km (Arab). The reading assumes a traveller came up the Niger's right bank and crossed the Sankarani near its mouth. The capital would then lie 15–20 km SW of the crossing, inside the wedge between the two rivers: 11.84–11.92 N, -8.38 to -8.47 (`t8_math_output.txt`). That is 2–8 km from Kangaba, mostly across the Niger from it, so it **converges on the already-proposed Kangaba area**. On the same logic Niani, less than 5 km from the Sankarani, is too close to the river to sit "ten miles" beyond a Sansara crossing.
  6. Itinerary time: Walata (17.300, -7.025) to this point is 617 km great-circle, or about 770 km assuming a route 1.25 times longer. That needs 32 km/day for 24 days. "Travelling rapidly" makes this possible, but the timing does not separate C4 from C5.
- Novelty check: the searches above, plus "Ibn Battuta Sansara identification Sankarani". The area is already proposed (the Sankarani focus since the 1920s, Kangaba as a candidate). The crossing-geometry point is my derivation from published premises.
- Orbital signature: a Sudanic town of earth architecture, probably mound(s) covering tens of hectares on a floodplain margin. **S2: no. DEM: unlikely** unless there are tells several metres high. Sub-metre imagery or lidar is needed. The region has heavy terracotta looting, so treat locations as sensitive.
- Biggest reason it could be wrong: the Sansara may not be the Sankarani. Ibn Battuta also never mentions crossing the Niger itself. And Fauvelle argues that the "capital" may not have been a fixed place.
- Confidence: **15**

### C5. Mali Empire capital, Hunwick's Niger left-bank corridor between Bamako and Ségou — PROPOSED
- Coordinates: **13.05, -7.10 (±70 km)**. This is the corridor midpoint; the corridor runs about 200 km from Bamako (12.652, -7.999) to Ségou (13.429, -6.254).
- What it would be / why it matters (significance **9**): same as C4.
- Evidence chain:
  1. Hunwick (1973) used Ibn Battuta's route to put the 1352 capital on the left bank of the Niger between Ségou and Bamako. He argued this suited a cavalry state drawing on the savanna and Sahel, and suggested the Sansara would have been fordable in winter: https://www.semanticscholar.org/paper/The-mid-fourteenth-century-capital-of-Mali-Hunwick/9332e08fd0fb0e0fbb5c62a4b96acf3512b4206b ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/midfourteenth-century-capital-of-mali/ACD0593AB1E1771CA663A7D4D76C529E
  2. MacDonald et al. on the Pays Dô support Hunwick's Niger-core view and link the Sorotomo mound to the Mali Empire: https://discovery.ucl.ac.uk/id/eprint/10063394/8/MacDonald_etal_PaysDo_revised&submitted.pdf
  3. Itinerary time: Walata to the corridor is 436–525 km great-circle, or 23–27 km/day over 24 days at 1.25 sinuosity. That is a more ordinary pace than C4 needs.
  4. **Contradiction mining (mine):** the corridor lies 80–275 km from the Sankarani confluence. Hunwick's location and "Sansara = Sankarani" therefore **cannot both be true**. The corridor needs the Sansara to be another stream within about 20 km of the city. That conflict is the cheapest test of C4 against C5.
- Novelty check: Hunwick proposed this corridor; Meillassoux's earlier Falémé/Gambia placement was rejected by Hunwick (http://www.the153club.org/battuta.html). Label: PROPOSED.
- Orbital signature: as for C4. **S2: no. DEM: no.** The corridor is too long to survey without a narrower text constraint.
- Biggest reason it could be wrong: the corridor is about 200 km long and has no fixed point; no excavated 14th-century city there has been tied to the capital.
- Confidence: **20** for the corridor; under 5 for any single point.

### C6. Fort Caroline (French, 1564) — St Johns Bluff vicinity, Jacksonville, Florida — PROPOSED
- Coordinates: **30.384, -81.497 (±3 km)**
- What it would be / why it matters (significance **7**): the first French colony in what is now the USA, destroyed by Menéndez in 1565.
- Evidence chain:
  1. The NPS says the exact site is unknown. The memorial sits on the bluff that scholars generally accept as near the fort, "though probably not the exact location": https://www.nps.gov/articles/ftcaroline.htm
  2. Sources put the fort on the south side of the St Johns, about six miles from the mouth: https://en.wikipedia.org/wiki/Fort_Caroline ; http://www.bibleorigins.net/FortCarolineSaintJohnsBluffFlorida.html
  3. **Geometry (mine, WorldCover):** the river mouth is at about 30.400, -81.395. The forested bluff block on the south bank spans 30.376–30.386 N, -81.52 to -81.48. Mouth to bluff is 10.0 km at 260°, which is **6.2 statute miles** in a straight line. The text distance therefore converges on the traditional bluff.
  4. Alternatives: Spanish Point, south of St Johns Bluff (Gissendaner 1996; https://npshistory.com/publications/foca/fleck-2017.pdf). An eroded site now in the river (Davis 1911, and Fairbanks's 1868 speculation; https://sciencythoughts.blogspot.com/2022/06/searching-for-fort-caroline.html). The Altamaha mouth in Georgia or the St Marys River (Spring and Crowe; https://www.sciencedaily.com/releases/2014/02/140221111218.htm ; https://medcraveonline.com/JHAAS/the-location-of-fort-caroline-in-ancient-maps.html). A 2014 claim of an undisclosed St Johns location, withheld "to prevent tampering and looting": https://904happyhour.com/article/major-ft-caroline-discovery
- Novelty check: I searched "Fort Caroline location still unknown candidates ... Altamaha" and "Laudonniere ... Spanish Point ... erosion". Every point I can derive has already been proposed.
- Orbital signature: a small earth-and-timber fort. If it eroded into the channel, nothing survives on land. **S2: no. DEM: no.** Lidar under the bluff forest, or sub-bottom profiling of the adjacent channel, would be needed.
- Biggest reason it could be wrong: the bank has eroded and the river has been dredged, so the site may be gone. "Six miles" may have been measured along the 1564 channel. The Georgia hypothesis has not been tested by excavation.
- Confidence: **40** for the vicinity.

### C7. Roanoke "Lost Colony" — Site X, Bertie County shore of the western Albemarle Sound — PROPOSED
- Coordinates: **36.003, -76.710 (±4 km)**. This is approximate. I traced the Bertie shoreline at the Chowan–Albemarle junction in WorldCover. My placement at the mouth of Salmon Creek is from memory and **was not verified in this session**. I read no published exact Site X coordinate.
- What it would be / why it matters (significance **7**): where some of the 1587 colonists went.
- Evidence chain:
  1. A patch on John White's *Virginea Pars* map hides a fort symbol, found in 2012, probably marking a planned second settlement: https://www.pbsnc.org/blogs/science/lost-colony-split/
  2. Site X was designated in 2015 and Site Y lies on county land. Surrey-Hampshire Border ware has otherwise been found in North America only at Roanoke Island and Jamestown. There is "no smoking gun", and less than a tenth of the site has been examined: https://journalnow.com/news/state/artifacts-possibly-from-lost-colony-found-in-bertie-county/article_d9dd3496-f154-5cc7-98e7-94c69254cca2.html ; https://www.dailyadvance.com/news/local/bertie-dig-sites-may-show-where-lost-colonists-moved/article_40f543be-23f9-11ef-8264-2319e0fa51b0.html ; http://www.co.bertie.nc.us/projects/2019/tgow/Discovery%20shows%20Lost%20Colony%20survivors%20lived%20inland%20FINAL%20Oct%2015%202020.pdf
  3. A 1,000-acre tract is preserved for future study: https://www.foxnews.com/us/land-deal-will-preserve-site-linked-to-lost-colony-mystery
  4. Geometry: Fort Raleigh (approx. 35.938, -75.712) to Site X is about 90 km at 275°, or 56 statute miles in a straight line. The often-quoted "fifty miles into the main" was **not re-verified** here and carries no weight in this assessment.
- Novelty check: I searched "Roanoke Lost Colony Site X Bertie County ... latest". The First Colony Foundation proposed and is excavating the site.
- Orbital signature: a small subsurface artifact scatter with no surface relief. **S2: no. DEM: no.** No orbital method applies.
- Biggest reason it could be wrong: the pottery could reflect later trade rather than the colonists, and the colonists may instead have gone to Croatoan (Hatteras).
- Confidence: **35**

### C8. Mabila (de Soto's battle town, 1540) — the Alabama–Tombigbee "Forks", southern Clarke County, Alabama; alternative Marengo County — PROPOSED
- Coordinates: **31.15, -87.95 (±20 km)** for the Forks. Alternative: **32.25, -87.80 (±30 km)**, Marengo County. Both are approximate placements by me; WorldCover at 600 m could not trace these forested rivers.
- What it would be / why it matters (significance **7**): the largest battle between Europeans and Native Americans on what is now US soil.
- Evidence chain:
  1. Mabila was Tuskaloosa's fortified town. Its location has been debated for centuries, and "southwest of present-day Selma" is one possibility: https://en.wikipedia.org/wiki/Mabila
  2. One researcher calls the upper Mobile Delta "Forks" region of southern Clarke County the most promising area: https://archeologyink.com/mapping-the-de-soto-route-through-south-alabama-in-the-chroniclers-own-words/ ; https://archeologyink.com/the-battle-of-mabila-recent-archeological-testing-in-the-forks/
  3. The University of West Alabama claimed Marengo County in December 2021. A critique notes that no hearths, pits, Spanish burials or structures have been found there: https://archeologyink.com/the-battle-site-of-mabila-a-critique-of-the-university-of-west-alabama-claim/
  4. Taskigi Mound in Elmore County identifies the Province of Tuskaloosa, not the battle site: https://en.wikipedia.org/wiki/Taskigi_Mound
  5. Geometry: Selma (approx. 32.407, -87.021) to the Forks is 165 km at 213°; Selma to Marengo is 75 km at 257°. The two claims are 123 km apart, so nothing converges. The search budget ran out before I could retrieve the chroniclers' league and day counts.
- Novelty check: both zones are already proposed.
- Orbital signature: the burned remains of a palisaded town of perhaps a few hectares under forest. **S2: no. DEM: no.** Lidar plus metal-detecting for 16th-century Spanish iron would be needed.
- Biggest reason it could be wrong: both claims rest on route reconstructions, and neither has produced the battle signature (burned palisade, mass Spanish artifacts).
- Confidence: **15**

## Dead ends (things you checked that did not pan out, 1 line each)
- **Not researched because the shared WebSearch budget was exhausted and WebFetch was blocked:** Hóp and other Norse sites; Vyadhapura (Funan); the Srivijaya capital debate; Majapahit-era towns; Champa citadels; Takedda; Mogadishu-hinterland towns; Aksumite outposts; Coronado's camps and Quivira's council circles; de Soto camps other than Mabila; Charlesfort. Nothing is claimed for these.
- The "al-Ghaba = the grove" vegetation proxy: WorldCover tree cover in the 9–12 km ring is about 0.06%. The nearest tree-and-water patch is a pond 17 km NE (15.883, -7.866), beyond 6 miles even in Arab miles. No signal.
- Detecting mounds near Koumbi Saleh in the 30 m DEM: dune residual relief up to 27 m. Koumbi Saleh itself (+11 m) does not stand out, so 30 m elevation data cannot find an earth-built royal town here.
- Flow accumulation near Koumbi Saleh: no channel draining more than 20 km² inside 14 km, so no wadi anchors al-Idrisi's "closer to the river".
- Ibn Battuta's 24-day figure: every candidate from Ségou to Niani needs 23–35 km/day, so the timing does not discriminate.
- Ibn Sa'id's "51° longitude" for Matan/Njimi: it cannot be converted without more anchor points in his system, so it is unresolved.
- Tracing the Mabila Forks rivers in WorldCover at 600 m: the rivers are hidden by forest, so no geometry was possible.

## Sources
Literature (all seen in WebSearch results this session):
- https://en.wikipedia.org/wiki/Koumbi_Saleh
- https://my.aui.ma/ICS/icsfs/Arab_Sources_on_Medieval_West_Africa.pdf?target=b1046592-a60d-4640-b35a-661239617e49
- https://jwsr.pitt.edu/ojs/jwsr/article/download/286/298/371
- https://kids.kiddle.co/Koumbi_Saleh
- https://grokipedia.com/page/Koumbi_Saleh (low reliability)
- https://halshs.archives-ouvertes.fr/halshs-01454893v1/file/C.CAPEL%20et%20al%20%282015%29%20-%20THE%20END%20OF%20A%20HUNDRED-YEAR-OLD%20ARCHAEOLOGICAL%20RIDDLE.%20FIRST%20DATING%20OF%20THE%20COLUMNS%20TOMB%20OF%20KUMBI%20SALEH%20%28MAURITANIA%29.pdf
- https://link.springer.com/article/10.1007/s10814-024-09201-w
- https://www.researchgate.net/publication/351359017_Monumental_funerary_landscapes_of_Dhar_Tagant_south-eastern_Mauritania_Towards_ethical_satellite_remote_sensing_in_the_West_African_Sahel
- https://pleiades.stoa.org/places/41177950/osm-location-of-koumbi-saleh
- https://frobenius-institut.de/images/stories/Ausstellungen/Kanem-Bornou/Broschure%20Tschad%20DS_web.pdf
- https://www.tandfonline.com/doi/abs/10.1080/0067270X.2020.1868752
- https://www.researchgate.net/publication/338039885_The_Lake_Chad_region_as_a_crossroads_an_archaeological_and_oral_historical_research_project_on_early_Kanem-Borno_and_its_intra-African_connections
- https://www.researchgate.net/publication/347483517_Archaeological_research_at_Tie_Kanem_Chad_excavations_on_Mound_1Recherches_archeologiques_a_Tie_Kanem_Tchad_fouilles_du_monticule_1
- https://link.springer.com/article/10.1007/s10437-025-09611-1
- https://www.dainst.blog/entangled-africa/en/report_2025_01/
- http://thedreamvariation.blogspot.com/2025/11/searching-for-njimi-and-medieval-kanem.html
- https://www.africanhistoryextra.com/p/a-forgotten-african-empire-the-history
- https://cambridge.org/core/journals/journal-of-african-history/article/old-kanuri-capitals/6C6F43F5C8828762041A84F5F30E4C3F
- https://en.wikipedia.org/wiki/Njimi
- https://www.floridamuseum.ufl.edu/histarch/research/haiti/en-bas-saline/
- https://ufdcimages.uflib.ufl.edu/AA/00/06/19/61/00363/11-41.pdf
- https://www.yahoo.com/news/world/articles/mystery-la-navidad-first-spanish-071002700.html
- https://haiti.fandom.com/wiki/Ville_de_Limonade
- https://www.history.com/articles/christopher-columbus-ships
- https://en.wikipedia.org/wiki/Santa_Mar%C3%ADa_(ship)
- https://archaeologymysteries.com/2019/02/13/where-is-the-santa-maria-the-ship-of-columbus/
- https://eathealthy365.com/the-final-voyage-what-really-happened-to-the-santa-maria/
- https://grokipedia.com/page/La_Navidad (low reliability)
- https://www.mdpi.com/2571-9408/3/3/41
- https://discovery.ucl.ac.uk/id/eprint/10198156/
- https://orias.berkeley.edu/node/176
- http://faculty.buffalostate.edu/oroszkj/Global%20I/Ibn%20Batuta%20on%20Mali.pdf
- http://www.the153club.org/battuta.html
- https://bookreadfree.com/527778/12960368.amp
- https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/midfourteenth-century-capital-of-mali/ACD0593AB1E1771CA663A7D4D76C529E
- https://www.semanticscholar.org/paper/The-mid-fourteenth-century-capital-of-Mali-Hunwick/9332e08fd0fb0e0fbb5c62a4b96acf3512b4206b
- https://www.academia.edu/3442795/Niani_redux_a_final_rejection_of_the_identification_of_the_site_of_Niani_Republic_of_Guinea_with_the_capital_of_the_kingdom_of_Mali
- https://www.britannica.com/place/Niani
- https://fr.wikipedia.org/wiki/Empire_du_Mali
- https://fr.wikipedia.org/wiki/Dakadjalan
- https://discovery.ucl.ac.uk/id/eprint/10063394/8/MacDonald_etal_PaysDo_revised&submitted.pdf
- https://www.nps.gov/articles/ftcaroline.htm
- https://en.wikipedia.org/wiki/Fort_Caroline
- http://www.bibleorigins.net/FortCarolineSaintJohnsBluffFlorida.html
- https://npshistory.com/publications/foca/fleck-2017.pdf
- https://sciencythoughts.blogspot.com/2022/06/searching-for-fort-caroline.html
- https://www.sciencedaily.com/releases/2014/02/140221111218.htm
- https://medcraveonline.com/JHAAS/the-location-of-fort-caroline-in-ancient-maps.html
- https://904happyhour.com/article/major-ft-caroline-discovery
- https://www.pbsnc.org/blogs/science/lost-colony-split/
- https://journalnow.com/news/state/artifacts-possibly-from-lost-colony-found-in-bertie-county/article_d9dd3496-f154-5cc7-98e7-94c69254cca2.html
- https://www.dailyadvance.com/news/local/bertie-dig-sites-may-show-where-lost-colonists-moved/article_40f543be-23f9-11ef-8264-2319e0fa51b0.html
- http://www.co.bertie.nc.us/projects/2019/tgow/Discovery%20shows%20Lost%20Colony%20survivors%20lived%20inland%20FINAL%20Oct%2015%202020.pdf
- https://www.foxnews.com/us/land-deal-will-preserve-site-linked-to-lost-colony-mystery
- https://en.wikipedia.org/wiki/Mabila
- https://archeologyink.com/mapping-the-de-soto-route-through-south-alabama-in-the-chroniclers-own-words/
- https://archeologyink.com/the-battle-of-mabila-recent-archeological-testing-in-the-forks/
- https://archeologyink.com/the-battle-site-of-mabila-a-critique-of-the-university-of-west-alabama-claim/
- https://en.wikipedia.org/wiki/Taskigi_Mound

Data (read directly; scripts in `discoveries/2026-11-09-hidden-earth/data/T8/`):
- Copernicus GLO-30 DEM: https://copernicus-dem-30m.s3.amazonaws.com/ (tiles N15W008, N15W009)
- ESA WorldCover 2021 v200: https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ (tiles N15W009, N09W009, N12W009, N12E015, N18W075, N18W072, N30W084, N33W078, N36W078, N30W090)
- Outputs: `koumbi_ring_dem.json`, `t8_math_output.txt`

```json
[
 {"id":"T8-C1","name":"Ghana royal town al-Ghaba: NNW low-plain sector 9-12 km from Koumbi Saleh","lat":15.846,"lon":-8.017,"radius_km":7,"feature_size_m":500,"signature":"Ruin field of low (1-3 m) earth/stone-rubble mounds, lighter tone than grassland, possible tumuli 10-30 m; check WorldCover built pixels at 15.8239,-7.9902 and 15.846,-8.019 and depressions at 15.855,-8.008 / 15.853,-7.963","s2_visible":false,"dem_visible":false,"significance":8,"novelty":"NOVEL-SYNTHESIS","confidence":10,"looting_sensitive":true,"category":"lost capital","one_line":"al-Bakri's 6 miles (8.9-11.8 km) + the DEM low plain (233-245 m) NW-N of Koumbi Saleh + closed-depression water points converge on an arc centred at 15.846,-8.017."},
 {"id":"T8-C2","name":"Njimi (Kanem capital) = Tie fired-brick enclosure","lat":14.121,"lon":15.729,"radius_km":8,"feature_size_m":180,"signature":"3.2 ha reddish fired-brick enclosure and rubble mounds amid ~11 smaller satellite sites on pale sandy grassland","s2_visible":true,"dem_visible":false,"significance":8,"novelty":"PROPOSED","confidence":60,"looting_sensitive":true,"category":"lost capital","one_line":"DAI/Frobenius identification (largest brick site, local name Njimi-ye, 11th-14th c. dates) placed about 45 km E of Mao (WorldCover-verified) gives 14.121,15.729."},
 {"id":"T8-C3","name":"La Navidad (1492) at En Bas Saline, Limonade, Haiti","lat":19.725,"lon":-72.125,"radius_km":2.5,"feature_size_m":500,"signature":"Large Taino town of low middens/mounds with a central mound (burned 1492 structure); fort not resolvable from orbit","s2_visible":false,"dem_visible":false,"significance":8,"novelty":"PROPOSED","confidence":55,"looting_sensitive":true,"category":"lost colonial site","one_line":"Diario 1.5 leagues to the village + 1 league from Picolet put the Santa Maria wreck offshore at ~19.80,-72.143, consistent with En Bas Saline (Deagan's 1492 burned structure) as La Navidad."},
 {"id":"T8-C4","name":"Mali capital, Sansara=Sankarani reading: Niger-Sankarani wedge opposite Kangaba","lat":11.88,"lon":-8.41,"radius_km":12,"feature_size_m":1000,"signature":"Earth-built town mounds on a floodplain margin; needs sub-metre/lidar","s2_visible":false,"dem_visible":false,"significance":9,"novelty":"PROPOSED","confidence":15,"looting_sensitive":true,"category":"lost capital","one_line":"If the Sansara is the Sankarani (confluence 12.01,-8.33), 'ten miles' beyond a crossing near its mouth lands 15-20 km SW in the wedge, 2-8 km from the Kangaba candidate."},
 {"id":"T8-C5","name":"Mali capital, Hunwick Niger left-bank corridor Bamako-Segou","lat":13.05,"lon":-7.10,"radius_km":70,"feature_size_m":1000,"signature":"Earth-built town mounds; corridor too long for orbital search without a narrower constraint","s2_visible":false,"dem_visible":false,"significance":9,"novelty":"PROPOSED","confidence":20,"looting_sensitive":true,"category":"lost capital","one_line":"Hunwick's corridor fits a 23-27 km/day 24-day itinerary but is 80-275 km from the Sankarani, so it needs the Sansara to be another stream; the two readings cannot both hold."},
 {"id":"T8-C6","name":"Fort Caroline (1564), St Johns Bluff vicinity","lat":30.384,"lon":-81.497,"radius_km":3,"feature_size_m":100,"signature":"Small earth-and-timber fort, possibly eroded into the channel; no orbital signature","s2_visible":false,"dem_visible":false,"significance":7,"novelty":"PROPOSED","confidence":40,"looting_sensitive":true,"category":"lost colonial site","one_line":"'South side, six miles from the mouth' measures to 6.2 mi (10.0 km at 260 deg) from the WorldCover river mouth to the bluff forest, matching the traditional (NPS) vicinity; Altamaha/St Marys alternatives are untested."},
 {"id":"T8-C7","name":"Roanoke Lost Colony Site X, Bertie County","lat":36.003,"lon":-76.710,"radius_km":4,"feature_size_m":200,"signature":"Subsurface artifact scatter; no surface relief","s2_visible":false,"dem_visible":false,"significance":7,"novelty":"PROPOSED","confidence":35,"looting_sensitive":true,"category":"lost colonial site","one_line":"Virginea Pars patch fort symbol + Border-ware finds at Site X/Y on the western Albemarle shore, about 90 km (56 mi) W of Fort Raleigh; coordinate approximate."},
 {"id":"T8-C8","name":"Mabila (1540) battle town, Alabama-Tombigbee Forks (alt. Marengo Co. 32.25,-87.80)","lat":31.15,"lon":-87.95,"radius_km":20,"feature_size_m":300,"signature":"Burned palisaded town under forest; needs lidar and metal detection","s2_visible":false,"dem_visible":false,"significance":7,"novelty":"PROPOSED","confidence":15,"looting_sensitive":true,"category":"lost colonial/contact site","one_line":"Two published claims (southern Clarke Co. Forks vs UWA Marengo Co.) lie 123 km apart; no convergence; battle signature not yet found at either."}
]
```
