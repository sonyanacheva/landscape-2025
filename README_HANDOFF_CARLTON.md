# LANDSCAPE — data handoff for Carlton
_Candasnos · Barranco de Valcuerna · Los Monegros · CRS **EPSG:25830** · study box `714913,4582331 → 784950,4639785`_

This package is the **raw source data** to start the territorial maps (§3–§5) in **QGIS with PyQGIS scripts**. Read `00_ADMIN/PROJECT_HUB.md` (master map list · data · method) and `00_ADMIN/CARLTON_HANDOFF.md` first.

---
## WHAT'S IN THIS ZIP

```
01_DATA/
  landcover/sigpac/        51 SIGPAC gpkg — every municipio whose parcels fall in the box
  landcover/mfe/           MFE Huesca (province 22) — Mapa Forestal
  infrastructure_osm/vias_pecuarias/  RGVP_SHP.zip — national vías pecuarias (cañadas)
07_SCRIPTS/                01_fetch_osm.py, 02_style_agri_matrix_45.py
00_ADMIN/                  full context: hub, checklist, handoff, downloads routes, municipios, log
README.md, PRODUCTION_PLAYBOOK.md
```

### SIGPAC (map 4.5 — agricultural matrix)
- **51 `*_rec_2026_*.gpkg`** files. These are the ONLY municipios (of 468 in the full Huesca+Zaragoza dump) whose parcels actually intersect the study box — verified by geometry, not bounding box.
- Each gpkg: default layer **`recinto`**, CRS **EPSG:4258** (reproject to 25830). Irrigation field `coef_regadio`; land-use codes in the `cod_usosigpac` lookup layer. Reclass table + ha logic are in `07_SCRIPTS` / the log.
- Whole municipios are included (not pre-clipped) so you can clip to the box in QGIS and keep full attributes.

### MFE (map 4.6 — forest / scrub / natural veg)
- **Huesca (22) only.** **Zaragoza (50) is NOT included — still to source** (see below). The box straddles both provinces, so 4.6 needs Zaragoza too.

### Cañadas / vías pecuarias (map 4.x)
- National RGVP shapefile (Ley 3/1995). Clip to box in QGIS.

---
## WHAT'S MISSING — please source (WCS-first, to save download time)

| Data | Map | Best route | Notes |
|---|---|---|---|
| **DEM 5 m** | 4.1–4.3, sections | **Aragón WCS** (one pull, whole box, no tiles) | `https://icearagon.aragon.es/arcgis/services/AragonReferencia/mde/MapServer/WCSServer?request=GetCapabilities&service=WCS&version=1.0.0` → pick 5 m DTM → set extent to box → save GeoTIFF |
| **MFE Zaragoza (50)** | 4.6 | 1-file (MITECO Mapa Forestal) | Huesca already here; add Zaragoza |
| **OSM infra** (roads/rail/canals/bridges/paths) | 4.4, 6, 7 | QuickOSM plugin or `07_SCRIPTS/01_fetch_osm.py` | one Overpass query for the box |
| **SNCZI flood zones** | 4.3 | 1-file download | flood overlay |
| **MDT02 2 m DEM** | 7, 8 (interventions) | WCS/CNIG, later | only the 5 intervention tiles |

### ⚠️ NOT in this package — lives in Sonya's older QGIS vault, not the clean folder
The log lists these as "HAVE," but they are **not physically in `01_DATA/`** — they're in the previous project (`x_LANDSCAPE` / `QGIS_007.qgz`): **geology (GEODE), hydrography (CHE), contours, Natura 2000, admin/municipios, buildings, orthophoto**. Sonya needs to **export these from the old project** (or you re-download) before §3/§4 can be fully built.

---
## SANDBOX / FILE NOTES (learned the hard way)
- **Large GeoPackages can corrupt when written to the synced folder.** For processed outputs to the mount, use **FlatGeobuf `.fgb`**, not `.gpkg`.
- SIGPAC plugin gpkgs are **EPSG:4258**, layer `recinto`.
- Standard for every sheet: scale bar + north, line-weight hierarchy + poché, quantified legends (ha/m/%), match the **Geomorphology map** as the clarity benchmark, export 300 dpi.
- Version control via **GitHub Desktop**; heavy geodata is git-ignored (that's why it's shipped as this zip, not in the repo).
