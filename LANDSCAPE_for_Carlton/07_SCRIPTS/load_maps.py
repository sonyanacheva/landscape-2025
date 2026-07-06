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
                       QgsRendererCategory, QgsFillSymbol, QgsLineSymbol, QgsMarkerSymbol,
                       QgsRasterLayer, QgsSingleBandPseudoColorRenderer, QgsRasterShader,
                       QgsColorRampShader, QgsSingleSymbolRenderer, QgsSingleBandGrayRenderer,
                       QgsContrastEnhancement)
from qgis.PyQt.QtGui import QColor, QPainter

# --- config -------------------------------------------------------------------
# Edit BASE once if the repo moves. Falls back to the saved .qgz project folder.
# Known repo locations, one per machine. Add yours here if it differs — no need to edit anything else.
BASES = [
    r"C:\Users\Sonya\Desktop\Work_Vault\_Github\New folder\landscape-2025\LANDSCAPE_for_Carlton",  # Sonya (Windows)
    "/Users/carltonfuturity/Developer/Github/landscape-2025/LANDSCAPE_for_Carlton",                # Carlton (Mac)
]
PROCESSED_REL  = "03_PROCESSED"
RESTYLE_LOADED = True   # re-apply styles to already-loaded layers on re-run (propagates edits)
ADD_PNOA_ORTHO = True   # stream the IGN PNOA orthophoto (greyscale + dim) as a backdrop (needs internet)

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
        ("Forest (natural)",                            "#2E5A32", 36853),
        ("Forest (plantation)",                         "#6E9B5A",  5730),
        ("Riparian woodland (riberas)",                 "#3E8E7E",  2719),
        ("Scrub (matorral)",                            "#C2A15E", 19396),
        ("Grassland–scrub mosaic",                      "#CBBE7A", 33470),
        ("Grassland (natural)",                         "#D9E4A5",   257),
        ("Wetland (humedal)",                           "#7EA6C4",  1056),
        ("Bare / sparse",                               "#CFC3AE",    38),
        ("Non-forest context (agri/artificial/water)",  "#ECECEC", 284039),
    ]
    cats = []
    for val, col, ha in CLASSES:
        outline = "no" if val.startswith("Non-forest") else "solid"
        sym = QgsFillSymbol.createSimple({"color": col, "outline_color": "#00000025",
                                          "outline_width": "0.04", "outline_style": outline})
        cats.append(QgsRendererCategory(val, sym, f"{val}  ({ha:,} ha)"))
    return QgsCategorizedSymbolRenderer("clase", cats)

def renderer_canada_lc():
    # 4.x-b Cañada × land-cover — categorized on readiness, km in labels.
    # Colours the protected spine by the matrix it runs through: green ready,
    # amber permeable, RED = intensive barrier (where §6 hedgerow/crossings go).
    STYLES = [
        ("Semi-natural (corridor-ready)",  "#2E7D32", 0.6, 205),
        ("Extensive farmland (permeable)", "#C9A227", 0.5, 161),
        ("Intensive farmland (barrier)",   "#C0392B", 0.8,  78),
        ("Other / non-agricultural",       "#9E9E9E", 0.3, 781),
    ]
    cats = []
    for val, col, w, km in STYLES:
        sym = QgsLineSymbol.createSimple({"line_color": col, "line_width": str(w),
                                          "capstyle": "round", "joinstyle": "round"})
        cats.append(QgsRendererCategory(val, sym, f"{val}  ({km:,} km)"))
    return QgsCategorizedSymbolRenderer("readiness", cats)

def renderer_barriers():
    # 4.4 barriers — corridor-fragmenting infrastructure, severity by colour/weight.
    STYLES = [
        ("Motorway / autovía",      "#B2182B", 1.3, None),
        ("Railway (incl. HS line)", "#542788", 1.0, "4;2"),
        ("Main road (N / primary)", "#EF6548", 0.8, None),
        ("Canal",                   "#2171B5", 0.8, None),
        ("Other major road",        "#FDAE61", 0.5, None),
    ]
    cats = []
    for val, col, w, dash in STYLES:
        props = {"line_color": col, "line_width": str(w), "capstyle": "round", "joinstyle": "round"}
        if dash:
            props.update({"line_style": "dash", "customdash": dash, "use_custom_dash": "1"})
        cats.append(QgsRendererCategory(val, QgsLineSymbol.createSimple(props), val))
    return QgsCategorizedSymbolRenderer("barrier_type", cats)

def renderer_crossings():
    # 4.4 crossing catalogue — RED triangle = open cut (needs structure), green = has one.
    open_s = QgsMarkerSymbol.createSimple({"name": "triangle", "color": "#B2182B",
                                           "outline_color": "#FFFFFF", "outline_width": "0.3", "size": "3.6"})
    has_s  = QgsMarkerSymbol.createSimple({"name": "circle", "color": "#1A9850",
                                           "outline_color": "#FFFFFF", "outline_width": "0.3", "size": "3.0"})
    cats = [QgsRendererCategory("Open barrier (no structure)", open_s, "Open barrier — needs crossing"),
            QgsRendererCategory("Has bridge/tunnel", has_s, "Has bridge/tunnel")]
    return QgsCategorizedSymbolRenderer("structure", cats)

def renderer_human_pressure():
    # 4.4 human-pressure envelope — translucent tint.
    sym = QgsFillSymbol.createSimple({"color": "178,24,43,40", "outline_color": "178,24,43,110",
                                      "outline_width": "0.1"})
    return QgsCategorizedSymbolRenderer("zone", [QgsRendererCategory("250 m human-pressure zone", sym, "250 m human-pressure zone")])

