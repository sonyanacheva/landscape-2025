# FILE STRUCTURE — where everything lives (for Sonya / her Claude)
_This is the layout every script expects. If you set this up once, the scripts find everything on their own. All scripts resolve the base folder automatically (BASE → saved-project folder → folder-picker), so you rarely need to touch paths._

## The one thing that matters: the repo root
Everything lives under **`landscape-2025\LANDSCAPE_for_Carlton\`** — that folder is the scripts' `BASE`. On Sonya's machine that is currently:
`C:\Users\Sonya\Desktop\Work_Vault\_Github\New folder\landscape-2025\LANDSCAPE_for_Carlton`

Tip: **save your QGIS project (`.qgz`) inside `landscape-2025\`** — then the scripts auto-detect the folder even if the `BASE` line is wrong, and you never edit paths.

## Expected tree
```
LANDSCAPE_for_Carlton\
├─ 00_ADMIN\                     ← docs (this file, LOG, HOWTOs, data requests)
├─ 01_DATA\                      ← RAW inputs (git-ignored, big)
│  ├─ DEM\                       ← script 10 writes dem_5m_box.tif here
│  ├─ context\                   ← script 11 writes the §3 bundle here
│  ├─ landcover\  (sigpac\ mfe\) ← SIGPAC gpkgs, MFE shapefiles
│  ├─ hydro\  geology\  human\   ← CHE water, GEODE, buildings/pressure
│  ├─ infrastructure_osm\        ← OSM roads/rail/canals/crossings
│  └─ tourism\                   ← parked §6 OSM points/trails
├─ 03_PROCESSED\                 ← Claude's finished .fgb layers (+ .qml, previews)
├─ 04_EXPORTS\                   ← your 300 dpi map exports (make as needed)
└─ 07_SCRIPTS\                   ← all the .py scripts
```

## Which script reads/writes what
| Script (run in QGIS) | Needs | Writes |
|---|---|---|
| `load_maps.py` | `03_PROCESSED\*.fgb` | applies styles + `.qml` sidecars |
| `10_fetch_dem5m_wcs.py` | internet (Aragón WCS) | `01_DATA\DEM\dem_5m_box.tif` + hillshade + slope |
| `11_export_vault_layers.py` | old vault `QGIS_007.qgz` **open** | `01_DATA\context\*.gpkg` |
| `01_fetch_osm.py` | internet (Overpass) | `01_DATA\infrastructure_osm\*` |

## If a script can't find things
It won't dump a confusing traceback — it prints what it looked for and **either lets you pick the folder in a dialog** or tells you exactly which line to edit. Just follow that message.

## For Sonya's Claude (Cowork)
If folders are missing, you can create the empty tree above under `LANDSCAPE_for_Carlton\` (the `01_DATA\` subfolders especially), so incoming downloads have a home. The scripts create their own output subfolders (`DEM\`, `context\`) automatically, so this is only to pre-place raw downloads tidily.
