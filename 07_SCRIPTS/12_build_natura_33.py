#!/usr/bin/env python3
# 12_build_natura_33.py
# Build the §3.3 Natura 2000 layer from the MITECO RN2000 Peninsula file. Selects whole
# sites intersecting the study box, classifies designation (LIC/ZEC/ZEPA), computes full-
# site hectares, and emits the auto-ha legend table (code · name · type · ha).
# NOTE: RN2000 naming — `_p` = Península (use this), `_c` = Canarias.
#
# Run: python3 12_build_natura_33.py
# Outputs: 03_PROCESSED/natura2000_box.fgb + 00_ADMIN/natura2000_legend.csv
import os, warnings
import geopandas as gpd
from shapely.geometry import box as shp_box
warnings.filterwarnings('ignore')

SRC = os.environ['SRC']                       # PS_Natura2000_2025_p.shp
OUT = os.environ.get('OUT', 'natura2000_box.fgb')
CSV = os.environ.get('CSV', 'natura2000_legend.csv')
BOX = (714913, 4582331, 784950, 4639785)

def desig(url):
    u = (url or '').lower()
    if 'specialprotectionarea' in u:                       return 'ZEPA'
    if 'specialareaofconservation' in u:                   return 'ZEC'
    if 'siteofcommunityimportance' in u:                   return 'LIC'   # incl. proposed
    return None

g = gpd.read_file(SRC).to_crs(25830)
sel = g[g.intersects(shp_box(*BOX))].copy()               # whole sites touching the box

# combine designations across desig0/1/2 → ZEC/ZEPA/both
def combine(row):
    tags = {desig(row.get(c)) for c in ('desig0', 'desig1', 'desig2')} - {None}
    if not tags:   # fallback: Spanish code convention — ES0000* = ZEPA (Birds Directive)
        if str(row.get('localId', '')).startswith('ES0000'):
            tags = {'ZEPA'}
    return ' + '.join(sorted(tags)) if tags else 'Natura 2000'
sel['tipo'] = sel.apply(combine, axis=1)
sel['codigo'] = sel['localId']
sel['nombre'] = sel['SOName']
sel['ha'] = sel.geometry.area / 10000.0

sel[['codigo', 'nombre', 'tipo', 'ha', 'geometry']].to_file(OUT, driver='FlatGeobuf', layer='natura2000')

leg = sel[['codigo', 'nombre', 'tipo', 'ha']].sort_values('ha', ascending=False)
leg.to_csv(CSV, index=False, float_format='%.0f')
print(f'\n=== §3.3 Natura 2000 — {len(sel)} sites intersecting box ===')
print(f"{'code':11} {'type':10} {'ha':>9}  name")
for _, r in leg.iterrows():
    print(f"{r.codigo:11} {r.tipo:10} {r.ha:>9,.0f}  {r.nombre}")
print(f"\nTotal (whole-site) ha: {leg.ha.sum():,.0f}  → legend CSV: {CSV}")
