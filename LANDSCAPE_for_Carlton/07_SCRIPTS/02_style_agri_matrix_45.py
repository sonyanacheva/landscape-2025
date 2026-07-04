# 02_style_agri_matrix_45.py
# Run in QGIS: Plugins > Python Console > Show Editor > open > Run.
# Loads the processed 4.5 Agricultural Matrix, styles it categorized by agri_class
# with hectares in every legend label (architectural quantified legend), own group.
#
# DATA: 03_PROCESSED/agri_matrix_45.fgb  (layer 'agri', EPSG:25830, 298,434 parcels)
# Built by 07_SCRIPTS/03_build_agri_matrix_45.py from raw SIGPAC recintos.
#
# NOTE ON CLASSES (data kept rich, per Sonya/teacher decision):
#   "Grazed scrub / pasto arbustivo" (SIGPAC uso PR, 26,775 ha) is kept as its OWN
#   class — it is grazed shrubland, structurally matorral but land-use pasture. It is
#   the scrub<->grassland ECOTONE that matters most for the lynx lens, so it is neither
#   merged into Pasture nor into Scrub. "Pasture (open)" = PA+PS grassland grazing only.
import os
from qgis.core import (QgsVectorLayer, QgsProject, QgsCategorizedSymbolRenderer,
                       QgsRendererCategory, QgsFillSymbol)

# --- locate the shared folder -------------------------------------------------
# If the repo moves, edit BASE once (this single line, in each script).
BASE = r"C:\Users\Sonya\Desktop\Work_Vault\_Github\New folder\landscape-2025\LANDSCAPE_for_Carlton"
DATA = r"03_PROCESSED\agri_matrix_45.fgb"

def _resolve(base, data):
    # Try BASE first; then fall back to the folder of the SAVED .qgz project
    # (handles the repo being cloned to a different path than BASE).
    cands = [base]
    proj = QgsProject.instance().fileName()
    if proj:
        d = os.path.dirname(proj)
        cands += [d, os.path.join(d, "LANDSCAPE_for_Carlton"),
                  os.path.join(os.path.dirname(d), "LANDSCAPE_for_Carlton")]
    for b in cands:
        p = os.path.join(b, data)
        if os.path.exists(p):
            return p
    return os.path.join(base, data)   # clear error below if truly missing

PATH = _resolve(BASE, DATA)

# class -> (fill colour, hectares) — ordered arable > woody > hort > pasture > ecotone > scrub > forest > non-agri
# dryland pale straw, irrigated greener, woody olive, ecotone sage (between pasture green & scrub tan)
CLASSES = [
    ("Arable dryland",                  "#E7D9A0", 120264),
    ("Arable irrigated",                "#A6C25A",  95399),
    ("Woody crops",                     "#7E8B3C",  26799),
    ("Horticulture/greenhouse",         "#E06666",    145),
    ("Pasture (open)",                  "#CDE0B0",   3700),
    ("Grazed scrub / pasto arbustivo",  "#B7C083",  26775),   # ecotone — kept distinct
    ("Scrub (matorral)",                "#CBB07A",  46389),
    ("Forest",                          "#3E6B3A",  25964),
    ("Non-agricultural",                "#BFBFBF",  30676),
]

lyr = QgsVectorLayer(PATH, "4.5 Agricultural matrix", "ogr")
if not lyr.isValid():
    raise Exception("Layer failed to load: " + PATH)

cats = []
for val, col, ha in CLASSES:
    sym = QgsFillSymbol.createSimple({"color": col, "outline_color": "#00000030", "outline_width": "0.05"})
    label = f"{val}  ({ha:,} ha)"
    cats.append(QgsRendererCategory(val, sym, label))
# catch-all
other = QgsFillSymbol.createSimple({"color": "#EAEAEA", "outline_style": "no"})
cats.append(QgsRendererCategory("", other, "Other"))
lyr.setRenderer(QgsCategorizedSymbolRenderer("agri_class", cats))

QgsProject.instance().addMapLayer(lyr, False)
root = QgsProject.instance().layerTreeRoot()
grp = root.findGroup("4.5 AGRICULTURAL MATRIX") or root.insertGroup(0, "4.5 AGRICULTURAL MATRIX")
grp.addLayer(lyr)

# Save a .qml style sidecar next to the .fgb (QGIS writes valid XML). Once it exists,
# dragging the .fgb into QGIS auto-applies this styling + legend -- no script needed.
qml = PATH[:-4] + ".qml"
msg, ok = lyr.saveNamedStyle(qml)
print("Style sidecar saved:" if ok else "Sidecar FAILED:", qml, msg or "")
print("Loaded + styled: 4.5 Agricultural matrix (9 classes, ha legend)")
