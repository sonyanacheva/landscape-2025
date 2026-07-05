#!/usr/bin/env python3
# 22_build_interventions_6a.py
# Stage the §6a masterplan interventions — grounded proposals from the analysis:
#   - Fauna crossings at the open barrier × corridor points (from 4.4 crossings)
#   - Hedgerow / field-corner nodes where cañadas cross intensive farmland (4.x-b readiness)
# Output: 03_PROCESSED/interventions_6a.fgb (points, tipo + priority).
# (Hunilla reconnection + the exact intervention set are Sonya/teacher design calls.)
import os, warnings
import geopandas as gpd, pandas as pd
warnings.filterwarnings('ignore')

CROSS=os.environ['CROSS']; CANLC=os.environ['CANLC']; OUT=os.environ.get('OUT','interventions_6a.fgb')

feats=[]
# 1. fauna crossings (open = priority)
cr=gpd.read_file(CROSS).to_crs(25830)
for _,r in cr.iterrows():
    prio = 'priority' if str(r.get('structure','')).startswith('Open') else 'verify'
    feats.append({'tipo':'Fauna crossing','detail':str(r.get('barrier_type','')),'priority':prio,'geometry':r.geometry})

# 2. hedgerow nodes: intensive-farmland cañada segments (>400 m) → representative points
cl=gpd.read_file(CANLC).to_crs(25830)
intens=cl[cl.readiness=='Intensive farmland (barrier)'].copy()
intens['len']=intens.geometry.length
for _,r in intens[intens.len>400].iterrows():
    feats.append({'tipo':'Hedgerow / field-corner','detail':'cañada × intensive crop','priority':'priority','geometry':r.geometry.interpolate(0.5, normalized=True)})

g=gpd.GeoDataFrame(feats, crs=25830)
try: g['geometry']=g.geometry.force_2d()
except Exception: pass
g.to_file(OUT, driver='FlatGeobuf', layer='interventions')
print("§6a interventions staged:")
print(g.groupby(['tipo','priority']).size().to_string())
print("total:", len(g), "nodes")
