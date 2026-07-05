#!/usr/bin/env python3
# 15_build_resistance_corridor_52.py
# Build the 5.2 resistance surface + least-cost corridor. Resistance = land-cover base
# (rebuilt on SIGPAC 4.5, replacing old CORINE) × slope factor + barrier penalty. Rabbit
# conditional permeability is embodied in the low ecotone/pasture values (matrix cells with
# rabbits cost less to cross). Least-cost path + corridor swath connect two protected cores
# (Sierra de Alcubierre ↔ Valcuerna/Serreta Negra Natura 2000 sites).
#
# Run headless. Outputs: 03_PROCESSED/resistance_52.tif, corridor_lcp_52.fgb, corridor_swath_52.tif
import os, warnings
import numpy as np, rasterio, geopandas as gpd
from rasterio.features import rasterize
from shapely.geometry import LineString
from skimage.graph import route_through_array, MCP_Geometric
warnings.filterwarnings('ignore')

DEM   = os.environ['DEM']            # dem_box.tif (grid reference)
SLOPE = os.environ['SLOPE']          # slope_deg.tif
AGRI  = os.environ['AGRI']           # agri_matrix_45.fgb
BARR  = os.environ['BARR']           # barriers_44.fgb
NAT   = os.environ['NAT']            # natura2000_box.fgb
OUT   = os.environ.get('OUT', '.')

ref = rasterio.open(DEM); T = ref.transform; H, W = ref.height, ref.width
slope = rasterio.open(SLOPE).read(1).astype('float32'); slope[slope < 0] = 0
valid = ref.read(1) != 0            # eastern Catalonia strip = no DEM

# land-cover resistance (lynx; 1 = optimal cover … 60 = hostile crop)
RES = {'Scrub (matorral)': 1, 'Grazed scrub / pasto arbustivo': 1, 'Forest': 3,
       'Pasture (open)': 8, 'Woody crops': 12, 'Arable dryland': 20,
       'Arable irrigated': 50, 'Horticulture/greenhouse': 60, 'Non-agricultural': 25}
agri = gpd.read_file(AGRI)
base = rasterize(((g, RES.get(c, 25)) for g, c in zip(agri.geometry, agri.agri_class)),
                 out_shape=(H, W), transform=T, fill=25, dtype='float32')

# slope factor (steep costs more, capped) + barrier penalty (near-absolute walls)
sfac = np.clip(1 + slope / 25.0, 1, 3)
BPEN = {'Motorway / autovía': 1000, 'Railway (incl. HS line)': 800,
        'Main road (N / primary)': 200, 'Canal': 150, 'Other major road': 100}
barr = gpd.read_file(BARR); barr['geometry'] = barr.geometry.buffer(25)   # ensure continuous wall
bpen = rasterize(((g, BPEN.get(t, 100)) for g, t in zip(barr.geometry, barr.barrier_type)),
                 out_shape=(H, W), transform=T, fill=0, dtype='float32')

resist = base * sfac + bpen
resist[~valid] = 1e6                 # no-data strip = impassable (for routing)
resist_out = resist.copy(); resist_out[~valid] = -9999   # display copy: strip = nodata
with rasterio.open(os.path.join(OUT, 'resistance_52.tif'), 'w', driver='GTiff',
                   height=H, width=W, count=1, dtype='float32', crs=ref.crs,
                   transform=T, nodata=-9999) as o:
    o.write(resist_out, 1)

# --- endpoints: interior point of two protected cores → nearest valid cell ---
nat = gpd.read_file(NAT).set_index('codigo')
def cell_of(code):
    p = nat.loc[code].geometry.representative_point()
    r = int((p.y - T.f) / T.e); c = int((p.x - T.c) / T.a)
    return max(0, min(H - 1, r)), max(0, min(W - 1, c))
src = cell_of('ES0000295')           # Sierra de Alcubierre (NW core)
dst = cell_of('ES0000182')           # Valcuerna, Serreta Negra y Liberola (central-S core)

# --- least-cost path ---------------------------------------------------------
path, cost = route_through_array(resist, src, dst, fully_connected=True, geometric=True)
pts = [rasterio.transform.xy(T, r, c) for r, c in path]
lcp = gpd.GeoDataFrame({'name': ['LCP: Alcubierre ↔ Valcuerna']},
                       geometry=[LineString(pts)], crs=ref.crs)
lcp['km'] = lcp.geometry.length / 1000.0
lcp.to_file(os.path.join(OUT, 'corridor_lcp_52.fgb'), driver='FlatGeobuf', layer='lcp')

# --- least-cost corridor swath = cost-from-src + cost-from-dst, low band = corridor ---
mcp_s = MCP_Geometric(resist); cs, _ = mcp_s.find_costs([src])
mcp_d = MCP_Geometric(resist); cd, _ = mcp_d.find_costs([dst])
corr = cs + cd
cmin = corr[np.isfinite(corr)].min()
TOL = float(os.environ.get('TOL', '0.02'))       # corridor band = within TOL of least-cost total
swath = np.where(np.isfinite(corr) & (corr <= cmin * (1 + TOL)), corr, -9999).astype('float32')
with rasterio.open(os.path.join(OUT, 'corridor_swath_52.tif'), 'w', driver='GTiff',
                   height=H, width=W, count=1, dtype='float32', crs=ref.crs,
                   transform=T, nodata=-9999) as o:
    o.write(swath, 1)

print(f"5.2 built. LCP length: {lcp.km.iloc[0]:,.1f} km (cost {cost:,.0f}).")
print(f"Resistance range: {resist[valid].min():.0f}–{resist[valid&(resist<1e5)].max():.0f} "
      f"(barriers spike to {int(bpen.max())}).")
print(f"Corridor swath (≤{TOL*100:.0f}% over least-cost): {np.sum(swath>-9999)*625/1e4:,.0f} ha.")
