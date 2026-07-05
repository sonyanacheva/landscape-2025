# HOW TO GRAB THE REMAINING MAP DATA — step by step
_Written for someone who hasn't touched QGIS in a while. Take it slowly; each item is independent. After each one, drop the file into the folder shown and tell Claude. CRS everywhere is **EPSG:25830**. Study box: `714913, 4582331 → 784950, 4639785`._

There are **4 things left**. In priority order: **1) DEM 5 m**, **2) Admin boundaries**, **3) WWF corridor**, **4) SNCZI flood** (no rush).

---

## 0. First, open your project cleanly
1. Open **QGIS**.
2. If you have a project file, open it (**Project ▸ Open**). If not, **Project ▸ New**, then **Project ▸ Save As** and save it **inside** `…\landscape-2025\` (this makes the scripts auto-find your data even if a path is wrong).
3. Bottom-right of the window, confirm the CRS reads **EPSG:25830**. If it says something else, click it and set **ETRS89 / UTM zone 30N (EPSG:25830)**.

---

## 1. DEM 5 m  ★ highest value (unlocks flow/erosion 4.3 and all of §5)
This is fully automated by a script.
1. In QGIS: **Plugins ▸ Python Console**.
2. In the console panel, click the **Show Editor** button (the little page/notepad icon).
3. In the editor, click the **Open Script** (folder) icon and open:
   `…\LANDSCAPE_for_Carlton\07_SCRIPTS\10_fetch_dem5m_wcs.py`
4. You don't need to edit anything — your Mac path is already in the `BASES` list near the top. (If you ever move the repo, add the new path to that list.)
5. Click the green **Run** ▶ arrow.
6. Watch the console. It should print `saved DEM: …\01_DATA\DEM\dem_5m_box.tif` plus hillshade and slope.
   - **If it errors on the coverage id or size:** the console prints a GetCapabilities link and fallback notes. Copy the message to Claude and we'll adjust.
7. **Result lands in:** `…\01_DATA\DEM\dem_5m_box.tif`. Tell Claude when it's there.

---

## 2. Admin boundaries (provinces / municipios / regions)  → finishes §3.1, 3.2, 3.3
Because the whole area is in Aragón, the easiest source is the **IDEAragón WFS** — it streams straight into QGIS, already in EPSG:25830. A WFS is just a map service you connect to once and then pull layers from.

### 2a. Add the IDEAragón WFS connection (once)
1. Menu: **Layer ▸ Add Layer ▸ Add WFS / OGC API Layer…**
2. Click **New**.
3. Fill in:
   - **Name:** `IDEAragon`
   - **URL:** paste this exactly:
     ```
     https://icearagon.aragon.es/Visor2D?service=WFS&request=GetCapabilities
     ```
4. Click **OK**, then **Connect**. A list of available layers appears (this can take a few seconds).

### 2b. Find and add the boundary layers
1. In the search/filter box above the list, type `limite` or `municip` or `administra`.
2. Look for layers named like **límites municipales**, **provincias**, **comunidad autónoma / límite autonómico**. Click one to select it (Ctrl-click to grab several).
3. Click **Add**, then **Close**. They'll draw on the map.
   - _Tip: if IDEAragón's list is overwhelming, just grab the municipios layer first; provinces/region can follow._

### 2c. Save each as a file (so Claude can use it)
For each boundary layer you added:
1. **Right-click the layer** in the Layers panel ▸ **Export ▸ Save Features As…**
2. **Format:** GeoPackage. **CRS:** EPSG:25830.
3. **File name:** save into `…\01_DATA\context\` with a clear name, e.g. `municipios.gpkg`, `provincias.gpkg`, `comunidades.gpkg`.
4. Click **OK**.
5. Tell Claude which files landed in `01_DATA\context\`.

**National fallback (if you need all-Spain provinces for the 3.1 map):** go to `https://centrodedescargas.cnig.es/`, section "Líneas límite municipales, provinciales y autonómicos", download the SHP, unzip into `01_DATA\context\`.

---

## 3. WWF "corredores prioritarios" corridor  → §3.1, 3.2, 3.4
This is the one layer **not** on the public portals. Two options:
- **Best:** it's in Sonya's old vault. When she's free, she runs `07_SCRIPTS\11_export_vault_layers.py` with the vault project open — it exports the corridor (and other §3 layers) to `01_DATA\context\` automatically.
- **If the vault copy is gone:** request the "corredores prioritarios / Sierras Litorales del Mediterráneo" layer from **WWF España**, or we substitute MITECO's national ecological-connectivity layer (coarser). Ask Claude and we'll pick.

_You can't grab this one yourself right now, so don't worry about it — flag it for Sonya._

---

## 4. SNCZI flood zones  → 4.3 overlay (LOW priority, needs the DEM first anyway)
Two ways:
- **Quick look (no download):** **Layer ▸ Add Layer ▸ Add WMS/WMTS Layer ▸ New**, URL:
  ```
  https://sig.miteco.gob.es/93/mapasrasters/mapas/Servicios/InundacionesZI/MapServer/WMSServer?request=GetCapabilities&service=WMS
  ```
  Connect, add the flood-zone layers. This shows them but you can't clip them.
- **Data to clip:** `https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/agua/` ▸ download **Zonas Inundables lámina T=100** and **T=500** (Peninsula, ETRS89) ▸ unzip into `01_DATA\hydro\`.

_Skip until the DEM is in and we're building 4.3._

---

## Quick reference: where each file goes
| Item | Save to |
|---|---|
| DEM 5 m (`dem_5m_box.tif`) | `01_DATA\DEM\` |
| Admin boundaries (`.gpkg`) | `01_DATA\context\` |
| WWF corridor (`.gpkg`) | `01_DATA\context\` |
| SNCZI flood (SHP) | `01_DATA\hydro\` |

After each drop, tell Claude what landed where and it gets processed into the maps.
