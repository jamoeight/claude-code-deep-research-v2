# T2 — Buried cities of the Silk Road deserts

> **Read this first: limits on this run.** About 20 WebSearch calls went through
> before the shared per-turn search cap (200 calls across all teams) ran out. WebFetch
> and curl were blocked for every literature host I tried (Wikipedia, archive.org,
> dsr.nii.ac.jp, Springer, Cambridge, CNKI-type sites, ctext, wikisource). So every
> citation below is a URL **seen in search results**, with the claim taken from the
> result snippet or summary. None of these pages was read in full. Three consequences:
> (1) The novelty checks are **partial**. Every `NOVEL-SYNTHESIS` label here is provisional.
> (2) A few itinerary figures come from the standard text of the *Xiyu ji* (book 12)
> or the *Luoyang qielan ji* (book 5) as I remember them. Each is marked **[text-from-memory]**
> and must be checked before anyone relies on it.
> (3) I could not evaluate Lop Nur/Loulan, Khwarezm/Tolstov, Juyan/Edsen Gol, Badain
> Jaran/Gobi or the CORONA studies. They appear under *Dead ends* as **not evaluated**.
> I make no claims about them.
> The data I could reach were Copernicus GLO-30 DEM (S3), the Pleiades gazetteer and
> Natural Earth (raw.githubusercontent). I used them for geodesy and palaeo-drainage tracing.

## Method (what you joined, what you searched; 5-10 lines)
1. **Itinerary geodesy.** Xuanzang gives a chain of distances in li from Khotan to Lop. I calibrated the length of his li on the
   Khotan→Pi-mo leg: 330 li = 93.0 km if Pi-mo = Uzun-tati, which is Stein's identification. That gives **282 m/li**.
   Two further legs, Ni-jang→Tukhara and Tukhara→Che-mo-t'o-na, independently give 306 and 260 m/li, so the
   scale holds (pyproj WGS84 geodesics; `data/T2/scripts/geodesy.py`).
2. **Contradiction mining.** On the same scale, the Pi-mo→Ni-jang leg (200 li) is about 2.9 times too long (815 m/li).
   Song Yun's distances are internally inconsistent as well. I worked out the consequences of both.
3. **Palaeo-drainage tracing.** I mosaicked the Copernicus GLO-30 DEM at about 250 m for 36–41°N, 79–87°E,
   smoothed it with a Gaussian (σ = 1 km or 3 km) to suppress the dunes, and traced steepest-descent
   flow lines from the oases, the present river termini and the known ruins (`flowlines.py`). These axes are a
   proxy for the ancient terminal-fan channels. **Calibration:** the axes pass within about 10–20 km of known
   sites, never closer, so I use them only as a coarse lateral constraint.
4. **Joins.** I combined the li-scale circles, the DEM fan axes, the dated settlement migration in the Keriya delta
   (Yuansha → Karadong, published ¹⁴C/OSL), and textual constraints on direction and date
   (e.g. "north of the kingdom", "fled east to Pi-mo", "already a sand mound in 644").
5. **Searches** (about 20): Ho-lao-lo-kia/曷劳落迦 identifications, the Pi-mo/Uzun-tati identification, Keriya delta
   chronology and coordinates, Endere and 睹货逻故国 dating, 宋云 末城/捍麽城, and site coordinates.

## Candidates (ranked)

### C1. Ho-lao-lo-kia (曷劳落迦), Xuanzang's sand-buried city "north of the kingdom" — NOVEL-SYNTHESIS (search box; the city's general setting was PROPOSED by Stein)
- **Coordinates:** 37.55, 80.58 (±30 km). This lies between the lower Yurungkash and the meridian of Uzun-tati (Pi-mo).
- **What it would be / why it matters (significance 8):** the town at the centre of the most famous sand-burial legend
  of the Silk Road. Xuanzang (644 CE) says it had already become "a great sand mound", and that kings who came to
  dig for its treasure were driven off by storms. It would be a Khotanese town abandoned before the 7th century,
  roughly contemporary with Karadong and Niya, in a sector of the Khotan hinterland that has never been mapped as a settlement zone.
