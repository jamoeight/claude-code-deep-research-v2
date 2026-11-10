# Operation Hidden Earth, round 2: human-made things only

The user asked for **human-made things**: lost cities, forts, caravan stations,
tombs, canals and walled towns. Round 1's general rules still apply (see `BRIEF.md`):
no fabrication, a mandatory novelty check, honest uncertainty radii, and labels of
`KNOWN` / `PROPOSED` / `NOVEL-SYNTHESIS`.

## What is different this round
1. **Look before you claim.** You have working imagery tools. Every candidate you
   rank must have been *looked at* by you, as a Sentinel-2 chip, a DEM hillshade
   or both. Say what you saw.
   ```
   cd /home/user/claude-code-deep-research-v2/discoveries/2026-11-09-hidden-earth
   # one place: S2 true colour + DEM hillshade, saved under imagery/chips/<ID>_s2.jpg / _dem.jpg
   python3 tools/geo.py chip <lat> <lon> <half_km> imagery/chips/<ID> --label "<ID>"
   python3 tools/geo.py dem  <lat> <lon> <half_km> imagery/chips/<ID> --label "<ID>"
   # many places at once: contact sheet (S2 + DEM pairs), then Read the jpg
   python3 tools/sheet.py my_cands.json imagery/sheets/<team>_<n>.jpg --cols 4 --px 260
   #   my_cands.json = [{"id":"H2-001","lat":..,"lon":..,"half_km":1.5}, ...]   (add --nodem for S2 only)
   ```
   Prefix every chip ID with your team code, e.g. `H2-017`, so they don't collide.
   Sentinel-2 is 10 m: walled enclosures of 80 m or more, big canals, field systems, tells
   and large mounds can show. Single walls, small towers and graves cannot.
   The Copernicus DEM (30 m) shows mounds of about 3 m and higher.
   Calibrate on 2 or 3 KNOWN sites of your target type first, so you know what a hit looks like.
2. **Budget:** at most **12 web searches** in total. WebFetch is blocked for most
   hosts, so don't retry it. Spend the effort on geometry and imagery, not
   literature. View at most ~12 contact sheets.
3. **Looting rule (this repo is public).** Write your full notes, with exact
   coordinates, to `notes_private/H<n>_<slug>.md`. That folder is git-ignored and
   goes only to the user's private report. Do not write exact coordinates of
   possibly unrecorded archaeological sites anywhere else.
4. Rank by **significance × chance it is real and unrecorded**. Six strong,
   eyeballed candidates beat twenty vague ones.

## Output
`notes_private/H<n>_<slug>.md`, in the same per-candidate format as BRIEF.md, plus a line
`- Imagery: <chip file(s)>; what I saw: ...`. End with the ```json candidate
block (same fields as BRIEF.md, plus `"chip": "<path>"`).
Final reply to the lead: at most 200 words, giving the file path and the top 3.
