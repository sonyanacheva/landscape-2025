#!/usr/bin/env python3
# 18_build_corridor_3.py
# Build the §3 corridor + critical-points layers from the vault export.
#   corredores_prioritarios → national LCP corridor network; flag the links through the
#     study area (in_study) → 3.1 (Spain, all corridors, ours highlighted) + 3.2.
#   zonas_criticas → WWF critical zones; flag the in-box one → 3.4.
# Run headless. Outputs to 03_PROCESSED/.
import os, warnings
import geopandas as gpd
from shapely.geometry import box as shp_box
warnings.filterwarnings('ignore')

SRC = os.environ['SRC']      # context folder
OUT = os.environ.get('OUT', '.')
BOX = shp_box(714913, 4582331, 784950, 4639785)

# corridor network (keep national extent for the 3.1 map; flag study links)
cor = gpd.read_file(os.path.join(SRC, 'corredores_prioritarios.gpkg')).to_crs(25830)
cor['in_study'] = cor.intersects(BOX)
cor['clase'] = cor['in_study'].map({True: 'Corridor through study area', False: 'Priority corridor network'})
cor[['Link_ID', 'From_Core', 'To_Core', 'LCP_Length', 'clase', 'geometry']].to_file(
    os.path.join(OUT, 'corridor_3.fgb'), driver='FlatGeobuf', layer='corridor')

# critical zones (WWF) — flag the in-box one(s)
zc = gpd.read_file(os.path.join(SRC, 'zonas_criticas.gpkg')).to_crs(25830)
zc['in_study'] = zc.intersects(BOX)
zc['clase'] = zc['in_study'].map({True: 'Critical zone (study area)', False: 'Critical zone (national)'})
keep = [c for c in ['zona_wwf', 'area_ha', 'clase', 'geometry'] if c in zc.columns]
zc[keep].to_file(os.path.join(OUT, 'zonas_criticas_34.fgb'), driver='FlatGeobuf', layer='zonas_criticas')

print(f"§3 corridor built: {len(cor)} links ({cor.in_study.sum()} through study area).")
print(f"Critical zones: {len(zc)} ({zc.in_study.sum()} in box) → {zc[zc.in_study]['zona_wwf'].tolist()}")
