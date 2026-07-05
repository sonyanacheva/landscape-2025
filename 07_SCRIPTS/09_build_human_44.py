#!/usr/bin/env python3
# 09_build_human_44.py
# Build the 4.4 Human pressure / barriers layer set. Box-clips + classifies the
# corridor-fragmenting infrastructure (motorway / main road / railway / canal), the
# crossing-point catalogue (flagging existing bridge/tunnel vs open barrier), and the
# 250 m human-pressure envelope. Feeds 4.4 and the 3.4 critical-points map.
#
# Run: python3 09_build_human_44.py
# Outputs (03_PROCESSED/, EPSG:25830):
#   barriers_44.fgb        (lines:  Motorway/autovía · Main road · Railway · Canal)
#   crossings_44.fgb       (points: corridor × barrier, structure flag)
#   human_pressure_44.fgb  (poly:   250 m human-pressure zone)
import os, warnings
import geopandas as gpd
from shapely.geometry import box as shp_box
warnings.filterwarnings('ignore')

D   = os.environ['D']            # DATA drop folder
OUT = os.environ.get('OUT', '.')
BOX = (714913, 4582331, 784950, 4639785)
BOXG = shp_box(*BOX)

def clip(f, layer):
    g = gpd.read_file(f, layer=layer, bbox=BOX)
    if len(g):
        g = gpd.clip(g, BOXG).to_crs(25830)
        g = g[~g.geometry.is_empty & g.geometry.notna()]
        try: g['geometry'] = g.geometry.force_2d()
        except Exception: pass
    return g

def barrier_type(r):
    if str(r.get('railway')) == 'rail':   return 'Railway (incl. HS line)'
    if str(r.get('waterway')) == 'canal': return 'Canal'
    h = str(r.get('highway'))
    if h in ('motorway', 'motorway_link', 'trunk', 'trunk_link'): return 'Motorway / autovía'
    if h in ('primary', 'secondary', 'primary_link', 'secondary_link'): return 'Main road (N / primary)'
    return 'Other major road'

def has_structure(r):
    b = str(r.get('bridge')); t = str(r.get('tunnel'))
    return b in ('yes', 'viaduct', 'aqueduct') or t in ('yes', 'culvert', 'building_passage')

# ---- barriers --------------------------------------------------------------
bar = clip(os.path.join(D, 'infrastructure_osm/osm_barriers.gpkg'), 'osm_barriers')
bar['barrier_type'] = bar.apply(barrier_type, axis=1)
bar['km'] = bar.geometry.length / 1000.0
bar[['barrier_type', 'name', 'bridge', 'tunnel', 'km', 'geometry']].to_file(
    os.path.join(OUT, 'barriers_44.fgb'), driver='FlatGeobuf', layer='barriers')

# ---- crossings catalogue ---------------------------------------------------
cr = clip(os.path.join(D, 'infrastructure_osm/osm_crossings.gpkg'), 'osm_crossings')
cr['barrier_type'] = cr.apply(barrier_type, axis=1)
cr['structure'] = cr.apply(lambda r: 'Has bridge/tunnel' if has_structure(r) else 'Open barrier (no structure)', axis=1)
keep = [c for c in ['barrier_type', 'structure', 'name', 'bridge', 'tunnel', 'LCP_Length', 'CW_Dist', 'geometry'] if c in cr]
cr[keep].to_file(os.path.join(OUT, 'crossings_44.fgb'), driver='FlatGeobuf', layer='crossings')

# ---- human-pressure envelope ----------------------------------------------
hp = clip(os.path.join(D, 'human/BUFFER_HUMANPRESSURE_250M.gpkg'), 'BUFFER_HUMANPRESSURE_250M')
hp['zone'] = '250 m human-pressure zone'
hp[['zone', 'geometry']].to_file(os.path.join(OUT, 'human_pressure_44.fgb'), driver='FlatGeobuf', layer='human_pressure')

# ---- summary ---------------------------------------------------------------
print('\n=== 4.4 Barriers — km in box ===')
for k, v in bar.groupby('barrier_type')['km'].sum().sort_values(ascending=False).items():
    print(f'  {k:26} {v:>6,.0f} km')
print(f'\n=== Crossing catalogue: {len(cr)} points ===')
print(cr.groupby(['barrier_type', 'structure']).size().to_string())
print(f'\nHuman-pressure zone: {hp.geometry.area.sum()/1e6:,.1f} km²')