def renderer_aos_frame():
    # AREA OF STUDY frame — bold outline, no fill, drawn over everything.
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"style": "no", "outline_color": "#111111", "outline_width": "0.5"}))

def renderer_towns():
    # §3.3 populated places — size hierarchy by place type (enable labels on 'name').
    STYLES = [("town", "#333333", "3.4"), ("village", "#555555", "2.4"), ("hamlet", "#888888", "1.7")]
    cats = [QgsRendererCategory(v, QgsMarkerSymbol.createSimple(
        {"name": "circle", "color": c, "outline_color": "#FFFFFF", "outline_width": "0.2", "size": s}), v)
        for v, c, s in STYLES]
    return QgsCategorizedSymbolRenderer("place", cats)

def _outline(color, width):
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"style": "no", "outline_color": color, "outline_width": str(width)}))

def renderer_municipios():  return _outline("#9A8C98", 0.12)   # 3.3 work-area municipios (enable labels on 'nombre')
def renderer_provinces():   return _outline("#6D6875", 0.35)   # province boundaries
def renderer_comunidades(): return _outline("#403A44", 0.55)   # Aragón boundary

def renderer_interventions():
    # 6a masterplan — proposed intervention nodes.
    fc = QgsMarkerSymbol.createSimple({"name": "diamond", "color": "#D7301F",
         "outline_color": "#FFFFFF", "outline_width": "0.3", "size": "3.6"})
    hg = QgsMarkerSymbol.createSimple({"name": "cross_fill", "color": "#238B45",
         "outline_color": "#FFFFFF", "outline_width": "0.2", "size": "3.0"})
    cats = [QgsRendererCategory("Fauna crossing", fc, "Fauna crossing (priority)"),
            QgsRendererCategory("Hedgerow / field-corner", hg, "Hedgerow / field-corner")]
    return QgsCategorizedSymbolRenderer("tipo", cats)

def renderer_viewpoints():
    # 5.1b storyboard viewpoints — categorized by what the lynx encounters.
    CLASSES = [
        ("Barrier crossing",             "circle",   "#B2182B", "3.6"),
        ("Ravine crossing (Valcuerna)",  "circle",   "#08306B", "3.4"),
        ("River crossing",               "circle",   "#2171B5", "3.4"),
        ("Protected core",               "star",     "#1A9850", "4.0"),
        ("Habitat discontinuity",        "triangle", "#FDAE61", "3.4"),
        ("Ecotone / cover",              "circle",   "#74C476", "3.0"),
        ("Transit",                      "circle",   "#BBBBBB", "2.6"),
    ]
    cats = []
    for val, shape, col, sz in CLASSES:
        sym = QgsMarkerSymbol.createSimple({"name": shape, "color": col,
              "outline_color": "#FFFFFF", "outline_width": "0.3", "size": sz})
        cats.append(QgsRendererCategory(val, sym, val))
    return QgsCategorizedSymbolRenderer("clase", cats)

def renderer_lcp():
    # 5.2 our least-cost corridor (Valcuerna ↔ Alcubierre) from the resistance surface.
    sym = QgsLineSymbol.createSimple({"line_color": "#7A0000", "line_width": "1.4", "capstyle": "round"})
    return QgsSingleSymbolRenderer(sym)

def renderer_wwf():
    # 5.2 WWF priority corridor — REFERENCE overlay (dashed) to validate our network against.
    sym = QgsLineSymbol.createSimple({"line_color": "#6A51A3", "line_width": "1.0",
                                      "line_style": "dash", "customdash": "4;2", "use_custom_dash": "1"})
    return QgsSingleSymbolRenderer(sym)

def renderer_flood():
    # 4.3 SNCZI flood zones — translucent blues; T=500 (broader) under T=100.
    CLASSES = [("T=500 (excepcional)", "158,202,225,90"), ("T=100 (ocasional)", "66,146,198,110")]
    cats = [QgsRendererCategory(v, QgsFillSymbol.createSimple(
        {"color": c, "outline_color": "#2171B5", "outline_width": "0.05"}), v) for v, c in CLASSES]
    return QgsCategorizedSymbolRenderer("periodo", cats)

def renderer_streams():
    # 4.3 drainage network — width hierarchy by contributing area.
    STYLES = [
        ("Main barranco",     "#08306B", 1.3),
        ("Secondary channel", "#3182BD", 0.7),
        ("Minor drainage",    "#9ECAE1", 0.3),
    ]
    cats = [QgsRendererCategory(v, QgsLineSymbol.createSimple(
        {"line_color": c, "line_width": str(w), "capstyle": "round"}), v) for v, c, w in STYLES]
    return QgsCategorizedSymbolRenderer("clase", cats)

def renderer_geomorph():
    # 4.2 Geomorphology (GEODE) — 58 units → 11 landform classes, earth tones,
    # gypsum + mudstone badlands foregrounded (the Monegros signature), salada highlighted.
    CLASSES = [
        ("Gypsum badlands (yesos)",     "#B7A6C9"),
        ("Mudstone badlands (lutitas)", "#C8A96A"),
        ("Sandstone / paleochannel",    "#C0714B"),
        ("Limestone / marl platform",   "#CFCBBE"),
        ("Glacis / pediment",           "#D8C98E"),
        ("River terrace / fan",         "#E3D6A0"),
        ("Alluvial valley floor",       "#C6D2A0"),
        ("Colluvium / slope deposit",   "#B58C64"),
        ("Endorheic basin / salada",    "#E3B7C0"),
        ("Water body",                  "#9EC5E8"),
        ("Other",                       "#EDEDED"),
    ]
    cats = []
    for val, col in CLASSES:
        sym = QgsFillSymbol.createSimple({"color": col, "outline_color": "#00000022", "outline_width": "0.04"})
        cats.append(QgsRendererCategory(val, sym, val))
    return QgsCategorizedSymbolRenderer("geomorph", cats)

