# T9 — Dynamic Earth: new landscape features that may be unreported

## Method (what you joined, what you searched; 5-10 lines)
- **Constraints.** WebFetch could not reach mdpi.com or doaj.org (host blocked), and the shared WebSearch budget (200 per turn) ran out partway through. Everything below therefore comes from search-result snippets plus my **own Sentinel-2 L2A and Copernicus GLO-30 checks** from the shell. The checks used the public `sentinel-cogs` and `copernicus-dem-30m` buckets and read only small windows. Scripts are in `data/T9/scripts/` (`s2chip.py`, `newwater.py`, `gecscan.py`, `panel.py`) and outputs in `data/T9/out/`.
- **(a) GECs.** I built a calibration list of gas-emission craters from the Zolkos/Dvornikov and Bogoyavlensky tables (via snippets). I then tested whether 10 m Sentinel-2 can see a fresh GEC: I re-found the 2023 C22 "Doublet" crater about 230 m from C2, which gave me its coordinates and a formation window. I wrote a small "new dark pit + bright rim" change detector and checked it on C22, where it ranked C22 #2 of 45 blobs. I then ran it over a 20×20 km central-Yamal box for 2024→2025 and 2025→2026. It found no convincing new GEC; the top hits I inspected were cloud shadows or vegetation changes.
- **(b, c).** I joined seismic and landslide reporting (Eos Landslide Blog, USGS, Alaska Earthquake Center, CCTV/Al Jazeera) with my own S2 and DEM checks. For the August 2026 Langtang/Lhende ice–rock avalanche, two independent clues match a single point on the map. The first is the barrier-lake elevation of 2,950 m reported by CCTV. The second is the junction where the debris meets the main valley, which I picked from S2 imagery. The GLO-30 DEM gives 2,873–2,947 m at that junction, which is 12 km from Rasuwagadhi; CCTV said ">10 km from Gyirong Port". I then tested whether the lake still exists.
- **(d).** I used gap analysis against the Kavan et al. (2025) new-island inventory, which covers 2000–2020, plus the 2025 Prow Knob and Austfonna cases.
- **(e)** I could not research this because the search budget was exhausted; see Dead ends.
- **Coordinates.** Some coordinates for well-known features are marked "approx., from general geographic knowledge, not sourced". The lead should take the authoritative value from the cited event page.

## Candidates (ranked)

### C1. Central-Yamal GEC cluster: "where to look" Box A — PROPOSED (box = our synthesis)
- Coordinates: 70.06, 68.70 (±25 km). Bounding box: **69.93–70.20 N, 68.30–69.15 E** (S2 tiles 42WVC/42WWC). Inner priority boxes:
  - **A1** 70.13–70.16 N, 68.47–68.53 E, around C2/C22.
  - **A2** 69.95–70.00 N, 68.33–68.42 E, around C1 and C17. C17 was reported "close to three other craters including the Yamal crater"; I did not obtain its exact coordinates.
- What it would be / why it matters (significance 7): new GECs are explosive blowouts of up to about 25–70 m across. The cluster lies a few km from the Bovanenkovo field and the Bovanenkovo–Ukhta trunk gas pipeline; C1 formed only 3.5 km from the pipeline.
- Evidence chain:
  1. Calibration GECs (all KNOWN). Sources: the ResearchGate table of crater coordinates and the Zolkos et al. 2021 Table 2, both via search snippets.

     | ID | Lat | Lon | Formed |
     |---|---|---|---|
     | C1 (GEC-1) | 69.9711 | 68.3703 | Oct 2013 – Apr 2014 |
     | C2 (GEC-2) | 70.1446 | 68.4959 | Sep–Oct 2012 |
     | C9 (GEC-3) | 70.0625 | 69.0995 | Oct 2012 – Jun 2013 |
     | C3 (AntGEC, Gydan) | 69.7946 | 75.0350 | Sep 2013 |
     | C11 Seyakha | 70.302 | 71.746 | 28 Jun 2017 |

     https://www.researchgate.net/figure/Coordinates-of-the-gas-blowout-craters-on-the-Yamal-Peninsula_tbl1_341905295 ; https://www.mdpi.com/2076-3263/11/1/21 ; https://doi.org/10.3390/en14175345
  2. C17 formed 15 May – 9 Jun 2020 on a perennial heaving mound on the third marine terrace in central Yamal, near C1. https://www.researchgate.net/publication/349110798 ; https://ui.adsabs.harvard.edu/abs/2021Geosc..11...71B
  3. C22 "Doublet" formed in 2023, 230 m from C2, so GECs recur at the same spots. http://eng.arctica-ac.ru/article/700/
  4. Four of the roughly eight confirmed giant GECs (C1, C2, C9, C22, plus C17 per the press) sit inside this box of about 30 × 40 km. That is the strongest spatial prior available.
  5. Sources disagree on the total: "8 GECs", "17 as of 2020", and ">20, most recent August 2024" (CNN snippet, unverified). The numbering has reached at least C22, so the inventory is incomplete in public.
