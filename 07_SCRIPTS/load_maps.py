# load_maps.py  —  THE styling script (run this one; it supersedes the per-map style scripts).
# Run in QGIS: Plugins > Python Console > Show Editor > open this file > Run (green arrow).
#
# For every processed layer in 03_PROCESSED it:
#   1) loads the layer (skips it if already loaded),
#   2) applies its style,
#   3) SAVES a .qml sidecar next to the .fgb, then LOADS that .qml back onto the layer
#      (so the .qml on disk is the single source of truth + drag-and-drop styles later),
#   4) drops it into its own layer group.
# Idempotent: safe to re-run. Emails to Sonya = the .fgb files + this one script.
#
# TO RESTYLE ONE MAP: edit only its renderer_*() block below, then re-run.
# TO ADD A MAP:       add one renderer_*() function + one line in the MAPS registry.
import os
from qgis.core import (QgsVectorLayer, QgsProject, QgsCategorizedSymbolRenderer,
                       QgsRendererCategory, QgsFillSymbol, QgsLineSymbol)

# --- config -------------------------------------------------------------------
# Edit BASE once if the repo moves. Falls back to the saved .qgz project folder.
BASE = r"C:\Users\Sonya\Desktop\Work_Vault\_Github\New folder\landscape-2025\LANDSCAPE_for_Carlton"
PROCESSED_REL  = "03_PROCESSED"
RESTYLE_LOADED = True   # re-apply styles to already-loaded layers on re-run (propagates edits)

# =====================  PER-MAP STYLE BLOCKS (edit here)  ======================
def renderer_agri():
    # 4.5 Agricultural matrix — categorized on agri_class, ha in every label.
    # "Grazed scrub / pasto arbustivo" (PR) kept as its own ecotone class (sage).
    CLASSES = [
        ("Arable dryland",                 "#E7D9A0", 120264),
        ("Arable irrigated",               "#A6C25A",  95399),
        ("Woody crops",                    "#7E8B3C",  26799),
        ("Horticulture/greenhouse",        "#E06666",    145),
        ("Pasture (open)",                 "#CDE0B0",   3700),
        ("Grazed scrub / pasto arbustivo", "#B7C083",  26775),
        ("Scrub (matorral)",               "#CBB07A",  46389),
        ("Forest",                         "#3E6B3A",  25964),
        ("Non-agricultural",               "#BFBFBF",  30676),
    ]
    cats = []
    for val, col, ha in CLASSES:
        sym = QgsFillSymbol.createSimple({"color": col, "outline_color": "#00000030", "outline_width": "0.05"})
        cats.append(QgsRendererCategory(val, sym, f"{val}  ({ha:,} ha)"))
    other = QgsFillSymbol.createSimple({"color": "#EAEAEA", "outline_style": "no"})
    cats.append(QgsRendererCategory("", other, "Other"))
    return QgsCategorizedSymbolRenderer("agri_class", cats)

def renderer_canadas():
    # 4.x Cañadas — categorized on tipo, line-weight hierarchy by legal width, km in labels.
    STYLES = [
        ("Cañada",                   "#8A4B1F", 1.4, None,    437.2),
        ("Cordel",                   "#B5651D", 1.0, None,    248.1),
        ("Vereda",                   "#C6893F", 0.6, None,    364.6),
        ("Colada (variable)",        "#C6A15B", 0.4, "2;1",   166.2),
        ("Sin clasificar / revisar", "#9E9E9E", 0.3, "1;1.5",  63.4),
    ]
    cats = []
    for tipo, col, w, dash, km in STYLES:
        props = {"line_color": col, "line_width": str(w), "capstyle": "round", "joinstyle": "round"}
        if dash:
            props.update({"line_style": "dash", "customdash": dash, "use_custom_dash": "1"})
        cats.append(QgsRendererCategory(tipo, QgsLineSymbol.createSimple(props), f"{tipo}  ({km:,.0f} km)"))
    return QgsCategorizedSymbolRenderer("tipo", cats)

