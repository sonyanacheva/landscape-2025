# Salvage map — audit of existing QGIS work (QGIS_007.qgz)

**Headline:** You're ~50–60% through the analysis. Working CRS is already **EPSG:25830** (good). A real analytical skeleton exists — the problem isn't that it's missing, it's (1) built on **CORINE** (too generic), (2) cluttered with `copy copy copy` duplicates and `OLD LAYERS` groups, and (3) **no saved print layouts / .qpt templates**, so nothing is reproducibly composed yet. That matches your feeling: the maps miss info and aren't readable. We fix, not restart.

## What exists → verdict
| Asset cluster (in your project) | Status | Verdict | Deliverable | Action |
|---|---|---|---|---|
| DEM chain: projected, fill-sinks, slope°, hillshade, flow-accum, slope/flow classes, **erosion index + MAP1 suitability** | Built | **KEEP** | 4.1, 4.3 | Restyle only. But source DEM is coarse (SRTM 30 m / MDT200) |
| Hydrography: CHE ES091 (Ebro) rivers, channels, drainage, lagoons, reservoirs, GEODE geology | Built | **KEEP** | 4.1, 4.2 | Restyle, dedupe. This is your Spanish-source win — better than OSM water |
| Natura 2000 Aragón (LIC/ZEPA), ESPACIOS_H1–H3 | Built | **KEEP** | 3.3, 3.4 | Add ha to legend (script 6a) |
| Resistance surface: RESIST_roads/water/buildings/humanpressure + **CORINE land-use** | Built | **UPGRADE** | 5.2 | Re-run with SIGPAC+MFE instead of CORINE |
| Habitat: Lynx / Rabbit / Non-habitat, Hunting_Suitability, Habitat Suitability Final | Built | **UPGRADE** | 5.1 | Same — de-CORINE the base |
| Corridors: LCP output (Link_ID, LCP_Length…), proposed 1 km, My_Corridors, Zonas_Criticas | Built | **KEEP/UPGRADE** | 3.4, 5.2, 6 | LCP already run (CorridorDesign). Re-run after resistance upgrade |
| Land cover / agri / opportunities: COORINE_Full, corine_subset_opportunities | **CORINE** | **REPLACE** | 4.5, 4.6 | Swap → SIGPAC (crops+ha) + MFE (forest/scrub) + Copernicus SWF |
| Human presence: buildings, activity zones, 250 m buffers, railway crossings barriers | Built | **KEEP** | 4.4 | Add manual bridge/underpass catalogue |
| Sections: SECTION A, SECTIONS 1KM, MY_SECTIONS, ARGE, E2500 | Lines exist | **KEEP** | 5.1, 7, 8 | Need finer DEM (2 m) + canopy height for quality |
| Tourism: POI's.gpkg, BTN_POI (culture, nature) | Gathered | **KEEP** | 6 | Feeds ecotourism masterplan |
| Intervention strategies.gpkg, 1 km grid | Started | **KEEP** | 6, 7 | Grid → Atlas coverage for the 5 sheets |
| Basemaps: PNOA ortho (Ortoimagen HQ), Google Satellite | Built | **KEEP** | all | — |
| Lynx+Rabbit analysis (2025-10-08 folder, HTML/PDF) | Done | **KEEP (ref)** | §1 | Section 1 complete — reference only |
| Corridor study Ex.2/001 + Danube-Carpathian refs | Done | **KEEP (ref)** | §2 | Section 2 material |
| Multi-GB gpkgs (PROJECT_LAYERS 25 GB, OUTPUT 18 GB, CLIPPED 9 GB) | Bloated | **IGNORE** | — | Never copy; re-clip only what's needed |
| `copy copy copy` layers, `OLD LAYERS`, sync-conflict files | Clutter | **ARCHIVE** | — | Leave in x_LANDSCAPE; don't bring across |

## The three highest-impact fixes (in order)
1. **De-CORINE the land cover.** Replace CORINE with **SIGPAC** (parcel crops → real agri matrix + ha, map 4.5) and **MFE + Copernicus Small Woody Features** (real forest/scrub/hedgerows, map 4.6). This single swap fixes readability *and* feeds a better resistance map (5.2) and habitat map (5.1).
2. **Finer DEM where it matters.** Territorial maps are fine on 30 m, but the barranco sections (§8) and 1:5000 interventions (§7) need **PNOA LiDAR MDT 2 m/5 m** for the Valcuerna corridor + 5 intervention tiles. Small download, big quality gain.
3. **Build reusable layouts.** One `.qpt` template (shared legend/scale/north) for territorial maps + one **Atlas** over your existing 1 km grid for the 5 intervention sheets. Nothing reproducible exists yet — this is where "not readable" gets solved.

## Data handling (tidy without moving 200 GB)
- **x_LANDSCAPE stays put as the data vault** — do not duplicate the big files.
- New **master project** lives clean at `02_QGIS/LANDSCAPE_MASTER.qgz`, pointing at the good existing layers + the new SIGPAC/MFE/DEM downloads.
- Only *new* processed outputs, styles, layouts, exports, and deliverables live in the clean `LANDSCAPE/` tree.
- Salvaged raw layers we do want long-term (SIGPAC, MFE, PNOA 2 m, CHE hydro subset) get re-clipped into `01_DATA/`, slim and reprojected to 25830.
