# HOW TO USE THE MAPS — a full walk-through
_Everything Claude has built lives as styled layers you load with one script. This covers loading them, reading them, adding context, and composing a print panel. Beginner-friendly._

---
## 1. Load all the maps (one step)
The reliable way (no editor needed): open QGIS, then **Plugins ▸ Python Console**. Click into the input line (the `>>>` prompt at the bottom) and paste:

```python
from pathlib import Path
p = '/Users/carltonfuturity/Developer/Github/landscape-2025/LANDSCAPE_for_Carlton/07_SCRIPTS/load_maps.py'
exec(compile(Path(p).read_text(), p, 'exec'))
```

Press Enter. In a few seconds the Layers panel (left) fills with grouped, styled layers. Re-running is safe.

_Editor alternative:_ Python Console ▸ **Show Editor** ▸ Open. If `load_maps.py` looks greyed-out, change the file-type dropdown at the bottom of the dialog to **Python Files (\*.py)** or **All files**, and browse to `LANDSCAPE_for_Carlton/07_SCRIPTS/`.

---
## 2. What loads (20 layers, in groups)
Each group is one analytical map. From the Layers panel you can tick a whole group on/off.

| Group | Layers | The argument |
|---|---|---|
| **3.1 CONTEXT** | National backdrop (Spain highlighted) | locates the work area nationally _(needs corridors + provinces to finish)_ |
| **3.3 NATURA 2000** | 18 protected sites by designation | the protected cores to reconnect (incl. Valcuerna) |
| **4.1 HYDROGRAPHY** | Watercourses + Valcuerna spine · Water bodies · Springs | the drainage skeleton |
| **4.2 GEOMORPHOLOGY** | Landforms (gypsum/mudstone badlands, saladas) | the physical substrate (your benchmark map) |
| **4.3 FLOW & EROSION** | Drainage network · Flow accumulation · Erosion (SPI) | where runoff + erosion concentrate |
| **4.4 HUMAN PRESSURE & BARRIERS** | Barriers · Crossing catalogue · Human-pressure zone | what fragments the corridor (14/16 crossings are open cuts) |
| **4.5 AGRICULTURAL MATRIX** | 9-class crop/veg matrix | the real agricultural fabric |
| **4.6 FOREST & NATURAL VEG** | 9-class MFE natural veg | real woody/scrub cover |
| **4.x CAÑADAS** | Vías pecuarias · Cañada × land cover | the public-land corridor spine |
| **5.1a HABITAT** | Lynx + rabbit habitat | where the species can live |
| **5.2 RESISTANCE & CORRIDOR** | Resistance surface · Least-cost corridor · Corridor swath | the modelled lynx corridor (92 km) |

---
## 3. Viewing tips
- **Turn groups on/off** with the checkbox next to the group name. Work on one map at a time.
- **Order matters:** the top layer draws on top. Drag groups up/down. For any map, put points/lines above fills (e.g. springs above water bodies).
- **See the legend/classes:** expand a layer (arrow) to see its colour classes and hectares/km labels.
- **A layer looks black?** That's a raw raster (like `dem_box`). Right-click ▸ Properties ▸ Symbology ▸ set "Min/Max". The `hillshade` raster already looks like 3-D relief.
- **Sanity check:** turn on 4.1 (Valcuerna spine) + 4.2 (gypsum badlands) + 5.2 (corridor). The corridor should thread the badlands/scrub and follow the Valcuerna. If layers don't line up, something's wrong — tell Claude.

---
## 4. Add context that isn't in the script
Some maps read better with a backdrop or a layer that lives in Sonya's vault, not in `03_PROCESSED`:
- **Hillshade** under 4.2 and 4.3: drag `01_DATA/DEM/hillshade.tif` in, put it at the bottom of the group, set the layer above it to ~60% opacity (Properties ▸ Transparency).
- **Towns + river + AOS frame** on 3.3: add Sonya's town/river layers from her vault drop when composing.
- **Orthophoto** for reference on any map: Plugins ▸ **QuickMapServices** ▸ add a satellite basemap (put at the very bottom).

---
## 5. Compose a print panel (the deliverable)
Do one as a test to validate the pipeline end-to-end.
1. Tick on the layers for one map (e.g. everything in 4.2 GEOMORPHOLOGY, plus hillshade).
2. **Project ▸ New Print Layout**, name it "Panel test".
3. In the layout: **Add Item ▸ Add Map**, drag a rectangle. It shows your current canvas.
4. Set scale: select the map item ▸ Item Properties ▸ Scale ▸ type e.g. `50000` (1:50,000) for the territorial maps.
5. **Add Item ▸ Add Scale Bar** and **Add North Arrow** (both required on every sheet).
6. **Add Item ▸ Add Legend** — it auto-lists visible layers; untick clutter in its properties.
7. **Layout ▸ Export as PDF/Image** at **300 dpi**. Save into `04_EXPORTS/`.

The panels are A0 vertical (three of them). Build each map, then arrange the finished maps onto the A0 sheet.

---
## 6. What's ready vs still pending
**Ready to view now:** all of §4 (4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.x), §5 (5.1a habitat, 5.2 corridor), and §3.3 Natura 2000 + the 3.1 backdrop.

**Still incomplete until you add the 3 remaining downloads:**
- **Admin boundaries** → finishes 3.1, 3.2, 3.3 (adds provinces/municipios/towns frame).
- **WWF corridor** → finishes 3.1, 3.2, 3.4.
- **SNCZI flood** → adds the flood overlay to 4.3.
(See `HOWTO_grab_remaining_data.md`. The DEM is done ✓.)
