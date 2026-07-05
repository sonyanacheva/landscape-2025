#!/usr/bin/env python3
# 13_build_flow_erosion_43.py
# Build the 4.3 Flow-accumulation + erosion layers from dem_box.tif (25 m).
# Conditions the DEM (mask 0-fill nodata → fill pits/depressions → resolve flats),
# computes D8 flow direction + accumulation, extracts the drainage network, and an
# erosion-susceptibility index (Stream Power Index, SPI = ln(A · tanβ)).
# NOTE: eastern ~8 km of the box (Catalonia) is outside the Aragón DEM → masked nodata.
# Run headless. Outputs to 03_PROCESSED/.
import os, warnings
import numpy as np, rasterio, geopandas as gpd
from shapely.geometry import shape
from pysheds.grid import Grid
from pysheds.view import Raster
warnings.filterwarnings('ignore')

DEM = os.environ['DEM']
OUT = os.environ.get('OUT', '.')
STREAM_CELLS = int(os.environ.get('STREAM_CELLS', '400'))   # min contributing cells (400 = 25 ha) for a channel
CELL = 25.0

# --- 1. condition DEM: 0-fill → nodata -------------------------------------
src = rasterio.open(DEM); arr = src.read(1).astype('float32')
arr[arr == 0] = np.nan
prof = src.profile; prof.update(dtype='float32', nodata=-9999.0)
clean = os.path.join(OUT, '_dem_clean.tif')
tmp = arr.copy(); tmp[np.isnan(tmp)] = -9999.0
with rasterio.open(clean, 'w', **prof) as d: d.write(tmp, 1)

# --- 2. hydrological conditioning + flow -----------------------------------
grid = Grid.from_raster(clean)
dem = grid.read_raster(clean)
flooded = grid.fill_depressions(grid.fill_pits(dem))
inflated = grid.resolve_flats(flooded)
fdir = grid.flowdir(inflated)
acc = grid.accumulation(fdir)                       # cells

# --- 3. slope + Stream Power Index (erosion susceptibility) ----------------
z = np.asarray(inflated, dtype='float32'); z[np.asarray(dem) == dem.nodata] = np.nan
gy, gx = np.gradient(z, CELL)
slope = np.arctan(np.sqrt(gx**2 + gy**2))           # radians
area = (np.asarray(acc, dtype='float32') + 1) * CELL * CELL      # m² contributing
spi = np.log(area * np.tan(slope) + 1e-6)
spi[np.isnan(z)] = np.nan

# --- 4. write rasters (flow accumulation log + erosion SPI) -----------------
def wr(name, data):
    p = prof.copy(); p.update(dtype='float32', nodata=-9999.0)
    d = np.where(np.isnan(data), -9999.0, data).astype('float32')
    with rasterio.open(os.path.join(OUT, name), 'w', **p) as o: o.write(d, 1)
wr('flowacc_43.tif', np.log10(np.asarray(acc, dtype='float32') + 1))
wr('erosion_spi_43.tif', spi)

# --- 5. drainage network → vector ------------------------------------------
mask = Raster((np.asarray(acc) > STREAM_CELLS), acc.viewfinder)
net = grid.extract_river_network(fdir, mask)
geoms = [shape(f['geometry']) for f in net['features']]
gdf = gpd.GeoDataFrame(geometry=geoms, crs='EPSG:25830')

# magnitude per segment = max flow-accumulation (cells) sampled along the line → width tier
accA = np.asarray(acc); T = prof['transform']; H, W = accA.shape
def seg_mag(geom):
    m = 0
    for x, y in geom.coords:
        c = int((x - T.c) / T.a); r = int((y - T.f) / T.e)
        if 0 <= r < H and 0 <= c < W:
            m = max(m, accA[r, c])
    return int(m)
gdf['acc_cells'] = [seg_mag(g) for g in gdf.geometry]
gdf['ha_upstream'] = gdf['acc_cells'] * CELL * CELL / 1e4
def tier(a):
    if a >= 8000:  return 'Main barranco'          # ≥ 500 ha upstream
    if a >= 2000:  return 'Secondary channel'      # ≥ 125 ha
    return 'Minor drainage'
gdf['clase'] = gdf['ha_upstream'].map(tier)
gdf['km'] = gdf.geometry.length / 1000.0
gdf.to_file(os.path.join(OUT, 'streams_43.fgb'), driver='FlatGeobuf', layer='streams')
os.remove(clean)

print(f"4.3 built. Drainage network: {len(gdf)} segments, {gdf.km.sum():,.0f} km "
      f"(threshold {STREAM_CELLS} cells = {STREAM_CELLS*CELL*CELL/1e4:.0f} ha).")
print(gdf.groupby('clase')['km'].sum().to_string())
print("Rasters: flowacc_43.tif (log flow accumulation), erosion_spi_43.tif (stream power index).")
