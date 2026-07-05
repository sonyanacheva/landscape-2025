#!/usr/bin/env python3
# 16_build_admin_3.py
# Build the §3 administrative layers. Municipios + provinces come from the NATIONAL
# (INSPIRE) set in context/ — they include the Lleida/Cataluña side of the box, unlike the
# Aragón-only IDEAragón export. Comunidad (Aragón boundary) kept from IDEAragón.
# Run headless. Outputs to 03_PROCESSED/.
import os, warnings
import geopandas as gpd
from shapely.geometry import box as shp_box
warnings.filterwarnings('ignore')

CTX = os.environ['CTX']      # context folder (national municipios/provinces)
IDE = os.environ['IDE']      # IDEAragon folder (comunidad)
OUT = os.environ.get('OUT', '.')
BOX = shp_box(714913, 4582331, 784950, 4639785)

# municipios in the work area (national INSPIRE set → includes Lleida side)
muni = gpd.read_file(os.path.join(CTX, 'municipios.gpkg'))
muni = muni[muni.intersects(BOX)].copy()
muni['nombre'] = muni['NAMEUNIT']; muni['natcode'] = muni['NATCODE']
muni[['natcode', 'nombre', 'geometry']].to_file(
    os.path.join(OUT, 'municipios_box_33.fgb'), driver='FlatGeobuf', layer='municipios')

# provinces (Huesca / Zaragoza / Lleida)
prov = gpd.read_file(os.path.join(CTX, 'provinces.gpkg'))
prov['nombre'] = prov['NAMEUNIT']
prov[['nombre', 'geometry']].to_file(
    os.path.join(OUT, 'provinces_3.fgb'), driver='FlatGeobuf', layer='provinces')

# comunidad — Aragón boundary (IDEAragón polygon)
com = gpd.read_file(os.path.join(IDE, 'comunidades.gpkg'))
namecol = 'comunidad' if 'comunidad' in com.columns else com.columns[1]
com = com.drop_duplicates(subset=namecol)
com[[namecol, 'geometry']].rename(columns={namecol: 'comunidad'}).to_file(
    os.path.join(OUT, 'comunidades_3.fgb'), driver='FlatGeobuf', layer='comunidades')

print("§3 admin (consolidated to national municipios/provinces):")
print(f"  municipios in box: {len(muni)}  provinces: {sorted(prov.nombre.tolist())}")
print(f"  comunidad: {len(com)}")
