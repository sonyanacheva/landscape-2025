# HOW TO GRAB THE 2 m DEM + LiDAR CANOPY (for §7 / §5.1c / §8 sections)
_The last data still needed. Only for the FIVE small intervention tiles (not the whole box), so downloads are small. These give fine terrain + tree/scrub heights for the 1:5000 site plans and the barranco/ecological sections. CRS EPSG:25830._

## The five tiles (where to look)
All five `grid_1km` cells cluster near Candasnos / lower Valcuerna, roughly **753,500 → 765,000 E · 4,590,000 → 4,599,000 N** (EPSG:25830). Load `01_DATA\context\grid_1km.gpkg` in QGIS to see them; that's the area to download for.

Tile centres (25830): (758505, 4590733) · (754071, 4598176) · (759084, 4593441) · (764514, 4593081) · (758242, 4598181).

---
## 1. MDT02 — 2 m terrain model  ★ needed for all sections
Source: **CNIG Centro de Descargas** → `https://centrodedescargas.cnig.es/`
1. Search / navigate to the area (Fraga / Candasnos, Huesca). Use **"Modelo Digital del Terreno – MDT02"** (2 m, from PNOA LiDAR).
2. On the map selector, pick the sheet(s) that cover the five tiles above (the cluster spans one or two MTN50 sheets). If unsure, select by the bounding box.
3. Download the GeoTIFF/ASC tiles → save into `01_DATA\DEM\mdt02\`.
4. Tell Claude — I'll clip each 1 km tile and build the fine sections.
   - _Alt (whole box, heavier): the Aragón WCS in `10_fetch_dem5m_wcs.py` can also serve 2 m; set `RES=2` and a small extent, but the CNIG per-sheet download is cleaner for just 5 tiles._

## 2. Canopy / scrub height  ★ needed for §5.1c + §8 vegetation sections
The sections need tree/scrub HEIGHTS, not just ground. Two routes:

**Route A — LiDAR Height Extractor plugin (you already have it, easiest):**
1. Download the **PNOA LiDAR point cloud** (`.laz`) for the tile area from CNIG (`Centro de Descargas` → **"PNOA LiDAR"** → second coverage if available → the sheets over the five tiles) → `01_DATA\DEM\lidar\`.
2. Run the **LiDAR Height Extractor** plugin on those `.laz` tiles to produce a canopy-height raster (vegetation height above ground).
3. Save the height raster → `01_DATA\DEM\canopy\`.

**Route B — surface-minus-terrain (nDSM), if the plugin is fiddly:**
1. From CNIG also grab **MDS02** (2 m digital *surface* model) for the same sheets.
2. In QGIS: **Raster ▸ Raster Calculator** → `MDS02 - MDT02` → canopy/scrub height raster → `01_DATA\DEM\canopy\`.

---
## What it unlocks
- **5.1c ecological sections** — elevation + tree/scrub heights along the transects.
- **§7 five sites (1:5000)** — plan + section per site, existing vs proposed, via QGIS **Atlas** over `grid_1km`.
- **§8 barranco sections** — the phased cohabitation sections with real terrain + vegetation profiles.

## Notes
- Small area = small files; no need for the whole box at 2 m.
- If CNIG's selector is confusing, download by drawing the bounding box above; or send Claude the sheet names and we'll confirm.
- Save under `01_DATA\DEM\` (mdt02 / lidar / canopy subfolders) and tell Claude what landed where.
