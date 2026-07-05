# 11_export_vault_layers.py   ⚠ RUN IN QGIS with the OLD VAULT project (QGIS_007.qgz) OPEN.
# Exports the §3 context bundle from the loaded vault to 01_DATA/context/ as GeoPackage,
# reprojected to EPSG:25830. Claude clips to the box as each §3 map needs it, so this just
# exports FULL layers (corridors + CCAA stay national for the 3.1 Spain map). Fuzzy-matches
# layer names — check the MISSING list at the end and adjust the substrings if needed.
#
# (Supersedes the "05_export_vault_layers.py" name in the data-handoff README —
#  05 is taken by 05_build_forest_46.py. Same job, clean number.)
import os
from qgis.core import (QgsProject, QgsVectorFileWriter, QgsCoordinateReferenceSystem,
                       QgsCoordinateTransform)

# --- config -----------------------------------------------------------------
# Known repo locations, one per machine. Add yours here if it differs.
BASES = [
    r"C:\Users\Sonya\Desktop\Work_Vault\_Github\New folder\landscape-2025\LANDSCAPE_for_Carlton",  # Sonya (Windows)
    "/Users/carltonfuturity/Developer/Github/landscape-2025/LANDSCAPE_for_Carlton",                # Carlton (Mac)
]

# --- preflight: locate the repo folder + confirm the vault is open. No picker, no SystemExit.
def resolve_base(sentinel="07_SCRIPTS"):
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
                    "BASES at the top of the script, or save your .qgz inside the repo.")

BASE = resolve_base()
OUT  = os.path.join(BASE, "01_DATA", "context")
os.makedirs(OUT, exist_ok=True)
if len(QgsProject.instance().mapLayers()) == 0:
    raise SystemExit("✗ No layers loaded. Open the OLD VAULT project (QGIS_007.qgz) first, then re-run.")
print("→ exporting context layers to:", OUT)

# output filename -> substrings that identify the loaded vault layer (first match wins).
WANT = {
    "corredores_prioritarios":  ["corredores_prioritarios", "corredor"],
    "zonas_criticas":           ["zonas_criticas_def", "zonas_critic", "critical"],
    "natura2000":               ["natura2000 site", "natura2000", "natura 2000"],
    "espacios_h1":              ["espacios_h1", "espacio h1", "h1"],
    "espacios_h2":              ["espacios_h2", "espacio h2", "h2"],
    "espacios_h3":              ["espacios_h3", "espacio h3", "h3"],
    "provinces":                ["provinces", "provincias", "provinc"],
    "municipios":               ["clipped_municipalities", "municipal", "municip"],
    "autonomous_communities":   ["clipped_autonomous", "autonomous", "comunidad"],
    "poi":                      ["poi"],
    "grid_1km":                 ["grid 1km", "grid_1km", "1km", "grid"],
}
DST = QgsCoordinateReferenceSystem("EPSG:25830")
project = QgsProject.instance()
layers = list(project.mapLayers().values())

def find(subs):
    # match loaded VECTOR layers by name substring (first substring, first layer wins)
    for s in subs:
        for lyr in layers:
            if hasattr(lyr, "geometryType") and s in lyr.name().lower():
                return lyr
    return None

done, missing = [], []
for out, subs in WANT.items():
    lyr = find([s.lower() for s in subs])
    if not lyr:
        missing.append(out); print("MISSING:", out, "(tried:", subs, ")"); continue
    dest = os.path.join(OUT, out + ".gpkg")
    opts = QgsVectorFileWriter.SaveVectorOptions()
    opts.driverName = "GPKG"
    opts.layerName = out
    if lyr.crs() != DST:
        opts.ct = QgsCoordinateTransform(lyr.crs(), DST, project)
    res = QgsVectorFileWriter.writeAsVectorFormatV3(lyr, dest, project.transformContext(), opts)
    ok = (res[0] == QgsVectorFileWriter.NoError)
    (done if ok else missing).append(out)
    print(("✓ exported: " if ok else "✗ FAILED: ") + out + "  ← layer '" + lyr.name() + "'"
          + ("" if ok else f"  ({res[1]})"))

print(f"\nDONE {len(done)} / {len(WANT)}.  MISSING/FAILED: {missing}")
print("→ zip 01_DATA/context/ back to Claude. Unlocks §3.1–3.4 (+ auto-ha Natura 2000 legend).")
print("If a layer is MISSING, find its real name in the Layers panel and add a substring to WANT above.")