def renderer_hydro_lines():
    # 4.1 Hydrography lines — Valcuerna spine drawn boldest (the §6 ecological spine).
    STYLES = [
        ("Barranco de Valcuerna (spine)",  "#08306B", 1.4, None),
        ("Main river",                     "#2171B5", 0.8, None),
        ("Natural drainage (seasonal)",    "#6BAED6", 0.4, None),
        ("Artificial drainage (acequias)", "#9ECAE1", 0.3, "3;1.5"),
    ]
    cats = []
    for val, col, w, dash in STYLES:
        props = {"line_color": col, "line_width": str(w), "capstyle": "round", "joinstyle": "round"}
        if dash:
            props.update({"line_style": "dash", "customdash": dash, "use_custom_dash": "1"})
        cats.append(QgsRendererCategory(val, QgsLineSymbol.createSimple(props), val))
    return QgsCategorizedSymbolRenderer("hydro_class", cats)

def renderer_hydro_water():
    # 4.1 water bodies — lagoons/saladas, reservoirs, main canals (fills).
    CLASSES = [("Lagoon / salada", "#C6DBEF"), ("Reservoir", "#4292C6"), ("Main canal", "#2171B5")]
    cats = []
    for val, col in CLASSES:
        sym = QgsFillSymbol.createSimple({"color": col, "outline_color": "#2171B5", "outline_width": "0.06"})
        cats.append(QgsRendererCategory(val, sym, val))
    return QgsCategorizedSymbolRenderer("hydro_class", cats)

def renderer_hydro_springs():
    # 4.1 springs — small points.
    sym = QgsMarkerSymbol.createSimple({"name": "circle", "color": "#08519C",
                                        "outline_color": "#FFFFFF", "outline_width": "0.2", "size": "1.4"})
    cat = QgsRendererCategory("Spring", sym, "Spring")
    return QgsCategorizedSymbolRenderer("hydro_class", [cat])

def renderer_natura():
    # §3.3 Natura 2000 — categorized by designation; semi-transparent fills so overlaps read.
    CLASSES = [
        ("ZEPA",             "166,217,106,90",  "#4D7A1F"),
        ("LIC + ZEC",        "116,173,209,90",  "#2C5985"),
        ("LIC + ZEC + ZEPA", "177,143,207,110", "#6A4A8E"),
        ("LIC",              "116,173,209,90",  "#2C5985"),
        ("Natura 2000",      "180,180,180,80",  "#666666"),
    ]
    cats = []
    for val, fill, outline in CLASSES:
        sym = QgsFillSymbol.createSimple({"color": fill, "outline_color": outline, "outline_width": "0.26"})
        cats.append(QgsRendererCategory(val, sym, val))
    return QgsCategorizedSymbolRenderer("tipo", cats)

def renderer_corridor():
    # §3.1/3.2 WWF priority corridor network — study-area links highlighted.
    STYLES = [
        ("Corridor through study area", "#D7301F", 1.4),
        ("Priority corridor network",  "#9E9AC8", 0.4),
    ]
    cats = [QgsRendererCategory(v, QgsLineSymbol.createSimple(
        {"line_color": c, "line_width": str(w), "capstyle": "round"}), v) for v, c, w in STYLES]
    return QgsCategorizedSymbolRenderer("clase", cats)

def renderer_zonas_criticas():
    # §3.4 WWF critical zones — study-area zone emphasised.
    CLASSES = [("Critical zone (study area)", "217,95,14,70", "#8C2D04"),
               ("Critical zone (national)",   "253,208,162,45", "#D9954B")]
    cats = [QgsRendererCategory(v, QgsFillSymbol.createSimple(
        {"color": c, "outline_color": o, "outline_width": "0.3"}), v) for v, c, o in CLASSES]
    return QgsCategorizedSymbolRenderer("clase", cats)

def renderer_frames():
    # Nested extent frames — dashed, no fill; heavier line for the finer scales.
    STYLES = [("Spain", "#B4B4B4", 0.2), ("Region", "#8A8A8A", 0.3),
              ("Work-area", "#333333", 0.45), ("Study-box", "#111111", 0.5)]
    cats = [QgsRendererCategory(v, QgsFillSymbol.createSimple(
        {"style": "no", "outline_color": c, "outline_width": str(w), "outline_style": "dash"}), v)
        for v, c, w in STYLES]
    return QgsCategorizedSymbolRenderer("frame", cats)

def renderer_reserves():
    # §3.2/3.3 protected "espacios" (named reserves) — green fill; enable labels on SITE_NAME.
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"color": "120,180,110,90", "outline_color": "#4C7A3A", "outline_width": "0.2"}))

def renderer_natura_green():
    # §3.1/3.2 Natura 2000 (region/national) — single green fill (no 'tipo' attribute here).
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"color": "150,190,120,80", "outline_color": "#5C7A3A", "outline_width": "0.1"}))

def renderer_workzones():
    # §3.4b work-area sub-zones (DRAFT) — light fill; enable labels on zone_no / SITE_NAME.
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"color": "200,180,140,70", "outline_color": "#8A6D3B", "outline_width": "0.25"}))

def renderer_provinces_region(): return _outline("#6D6875", 0.3)    # 3.2 province borders (region)
def renderer_comunidad_region(): return _outline("#403A44", 0.6)    # 3.2 Aragón|Catalunya boundary

