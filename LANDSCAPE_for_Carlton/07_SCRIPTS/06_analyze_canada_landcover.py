#!/usr/bin/env python3
# 06_analyze_canada_landcover.py
# Overlay the cañada / vías-pecuarias network on the 4.5 agricultural-matrix land cover
# (whole-box, both provinces) to quantify what each km of the protected public spine
# runs through: semi-natural (corridor-ready) vs farmland (hedgerow-intervention needed).
# Feeds 4.x argument, 5.2 resistance logic, and §6 masterplan (where interventions go).
#
# Run: python3 06_analyze_canada_landcover.py
# Outputs: 03_PROCESSED/canada_landcover.fgb (segments tagged agri_class + readiness)
import os, warnings
import geopandas as gpd
warnings.filterwarnings('ignore')

CAN  = os.environ.get('CAN',  '/tmp/build/canadas_4x.fgb')
AGRI = os.environ.get('AGRI', '/tmp/build/agri_matrix_45_s3.fgb')
OUT  = os.environ.get('OUT',  'canada_landcover.fgb')

# agri_class -> corridor-readiness tier (lynx/hedgerow lens; transparent + defensible)
READY = {
    'Scrub (matorral)':               'Semi-natural (corridor-ready)',
    'Grazed scrub / pasto arbustivo': 'Semi-natural (corridor-ready)',
    'Forest':                         'Semi-natural (corridor-ready)',
    'Pasture (open)':                 'Semi-natural (corridor-ready)',
    'Arable dryland':                 'Extensive farmland (permeable)',
    'Woody crops':                    'Extensive farmland (permeable)',
    'Arable irrigated':               'Intensive farmland (barrier)',
    'Horticulture/greenhouse':        'Intensive farmland (barrier)',
    'Non-agricultural':               'Other / non-agricultural',
}

can  = gpd.read_file(CAN)[['tipo', 'geometry']].to_crs(25830)
agri = gpd.read_file(AGRI)[['agri_class', 'geometry']].to_crs(25830)

# subset agri to polygons the network actually touches (speed) then intersect lines×polys
cand = gpd.sjoin(agri, can[['geometry']], predicate='intersects').drop(columns='index_right').drop_duplicates('geometry')
seg  = gpd.overlay(can, cand, how='intersection', keep_geom_type=True)
seg['km']        = seg.geometry.length / 1000.0
seg['readiness'] = seg['agri_class'].map(READY).fillna('Other / non-agricultural')
seg.to_file(OUT, driver='FlatGeobuf', layer='canada_lc')

total = seg.km.sum()
print(f"\nCañada km overlaid on land cover: {total:,.0f} km\n")
print("=== by land-cover class ===")
by_c = seg.groupby('agri_class')['km'].sum().sort_values(ascending=False)
for k, v in by_c.items():
    print(f"  {k:34} {v:>7,.0f} km  {100*v/total:>4.0f}%")
print("\n=== by corridor-readiness tier ===")
order = ['Semi-natural (corridor-ready)', 'Extensive farmland (permeable)',
         'Intensive farmland (barrier)', 'Other / non-agricultural']
by_r = seg.groupby('readiness')['km'].sum()
for k in order:
    if k in by_r:
        print(f"  {k:34} {by_r[k]:>7,.0f} km  {100*by_r[k]/total:>4.0f}%")
# headline for cañadas specifically (the ≤75 m protected spine)
cn = seg[seg.tipo == 'Cañada']
if len(cn):
    cnr = cn.groupby('readiness')['km'].sum(); ct = cn.km.sum()
    print(f"\n=== CAÑADAS only ({ct:,.0f} km) ===")
    for k in order:
        if k in cnr:
            print(f"  {k:34} {cnr[k]:>7,.0f} km  {100*cnr[k]/ct:>4.0f}%")

# --- BUFFERED MATRIX: what the corridor runs THROUGH (surroundings, area-weighted) ---
# Buffer 100 m each side (200 m band), dissolve to avoid double-count, intersect agri, area by class.
BUF = float(os.environ.get('BUF', '100'))
band = can.buffer(BUF).unary_union
band = gpd.GeoDataFrame(geometry=[band], crs=25830)
mat = gpd.overlay(cand.reset_index(drop=True), band, how='intersection', keep_geom_type=True)
mat['ha']        = mat.geometry.area / 10000.0
mat['readiness'] = mat['agri_class'].map(READY).fillna('Other / non-agricultural')
tot_ha = mat.ha.sum()
print(f"\n=== BUFFERED MATRIX ({BUF:.0f} m each side, {tot_ha:,.0f} ha) — surroundings the spine passes through ===")
mr = mat.groupby('readiness')['ha'].sum()
for k in order:
    if k in mr:
        print(f"  {k:34} {mr[k]:>8,.0f} ha  {100*mr[k]/tot_ha:>4.0f}%")
print("  --- by class ---")
for k, v in mat.groupby('agri_class')['ha'].sum().sort_values(ascending=False).items():
    print(f"  {k:34} {v:>8,.0f} ha  {100*v/tot_ha:>4.0f}%")
