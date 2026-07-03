# 01_fetch_osm.py
# Run in QGIS: Plugins > Python Console > Show Editor > open this file > Run (green arrow).
# Fetches roads, railways, canals, tourism, historic for the study box from Overpass,
# saves clean GeoPackages into 01_DATA/infrastructure_osm/ and loads them.
# (Reprojection/clip to the box I handle later, headless.)

import os, urllib.request, urllib.parse
from qgis.core import (QgsVectorLayer, QgsVectorFileWriter, QgsProject)

OUT  = r"C:\Users\Sonya\Desktop\Work_Vault\1_University\4th Year\2_LANDSCAPE\LANDSCAPE\01_DATA\infrastructure_osm"
BBOX = "41.36,-0.41,41.86,0.41"   # S,W,N,E in EPSG:4326 = your study box
os.makedirs(OUT, exist_ok=True)

query = f"""
[out:xml][timeout:240];
(
  way["highway"]({BBOX});
  way["railway"]({BBOX});
  way["waterway"="canal"]({BBOX});
  way["waterway"="ditch"]({BBOX});
  nwr["tourism"]({BBOX});
  nwr["historic"]({BBOX});
);
(._;>;);
out body;
"""

osm_path = os.path.join(OUT, "osm_box.osm")
print("Downloading from Overpass (can take up to a few minutes)...")
data = urllib.parse.urlencode({"data": query}).encode()
req  = urllib.request.Request("https://overpass-api.de/api/interpreter", data=data)
with urllib.request.urlopen(req, timeout=600) as r:
    open(osm_path, "wb").write(r.read())
print("Saved raw:", osm_path)

def export(sublayer, out_name):
    lyr = QgsVectorLayer(f"{osm_path}|layername={sublayer}", out_name, "ogr")
    if not lyr.isValid() or lyr.featureCount() == 0:
        print("  skip (empty):", sublayer); return
    dest = os.path.join(OUT, out_name + ".gpkg")
    opts = QgsVectorFileWriter.SaveVectorOptions(); opts.driverName = "GPKG"
    try:
        QgsVectorFileWriter.writeAsVectorFormatV3(lyr, dest, QgsProject.instance().transformContext(), opts)
    except Exception:
        QgsVectorFileWriter.writeAsVectorFormat(lyr, dest, "UTF-8", lyr.crs(), "GPKG")
    QgsProject.instance().addMapLayer(QgsVectorLayer(dest, out_name, "ogr"))
    print("  wrote:", dest, "|", lyr.featureCount(), "features")

# GDAL OSM driver exposes these sublayers:
export("lines",         "osm_lines")     # roads, railways, canals (fields: highway, railway, waterway, bridge, tunnel...)
export("points",        "osm_points")    # tourism / historic nodes
export("multipolygons", "osm_polygons")  # areas (some tourism/historic)
print("Done. Files in", OUT)
