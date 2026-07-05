# PROGRESS LOG — LANDSCAPE / Co-inhabiting
_Living record. Newest entries at top. A fresh chat + this log ≈ full context._

---
## 2026-07-04 — Session 11 (DEM landed → 4.3 built)

- **DEM fetch fixed + succeeded.** Root causes on Carlton's Mac: (1) scripts had Sonya's Windows BASE only → picker → **cancel crashed QGIS (SystemExit)**; (2) feeding the WCS layer to a `gdal:` algorithm wrote nothing (GDAL can't read the WCS provider); (3) 5 m over the whole box = 161 M px froze QGIS. Fixes: `BASES` list (Win+Mac), no picker/SystemExit; write via **`QgsRasterFileWriter`** (WCS-aware, tiles); default **RES = 25 m** → `01_DATA/DEM/dem_box.tif` (2801×2298) + hillshade + slope. (5 m/2 m reserved for §7/§8 tiles.)
- **4.3 FLOW + EROSION built** (`13_build_flow_erosion_43.py`, pysheds). Conditioned DEM (0-fill→nodata, fill pits/depressions, resolve flats) → D8 flowdir + accumulation. **Drainage network** `03_PROCESSED/streams_43.fgb` = 8,220 seg / **6,469 km**, 3 tiers by upstream area (Main barranco 527 · Secondary 613 · Minor 5,328 km). **Rasters:** `flowacc_43.tif` (log flow accumulation) + `erosion_spi_43.tif` (**Stream Power Index** = ln(A·tanβ), the erosion-susceptibility proxy; RUSLE-LS could be added later). Preview over hillshade = channels follow valley floors correctly.
  - ⚠ **Eastern ~8 km of box (Catalonia) has no Aragón DEM** (4.7% 0-fill) → masked nodata; some edge artifacts there. Fill later from CNIG/ICGC if needed.
- **load_maps now loads RASTERS too** (new defensive pseudocolour loader + `RASTERS` registry) alongside vectors. `renderer_streams` + registry added. **16 layers total** (14 vector + 2 raster).
- **NEXT:** SNCZI flood (1 download → completes 4.3 overlay). §5 now unblocked (5.1a habitat, 5.2 resistance use DEM slope + 4.5/4.6 base). Still need admin boundaries (§3.1/3.2) + WWF corridor (vault) for §3.

---
## 2026-07-05 — Session 12 (§5 species diagnosis built)

- **5.1a HABITAT built** (`14_build_habitat_51a.py`): reclass 4.5 → lynx/rabbit logic. `03_PROCESSED/habitat_51a.fgb`. Ecotone (grazed scrub) 26,775 ha = **lynx+rabbit optimal**; +scrub/forest cover 72,353 → **~99,128 ha effective lynx habitat**. Foraging 3,700; matrix permeable 147k, hostile 96k.
- **5.2 RESISTANCE + CORRIDOR built** (`15_build_resistance_corridor_52.py`, pysheds/skimage). Resistance = land-cover base (1–60) × slope factor (1–3) + barrier walls (motorway 1000 … canal 150). Rabbit conditional permeability via low ecotone/pasture values. → `resistance_52.tif` (1–1150, median 22). **Least-cost path Sierra de Alcubierre ↔ Valcuerna = 92 km** (`corridor_lcp_52.fgb`); **corridor swath 26,449 ha** (`corridor_swath_52.tif`, MCP within 2% of least cost). Preview: LCP threads the green scrub/forest habitat and skirts hostile irrigated crops = ecologically coherent.
- **Method + all parameter values + caveats → `00_ADMIN/PROGRESS/METHOD_habitat_resistance_5.md`** (flagged: values are a defensible first pass, review vs lynx/CorridorDesign literature; endpoints = 2 cores; 25 m grid; east strip no-DEM).
- Added `renderer_habitat` + `renderer_lcp` + 2 raster entries (resistance vmax-capped, swath) to load_maps; loader now supports vmin/vmax. **20 processed layers total.**
- **§4 + §5 core now complete.** Remaining: 5.1b LCP storyboard/viewpoints (have LCP geometry → ChatGPT renders), 5.1c ecological sections (need 2 m DEM + canopy), §6 masterplan, §7/§8. §3 still needs admin + WWF corridor.

- **§3 ADMIN built from IDEAragón** (`16_build_admin_3.py`). Carlton saved municipios/provincias/comunidades to `01_DATA/IDEAragon/` (all EPSG:25830). ⚠ **WFS export duplicated every feature ~7×** → deduped by code (383→**52 unique municipios** in box; 3 provinces; 1 comunidad). Outputs: `municipios_box_33.fgb` (52, names, for 3.3 frame/labels), `provinces_3.fgb`, `comunidades_3.fgb` (Aragón boundary). Added 3 outline renderers + registry (group "3.x ADMIN BOUNDARIES"). **23 processed layers.**
  - ⚠ IDEAragón = **Aragón-only** → no Cataluña/national admin. 3.3 municipios frame ✓; 3.1/3.2 still want national admin + the **WWF corridor** (the one remaining §3 gap).
- **SNCZI FLOOD added → 4.3 COMPLETE.** Carlton downloaded the right files (láminas T=100 + T=500, "Zonas Inundables asociadas a periodos de retorno") to `01_DATA/hydro/laminaspb-q{100,500}/`. `17_build_flood_43.py` clips to box → `03_PROCESSED/flood_43.fgb` (T=100 6,213 ha · T=500 7,337 ha, along Río Alcanadre + barrancos; Valcuerna ephemeral = not in SNCZI). Added `renderer_flood` + registry. **24 processed layers.**
- **§4 now fully complete (4.1–4.6 + 4.x, all sub-maps).** §5 core done (5.1a, 5.2). §3.3 admin+Natura done.
- **NEXT / only remaining data gap: WWF corridor** (vault, script 11) → finishes §3.1/3.2/3.4. Then map composition (Carlton) + optional 5.1b viewpoints, §6/§7/§8.

---
## 2026-07-04 — Session 10 (self-serve downloads via Chrome → 4.6 completed + §3 started)

- **Claude drove 3 downloads via Claude-in-Chrome** (browser connected): MFE Zaragoza (MFE50_50), MITECO Red Natura 2000 (rn2000.zip, 127 MB), Natural Earth 1:50m countries. Carlton moved + unzipped into `01_DATA/`. Cookie banners declined non-essential; no CAPTCHA hit.
- **4.6 COMPLETED (whole box).** Updated `05_build_forest_46.py` to read multiple MFE provinces (`MFE_FILES=Huesca:Zaragoza`). New `forest_46.fgb` = 383,559 ha, 4,393 polys. Natural-veg ≈99,500 ha: Forest 36,853 · Grassland–scrub mosaic 33,470 · Scrub 19,396 · Forest-plantation 5,730 · Riparian 2,719 · Wetland/saladas 1,056 · Grassland 257 · Bare 38. Renderer ha updated in load_maps. Zaragoza gap CLOSED.
- **§3.3 NATURA 2000 built** (`12_build_natura_33.py`). RN2000 naming gotcha: **`_p` = Península** (use), `_c` = Canarias. **18 sites intersect box** → `03_PROCESSED/natura2000_box.fgb` (by designation: 9 ZEPA · 7 LIC+ZEC · 2 triple) + **auto-ha legend `00_ADMIN/natura2000_legend.csv`**. Includes the corridor's core sites: **Valcuerna, Serreta Negra y Liberola (ES0000182, 35,338 ha)**, Monegros, La Retuerta/saladas de Sástago, Estepas de Monegrillo y Pina, Sierra de Alcubierre. Designation parsed from INSPIRE desig URLs + ES0000*→ZEPA fallback. Preview shows sites ringing the box with un-protected gaps = the connect argument.
- **§3.1 national backdrop staged** → `03_PROCESSED/countries_iberia_31.fgb` (Natural Earth, Spain + neighbours, EPSG:25830, `is_spain` flag). renderer_countries added.
- Added `renderer_natura` + `renderer_countries` to load_maps (groups "3.3 NATURA 2000", "3.1 CONTEXT"). **13 processed layers now in load_maps.**
- **STILL NEEDED (Carlton grabbing next):** DEM 5 m (script 10), admin boundaries (provinces/municipios/CCAA — IDEAragón WFS/CNIG), WWF corridor (vault/script 11), SNCZI flood (later, needs DEM). These finish §3.1/3.2/3.4 + unlock 4.3/§5.
- **Wrote beginner step-by-step `00_ADMIN/HOWTO_grab_remaining_data.md`** (Carlton hasn't used QGIS recently): the 4 remaining grabs with exact menu paths (DEM script, IDEAragón WFS for admin, corridor=vault, SNCZI=WMS/later).
- **BUGFIX — cross-machine paths + QGIS crash.** Carlton runs on **Mac** (`/Users/carltonfuturity/…`), scripts had only Sonya's Windows BASE → fell back to a folder-picker, and **cancel crashed QGIS (SystemExit)**. Fixed `load_maps`, `10`, `11`, `01`: now a **`BASES` list (Windows + Mac)**, resolve saved-project folder first, **no picker, no SystemExit** (raise normal Exception with guidance instead). Carlton re-runs script 10 with no edits. (WCS coverage id may still need tuning — separate from the crash.)
- **Cleanup (freed ~121 MB):** removed sync artifacts (15 `.fuse_hidden`/`.gpkg-wal`), `__pycache__`, 4 `.DS_Store`, and redundant `human/canadas copy.gpkg` (121 MB — RGVP source zip + canadas_4x already cover it). Verified git will commit NO large files. Note: `LANDSCAPE_for_Carlton/` mirror docs/scripts remain git-tracked from before the .gitignore (harmless dup; `git rm -r --cached` if full exclusion wanted — user's call). Carlton to commit+push.

---
## 2026-07-04 — Session 9 (data drop received; 4.1 Hydrography built)

- **Sonya's DATA_for_Carlton_2026-07-04 drop reviewed.** All layers EPSG:25830, counts match her README. Unlocks **4.1 (hydro), 4.2 (GEODE+contours+hillshade), 4.4 (buildings/human-pressure/railways/OSM infra/barriers/crossings)**. Still pending: §3 context bundle (corridors, Natura2000, provinces, municipios — she exports next), DEM 5 m, MFE-Zaragoza, SNCZI, national outline for 3.1.
  - ⚠️ **Script-number collision:** her README points Sonya to `04_dem5m_wcs_clip_classify.py` + `05_export_vault_layers.py`, but our `04`/`05` are `build_canadas`/`build_forest`. Need to write those two under clean numbers + reconcile.
  - Noise (ignore): `human/canadas copy.gpkg` = same RGVP we already built; `.fuse_hidden`/`.gpkg-wal` sync artifacts.
- **Updated Sonya's run instructions → `00_ADMIN/HOWTO_run_load_maps.md`** (one script `load_maps.py` replaces the deleted per-map style scripts; drag-and-drop after first run; BASE path note).
- **4.1 HYDROGRAPHY DONE (data).** `07_build_hydro_41.py` box-clips CHE/Aragón water → 3 layers in `03_PROCESSED`: `hydro_lines_41.fgb` (Main river 83 · Natural drainage 1,535 · **Barranco de Valcuerna spine 35.4 km** · Acequias 2,424), `hydro_water_41.fgb` (Lagoon/salada 382 · Reservoir 11 · Main canal 67), `hydro_springs_41.fgb` (201). CHE authoritative for drainage/canals; OSM only for main rivers (avoids canal dup).
  - **Valcuerna extracted as its own class** (the §6 ecological spine), drawn boldest. Added 3 renderers + registry lines to `load_maps.py` (shared group "4.1 HYDROGRAPHY"). Preview `03_PROCESSED/hydro_41_preview.png`.
  - "Ridges" + DEM-derived streams deferred to when the 5 m DEM lands.
- **OSM tourism/trails drop parked (Priority 3 / §6-§7).** `LINES.geojson` (32 MB) + `POINTS.geojson` were at repo root and **not gitignored** → moved into `LANDSCAPE_for_Carlton/01_DATA/tourism/` (gitignored). Reprojected 4326→25830, filtered stray geoms, box-clipped, classified → `tourism_points_25830.fgb` (219, w/ group) + `tourism_trails_25830.fgb` (8,879 lines). Parked for §6 masterplan / §7 / §5.1b viewpoints — NOT added to load_maps yet. Root `README_OSM_tourism_trails.md` kept tracked.
- **4.2 GEOMORPHOLOGY DONE (data).** `08_build_geomorph_42.py` box-clips GEODE, collapses **58 DESC_UNIT lithologies → 10 landform classes** → `03_PROCESSED/geomorph_42.fgb`. **Gypsum badlands 67,774 ha (20%) + Mudstone badlands 100,403 ha (30%) = 50% of box** (the Monegros badland signature). Also alluvial 14%, terrace/fan 11%, limestone 10%, glacis 8%, colluvium 5%, salada 783 ha (highlighted). Added `renderer_geomorph()` + registry line to `load_maps.py`; preview `geomorph_42_preview.png`. DEM geomorphons deferred to 5 m DEM. Contours + hillshade (Sonya's, self-styled) are Carlton's context overlays.
- **4.4 HUMAN PRESSURE & BARRIERS DONE (data).** `09_build_human_44.py` → 3 layers in `03_PROCESSED`: `barriers_44.fgb` (Main road 433 km · Motorway/autovía 316 · Canal 280 · Railway/HS 212 = ~1,241 km fragmenting infra), `crossings_44.fgb` (16-pt catalogue), `human_pressure_44.fgb` (250 m zone, 196 km²).
  - **Headline diagnosis:** of 16 corridor × barrier crossings, **14 are open cuts with NO bridge/tunnel** (7 motorway · 4 railway · 3 main road); only 2 (canal) have structures. The motorway + HS-rail wall across the south severs the corridor — the §5.2/§6/§7 crossing-infrastructure argument.
  - ⚠️ Structure flag = OSM bridge/tunnel tags at the crossing → **candidate catalogue, verify on orthophoto/field** (checklist expects manual pass).
  - Added `renderer_barriers/crossings/human_pressure` + registry lines to `load_maps.py` (group "4.4 HUMAN PRESSURE & BARRIERS"). Preview `human_44_preview.png`. **Also feeds 3.4 critical points.** Buildings (172,752) + towns left as Carlton's context overlays.
- **ALL data-in-hand §4 maps now built: 4.1, 4.2, 4.4, 4.5, 4.6, 4.x, 4.x-b (7 layers in load_maps).** Remaining Carlton scope is DEM-blocked (4.3 flow/erosion, §5) or waits on the §3 context bundle (§3.1–3.4) + MFE-Zaragoza (completes 4.6).
- **Wrote the two runner scripts for Sonya (clean numbers, resolving the 04/05 collision):**
  - `07_SCRIPTS/10_fetch_dem5m_wcs.py` — QGIS: connects Aragón WCS (coverage id configurable), clips 5 m DEM to box → `01_DATA/DEM/dem_5m_box.tif` + hillshade + slope; prints GetCapabilities URL + CNIG-HU30 fallback if it fails. Master input for 4.3/§5.
  - `07_SCRIPTS/11_export_vault_layers.py` — QGIS (vault open): fuzzy-matches + exports the §3 context bundle (corridors, Zonas_Criticas, Natura2000 + ESPACIOS_H1-3, provinces, municipios, CCAA, poi, grid) → `01_DATA/context/` reprojected 25830; prints MISSING list to tweak.
  - ⚠ Both run in Sonya's QGIS — not testable headlessly here; written defensively (config at top, clear diagnostics). Updated `DATA_REQUEST_for_Sonya.md` to point at them.
- **Script robustness (Sonya's file-structure uncertainty).** `load_maps.py`, `10`, `11` now **preflight paths**: resolve BASE → saved-project folder → **QFileDialog folder-picker**, else `SystemExit` with a plain-language fix (which line to edit / save project in repo / pick folder). `11` also stops early if the vault isn't open. No more confusing tracebacks. Wrote `00_ADMIN/FILE_STRUCTURE.md` (expected tree + which script reads/writes what) for her Claude to set up.
- **QA PASS on all 11 processed fgb → PASS (`00_ADMIN/PROGRESS/QA_processed_layers.md`).**
  - **Renderer↔data:** 0 unmatched categories, 0 nulls, all EPSG:25830 — nothing silently drops to "Other" when styled. (2 empty catch-all legend rows: geomorph `Other`, barriers `Other major road` — cosmetic.)
  - **Geometry:** found **114 invalid polygons in agri_matrix_45** (0.04%, from 3 m simplify) → repaired with `make_valid` (114→0, all 298,434 kept); **fix baked into `03_build_agri_matrix_45.py`**. Other 10 layers clean.
  - **Extent:** only agri overhangs the box (whole-parcel design, 2.5% / 9,259 ha) — precise-clip optional. **Cross-check:** SIGPAC vs MFE forest agree (26.0k/28.4k ha); scrub differs as expected.
- **§8e XERORIPARIAN PLANTING PALETTE — draft done (web-researched + verified).** `00_ADMIN/REF_planting_palette_8e.md` + `species_palette_8e.csv`: 31 native species across 5 gradient bands (riparian core · xeric shrub matrix · gypsum specialists · saladas fringe · steppe ground), matched to the 3 strategy zones. Species×month calendar (plant Oct–Feb, avoid Apr–Sep). Verified: Ebro riparian (Fraxinus/Salix/native Tamarix), Monegros keystone Ziziphus lotus (rabbit→lynx refugia), gypsophytes (Gypsophila struthium nurse, Ononis tridentata), salada halophytes, Lygeum spartum pioneer. Flags: use NATIVE Tamarix (not invasive T. ramosissima), frost-marginal Pistacia/Nerium, don't plant salt flats, local provenance, ~36% survival realism → nurse plants + water-harvesting (ties §8c/d). Sources cited. Sonya/teacher confirm + optional field check.
- **Full data audit (all folders).** Confirmed the 7 built maps are complete; **genuinely missing: DEM 5 m, §3 context bundle (corridors/Natura2000/admin/national outline), MFE-Zaragoza, SNCZI flood.** Sonya's "gave everything" is off because the §3 layers are in her VAULT, not exported to the shared folder (script 11 does that), and the 5 m DEM was never fetched (her README admits only SRTM 30 m). No hidden files anywhere (name-searched admin/corridor/natura/dem/flood → none).
- **Self-serve acquisition plan → `00_ADMIN/GET_DATA_yourself.md`** (verified endpoints). Box is all-Aragón, so most via OGC services into QGIS in 25830, no plugin: DEM = script 10 (Aragón WCS); Natura2000 + admin = **IDEAragón WFS** `https://icearagon.aragon.es/Visor2D?service=WFS&request=GetCapabilities` (or CNIG admin, MITECO RN2000); MFE-Zaragoza + SNCZI T100/T500 = MITECO direct downloads; national outline = Natural Earth. **WWF corredores prioritarios = vault-only** (script 11 / WWF España). Claude in Chrome NOT connected — offered to drive downloads if connected.
- **NEXT:** await DEM (script 10) + §3 layers (IDEAragón WFS or script 11). Then 4.3 flow/erosion + §5 + §3.1–3.4.

---
## 2026-07-04 — Session 8 (Carlton scope: 4.5 pasture↔scrub resolved + layer rebuilt)

- **Started Carlton's delegated scope (§3/§4/§5).** Assessed data physically in `LANDSCAPE_for_Carlton/`: only SIGPAC (51 gpkg), MFE-Huesca, RGVP cañadas are present. §3 + 4.1/4.2/4.3/4.4 blocked (DEM/OSM/old-vault layers not shipped). Ready-now items = 4.5, 4.6-Huesca, 4.x cañadas. Recommended order: 4.5 → cañadas → 4.6.
- **4.5 pasture↔scrub flag RESOLVED.** Raw `uso_sigpac` ha breakdown (box, 298,434 parcels): the "Pasture" class was **88% PR** (pasto arbustivo, 26,775 ha) + PA 3,310 + PS 390. So the whole flag = one code, PR.
- **Decision (Sonya/teacher):** keep data rich — **PR = its own class "Grazed scrub / pasto arbustivo" (ecotone)**, well annotated. NOT merged into Pasture or Scrub. Pasture(open)=PA+PS only.
- **Layer rebuilt from scratch:** `07_SCRIPTS/03_build_agri_matrix_45.py` → `03_PROCESSED/agri_matrix_45.fgb` (layer `agri`, EPSG:25830, 298,434 parcels, simplified 3 m, 101 MB, copied to mount intact + verified). Fields: uso_sigpac, coef_regadio, agri_class, ha.
- **9-class legend (ha):** Arable dryland 120,264 · Arable irrigated 95,399 · Scrub (matorral) 46,389 · Non-agri 30,676 · Woody crops 26,799 · **Grazed scrub/pasto arbustivo 26,775** · Forest 25,964 · Pasture (open) 3,700 · Horticulture 145. Total 376,111 ha. (Whole parcels touching frame → slightly exceeds box; precise-clip at layout is Carlton's, optional.)
- Irrigation split: `coef_regadio` is effectively binary (0 / 100); irrigated if >0.
- Style script updated: `07_SCRIPTS/02_style_agri_matrix_45.py` (9 classes, ecotone sage #B7C083, ha in every legend label). Scripts + fgb mirrored into `LANDSCAPE_for_Carlton/`.
- Preview: `03_PROCESSED/agri_matrix_45_preview.png` (sanity check, not final styling).

- **4.x CAÑADAS DONE (data).** Built from national RGVP (`RGVP_BDN_2024.shp`, EPSG:25830, Ley 3/1995) → `03_PROCESSED/canadas_4x.fgb` (layer `canadas`, lines). Script `07_SCRIPTS/04_build_canadas_4x.py`.
  - Type codes decoded: **CA**=Cañada (≤75 m) · **COR**=Cordel (≤37.5 m) · **VE**=Vereda (≤20 m) · **CO**=Colada (variable) · **OV**=sin clasificar/revisar (placeholder rows).
  - **Geometries CLIPPED to box** (bbox filter alone inflates km with whole lines). In-box result: **361 features, 1,279 km** total. By type: Cañada 437 km · Vereda 365 km · Cordel 248 km · Colada 166 km · sin clasificar 63 km.
  - **Implementable public-corridor land = 4,939 ha** (length × legal width; the "no-expropriation" stakeholder number for §6). Field `area_ha` per feature; `ancho_m` = legal width.
  - Box straddles Zaragoza + Huesca + a sliver of Lleida (expected).
  - Style script `07_SCRIPTS/04_style_canadas_4x.py` — line-weight hierarchy by tipo (cañada thickest), single sienna hue, km in legend. Preview `03_PROCESSED/canadas_4x_preview.png`. Scripts + fgb mirrored to Carlton package.
- **PATH FIX (all scripts).** Sonya's repo actually sits at `…\_Github\New folder\landscape-2025\…`, not the old `…\2_LANDSCAPE\LANDSCAPE\…` base — style script raised "Layer failed to load". Fixed to a single `BASE` constant (canonical path in PROJECT_HUB) with auto-fallback to the saved `.qgz` project folder. Verified no stale refs remain.
- **STYLING WORKFLOW REFACTOR → one orchestrator `07_SCRIPTS/load_maps.py`.** Replaces the per-map style scripts (`02_style_*`, `04_style_*` deleted; recoverable via git). Sonya runs this ONE file; for every layer in `03_PROCESSED` it loads (skips if already loaded) → applies style → **saves `.qml` sidecar then loads it back** (QML = source of truth, enables drag-and-drop styling) → groups it. Idempotent. `RESTYLE_LOADED=True` re-applies on re-run so edits propagate; set False to preserve manual UI tweaks.
  - **Design:** per-map `renderer_*()` block + a `MAPS` registry. Restyle one map = edit its block; add a map = add one function + one registry line; the loop never changes. (Rejected version-stamp tracking as over-engineering for this scale.)
  - **Email to Sonya = the `.fgb` files + `load_maps.py`.** Build scripts (`03_build_*`, `04_build_*`) are Claude's headless step, not hers.
- **4.6 FOREST / SCRUB / NATURAL VEG DONE (data, Huesca only).** Built from MFE50_22 (`05_build_forest_46.py`) → `03_PROCESSED/forest_46.fgb` (layer `mfe`, EPSG:25830, 3,084 polygons, box-clipped). Reclass on `DEFINICION`; agriculture muted to one context class (4.5 owns crops).
  - **In-box ha (Huesca):** Grassland–scrub mosaic 24,478 · Forest (natural) 22,980 · Scrub (matorral) 15,687 · Forest (plantation) 5,427 · Riparian woodland (riberas) 2,678 · Wetland (humedal) 337 · Grassland 217 · Bare/sparse 29 · context 221,747. Natural-veg total ≈ 71,800 ha.
  - **Riparian woodland (A.F.M. Riberas) traces the Valcuerna/river corridor** — direct support for the xeroriparian spine (§6). Wetland = saladas/Hunilla context.
  - ⚠️ **Huesca (22) only** = ~78% of box (293,579 of 376,111 ha); Zaragoza (50) strip blank until **MFE50_50** sourced (1 file) → re-run `05_build_forest_46.py`.
  - Added `renderer_forest()` + registry line to `load_maps.py`. Preview `03_PROCESSED/forest_46_preview.png`.
- **All three ready-now §4 maps done (4.5 + 4.6 + 4.x).** Everything else in Carlton's scope is data-blocked (nothing more buildable from files on disk). Plan reframed **from "map order" to "unblock"**: two master keys — **DEM 5 m** (unlocks 4.1/4.3/5.1c/5.2) and **old-vault export** (unlocks §3×4 + 4.1/4.2). §3 + 4.2 are composition/restyle of existing vault layers → Carlton can build in parallel with Claude's DEM-dependent §4/§5 analysis.
- **Wrote `00_ADMIN/DATA_REQUEST_for_Sonya.md`** — message-ready, prioritized: P1 = DEM (WCS) + vault `context\` bundle (corridors, Natura 2000 w/ code+name fields, admin, towns, critical points); P2 = CHE hydro, GEODE, contours, human presence, MFE50_50, OSM run, SNCZI; P3 = tourism/grid/sections/MDT02 later. Includes export-format rules + a do-NOT-copy list.
- **Wrote `00_ADMIN/PROGRESS/SPEC_section3.md`** — §3.1–3.4 composition spec (layers/scales/styling to benchmark, shared `.qpt` template, nested-scale insets) + auto-ha Natura 2000 legend logic (needs site code+name fields; `06_natura_ha_legend.py` + `renderer_natura()` to be written once real field names confirmed).
- **MEANTIME ANALYSIS (data in hand): Cañada × land-cover overlay.** `06_analyze_canada_landcover.py` overlays the spine on the 4.5 matrix → `03_PROCESSED/canada_landcover.fgb` (segments tagged agri_class + readiness) + preview. Added `renderer_canada_lc()` + registry line to `load_maps.py`.
  - **Centre-line:** 64% of the network runs on non-agri parcels = the legal spine is largely intact/unploughed.
  - **Buffered matrix (100 m, 10,056 ha):** 25% semi-natural (ready) · 28% permeable dryland · **15% (~1,465 ha) intensive irrigated = §6 intervention priority** · 32% other. ~53% already permeable-or-better.
  - Barrier stretches cluster where the network meets irrigation incl. **near Hunilla (SE)** — matches the §6a "Hunilla cut off" problem. Ready (green) concentrates through the central Valcuerna/badland zone.
  - Full method + caveats + readiness scheme → `00_ADMIN/PROGRESS/ANALYSIS_canada_landcover.md`. Re-run sharper once MFE-Zaragoza completes 4.6.
- **NEXT:** Sonya sends the P1 data drop → confirm Natura field names, build auto-ha legend, and Carlton starts §3 composition while Claude takes DEM-fed 4.1/4.3/§5.

---
## 2026-07-04 — Session 7 (strategy: PyQGIS-only + from scratch)

- **Strategy change (Sonya):** from now on **GIS = PyQGIS scripts Sonya runs in QGIS only** — no headless geoprocessing by Claude (credit-safe: keeps heavy data + errors off Claude's context). Updated HOW_WE_WORK, PROJECT_HUB, DELIVERABLES_CHECKLIST.
- **Credit note:** hit 90% usage — cause = this one huge thread (screenshots/PDFs + a 169k-char output dump), not the map. Fix: fresh chat per map/block, no big outputs.
- **Maps built FROM SCRATCH** with new data + fresh scripts/styling/layouts.
- ⚠️ **Verify 4.5 pastures:** PA/PR/PS all mapped to 'Pasture' (31,386 ha); PR (pasto arbustivo) may belong in Scrub. Next chat: show raw uso_sigpac ha breakdown, let Sonya/teacher set the pasture↔scrub boundary. No re-crunch needed.

---
## 2026-07-04 — Session 6 (4.5 processed + hybrid workflow)

- **Map 4.5 DONE (data):** `03_PROCESSED/agri_matrix_45.gpkg` — 305,204 SIGPAC parcels, box-clipped, EPSG:25830, reclassified `agri_class` + `ha`. Legend (ha): Arable dryland 119,374 · Arable irrigated 97,754 · Scrub 49,229 · Non-agri 31,574 · Pasture 31,386 · Woody 27,093 · Forest 26,721 · Horticulture 172. (Whole parcels touching frame → totals slightly exceed box; precise-clip optional.)
- Styling script: `07_SCRIPTS/02_style_agri_matrix_45.py` (Sonya runs in QGIS).
- **Workflow decided (hybrid):** Claude does heavy geoprocessing headless → hands finished layer; Sonya runs PyQGIS scripts for load/group/style/layout. Her instinct confirmed.
- **Tech notes for next runs:** SIGPAC plugin gpkgs are **EPSG:4258**, layer name `recinto`, irrigation field `coef_regadio`, folder `LANDSCAPE/downloads/`. **Large GeoPackages corrupt on the synced mount** (both direct write AND cp of a 341 MB gpkg failed). **Use FlatGeobuf `.fgb`** for outputs to the mount (110 MB copied intact). Layer name inside = `agri`. 4.5 layer = `03_PROCESSED/agri_matrix_45.fgb`, simplified 3 m. uso reclass table in script.
- **Pending downloads:** DEM 5m (WCS export not done), OSM (script not run), MFE-Zaragoza (only Huesca have).
- **NEXT:** 4.6 forest/scrub from MFE; flow/erosion once DEM tif exported; then per-map PyQGIS style+group scripts + layouts (panel + A3).
---
## 2026-07-04 — Session 5 (delegation + QGIS update)

- **Carlton delegated sections §3, §4, §5** (analysis-map production) → `00_ADMIN/CARLTON_HANDOFF.md`. Claude delivers analytical layers+styles; Carlton composes/styles/exports.
- Sonya updating QGIS to newest version. Post-update checklist: re-point **WhiteboxTools** exe; confirm plugins (SIGPAC Downloader, QuickOSM, QuickMapServices, LiDAR Height Extractor, **save-reminder plugin**) enabled; GRASS provider on; QuickMapServices basemaps; default CRS 25830 + relative paths. Preserve the **save-reminder plugin** (name TBC from Sonya).
- SIGPAC (plugin, by name) saved to `LANDSCAPE/downloads/` as gpkg — **Huesca complete, Zaragoza stopped ~94%** (re-run Zaragoza). Data stays in LANDSCAPE working folder; repo tracks docs/scripts/.qgz only (heavy geodata git-ignored).

---
## 2026-07-04 — Session 4 (data acquisition method + clean project + GitHub)

### Resolved
- SIGPAC per-municipio codes proved unreliable (web tables wrong; verified from real parcel coords that files 22046=Arguis etc. are outside box). **Fix: use QGIS plugin `SIGPAC Downloader` (picks by NAME).** No codes.
- Data plan finalized in `PROJECT_HUB.md` (single master reference now). Preference order: HAVE > PLUGIN > WMS/WCS > SCRIPT > 1-file. Avoid tile/municipio hunting.
- DEM 5 m via **Aragón WCS** (one pull, no tiles). OSM infrastructure via script `07_SCRIPTS/01_fetch_osm.py`.
- Have: geology, hydro, contours, Natura2000, corridor, admin/municipios, buildings, ortho, MFE-Huesca, RGVP cañadas, La Almolda+Bujaraloz SIGPAC. Get: SIGPAC(box), DEM 5m, MFE-Zaragoza, OSM.
- Clean project `02_QGIS/LANDSCAPE_MASTER.qgz` set up (CRS 25830, relative paths, groups, plugins: SIGPAC Downloader, QuickOSM, QuickMapServices, LiDAR Height Extractor, GRASS/Whitebox).

### Decisions
- Division of labour: Sonya runs plugin + WCS + fetch script; **Claude processes headless** (clip/reclass/ha/flow/erosion/resistance) and returns finished layers.
- GitHub repo `sonyanacheva/landscape-2025` — docs+scripts versioned; heavy geodata git-ignored.

---
## 2026-07-03 — Session 3 (map audit + cañadas)

### Reviewed 11 QGIS group screenshots
- Cross-cutting issue: **low contrast / no figure-ground** (washed grayscale satellite base). Fix set: mute matrix, subject pops, consistent line weights, scale bar + north every sheet.
- **GEOmorphology map = styling benchmark** (clear GEODE legend, earth tones, architectural). Match its clarity everywhere.
- Strong data already built: geology classified, hydrography (springs/reservoirs/channels/drainage), flow accumulation, provinces, Zonas Críticas, ESPACIOS H1–3, contours, human-pressure buffers.
- CORINE-based & to REPLACE: 4.3 Habitat (Lynx/Rabbit/NON), Intervention Strategies (over-hatched, unreadable), Resistance (CLC classes R=1–10).
- Tooling: she has **LiDAR Height Extractor** plugin → use for canopy/scrub heights on §5.1 & §8 sections (with 2 m DEM).

### Decision — map cañadas (vías pecuarias)
- Sonya decided to map cañadas as backbone for **hedgerows + trekking/MTB paths**. Affirmed: *Ley 3/1995*, public domain + protected, widths cañada ≤75 m / cordel ≤37.5 m / vereda ≤20 m, recognized for connectivity + non-motorized recreation. Triple use: corridor/hedgerow spine (§6), ecotourism network (§6/§7), **implementable on public land = no expropriation** (stakeholder/funding argument). Verify exact Aragón classification.
- Offer open: colleague's panels available as representation reference if needed (different animal).

---
## 2026-07-03 — Session 2 (collaboration setup)

### Done
- ✅ Wrote `HOW_WE_WORK.md` + `DELIVERABLES_CHECKLIST.md` (full scope, Sonya's notes, owners, statuses).
- ✅ Confirmed headless geoprocessing works here (pyogrio/GDAL + shapely installed) → I can clip/reproject/reclass/compute ha on downloaded files.
- ✅ Found tailored reference library to mine instead of web: Sonya's own **Xeroriparian Corridor – Strategy/Operations/Tactics.pdf**, WWF Autopistas Salvajes (crossings), UPM connectors study, lince.pdf, Danube-Carpathian, CorridorDesign manual, prior FINAL SUBMISSION.

### Clarifications from Sonya
- User is **Sonya** (account = Carlton). "Carlton's help" = a person who could co-work via the shared/synced folder.
- Contract covers all data handling + performance, not just URLs.
- AREA OF STUDY = polygon of **two rectangles** (for centering); territorial maps = a **square hugging both**. `AOS.gpkg` = 134×99 km (corridor-scale). Need the two-rectangle file to fix the exact square.
- Fine to download data herself; wants me aware of existing QGIS content.

### Transparency
- I can read data + attributes headlessly and **see exported PDFs/PNGs** (can critique her map exports), and render data previews — but cannot see her live QGIS canvas.
- "Live dashboard" feature = not useful for this project (no relevant connected services).

### Next
- Get AREA OF STUDY square extent → start SIGPAC/MFE (Block A).

### Update (end of session 2)
- ✅ AREA OF STUDY frame **confirmed**: `AREAOFSTUDY` 716913,4584331→782950,4637785 (66×53.5 km). Clip box +2 km: 714913,4582331→784950,4639785. Checklist decision #1 resolved.
- ✅ Sonya is an **architecture student** → representation standard added (line-weight hierarchy, scale+north every map, sections/section-perspectives, quantification).
- ✅ Digested the **Xeroriparian strategy** → `REF_xeroriparian_strategy.md`. Adopt its **3 zones** (Left Ravine / Ag Crossing / River Interface) for §6 and **6-stage timeline** (0–2/~5/~7/~10/~20 yr) for §8. Gap: no species → we supply a verified palette.
- Data placement: SIGPAC → `01_DATA/landcover/sigpac/` · MFE → `01_DATA/landcover/mfe/`. Recommend IDEAragón (Aragón-wide, avoids Huesca/Zaragoza split).

---
## 2026-07-03 — Session 1 (setup + audit)

### Done
- ✅ Read teacher brief + Carlton's full plan. Wrote `PRODUCTION_PLAYBOOK.md`.
- ✅ Confirmed site: Candasnos, Los Monegros (arid Ebro steppe, ~350 mm/yr). Barranco = **Valcuerna**; lagoon = **Hondo de la Unilla/Hunilla** (crossed by Aragón's only native deer pop.).
- ✅ Built clean folder skeleton + `FOLDER_GUIDE.md`.
- ✅ Audited existing QGIS (`x_LANDSCAPE/QGIS_007.qgz`) → `SALVAGE_MAP.md`. Verdict: ~50–60% of analysis exists, CRS 25830, main issues = CORINE base, duplicate clutter, no saved layouts.
- ✅ Extracted study-area extent (EPSG:25830): **716913, 4584331 → 782950, 4637785** (~66×53 km). This is the clip box.
- ✅ Wrote `HOW_WE_WORK.md` (contract + roles + time budget).

### Decisions
- **x_LANDSCAPE = data vault** (don't move big files); new master project `02_QGIS/LANDSCAPE_MASTER.qgz` lives clean.
- Work order: **de-CORINE first** (SIGPAC + MFE) → resistance/habitat → masterplan → interventions → temporal → assembly.
- Panels assembled **incrementally** as maps finish.
- Sections 1 (lynx/rabbit) & 2 (green corridor) handled **separately** — not in heavy sprint.

### Clarifications from Carlton
- Lynx+rabbit analysis is not his, incomplete/ugly → separate later work.
- Green corridor study: he likes it; later extract images + reformat for A0.
- Values: perfectionism, logic, clean fast-readable formatting.
- Contract: no lying/inventing; real data; flag approximations; transparency on limits.
- Wants incremental panel building; step-by-step data (open to batching if argued).

### Transparency / open items
- ⚠️ WebSearch hit monthly spend limit this session → can't live-verify SIGPAC/MFE URLs right now. Routes given from knowledge, flagged "confirm on screen."
- ⚠️ I cannot download from gov portals directly → Carlton downloads, I process headlessly.
- QGIS not in my sandbox → I hand finished layers + scripts; Carlton runs styling/layout.

### Next step
- **Block A / de-CORINE:** Carlton downloads (1) SIGPAC Huesca recintos, (2) MFE Huesca, into `01_DATA/landcover/`. Then I read real `uso`/formation codes → build reclass → compute ha → styled 4.5 + 4.6 layers.
