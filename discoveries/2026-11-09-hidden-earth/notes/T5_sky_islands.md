# T5 — Unsurveyed sky-island forests (the next Mount Mabu)

> **Status: partial run, read before using.** Two of the three evidence legs
> required by the mandate could not be completed in this session.
> (a) **GBIF record counts were NOT obtained.** `api.gbif.org` is outside this session's
> network allow-list: WebFetch failed with "getaddrinfo ENOTFOUND" and shell curl got
> "CONNECT tunnel failed, 403". The anonymous GBIF S3 snapshot
> (`gbif-open-data-us-east-1/occurrence/2026-11-01/`) *is* reachable, but it is about
> 10,346 parquet files, and they are not partitioned by geography. A bounding-box count
> would mean reading about 90 GB of lat/lon columns, which is a bulk pull, so I did not do it.
> (b) **No literature novelty check was possible.** The shared WebSearch budget (200 per turn)
> was used up before T5's first query, and WebFetch to `en.wikipedia.org` also failed DNS.
> Every candidate below therefore rests on **terrain isolation plus forest presence
> only**, both measured from open data. All novelty labels are **provisional**.
> **To finish:** allow `api.gbif.org` and run the GBIF bbox counts listed per candidate.

## Method (what you joined, what you searched)
1. **Terrain isolation (DEM scan).** I wrote `data/T5/massif_scan.py`, which reads the Copernicus GLO-30 DEM (s3://copernicus-dem-30m) on a grid of about 280 m over 11–18°S, 33–41°E (northern Mozambique and Malawi). It flags summits that dominate an ~8 km radius and stand more than 600 m above the 10th-percentile elevation of a ~25 km window. That gave 324 hits, which collapse to 106 massifs once hits within 12 km are merged (`moz_mw_massifs.csv`, `moz_mw_clusters.csv`). I kept the 47 on the Mozambique side (`moz_targets.csv`).
2. **Forest presence.** `data/T5/probe.py` takes a box of ±0.045° around each summit and reads:
   - the ESA WorldCover 2021 tree fraction (s3://esa-worldcover);
   - the **Meta/WRI 1 m global canopy-height model** (dataforgood-fb-data, `alsgedi_global_v6_float/chm`), sampled at about 4 m.
   WorldCover does not separate miombo from moist forest: tree cover is 81–88% in miombo too. Canopy height does separate them. Results are in `moz_probe.jsonl`.
3. **Calibration.** I ran three known boxes through the same probe:

   | Box | Canopy >20 m | Canopy >15 m | p90 height |
   |---|---|---|---|
   | Mount Mabu core | 16.6% | 37.8% | 22 m |
   | Lowland miombo 25 km SE of Mabu | 0.6% | 12.3% | 16 m |
   | Namuli plateau | 0.4% | — | — (false negative: its forest patches are small and its plateau is grassland) |

   **Rule used:** canopy above 20 m in more than 2.5% of a summit box, at more than 2× the miombo baseline, means a candidate tall moist forest.
4. **Locating the forest.** For the hits that passed, `refine.py` finds the 0.01° cell with the densest canopy above 20 m. It also gives the extent of that canopy (5th–95th percentile) and its area minus the miombo baseline (`refine_results.jsonl`).
5. **Survey gaps.** Not measured (see the status note above). The other regions in the mandate were **not swept**: Angola, Tanzania, Zambia, DRC, Cameroon/Nigeria, Madagascar, the Guiana Shield, New Guinea, Borneo/Sulawesi, Myanmar and the Andes. Without web access I could not anchor named massifs to sourced coordinates. In closed-forest regions (New Guinea, Borneo) canopy height cannot pick out sky-island forest anyway.

## Candidates (ranked)

### C1. Unnamed massif 20 km east of Mount Mabu (Lugela district, Zambézia), the "Mabu twin" — NOVEL-SYNTHESIS (provisional; novelty not web-checked)
- Coordinates: **-16.304, 36.586** (±3 km). Tall-canopy core cell; the median of all pixels above 20 m is -16.307, 36.603.
- What it would be / why it matters (significance 8/10):
  - A second Mabu-class moist forest on an isolated massif in the same rainshadow-free belt. If it is unsurveyed, it is the most direct application of the Bayliss method: a forest found from imagery that has the same structure as Mabu.
  - It would test whether Mabu's endemics, such as the *Nadzikambia*/*Rhampholeon* lineages, are shared with it or replaced by new species.
- Evidence chain:
  1. DEM scan: an isolated summit at -16.309, 36.591. Summit about 1262–1314 m over a base of about 325 m, so about 940 m of relief. It is a separate massif from Mabu (summit -16.299, 36.394; 1661 m), 20.6 km away at a bearing of about 90°. Sources: `data/T5/moz_mw_clusters.csv`, s3://copernicus-dem-30m.
  2. Forest presence in a ±0.045° box: WorldCover tree cover 96.8%. Meta CHM canopy >20 m 7.3%, >15 m 22.7%, p90 19 m, p98 24 m. That is **12× the miombo baseline for >20 m**, and the strongest signal in northern Mozambique after Mabu itself. Sources: `data/T5/moz_probe.jsonl`, https://dataforgood-fb-data.s3.amazonaws.com/forests/v1/alsgedi_global_v6_float/chm/, s3://esa-worldcover/v200/2021/map/.
  3. Refined over a ±0.07° box: **11.0 km² of canopy >20 m** (about 9.6 km² after subtracting the baseline) and 40.9 km² >15 m. Extent: lat -16.357 to -16.269, lon 36.552 to 36.657. The densest 0.01° cell is 48% covered by canopy >20 m. Source: `data/T5/refine_results.jsonl`.
  4. Precedent: Mabu's forest went unrecorded until it was spotted on Google Earth in 2005 (the team mandate from the lead, which restates the BRIEF's precedent-transfer example). The Mabu calibration box (C5) gives 16.6% >20 m, which puts C1 at roughly half Mabu's tall-canopy density.
- Novelty check: **not performed.** Web search and fetch were blocked and the GBIF API was unreachable. Searches to run:
  - the name of this massif (my data cannot name it);
  - "Mabu" together with "Lugela" and "Tacuane", to see whether it falls within Mabu's surveyed area or the follow-up surveys;
  - the GBIF bbox lat -16.36,-16.26, lon 36.55,36.66.
- Orbital signature: a dark-green, rough-textured closed canopy of about 10–15 km² on the slopes of a dome or ridge about 1 km high. It should stand out sharply against lighter miombo and smallholder mosaic. Clearly **visible in S2 at 10 m**, and the massif is **visible in GLO-30**.
- Biggest reason it could be wrong:
  1. It could be plantation canopy (eucalyptus or pine) or old tea-estate shade trees in the Lugela/Tacuane tea area, which would give tall CHM without moist forest. S2 texture and phenology should tell them apart.
  2. Or it is already known: it may be one of the nearby forests visited during the Mabu expeditions.
- Confidence: 40. That forest is there: about 65. That it is biologically unsurveyed: unknown.

### C2. Unnamed massif 37 km east of Mabu (Lugela/Namarrói border area) — NOVEL-SYNTHESIS (provisional)
- Coordinates: **-16.354, 36.734** (±3 km).
- What it would be / why it matters (significance 6/10): a smaller tall-forest patch on a third isolated massif in the Mabu cluster. It would be a stepping stone for testing connectivity between the Mabu and Namuli faunas.
- Evidence chain:
  1. DEM: summit 1145 m over a base of 277 m, so 868 m of relief, at -16.359, 36.759. Source: `moz_mw_clusters.csv`.
  2. CHM in a ±0.045° box: >20 m 2.5%, >15 m 14%, WorldCover tree 87%. Source: `moz_probe.jsonl`.
  3. Refined: 3.7 km² >20 m (about 2.7 km² above baseline), centred on lat -16.381 to -16.309, lon 36.70 to 36.76. Source: `refine_results.jsonl`.
- Novelty check: not performed. Run GBIF bbox lat -16.39,-16.30, lon 36.69,36.77.
- Orbital signature: closed canopy patches totalling 2–4 km² on mid-slopes. S2-visible; the DEM massif is visible.
- Biggest reason it could be wrong: the area is small and could be riparian forest or plantation. The signal is near the detection threshold.
- Confidence: 25.

### C3. Massif 17 km SE of Chiperone summit (Milange/Morrumbala border) — NOVEL-SYNTHESIS (provisional; may belong to the already-visited Chiperone complex)
- Coordinates: **-16.611, 35.819** (±3 km).
- What it would be / why it matters (significance 5/10): a separate forested summit (1409 m) next to Chiperone. Chiperone is in the lead's list of surveyed massifs, which is why it holds a *Rhampholeon* endemic. If C3 was not part of that survey, it is a sister sky island.
- Evidence chain:
  1. DEM: summit 1363–1409 m over a base of about 250 m, so 1113 m of relief, at -16.606, 35.824. That is 17.6 km from the Chiperone summit hit (-16.479, 35.711; 2053 m) at a bearing of about 140°. Source: `moz_mw_clusters.csv`.
  2. CHM: >20 m 3.0% (Chiperone box: 3.1%), WorldCover tree 83%. Source: `moz_probe.jsonl`.
  3. Refined: 3.9 km² >20 m (about 2.9 km² above baseline). Extent lat -16.657 to -16.599, lon 35.769 to 35.845. Source: `refine_results.jsonl`.
- Novelty check: not performed. Check whether the Chiperone surveys covered the SE summit. GBIF bbox lat -16.66,-16.59, lon 35.76,35.85.
- Orbital signature: 3–5 km² of closed canopy on the S/SE slopes of a 1.4 km dome. S2-visible.
- Biggest reason it could be wrong: it is probably part of the Chiperone massif, which is surveyed.
- Confidence: 20.

### C4. Forested massif at -15.72, 37.25 (Ile / Lugela / Alto Molócuè area) — identity UNRESOLVED (could be Mount Lico, i.e. KNOWN)
- Coordinates: **-15.714, 37.236** (±4 km).
- What it would be / why it matters (significance 5/10): a summit of 1473–1562 m standing about 960 m above the plain, with a tall-canopy core. **If it is Mount Lico** (found by imagery in 2018 according to the lead's mandate), it is a positive control that the method recovers Lico. If not, it is a new candidate.
- Evidence chain:
  1. DEM: summit 1562 m over a base of 511 m, so 962 m of relief, at -15.739, 37.281. Source: `moz_mw_clusters.csv`.
  2. CHM: >20 m 2.7%, >15 m 9.7%, WorldCover tree 75%. Source: `moz_probe.jsonl`.
  3. Refined: 3.8 km² >20 m (about 2.8 km² above baseline). Extent lat -15.748 to -15.697, lon 37.225 to 37.312. Source: `refine_results.jsonl`.
- Novelty check: not performed. **First step: compare these coordinates with Mount Lico's published position.** I could not retrieve it.
- Orbital signature: 3–4 km² of closed canopy. Lico would show as a sheer-walled inselberg with forest on the summit, which is distinctive in S2.
- Biggest reason it could be wrong: it is Lico (KNOWN), or a neighbour of it, or riparian or plantation canopy.
- Confidence: 15 that it is new; 50 that it is a real moist-forest patch.

### C5. Mount Mabu (calibration) — KNOWN
- Coordinates: -16.29, 36.40 (±4 km). Summit hit -16.299, 36.394; 1661 m; 1341 m of relief.
- Why it is here (significance 9/10 historically): it is the reference forest. Forest found on Google Earth in 2005, followed by the Kew expedition (lead mandate).
- Evidence chain:
  1. Same pipeline: >20 m 16.6%, >15 m 37.8%, p90 22 m; 7.1 km² >20 m in a 0.06° box and 16 km² in a 0.09° box. Source: `moz_probe.jsonl` and the calibration run.
  2. Miombo control 25 km SE: >20 m 0.6%.
- Novelty check: KNOWN per the lead's mandate.
- Orbital signature: about 10–20 km² of tall closed canopy (CHM-detectable). S2-visible.
- Biggest reason it could be wrong: n/a. The Meta CHM saturates at about 25 m, so tall-forest area is understated.
- Confidence: 95 (as calibration).

### C6. Serra Mecula, Niassa (context) — KNOWN (it is on the lead's list of already-surveyed massifs)
- Coordinates: -12.08, 37.63 (±5 km). Summit 1436 m, relief 947 m.
- Evidence: CHM >20 m only 0.7%, >15 m 6.7%, WorldCover tree 78% (`moz_probe.jsonl`). Either the moist forest here is small or short, or canopy height under-detects it.
- Why it is included: it shows the detection floor. A KNOWN forested massif that barely registers means a near-zero CHM score does not rule out forest. Namuli shows the same.
- Confidence: n/a (context).

## Dead ends (things you checked that did not pan out, 1 line each)
- The GBIF occurrence API (WebFetch and shell) is blocked by the network policy; record counts were not obtained.
- The GBIF S3 parquet snapshot is reachable but not spatially partitioned: about 10,346 files and about 90 GB of coordinate columns, so it was not scanned.
- BigQuery (`bq`) has no credentials, so the public-dataset GBIF query route is unavailable.
- WebSearch: the shared budget was exhausted. WebFetch to en.wikipedia.org failed DNS. No literature novelty checks were possible.
- WorldCover tree fraction alone does not discriminate: miombo control 88% vs Mabu 97%.
- Massif W of Mabu (-16.309, 36.224): only 1.2 km² of canopy >20 m, about 0.5 km² above baseline, which is noise level.
- Namuli (-15.356, 37.059), Inago (-15.064, 37.341), Ribáuè/Mepáluè (-14.886, 38.311), and the Gurué massifs (-15.189, 36.989): canopy >20 m at or below 0.9% in summit boxes. These are known massifs whose forests are small or short, so the method gives false negatives here.
- Niassa/Nampula summits produced no tall-canopy signal (canopy >20 m at or below 0.4%): -14.749, 36.689; -14.641, 37.564; -14.056, 39.396; -14.586, 38.054; -15.061, 38.546.
- Morrumbala (-17.469, 35.384): canopy >20 m 0.3%.
- Regions not swept at all for lack of sourced coordinates or web access: Angola, Tanzania, Zambia, DRC, Cameroon/Nigeria, Madagascar, the Guiana tepuis, New Guinea (Van Rees/Gauttier), Borneo/Sulawesi, Myanmar, and the Andes.

## Sources
- Team mandate from the lead (Mount Mabu 2005 Google Earth discovery and Kew expedition; Mount Lico 2018) and `discoveries/2026-11-09-hidden-earth/BRIEF.md`.
- Copernicus GLO-30 DEM, anonymous S3: s3://copernicus-dem-30m/ (read directly).
- ESA WorldCover 10 m 2021 v200: s3://esa-worldcover/v200/2021/map/ (read directly).
- Meta/WRI 1 m global canopy height (Tolan et al.): https://dataforgood-fb-data.s3.amazonaws.com/forests/v1/alsgedi_global_v6_float/ (tile index `tiles.geojson` plus the CHM tiles, read directly).
- GBIF monthly snapshot (inspected, not scanned): https://gbif-open-data-us-east-1.s3.amazonaws.com/occurrence/2026-11-01/occurrence.parquet/
- Scripts and outputs: `discoveries/2026-11-09-hidden-earth/data/T5/` (`probe.py`, `massif_scan.py`, `refine.py`, `run_probe_list.sh`, `moz_mw_massifs.csv`, `moz_mw_clusters.csv`, `moz_targets.csv`, `moz_probe.jsonl`, `refine_results.jsonl`).

```json
[
 {"id":"T5-C1","name":"Unnamed massif 20 km E of Mount Mabu (Lugela, Zambezia)","lat":-16.304,"lon":36.586,"radius_km":3,"feature_size_m":4000,"signature":"~10-15 km2 dark rough closed canopy (Meta CHM >20 m on 11 km2) on slopes of an isolated ~940 m-relief massif amid lighter miombo/farmland","s2_visible":true,"dem_visible":true,"significance":8,"novelty":"NOVEL-SYNTHESIS","confidence":40,"looting_sensitive":false,"category":"sky-island forest","one_line":"Strongest tall-canopy signal in N Mozambique after Mabu itself; novelty and GBIF count unchecked (web/GBIF blocked); rule out plantations."},
 {"id":"T5-C2","name":"Unnamed massif 37 km E of Mount Mabu","lat":-16.354,"lon":36.734,"radius_km":3,"feature_size_m":2000,"signature":"2-4 km2 closed tall canopy on a 1145 m massif (868 m relief)","s2_visible":true,"dem_visible":true,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":25,"looting_sensitive":false,"category":"sky-island forest","one_line":"Third forested massif in the Mabu cluster; weak but above-baseline tall-canopy signal."},
 {"id":"T5-C3","name":"Massif 17 km SE of Chiperone summit","lat":-16.611,"lon":35.819,"radius_km":3,"feature_size_m":2000,"signature":"3-5 km2 tall canopy on S/SE slopes of a 1409 m dome (1113 m relief)","s2_visible":true,"dem_visible":true,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":20,"looting_sensitive":false,"category":"sky-island forest","one_line":"Possible sister sky island to Chiperone; may already be covered by Chiperone surveys."},
 {"id":"T5-C4","name":"Forested massif at -15.72, 37.25 (possibly Mount Lico)","lat":-15.714,"lon":37.236,"radius_km":4,"feature_size_m":2000,"signature":"3-4 km2 tall canopy on a 1562 m massif (962 m relief)","s2_visible":true,"dem_visible":true,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":15,"looting_sensitive":false,"category":"sky-island forest","one_line":"Identity unresolved: either Mount Lico (KNOWN, positive control) or a new forested inselberg nearby."},
 {"id":"T5-C5","name":"Mount Mabu (calibration)","lat":-16.29,"lon":36.40,"radius_km":4,"feature_size_m":7000,"signature":"10-20 km2 tall closed canopy; CHM >20 m on 16.6% of core box vs 0.6% miombo","s2_visible":true,"dem_visible":true,"significance":9,"novelty":"KNOWN","confidence":95,"looting_sensitive":false,"category":"sky-island forest","one_line":"Reference forest used to calibrate the canopy-height detector."},
 {"id":"T5-C6","name":"Serra Mecula, Niassa (context)","lat":-12.08,"lon":37.63,"radius_km":5,"feature_size_m":1000,"signature":"weak tall-canopy signal (0.7 km2 >20 m) on 1436 m massif","s2_visible":true,"dem_visible":true,"significance":4,"novelty":"KNOWN","confidence":90,"looting_sensitive":false,"category":"sky-island forest","one_line":"Known surveyed massif that barely registers; shows the detector's false-negative floor."}
]
```
