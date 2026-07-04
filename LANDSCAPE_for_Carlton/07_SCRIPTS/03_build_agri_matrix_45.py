#!/usr/bin/env python3
# 03_build_agri_matrix_45.py
# Headless build of the 4.5 Agricultural Matrix layer from raw SIGPAC recintos.
# Reads the 51 box municipios, filters to the study box, reprojects 4258 -> 25830,
# reclassifies uso_sigpac -> agri_class (data-rich: PR kept as its own ecotone class),
# carries authoritative SIGPAC area as `ha`, writes FlatGeobuf (mount-safe).
#
# Run: python3 03_build_agri_matrix_45.py
# Output: 03_PROCESSED/agri_matrix_45.fgb  (layer 'agri', EPSG:25830)
import glob, os, warnings
import pandas as pd, geopandas as gpd, pyogrio
from pyproj import Transformer
warnings.filterwarnings('ignore')

SIGPAC_DIR = os.environ.get('SIGPAC_DIR', '.')
OUT = os.environ.get('OUT', 'agri_matrix_45.fgb')
BOX_25830 = (714913, 4582331, 784950, 4639785)   # clip box (AOS + 2 km)

# --- reclass: SIGPAC uso_sigpac -> agri_class -------------------------------
WOODY = {'FY','FS','OV','VI','FL','CF','CS','OF','OP','VO','VF','FF','FV','OC','CV','CI'}
HORT  = {'TH','IV'}
NONAG = {'AG','CA','IM','ZU','ED','ZC','ZV'}
def reclass(uso, coef):
    if uso == 'TA':  return 'Arable irrigated' if (coef or 0) > 0 else 'Arable dryland'
    if uso == 'PR':  return 'Grazed scrub / pasto arbustivo'   # ecotone, kept distinct
    if uso == 'MT':  return 'Scrub (matorral)'
    if uso in ('PA','PS'): return 'Pasture (open)'
    if uso == 'FO':  return 'Forest'
    if uso in WOODY: return 'Woody crops'
    if uso in HORT:  return 'Horticulture/greenhouse'
    if uso in NONAG: return 'Non-agricultural'
    return 'Non-agricultural'

# --- read + filter + reproject ----------------------------------------------
t = Transformer.from_crs(25830, 4258, always_xy=True)
minx, miny = t.transform(BOX_25830[0], BOX_25830[1])
maxx, maxy = t.transform(BOX_25830[2], BOX_25830[3])
bbox4258 = (minx, miny, maxx, maxy)

parts = []
files = sorted(glob.glob(os.path.join(SIGPAC_DIR, '*_rec_2026_*.gpkg')))
for i, f in enumerate(files, 1):
    g = pyogrio.read_dataframe(f, layer='recinto',
        columns=['uso_sigpac','dn_surface','coef_regadio'], bbox=bbox4258)
    if len(g):
        parts.append(g)
    print(f'[{i}/{len(files)}] {os.path.basename(f)}: {len(g)} parcels in box', flush=True)

gdf = gpd.GeoDataFrame(pd.concat(parts, ignore_index=True), crs='EPSG:4258')
gdf = gdf.to_crs(25830)
gdf['agri_class'] = [reclass(u, c) for u, c in zip(gdf.uso_sigpac, gdf.coef_regadio)]
gdf['ha'] = gdf['dn_surface'] / 10000.0        # authoritative SIGPAC area

# --- write FlatGeobuf (mount-safe; .gpkg corrupts on synced mount) ----------
gdf[['uso_sigpac','coef_regadio','agri_class','ha','geometry']].to_file(
    OUT, driver='FlatGeobuf', layer='agri')

# --- legend summary ---------------------------------------------------------
leg = gdf.groupby('agri_class')['ha'].sum().sort_values(ascending=False)
print('\n=== 4.5 legend (ha) ===')
for k, v in leg.items():
    print(f'{k:34} {v:>12,.0f} ha')
print(f'{"TOTAL":34} {leg.sum():>12,.0f} ha   parcels: {len(gdf):,}')
