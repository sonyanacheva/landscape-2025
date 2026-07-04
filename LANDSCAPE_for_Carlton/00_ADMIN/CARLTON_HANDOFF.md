# HANDOFF → Carlton: build sections §3, §4, §5 (QGIS map production)
_Read first: `README.md`, `00_ADMIN/PROJECT_HUB.md` (master map list · data · method), `00_ADMIN/HOW_WE_WORK.md`._

**Standard for every map:** CRS **EPSG:25830** · scale bar + north on every sheet · line-weight hierarchy + poché · quantified legends (ha / m / %) · match the **Geomorphology map** (our clarity benchmark) · export **300 dpi** to `04_EXPORTS/panelX/`.
**Version control:** commit via **GitHub Desktop**. Log what you finish in `00_ADMIN/PROGRESS/LOG.md`.
**Division:** Claude delivers finished analytical layers + `.qml` styles; Carlton composes, styles to standard, adds legends/scale/north, exports. Ping Claude for any layer/script/legend.

## §3 — Work area in the Iberian corridor (Panel 1, top)
| Map | Scale | Data | Status |
|---|---|---|---|
| 3.1 Spain + "Sierras Litorales del Mediterráneo" corridor highlighted | 1:3,000,000 | corredores_prioritarios + provinces | **HAVE** — restyle |
| 3.2 Cataluña–Aragón + territorial units, locate work area | 1:500,000 | admin + corridor | **HAVE** |
| 3.3 Work area + Natura 2000 (legend: site ID / name / **ha**), cities, river | 1:50,000 | Natura2000 + towns | HAVE + Claude auto-ha legend |
| 3.4 Critical points: corridor discontinuities (canals/roads/rail), Natura sites to connect | 1:50,000 | barriers + OSM | HAVE + OSM script |

## §4 — Territorial analysis (Panel 1)
| Map | Data | Status |
|---|---|---|
| 4.1 Hydrography (rivers/streams/drainage/Valcuerna) | CHE + DEM streams | **HAVE** — restyle |
| 4.2 Geomorphology (gypsum badlands, saladas) | GEODE + DEM | **HAVE** (benchmark) |
| 4.3 Flow accumulation + erosion + flood zones | DEM (5 m) + SNCZI | **Claude produces rasters → Carlton styles** |
| 4.4 Human pressure + barriers + underpass/bridge catalogue | OSM + buildings | OSM script + HAVE |
| 4.5 Agricultural matrix (+ **ha**) | SIGPAC | **Claude produces → Carlton styles** |
| 4.6 Forest / scrub / natural veg | MFE | **Claude produces → Carlton styles** |

## §5 — Species-specific ecological diagnosis (Panel 2)
| Map | Data | Status |
|---|---|---|
| 5.1a Lynx + rabbit habitat (2 colours) | reclass 4.5/4.6 + DEM | **Claude produces → Carlton styles** |
| 5.1b Lynx-path storyboard + classified views | LCP + viewpoints | Claude gives geometry → ChatGPT renders |
| 5.1c Ecological sections (elevation + veg heights) | DEM 2 m + canopy (LiDAR Height Extractor) | Carlton builds sections |
| 5.2 Resistance map + corridor (rabbit = lower resistance) | reclass + slope + human | **Claude produces → Carlton styles** |

## Data status (what's ready vs incoming)
- **HAVE:** geology GEODE, hydrography, contours, Natura 2000, corridor, admin/municipios, buildings, orthophoto, MFE-Huesca, cañadas (RGVP).
- **Incoming:** SIGPAC box municipios (plugin, in `01_DATA/.../sigpac` or `downloads/`), DEM 5 m (Aragón WCS), MFE-Zaragoza, OSM (script), MDT02 2 m (later, interventions).
