# §3 COMPOSITION SPEC — Work area in the Iberian corridor network
_Panel A0-1, top band. Ready to execute once the vault `context\` bundle lands (see DATA_REQUEST_for_Sonya.md). Benchmark for clarity = the Geomorphology map. Every sheet: scale bar + north, line-weight hierarchy + poché, quantified legend, 300 dpi. CRS 25830._

**Shared template:** build ONE `.qpt` layout template (shared legend box, scale bar, north arrow, title block) and reuse across 3.1–3.4 so the band reads as a set. Nest scales as insets (3.1 locates 3.2 locates 3.3/3.4).

---
## 3.1 — Spain + priority corridor network (≈1:3,000,000)
**Argues:** where the "Sierras Litorales del Mediterráneo" corridor sits nationally.
- **Layers (bottom→top):** Spain CCAA/provinces (light poché, thin outline) · all priority corridors (muted grey-green) · **"Sierras Litorales del Mediterráneo" highlighted** (single saturated accent) · study-area locator dot/frame.
- **Style:** minimal national base, one accent colour only; everything else desaturated so the highlighted corridor pops (figure-ground). Thin hairline admin borders.
- **Legend:** corridor network / highlighted corridor / study area. Small.

## 3.2 — Cataluña–Aragón zoom (≈1:500,000)
**Argues:** place the work area within the corridor + main territorial units.
- **Layers:** provinces (Cataluña + Aragón) · corridor (same accent as 3.1) · main territorial units / comarcas · **AREAOFSTUDY frame** (66×53.5 km box) as a bold locator rectangle · main towns.
- **Style:** carry 3.1's accent; add place labels; AREAOFSTUDY frame in the panel's "subject" line-weight.

## 3.3 — Work area + Natura 2000 (≈1:50,000)
**Argues:** the protected sites the corridor must connect — named and quantified.
- **Layers:** AREAOFSTUDY frame · **Natura 2000** (LIC/ZEC + ZEPA, categorized by type) · ESPACIOS_H1–H3 · main river (Valcuerna / Cinca / Ebro) · towns · study box.
- **Legend = the deliverable here:** each site as **ID · name · hectares** (auto-computed — see below).
- **Style:** Natura polygons as light fills with distinct outline per designation; river in hydro blue; poché the frame surround so the work area reads as figure.

## 3.4 — Critical points / corridor discontinuities (≈1:50,000)
**Argues:** where the corridor breaks, and which Natura sites need reconnecting.
- **Layers:** Natura 2000 sites to connect (from 3.3) · **barriers**: canals (OSM `waterway=canal`), major roads, rail · `Zonas_Criticas` · crossing/underpass points · Valcuerna spine.
- **Style:** barriers in a warning line-weight/hatch; discontinuity points marked (numbered) with callouts; keep base muted so breaks read instantly.
- **Depends on:** OSM run (barriers) + vault `Zonas_Criticas` + crossings.

---
## Auto-ha Natura 2000 legend — logic (script when data lands)
Once `01_DATA\context\natura2000.gpkg` exists:
1. Reproject → 25830 (if needed); optionally **clip to the AREAOFSTUDY frame** (decide: full-site ha vs in-frame ha — recommend **full-site ha**, footnote any site only partly in frame).
2. Dissolve by **site code** (field TBC — likely `CODIGO` / `SITECODE`); keep the **name** field (`NOMBRE` / `SITE_NAME`).
3. Compute area → hectares (`geometry.area / 10000`).
4. Emit an ordered table **code · name · ha** → feeds the 3.3 legend (and a small QGIS-friendly CSV/attribute for label-driven legend).
- **Needs from the export:** the site-code + site-name fields intact (flagged in the data request). Claude writes `06_natura_ha_legend.py` (build step) + adds a `renderer_natura()` block to `load_maps.py` once the real field names are confirmed from the delivered file.

## Build order once data lands
1. Confirm Natura field names → run auto-ha → 3.3 legend table.
2. §3 is mostly **composition on existing vault layers**, so **Carlton can build 3.1–3.4 in parallel** with Claude's §4/§5 analysis (which waits on the DEM). Claude supplies: the highlighted-corridor selection, the AREAOFSTUDY frame layer, the Natura ha table, and `.qml`/renderer styles; Carlton composes to the `.qpt` template + exports.
