# §5 METHOD — habitat (5.1a) + resistance & corridor (5.2)
_Built on a **COMBINED land-cover base**: MFE natural-veg (4.6) where present, else the SIGPAC matrix (4.5) — so riparian woodland and wetland/salada are distinct. + 25 m DEM. Single script: `19_build_combined_hab_resist_5.py` (supersedes 14+15). First-pass parameter values — **review with the teacher / lynx-corridor literature before final use**._

## 5.1a Habitat (combined base → categorical 25 m raster `habitat_51a.tif`)
Two-species logic: lynx needs scrub/forest **cover**; the rabbit (prey base) needs the scrub-grassland **ecotone** + open foraging. Where they meet = optimal. MFE adds **Riparian corridor** (dispersal along water) and **Wetland/salada** as their own classes.

| Habitat class | ha |
|---|---|
| Lynx + rabbit optimal (ecotone) — MFE mosaic + SIGPAC grazed scrub | 36,795 |
| Lynx cover (scrub/forest) — MFE + SIGPAC scrub/forest | 76,815 |
| Riparian corridor — MFE riberas | 2,716 |
| Wetland / salada — MFE humedal | 1,056 |
| Rabbit foraging (open) — pasture/grassland | 632 |
| Matrix (permeable) — dryland arable, woody | 137,935 |
| Matrix (hostile) — irrigated arable, horticulture | 91,974 |
| Non-habitat | 54,372 |

Effective lynx habitat (ecotone + cover + riparian) ≈ **116,300 ha**. Terrain/human-pressure are secondary modifiers (noted, cover type dominates).

## 5.2 Resistance surface (25 m raster)
`resistance = land-cover base × slope factor + barrier penalty`

**Land-cover base** (lynx; 1 = optimal cover … 60 = hostile crop), from the combined base:
MFE Scrub/mosaic 1 · MFE Riparian 2 · MFE Forest 3 (plantation 5) · MFE Grassland 8 · MFE Bare 15 · MFE Wetland 20; where MFE = non-natural, SIGPAC: Grazed scrub/Scrub 1 · Forest 3 · Pasture 8 · Woody 12 · Arable dryland 20 · Arable irrigated 50 · Horticulture 60 · Non-agri 25.

**Slope factor** = clip(1 + slope°/25, 1–3) — steep costs more, capped (lynx still use ravines).

**Barrier penalty** (added; rasterised from 4.4, buffered 25 m for continuity): Motorway/autovía 1000 · Railway/HS 800 · Main road 200 · Canal 150 · other 100. → near-absolute walls.

**Rabbit conditional permeability** ("visited, not lived-in"): embodied in the low ecotone/pasture base values — matrix cells with rabbit habitat cost less to cross, so the path is drawn through prey-rich ground rather than only through dense cover. (A separate rabbit-availability multiplier could be added later.)

Result: resistance 1–1150 (median 22). No-DEM eastern strip = impassable/nodata.

## Corridor (least-cost) + WWF reference
- **Single least-cost path** connecting two protected cores — **Valcuerna, Serreta Negra y Liberola (ES0000182, S-central)** ↔ **Sierra de Alcubierre (ES0000295, NW)** — via `MCP_Geometric` on the resistance surface. → `corridor_lcp_52.fgb` (93 km).
- **WWF corridor drawn as a dashed reference overlay** on the same 5.2 map (`corridor_wwf_52.fgb`) — our independent path matches **4 of 5** WWF study-area links (within 2 km).
- **Corridor swath = our precise resistance-based least-cost band** (`corridor_swath_52.tif`, 19,722 ha, kept sharp).
- **WWF corridor zone = separate swath-like layer beneath it** (`20_build_wwf_swath_52.py` → `corridor_wwf_swath_52.tif`): a soft distance gradient (0 on the WWF line → fades out at 1,500 m, 39,980 ha), pale purple, so it *suggests* the WWF corridor in the same visual language as the swath without a hard buffer. Plus the WWF corridor **line** on top. (An earlier attempt to merge the WWF buffer into the swath itself was rejected — it coarsened the precise cost-surface band.)
- ⚠ **Multi-core network attempted and REVERTED** (Session 13): an MST over 5 cores produced a sprawling, off-message result because two anchors were bad — Alcubierre's site is only 42% inside the box so its representative point fell OUTSIDE the box (clamped to the edge), and Monegros/Retuerta-Sástago collapsed to one point. A proper network would need in-box, best-habitat-cell anchors; kept the clean single path instead.
- **Least-cost path** (`MCP_Geometric` traceback, geometric, 8-connected): **93 km**, cost 10,111 (lower than the SIGPAC-only 11,374 — the combined base finds cheaper riparian/forest cover). → `corridor_lcp_52.fgb`.
- **Corridor swath** = cost-from-source + cost-from-target, cells within **2%** of the least-cost total: **19,722 ha** band. → `corridor_swath_52.tif`.
- **Cross-check:** this independent LCP aligns with **4 of the 5 WWF study-area corridor links** (within 2 km) — two methods, same route.

## Caveats / to review
- **Parameter values are a defensible first pass**, not calibrated to Iberian-lynx telemetry. Review the base/slope/barrier weights with the teacher and the CorridorDesign / WWF Autopistas Salvajes references before final maps.
- Endpoints chosen = two cores; a multi-core network (all Natura sites) LCP could follow.
- 25 m resolution (territorial); barrier walls are approximate at that grid.
- East ~8 km (Catalonia) outside the DEM → corridor logic stops at the Aragón edge there.
- Erosion (4.3) uses Stream Power Index; a full RUSLE could complement.