- Novelty check: I searched for 2024–2025 new Yamal craters and found nothing specific beyond C22. The August 2024 crater mentioned by CNN has no published location in my results.
  - My S2 scan of a 20×20 km window centred at 70.07, 68.55 (2025-08-18 vs 2026-08-18) found no convincing new pit; the top hits were cloud shadows.
  - The 2024-07-29 vs 2025-08-18 scan produced unverified single-pixel hits I did not inspect. The highest was 70.0559, 68.5975 (rim-brightening only, probably an artefact). Outputs are in `data/T9/out/scan_box1_*.txt`.
- Orbital signature: a dark pit 1–5 S2 pixels across with a bright ejecta ring up to ~100 m, appearing between two summer scenes. A water-filled pit in later years. A pre-event heaving mound may show in the DEM (2–6 m), but that is below GLO-30 reliability. S2-visible: yes (borderline, as C22 shows). DEM: no.
- Biggest reason it could be wrong: GECs are rare (about 1 per 1–2 years region-wide), and the next one may form anywhere on Yamal or Gydan.
- Confidence: 55 that the next GEC on Yamal forms in this box. 15 that one formed here in 2024–2026 and is still unreported.
- **Date window for the lead:** summer scenes 2024-07-29, 2025-08-18 and 2026-08-18 (tile 42WVC, orbit about 07:49 UTC).

### C2. C22 "Doublet" crater: S2-derived coordinates and formation window — KNOWN (coordinates are our derivation)
- Coordinates: **70.1460, 68.5002 (±0.05 km)**.
- What it would be / why it matters (significance 5): a calibration GEC formed in 2023 that shows 10 m Sentinel-2 can detect GECs.
- Evidence chain:
  1. Arctica-AC: C22 formed in 2023, 230 m from C2. http://eng.arctica-ac.ru/article/700/
  2. My S2 check found a dark-centred, bright-rimmed feature about 210–240 m NE of the published C2 coordinate.
     - Absent on 2022-08-01 (S2A_42WVC_20220801) and 2023-06-30.
     - Present on 2023-09-05 and 2024-07-29 (S2B_42WVC_20240729).
     - My change detector ranked it #2 of 45 blobs in a 6×6 km window.
     - Panels: `data/T9/out/c22_series.png`, `c2_zoom.png`.
- Novelty check: I found no published coordinates for C22 in search results; the location derived here is new to me.
- Orbital signature: pit about 20–40 m with an ejecta ring about 60–80 m. S2: yes (2–4 px). DEM: no.
- Biggest reason it could be wrong: a pre-existing pond lies about 80 m away and could be confused with the crater. Final identification needs the Arctica-AC figure or sub-metre imagery.
- Confidence: 75.
- **Formation window (S2): 2023-06-30 → 2023-09-05.**

