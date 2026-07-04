# LANDSCAPE | CO-INHABITING — Production Playbook
### Work area: Barranco de Valcuerna / Candasnos, Los Monegros, Aragón · Reference species: Iberian lynx (as lens)
_1.5-day battle plan · 3 A0 vertical panels + A3 dossier + A4 memory_

---

## 0. How to use this document
This is the single reference for the whole sprint. Every map has: **what it shows → data source → QGIS process/plugin/script → export → time budget.** Work top-to-bottom through the schedule in §8. Nothing here needs CORINE and nothing needs Illustrator until the very end.

**Working CRS for everything: `EPSG:25830` (ETRS89 / UTM 30N).** Set it in Project → Properties before you import anything.

---

## 1. The thesis (keep every map serving this)
Candasnos is arid Ebro steppe (~350 mm/yr, gypsum badlands, saline *saladas*). The lynx is the **client/lens**, but the land can't be a permanent lynx habitat — and saying that out loud is your strongest move. The real beneficiaries are the **steppe birds** (great/little bustard, Dupont's lark, Montagu's harrier), the **only native deer population in Aragón** (which crosses at the Hunilla lagoon), and the whole mosaic. Your intervention reactivates the **Barranco de Valcuerna as an ecological spine** that reduces erosion, restarts a seed-dispersal + infiltration feedback loop, and folds in ecotourism (Nowhere festival identity ~30 km west, huts, historical ruins, the Hunilla reserve). This is exactly the brief's "catalytic intervention / diversified economic model / cohabitation contract" (brief pp. 11, 16).

**Design register: arid-honest.** Not a lush garden — a specific, ever-improving dryland mosaic. Small-to-mid interventions that trigger a natural feedback loop.

---

