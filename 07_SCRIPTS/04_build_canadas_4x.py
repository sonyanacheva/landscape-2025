#!/usr/bin/env python3
# 04_build_canadas_4x.py
# Build the 4.x Cañadas / vías pecuarias layer from the national RGVP shapefile.
# Clips to the study box (real in-box length, not whole lines), classifies
# cd_tipo_vp -> tipo + legal max width (Ley 3/1995), recomputes km on the CLIPPED
# geometry, and computes the implementable public-corridor area (length x legal width)
# -- the "no-expropriation" stakeholder number. Writes FlatGeobuf (mount-safe).
#
# Run: python3 04_build_canadas_4x.py
# Output: 03_PROCESSED/canadas_4x.fgb (layer 'canadas', EPSG:25830, lines)
import os, warnings
import geopandas as gpd, pyogrio
from shapely.geometry import box as shp_box
warnings.filterwarnings('ignore')

RGVP = os.environ.get('RGVP', '/tmp/rgvp/RGVP_BDN_2024.shp')
OUT  = os.environ.get('OUT', 'canadas_4x.fgb')
BOX  = (714913, 4582331, 784950, 4639785)   # clip box (AOS + 2 km), EPSG:25830

# cd_tipo_vp -> (tipo label, legal max width m per Ley 3/1995). Colada width is set by
# its classification act (variable) -> None. OV = "REVISAR" placeholders -> to-review.
TIPO = {
    'CA':  ('Cañada',           75.0),
    'COR': ('Cordel',           37.5),
    'VE':  ('Vereda',           20.0),
    'CO':  ('Colada (variable)', None),
    'OV':  ('Sin clasificar / revisar', None),
}

g = pyogrio.read_dataframe(RGVP, bbox=BOX)   # already EPSG:25830
g = g.to_crs(25830)
clip = gpd.clip(g, shp_box(*BOX))            # real length inside the study frame
clip = clip[~clip.geometry.is_empty & clip.geometry.notna()]

clip['tipo']    = clip['cd_tipo_vp'].map(lambda c: TIPO.get(c, ('Otra', None))[0])
clip['ancho_m'] = clip['cd_tipo_vp'].map(lambda c: TIPO.get(c, ('Otra', None))[1])
clip['km']      = clip.geometry.length / 1000.0
# implementable public corridor area (ha) where a legal width exists
clip['area_ha'] = clip.apply(
    lambda r: (r.geometry.length * r.ancho_m / 10000.0) if r.ancho_m else None, axis=1)

cols = ['id_cod_vp', 'nb_via', 'cd_tipo_vp', 'tipo', 'ancho_m', 'km', 'area_ha', 'geometry']
clip[cols].to_file(OUT, driver='FlatGeobuf', layer='canadas')

# --- summary ---------------------------------------------------------------
order = ['Cañada', 'Cordel', 'Vereda', 'Colada (variable)', 'Sin clasificar / revisar']
s = clip.groupby('tipo').agg(n=('km', 'size'), km=('km', 'sum'), area_ha=('area_ha', 'sum'))
print('\n=== 4.x Cañadas — in-box summary (clipped) ===')
print(f"{'tipo':28} {'legal w':>8} {'n':>4} {'km':>8} {'ha(public)':>11}")
for t in order:
    if t in s.index:
        w = {'Cañada':'≤75 m','Cordel':'≤37.5 m','Vereda':'≤20 m'}.get(t, 'var')
        r = s.loc[t]
        ha = f"{r.area_ha:,.0f}" if r.area_ha == r.area_ha else '—'
        print(f"{t:28} {w:>8} {int(r.n):>4} {r.km:>8,.1f} {ha:>11}")
tot_km = s.km.sum(); tot_ha = s.area_ha.sum()
print(f"{'TOTAL':28} {'':>8} {int(s.n.sum()):>4} {tot_km:>8,.1f} {tot_ha:>11,.0f}")
