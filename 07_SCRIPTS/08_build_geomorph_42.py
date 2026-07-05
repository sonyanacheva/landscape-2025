#!/usr/bin/env python3
# 08_build_geomorph_42.py
# Build the 4.2 Geomorphology layer from GEODE (IGME). Box-clips, collapses the 58
# lithological DESC_UNIT descriptions into ~11 geomorphological LANDFORM classes with
# the Monegros signature foregrounded (gypsum badlands, mudstone badlands, saladas/
# endorheic basins, terraces, glacis). DEM geomorphons deferred until the 5 m DEM lands.
#
# Run: python3 08_build_geomorph_42.py
# Output: 03_PROCESSED/geomorph_42.fgb (layer 'geomorph', EPSG:25830, polygons)
import os, warnings, re
import geopandas as gpd
from shapely.geometry import box as shp_box
warnings.filterwarnings('ignore')

SRC = os.environ.get('SRC', 'GEODE_WIP _ recintos_clip.gpkg')
LYR = 'GEODE_WIP _ recintos_clip'
OUT = os.environ.get('OUT', 'geomorph_42.fgb')
BOX = (714913, 4582331, 784950, 4639785)

def landform(d):
    s = (d or '').lower()
    if 'endorre' in s:                                   return 'Endorheic basin / salada'
    if 'masa de agua' in s:                              return 'Water body'
    if 'yeso' in s:                                      return 'Gypsum badlands (yesos)'
    if 'glacis' in s:                                    return 'Glacis / pediment'
    if 'terraza' in s or 'abanico' in s:                 return 'River terrace / fan'
    if any(k in s for k in ('aluvial','fondo de valle','llanura de inund','barra')): return 'Alluvial valley floor'
    if any(k in s for k in ('coluvi','canchal','cono de dey','piedemonte')):         return 'Colluvium / slope deposit'
    if 'lutita' in s:                                    return 'Mudstone badlands (lutitas)'
    if any(k in s for k in ('caliza','marga','costra')): return 'Limestone / marl platform'
    if any(k in s for k in ('arenisca','paleocanal','conglomerad')):                 return 'Sandstone / paleochannel'
    return 'Other'

g = gpd.read_file(SRC, layer=LYR, bbox=BOX)
g = gpd.clip(g, shp_box(*BOX))
g = g[~g.geometry.is_empty & g.geometry.notna()].copy()
g['geomorph'] = g['DESC_UNIT'].map(landform)
g['ha'] = g.geometry.area / 10000.0
g[['DESC_UNIT', 'NAME_EDA1', 'geomorph', 'ha', 'geometry']].to_file(OUT, driver='FlatGeobuf', layer='geomorph')

order = ['Gypsum badlands (yesos)', 'Mudstone badlands (lutitas)', 'Sandstone / paleochannel',
         'Limestone / marl platform', 'Glacis / pediment', 'River terrace / fan',
         'Alluvial valley floor', 'Colluvium / slope deposit', 'Endorheic basin / salada',
         'Water body', 'Other']
s = g.groupby('geomorph')['ha'].sum()
print('\n=== 4.2 Geomorphology — landform classes (in box) ===')
for k in order:
    if k in s.index:
        print(f'{k:32} {s[k]:>10,.0f} ha  {100*s[k]/s.sum():>4.0f}%')
print(f'{"TOTAL":32} {s.sum():>10,.0f} ha   polygons: {len(g):,}  (from 58 units → {g.geomorph.nunique()} classes)')