### C3. Lhende Khola (Nepal–Tibet) 2026 barrier-lake dam site — KNOWN event; NOVEL-SYNTHESIS coordinates and status
- Coordinates: **28.334, 85.484 (±1 km)**. This is where the 26 Aug 2026 avalanche-debris tributary enters the main valley.
- What it would be / why it matters (significance 8): a transboundary landslide-dam hazard. The 26 Aug 2026 ice–rock avalanche and debris flow killed hundreds and destroyed Gyirong Port. Two "new lakes" were reported, one of them already overtopping on 27–28 Aug. Such lakes are absent from GLOF inventories, which list glacial lakes only.
- Evidence chain:
  1. Eos Landslide Blog gives 28.2765, 85.5194. USGS reports seismic energy equivalent to M5.2 and a second event about M4.2 three hours later. https://eos.org/thelandslideblog/26-august-2026-nepal-and-tibet ; https://www.usgs.gov/programs/landslide-hazards/science/2026-nepal-debris-avalanche-and-flash-flood
  2. CCTV via CNN: the barrier lies >10 km from Gyirong Port, and the lake is at 2,950 m, about 1,000 m above the port. Al Jazeera: the lake is near the Chhochen Khola / Purepu Tsangpo confluence on the Lhende system, and there are two lakes. https://www.cnn.com/2026/08/28/china/china-secondary-disaster-flood-lake-breach-intl-hnk ; https://www.aljazeera.com/news/2026/8/28/is-nepal-facing-another-devastating-flood-from-a-new-lake
  3. My S2 imagery (S2B_45RUM_20251021 vs S2B_45RUM_20261026) shows a fresh grey debris track running NW from the Langtang Lirung north-side ice to the main valley. The track meets the valley at about 28.334, 85.484. `data/T9/out/lhende_*_small.png`
  4. GLO-30 elevation at that junction is 2,873–2,947 m, and it is 12.1 km from Rasuwagadhi (DEM 1,873–1,994 m). Both match the CCTV figures (2,950 m; >10 km; about 1,000 m higher).
  5. Status test: with `newwater.py` over a 24×24 km window, no new water body ≥0.003 km² was present on 2026-09-28 or 2026-10-26. **The barrier lakes appear to have drained or breached by late September 2026.**
- Novelty check: news gives only a river confluence; I found no published coordinates for the dam and no report of the lake's fate.
- Orbital signature: a grey debris fan 0.5–1 km across choking the valley. While the lake existed, a lake of 0.1–0.5 km² upstream. S2: yes. DEM: the dam is about 10–40 m high, which is marginal for GLO-30 (2021 epoch, so pre-event anyway).
- Biggest reason it could be wrong: the Nepal-side "much larger" lake may lie on a different branch outside my window. The SCL cloud mask may also have hidden water.
- Confidence: 70 for the dam location; 60 that no lake persists.
- **Window:** before 2025-10-21; after 2026-08-28 (cloudy), 2026-09-28 and 2026-10-26.

### C4. Langtang Lirung north-face ice–rock avalanche (26 Aug 2026) — KNOWN (seismically detected)
- Coordinates: 28.2765, 85.5194 (±2 km). Source per Eos; on S2 the track runs about 28.29, 85.51 → 28.334, 85.484.
- What it would be / why it matters (significance 8): the largest seismically recorded mass movement of 2026. The initial avalanche and debris stage ran out 22–23 km, and the flood ran about 100 km. https://en.wikipedia.org/wiki/2026_Nepal%E2%80%93Tibet_floods ; https://www.sciencedirect.com/science/article/pii/S2667325826008277
- Evidence chain: as in C3, items 1 and 3. The Langtang Lirung summit is at about 7,234 m, while the DEM at the Eos coordinate reads 4,884 m. The Eos point is therefore in the deposit or the upper track, not the summit.
- Novelty check: well reported. Our addition is the S2 before/after pair and the track geometry.
- Orbital signature: a light-grey scar and track about 4–5 km long and 200–600 m wide, plus a fresh ice scar. S2: yes. DEM: no (pre-event DEM).
- Biggest reason it could be wrong: none for existence. The exact failure scar is still unconfirmed.
- Confidence: 85.
- **Window:** 2025-10-21 vs 2026-10-26 (tile 45RUM, 05:10 UTC orbit).

