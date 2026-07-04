# DOWNLOAD LIST — final, confirmed routes
_Clip box (EPSG:25830): 714913, 4582331 → 784950, 4639785 · study frame AREAOFSTUDY 66×53.5 km around Candasnos. Drop everything raw; I clip/reproject/reclassify._

---
## 1. SIGPAC — crops per parcel → map 4.5 (agri matrix + ha)
**Route:** FEGA ATOM → `2026/` → province folder → download the **`_shp.zip`** (or `_gpkg.zip`) per municipio.
Base: `https://www.fega.gob.es/atom/2026/rec_2026/22/` (Huesca) and `.../50/` (Zaragoza).

**CORE municipios first (INE codes verified via INE + IGN — file = `<code>_rec_2026_..._shp.zip`):**
| Municipio | file code | | Municipio | file code |
|---|---|---|---|---|
| Candasnos | **22072** | | Osso de Cinca | 22167 |
| Peñalba | 22172 | | Zaidín | 22254 |
| Valfarta | 22242 | | Fraga | 22112 |
| Castejón de Monegros | 22083 | | La Almolda | **50022** |
| Castelflorite | 22085 | | Bujaraloz | **50059** |
| Ballobar | 22046 | | Velilla de Ebro | **50278** |
| Chalamera | 22094 | | | |
| Ontiñena | 22165 | | | |

⚠ Candasnos = 22077 is INE-verified but confirm the file exists in the `/22/` folder; if it's missing, tell me. → save `01_DATA\landcover\sigpac\`
_(Full 66 km map needs the outer municipios too — see `MUNICIPIOS_IN_BOX.md`. Do core first.)_

## 2. DEM 5 m → sharpens 4.1–4.3 + feeds sections
**BEST — Aragón WCS (one pull for the whole box, no tiles):** in QGIS → Layer ▸ Add ▸ **WCS**, new connection:
`https://icearagon.aragon.es/arcgis/services/AragonReferencia/mde/MapServer/WCSServer?request=GetCapabilities&service=WCS&version=1.0.0`
→ connect → pick the **5 m DTM** coverage → set extent to the box → save as GeoTIFF into `01_DATA\DEM\`.
**ALT — CNIG MDT05:** you're currently on **HU29 (wrong zone)**. Filter to **HU30** (our area is UTM 30N) and pick the sheets over the box. → `01_DATA\DEM\`
_(MDT02 / 2 m later, only for the 5 intervention tiles.)_

## 3. MFE — forest/scrub/natural veg → map 4.6
MITECO biodiversity **Downloads** → Mapa Forestal → **Huesca** + **Zaragoza** (SHP). → `01_DATA\landcover\mfe\`

## 4. Cañadas / vías pecuarias → corridor + hedgerow + paths backbone
**One national shapefile (easy):** MITECO RGVP page → *Supply:* **"Shapefile of the General Network of Livestock Routes of Spain (RGVP) (34.5 MB)"** → download, I clip to the box. (Ley 3/95, updated 31/12/2024.) → `01_DATA\infrastructure_osm\vias_pecuarias\`

## 5. Copernicus Small Woody Features — OPTIONAL hedgerow overlay (4.6)
It's a **WMS** (display/GetMap raster), not needed for core analysis — MFE is primary. If wanted, add in QGIS as WMS:
`https://copernicus.discomap.eea.europa.eu/arcgis/services/GioLandPublic/HRL_SmallWoodyFeatures_2021/ImageServer/WMSServer?request=GetCapabilities&service=WMS`
Skip unless time allows. → `01_DATA\landcover\swf\`

---
**Priority to unblock maps:** #2 DEM (WCS, quick) + #1 SIGPAC core + #3 MFE. #4 cañadas is a 1-file grab. #5 optional.
**Already in hand:** geology GEODE, CHE hydrography, contours, Natura 2000, human-pressure, orthophoto.
