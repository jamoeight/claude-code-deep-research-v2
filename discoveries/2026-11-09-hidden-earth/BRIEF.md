# Operation Hidden Earth — shared brief for all research teams

**Mode:** DISCOVERY (see `SKILL.md` in the repo root, Co-Scientist / Aletheia pattern):
generate candidates, critique them yourself, keep only what survives, and say
"cannot resolve" when the evidence is too thin.

## Mission
Find things on Earth that matter a lot and whose existence or exact location is
**not established**: lost cities, unconfirmed craters, biologically unsurveyed
forests, unexplored sinkholes and waterfalls, lost colonial sites, unrecorded
earthworks, newly formed landscape features. Do this by **aggressively joining
independent pieces of evidence**, such as an ancient itinerary plus a river
paleochannel plus a pottery scatter report, or a tektite age plus a gravity
anomaly plus a DEM depression. The result is a **concrete location** that someone
can open in Google Earth.

Pattern matching that counts as a real contribution:
- Triangulation: two or more independent lines of evidence (texts, maps,
  geology, ecology, datasets, prior surveys) that converge on one place.
- Gap analysis: where a known phenomenon's distribution (geoglyphs, craters,
  sky-island forests) predicts more examples, but no one has surveyed.
- Precedent transfer: a discovery method that worked once, such as Mount Mabu
  found on Google Earth or Valeriana found in an old environmental lidar survey,
  applied to the next most likely place.
- Contradiction mining: where two published sources disagree and the
  disagreement points at an unexamined place.

## Hard rules
1. **No fabrication.** Every factual claim gets a source URL that you actually
   opened or saw in search results. If you derive coordinates yourself, show the
   derivation (distances, bearings, which features).
2. **Novelty check is mandatory.** Before you call something new, search for it
   (the place name, the coordinates, the "candidate site for X" phrasing) and
   label it:
   - `KNOWN`: already identified or excavated. Include it only as context or a
     calibration example.
   - `PROPOSED`: someone else has proposed this location. Cite them; you may
     add new supporting or contradicting evidence.
   - `NOVEL-SYNTHESIS`: a location or claim we could not find published. These
     are the prize.
3. Give each candidate **decimal lat/lon (WGS84)** and an **uncertainty radius
   in km**. Be honest about it; a 30 km radius is fine if that is what the
   evidence supports.
4. Say what the feature should **look like from orbit**: size in metres, shape,
   tone or vegetation contrast, relief. Say whether it should be visible in
   10 m Sentinel‑2 imagery or 30 m elevation data, or whether it needs
   sub‑metre imagery or lidar. The lead runs imagery checks centrally with
   Sentinel‑2 L2A (10 m) and Copernicus DEM GLO‑30, and sends the user Google
   Earth links.
5. **Ethics:** do not look for uncontacted peoples. Do not target military or
   security sites. For undocumented archaeological candidates in regions with
   active looting, set `looting_sensitive: true`.
6. Quality over quantity: **6–12 candidates per team**, ranked. One strong
   `NOVEL-SYNTHESIS` beats ten restated legends.

## Tools and network
- Use **WebSearch** and **WebFetch** for research. `curl` from the shell
  cannot reach most websites.
- The shell **can** reach: AWS S3 open data (`copernicus-dem-30m`,
  `sentinel-cogs`, `elevation-tiles-prod`, `esa-worldcover`, `maxar-opendata`),
  Google Cloud Storage public data, `raw.githubusercontent.com` (GitHub-hosted
  datasets), and PyPI. Python 3 has numpy, scipy, rasterio, pyproj, shapely,
  scikit-image and mgrs. Use them for distance and bearing math or small
  dataset pulls if that helps. Do **not** do bulk imagery downloads; the lead
  handles imagery.
- Save scratch files under `discoveries/2026-11-09-hidden-earth/data/T<n>/`.

## Output (required)
Write your full notes to `discoveries/2026-11-09-hidden-earth/notes/T<n>_<slug>.md`:

```
# T<n> — <team name>
## Method (what you joined, what you searched; 5-10 lines)
## Candidates (ranked)
### C1. <name> — <KNOWN|PROPOSED|NOVEL-SYNTHESIS>
- Coordinates: <lat>, <lon> (±<r> km)
- What it would be / why it matters (significance 1–10):
- Evidence chain (numbered, each with source URL):
- Novelty check (what you searched, what you found):
- Orbital signature (size, shape, tone; S2-visible? DEM-visible?):
- Biggest reason it could be wrong:
- Confidence (0-100):
...
## Dead ends (things you checked that did not pan out, 1 line each)
## Sources
```

End the file with a fenced ```json block holding a list of candidate objects:
`{"id":"T<n>-C<k>","name":..., "lat":..., "lon":..., "radius_km":...,
"feature_size_m":..., "signature":..., "s2_visible":true/false,
"dem_visible":true/false, "significance":1-10, "novelty":"KNOWN|PROPOSED|NOVEL-SYNTHESIS",
"confidence":0-100, "looting_sensitive":true/false, "category":..., "one_line":...}`

Your **final reply** to the lead should be at most 250 words: the file path, the
number of candidates, and the top 3, each with one line.
