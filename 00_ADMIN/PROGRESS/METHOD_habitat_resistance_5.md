# §5 METHOD — habitat (5.1a) + resistance & corridor (5.2)
_Rebuilt on the new SIGPAC/MFE + 25 m DEM base (replaces the old CORINE-based habitat/resistance). Scripts: `14_build_habitat_51a.py`, `15_build_resistance_corridor_52.py`. First-pass parameter values — **review with the teacher / lynx-corridor literature before final use**._

## 5.1a Habitat (vector reclass of the 4.5 land cover)
Two-species logic: the lynx needs scrub/forest **cover**; the rabbit (prey base) needs the scrub-grassland **ecotone** + open foraging. Where they meet = optimal.

| Habitat class | From agri_class | ha |
|---|---|---|
| Lynx + rabbit optimal (ecotone) | Grazed scrub / pasto arbustivo | 26,775 |
| Lynx cover (scrub/forest) | Scrub, Forest | 72,353 |
| Rabbit foraging (open) | Pasture (open) | 3,700 |
| Matrix (permeable) | Arable dryland, Woody crops | 147,063 |
| Matrix (hostile) | Arable irrigated, Horticulture | 95,544 |
| Non-habitat | Non-agricultural | 30,676 |

Effective lynx habitat (cover + ecotone) ≈ **99,128 ha**. Terrain/human-pressure are secondary modifiers (noted, not yet applied at parcel level — cover type dominates).

## 5.2 Resistance surface (25 m raster)
`resistance = land-cover base × slope factor + barrier penalty`

**Land-cover base** (lynx; 1 = optimal cover … 60 = hostile crop):
Scrub 1 · Grazed scrub (ecotone) 1 · Forest 3 · Pasture 8 · Woody crops 12 · Arable dryland 20 · Arable irrigated 50 · Horticulture 60 · Non-agri 25.

**Slope factor** = clip(1 + slope°/25, 1–3) — steep costs more, capped (lynx still use ravines).

**Barrier penalty** (added; rasterised from 4.4, buffered 25 m for continuity): Motorway/autovía 1000 · Railway/HS 800 · Main road 200 · Canal 150 · other 100. → near-absolute walls.

**Rabbit conditional permeability** ("visited, not lived-in"): embodied in the low ecotone/pasture base values — matrix cells with rabbit habitat cost less to cross, so the path is drawn through prey-rich ground rather than only through dense cover. (A separate rabbit-availability multiplier could be added later.)

Result: resistance 1–1150 (median 22). No-DEM eastern strip = impassable/nodata.

## Corridor (least-cost)
- **Endpoints:** interior points of two protected cores — **Sierra de Alcubierre (ES0000295, NW)** ↔ **Valcuerna, Serreta Negra y Liberola (ES0000182, S-central)**.
- **Least-cost path** (`skimage.route_through_array`, geometric, 8-connected): **92 km**, cost 11,374. → `corridor_lcp_52.fgb`.
- **Corridor swath** = cost-from-source + cost-from-target, cells within **2%** of the least-cost total (`MCP_Geometric`): **26,449 ha** band (~3 km avg width). → `corridor_swath_52.tif`. Tune with `TOL`.

## Caveats / to review
- **Parameter values are a defensible first pass**, not calibrated to Iberian-lynx telemetry. Review the base/slope/barrier weights with the teacher and the CorridorDesign / WWF Autopistas Salvajes references before final maps.
- Endpoints chosen = two cores; a multi-core network (all Natura sites) LCP could follow.
- 25 m resolution (territorial); barrier walls are approximate at that grid.
- East ~8 km (Catalonia) outside the DEM → corridor logic stops at the Aragón edge there.
- Erosion (4.3) uses Stream Power Index; a full RUSLE could complement.