def renderer_corridor_focus():
    # §3.1 corridor network — grey where it doesn't concern us, BLUE for the Sierras-Litorales
    # arc near/around the study area (focus = 1).
    grey = QgsLineSymbol.createSimple({"line_color": "#B9B9B9", "line_width": "0.22", "capstyle": "round"})
    blue = QgsLineSymbol.createSimple({"line_color": "#1F6FB2", "line_width": "0.9",  "capstyle": "round"})
    cats = [QgsRendererCategory(0, grey, "Corridor network (other)"),
            QgsRendererCategory(1, blue, "Sierras Litorales (our corridor)")]
    return QgsCategorizedSymbolRenderer("focus", cats)

def renderer_aragon_land():
    # §3.2 Aragón — light land fill + visible border (map 2 base; nothing shown outside it).
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"color": "#F3EFE3", "outline_color": "#333333", "outline_width": "0.5"}))

def renderer_urban():
    # §5.1a urban footprints (SIGPAC ZU + ED) — signalled in RED on the habitats map.
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"color": "200,50,40,190", "outline_color": "#7E1A10", "outline_width": "0.12"}))

def renderer_corridor_grey():
    # §3.1 whole national corridor network — the ones we don't focus on (grey).
    return QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
        {"line_color": "#BEBEBE", "line_width": "0.2", "capstyle": "round"}))

def renderer_corridor_sierras():
    # §3.1 Sierras Litorales del Mediterráneo — OUR corridor (blue), corrected dataset from Sonya.
    return QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
        {"line_color": "#1F6FB2", "line_width": "0.9", "capstyle": "round"}))

def renderer_aragon_border():
    # §3.2 Aragón outline only (no land fill — greyscale orthophoto sits underneath).
    return _outline("#333333", 0.5)

def renderer_mask_white():
    # §3.2 white donut = everything outside Aragón; clips the orthophoto to the region.
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"color": "255,255,255,255", "outline_style": "no"}))

def renderer_water_polys():
    # Real-width water SHAPES (OSM). Sonya's palette: light blue #B2CADC for river/lake,
    # deeper blue-grey for embalses. Sized by true feature width — no fake-fat lines.
    blue = QgsFillSymbol.createSimple({"color": "#B2CADC", "outline_color": "#7FA8C9", "outline_width": "0.06"})
    resv = QgsFillSymbol.createSimple({"color": "#8FB0C9", "outline_color": "#6E93B0", "outline_width": "0.06"})
    cats = [QgsRendererCategory("riverbank", blue.clone(), "River"),
            QgsRendererCategory("water",     blue.clone(), "Water body"),
            QgsRendererCategory("reservoir", resv,         "Reservoir (embalse)")]
    return QgsCategorizedSymbolRenderer("fclass", cats)

def renderer_hydro_lines_che():
    # §4.1 official water lines — width scaled by class so big rivers read thick, streams thin.
    STY = [("river", "#4E86C5", 0.7), ("canal", "#8FB0C9", 0.45),
           ("stream", "#6E9BC0", 0.3), ("drain", "#A9C0D2", 0.18)]
    cats = [QgsRendererCategory(v, QgsLineSymbol.createSimple(
        {"line_color": c, "line_width": str(w), "capstyle": "round"}), v) for v, c, w in STY]
    return QgsCategorizedSymbolRenderer("fclass", cats)

def renderer_seasonal():
    # §4.1 seasonal barrancos (incl. the dry Valcuerna) — dashed, thin, scaled by hierarchy.
    STY = [("01", 0.5), ("02", 0.4), ("03", 0.26), ("04", 0.15)]
    cats = [QgsRendererCategory(v, QgsLineSymbol.createSimple(
        {"line_color": "#A1BBCF", "line_width": str(w), "line_style": "dash", "capstyle": "round"}),
        f"Seasonal (order {v})") for v, w in STY]
    return QgsCategorizedSymbolRenderer("jerar_0302", cats)

def renderer_saladas():
    # §4.1 saladas — Monegros salt lagoons; pale salt-pink to distinguish from freshwater.
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"color": "#E0C6D0", "outline_color": "#B98CA0", "outline_width": "0.1"}))

def renderer_reservoirs_che():
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"color": "#8FB0C9", "outline_color": "#6E93B0", "outline_width": "0.08"}))

def renderer_canals_poly():
    # §4.1 main artificial channels — muted grey-blue (irrigation infrastructure).
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {"color": "#9AAAB5", "outline_color": "#6F7F8A", "outline_width": "0.08"}))

def renderer_springs_che():
    return QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple(
        {"name": "circle", "color": "#3E78B2", "outline_color": "#FFFFFF", "outline_width": "0.2", "size": "1.3"}))

def renderer_contours():
    # Territorial map — 20 m contours, index (100 m) heavier; muted brown so ortho reads through.
    reg = QgsLineSymbol.createSimple({"line_color": "150,120,90,110", "line_width": "0.05"})
    idx = QgsLineSymbol.createSimple({"line_color": "120,90,60,175", "line_width": "0.18"})
    cats = [QgsRendererCategory(0, reg, "Contour (20 m)"), QgsRendererCategory(1, idx, "Index (100 m)")]
    return QgsCategorizedSymbolRenderer("idx", cats)

def renderer_trails():
    # Human map — OSM tracks / paths (fine brown dashed).
    return QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
        {"line_color": "140,110,80,170", "line_width": "0.12", "line_style": "dash", "capstyle": "round"}))

def renderer_countries():
    # §3.1 national backdrop — Spain highlighted, neighbours muted.
    es = QgsFillSymbol.createSimple({"color": "#EFE7D3", "outline_color": "#7A6A55", "outline_width": "0.2"})
    other = QgsFillSymbol.createSimple({"color": "#F2F2F0", "outline_color": "#C8C8C8", "outline_width": "0.12"})
    cats = [QgsRendererCategory("Spain", es, "Spain"), QgsRendererCategory("", other, "Neighbours")]
    return QgsCategorizedSymbolRenderer("ADMIN", cats)

