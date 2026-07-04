# ANALYSIS — Cañada network × land cover (corridor readiness)
_Data in hand only (no new downloads). Inputs: `canadas_4x.fgb` (RGVP, box-clipped) × `agri_matrix_45.fgb` (SIGPAC, whole box, both provinces). Script: `07_SCRIPTS/06_analyze_canada_landcover.py`. Output layer: `03_PROCESSED/canada_landcover.fgb` (+ preview). CRS 25830._

**Why:** the cañadas are the "implementable on public land" spine for §6. This asks: how much of that spine is already embedded in semi-natural cover (works as corridor + hedgerow now) vs cuts through intensive farmland (needs intervention)? Feeds 4.x, 5.2 resistance logic, and §6 intervention siting.

## Two complementary cuts

### 1. Centre-line — is the legal spine intact on the ground?
Overlay of the cañada centre-lines on SIGPAC parcels (1,225 km overlaid):
- **64% runs on "Non-agricultural" parcels** — i.e. the drover's roads' own viales/improductivo footprint. Read positively: **the legal corridor surface is largely still open and unploughed**, not cultivated over.
- Remainder: Scrub 12% · Arable dryland 12% · Arable irrigated 6% · Grazed scrub 3% · Woody 2% · Forest 1%.
- ⚠️ *Caveat:* a centre-line samples the parcel it sits in, which is often the road itself — so this cut measures spine integrity, not surroundings.

### 2. Buffered matrix (100 m each side, 200 m band, 10,056 ha) — what it passes through
Area-weighted land cover of the corridor's surroundings — the cut that sites interventions:
| Readiness tier | ha | % |
|---|---|---|
| Semi-natural (corridor-ready) — scrub, grazed scrub, forest, pasture | 2,544 | 25% |
| Extensive farmland (permeable) — dryland arable, woody crops | 2,814 | 28% |
| **Intensive farmland (barrier) — irrigated arable, horticulture** | **1,465** | **15%** |
| Other / non-agricultural (roads, water, spine footprint) | 3,232 | 32% |

## Headline for §6
- **~53% of the corridor band is already permeable or semi-natural** — the network is a largely-functional backbone before any planting.
- **~1,465 ha (15%) sits in intensive irrigated farmland** — the priority stretches for hedgerows / field-corner planting / crossing structures. On the map these cluster where the network meets irrigation, incl. **near the Hunilla lagoon (SE)** — consistent with the known "Hunilla cut off by intensive agri machinery" problem (§6a).
- Green (ready) concentrates through the central **Valcuerna / badland** zone — the spine to reactivate first.

## Readiness scheme (transparent, revisit if needed)
Semi-natural = Scrub, Grazed scrub / pasto arbustivo, Forest, Pasture (open) · Extensive = Arable dryland, Woody crops · Intensive = Arable irrigated, Horticulture · Other = Non-agricultural. Tune the tiers with Sonya if the teacher wants a different permeability read.

## Caveats
- Land-cover base = SIGPAC agri matrix (whole box). When MFE-Zaragoza lands and 4.6 is box-complete, an MFE-based re-run would sharpen the semi-natural read (scrub/forest structure).
- Buffer = uniform 100 m; not the legal per-type width. Change via `BUF` env var. Whole-parcel edge effects as in 4.5.