### C5. St Elias (Hubbard Glacier Mw 7.0, 6–7 Dec 2025) co-seismic landslides — KNOWN; optical gap
- Coordinates: Mt King George massif, approx. 60.35, −139.30 (±15 km; approx., from general geographic knowledge, not sourced).
- What it would be / why it matters (significance 6): more than 700 landslides and avalanches. The largest was a 9 km² rock-and-ice avalanche from the SW ridge, which ran out 7.4 km onto the Hubbard Glacier. Mapping used SAR because of cloud and winter darkness, so the **first clear summer-2026 Sentinel-2 imagery is the first optical record** for most slides.
- Evidence chain: https://eos.org/thelandslideblog/hubbard-glacier-earthquake-1 ; https://www.usgs.gov/programs/landslide-hazards/science/2025-m70-hubbard-glacier-earthquake-triggered-landslides-and ; https://explorersweb.com/avalanches-and-serac-falls-after-major-glacier-earthquake/ ; https://www.alaskasnewssource.com/2025/12/31/more-than-700-landslides-avalanches-discovered-after-m70-alaska-earthquake/
- Novelty check: inventoried by USGS and the Yukon Geological Survey (ScienceBase). Optically undocumented slides are likely among the smaller ones.
- Orbital signature: debris sheets 0.1–9 km² on glacier ice; they get advected and snow-covered. S2: yes in Jul–Sep 2026. DEM: no.
- Biggest reason it could be wrong: deposits on glaciers get buried by snow, so summer imagery may show less than the SAR did.
- Confidence: 50 for the coordinate box.
- **Window:** Sep 2025 vs Jul–Sep 2026.

### C6. Kamchatka M8.8 (29 Jul 2025): coastal-cliff and cloud-gap landslides — PROPOSED (USGS states its inventory is incomplete)
- Coordinates: approx. 52.8, 159.0 (±80 km; approx., from general geographic knowledge, not sourced; the target is the Pacific coast nearest the rupture).
- What it would be / why it matters (significance 5): USGS mapped 346 landslides from S2 over about 33,000 km², using imagery from Aug 4–22, 2025. It explicitly says the inventory may miss "rockfall on coastal cliffs" and slides under persistent cloud. https://www.usgs.gov/data/landslides-triggered-2025-m88-kamchatka-peninsula-russia-earthquake
- Evidence chain: the USGS data release above, plus https://www.sciencebase.gov/catalog/item/691ceda3d4be021d1d89b3ba
- Novelty check: anything outside the 346 mapped slides would be new.
- Orbital signature: fresh scars ≥0.001 km² (≥3×3 px); coastal talus fans. S2: yes. DEM: no.
- Biggest reason it could be wrong: most missed slides are small, below 10 m resolution.
- Confidence: 30.
- **Window:** Jun–Jul 2025 vs Sep 2025 and Jun 2026.

### C7. NE Greenland post-2020 new islands (Storstrømmen / Zachariae Isstrøm fronts) — PROPOSED (gap analysis)
- Coordinates: approx. 77.2, −22.5 (Storstrømmen) and 78.9, −21.0 (Zachariae) (±30 km; approx., from general geographic knowledge, not sourced).
- What it would be / why it matters (significance 6): new land exposed by glacier retreat. Kavan et al. (2025) counted 35 new islands >0.5 km² between 2000 and 2020, mostly in Greenland, with Zachariae Isstrøm the largest single contributor (81 km of new coastline). **Islands emerging in 2021–2026 are outside that inventory.** Pelto describes Storstrømmen thinning "releasing new islands" ("Island A", 2023), which are unnamed.
- Evidence chain: https://www.carbonbrief.org/global-warming-is-exposing-new-coastlines-and-islands-as-arctic-glaciers-shrink ; https://www.euronews.com/2025/04/02/the-arctics-glaciers-are-retreating-exposing-new-coastlines-that-could-trigger-tsunamis ; https://glacierchange.blog/category/greenland-glacier-retreat/
- Novelty check: I could not search further (budget). Islands are blog-noted but unnamed and not in the 2000–2020 inventory.
- Orbital signature: rock or sediment islands 0.1–2 km² separated from the ice front by open water or mélange. S2: yes (late-summer scenes). DEM: GLO-30 shows them as ice-covered (pre-exposure).
- Biggest reason it could be wrong: many "islands" are ice-cored or are nunataks still connected through the mélange.
- Confidence: 35.
- **Window:** Aug 2020 vs Aug 2025 or 2026.

