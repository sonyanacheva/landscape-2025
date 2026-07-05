#!/usr/bin/env python3
# 23_build_frame_towns.py
# Two small context layers used across the territorial maps:
#   - aos_frame.fgb : the AREA OF STUDY rectangle (66 × 53.5 km) as a frame outline
#   - towns_33.fgb  : populated places in the box (name + place + population) for §3.3 labels
# Run headless. Outputs to 03_PROCESSED/.
import os, warnings
import geopandas as gpd
from shapely.geometry import box as shp_box
warnings.filterwarnings('ignore')

TOWNS_SRC=os.environ['TOWNS']; OUT=os.environ.get('OUT','.')
AOS=(716913, 4584331, 782950, 4637785)   # AREAOFSTUDY (the 66×53.5 km frame), EPSG:25830
BOX=(714913, 4582331, 784950, 4639785)

# AOS frame (single rectangle outline)
frame=gpd.GeoDataFrame({'name':['AREA OF STUDY']}, geometry=[shp_box(*AOS)], crs=25830)
frame.to_file(os.path.join(OUT,'aos_frame.fgb'), driver='FlatGeobuf', layer='aos_frame')

# towns in box
t=gpd.read_file(TOWNS_SRC).to_crs(25830)
t=t[t.intersects(shp_box(*BOX))].copy()
try: t['geometry']=t.geometry.force_2d()
except Exception: pass
t['pop']=t['population'].fillna('0').astype(str).str.extract(r'(\d+)').fillna('0').astype(int) if 'population' in t else 0
keep=[c for c in ['name','place','pop','geometry'] if c in t.columns]
t[keep].to_file(os.path.join(OUT,'towns_33.fgb'), driver='FlatGeobuf', layer='towns')

print(f"aos_frame: 1 rectangle ({(AOS[2]-AOS[0])/1000:.0f}×{(AOS[3]-AOS[1])/1000:.0f} km)")
print(f"towns in box: {len(t)}  ({t.place.value_counts().to_dict() if 'place' in t else ''})")
print("  biggest:", t.nlargest(5,'pop')[['name','pop']].values.tolist() if 'pop' in t else '')
