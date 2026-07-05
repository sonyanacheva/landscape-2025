#!/usr/bin/env python3
# 21_build_viewpoints_51b.py
# Build the 5.1b lynx-path storyboard viewpoints: sample points along the least-cost
# corridor and classify each by what the lynx encounters there — ecotone, ravine /
# watercourse crossing, barrier crossing, habitat discontinuity, or protected core —
# with the intervention opportunity noted. Output: numbered viewpoint layer + CSV table.
import os, warnings
import numpy as np, rasterio, geopandas as gpd
from shapely.geometry import Point
warnings.filterwarnings('ignore')

LCP=os.environ['LCP']; HAB=os.environ['HAB']; BARR=os.environ['BARR']
HYD=os.environ['HYD']; NAT=os.environ['NAT']; OUT=os.environ.get('OUT','.')
STEP=float(os.environ.get('STEP','6000'))   # sample every 6 km along the path

lcp=gpd.read_file(LCP).to_crs(25830); line=lcp.geometry.iloc[0]
barr=gpd.read_file(BARR).to_crs(25830)
hyd=gpd.read_file(HYD).to_crs(25830)
valc=hyd[hyd.hydro_class.str.startswith('Barranco')] if 'hydro_class' in hyd else hyd.iloc[0:0]
nat=gpd.read_file(NAT).to_crs(25830)
hr=rasterio.open(HAB); ha=hr.read(1); HT=hr.transform
HABNAME={1:'ecotone',2:'riparian',3:'lynx cover',4:'rabbit foraging',5:'wetland',6:'permeable matrix',7:'hostile matrix',8:'non-habitat'}

def hab_at(p):
    r=int((p.y-HT.f)/HT.e); c=int((p.x-HT.c)/HT.a)
    return HABNAME.get(int(ha[r,c]),'?') if 0<=r<ha.shape[0] and 0<=c<ha.shape[1] else '?'

pts=[]
n=int(line.length//STEP)+1
for i in range(n+1):
    p=line.interpolate(min(i*STEP, line.length))
    d_barr=barr.distance(p).min(); d_valc=valc.distance(p).min() if len(valc) else 9e9
    d_river=hyd[hyd.hydro_class=='Main river'].distance(p).min() if 'hydro_class' in hyd else 9e9
    in_core=nat.contains(p).any(); habt=hab_at(p)
    # classify
    if d_barr<300:
        bt=barr.iloc[barr.distance(p).values.argmin()]['barrier_type']
        cls='Barrier crossing'; feat=bt; opp='Wildlife crossing / underpass'
    elif d_valc<250:
        cls='Ravine crossing (Valcuerna)'; feat='Barranco de Valcuerna'; opp='Xeroriparian planting; check dams'
    elif d_river<300:
        cls='River crossing'; feat='Main river'; opp='Riparian stepping-stone; bank cover'
    elif in_core:
        cls='Protected core'; feat='Natura 2000 site'; opp='Source population; protect'
    elif habt in ('permeable matrix','hostile matrix','non-habitat'):
        cls='Habitat discontinuity'; feat=f'{habt}'; opp='Hedgerow; un-ploughed field corners; SWF'
    elif habt in ('ecotone','riparian','lynx cover'):
        cls='Ecotone / cover'; feat=f'{habt}'; opp='Reinforce cover; connect patches'
    else:
        cls='Transit'; feat=habt; opp='—'
    pts.append({'view':len(pts)+1,'km':round(line.project(p)/1000,1),'clase':cls,'feature':feat,
                'habitat':habt,'opportunity':opp,'geometry':p})

gdf=gpd.GeoDataFrame(pts, crs=25830)
gdf.to_file(os.path.join(OUT,'viewpoints_51b.fgb'), driver='FlatGeobuf', layer='viewpoints')
gdf.drop(columns='geometry').to_csv(os.path.join(OUT.replace('03_PROCESSED','00_ADMIN'),'viewpoints_51b.csv') if '03_PROCESSED' in OUT else os.path.join(OUT,'viewpoints_51b.csv'), index=False)
print(f"5.1b: {len(gdf)} viewpoints along {line.length/1000:.0f} km corridor")
for _,r in gdf.iterrows(): print(f"  V{r['view']:>2} @ {r['km']:>4} km  {r['clase']:28} {r['feature']}")
