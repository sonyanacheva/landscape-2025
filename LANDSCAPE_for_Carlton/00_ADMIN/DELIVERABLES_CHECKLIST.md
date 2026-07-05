# DELIVERABLES CHECKLIST — LANDSCAPE / Co-inhabiting
_Single source of truth for scope. Every item = teacher requirement + Sonya's intent + method + status + owner._
_**All maps built FROM SCRATCH** with new data + PyQGIS scripts (no reuse of old CORINE maps). GIS = PyQGIS-scripts-only._
_Status: ☐ todo · ◐ in progress · ☑ done · ⏸ later/out-of-sprint. Owner: S=Sonya, C=Claude, K=Carlton(help)_

**Format targets:** 3 × A0 vertical panels · A4 memory text · A3 bound dossier (one page per document) · print 300 dpi (200 dpi ok for raster backgrounds). CRS **EPSG:25830**. Project name: TBD.

**Representation standard (architecture):** every sheet reads as architecture — line-weight hierarchy + poché, **scale bar + north on every map**, section & section-perspective drawings, quantified legends (ha, m, %, counts), clean fast-read hierarchy. GIS supplies correct data; panels supply architectural representation.

**AREA OF STUDY frame (confirmed):** two-rectangle polygon `AREAOFSTUDY`, bbox **716913, 4584331 → 782950, 4637785** (EPSG:25830) = 66.0 × 53.5 km. Territorial maps = square hugging this. Clip box for downloads (bbox + 2 km): **714913, 4582331 → 784950, 4639785**.

---
## PANEL A0-1 — CONTEXT & TERRITORY (§3–§4)