### C8. Talidas (Gupis, Ghizer) GLOF source lake and Ghizer River blockage (22 Aug 2025) — KNOWN; inventory gap
- Coordinates: approx. 36.20, 73.40 (±10 km; approx., from general geographic knowledge of the Gupis valley, not sourced).
- What it would be / why it matters (significance 6): a moraine-dammed lake drained on 22 Aug 2025. The debris blocked the Ghizer River and created a lake about 7–8 km long for 6–10 hours, and more than 160 houses were damaged. The preprint says the lake formed only intermittently in the past, so it is likely absent from static GLOF inventories, and it may refill. https://www.preprints.org/manuscript/202603.0519/v1 ; https://www.dawn.com/news/1933779 ; https://www.pakistantoday.com.pk/2025/08/31/over-100-houses-swept-away-as-glacial-flood-creates-artificial-lake-in-ghizer/
- Novelty check: covered by the news and a preprint, but no coordinates in my results.
- Orbital signature: an empty or refilling basin (lake about 0.05–0.3 km²) and a debris fan in the Ghizer channel. S2: yes. DEM: no.
- Biggest reason it could be wrong: my coordinate is approximate, so the lead must locate the debris fan in S2 first.
- Confidence: 40.
- **Window:** Jul 2025 vs Sep 2025 and Sep 2026 (look for refilling).

### C9. GEC Box B: Seyakha (east Yamal) — PROPOSED
- Coordinates: 70.30, 71.75 (±15 km). Bounding box 70.20–70.40 N, 71.45–72.05 E (tile 42WXD).
- Significance 5. C11 formed on 28 Jun 2017 by blowout, self-ignition and explosion at a pingo-like mound in a river channel, and was still emitting gas in 2017–2020. https://doi.org/10.3390/en14175345 ; https://www.sciencedirect.com/science/article/abs/pii/S0165232X2200026X
- Novelty check: no newer craters were found near Seyakha in my results.
- Orbital signature: as in C1; channel and floodplain sites may fill with water quickly. S2: yes (borderline). DEM: no.
- Biggest reason it could be wrong: a single-crater prior.
- Confidence: 25.
- **Window:** Jul 2023 vs Aug 2026.

### C10. GEC Box C: Gydan, AntGEC area — PROPOSED
- Coordinates: 69.79, 75.04 (±20 km). Bounding box 69.65–69.95 N, 74.6–75.5 E (tile 43WET).
- Significance 5. AntGEC formed in Sep 2013; Gydan has far less monitoring than Yamal. Sources: the Zolkos/Dvornikov table, via snippet; https://www.ikz.ru/wp-content/uploads/2019/06/PPP_Dvornikov.pdf
- Novelty check: the AntGEC coordinate came from a search summary (Table 2), so it needs verification.
- Orbital signature: as in C1. S2: yes (borderline). DEM: no.
- Biggest reason it could be wrong: the coordinate itself may be off.
- Confidence: 20.
- **Window:** 2020 vs 2026 summers.

### C11. Tracy Arm landslide (10 Aug 2025) — KNOWN calibration
- Coordinates: approx. 57.88, −133.15 (±5 km; South Sawyer Glacier terminus, approx., from general geographic knowledge, not sourced).
- What it is (significance 7): more than 64×10⁶ m³ fell about 1 km onto South Sawyer Glacier. The tsunami ran up 481 m, and the long-period signal was equivalent to M5.4. It was detected manually because it lay outside automatic coverage. https://www.usgs.gov/programs/landslide-hazards/science/2025-tracy-arm-landslide-generated-tsunami ; https://earthquake.alaska.edu/event/025a7d7cil/detail ; https://www.science.org/doi/10.1126/science.aec3187
- Orbital signature: a scar of about 1 km, a trimline up to 481 m, and stripped vegetation. S2: yes.
- Confidence: 95 for the event; 50 for my coordinates.
- **Window:** Jul 2025 vs Sep 2025.
- Dickson Fjord (16 Sep 2023, 25.5×10⁶ m³, the 9-day VLP signal) is the analogous Greenland calibration. I did not obtain its coordinates. https://www.science.org/doi/10.1126/science.adm9247

### C12. Prow Knob, Alsek Lake (Alaska): new island 2025 — KNOWN calibration for (d)
- Coordinates: approx. 59.15, −138.05 (±5 km; approx., from general geographic knowledge, not sourced).
- What it is (significance 4): about 5 km² of land became an island between 13 Jul and 6 Aug 2025. https://science.nasa.gov/earth/earth-observatory/alaskas-brand-new-island-154764/ ; https://www.adn.com/alaska-news/2025/09/18/a-retreating-glacier-has-revealed-a-new-island-in-southeast-alaska/
- Analogous case: the Austfonna (Svalbard) island of 0.45 km² off SE Harald V Land is KNOWN but unnamed in my sources. https://qazinform.com/news/new-island-appears-in-norways-svalbard-amid-rapid-glacier-melt-4c2e76
- Orbital signature: an ice-free strait between knob and glacier. S2: yes.
- Confidence: 90 for the event.
- **Window:** 2025-07-13 vs 2025-08-06.