def renderer_forest():
    # 4.6 Forest / scrub / natural veg (MFE) — categorized on clase, ha in labels.
    # Agriculture is 4.5's job -> muted to a single context class (drawn as backdrop).
    # ⚠️ MFE = Huesca only; Zaragoza strip is blank until MFE50_50 is sourced.
    CLASSES = [
        ("Forest (natural)",                            "#2E5A32", 22980),
        ("Forest (plantation)",                         "#6E9B5A",  5427),
        ("Riparian woodland (riberas)",                 "#3E8E7E",  2678),
        ("Scrub (matorral)",                            "#C2A15E", 15687),
        ("Grassland–scrub mosaic",                      "#CBBE7A", 24478),
        ("Grassland (natural)",                         "#D9E4A5",   217),
        ("Wetland (humedal)",                           "#7EA6C4",   337),
        ("Bare / sparse",                               "#CFC3AE",    29),
        ("Non-forest context (agri/artificial/water)",  "#ECECEC", 221747),
    ]
    cats = []
    for val, col, ha in CLASSES:
        outline = "no" if val.startswith("Non-forest") else "solid"
        sym = QgsFillSymbol.createSimple({"color": col, "outline_color": "#00000025",
                                          "outline_width": "0.04", "outline_style": outline})
        cats.append(QgsRendererCategory(val, sym, f"{val}  ({ha:,} ha)"))
    return QgsCategorizedSymbolRenderer("clase", cats)

# =====================  REGISTRY (one line per map)  ==========================
MAPS = [
    {"file": "agri_matrix_45.fgb", "name": "4.5 Agricultural matrix",       "group": "4.5 AGRICULTURAL MATRIX", "renderer": renderer_agri},
    {"file": "canadas_4x.fgb",     "name": "4.x Cañadas (vías pecuarias)",  "group": "4.x CAÑADAS",             "renderer": renderer_canadas},
    {"file": "forest_46.fgb",      "name": "4.6 Forest / scrub / natural",  "group": "4.6 FOREST & NATURAL VEG","renderer": renderer_forest},
]

# =====================  ORCHESTRATOR (stable; no need to edit)  ================
def _base():
    cands = [BASE]
    proj = QgsProject.instance().fileName()
    if proj:
        d = os.path.dirname(proj)
        cands += [d, os.path.join(d, "LANDSCAPE_for_Carlton"),
                  os.path.join(os.path.dirname(d), "LANDSCAPE_for_Carlton")]
    for b in cands:
        if os.path.isdir(os.path.join(b, PROCESSED_REL)):
            return b
    return BASE

def _find_loaded(path):
    target = os.path.normcase(os.path.normpath(path))
    for lyr in QgsProject.instance().mapLayers().values():
        if os.path.normcase(os.path.normpath(lyr.source().split("|")[0])) == target:
            return lyr
    return None

def run():
    proc = os.path.join(_base(), PROCESSED_REL)
    root = QgsProject.instance().layerTreeRoot()
    for m in MAPS:
        path = os.path.join(proc, m["file"])
        if not os.path.exists(path):
            print("SKIP (file missing):", m["file"]); continue
        lyr = _find_loaded(path)
        already = lyr is not None
        if already and not RESTYLE_LOADED:
            print("SKIP (already loaded):", m["name"]); continue
        if not already:
            lyr = QgsVectorLayer(path, m["name"], "ogr")
            if not lyr.isValid():
                print("FAIL (invalid layer):", path); continue
        lyr.setRenderer(m["renderer"]())                 # apply style
        qml = os.path.splitext(path)[0] + ".qml"
        lyr.saveNamedStyle(qml)                           # 1) write .qml
        lyr.loadNamedStyle(qml)                           # 2) load .qml back (QML = source of truth)
        lyr.triggerRepaint()
        if not already:
            QgsProject.instance().addMapLayer(lyr, False)
            grp = root.findGroup(m["group"]) or root.insertGroup(0, m["group"])
            grp.addLayer(lyr)
        print(("RESTYLED" if already else "LOADED") + " + QML saved:", m["name"])
    print("load_maps: done.")

run()
