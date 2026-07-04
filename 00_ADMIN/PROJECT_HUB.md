# PROJECT HUB — LANDSCAPE / Co-inhabiting
### Candasnos · Barranco de Valcuerna · Los Monegros · reference species: Iberian lynx (lens)
**This is the single reference file. I keep it rewritten so you never scroll the chat.** CRS everywhere: **EPSG:25830**. Study box: 714913,4582331 → 784950,4639785.

> **GIS = PyQGIS only.** All processing + mapping happens through PyQGIS scripts Sonya runs in QGIS (credit-safe: heavy data stays off Claude's context). **We build the new maps FROM SCRATCH** — new data + fresh scripts, styling and layouts; old CORINE maps are replaced, not reused.

---
## HOW WE GET DATA — order of preference
1. **[HAVE]** already in your files → I just clip/restyle.
2. **[PLUGIN]** a QGIS plugin does it → fastest, no manual tiles.
3. **[WMS/WCS]** pull from a server for the box in one go.
4. **[PyQGIS SCRIPT]** Claude writes it; Sonya runs it in QGIS (processing + styling; data stays local).
5. **[1-FILE]** one clean download.
_(Avoid: per-tile / per-municipio manual hunting. That's what wasted time.)_

## PLUGINS WE USE
- **SIGPAC Downloader** — crops by municipio **name** (no codes). → 4.5
- **QuickOSM** — roads/rail/canals/bridges/paths/tourism via one Overpass query for the box. → 4.4, 6, 7
- **QuickMapServices** — PNOA / satellite basemaps.
- **LiDAR Height Extractor** (you have) — tree/scrub heights on sections. → 5.1, 8
- **GRASS / WhiteboxTools** (Processing) — flow, erosion, least-cost paths. → 4.3, 5.2

---
## MASTER MAP LIST — data · logic · best option

### PANEL A0-1 · CONTEXT & TERRITORY
| Map | Logic (what it argues) | Data | Best option |
|---|---|---|---|
| **3.1** Spain + corridor (1:3M) | locate "Sierras Litorales del Mediterráneo" corridor nationally | WWF corridor, admin | **[HAVE]** corredores_prioritarios + provinces |
| **3.2** Cat–Aragón (1:500k) | zoom corridor to your region, place work area | corridor, admin units | **[HAVE]** restyle |
| **3.3** Work area + Natura 2000 (1:50k) | protected sites needing connection; ID/name/**ha** | Natura2000, towns, river | **[HAVE]** + **[SCRIPT]** auto-ha legend |
| **3.4** Critical points (1:50k) | where the corridor breaks — canals, roads, rail | barriers | **[HAVE]** + **[PLUGIN]** QuickOSM canals |
| **4.1** Hydrography | drainage skeleton incl. Valcuerna | CHE/Aragón water, DEM streams | **[HAVE]** + **[SCRIPT]** streams from DEM |
| **4.2** Geomorphology | gypsum badlands, saladas, landforms | GEODE geology, DEM | **[HAVE]** (your best map) |
| **4.3** Flow + erosion | runoff concentration + soil loss + flood zones | DEM; SNCZI flood | **[SCRIPT]** Whitebox/GRASS + **[1-FILE]** SNCZI |
| **4.4** Human pressure / barriers | population, infrastructure, **underpass/bridge catalogue** | OSM roads/rail/canals/bridges, buildings | **[PLUGIN]** QuickOSM + **[HAVE]** buildings |
| **4.5** Agricultural matrix (+ha) | intensive/extensive/woody crops, real not generic | **SIGPAC** | **[PLUGIN]** SIGPAC Downloader (by name) |
| **4.6** Forest / scrub / natural veg | real woody cover | MFE (+ optional SWF) | **[1-FILE]** MFE Huesca✓/Zaragoza + **[WMS]** SWF optional |
| **4.x** Cañadas | protected public spine for corridor+paths+hedgerows | RGVP | **[HAVE]** RGVP → **[SCRIPT]** clip |

### PANEL A0-2 · DIAGNOSIS & STRATEGY
| Map | Logic | Data | Best option |
|---|---|---|---|
| **5.1a** Lynx + rabbit habitat | suitability in 2 colours, ecotones | land cover (4.5/4.6), DEM | **[SCRIPT]** reclassify on new base |
| **5.1b** Lynx-path storyboard | classified journey (ecotone/ravine/barrier/opportunity) | LCP line + viewpoints | **[SCRIPT]** LCP → **ChatGPT** renders |
| **5.1c** Ecological sections | typologies, elevation, veg heights | DEM 2m + canopy | **[PLUGIN]** LiDAR Height Extractor |
| **5.2** Resistance + corridor | friction surface; rabbits lower resistance (visited-not-lived) | reclass 4.5/4.6 + slope + human | **[SCRIPT]** reclass → GRASS r.cost |
| **6** Masterplan | reactivate Valcuerna spine; 3 zones; Hunilla reconnection | all above + tourism POIs | **[HAVE]** + compose |
| **6** Forman scheme-sections | argue each intervention type | base geometry | **[SCRIPT]** base → Figma styling |

### PANEL A0-3 · INTERVENTIONS & TIME
| Map | Logic | Data | Best option |
|---|---|---|---|
| **7** ×5 sites (1:5000) | existing + proposed, plan + section each | DEM **2m**, ortho, all | **[PLUGIN]** Atlas over 1km grid + **[WCS]** MDT02 |
| **8** Phased barranco sections | cohabitation over 6 stages (0–2/~5/~7/~10/~20 yr) | DEM profile, canopy | **[SCRIPT]** base → **ChatGPT** phase renders |
| **8** Planting calendar | xeroriparian species × month | (we author) | **[SCRIPT]** table, Monegros palette |

---
## DEM — the one server win
**Aragón WCS (5 m, whole box in one pull, no tiles):** QGIS ▸ Layer ▸ Add ▸ **WCS** ▸ New:
`https://icearagon.aragon.es/arcgis/services/AragonReferencia/mde/MapServer/WCSServer?request=GetCapabilities&service=WCS&version=1.0.0`
→ pick 5 m DTM → set extent to box → save GeoTIFF to `01_DATA\DEM\`. (MDT02/2 m later, only for the 5 tiles.)

---
## DATA STATUS
| Have ✓ | Get now | Get later |
|---|---|---|
| geology GEODE, hydrography, contours, Natura2000, corridor, admin/municipios, human-pressure/buildings, orthophoto, MFE-Huesca, RGVP cañadas, La Almolda+Bujaraloz SIGPAC | **SIGPAC** (plugin, box municipios), **DEM 5m** (Aragón WCS), **MFE-Zaragoza** (1 file), **OSM** infrastructure (QuickOSM) | MDT02 2m (5 tiles), SWF (optional) |

## NEXT ACTIONS
1. **You:** set up clean project (steps in chat) + run **SIGPAC Downloader** for the box municipios + add **Aragón WCS DEM**.
2. **Me:** once SIGPAC + DEM land → build 4.5 (agri matrix + ha), 4.6, then flow/erosion (4.3) headlessly.
