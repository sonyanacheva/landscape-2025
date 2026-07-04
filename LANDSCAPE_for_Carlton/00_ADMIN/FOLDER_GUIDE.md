# Folder guide — LANDSCAPE (clean working home)

This folder is now the **single source of truth**. Everything old/uncertain stays quarantined in `99_ARCHIVE_OLD/` until we've scrutinised it — nothing from the old tries goes live without a check.

```
LANDSCAPE/
├── PRODUCTION_PLAYBOOK.md      ← the battle plan (top-level reference)
├── 00_ADMIN/                   ← brief, this guide, name + A4 memory drafts
├── 01_DATA/                    ← RAW downloads only (never edit in place)
│   ├── DEM/                    MDT 2m/5m (CNIG)
│   ├── hydro/                  CHE rivers/barrancos, SNCZI flood zones
│   ├── landcover/              SIGPAC, MFE, Copernicus SWF/TCD, canopy height
│   ├── natura2000/             MITECO + IDEAragón RNA / Hunilla
│   ├── geology/                IGME MAGNA50
│   ├── infrastructure_osm/     QuickOSM exports (roads/rail/canals/bridges)
│   └── reference/              WWF corridor, orthophoto cache, screenshots
├── 02_QGIS/                    ← project + styling
│   ├── LANDSCAPE.qgz           the working project (one file)
│   ├── styles/                 .qml symbology per layer
│   └── layouts/                .qpt print templates (shared style)
├── 03_PROCESSED/               ← derived layers we generate (flow, erosion,
│                                 resistance, least-cost path, suitability)
├── 04_EXPORTS/                 ← finished maps: 300dpi PNG + vector PDF
│   ├── panel1/ panel2/ panel3/
├── 05_FIGMA_ASSEMBLY/          ← assets staged for Figma
├── 06_DELIVERABLES/            ← final A0 panels, A3 dossier, A4 memory
├── 07_SCRIPTS/                 ← PyQGIS / Processing scripts (versioned)
└── 99_ARCHIVE_OLD/             ← old QGIS project, previous tries, partial data
                                  (quarantine — copy here, don't delete originals)
```

## Naming conventions
- Maps/exports: `P{panel}_{section}_{name}_{scale}.{ext}` → e.g. `P1_4-5_agri-matrix_50k.png`
- Processed layers: `proc_{what}.tif/gpkg` → e.g. `proc_resistance.tif`, `proc_lynx-LCP.gpkg`
- CRS for everything: **EPSG:25830** (ETRS89 / UTM 30N)

## What to drop where (when you copy your current work in)
1. **Downloaded raw data** (DEM, SIGPAC, MFE, Natura2000, etc.) → matching `01_DATA/` subfolder. This is the most reusable part of your old work — keep it.
2. **Your current .qgz project + any scripts** → `99_ARCHIVE_OLD/` first. We open it, judge each layer, and promote only the good ones into `02_QGIS/`.
3. **Old map exports / screenshots** you want me to critique → `99_ARCHIVE_OLD/exports/`.
4. Don't hand-sort the messy stuff — dump it in `99_ARCHIVE_OLD/` and I'll triage.

## Rule of thumb
Raw data is almost always worth salvaging. Styling, layouts, and "final" maps we rebuild from the playbook so they're readable and carry the narrative — that's the part you weren't happy with anyway.
