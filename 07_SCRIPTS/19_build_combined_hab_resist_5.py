#!/usr/bin/env python3
# 19_build_combined_hab_resist_5.py   (supersedes 14 + 15)
# Rebuild §5 on a COMBINED land-cover base: MFE natural-veg (4.6) where present, else the
# SIGPAC matrix (4.5). Adds MFE Riparian corridor + Wetland/salada as distinct habitat and
# sharpens resistance. Fast raster pipeline: rasterize each base once → numpy lookups.
# Outputs: habitat_51a.tif (categorical) + resistance_52.tif + corridor_lcp_52.fgb + corridor_swath_52.tif
import os, warnings, time
import numpy as np, rasterio, geopandas as gpd
from rasterio.features import rasterize
from shapely.geometry import LineString
from skimage.graph import MCP_Geometric
warnings.filterwarnings('ignore')
t0=time.time(); log=lambda m: print(f"[{time.time()-t0:4.0f}s] {m}", flush=True)

DEM=os.environ['DEM']; SLOPE=os.environ['SLOPE']; AGRI=os.environ['AGRI']
FOREST=os.environ['FOREST']; BARR=os.environ['BARR']; NAT=os.environ['NAT']
OUT=os.environ.get('OUT','.'); CELL=25.0
ref=rasterio.open(DEM); T=ref.transform; H,W=ref.height,ref.width
slope=rasterio.open(SLOPE).read(1).astype('float32'); slope[slope<0]=0
valid=ref.read(1)!=0

HABS=['(nodata)','Lynx + rabbit optimal (ecotone)','Riparian corridor','Lynx cover (scrub/forest)',
 'Rabbit foraging (open)','Wetland / salada','Matrix (permeable)','Matrix (hostile)','Non-habitat']
HC={h:i for i,h in enumerate(HABS)}
MFE_HAB={'Riparian woodland (riberas)':'Riparian corridor','Wetland (humedal)':'Wetland / salada',
 'Forest (natural)':'Lynx cover (scrub/forest)','Forest (plantation)':'Lynx cover (scrub/forest)',
 'Scrub (matorral)':'Lynx cover (scrub/forest)','Grassland–scrub mosaic':'Lynx + rabbit optimal (ecotone)',
 'Grassland (natural)':'Rabbit foraging (open)','Bare / sparse':'Matrix (permeable)'}
SIG_HAB={'Grazed scrub / pasto arbustivo':'Lynx + rabbit optimal (ecotone)','Scrub (matorral)':'Lynx cover (scrub/forest)',
 'Forest':'Lynx cover (scrub/forest)','Pasture (open)':'Rabbit foraging (open)','Arable dryland':'Matrix (permeable)',
 'Woody crops':'Matrix (permeable)','Arable irrigated':'Matrix (hostile)','Horticulture/greenhouse':'Matrix (hostile)',
 'Non-agricultural':'Non-habitat'}
MFE_RES={'Riparian woodland (riberas)':2,'Wetland (humedal)':20,'Forest (natural)':3,'Forest (plantation)':5,
 'Scrub (matorral)':1,'Grassland–scrub mosaic':1,'Grassland (natural)':8,'Bare / sparse':15}
SIG_RES={'Grazed scrub / pasto arbustivo':1,'Scrub (matorral)':1,'Forest':3,'Pasture (open)':8,
 'Arable dryland':20,'Woody crops':12,'Arable irrigated':50,'Horticulture/greenhouse':60,'Non-agricultural':25}

