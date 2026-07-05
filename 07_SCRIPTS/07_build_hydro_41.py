#!/usr/bin/env python3
# 07_build_hydro_41.py
# Build the 4.1 Hydrography layer set from the CHE/Aragón water exports.
# Box-clips, reprojects (already 25830), unifies into 3 processed layers with a
# hydro_class field, and EXTRACTS the Barranco de Valcuerna as its own class (the
# ecological spine, §6). Authoritative CHE layers used for drainage/canals; OSM used
# only for the main rivers/streams (avoids duplicating CHE canals).
#
# Run: python3 07_build_hydro_41.py
# Outputs (03_PROCESSED/, EPSG:25830):
#   hydro_lines_41.fgb   (lines:   Main river / Natural drainage / Valcuerna / Acequias)
#   hydro_water_41.fgb   (polys:   Lagoon-salada / Reservoir / Main canal)
#   hydro_springs_41.fgb (points:  Spring)
import os, warnings
import geopandas as gpd, pandas as pd
from shapely.geometry import box as shp_box
warnings.filterwarnings('ignore')

SRC = os.environ.get('SRC', '.')      # the hydro/ folder
OUT = os.environ.get('OUT', '.')      # where to write the .fgb
BOX = (714913, 4582331, 784950, 4639785)
BOXG = shp_box(*BOX)

def load(fname, layer):
    g = gpd.read_file(os.path.join(SRC, fname), layer=layer, bbox=BOX)
    if len(g):
        g = gpd.clip(g, BOXG).to_crs(25830)
        g = g[~g.geometry.is_empty & g.geometry.notna()]
        try: g['geometry'] = g.geometry.force_2d()
        except Exception: pass
    return g

def keep(g, cls, name_field):
    g = g.copy()
    g['hydro_class'] = cls
    g['nombre'] = g[name_field] if name_field in g else None
    return g[['hydro_class', 'nombre', 'geometry']]

# ---- LINES -----------------------------------------------------------------
water = load('ARAGON WATER SHP.gpkg', 'ARAGON WATER SHP')
rivers = keep(water[water.fclass.isin(['river', 'stream'])], 'Main river', 'name')

nat = load('Minor Natural Drainage (seasonal) Linear drainage.gpkg',
           'Minor Natural Drainage (seasonal) Linear drainage')
is_valc = nat['nombre'].astype(str).str.contains('valcuerna', case=False, na=False)
valcuerna = keep(nat[is_valc], 'Barranco de Valcuerna (spine)', 'nombre')
natdrain  = keep(nat[~is_valc], 'Natural drainage (seasonal)', 'nombre')

acequias = keep(load('Minor artificial drainage.gpkg', 'Minor artificial drainage'),
                'Artificial drainage (acequias)', 'nombre')

lines = gpd.GeoDataFrame(pd.concat([rivers, natdrain, valcuerna, acequias], ignore_index=True), crs=25830)
lines.to_file(os.path.join(OUT, 'hydro_lines_41.fgb'), driver='FlatGeobuf', layer='hydro_lines')

# ---- WATER BODIES (polygons) ----------------------------------------------
lag = keep(load('Natural or semi-natural lagoons.gpkg', 'Natural or semi-natural lagoons'),
           'Lagoon / salada', 'nombre')
res = keep(load('Reservoirs.gpkg', 'Reservoirs'), 'Reservoir', 'nombre')
can = keep(load('Main artificial channels.gpkg', 'Main artificial channels'), 'Main canal', 'nombre')
water_b = gpd.GeoDataFrame(pd.concat([lag, res, can], ignore_index=True), crs=25830)
water_b.to_file(os.path.join(OUT, 'hydro_water_41.fgb'), driver='FlatGeobuf', layer='hydro_water')

# ---- SPRINGS (points) ------------------------------------------------------
spr = keep(load('Springs _ water emergence.gpkg', 'Springs _ water emergence'), 'Spring', 'nombre')
spr.to_file(os.path.join(OUT, 'hydro_springs_41.fgb'), driver='FlatGeobuf', layer='hydro_springs')

# ---- summary ---------------------------------------------------------------
print('\n=== 4.1 Hydrography — in-box ===')
print('LINES:'); print(lines.groupby('hydro_class').size().to_string())
print('WATER BODIES:'); print(water_b.groupby('hydro_class').size().to_string())
print('SPRINGS:', len(spr))
vlen = lines[lines.hydro_class.str.startswith('Barranco')].geometry.length.sum() / 1000
print(f'Valcuerna spine length in box: {vlen:,.1f} km')
