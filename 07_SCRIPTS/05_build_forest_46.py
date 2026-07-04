#!/usr/bin/env python3
# 05_build_forest_46.py
# Build the 4.6 Forest / scrub / natural-veg layer from the MFE50 (Mapa Forestal).
# Clips MFE to the study box, reclassifies DEFINICION -> natural-veg class (agriculture
# is 4.5's job, so it's muted to a single context class here), recomputes ha on the
# clipped geometry, writes FlatGeobuf (mount-safe).
#
# ⚠️ MFE ships per province: this file is HUESCA (22) only. The box also covers a
# Zaragoza (50) strip -> that area is blank until MFE50_50 is sourced. Re-run then.
#
# Run: python3 05_build_forest_46.py
# Output: 03_PROCESSED/forest_46.fgb  (layer 'mfe', EPSG:25830, polygons)
import os, warnings
import geopandas as gpd, pyogrio
from shapely.geometry import box as shp_box
warnings.filterwarnings('ignore')

MFE = os.environ.get('MFE', '/tmp/mfe/mfe50_22.shp')
OUT = os.environ.get('OUT', 'forest_46.fgb')
BOX = (714913, 4582331, 784950, 4639785)   # clip box (AOS + 2 km), EPSG:25830

# DEFINICION -> 4.6 class. Default (agri/artificial/water/infra) -> muted context.
CLASS = {
    'Bosque':                                      'Forest (natural)',
    'A.F.M. (Bosquetes)':                          'Forest (natural)',
    'Mosaico arbolado sobre cultivo':              'Forest (natural)',
    'Mosaico arbolado sobre forestal desarbolado': 'Forest (natural)',
    'Complementos del bosque':                     'Forest (natural)',
    'Bosque Plantación':                           'Forest (plantation)',
    'A.F.M. (Riberas)':                            'Riparian woodland (riberas)',
    'Matorral':                                    'Scrub (matorral)',
    'Pastizal-Matorral':                           'Grassland–scrub mosaic',
    'Herbazal':                                    'Grassland (natural)',
    'Prado':                                       'Grassland (natural)',
    'Humedal':                                     'Wetland (humedal)',
    'Monte sin vegetación superior':               'Bare / sparse',
}
def reclass(d): return CLASS.get(d, 'Non-forest context (agri/artificial/water)')

g = pyogrio.read_dataframe(MFE, bbox=BOX)              # EPSG:25830 already
clip = gpd.clip(g, shp_box(*BOX))
clip = clip[~clip.geometry.is_empty & clip.geometry.notna()].copy()
clip['clase'] = clip['DEFINICION'].map(reclass)
clip['ha']    = clip.geometry.area / 10000.0

cols = ['DEFINICION', 'USOS_SUELO', 'NOM_FORARB', 'TFCCARB', 'clase', 'ha', 'geometry']
clip[cols].to_file(OUT, driver='FlatGeobuf', layer='mfe')

order = ['Forest (natural)', 'Forest (plantation)', 'Riparian woodland (riberas)',
         'Scrub (matorral)', 'Grassland–scrub mosaic', 'Grassland (natural)',
         'Wetland (humedal)', 'Bare / sparse', 'Non-forest context (agri/artificial/water)']
s = clip.groupby('clase')['ha'].sum()
print('\n=== 4.6 Forest / scrub / natural veg — in-box (Huesca only) ===')
for c in order:
    if c in s.index:
        print(f'{c:44} {s[c]:>11,.0f} ha')
print(f'{"TOTAL (Huesca coverage)":44} {s.sum():>11,.0f} ha   polygons: {len(clip):,}')
