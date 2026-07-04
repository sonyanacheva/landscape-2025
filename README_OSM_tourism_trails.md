# OSM Tourism & Trails → Carlton
**Two OSM extracts for the study box** (fetched 2026-07-04, Overpass). Feed §6 masterplan + §7 interventions + §5.1b viewpoints.
⚠ **Both are EPSG:4326 (WGS84) — reproject to EPSG:25830** before use. Style with a **categorized renderer** on the type field (`tourism` / `historic` / `natural`) to get per-type symbols; use `name` for labels.

---

## `POINTS.geojson` — 222 points
Recreation / heritage / scenic nodes. 133 are named. Groups:

| Group | Tags (count) | Use for |
|---|---|---|
| **Scenic / summits** | `natural=peak` (49), `tourism=viewpoint` (11) | §6 scenic nodes · **§5.1b lynx-path storyboard viewpoints** |
| **Heritage / monuments / ruins** | `historic`: ruins 13, archaeological_site 12, castle 9, monument 8, memorial 8, wayside_cross 6, wayside_shrine 5, tomb 3, +others (~76) | §6 cultural-route stops, interpretation |
| **Interpretation / attractions** | `tourism`: information 23, attraction 16, artwork 9, museum 5 (53) | §6 signage/trailhead network, visitor points |
| **Stay / shelter** | `amenity=shelter` 8, `tourism`: caravan_site 6, camp_site 5, chalet 1 (20) | §6/§7 rest stops, camping, trail refuges |
| **Support** | place_of_worship 5, parking 3 | trailheads / access points |

_(A few stray `highway=track` points slipped in — ignore or filter them out.)_

## `LINES.geojson` — 10,138 features (the walking / MTB network)
| Type | Count | Note |
|---|---|---|
| `highway=track` | 9,378 | dominant — agricultural/rural tracks (the de-facto walking/MTB surface) |
| `highway=path` | 541 | footpaths |
| `highway=footway` | 162 | |
| `highway=steps` | 40 | |
| `highway=cycleway` | 3 | |
| `route=hiking` (relations) | 10 | named long-distance / GR routes |
| `route=mtb` | 2 | mountain-bike routes |

⚠ The file has a few **stray Point/Polygon geometries** (from relation members/areas) — in QGIS run *Filter → geometry type = Line* or Export → geometry LineString to keep the network clean.

---

## Where each goes (map by map)
- **§6 Ecotourism masterplan** — the core use. Combine POIs (heritage + attractions + viewpoints + shelters/campsites) with the **cañadas (RGVP)** and this trail network to design the visitor routes, nodes and rest stops.
- **§7 Interventions (1:5000 sites)** — local `path`/`track` lines + shelters/viewpoints to place trailheads, rest points and signage on each site.
- **§5.1b Lynx-path storyboard** — `viewpoint` + `peak` give the section/journey viewpoints.
- **§4.4 Human pressure** — the path/track density is also a recreational-access layer; overlay lightly if useful.

## Notes / caveats
- **Cañadas are NOT in here** — the legal vías pecuarias network is your **RGVP** layer (already in hand). OSM tracks/paths only *complement* it. Keep them separate.
- Rural arid box → accommodation is sparse (expected); `track` dominates the network.
- `historic=*` is one tag that already catches ruins, castles, monuments and memorials — no separate "monument" query needed.
- These are §6/§7 (**Priority 3 / later**) data — gathered ahead of schedule, park until the masterplan phase.
