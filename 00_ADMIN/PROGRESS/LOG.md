# PROGRESS LOG — LANDSCAPE / Co-inhabiting
_Living record. Newest entries at top. A fresh chat + this log ≈ full context._

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
- **NEXT (still blocked on downloads/vault):** DEM 5 m (Aragón WCS) unlocks 4.1/4.3 + §5 terrain; OSM (QuickOSM) unlocks 4.4; MFE50_50 completes 4.6; old-vault export unlocks §3 + 4.1/4.2. Carlton composes/styles/exports 4.5 + 4.6 + 4.x via `load_maps.py`.

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
