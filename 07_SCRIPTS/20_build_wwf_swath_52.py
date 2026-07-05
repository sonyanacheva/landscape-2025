#!/usr/bin/env python3
# 20_build_wwf_swath_52.py
# Build a WWF corridor ZONE as a separate swath-like layer: a soft distance gradient that
# fades out from the WWF corridor line (dark on the line → light at the edge), so it reads
# like the model swath but suggests the WWF corridor. Sits BENEATH our precise swath.
# Run headless. Output: 03_PROCESSED/corridor_wwf_swath_52.tif
import os, warnings
import numpy as np, rasterio, geopandas as gpd
from rasterio.features import rasterize
from scipy.ndimage import distance_transform_edt
warnings.filterwarnings('ignore')

REF=os.environ['REF']          # resistance_52.tif (grid reference)
WWF=os.environ['WWF']          # corridor_wwf_52.fgb (WWF corridor line)
OUT=os.environ.get('OUT','corridor_wwf_swath_52.tif')
MAXD=float(os.environ.get('MAXD','1500'))   # zone half-width (m), fade distance
CELL=25.0

ref=rasterio.open(REF); T=ref.transform; H,W=ref.height,ref.width
wwf=gpd.read_file(WWF).to_crs(25830)
line=rasterize(((g,1) for g in wwf.geometry), out_shape=(H,W), transform=T, fill=0, dtype='uint8')
dist=distance_transform_edt(line==0)*CELL            # metres from nearest corridor cell
band=np.where(dist<=MAXD, dist, -9999).astype('float32')   # 0 on line … MAXD at edge

with rasterio.open(OUT,'w',driver='GTiff',height=H,width=W,count=1,dtype='float32',
                   crs=ref.crs,transform=T,nodata=-9999,compress='DEFLATE') as o: o.write(band,1)
print(f"WWF corridor zone: {int((band!=-9999).sum())*625/1e4:,.0f} ha (fade {MAXD:.0f} m)")