### §3 Work area in the Iberian corridor network
- ◐ **3.1** Spain map, all corridors, **highlight "Sierras Litorales del Mediterráneo"** (Cataluña+Aragón). Scale ~1:3,000,000. _Data: WWF corridor + IGN base._ **DATA DONE** → `03_PROCESSED/corridor_3.fgb` (1,492-link WWF network, **5 study-area links highlighted**) + `countries_iberia_31.fgb` + provinces. _(Note: corridor = the WWF/LCP connectivity network; if teacher wants the specifically-named "Sierras Litorales del Mediterráneo" polygon, confirm it's this or a separate WWF product.)_ [C map ✓ / K style]
- ◐ **3.2** Cataluña–Aragón zoom, main territorial units, locate work area. ~1:500,000. **DATA READY** — corridor + provinces (Huesca/Zaragoza/Lleida) + comunidades + AOS frame. [C ✓ / K compose]
- ◐ **3.3** Work area (Candasnos) + **Natura 2000** — legend with site **ID, name, hectares**; main cities; river. ~1:50,000. **DATA DONE** → `03_PROCESSED/natura2000_box.fgb` (18 sites by designation) + **auto-ha legend** `00_ADMIN/natura2000_legend.csv` (incl. Valcuerna 35,338 ha). Still needs towns + river overlay + AOS frame at compose. [C data+ha ✓ / K style]
- ◐ **3.4** Work-area **critical points** — obvious corridor discontinuities + Natura 2000 sites **requiring connection**. _Barriers = canals, roads, rail._ **DATA DONE** → `zonas_criticas_34.fgb` (WWF "Valle del Ebro oriental") + barriers/crossings (4.4) + corridor + Natura (3.3). Carlton composes the discontinuity callouts. [C ✓ / K compose]

### §4 Territorial analysis  (frame = AREA OF STUDY, square hugging the two rectangles — extent TBC)
- ◐ **4.1 Hydrography** — rivers, streams, drainage, ridges, Valcuerna. _Have: CHE Ebro layers + DEM streams. Restyle._ **DATA DONE** → `03_PROCESSED/hydro_{lines,water,springs}_41.fgb` (box-clipped; **Valcuerna spine 35.4 km extracted + highlighted**; lagoons/saladas, springs, canals). Ridges + DEM streams pending 5 m DEM. Carlton composes/styles/exports. [C process ✓ / K style]
- ◐ **4.2 Geomorphology** — landforms, gypsum badlands, saladas. _Have: IGME GEODE. Add DEM geomorphons._ **DATA DONE** → `03_PROCESSED/geomorph_42.fgb` (58 units → 10 landforms; **gypsum+mudstone badlands = 50% of box**; saladas highlighted). DEM geomorphons + hillshade context pending 5 m DEM. Carlton composes/styles/exports. [C process ✓ / K style]
- ◐ **4.3 Flow accumulation + erosion** — + flood zones (SNCZI). **DATA DONE (from 25 m DEM)** → `03_PROCESSED/streams_43.fgb` (6,469 km drainage, 3 tiers: Main barranco 527 · Secondary 613 · Minor 5,328 km) + rasters `flowacc_43.tif` + `erosion_spi_43.tif` (Stream Power Index). ⚠ eastern ~8 km (Catalonia) outside Aragón DEM = masked. **SNCZI flood overlay DONE** → `03_PROCESSED/flood_43.fgb` (T=100 6,213 ha + T=500 7,337 ha, along Alcanadre + barrancos). **4.3 complete.** Carlton composes. [C process ✓ / K style]
- ◐ **4.4 Human presence / barriers** — population, roads, rail, **canals**; **catalogue underpasses & bridges** (flag under-utilised / overkill; multiple bridges seen). _OSM + manual over orthophoto._ **DATA DONE** → `03_PROCESSED/barriers_44.fgb` (~1,241 km, classed) + `crossings_44.fgb` (**14/16 crossings = open cuts, no structure**) + `human_pressure_44.fgb` (250 m, 196 km²). Structure flags need ortho/field verification. Feeds 3.4. Carlton composes + manual catalogue pass. [C base ✓ / S+K catalogue verify]
- ◐ **4.5 Agricultural matrix** — intensive / extensive / woody crops, **legend summing ha**. _REPLACE CORINE → **SIGPAC** real crops._ **DATA DONE** → `03_PROCESSED/agri_matrix_45.fgb` (9 classes, 298,434 parcels, PR kept as own ecotone class). Carlton composes/styles/exports. [C process+ha ✓ / K style]
- ◐ **4.6 Forest / shrub / scrub / natural veg** — realistically proven, not generic. _REPLACE CORINE → **MFE + Copernicus Small Woody Features**._ **DATA DONE (WHOLE BOX — Huesca + Zaragoza)** → `03_PROCESSED/forest_46.fgb` (9 classes; natural-veg ≈99,500 ha; Forest 36,853 · Grassland–scrub mosaic 33,470 · Scrub 19,396 · Riparian 2,719 · Wetland/saladas 1,056). Carlton composes/styles/exports. [C process ✓ / K style]
- ◐ **4.x Cañadas / vías pecuarias** — map protected public drover's roads (Ley 3/1995; cañada ≤75 m / cordel ≤37.5 m / vereda ≤20 m). **Triple use:** corridor+hedgerow backbone (§6), trekking/MTB ecotourism network (§6/§7), implementable on public land = no expropriation (stakeholder argument). **DATA DONE** → `03_PROCESSED/canadas_4x.fgb` from national RGVP 2024, clipped to box: **1,279 km** in-box (Cañada 437 · Vereda 365 · Cordel 248 · Colada 166 · sin clasificar 63) · **4,939 ha** implementable public corridor. Carlton composes/styles/exports. [C classify+quantify ✓ / K style]

---
## PANEL A0-2 — DIAGNOSIS & STRATEGY (§5–§6)

### §5 Species-specific ecological diagnosis
- ◐ **5.1a Lynx + rabbit habitat** — differentiated colours. _Rebuild on SIGPAC/MFE base._ **DATA DONE** → `03_PROCESSED/habitat_51a.tif` (categorical raster on **combined SIGPAC+MFE base**; adds Riparian corridor + Wetland/salada; **~116,300 ha effective lynx habitat**, 36,795 ha optimal ecotone). Method + caveats: `PROGRESS/METHOD_habitat_resistance_5.md`. [C ✓ / K style]
- ◐ **5.1b Lynx-path storyboard** **DATA DONE** → `viewpoints_51b.fgb` (17 classified views) + `REF_storyboard_51b.md`. ORIG: — numbered path; each view **classified**: ecotone, ravine, large-river crossing, habitat discontinuity, barrier; **opportunities**: hedgerow, un-ploughed field corners (machine turn-circles), Small Woody Features. _LCP in QGIS → viewpoints → ChatGPT renders._ [C locate+classify / S+ChatGPT render]
- ☐ **5.1c Ecological sections** — typologies, elevation change, **tree/scrub cover heights**. _Needs finer DEM (2 m) + canopy height raster._ [C/S]
- ◐ **5.2 Resistance map** — lynx-specific friction + **rabbit availability as conditional permeability** (matrix cells with rabbits = lower resistance; explains "out-of-habitat but visited"). _Have resistance surface (CORINE) → re-run on new base; re-run LCP._ **DATA DONE** → `03_PROCESSED/resistance_52.tif` (combined base × slope + barrier walls) + `corridor_lcp_52.fgb` (**93 km LCP, Alcubierre ↔ Valcuerna**; matches 4/5 WWF links) + `corridor_swath_52.tif` (19,722 ha band). Values = first pass, review vs literature (see METHOD doc). [C ✓ / K style]

### §6 Masterplan — the intervention strategy
- ◐ **6a Masterplan** **STAGED** → `interventions_6a.fgb` (55 nodes) + `REF_masterplan_6a.md`. ORIG: — reactivate the dried **Barranco de Valcuerna** as **ecological spine**; show patches, connectors, interventions, **Hondo de la Hunilla** reconnection (currently cut off by intensive agri machinery → add wildlife infrastructure link). [C/S]
- ◐ **6b Feedback-loop diagram** **DRAFT** → `REF_interventions_methods_6_8.md`. ORIG: — erosion control (slopes+barranco) → seed dispersal by roaming fauna → ecotourism → regenerative agriculture (financially viable) → biodiversity. Arid-honest, not a lush garden. [C draft / S]
- ◐ **6c Forman scheme-sections** **DRAFT** → `REF_interventions_methods_6_8.md`. ORIG: Forman-inspired scheme-sections + short argument text** — per intervention type; stakeholder case (spending justification). [C draft / S]
- ⏳ **Decision:** which ecotourism assets to show here vs earlier — huts, fisherman lodges, ruins/historical sites, **Nowhere festival** (~30 km, regional identity), hiking + MTB routes. [S decide]

---
## PANEL A0-3 — INTERVENTIONS & TIME (§7–§8)

### §7 Detailed interventions
- ☐ **7 · five sites** — each: **1×1 km plan + section (existing + proposed)**, scale **1:5000**. Placed along corridor / strategy logic. _QGIS **Atlas** over your 1 km grid; needs 2 m DEM._ [C setup / S]
   - ☐ site 1 · ☐ site 2 · ☐ site 3 · ☐ site 4 · ☐ site 5 _(pick locations)_ [S pick / C]

### §8 Temporal evolution (hero = the barranco)
- ☐ **8a Phased plan** of the key area (barranco). _Overlay choice pending (existing + staged interventions, or existing + long-term vision; maybe human-intervention only, not feedback loop)._ ⏳ [S decide]
- ☐ **8b Phased section(s)** showing cohabitation over time — barranco, hills, fauna (birds, insects, mammals), tourists appearing across phases. Detailed. [C storyboard / S+ChatGPT]
   - ☐ **P1 (yr 0–?)** early human intervention restoring processes + **artificial rabbit warrens** (habitat + infiltration) + erosion works.
   - ☐ **P2** land improved → more replanting; wildlife present as **seed dispersers**; ground indents store dew/humidity → some autonomous planting.
   - ☐ **P3** post-**flood event** + light **community intervention** (families stabilising trees, clearing enlarged barranco to prevent short-circuit); shows built resilience.
   - ☐ **P4** long-term vision — fully activated, bold but sensible, true to the arid ecology.
- ☑ **8c Erosion mechanism** VERIFIED (`REF_interventions_methods_6_8.md`). ORIG: — name it right: surface runoff / sheet–rill–gully; water-harvesting + deep roots for infiltration.
- ☑ **8d Flood-establishment method** VERIFIED (`REF_interventions_methods_6_8.md`). ORIG: — CORRECTED: rock-detention structures (check dams / one-rock dams / gully plugs) + seed pelleting/seed balls + flood-timed sowing (not the cork-tap method). [C verify sources]
- ◐ **8e Planting calendar** — xeroriparian species × month; autumn–winter window. **DRAFT DONE** → `00_ADMIN/REF_planting_palette_8e.md` + `species_palette_8e.csv` (31 verified native species across 5 gradient bands: riparian core, xeric shrub matrix, gypsum specialists, saladas fringe, steppe ground; species×month calendar; nurse-plant + water-harvesting techniques; caveats). Sonya/teacher to confirm + optional field check. [C draft ✓ / S confirm]

---
## FINAL / CROSS-CUTTING
- ☐ **Project name** — shortlist exists (La Espina Seca / El Pulso del Barranco / Contrato Valcuerna…). [S pick]
- ◐ **A4 memory text** DRAFT → `00_ADMIN/A4_memory_text.md`. ORIG: — narrative, goals, vision, stakeholder case. [C draft / S edit]
- ☐ **A3 dossier** — one page per document, bound. [S assemble / C stage]
- ☐ **Panel assembly (Figma)** — incremental as maps finish; 300 dpi export. [S / C stage assets]
- ⏸ **§1 Lynx+rabbit analysis** — not Sonya's, incomplete → separate later. [out of sprint]
- ⏸ **§2 Existing green corridor** — liked; later extract images + reformat for A0 band. [S later / C format]

---
## OPEN DECISIONS (need Sonya)
1. ~~Confirm the AREA OF STUDY square extent~~ ✅ RESOLVED — `AREAOFSTUDY` 66×53.5 km, clip box 714913,4582331→784950,4639785.
2. §6c — which ecotourism assets appear on masterplan vs elsewhere.
3. §8a — plan overlay approach.
4. §7 — the five intervention locations.
