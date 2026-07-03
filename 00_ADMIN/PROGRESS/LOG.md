# PROGRESS LOG — LANDSCAPE / Co-inhabiting
_Living record. Newest entries at top. A fresh chat + this log ≈ full context._

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
