# 04_style_canadas_4x.py
# Run in QGIS: Plugins > Python Console > Show Editor > open > Run.
# Styles 4.x Cañadas / vías pecuarias with a line-weight hierarchy by tipo
# (cañada thickest -> colada thinnest), single sienna hue, km in every legend label.
#
# DATA: 03_PROCESSED/canadas_4x.fgb (layer 'canadas', EPSG:25830, lines)
# Built by 07_SCRIPTS/04_build_canadas_4x.py from national RGVP (Ley 3/1995).
# Field `ancho_m` = legal max width; `area_ha` = implementable public-corridor land.
from qgis.core import (QgsVectorLayer, QgsProject, QgsCategorizedSymbolRenderer,
                       QgsRendererCategory, QgsLineSymbol)

PATH = r"C:\Users\Sonya\Desktop\Work_Vault\1_University\4th Year\2_LANDSCAPE\LANDSCAPE_for_Carlton\03_PROCESSED\canadas_4x.fgb"

# tipo -> (line colour, width mm, dash) + km for the label. Width hierarchy = legal width.
STYLES = [
    ("Cañada",                    "#8A4B1F", 1.4, None,       437.2),
    ("Cordel",                    "#B5651D", 1.0, None,       248.1),
    ("Vereda",                    "#C6893F", 0.6, None,       364.6),
    ("Colada (variable)",         "#C6A15B", 0.4, "2;1",      166.2),
    ("Sin clasificar / revisar",  "#9E9E9E", 0.3, "1;1.5",     63.4),
]

lyr = QgsVectorLayer(PATH, "4.x Cañadas (vías pecuarias)", "ogr")
if not lyr.isValid():
    raise Exception("Layer failed to load: " + PATH)

cats = []
for tipo, col, w, dash, km in STYLES:
    props = {"line_color": col, "line_width": str(w), "capstyle": "round", "joinstyle": "round"}
    if dash:
        props["line_style"] = "dash"; props["customdash"] = dash; props["use_custom_dash"] = "1"
    sym = QgsLineSymbol.createSimple(props)
    cats.append(QgsRendererCategory(tipo, sym, f"{tipo}  ({km:,.0f} km)"))
lyr.setRenderer(QgsCategorizedSymbolRenderer("tipo", cats))

QgsProject.instance().addMapLayer(lyr, False)
root = QgsProject.instance().layerTreeRoot()
grp = root.findGroup("4.x CAÑADAS") or root.insertGroup(0, "4.x CAÑADAS")
grp.addLayer(lyr)
print("Loaded + styled: 4.x Cañadas — 1,279 km in box; 4,939 ha implementable public corridor")