def renderer_resistance_classes():
    # 5.2 resistance surface as BLACK-AND-WHITE hatching; denser hatch = more resistance.
    # Brush ramp light->dark = low->high resistance (Qt fill styles):
    #   dense7 (sparsest) -> dense5 -> dense3 -> dense1 -> solid (black barrier).
    CLASSES = [
        (1, "Very low (1-5) - permeable",  "dense7"),
        (2, "Low (5-20)",                  "dense5"),
        (3, "Moderate (20-40)",            "dense3"),
        (4, "High (40-60)",                "dense1"),
        (5, "Very high / barrier (>60)",   "solid"),
    ]
    cats = []
    for v, lbl, brush in CLASSES:
        sym = QgsFillSymbol.createSimple({
            "color": "0,0,0,255", "style": brush,
            "outline_color": "90,90,90,255", "outline_width": "0.05", "outline_style": "solid"})
        cats.append(QgsRendererCategory(v, sym, lbl))
    return QgsCategorizedSymbolRenderer("cls", cats)

# =====================  REGISTRY (one line per map)  ==========================
MAPS = [
    {"file": "agri_matrix_45.fgb",   "name": "4.5 Agricultural matrix",        "group": "4.5 AGRICULTURAL MATRIX",  "renderer": renderer_agri},
    {"file": "canadas_4x.fgb",       "name": "4.x Cañadas (vías pecuarias)",   "group": "4.x CAÑADAS",              "renderer": renderer_canadas},
    {"file": "forest_46.fgb",        "name": "4.6 Forest / scrub / natural",   "group": "4.6 FOREST & NATURAL VEG", "renderer": renderer_forest},
    {"file": "canada_landcover.fgb", "name": "4.x-b Cañada × land cover",      "group": "4.x CAÑADAS",              "renderer": renderer_canada_lc},
    {"file": "hydro_springs_41.fgb", "name": "4.1 Springs",                    "group": "4.1 HYDROGRAPHY",          "renderer": renderer_hydro_springs},
    {"file": "hydro_lines_41.fgb",   "name": "4.1 Watercourses + Valcuerna",   "group": "4.1 HYDROGRAPHY",          "renderer": renderer_hydro_lines},
    {"file": "hydro_water_41.fgb",   "name": "4.1 Water bodies",               "group": "4.1 HYDROGRAPHY",          "renderer": renderer_hydro_water},
    {"file": "geomorph_42.fgb",      "name": "4.2 Geomorphology",              "group": "4.2 GEOMORPHOLOGY",        "renderer": renderer_geomorph},
    {"file": "countries_iberia_31.fgb","name": "3.1 National backdrop",         "group": "3.1 CONTEXT",              "renderer": renderer_countries},
    {"file": "natura2000_box.fgb",   "name": "3.3 Natura 2000 sites",          "group": "3.3 NATURA 2000",          "renderer": renderer_natura},
    {"file": "crossings_44.fgb",     "name": "4.4 Crossing catalogue",         "group": "4.4 HUMAN PRESSURE & BARRIERS", "renderer": renderer_crossings},
    {"file": "barriers_44.fgb",      "name": "4.4 Barriers",                   "group": "4.4 HUMAN PRESSURE & BARRIERS", "renderer": renderer_barriers},
    {"file": "human_pressure_44.fgb","name": "4.4 Human-pressure zone",        "group": "4.4 HUMAN PRESSURE & BARRIERS", "renderer": renderer_human_pressure},
    {"file": "streams_43.fgb",       "name": "4.3 Drainage network",           "group": "4.3 FLOW & EROSION",       "renderer": renderer_streams},
    {"file": "flood_43.fgb",         "name": "4.3 Flood zones (SNCZI)",        "group": "4.3 FLOW & EROSION",       "renderer": renderer_flood},
    {"file": "corridor_wwf_52.fgb",  "name": "5.2 WWF corridor (reference)",   "group": "5.2 RESISTANCE & CORRIDOR","renderer": renderer_wwf},
    {"file": "corridor_lcp_52.fgb",  "name": "5.2 Least-cost corridor",        "group": "5.2 RESISTANCE & CORRIDOR","renderer": renderer_lcp},
    {"file": "resistance_classes_52.fgb","name": "5.2 Resistance (B&W hatch)",  "group": "5.2 RESISTANCE & CORRIDOR","renderer": renderer_resistance_classes},
    {"file": "viewpoints_51b.fgb",   "name": "5.1b Storyboard viewpoints",     "group": "5.1b STORYBOARD",          "renderer": renderer_viewpoints},
    {"file": "interventions_6a.fgb", "name": "6a Interventions (proposed)",    "group": "6a MASTERPLAN",            "renderer": renderer_interventions},
    {"file": "comunidades_3.fgb",    "name": "3.x Aragón boundary",            "group": "3.x ADMIN BOUNDARIES",    "renderer": renderer_comunidades},
    {"file": "provinces_3.fgb",      "name": "3.x Provinces",                  "group": "3.x ADMIN BOUNDARIES",    "renderer": renderer_provinces},
    {"file": "municipios_box_33.fgb","name": "3.3 Municipios (work area)",      "group": "3.x ADMIN BOUNDARIES",    "renderer": renderer_municipios},
    {"file": "towns_33.fgb",         "name": "3.3 Towns",                      "group": "3.x ADMIN BOUNDARIES",    "renderer": renderer_towns},
    {"file": "aos_frame.fgb",        "name": "Area of study frame",            "group": "FRAME (AOS)",              "renderer": renderer_aos_frame},
    {"file": "corridor_3.fgb",       "name": "3.1 Corridor network (grey)",    "group": "3.1 CONTEXT",              "renderer": renderer_corridor_grey},
    {"file": "corridor_sierras.fgb", "name": "3.1 Sierras Litorales corridor", "group": "3.1 CONTEXT",              "renderer": renderer_corridor_sierras},
    {"file": "zonas_criticas_34.fgb","name": "3.4 Critical zones (WWF)",       "group": "3.4 CRITICAL POINTS",      "renderer": renderer_zonas_criticas},
    # --- §3 context rebuilt WIDE (nested extents; crop later via layout frame + Map Themes) ---
    {"file": "frames_extents.fgb",       "name": "Nested extent frames",         "group": "FRAME (AOS)",         "renderer": renderer_frames},
    {"file": "natura2000_national.fgb",  "name": "3.1 Natura 2000 (Spain)",      "group": "3.1 CONTEXT",         "renderer": renderer_natura_green},
    {"file": "reserves_espacios.fgb",    "name": "3.2 Reserves / espacios (named)","group": "3.2 REGION",        "renderer": renderer_reserves},
    {"file": "natura2000_region.fgb",    "name": "3.2 Natura 2000 (region)",     "group": "3.2 REGION",          "renderer": renderer_natura_green},
    {"file": "admin_comunidad_region.fgb","name": "3.2 Aragón boundary (region)", "group": "3.x ADMIN BOUNDARIES","renderer": renderer_comunidad_region},
    {"file": "admin_provinces_region.fgb","name": "3.2 Provinces (region)",      "group": "3.x ADMIN BOUNDARIES","renderer": renderer_provinces_region},
    {"file": "workzones_34b_draft.fgb",  "name": "3.4b Work-area sub-zones (draft)","group": "3.4b WORK ZONES",  "renderer": renderer_workzones},
    # --- map 2 (Aragón): border-only + clip mask + Aragón-clipped reserves/natura ---
    {"file": "admin_aragon.fgb",       "name": "3.2 Aragón (border only)",       "group": "3.2 REGION",   "renderer": renderer_aragon_border},
    {"file": "mask_outside_aragon.fgb","name": "3.2 Aragón clip mask (white)",   "group": "3.2 REGION",   "renderer": renderer_mask_white},
    {"file": "reserves_aragon.fgb",    "name": "3.2 Reserves (Aragón)",          "group": "3.2 REGION",   "renderer": renderer_reserves},
    {"file": "natura_aragon.fgb",      "name": "3.2 Natura 2000 (Aragón)",       "group": "3.2 REGION",   "renderer": renderer_natura_green},
    {"file": "corridor_sierras_aragon.fgb","name": "3.2 Sierras corridor (Aragón)","group": "3.2 REGION",  "renderer": renderer_corridor_sierras},
    {"file": "urban_areas.fgb",        "name": "5.1a Urban areas (red)",         "group": "5.1a HABITAT", "renderer": renderer_urban},
    {"file": "water_owm.fgb",          "name": "4.1 Water (real-width shapes)",  "group": "4.1 HYDROGRAPHY", "renderer": renderer_water_polys},
    # --- richer official (CHE) hydrography from Sonya's hydro.zip ---
    {"file": "saladas.fgb",            "name": "4.1 Saladas (salt lagoons)",     "group": "4.1 HYDROGRAPHY", "renderer": renderer_saladas},
    {"file": "reservoirs_che.fgb",     "name": "4.1 Reservoirs (embalses)",      "group": "4.1 HYDROGRAPHY", "renderer": renderer_reservoirs_che},
    {"file": "canals_poly.fgb",        "name": "4.1 Main channels (canals)",     "group": "4.1 HYDROGRAPHY", "renderer": renderer_canals_poly},
    {"file": "hydro_lines_che.fgb",    "name": "4.1 Water lines (by class)",     "group": "4.1 HYDROGRAPHY", "renderer": renderer_hydro_lines_che},
    {"file": "seasonal_drainage.fgb",  "name": "4.1 Seasonal barrancos",         "group": "4.1 HYDROGRAPHY", "renderer": renderer_seasonal},
    {"file": "springs_che.fgb",        "name": "4.1 Springs (CHE)",              "group": "4.1 HYDROGRAPHY", "renderer": renderer_springs_che},
    {"file": "contours.fgb",           "name": "Contours (5 m)",                 "group": "4.2 GEOMORPHOLOGY", "renderer": renderer_contours},
    {"file": "trails_human.fgb",       "name": "4.4 Trails (OSM tracks/paths)",  "group": "4.4 HUMAN PRESSURE & BARRIERS", "renderer": renderer_trails},
]

