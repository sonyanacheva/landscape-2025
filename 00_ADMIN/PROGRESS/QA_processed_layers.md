# QA PASS — processed layers (11 fgb across 7 maps)
_Ran 2026-07-04 on everything in `03_PROCESSED`. CRS, geometry, class coverage, renderer↔data match, extent, cross-consistency._

## Verdict: PASS (1 issue found + fixed)

### 1. Renderer ↔ data category match — ✅ PASS (the important one)
For every layer, checked that the field + category labels in `load_maps.py` exactly match the values in the data. **0 unmatched values, 0 nulls, all EPSG:25830.** Nothing will silently fall through to "Other" when styled.
- Two *empty* catch-all categories exist (geomorph `Other`, barriers `Other major road`) — 0 features, harmless safety nets. Carlton can delete the empty legend rows in the layout, or leave them.

### 2. Geometry validity — ⚠️ 1 issue → ✅ FIXED
- `agri_matrix_45.fgb` had **114 invalid polygons** (0.04%, self-intersections from the 3 m simplify). Repaired with `make_valid` (114 → 0, all 298,434 features retained). Fix **baked into `03_build_agri_matrix_45.py`** (simplify + make_valid + polygon-only filter) so re-runs stay clean.
- All other 10 layers: 0 invalid, 0 empty.

### 3. Extent — ✅ expected
- Only `agri_matrix_45` extends past the box, by design (whole parcels touching the frame). Overhang = **9,259 ha (2.5%)**. Precise-clip to the frame stays **optional** — Carlton can clip at layout; full-parcel keeps attributes intact.
- All other layers sit within box + margin (no stray geometries; the earlier springs outlier was already bbox-filtered out).

### 4. Cross-consistency SIGPAC (4.5) vs MFE (4.6) — ✅ sane
- **Forest:** SIGPAC 25,964 ha vs MFE 28,407 ha (Huesca) — close agreement, reassuring.
- **Scrub-ish:** SIGPAC 73,164 ha vs MFE 40,165 ha — differs as expected (SIGPAC covers both provinces + counts *pasto arbustivo*; MFE is Huesca-only, different taxonomy). Not an error.

## Notes / not-yet-done
- `canada_landcover.fgb` was derived from the pre-repair agri (0.04% invalid); the overlay is a length statistic robust to that noise → **not re-run** (within tolerance). Re-run after the next agri change if desired.
- Dead legend entries (see §1) are cosmetic.
- When MFE-Zaragoza lands, re-run 4.6 → the 4.5/4.6 scrub cross-check should tighten.