- **Evidence chain:**
  1. Xuanzang: the Udayana sandalwood image flew "to the city of Ho-lao-lo-kia in the north of this kingdom"
     (凌空至此国北曷劳落迦城). Pi-mo lies about 30 li east of the "battlefield"
     ([quanxue Xiyuji ch.145](https://www.quanxue.cn/ct_fojia/xiyuji/xiyuji145.html); [Wikisource 四部丛刊 卷十二](https://zh.wikisource.org/zh-hans/%E5%A4%A7%E5%94%90%E8%A5%BF%E5%9F%9F%E8%A8%98_(%E5%9B%9B%E9%83%A8%E5%8F%A2%E5%88%8A%E6%9C%AC)/%E5%8D%B7%E7%AC%AC%E5%8D%81%E4%BA%8C)).
  2. The town "is now a great sand mound". The one survivor escaped through a passage and "**went eastwards** and took up his abode in P'i-mo".
     Stein reports that a local legend he heard "placed the buried town somewhere in the great desert to the north of Khotan"
     ([Stein, *Sand-Buried Ruins of Khotan*, DSR p.491](https://dsr.nii.ac.jp/toyobunko/VIII-5-B2-5/V-1/page-hr/0491.html.en)).
     So the city lies **west of Pi-mo and north of the oasis belt**.
  3. Pi-mo is 330 li east of Khotan. That points to the Chira–Gulakhma–Domoko oases
     ([Indian Antiquary 59](https://jainqq.org/pagetext/Indian_Antiquary_Vol_59/032551/55)). Stein equates Pi-mo with **Uzun-tati**
     ([DSR p.659](https://dsr.nii.ac.jp/toyobunko/III-2-F-c-30/V-2/page/0659.html.en)), at 37.28 N, 80.95 E
     ([WP list](https://en.wikipedia.org/wiki/List_of_archaeological_sites_of_the_Taklamakan_and_Lop_Desert)).
     The Indian Antiquary also records Stein linking the Indian legend of Roruka, buried under a rain of sand, to "Phimo or a place near by".
  4. **Exclusions, from date and direction.** Dandan Oilik (37.7744 N, 81.0731 E) was occupied from the 6th to the late 8th century
     ([WP Dandan Oilik](https://en.wikipedia.org/wiki/Dandan_Oilik)), so it was not a ruin in 644. It also lies NNE of Pi-mo (az 11°, 56 km).
     Karadong (38.53 N, 81.87 E) and Yuansha (38.87 N, 81.58 E) lie NE of Pi-mo, so a survivor fleeing from either would have gone SW, not east.
  5. **DEM join.** On the smoothed GLO-30, the regional drainage from the Chira–Uzun-tati and Domoko fans runs NW, through
     37.44 N 80.87 E → 37.58 N 80.73 E → 37.74 N 80.64 E, before it joins the Khotan-river trough at about 38.2–38.4 N.
     The Yurungkash axis runs through 37.58 N 80.15 E → 37.79 N 80.36 E. The box sits on the distal, now-dry fan between the two:
     the reach downstream of Pi-mo's own streams. From the box centre, Pi-mo bears 132° (ESE) at 44 km, which fits "went east".
     Khotan is 76 km SW (az 229°) and Dandan Oilik is 50 km ENE.
- **Novelty check:** I searched "Ho-lao-lo-kia … Stein identification", "曷劳落迦 城 位置 考证 媲摩 沙埋" and "曷劳落迦 喀拉墩/丹丹乌里克/乌曾塔提 比定".
  No published coordinate identification turned up. The results give only Stein's "desert north of Khotan", the Roruka/Phimo
  link, and popular accounts calling the city lost ([NTDTV 2023](https://www.ntdtv.com/gb/2023/11/16/a103825528.html)).
  This was not a full check: I did not search CNKI, nor the Chinese–Japanese Dandan Oilik reports.
  Known sites near the box should be excluded first: Rawak and Aksipil (Stein 1901). I did not verify their positions this session.
- **Orbital signature:** a walled town about 200–500 m across, probably partly sand-filled. What would show: a curvilinear rammed-earth
  or wattle wall line; fields of timber posts; dark "tati" spreads of sherds and slag (0.1–2 km²) in interdune corridors, contrasting
  with pale dune sand; and lines of dead poplar or tamarisk cones along the abandoned channels. Sentinel-2 can show the tati patches
  and any exposed wall ring. Recognising buildings needs sub-metre imagery. The site will not show in GLO-30, because 20–60 m dunes dominate.
- **Biggest reason it could be wrong:** the city may be purely legendary, a Khotanese localisation of the Indian Roruka story. And
  "north of this kingdom" may be loose. The real ruin behind the legend may also already be one of the known sites, such as Rawak.
- **Confidence:** 20 that an unpublished pre-7th-century town lies inside the circle. 10 that it is the city of the legend.

### C2. Xuanzang's "old Tukhara kingdom" (睹货逻故国): pre-Tang walled town on the western Endere fan — PROPOSED (Stein's Endere identification) with a new coordinate refinement
- **Coordinates:** 37.78, 83.67 (±20 km). This is about 13 km W of the Tang fort at Endere.
- **What it would be / why it matters (significance 6):** the deserted walled city Xuanzang passed in 644, between Ni-jang and Che-mo-t'o-na.
  This would be the "Tukhara" toponym on the Southern Route (the Kharoshthi-era settlement at Endere).
- **Evidence chain:**
  1. The chain Ni-jang → (400 li) → old Tukhara → (600 li) → Che-mo-t'o-na (Cherchen) **[text-from-memory, Xiyu ji book 12]**.
     Stein records that Xuanzang crossed this stretch and found the settlements deserted
     (search summary of [Stein/DSR](https://dsr.nii.ac.jp/toyobunko/VIII-5-B2-19/V-1/page-hr/0193.html.en); [Endere WP](https://en.wikipedia.org/wiki/Endere)).
  2. The standing fort at Endere carries a Chinese inscription of **719 CE** and was occupied in the 8th century. Kharoshthi tablets show
     occupation in the early centuries CE. Stein judged the Endere = Tukhara identification valid "only in a negative sense"
     (search summary of the same results; Endere 37°47′N 83°49′E, [Wikidata Q491836](https://www.wikidata.org/wiki/Q491836)).
     A 2009 *Chinese Science Bulletin* paper discusses the old Tukhara ruins and suggests the walls Xuanzang saw were abandoned after the
     3rd–4th centuries ([doi:10.1007/s11434-009-0586-4](https://dx.doi.org/10.1007/s11434-009-0586-4); seen only as a search summary).
     So the city Xuanzang saw is **not** the Tang fort. It is an earlier walled site nearby.
  3. **Geodesy.** The li scale comes from Khotan→Uzun-tati (282 m/li) and is independent of Endere. The 400-li circle about Niya/Minfeng
     (37.067 N, 82.767 E; [WP Niya County](https://en.wikipedia.org/wiki/Niya_County)) and the 600-li circle about Qiemo
     (38.1338 N, 85.5333 E; Natural Earth) intersect at **37.755 N, 83.690 E** at 279 m/li. That point is 11.6 km WSW of the fort.
     At ±20 m/li the point slides along a NW–SE line, from 37.60 N 83.89 E to 37.98 N 83.49 E.
  4. **DEM join.** The smoothed-DEM fan axis of the Endere river runs 37.62 N 83.81 E → **37.75 N 83.71 E** → 37.85 N 83.61 E → 37.95 N 83.51 E,
     i.e. the western branch of the fan. It passes within 2 km of the itinerary point. Solving the chain on the DEM axes
     (`chain_solve.py`) at 282 m/li puts Tukhara at 37.806 N, 83.652 E, and Ni-jang back on the Niya axis 3.8 km from Minfeng.
     The chain is therefore self-consistent.
- **Novelty check:** search for "安迪尔古城 睹货逻故国 碳十四 年代" found no published coordinates for a pre-Tang walled site west of the fort.
  From memory (not verified this session), Chinese surveys record several walled sites in the Andir desert, under names such as
  Daozilik and Akkoqikrek. **Assume one of them may be this site.** For that reason the label is PROPOSED, not novel.
- **Orbital signature:** a rammed-earth enclosure 100–300 m across, round or square, possibly with a stupa mound. Sentinel-2 should show
  the wall ring if it is not dune-covered. Endere-type walls are a few metres high, which is marginal in GLO-30.
- **Biggest reason it could be wrong:** the li scale is the dominant error. 10 % moves the point about 25 km along the axis.
  The "old Tukhara" ruin may also lie on the eastern branch.
- **Confidence:** 35.

### C3. Keriya delta: northern trunk-axis zone beyond Yuansha (Bronze Age/Early Iron Age terminal settlements) — NOVEL-SYNTHESIS (provisional)
- **Coordinates:** 39.25, 81.88 (±30 km).
- **What it would be / why it matters (significance 6):** settlements at the former terminus of the Keriya at its longest extent,
  before Yuansha (c. 400–130 BCE). These would be analogues of the Xiaohe-type terminal-delta Bronze Age sites. One would
  push the history of the Keriya oasis back before the earliest walled town.
- **Evidence chain:**
  1. Yuansha (38°52′N 81°35′E, [RG figure](https://www.researchgate.net/figure/Location-of-the-Yuansha-site_fig1_5606509)) has a
     995 m wall circuit, walls 3–11 m high, was found in 1994, and dates to c. 400 BCE
     ([xinjiangtravel](https://xinjiangtravel.org/khotan/attraction/ancient-city-of-yuansha.html)).
     Settlement there dates to about 2.6 ka. About 400 years later the channel had moved about 40 km SE, to Karadong
     ([Science China, s11430-011-4206-1](https://link.springer.com/article/10.1007/s11430-011-4206-1)).
     Holocene OSL ages lie along the ancient channels around both sites, and some near Yuansha are as old as about 14.5 ka
     ([J. Geogr. Sci. 2023](https://www.geogsci.com/EN/abstract/article/1009-637X/53877)).
  2. **DEM join.** The smoothed-DEM trunk axis of the Keriya fan runs Keriya town → 37.53 N 81.37 E → 38.12 N 81.61 E → **38.70 N 81.74 E**,
     passing *between* Yuansha (about 18 km W of it) and Karadong (about 15 km E of it). From there it continues north to
     **39.29 N 81.94 E** and 39.87 N 82.10 E, and reaches the Tarim at about 40.6 N. This is the corridor the river followed when it reached further north.
  3. The modern Keriya terminus is at 38.603 N 82.097 E ([WP Keriya River](https://en.wikipedia.org/wiki/Keriya_River)).
     Koyuk Shahri (41.606 N 84.347 E, [Pleiades](https://pleiades.stoa.org/places/418515134); [Antiquity 2022](https://www.cambridge.org/core/product/8F1FC55E08A966AC0F530D1FEFF124D4/core-reader))
     shows that walled sites older than Yuansha exist on the Tarim terminal fans.
  4. An alternative placement comes from simply extrapolating the Yuansha→Karadong migration vector backwards
     (az 146°, 44.6 km): **39.20 N, 81.30 E**. That is about 56 km west of the DEM axis. Keep it as a second search point.
- **Novelty check:** the Sino-French mission surveyed the Keriya delta "systematically" from 1993 to 2005
  ([Iranica, Keriya](https://www.iranicaonline.org/articles/keriya/)), and it may already have covered 39.0–39.5 N.
  I could not check its survey limits or the Chinese reports on the northern delta. I did not search the "Keriya Northern Cemetery" that I half-remember.
- **Orbital signature:** dead channels as sinuous lines of dead poplar and tamarisk (10–50 m wide, km long). Sherd and lithic scatters and
  small enclosures 50–150 m across. Possibly field and canal patterns at km scale. Sentinel-2 shows the channels and vegetation lines,
  and the sites only marginally. GLO-30 does not show the sites.
- **Biggest reason it could be wrong:** the Holocene terminus may never have reached this far during an occupation phase. The area may also
  already be surveyed and empty.
- **Confidence:** 12.

### C4. Lower Keriya–Niya interfluve east of Karadong: the 3rd–5th-century successor to Karadong — NOVEL-SYNTHESIS (provisional)
- **Coordinates:** 38.36, 82.20 (±25 km).
- **What it would be / why it matters (significance 5):** the place the Keriya delta population would have moved after Karadong was
  abandoned in the 4th century, if the river kept shifting east. It would also be where the distal waters of the Keriya and Niya systems met.
- **Evidence chain:**
  1. Karadong was the capital of the Keriya oasis in the first three centuries CE and was abandoned in the 4th century (search summaries citing
     [Iranica](https://www.iranicaonline.org/articles/keriya/) and [WP list](https://en.wikipedia.org/wiki/List_of_archaeological_sites_of_the_Taklamakan_and_Lop_Desert)).
     The settlement moved SE from Yuansha as the channel shifted ([Science China](https://link.springer.com/article/10.1007/s11430-011-4206-1)).
  2. Extending the Yuansha→Karadong vector by 0.5–1.0 steps gives 38.37 N 82.01 E to 38.20 N 82.15 E.
     The modern terminus is 28 km NNW of the box centre.
  3. **DEM join.** The smoothed flow line from the Niya ruins (38.0 N 82.68 E; [aroundus](https://aroundus.com/p/6449297-niya))
     heads NW, through **38.43 N 82.31 E**, and joins the Keriya-terminus line at about 38.9 N 82.2 E. The box is therefore where both terminal systems converge.
- **Novelty check:** none specific (search budget). This zone lies east of the classic Sino-French delta sites, but the 1993–2005 survey limits are unknown.
- **Orbital signature:** as for C3. Possible confusion with modern Darya Boyi pastoral houses and fields near the modern channel.
  Sentinel-2 would show channels and fields. GLO-30 does not show the sites.
- **Biggest reason it could be wrong:** after Karadong the river may simply have retreated south, so that no successor existed on the distal fan.
- **Confidence:** 12.

### C5. Song Yun's "Mo city" (末城), 22 li east of Hanmo (捍麽 = Pi-mo) — cannot resolve (probably within the known Domoko/Damagou site cluster)
- **Coordinates:** 37.28, 81.02 (±10 km).
- **What it would be / why it matters (significance 4):** the 6th-century town Song Yun (519 CE) reached just before Hanmo/Pi-mo.
- **Evidence chain:** Song Yun's Han-mo is identified with Pi-mo ([Indian Antiquary 59 index](https://jainqq.org/pagetext/Indian_Antiquary_Vol_59/032551/55)).
  "Mo city … west 22 li to Hanmo" **[text-from-memory, Luoyang qielan ji book 5]**. At 282 m/li, 22 li is 6.2 km east of Uzun-tati, which gives 37.28 N, 81.02 E.
  The Domoko-area sites were still occupied in the Muslim period and are linked with Marco Polo's "Pein" ([DSR/Serindia](https://dsr.nii.ac.jp/toyobunko/VIII-5-B2-9/V-3/page/0223.html.ja)).
- **Novelty check:** "宋云 末城 捍麽城 比定 位置" returned nothing on 末城.
- **Orbital signature:** a small walled town or a tati debris spread at the oasis edge. Sentinel-2 detection is marginal, and modern fields interfere.
- **Biggest reason it could be wrong:** Song Yun's li are unreliable (see *Dead ends*), and this area is densely studied.
- **Confidence:** 15 that a distinct, unpublished site exists there.

### C6. Uzun-tati = Pi-mo / Phema / Kan-cheng — KNOWN (calibration anchor)
- **Coordinates:** 37.28, 80.95 (±3 km) ([WP list](https://en.wikipedia.org/wiki/List_of_archaeological_sites_of_the_Taklamakan_and_Lop_Desert); Stein's identification, [DSR p.659](https://dsr.nii.ac.jp/toyobunko/III-2-F-c-30/V-2/page/0659.html.en)).
- Use: it sets the li scale (330 li = 93.0 km = 282 m/li). **Contradiction:** on the same scale, Pi-mo→Ni-jang should be 56 km, but Uzun-tati→Minfeng is 163 km.
  Either "200 li" is corrupt, or it counts only the sand crossing east of a Pi-mo district that reached the Keriya river.
  Significance 3. Confidence 90. Visible in Sentinel-2 (tati debris).

### C7. Yuansha (Djoumboulak Koum) and Karadong — KNOWN (calibration of the migration vector)
- **Coordinates:** Yuansha 38.867, 81.583 and Karadong 38.533, 81.867 (±2 km). Yuansha→Karadong is az 146°, 44.6 km.
  Significance 3 as context. Confidence 95. Yuansha's ring (about 300 m across) should be visible in Sentinel-2.

### C8. Endere Tang fort and Dandan Oilik — KNOWN (exclusion anchors)
- **Coordinates:** Endere fort 37.783, 83.817 (719 CE inscription; it post-dates Xuanzang, so it is excluded as his Tukhara city).
  Dandan Oilik 37.7744, 81.0731 (6th–8th c.; it was not a ruin in 644, so it is excluded as Ho-lao-lo-kia).
  ([WP Endere](https://en.wikipedia.org/wiki/Endere), [WP Dandan Oilik](https://en.wikipedia.org/wiki/Dandan_Oilik), [British Museum](https://www.britishmuseum.org/collection/term/x21364)).
  Significance 3. Confidence 95.

## Dead ends (things you checked that did not pan out, 1 line each)
- DEM "interdune flat" detector (large flats with less than 6 m relief within 1 km): **none of the five known sites** (Endere, Yuansha, Karadong, Dandan Oilik, Niya) sits on such a flat, so the method was rejected as a predictor (`flats.py`, `dem/flats_cal_*.json`).
- Song Yun's figures **[text-from-memory]** (Zuomo→Mo 1275, Mo→Hanmo 22, Hanmo→Khotan 878 li) give 234 m/li overall but 106 m/li if Hanmo = Uzun-tati. His statue legend ties Hanmo to Pi-mo, so I treated his distances as unusable for positioning.
- Ni-jang (尼壤): when the chain is solved on the DEM axes, it lands 3.8 km from the modern Minfeng county seat, i.e. under the modern oasis. That gives no desert candidate.
- Pleiades and Natural Earth hold almost nothing for the Tarim, Lop, Juyan or Khwarezm deserts (12 Pleiades places in 35–43.5 N, 76–102 E; 8 in Khwarezm), so they are useless for novelty checks there.
- **Not evaluated (search cap and blocked hosts):** Lop Nur/Loulan (Yuni, Haitou, the Sapi city of the Dunhuang geographies), Khwarezm (Tolstov's Akchadarya/Uzboy castles), Juyan (the Han county seat, Zhelu-zhang), Badain Jaran/Gobi, CORONA-based studies, Faxian's crossing from Agni to Khotan, Huntington, and the stations of the Tang Khotan-river itinerary (睢阳, 咸泊, 疏树). These are worth a second pass with search access.

## Sources
- Xiyu ji text: https://www.quanxue.cn/ct_fojia/xiyuji/xiyuji145.html ; https://zh.wikisource.org/zh-hans/%E5%A4%A7%E5%94%90%E8%A5%BF%E5%9F%9F%E8%A8%98_(%E5%9B%9B%E9%83%A8%E5%8F%A2%E5%88%8A%E6%9C%AC)/%E5%8D%B7%E7%AC%AC%E5%8D%81%E4%BA%8C
- Stein (Digital Silk Road): https://dsr.nii.ac.jp/toyobunko/VIII-5-B2-5/V-1/page-hr/0491.html.en ; https://dsr.nii.ac.jp/toyobunko/III-2-F-c-30/V-2/page/0659.html.en ; https://dsr.nii.ac.jp/toyobunko/VIII-5-B2-19/V-1/page-hr/0193.html.en ; https://dsr.nii.ac.jp/toyobunko/VIII-5-B2-9/V-3/page/0223.html.ja
- Indian Antiquary 59: https://jainqq.org/pagetext/Indian_Antiquary_Vol_59/032551/55
- Site lists and coordinates: https://en.wikipedia.org/wiki/List_of_archaeological_sites_of_the_Taklamakan_and_Lop_Desert ; https://en.wikipedia.org/wiki/Dandan_Oilik ; https://en.wikipedia.org/wiki/Endere ; https://www.wikidata.org/wiki/Q491836 ; https://en.wikipedia.org/wiki/Keriya_River ; https://en.wikipedia.org/wiki/Keriya_Town ; https://en.wikipedia.org/wiki/Niya_County ; https://aroundus.com/p/6449297-niya ; https://www.britishmuseum.org/collection/term/x21364
- Keriya delta: https://link.springer.com/article/10.1007/s11430-011-4206-1 ; https://www.geogsci.com/EN/abstract/article/1009-637X/53877 ; https://www.researchgate.net/figure/Location-of-the-Yuansha-site_fig1_5606509 ; https://xinjiangtravel.org/khotan/attraction/ancient-city-of-yuansha.html ; https://www.iranicaonline.org/articles/keriya/ ; https://www.unesco-hist.org/uploads/2018/Mapping%20a%20paleodrainage%20system%20of%20the%20Keriya%20River%20using%20remote%20sensing%20data%20and%20historical%20materials.pdf ; https://depts.washington.edu/silkroad/texts/hhshu/notes3.html
- Endere/Tukhara: https://dx.doi.org/10.1007/s11434-009-0586-4
- Koyuk Shahri: https://www.cambridge.org/core/product/8F1FC55E08A966AC0F530D1FEFF124D4/core-reader ; https://pleiades.stoa.org/places/418515134
- Popular: https://www.ntdtv.com/gb/2023/11/16/a103825528.html
- Data: Copernicus GLO-30 https://copernicus-dem-30m.s3.amazonaws.com/ ; Pleiades https://raw.githubusercontent.com/isawnyu/pleiades.datasets/main/data/gis/places.csv ; Natural Earth https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_populated_places_simple.geojson
- Scripts and outputs: `discoveries/2026-11-09-hidden-earth/data/T2/` (scripts/, dem/flow_*.json, derivations_output.txt)

```json
[
 {"id":"T2-C1","name":"Ho-lao-lo-kia (曷劳落迦) sand-buried city search box","lat":37.55,"lon":80.58,"radius_km":30,"feature_size_m":400,"signature":"partly sand-filled walled town 200-500 m; dark sherd/slag tati patches 0.1-2 km2 in interdune corridors; dead-poplar channel lines","s2_visible":true,"dem_visible":false,"significance":8,"novelty":"NOVEL-SYNTHESIS","confidence":20,"looting_sensitive":true,"category":"lost city (pilgrim text)","one_line":"Xuanzang: north of Khotan kingdom, survivor fled east to Pi-mo (Uzun-tati), already a sand mound in 644; DEM puts Pi-mo's distal fan here"},
 {"id":"T2-C2","name":"Xuanzang's old Tukhara walled town, western Endere fan","lat":37.78,"lon":83.67,"radius_km":20,"feature_size_m":250,"signature":"rammed-earth enclosure 100-300 m, round/square, possible stupa mound","s2_visible":true,"dem_visible":false,"significance":6,"novelty":"PROPOSED","confidence":35,"looting_sensitive":true,"category":"lost city (pilgrim text)","one_line":"400-li/600-li circles (282 m/li calibrated on Khotan-Pi-mo) intersect 12 km W of the post-Xuanzang Tang fort, on the DEM fan axis"},
 {"id":"T2-C3","name":"Northern Keriya trunk-axis terminal settlements beyond Yuansha","lat":39.25,"lon":81.88,"radius_km":30,"feature_size_m":1000,"signature":"dead-channel vegetation lines, sherd scatters, small enclosures 50-150 m, possible km-scale fields","s2_visible":true,"dem_visible":false,"significance":6,"novelty":"NOVEL-SYNTHESIS","confidence":12,"looting_sensitive":true,"category":"buried settlement / palaeodelta","one_line":"DEM trunk axis threading Yuansha-Karadong continues N; pre-Yuansha terminus settlements expected here (alt point 39.20,81.30)"},
 {"id":"T2-C4","name":"Lower Keriya-Niya interfluve successor to Karadong","lat":38.36,"lon":82.20,"radius_km":25,"feature_size_m":1000,"signature":"settlement cluster on dead channels; fields; confusable with modern Darya Boyi pastoral sites","s2_visible":true,"dem_visible":false,"significance":5,"novelty":"NOVEL-SYNTHESIS","confidence":12,"looting_sensitive":true,"category":"buried settlement / palaeodelta","one_line":"Yuansha->Karadong SE migration extrapolated + Niya-ruins flow line converge east of Karadong"},
 {"id":"T2-C5","name":"Song Yun's Mo city (末城), 22 li E of Hanmo/Pi-mo","lat":37.28,"lon":81.02,"radius_km":10,"feature_size_m":200,"signature":"small walled town or tati spread at oasis edge","s2_visible":false,"dem_visible":false,"significance":4,"novelty":"NOVEL-SYNTHESIS","confidence":15,"looting_sensitive":true,"category":"lost town (pilgrim text)","one_line":"22 li x 282 m/li east of Uzun-tati; likely within the known Domoko/Damagou cluster - cannot resolve"},
 {"id":"T2-C6","name":"Uzun-tati = Pi-mo (calibration)","lat":37.28,"lon":80.95,"radius_km":3,"feature_size_m":2000,"signature":"tati debris field","s2_visible":true,"dem_visible":false,"significance":3,"novelty":"KNOWN","confidence":90,"looting_sensitive":false,"category":"calibration","one_line":"Sets Xuanzang li = 282 m; exposes the Pi-mo->Ni-jang 200-li contradiction"},
 {"id":"T2-C7","name":"Yuansha and Karadong (calibration)","lat":38.867,"lon":81.583,"radius_km":2,"feature_size_m":320,"signature":"ring wall ~300 m (Yuansha); Karadong 44.6 km at az 146","s2_visible":true,"dem_visible":false,"significance":3,"novelty":"KNOWN","confidence":95,"looting_sensitive":false,"category":"calibration","one_line":"Dated NW->SE settlement migration used for C3/C4"},
 {"id":"T2-C8","name":"Endere Tang fort and Dandan Oilik (exclusion anchors)","lat":37.783,"lon":83.817,"radius_km":2,"feature_size_m":150,"signature":"walled fort; Dandan Oilik at 37.7744,81.0731","s2_visible":true,"dem_visible":false,"significance":3,"novelty":"KNOWN","confidence":95,"looting_sensitive":false,"category":"calibration","one_line":"Post-644 fort excluded as Tukhara city; 6th-8th c. Dandan Oilik excluded as Ho-lao-lo-kia"}
]
```
