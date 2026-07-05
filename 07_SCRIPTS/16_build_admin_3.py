#!/usr/bin/env python3
# 16_build_admin_3.py
# Build the §3 administrative layers from the IDEAragón exports (already EPSG:25830):
#   - municipios truly intersecting the study box (with names) → 3.3 work-area frame + labels
#   - province boundaries (Aragón provinces flagged) → 3.2 regional map
#   - comunidad boundaries (Aragón flagged) → 3.1/3.2 context
# Run headless. Outputs to 03_PROCESSED/.
import os, warnings
import geopandas as gpd
from shapely.geometry import box as shp_box
warnings.filterwarnings('ignore')

SRC = os.environ['SRC']     # the IDEAragon folder
OUT = os.environ.get('OUT', '.')
BOX = shp_box(714913, 4582331, 784950, 4639785)

# municipios in the work area (true intersection, whole units) with a clean name field.
# NOTE: the IDEAragón WFS export duplicated every feature ~7× → dedupe by INE code first.
muni = gpd.read_file(os.path.join(SRC, 'municipios.gpkg')).drop_duplicates(subset='c_muni_ine')
muni = muni[muni.intersects(BOX)].copy()
muni['nombre'] = muni['d_muni_ine']; muni['ine'] = muni['c_muni_ine']
muni['comarca'] = muni['d_comarca']
muni[['ine', 'nombre', 'comarca', 'provincia', 'geometry']].to_file(
    os.path.join(OUT, 'municipios_box_33.fgb'), driver='FlatGeobuf', layer='municipios')

# provinces (whole layer) — flag the ones the box spans (dedupe WFS duplicates)
prov = gpd.read_file(os.path.join(SRC, 'provincias.gpkg')).drop_duplicates(subset='c_prov')
STUDY_PROV = {'Huesca', 'Zaragoza', 'Lleida', 'Lérida'}
prov['study'] = prov['provincia'].isin(STUDY_PROV)
prov[['provincia', 'study', 'geometry']].to_file(
    os.path.join(OUT, 'provinces_3.fgb'), driver='FlatGeobuf', layer='provinces')

# comunidades (whole) — flag Aragón (dedupe WFS duplicates)
com = gpd.read_file(os.path.join(SRC, 'comunidades.gpkg'))
namecol = 'comunidad' if 'comunidad' in com.columns else com.columns[1]
com = com.drop_duplicates(subset=namecol)
com['aragon'] = com[namecol].astype(str).str.contains('arag', case=False, na=False)
com[[namecol, 'aragon', 'geometry']].rename(columns={namecol: 'comunidad'}).to_file(
    os.path.join(OUT, 'comunidades_3.fgb'), driver='FlatGeobuf', layer='comunidades')

print(f"§3 admin built:")
print(f"  municipios in box: {len(muni)}  → {sorted(muni.nombre.dropna().unique())[:8]} …")
print(f"  provinces flagged study: {prov.study.sum()} of {len(prov)}")
print(f"  comunidades (Aragón flagged): {com.aragon.sum()} of {len(com)}")