## 2. Toolchain & pipeline
```
QGIS 3.34+  →  (style & compose as much as possible here)
   ├─ raster maps  → export PNG @ 300 dpi (final placed size)  ─┐
   ├─ vector maps  → export PDF (vector, layers kept)          ─┤→ Figma (assemble panels)
   └─ sections/base→ export SVG or DXF                          ─┘      ↑
Illustrator / AutoCAD → ONLY vector touch-ups (Illustrator crashes → keep files small, 1 map at a time)
Photoshop → only if a raster needs retouching
ChatGPT → perspective/collage rendering (lynx-path views, phased sections)
```
**Golden rules to avoid Illustrator pain:** do labeling, legends, hillshade blending, and color inside QGIS (it's fully capable). Export finished maps as flat 300-dpi PNGs for Figma placement, plus a vector PDF backup per map in case you need to edit lines. Only open Illustrator for a single problem map, never the whole panel.

### DPI reality for A0
A0 = 841 × 1189 mm. True 300 dpi across a full A0 ≈ 9933 × 14043 px — heavy and unnecessary; A0 is viewed at distance. **Target 200 dpi for full-bleed raster backgrounds, 300 dpi for individual map frames at their placed size.** Keep all line/type work vector (PDF/SVG) so it prints crisp regardless. This keeps Figma responsive and print sharp.

---

## 3. Panel allocation (adjustable)
| Panel | Theme | Sections | Core contents |
|---|---|---|---|
| **A0-1 CONTEXT & TERRITORY** | Where & what | §3 + §4 | Corridor scaling (Spain→Cat/Aragón→work area), Natura 2000 + critical points, hydrography, geomorphology, flow/erosion, human pressure & barriers, agricultural matrix (ha), forest/scrub |
| **A0-2 DIAGNOSIS & STRATEGY** | Why & the big move | §5 + §6 | Lynx+rabbit habitat, resistance map, lynx-path storyboard + sections, masterplan of the spine, Forman scheme-sections, Hunilla reconnection |
| **A0-3 INTERVENTIONS & TIME** | How & when | §7 + §8 | 5 intervention sites @1:5000 (existing + proposed sections), phased barranco sections (P1–P4), planting calendar, conclusion strip |
| **A4 memory** | The argument in text | narrative | Project name, thesis, goals, stakeholder case |
| **A3 dossier** | Everything, bound | all | One page per document from the panels |

Title strip + project name + intro narrative runs across the top of A0-1; conclusion/"cohabitation contract" line closes A0-3.

---

## 4. Master data download checklist
Pull everything **once**, clip to a generous work-area bounding box (~15×15 km around Candasnos), reproject to 25830, save into `/DATA/` subfolders. Do this first — it unblocks every map.

| # | Layer | Source (portal) | Format | Feeds maps |
|---|---|---|---|---|
| D1 | DEM 2 m & 5 m (PNOA LiDAR) | CNIG — centrodedescargas.cnig.es (MDT) | GeoTIFF | 3.x, 4.1–4.3, all sections |
| D2 | PNOA orthophoto (WMS or tiles) | CNIG / PNOA WMS | WMS | basemaps, 4.4 cataloguing |
| D3 | Natura 2000 (LIC/ZEC/ZEPA) | MITECO descargas | SHP | 3.3, 3.4 |
| D4 | Red Natural de Aragón + humedales (Hunilla) | IDEAragón | SHP/WFS | 3.3, 6 |
| D5 | Hydrography + barrancos | Confederación Hidrográfica del Ebro (CHE) | SHP | 4.1 |
| D6 | Flood zones (return periods) | SNCZI (MITECO) | SHP/WMS | 4.3, §8 phase 3 |
| D7 | Geology MAGNA 50 | IGME | SHP/WMS | 4.2 |
| D8 | SIGPAC parcels + crop use | SIGPAC / IDEAragón visor | SHP/WFS | 4.5 |
| D9 | Mapa Forestal de España (MFE) | MITECO BDN | SHP | 4.6 |
| D10 | Copernicus Small Woody Features + Tree Cover Density | land.copernicus.eu | GeoTIFF | 4.6, opportunities |
| D11 | Canopy height (ETH 10 m or Meta 1 m) | GEE / public tiles | GeoTIFF | 5.1 sections |
| D12 | OSM: roads, rail, canals, bridges, tunnels, tracks, tourism, huts | QuickOSM (in QGIS) | live | 4.4, 6, 7 |
| D13 | WWF Iberian connectivity corridor (reference) | your §3 source | image/geo | 3.1–3.2 |

> **Verdict on turbo.overpass:** use it **only through QuickOSM for D12** (infrastructure/barriers/paths/tourism). For land cover, crops, forest, hydro, Natura 2000, DEM — Spanish official DBs win on detail and citability.

---

## 5. Per-deliverable production table

### PANEL A0-1 — CONTEXT & TERRITORY
| Map | Shows | Data | QGIS process / plugin | Scale | Time |
|---|---|---|---|---|---|
| 3.1 Spain + corridor | Iberian corridors, "Sierras Litorales del Mediterráneo" highlighted | D13 + IGN provinces | Style WWF corridor over muted Spain; highlight corridor | 1:3,000,000 | 30 m |
| 3.2 Cat–Aragón zoom | Corridor + main territorial units, locate work area | D13 + admin | Same template, zoom; inset locator | 1:500,000 | 20 m |
| 3.3 Work area + Natura 2000 | Sites w/ ID, name, ha; cities; river | D3, D4 + admin | **Auto-legend-with-ha script (§6)**; label site IDs | 1:50,000 | 45 m |
| 3.4 Critical points | Corridor discontinuities, Natura sites needing connection | D3, D5, D12 canals | Mark barriers (canals/roads) breaking connectivity | 1:50,000 | 40 m |
| 4.1 Hydrography | Rivers, streams, drainage, ridges, Valcuerna | D1, D5 | GRASS `r.watershed` streams + CHE overlay | 1:50,000 | 40 m |
| 4.2 Geomorphology | Landforms, gypsum badlands, saladas | D1, D7 | Geomorphon (`r.geomorphon`) + IGME | 1:50,000 | 45 m |
| 4.3 Flow + erosion | Flow accumulation + RUSLE erosion + flood zones | D1, D6 | WhiteboxTools flow-accum; RUSLE raster (§6) | 1:50,000 | 60 m |
| 4.4 Human pressure/barriers | Population, roads, rail, **canals**, bridges/underpasses catalogue | D2, D12 | QuickOSM; **manual underpass/bridge catalogue over orthophoto** | 1:50,000 | 60 m |
| 4.5 Agricultural matrix | Intensive/extensive/woody crops, **ha per class** | D8 SIGPAC | Categorize by crop code; **area-by-class legend script (§6)** | 1:50,000 | 45 m |
| 4.6 Forest/shrub/scrub/natural veg | Real woody cover (not generic) | D9 MFE + D10 SWF/TCD | MFE polygons + Small Woody Features to *prove* hedgerows/isolated trees | 1:50,000 | 45 m |

### PANEL A0-2 — DIAGNOSIS & STRATEGY
| Map | Shows | Data | QGIS process | Time |
|---|---|---|---|---|
| 5.1 Lynx + rabbit habitat | Suitability, two colors; ecotones | D9, D10, D1 | Weighted suitability raster; classify | 60 m |
| 5.1 Lynx-path storyboard | Numbered path + classified views | LCP output | Least-cost path → viewpoints → ChatGPT renders | 90 m |
| 5.1 Ecological sections | Typologies, elevation, veg heights | D1, D11 | Terrain Profile + canopy sampled on line | 60 m |
| 5.2 Resistance map | Friction surface + rabbit conditional permeability | reclass of 4.5/4.6 | **Reclass→resistance + `r.cost` script (§6)** | 75 m |
| 6 Masterplan | Spine, patches, connectors, Hunilla link, interventions located | all above | Composite strategy plan | 120 m |
| 6 Forman scheme-sections | Argument diagrams of interventions | hand/vector | QGIS base → Figma/Illustrator styling | 60 m |

### PANEL A0-3 — INTERVENTIONS & TIME
| Map | Shows | Data | QGIS process | Time |
|---|---|---|---|---|
| 7 ×5 intervention sheets | 1×1 km existing + proposed, section each | D2, D1, all | **QGIS Atlas** (1 layout, 5-feature coverage → 5 sheets) @1:5000 | 150 m all 5 |
| 8 Phased barranco sections | P1–P4 over years; cohabitation | D1 profile | 1 base section → 4 phase variants; ChatGPT layers fauna/tourists | 120 m |
| 8 Phase plan | Existing + long-term overlay | masterplan | Simplified masterplan variant | 45 m |
| 8 Planting calendar | Species × month, xeroriparian | table | Designed table (see §7 species list) | 45 m |

---

## 6. Key ready-to-run scripts
Paste into **Plugins → Python Console → Show Editor**. I'll adapt each to your real layer names when you reach that step — tell me the layer name and field.

### 6a. Area-by-class → hectares into the legend (for 3.3, 4.5, 4.6)
```python
# Sums area per category and rewrites labels as "Class — 123.4 ha"
from qgis.core import QgsProject
layer = iface.activeLayer()
field = 'crop_class'          # <-- change to your category field
areas = {}
for f in layer.getFeatures():
    k = f[field]
    areas[k] = areas.get(k, 0) + f.geometry().area()/10000.0  # m2 -> ha
for k, v in sorted(areas.items(), key=lambda x:-x[1]):
    print(f"{k}: {v:,.1f} ha")
# (categorized renderer labels can then be set to include these values)
```

### 6b. Reclassify land cover → resistance, then least-cost corridor (5.2 + lynx path)
```python
# 1) Build a resistance raster by reclassifying land cover (lower = easier to move)
#    scrub/forest=1, ecotone=5, dry crop=20, irrigated crop=50, canal/road/urban=100
# 2) Lower resistance where rabbits are available (conditional permeability)
# Use Processing: 'grass7:r.reclass' then 'grass7:r.cost' (start = source patch)
import processing
processing.run("grass7:r.cost", {
    'input':'resistance_raster',
    'start_points':'source_patch_points',
    'output':'cost_surface',
    'GRASS_REGION_CELLSIZE_PARAMETER':10})
# Then r.drain from the target patch back down the cost surface = least-cost path
```

### 6c. RUSLE erosion (4.3) — compute A = R·K·LS·C·P
```python
# Build each factor raster (R climate, K soil erodibility from IGME/soil,
# LS from DEM slope-length via WhiteboxTools 'SedimentTransportIndex' or r.watershed length_slope,
# C from land cover, P=1). Multiply with raster calculator.
# I'll generate the full factor-by-factor recipe with Monegros R/K values on request.
```

### 6d. Merge layers preserving all attributes (not a flattening dissolve)
Use **Vector → Data Management → Merge Vector Layers** (same geometry type) or **Processing → Union** (to combine attributes of overlapping polygons). Never "Dissolve" if you need the attribute detail — Dissolve collapses it.

---

## 7. Xeroriparian planting palette + calendar (for §8)
Arid Monegros / Valcuerna-appropriate, drought- and salt-tolerant, structured by role. **Plant bare-root/seed in the autumn–winter window** (Oct–Mar) to exploit winter moisture; sow enhancement-coated seed *before* rain events.

- **Barranco bed / xeroriparian:** *Tamarix canariensis/gallica*, *Salix* spp., *Populus alba* (only where water persists), *Nerium oleander*.
- **Slopes / erosion control (deep roots, infiltration):** *Retama sphaerocarpa*, *Atriplex halimus*, *Lygeum spartum* (albardín), *Stipa tenacissima* (esparto), *Thymus*, *Rosmarinus*.
- **Scrub / cover for prey (lynx/rabbit):** *Pistacia lentiscus*, *Quercus coccifera*, *Rhamnus lycioides*, *Juniperus oxycedrus/phoenicea*, *Ephedra*.
- **Field-edge / hedgerow (agri matrix):** *Crataegus*, almond (existing), aromatic strips for pollinators.

**Erosion mechanism, named correctly:** water that sheets off crusted/sealed soil is **surface runoff / overland flow**, stripping topsoil as **sheet → rill → gully erosion**. Counter it with **water-harvesting earthworks** ("slow it, spread it, sink it"): check dams / one-rock dams / gully plugs in the barranco, plus deep-rooted plants that build soil structure and open infiltration paths.

**Flood-triggered establishment (corrected):** the "cork-tap seedbag" isn't in the literature — the proven arid equivalents are **rock-detention structures** (trap flood sediment + seed), **seed enhancement** (pelleting/coating, seed balls sown before rain), and **flood-timed germination**. Use these; they're citable and stronger.

---

## 8. The 1.5-day schedule (≈12 working hours)
**DAY 1 (8 h)**
- **H0–1 Setup:** project CRS 25830, folder structure, install plugins (QuickOSM, WhiteboxTools, Terrain Profile, QuickMapServices), pull D1–D12 clipped to bbox.
- **H1–3 Territorial base (4.1, 4.2, 4.3):** run flow/erosion/geomorph scripts once, style with shared `.qpt` template.
- **H3–5 Land-cover maps (4.5, 4.6, 4.4):** SIGPAC + MFE + SWF; auto-ha legends; barrier/underpass catalogue.
- **H5–6 Context maps (3.1–3.4):** corridor scaling + Natura 2000.
- **H6–8 Diagnosis (5.1 habitat, 5.2 resistance):** suitability + resistance + least-cost path. Fire ChatGPT renders for the lynx-path views to process overnight.

**DAY 2 (4 h — half day)**
- **H8–10 Masterplan (§6) + Forman sections + Hunilla link.**
- **H10–11.5 Interventions (§7): Atlas 5 sheets @1:5000 + sections.**
- **H11.5–12.5 Temporal (§8): phased barranco sections + planting calendar.**
- **H12.5–13.5 Assembly:** export all maps (300 dpi PNG + vector PDF), compose 3 panels in Figma, build A3 dossier, write A4 memory. Final CRS/scale/legend verification pass.

---

## 9. Triage — if time runs short, cut in this order
1. Keep: masterplan (§6), one hero intervention (§7), phased barranco sections (§8), resistance map (5.2) — these carry the argument.
2. Trim: reduce §7 from 5 to 3 fully-detailed sites + 2 diagrammatic.
3. Simplify: geomorphology (4.2) can be orthophoto + annotation instead of full geomorphon.
4. Never cut: the narrative thread and the ha-quantified legends — the brief grades on quantification + argument.

---

## 10. A4 memory + project name (finalize last)
**Name shortlist:** *La Espina Seca* (The Dry Spine) · *El Pulso del Barranco* (flood-pulse feedback loop) · *Contrato Valcuerna* (site-named cohabitation contract) · *Monegros Vivo* · *Reactivar el Barranco*. — Recommend **La Espina Seca** or **El Pulso del Barranco**.

**Memory structure (1 × A4):** (1) the question — cohabitation in an arid, damaged land; (2) the client — lynx as lens, deer/steppe birds/mosaic as beneficiaries; (3) the diagnosis — fragmented spine, erosion, canal barriers; (4) the move — reactivate the Valcuerna spine + Hunilla reconnection, feedback loop of infiltration/seed-dispersal/ecotourism; (5) the phasing — small interventions → natural self-reinforcement; (6) the contract — a good-practice model of wildlife + agriculture + ecotourism cohabitation.

---
_Sources for site facts: Monegros/Candasnos (birdinginspain, Wikipedia), Hondo de la Unilla + Barranco de Valcuerna (Huesca la Magia), dryland rock-detention restoration (Frontiers 2021), Nowhere festival Monegros (Wikipedia)._