## Dead ends (things you checked that did not pan out, 1 line each)
- WebFetch to mdpi.com and doaj.org was blocked, so I could not read the GEC Table 2 or the C17 paper directly. C17 coordinates are still unknown, and my 2019→2020 S2 scan around C1 gave only unverified dark-pixel hits (`out/scan_C17_2019_2020.txt`).
- "New GEC in August 2024" (CNN, via search snippet): I could not confirm the location or the source text.
- A GEC susceptibility map produced by ML: none found. Zolkos et al. 2021 is change detection; it found 3 "GEC-like" features whose coordinates I could not read.
- Top hit of the S2 GEC scan 2022→2024 (70.1537, 68.5386): a false positive (vegetation and drained-lake phenology).
- The 2025→2026 scan hits at 70.114, 68.459 and 70.036, 68.652 were unmasked cloud shadows.
- Seismically detected 2024 landslides in Patagonia, Karakoram or Kamchatka with no imagery: none found within the search budget. The ESEC / USGS "Seismogenic Landslides" v3.0 (May 2025) and v4.0 (Oct 2026) Events.csv are the right source but were not reachable from the shell.
- Gorkha (Samdo, Dhindhur River) landslide lake of Nov 2026: about 500 m², too small for S2.
- Siji River (Arunachal, Jun 2026) and Kuwari/Shambhu River (Uttarakhand, 1.13 km, up to 3.7 Mm³) landslide lakes: real hazards, but I had no coordinates; these are leads for the lead.
- (e) volcanic and thermal features from 2023–2026 were **not researched** because the search budget was exhausted. Unsourced leads to verify: Iwo-tō (Iō-jima) new land in late 2023; Home Reef (Tonga) 2022–24; Hayli Gubbi (Ethiopia) eruption, Nov 2025; Fentale/Dofen (Afar) dike fissures, 2025; Krasheninnikov (Kamchatka), 2025; the Biscuit Basin (Yellowstone) hydrothermal explosion, Jul 2024.

## Sources
- https://www.researchgate.net/figure/Coordinates-of-the-gas-blowout-craters-on-the-Yamal-Peninsula_tbl1_341905295
- https://www.mdpi.com/2076-3263/11/1/21 ; https://www.fs.usda.gov/rm/pubs_journals/2021/rmrs_2021_zolkos_s001.pdf
- https://doi.org/10.3390/en14175345 ; https://www.sciencedirect.com/science/article/abs/pii/S0165232X2200026X
- https://www.researchgate.net/publication/349110798 ; https://ui.adsabs.harvard.edu/abs/2021Geosc..11...71B
- http://eng.arctica-ac.ru/article/700/ ; http://eng.arctica-ac.ru/article/454/ ; https://geoexpro.com/gas-blowouts-on-the-yamal-and-gydan-peninsulas/
- https://en.wikipedia.org/wiki/Gas_emission_crater ; https://www.ikz.ru/wp-content/uploads/2019/06/PPP_Dvornikov.pdf
- https://eos.org/thelandslideblog/26-august-2026-nepal-and-tibet ; https://www.usgs.gov/programs/landslide-hazards/science/2026-nepal-debris-avalanche-and-flash-flood ; https://en.wikipedia.org/wiki/2026_Nepal%E2%80%93Tibet_floods
- https://www.cnn.com/2026/08/28/china/china-secondary-disaster-flood-lake-breach-intl-hnk ; https://www.aljazeera.com/news/2026/8/28/is-nepal-facing-another-devastating-flood-from-a-new-lake ; https://news.cgtn.com/news/2026-08-28/Barrier-lake-forms-after-Gyirong-mudslide-in-Xizang-1PYx0bgPkxG/p.html
- https://eos.org/thelandslideblog/hubbard-glacier-earthquake-1 ; https://www.usgs.gov/programs/landslide-hazards/science/2025-m70-hubbard-glacier-earthquake-triggered-landslides-and ; https://explorersweb.com/avalanches-and-serac-falls-after-major-glacier-earthquake/
- https://www.usgs.gov/data/landslides-triggered-2025-m88-kamchatka-peninsula-russia-earthquake ; https://www.sciencebase.gov/catalog/item/691ceda3d4be021d1d89b3ba
- https://www.usgs.gov/programs/landslide-hazards/science/2025-tracy-arm-landslide-generated-tsunami ; https://earthquake.alaska.edu/event/025a7d7cil/detail ; https://www.science.org/doi/10.1126/science.aec3187 ; https://www.science.org/doi/10.1126/science.adm9247
- https://www.preprints.org/manuscript/202603.0519/v1 ; https://www.dawn.com/news/1933779 ; https://kathmandupost.com/national/2026/11/06/landslide-dams-river-forming-lake-in-gorkha
- https://www.carbonbrief.org/global-warming-is-exposing-new-coastlines-and-islands-as-arctic-glaciers-shrink ; https://glacierchange.blog/category/greenland-glacier-retreat/ ; https://science.nasa.gov/earth/earth-observatory/alaskas-brand-new-island-154764/ ; https://qazinform.com/news/new-island-appears-in-norways-svalbard-amid-rapid-glacier-melt-4c2e76
- https://www.usgs.gov/data/seismogenic-landslides-and-other-mass-movements-ver-30-may-2025
- Data: s3://sentinel-cogs (scenes named above); s3://copernicus-dem-30m tile N28_E085.

