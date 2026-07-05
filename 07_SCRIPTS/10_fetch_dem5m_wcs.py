# 10_fetch_dem5m_wcs.py   ⚠ RUN IN QGIS (Plugins ▸ Python Console ▸ open ▸ Run).
# Fetches the Aragón 5 m DEM (WCS) for the study box, saves a clipped GeoTIFF, and
# derives hillshade + slope. This DEM is the MASTER INPUT for 4.1 ridges, 4.3 flow/
# erosion, 5.1c sections and 5.2 resistance. Send `dem_5m_box.tif` back to Claude.
#
# (Supersedes the "04_dem5m_wcs_clip_classify.py" name in the data-handoff README —
#  04 is taken by 04_build_canadas_4x.py. Same job, clean number.)
#
# NOTE: not testable headlessly by Claude — if the WCS COVERAGE id or size limit bites,
# see the fallbacks at the bottom.
import os
from qgis.core import QgsRasterLayer
import processing

# --- config -----------------------------------------------------------------
# Known repo locations, one per machine. Add yours here if it differs.
BASES = [
    r"C:\Users\Sonya\Desktop\Work_Vault\_Github\New folder\landscape-2025\LANDSCAPE_for_Carlton",  # Sonya (Windows)
    "/Users/carltonfuturity/Developer/Github/landscape-2025/LANDSCAPE_for_Carlton",                # Carlton (Mac)
]
BOX  = (714913, 4582331, 784950, 4639785)          # minx,miny,maxx,maxy  EPSG:25830
WCS_URL  = "https://icearagon.aragon.es/arcgis/services/AragonReferencia/mde/MapServer/WCSServer"
COVERAGE = "1"    # MDE 5 m 25830. If invalid, open GetCapabilities (URL printed below) and use the right identifier.

# --- preflight: locate the repo folder (saved project → BASES). No picker, no SystemExit.
def resolve_base(sentinel="07_SCRIPTS"):
    from qgis.core import QgsProject
    cands = []
    proj = QgsProject.instance().fileName()
    if proj:
        d = os.path.dirname(proj)
        cands += [d, os.path.join(d, "LANDSCAPE_for_Carlton"),
                  os.path.join(os.path.dirname(d), "LANDSCAPE_for_Carlton")]
    cands += BASES
    for b in cands:
        if b and os.path.isdir(os.path.join(b, sentinel)):
            return b
    raise Exception("Couldn't locate LANDSCAPE_for_Carlton. Add this machine's path to "
                    "BASES at the top of the script, or save your .qgz inside the repo. "
                    "Looked in: %s" % [c for c in cands if c])

BASE = resolve_base()
OUT  = os.path.join(BASE, "01_DATA", "DEM")
os.makedirs(OUT, exist_ok=True)
print("→ writing DEM outputs to:", OUT)

# --- 1. connect the WCS coverage -------------------------------------------
uri = f"dpiMode=7&identifier={COVERAGE}&crs=EPSG:25830&format=GeoTIFF&url={WCS_URL}"
dem = QgsRasterLayer(uri, "Aragon DEM 5m (WCS)", "wcs")
if not dem.isValid():
    raise Exception(
        "WCS DEM failed to load. Check the COVERAGE identifier in GetCapabilities:\n"
        f"{WCS_URL}?request=GetCapabilities&service=WCS&version=1.0.0")

# --- 2. write the box to a real GeoTIFF via the QGIS WCS writer --------------
# (Do NOT feed the WCS layer to a gdal: algorithm — GDAL can't read the WCS provider,
#  which silently produced no file. QgsRasterFileWriter uses the WCS provider itself and
#  fetches in tiles, respecting the server's per-request size cap.)
from qgis.core import (QgsRasterFileWriter, QgsRasterPipe, QgsRectangle,
                       QgsCoordinateReferenceSystem)
# metres/pixel. 25 m = fast, territorial-grade (fine for 4.3 flow/erosion + §5; ~6 M px).
# The 5 m source over the whole box is ~161 M px (~600 MB) and FREEZES interactive QGIS,
# so we pull territorial here and grab 2 m only for the small §7/§8 tiles later.
RES = float(os.environ.get('RES', '25'))
dem_tif = os.path.join(OUT, "dem_box.tif")
extent  = QgsRectangle(BOX[0], BOX[1], BOX[2], BOX[3])
cols = int(round((BOX[2] - BOX[0]) / RES))
rows = int(round((BOX[3] - BOX[1]) / RES))

pipe = QgsRasterPipe()
if not pipe.set(dem.dataProvider().clone()):
    raise Exception("Could not build a raster pipe from the WCS provider.")
writer = QgsRasterFileWriter(dem_tif)
writer.setOutputFormat("GTiff")
err = writer.writeRaster(pipe, cols, rows, extent, QgsCoordinateReferenceSystem("EPSG:25830"))
if err != 0 or not os.path.exists(dem_tif):
    raise Exception(
        f"WCS write failed (code {err}). The server likely caps request size — set RES=10 "
        f"at the top and re-run, or fall back to CNIG MDT05 tiles (zone HU30). "
        f"GetCapabilities: {WCS_URL}?request=GetCapabilities&service=WCS&version=1.0.0")
print(f"✓ saved DEM: {dem_tif}  ({cols}x{rows} @ {RES:.0f} m)")

# --- 3. hillshade + slope (now the tif is a real GDAL file) ------------------
try:
    processing.run("gdal:hillshade", {'INPUT': dem_tif, 'BAND': 1, 'Z_FACTOR': 1,
        'OUTPUT': os.path.join(OUT, "hillshade.tif")})
    processing.run("gdal:slope", {'INPUT': dem_tif, 'BAND': 1,
        'OUTPUT': os.path.join(OUT, "slope_deg.tif")})
    print("✓ hillshade + slope written to", OUT)
except Exception as e:
    print("hillshade/slope step skipped:", e, "— the DEM itself is fine.")

print("\nNEXT: `dem_box.tif` is in 01_DATA/DEM — tell Claude → unlocks 4.3 flow/erosion + §5.")
# --- FALLBACKS if the WCS refuses the full box (size limit) ------------------
# a) Lower to a coarser request first to confirm connectivity, or
# b) Use CNIG MDT05 tiles filtered to zone HU30 (UTM 30N) over the box → merge in QGIS,
#    then re-run steps 2–3 on the merged raster.
