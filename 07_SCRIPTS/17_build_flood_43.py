#!/usr/bin/env python3
# 17_build_flood_43.py
# Build the 4.3 flood overlay from the SNCZI flood-extent (láminas) T=100 + T=500.
# Clips to the study box, reprojects to EPSG:25830, tags the return period. These are the
# fluvial flood zones along the studied rivers (Cinca/Alcanadre/Ebro); ephemeral barrancos
# like the Valcuerna are not in SNCZI. Run headless. Output: 03_PROCESSED/flood_43.fgb
import os, warnings
import geopandas as gpd, pandas as pd
from shapely.geometry import box as shp_box
warnings.filterwarnings('ignore')

Q100 = os.environ['Q100']
Q500 = os.environ['Q500']
OUT  = os.environ.get('OUT', 'flood_43.fgb')
BOX  = (714913, 4582331, 784950, 4639785)
BOXG = shp_box(*BOX)

def load(path, periodo):
    g = gpd.read_file(path, bbox=BOX).to_crs(25830)
    g = gpd.clip(g, BOXG)
    g = g[~g.geometry.is_empty & g.geometry.notna()].copy()
    g['periodo'] = periodo
    keep = [c for c in ['periodo', 'RIO', 'ZONA', 'geometry'] if c in g.columns or c == 'periodo']
    return g[keep]

# T=500 first (larger extent, drawn under), then T=100 on top
f500 = load(Q500, 'T=500 (excepcional)')
f100 = load(Q100, 'T=100 (ocasional)')
flood = gpd.GeoDataFrame(pd.concat([f500, f100], ignore_index=True), crs=25830)
flood['ha'] = flood.geometry.area / 1e4
flood.to_file(OUT, driver='FlatGeobuf', layer='flood')

print('=== 4.3 flood overlay (in box) ===')
for p, sub in flood.groupby('periodo'):
    print(f'  {p:22} {len(sub)} polygons, {sub.ha.sum():,.0f} ha, rivers: {sorted(sub.RIO.dropna().unique())[:5]}')
