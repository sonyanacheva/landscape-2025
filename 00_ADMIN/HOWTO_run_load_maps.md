# HOW TO LOAD + STYLE THE PROCESSED MAPS — for Sonya
_This replaces the old per-map style scripts (`02_style_…`, `04_style_…` — deleted). There is now **one** script: `07_SCRIPTS\load_maps.py`._

## What it does
For every processed layer in `03_PROCESSED\`, in one run, it:
1. loads the layer (skips it if it's already loaded),
2. applies its full classified styling (legend on the left),
3. saves a `.qml` sidecar next to the `.fgb` and loads it back (so the `.qml` becomes the source of truth),
4. drops it into its own layer group.

It's safe to re-run — nothing duplicates.

## Run it (once per work session)
1. Make sure the delivered `.fgb` files are in
   `…\LANDSCAPE_for_Carlton\03_PROCESSED\` (that's where Claude puts them).
2. In QGIS: **Plugins ▸ Python Console ▸ Show Editor** (the little page icon).
3. **Open** `…\LANDSCAPE_for_Carlton\07_SCRIPTS\load_maps.py`.
4. Click **Run** (green ▶). Done — the maps appear grouped and styled, legends on the left.

## After the first run — even easier
Once a layer has been run once, its `.qml` exists next to the `.fgb`, so you can just
**drag the `.fgb` onto the map** and it styles itself. You don't have to run the script again
unless there are new layers or Claude changed a style.

## If a layer fails to load ("Layer failed to load")
It's almost always the path. Open `load_maps.py` and check the **`BASE`** line near the top
points to your repo folder:
`C:\Users\Sonya\Desktop\Work_Vault\_Github\New folder\landscape-2025\LANDSCAPE_for_Carlton`
Tip: if you **save your QGIS project (`.qgz`) inside the repo**, the script auto-finds the data
even if `BASE` is wrong — so saving the project there makes it bulletproof.

## Good to know
- **Currently styled by the script:** 4.5 Agricultural matrix · 4.6 Forest/scrub/natural veg · 4.x Cañadas · 4.x-b Cañada × land cover. More get added as they're built (Claude just adds one line).
- **Re-running after a style change:** `RESTYLE_LOADED = True` at the top means a re-run re-applies Claude's latest styles to layers already loaded. If you've hand-tweaked a layer in the UI and want to keep it, set that to `False` before re-running.
- **The vault layers you exported** (hydro, geology, human, etc.) already carry their own embedded styles + `.qml`, so those load styled on their own — `load_maps.py` is only for the processed analytical layers in `03_PROCESSED\`.
