# GET THE MISSING DATA YOURSELF — routes + exact endpoints
_Verified 2026-07-04. The study box is entirely in **Aragón**, so most layers come straight into QGIS via OGC services (WFS/WMS/WCS) already in **EPSG:25830** — no plugin required, no manual reprojection. Drop everything into `01_DATA\...`; Claude clips + processes._

## How to add an OGC service in QGIS (once per service)
- **WFS (vector, downloadable):** Layer ▸ Add Layer ▸ **Add WFS/OGC API Layer** ▸ New ▸ paste the GetCapabilities URL ▸ Connect ▸ tick the layer(s) ▸ Add. Then right-click ▸ Export ▸ Save Features As ▸ GeoPackage into the target folder.
- **WMS (image overlay only):** Layer ▸ Add ▸ **Add WMS/WMTS Layer** ▸ New ▸ paste URL ▸ Connect ▸ pick layer.
- **WCS (raster/DEM):** Layer ▸ Add ▸ **Add WCS Layer** (script 10 already automates the DEM one).

---
## The 4 gaps, best route each

### 1. DEM 5 m  ★ master key (4.3, §5)
**Run `07_SCRIPTS\10_fetch_dem5m_wcs.py`** (Aragón WCS). If the coverage id errors, the script prints the GetCapabilities URL. WCS portal: `https://idearagon.aragon.es/wcs.jsp`. → `01_DATA\DEM\`

### 2. §3 context bundle (§3.1–3.4)
Two of these are one WFS connection each; use **IDEAragón WFS** — GetCapabilities:
`https://icearagon.aragon.es/Visor2D?service=WFS&request=GetCapabilities`
- **Natura 2000 (ZEC/ZEPA)** + **ESPACIOS naturales** — pick the RN2000 / protected-spaces layers → `01_DATA\context\`.
  - National fallback (shp/GeoJSON, all Spain): MITECO RN2000 → `https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/biodiversidad/rn2000.html`
- **Admin boundaries** (provinces / municipios / CCAA) — from IDEAragón WFS (Aragón) **or** CNIG for all-Spain (needed for the 3.1 national map):
  `https://centrodedescargas.cnig.es/` ▸ "Líneas límite municipales, provinciales y autonómicos" (SHP, ETRS89) → `01_DATA\context\`
- **National / Iberia outline** (map 3.1 backdrop): **Natural Earth** Admin-0 Countries (public domain, 1:10m/1:50m):
  `https://www.naturalearthdata.com/downloads/` → Cultural ▸ Admin 0 – Countries. → `01_DATA\context\`
- **WWF "corredores prioritarios" (Sierras Litorales del Mediterráneo)** — ⚠ **not on the open portals.** This one really is **vault-only**: export it via `11_export_vault_layers.py`. If the vault copy is lost, request the layer from WWF España, or substitute MITECO's ecological-connectivity layers (coarser).

### 3. MFE Zaragoza → completes 4.6
Direct download, one province: MITECO MFE50 by CCAA →
`https://www.miteco.gob.es/es/biodiversidad/servicios/banco-datos-naturaleza/informacion-disponible/mfe50_descargas_ccaa.html`
▸ Aragón ▸ **Zaragoza (province 50)** ▸ SHP zip → `01_DATA\landcover\mfe\`. (Huesca already in.) Claude re-runs `05_build_forest_46.py`.

### 4. SNCZI flood zones → 4.3 overlay
- **Quick look (WMS):** SNCZI geoportal `https://sig.miteco.gob.es/snczi/` (add as WMS).
- **Data to clip (SHP):** MITECO SNCZI downloads → `https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/agua/` ▸ Zonas Inundables lámina **T=100** and **T=500** (Peninsula, ETRS89) → `01_DATA\hydro\`.

---
## Fastest path (least clicks)
1. **Script 10** → DEM. 2. **IDEAragón WFS** once → Natura 2000 + admin (Aragón), save as GeoPackage. 3. **MFE Zaragoza** (1 file) + **SNCZI T=100/500** (2 files) from MITECO. 4. **Natural Earth** outline for 3.1. 5. **Corridor** → from the vault (script 11).
That clears everything except the WWF corridor, which stays a vault/WWF item.

## Note on doing it via browser
Claude can drive these downloads directly with the **Claude in Chrome** extension (MFE, SNCZI, Natura 2000, Natural Earth are all straight file downloads). It wasn't connected when this was written — connect it and Claude can fetch them for you.