```json
[
{"id":"T9-C1","name":"Central-Yamal GEC cluster search box A (69.93-70.20N, 68.30-69.15E)","lat":70.06,"lon":68.70,"radius_km":25,"feature_size_m":40,"signature":"new dark pit 20-70 m with bright ejecta ring; compare 2024-07-29 / 2025-08-18 / 2026-08-18 (42WVC)","s2_visible":true,"dem_visible":false,"significance":7,"novelty":"PROPOSED","confidence":55,"looting_sensitive":false,"category":"gas-emission crater","one_line":"4-5 of ~8 giant GECs (C1,C2,C9,C17,C22) cluster here near Bovanenkovo pipeline; next GEC most likely here; our 2025-26 S2 scan found none"},
{"id":"T9-C2","name":"C22 'Doublet' GEC, S2-derived location","lat":70.1460,"lon":68.5002,"radius_km":0.05,"feature_size_m":35,"signature":"dark pit with bright rim ~230 m NE of C2; absent 2023-06-30, present 2023-09-05","s2_visible":true,"dem_visible":false,"significance":5,"novelty":"KNOWN","confidence":75,"looting_sensitive":false,"category":"gas-emission crater","one_line":"Calibration: 2023 crater recovered in 10 m S2, formation window 2023-06-30..2023-09-05"},
{"id":"T9-C3","name":"Lhende Khola 2026 landslide-dam / barrier-lake site","lat":28.334,"lon":85.484,"radius_km":1,"feature_size_m":800,"signature":"grey debris fan blocking valley at DEM 2873-2947 m; compare S2 2025-10-21 vs 2026-09-28/10-26 (45RUM)","s2_visible":true,"dem_visible":false,"significance":8,"novelty":"NOVEL-SYNTHESIS","confidence":70,"looting_sensitive":false,"category":"landslide-dammed lake","one_line":"CCTV 2950 m + >10 km from Gyirong Port + S2 debris junction + DEM converge here; no lake persisted by late Sep 2026"},
{"id":"T9-C4","name":"Langtang Lirung north-face ice-rock avalanche, 26 Aug 2026","lat":28.2765,"lon":85.5194,"radius_km":2,"feature_size_m":4500,"signature":"fresh light-grey track 4-5 km long from ice to valley; S2 2025-10-21 vs 2026-10-26","s2_visible":true,"dem_visible":false,"significance":8,"novelty":"KNOWN","confidence":85,"looting_sensitive":false,"category":"seismically detected rock-ice avalanche","one_line":"M5.2-equivalent seismic signal; deadly Nepal-Tibet debris flow; S2 before/after confirmed"},
{"id":"T9-C5","name":"Mt King George / Hubbard Glacier co-seismic landslides (Dec 2025)","lat":60.35,"lon":-139.30,"radius_km":15,"feature_size_m":3000,"signature":"rock-ice debris sheets on glacier, largest 9 km2, 7.4 km runout; first optical view summer 2026","s2_visible":true,"dem_visible":false,"significance":6,"novelty":"KNOWN","confidence":50,"looting_sensitive":false,"category":"co-seismic landslides","one_line":">700 slides mapped by SAR only; compare S2 Sep 2025 vs Jul-Sep 2026 (coords approx.)"},
{"id":"T9-C6","name":"Kamchatka M8.8 coastal-cliff/cloud-gap landslides","lat":52.8,"lon":159.0,"radius_km":80,"feature_size_m":50,"signature":"fresh scars and talus fans on Pacific coastal cliffs missed by USGS inventory","s2_visible":true,"dem_visible":false,"significance":5,"novelty":"PROPOSED","confidence":30,"looting_sensitive":false,"category":"co-seismic landslides","one_line":"USGS 346-slide inventory admits missing coastal rockfall and cloud-covered areas; compare Jul 2025 vs Sep 2025/Jun 2026 (coords approx.)"},
{"id":"T9-C7","name":"NE Greenland post-2020 new islands (Storstrommen / Zachariae fronts)","lat":77.2,"lon":-22.5,"radius_km":30,"feature_size_m":800,"signature":"rock islands separated from retreating ice front by water/melange; Aug 2020 vs Aug 2025-26","s2_visible":true,"dem_visible":false,"significance":6,"novelty":"PROPOSED","confidence":35,"looting_sensitive":false,"category":"new land from glacier retreat","one_line":"Kavan et al. 2025 inventory stops at 2020; Pelto notes unnamed islands released at Storstrommen (coords approx.)"},
{"id":"T9-C8","name":"Talidas GLOF source lake and Ghizer River blockage (Aug 2025)","lat":36.20,"lon":73.40,"radius_km":10,"feature_size_m":7000,"signature":"drained moraine lake basin + debris fan in Ghizer channel; 7-8 km temporary lake for hours","s2_visible":true,"dem_visible":false,"significance":6,"novelty":"KNOWN","confidence":40,"looting_sensitive":false,"category":"GLOF / landslide-dammed lake","one_line":"Intermittent lake likely absent from GLOF inventories; check refilling Jul 2025 vs Sep 2025/Sep 2026 (coords approx.)"},
{"id":"T9-C9","name":"Seyakha GEC search box B","lat":70.30,"lon":71.75,"radius_km":15,"feature_size_m":40,"signature":"new pit with ejecta near river channels/pingo-like mounds (42WXD)","s2_visible":true,"dem_visible":false,"significance":5,"novelty":"PROPOSED","confidence":25,"looting_sensitive":false,"category":"gas-emission crater","one_line":"Around 2017 Seyakha blowout crater C11; compare Jul 2023 vs Aug 2026"},
{"id":"T9-C10","name":"Gydan AntGEC search box C","lat":69.79,"lon":75.04,"radius_km":20,"feature_size_m":40,"signature":"new pit with ejecta (43WET)","s2_visible":true,"dem_visible":false,"significance":5,"novelty":"PROPOSED","confidence":20,"looting_sensitive":false,"category":"gas-emission crater","one_line":"Around 2013 AntGEC on poorly monitored Gydan; compare 2020 vs 2026 summers"},
{"id":"T9-C11","name":"Tracy Arm landslide, 10 Aug 2025 (calibration)","lat":57.88,"lon":-133.15,"radius_km":5,"feature_size_m":1000,"signature":"~1 km scar above South Sawyer Glacier, 481 m tsunami trimline","s2_visible":true,"dem_visible":false,"significance":7,"novelty":"KNOWN","confidence":50,"looting_sensitive":false,"category":"seismically detected landslide","one_line":"M5.4-equivalent signal, >64 Mm3; compare Jul 2025 vs Sep 2025 (coords approx.)"},
{"id":"T9-C12","name":"Prow Knob new island, Alsek Lake (calibration)","lat":59.15,"lon":-138.05,"radius_km":5,"feature_size_m":2500,"signature":"knob fully surrounded by water after glacier separation","s2_visible":true,"dem_visible":false,"significance":4,"novelty":"KNOWN","confidence":90,"looting_sensitive":false,"category":"new land from glacier retreat","one_line":"Became an island between 2025-07-13 and 2025-08-06 (coords approx.)"}
]
```