# ---- RASTERS (loaded + pseudocolour-styled; add one line per raster) ----------
RASTERS = [
    {"file": "erosion_spi_43.tif",    "name": "4.3 Erosion (stream power)", "group": "4.3 FLOW & EROSION",
     "colors": ["#f7fcf0", "#c7e9b4", "#fed976", "#fd8d3c", "#bd0026"]},
    {"file": "flowacc_43.tif",        "name": "4.3 Flow accumulation",      "group": "4.3 FLOW & EROSION",
     "colors": ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08306b"]},
    # 5.2 resistance now shown as B&W hatch VECTOR (resistance_classes_52.fgb, see MAPS).
    # Colour raster kept here but disabled; uncomment to restore the pseudocolour version.
    # {"file": "resistance_52.tif",     "name": "5.2 Resistance surface",     "group": "5.2 RESISTANCE & CORRIDOR",
    #  "colors": ["#1a9850", "#a6d96a", "#ffffbf", "#fdae61", "#d73027"], "vmin": 1, "vmax": 80},
    {"file": "corridor_swath_52.tif", "name": "5.2 Corridor swath",         "group": "5.2 RESISTANCE & CORRIDOR",
     "colors": ["#54278f", "#9e9ac8", "#dadaeb"]},
    {"file": "corridor_wwf_swath_52.tif", "name": "5.2 WWF corridor zone",  "group": "5.2 RESISTANCE & CORRIDOR",
     "colors": ["#9e9ac8", "#cbc9e2", "#f2f0f7"], "vmin": 0, "vmax": 1500},
    # Habitat classes (1-5) in green/blue so habitat reads; matrix/non-habitat (6-8) greyscale + recede.
    {"file": "habitat_51a.tif",       "name": "5.1a Lynx + rabbit habitat", "group": "5.1a HABITAT", "categories": [
        (1, "#2E7D32", "Lynx + rabbit optimal (ecotone)"), (2, "#3E8E9C", "Riparian corridor"),
        (3, "#6FA96B", "Lynx cover (scrub/forest)"),       (4, "#B7D6A6", "Rabbit foraging (open)"),
        (5, "#7FA8C9", "Wetland / salada"),                (6, "#ECECE8", "Matrix (permeable)"),
        (7, "#D9D9D6", "Matrix (hostile)"),                (8, "#F5F5F3", "Non-habitat")]},
    # Dramatic relief for the hydrography map (only place it's used now): high contrast, near-opaque.
    {"file": "hillshade.tif",         "name": "Hillshade (backdrop)",       "group": "0 BASEMAP", "gray": True,
     "brightness": -10, "contrast": 55, "opacity": 0.9, "blend": "normal"},
]

# Layer-tree group order, TOP → BOTTOM (subject/points up, fills down, basemap at the bottom).
GROUP_ORDER = [
    "FRAME (AOS)",
    "5.1b STORYBOARD", "6a MASTERPLAN", "5.2 RESISTANCE & CORRIDOR", "5.1a HABITAT",
    "3.4b WORK ZONES", "3.4 CRITICAL POINTS", "4.4 HUMAN PRESSURE & BARRIERS", "4.x CAÑADAS",
    "4.3 FLOW & EROSION", "4.1 HYDROGRAPHY", "3.3 NATURA 2000",
    "4.6 FOREST & NATURAL VEG", "4.5 AGRICULTURAL MATRIX", "4.2 GEOMORPHOLOGY",
    "3.2 REGION", "3.x ADMIN BOUNDARIES", "3.1 CONTEXT", "0 BASEMAP",
]

# =====================  ORCHESTRATOR (stable; no need to edit)  ================
def _base():
    # Return a folder that actually contains 03_PROCESSED. Tries the saved-project folder
    # first (works on any machine), then the known BASES. No folder-picker, no SystemExit
    # (SystemExit crashes QGIS). If nothing matches, raise a normal error with guidance.
    cands = []
    proj = QgsProject.instance().fileName()
    if proj:
        d = os.path.dirname(proj)
        cands += [d, os.path.join(d, "LANDSCAPE_for_Carlton"),
                  os.path.join(os.path.dirname(d), "LANDSCAPE_for_Carlton")]
    cands += BASES
    for b in cands:
        if b and os.path.isdir(os.path.join(b, PROCESSED_REL)):
            return b
    raise Exception(
        "load_maps: couldn't find a folder containing '%s'. "
        "Add this machine's path to the BASES list at the top of the script "
        "(or save your .qgz inside the repo). Looked in: %s"
        % (PROCESSED_REL, [c for c in cands if c]))

def _find_loaded(path):
    target = os.path.normcase(os.path.normpath(path))
    for lyr in QgsProject.instance().mapLayers().values():
        if os.path.normcase(os.path.normpath(lyr.source().split("|")[0])) == target:
            return lyr
    return None

def run():
    proc = os.path.join(_base(), PROCESSED_REL)
    root = QgsProject.instance().layerTreeRoot()
    # drop orphans: layers pointing at a 03_PROCESSED file that no longer exists (superseded outputs)
    procn = os.path.normcase(os.path.normpath(proc))
    for lyr in list(QgsProject.instance().mapLayers().values()):
        src = lyr.source().split("|")[0]
        if src.startswith(("/", "\\")) or ":" in src[:3]:  # a file path
            n = os.path.normcase(os.path.normpath(src))
            if n.startswith(procn) and not os.path.exists(src):
                nm, lid = lyr.name(), lyr.id()             # read BEFORE removing (wrapper dies after)
                QgsProject.instance().removeMapLayer(lid); print("removed orphan:", nm)
    for m in MAPS:
        path = os.path.join(proc, m["file"])
        if not os.path.exists(path):
            print("SKIP (file missing):", m["file"]); continue
        old = _find_loaded(path)
        if old is not None:
            if not RESTYLE_LOADED:
                print("SKIP (already loaded):", m["name"]); continue
            QgsProject.instance().removeMapLayer(old.id())   # drop stale → reload fresh (data + style)
        lyr = QgsVectorLayer(path, m["name"], "ogr")
        if not lyr.isValid():
            print("FAIL (invalid layer):", path); continue
        lyr.setRenderer(m["renderer"]())
        qml = os.path.splitext(path)[0] + ".qml"
        lyr.saveNamedStyle(qml)                           # 1) write .qml
        lyr.loadNamedStyle(qml)                           # 2) load it back (QML = source of truth)
        QgsProject.instance().addMapLayer(lyr, False)
        grp = root.findGroup(m["group"]) or root.insertGroup(0, m["group"])
        grp.addLayer(lyr)
        print(("RELOADED" if old is not None else "LOADED") + " + QML:", m["name"])

    # ---- rasters (pseudocolour) — defensive: a raster hiccup won't break the vectors ----
    for r in RASTERS:
        path = os.path.join(proc, r["file"])
        if not os.path.exists(path):
            print("SKIP (raster missing):", r["file"]); continue
        old = _find_loaded(path)
        if old is not None:
            if not RESTYLE_LOADED:
                print("SKIP (already loaded):", r["name"]); continue
            QgsProject.instance().removeMapLayer(old.id())   # drop stale → reload fresh
        try:
            rl = QgsRasterLayer(path, r["name"])
            if not rl.isValid():
                print("FAIL (invalid raster):", path); continue
            if r.get("gray"):                                 # hillshade — soft, light, multiply-blended
                prov = rl.dataProvider()
                gr = QgsSingleBandGrayRenderer(prov, 1)
                st = prov.bandStatistics(1)
                ce = QgsContrastEnhancement(prov.dataType(1))
                ce.setContrastEnhancementAlgorithm(QgsContrastEnhancement.StretchToMinimumMaximum)
                ce.setMinimumValue(r.get("vmin", st.minimumValue))
                ce.setMaximumValue(r.get("vmax", st.maximumValue))
                gr.setContrastEnhancement(ce)
                rl.setRenderer(gr)
                bcf = rl.brightnessFilter()                   # lift + flatten so it's not a harsh grey
                bcf.setBrightness(r.get("brightness", 35)); bcf.setContrast(r.get("contrast", -25))
                rl.setOpacity(r.get("opacity", 0.5))
                if r.get("blend", "multiply") == "multiply":  # relief shows THROUGH the land colours
                    rl.setBlendMode(QPainter.CompositionMode_Multiply)
                rl.triggerRepaint()
                QgsProject.instance().addMapLayer(rl, False)
                grp = root.findGroup(r["group"]) or root.insertGroup(0, r["group"])
                grp.addLayer(rl); print("LOADED raster (hillshade soft):", r["name"]); continue
            shader = QgsRasterShader(); ramp = QgsColorRampShader()
            if "categories" in r:                             # discrete categorical raster
                items = [QgsColorRampShader.ColorRampItem(v, QColor(c), lab)
                         for v, c, lab in r["categories"]]
                ramp.setColorRampType(QgsColorRampShader.Exact)
                ramp.setColorRampItemList(items)
            else:                                             # continuous pseudocolour
                stats = rl.dataProvider().bandStatistics(1)
                lo = r.get("vmin", stats.minimumValue); hi = r.get("vmax", stats.maximumValue)
                cols = r["colors"]
                items = [QgsColorRampShader.ColorRampItem(lo + (hi - lo) * i / (len(cols) - 1),
                         QColor(c)) for i, c in enumerate(cols)]
                ramp.setColorRampType(QgsColorRampShader.Interpolated); ramp.setColorRampItemList(items)
            shader.setRasterShaderFunction(ramp)
            rl.setRenderer(QgsSingleBandPseudoColorRenderer(rl.dataProvider(), 1, shader))
            rl.triggerRepaint()
            QgsProject.instance().addMapLayer(rl, False)
            grp = root.findGroup(r["group"]) or root.insertGroup(0, r["group"])
            grp.addLayer(rl)
            print("LOADED raster:", r["name"])
        except Exception as e:
            print("raster style failed for", r["name"], "->", e)

    # IGN PNOA orthophoto (WMS) — faint backdrop for the work-area maps. Two variants:
    #   "PNOA ortho"        : TRUE COLOUR, very low opacity + high brightness (work maps)
    #   "PNOA ortho (grey)" : greyscale (kept hidden; optional for the habitats map)
    if ADD_PNOA_ORTHO:
        uri = ("crs=EPSG:25830&dpiMode=7&format=image/jpeg&"
               "layers=OI.OrthoimageCoverage&styles&url=https://www.ign.es/wms-inspire/pnoa-ma")
        # (name, greyscale?, opacity, brightness, contrast, visible-by-default?)
        DEFS = [("PNOA ortho",        False, 0.20, 60, -5,  True),
                ("PNOA ortho (grey)", True,  0.35, 20, -25, False)]
        grp = root.findGroup("0 BASEMAP") or root.insertGroup(0, "0 BASEMAP")
        for nm, grey, op, br, ct, vis in DEFS:
            try:
                old = next((l for l in QgsProject.instance().mapLayers().values() if l.name() == nm), None)
                if old:
                    QgsProject.instance().removeMapLayer(old.id())
                wl = QgsRasterLayer(uri, nm, "wms")
                if not wl.isValid():
                    print("PNOA WMS not reachable — skipped '%s' (check internet)." % nm); continue
                if grey:
                    wl.hueSaturationFilter().setSaturation(-100)
                bcf = wl.brightnessFilter(); bcf.setBrightness(br); bcf.setContrast(ct)
                wl.setOpacity(op)
                QgsProject.instance().addMapLayer(wl, False)
                node = grp.addLayer(wl)
                if node is not None:
                    node.setItemVisibilityChecked(vis)
                print("LOADED", nm)
            except Exception as e:
                print("PNOA WMS add failed for", nm, "->", e)

    # order the groups top→bottom per GROUP_ORDER (basemap ends at the bottom)
    for name in reversed(GROUP_ORDER):
        g = root.findGroup(name)
        if g is not None:
            root.insertChildNode(0, g.clone()); root.removeChildNode(g)
    print("load_maps: done.")

run()
