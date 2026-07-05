# DATA REQUEST → Sonya
_What Claude needs to unblock the rest of Carlton's scope (§3, §4, §5). CRS everywhere **EPSG:25830**. Study box: 714913,4582331 → 784950,4639785._

**Two kinds of items:** (A) **export from the old vault** (`x_LANDSCAPE / QGIS_007.qgz`) — you already own these, just export them clean; (B) **fresh downloads** not in the vault.

**How to export from the vault (A):** right-click layer ▸ Export ▸ **Save Features As** ▸ *GeoPackage* ▸ CRS **EPSG:25830** ▸ save into the folder shown. Small layers → GeoPackage is fine. (Only big rasters go to GeoTIFF; only large processed layers use `.fgb`.)

---
## ★ PRIORITY 1 — the two "master keys" (each unlocks a whole cluster)

### DEM 5 m  → unlocks 4.1 streams, 4.3 flow/erosion, 5.1c sections, 5.2 resistance
- **Just run `07_SCRIPTS\10_fetch_dem5m_wcs.py`** in QGIS (Python Console ▸ open ▸ Run). It connects the Aragón WCS, clips to the box, saves `01_DATA\DEM\dem_5m_box.tif` + hillshade + slope. If it errors on the coverage id or size, the script prints the GetCapabilities URL + fallbacks. **Send `dem_5m_box.tif` back.**

### Vault export bundle  → unlocks all of §3, plus 4.1 and 4.2
- **Just run `07_SCRIPTS\11_export_vault_layers.py`** with the **old vault `QGIS_007.qgz` open** — it fuzzy-matches and exports the layers below to `01_DATA\context\` (reprojected to 25830). Check its MISSING list at the end and tweak name substrings if needed. Then zip `01_DATA\context\` back.
Layers it exports (for reference):
1. **Priority corridors** — `corredores_prioritarios` (the WWF/priority network, includes *"Sierras Litorales del Mediterráneo"*). → 3.1, 3.2
2. **Natura 2000 Aragón** — LIC/ZEC + ZEPA **and** `ESPACIOS_H1–H3`. **Keep the site-code and site-name fields** (needed for the auto-ha legend). → 3.3, 3.4
3. **Administrative boundaries** — CCAA + provinces (+ municipios if a separate layer). → 3.1–3.4
4. **Towns / populated places** (with name field). → 3.2, 3.3
5. **Critical points** — `Zonas_Criticas` + the railway/road **crossing/barrier** layers. → 3.4

---
## ★ PRIORITY 2 — completes §4 territorial analysis

From the **vault** → `01_DATA\` subfolders (GeoPackage, 25830):
6. **CHE hydrography** (Ebro ES091: rivers, channels, drainage, **lagoons incl. Hunilla**, reservoirs) → `01_DATA\hydro\` → 4.1, 3.3 river
7. **GEODE geology** → `01_DATA\geology\` → 4.2 (benchmark map, restyle)
8. **Contours** → `01_DATA\hydro\` → 4.1/4.2 context
9. **Human presence** — buildings, activity zones, 250 m buffers, railway crossings → `01_DATA\human\` → 4.4

**Fresh downloads:**
10. **MFE Zaragoza** — `MFE50_50` (SHP) from MITECO Mapa Forestal → `01_DATA\landcover\mfe\`. _(Huesca already in; this fills the box for 4.6 — I re-run one script.)_
11. **OSM infrastructure** — run `07_SCRIPTS\01_fetch_osm.py` in QGIS (or QuickOSM for the box). Writes to `01_DATA\infrastructure_osm\`. → 4.4, 3.4 barriers
12. **SNCZI flood zones** — 1-file download (MITECO/SNCZI) → `01_DATA\hydro\` → 4.3 overlay

---
## ○ PRIORITY 3 — later (§6 / §7 / §8, not needed yet)

From the **vault** (export when we reach §6):
13. **Tourism POIs** — `POI's.gpkg`, `BTN_POI` → `01_DATA\tourism\` → §6 masterplan
14. **1 km grid + sections** (`SECTION A`, `SECTIONS 1KM`, `MY_SECTIONS`) + `Intervention strategies` → §6, §7
15. **MDT02 2 m DEM** — only the 5 intervention tiles (WCS/CNIG) → `01_DATA\DEM\` → §7, §8

**Do NOT bring across:** the multi-GB gpkgs (PROJECT_LAYERS/OUTPUT/CLIPPED), `copy copy copy` layers, `OLD LAYERS`, CORINE land-cover (replaced by SIGPAC/MFE), old CORINE-based habitat/resistance (being rebuilt).

---
### One-line summary to unblock the most, fastest
**DEM 5 m (WCS) + the vault `context\` bundle (corridors, Natura 2000, admin, towns, critical points).** Those two together open all of §3 and most of §4. MFE-Zaragoza + OSM are quick follow-ups.