# rasterize each base ONCE to a class-index raster, then numpy-remap
mfe=gpd.read_file(FOREST); sig=gpd.read_file(AGRI); log("read vectors")
mclasses=list(MFE_HAB); midx={c:i+1 for i,c in enumerate(mclasses)}
sclasses=list(SIG_HAB); sidx={c:i+1 for i,c in enumerate(sclasses)}
mr=rasterize(((g,midx[c]) for g,c in zip(mfe.geometry,mfe.clase) if c in midx), out_shape=(H,W), transform=T, fill=0, dtype='uint8')
sr=rasterize(((g,sidx.get(c,0)) for g,c in zip(sig.geometry,sig.agri_class)), out_shape=(H,W), transform=T, fill=0, dtype='uint8')
log("rasterized bases")
# lookup tables (index 0 = absent)
m_hab=np.array([0]+[HC[MFE_HAB[c]] for c in mclasses], 'uint8')
m_res=np.array([0]+[MFE_RES[c] for c in mclasses], 'float32')
s_hab=np.array([HC['Non-habitat']]+[HC[SIG_HAB[c]] for c in sclasses], 'uint8')
s_res=np.array([25.0]+[SIG_RES[c] for c in sclasses], 'float32')
mnat=mr>0
habc=np.where(mnat, m_hab[mr], s_hab[sr]).astype('uint8')
base=np.where(mnat, m_res[mr], s_res[sr]).astype('float32')

# habitat categorical raster (+ .tif.aux categories via a sidecar txt)
with rasterio.open(os.path.join(OUT,'habitat_51a.tif'),'w',driver='GTiff',height=H,width=W,count=1,
                   dtype='uint8',crs=ref.crs,transform=T,nodata=0,compress='DEFLATE') as o: o.write(habc,1)
open(os.path.join(OUT,'habitat_51a.codes.txt'),'w').write("\n".join(f"{i}\t{h}" for i,h in enumerate(HABS)))
log("wrote habitat raster")

# resistance + LCP
sfac=np.clip(1+slope/25.0,1,3)
BPEN={'Motorway / autovía':1000,'Railway (incl. HS line)':800,'Main road (N / primary)':200,'Canal':150,'Other major road':100}
barr=gpd.read_file(BARR); barr['geometry']=barr.geometry.buffer(25)
bpen=rasterize(((g,BPEN.get(t,100)) for g,t in zip(barr.geometry,barr.barrier_type)), out_shape=(H,W), transform=T, fill=0, dtype='float32')
resist=base*sfac+bpen; resist[~valid]=1e6
out=resist.copy(); out[~valid]=-9999
with rasterio.open(os.path.join(OUT,'resistance_52.tif'),'w',driver='GTiff',height=H,width=W,count=1,dtype='float32',crs=ref.crs,transform=T,nodata=-9999,compress='DEFLATE') as o: o.write(out,1)
log("wrote resistance")

nat=gpd.read_file(NAT).set_index('codigo')
def cell(code):
    p=nat.loc[code].geometry.representative_point(); return (max(0,min(H-1,int((p.y-T.f)/T.e))),max(0,min(W-1,int((p.x-T.c)/T.a))))
src,dst=cell('ES0000295'),cell('ES0000182')
mcp_s=MCP_Geometric(resist); cs,_=mcp_s.find_costs([src]); path=mcp_s.traceback(dst); log("LCP traceback")
lcp=gpd.GeoDataFrame({'name':['LCP: Alcubierre ↔ Valcuerna']}, geometry=[LineString([rasterio.transform.xy(T,r,c) for r,c in path])], crs=25830)
lcp['km']=lcp.geometry.length/1000.0
lcp.to_file(os.path.join(OUT,'corridor_lcp_52.fgb'), driver='FlatGeobuf', layer='lcp')
cd,_=MCP_Geometric(resist).find_costs([dst]); corr=cs+cd; cmin=corr[np.isfinite(corr)].min()
sw=np.where(np.isfinite(corr)&(corr<=cmin*1.02),corr,-9999).astype('float32')
with rasterio.open(os.path.join(OUT,'corridor_swath_52.tif'),'w',driver='GTiff',height=H,width=W,count=1,dtype='float32',crs=ref.crs,transform=T,nodata=-9999,compress='DEFLATE') as o: o.write(sw,1)
log("wrote swath + done")

for i,h in enumerate(HABS):
    if i==0: continue
    ha=int((habc==i).sum())*625/1e4
    if ha: print(f"  {h:34} {ha:>10,.0f} ha")
print(f"5.2 LCP {lcp.km.iloc[0]:.0f} km (cost {cs[dst]:,.0f}); swath {np.sum(sw>-9999)*625/1e4:,.0f} ha")
