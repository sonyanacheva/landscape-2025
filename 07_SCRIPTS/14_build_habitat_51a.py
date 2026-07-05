#!/usr/bin/env python3
# 14_build_habitat_51a.py
# Build the 5.1a lynx + rabbit habitat layer by reclassifying the 4.5 land-cover base
# into the two-species logic. The Iberian lynx needs scrub/forest COVER; the rabbit (its
# prey base) needs the scrub-grassland ECOTONE + open foraging. Where both meet (grazed
# scrub / pasto arbustivo) is the optimal cell — the "visited, not just lived-in" argument.
# Terrain/human-pressure are secondary modifiers (noted; cover type dominates habitat).
#
# Run headless. Output: 03_PROCESSED/habitat_51a.fgb
import os, warnings
import geopandas as gpd
warnings.filterwarnings('ignore')

AGRI = os.environ['AGRI']
OUT  = os.environ.get('OUT', 'habitat_51a.fgb')

HAB = {
    'Grazed scrub / pasto arbustivo': 'Lynx + rabbit optimal (ecotone)',
    'Scrub (matorral)':               'Lynx cover (scrub/forest)',
    'Forest':                         'Lynx cover (scrub/forest)',
    'Pasture (open)':                 'Rabbit foraging (open)',
    'Arable dryland':                 'Matrix (permeable)',
    'Woody crops':                    'Matrix (permeable)',
    'Arable irrigated':               'Matrix (hostile)',
    'Horticulture/greenhouse':        'Matrix (hostile)',
    'Non-agricultural':               'Non-habitat',
}
g = gpd.read_file(AGRI)
g['habitat'] = g['agri_class'].map(HAB).fillna('Non-habitat')
g[['agri_class', 'habitat', 'ha', 'geometry']].to_file(OUT, driver='FlatGeobuf', layer='habitat')

order = ['Lynx + rabbit optimal (ecotone)', 'Lynx cover (scrub/forest)', 'Rabbit foraging (open)',
         'Matrix (permeable)', 'Matrix (hostile)', 'Non-habitat']
s = g.groupby('habitat')['ha'].sum()
print('=== 5.1a Lynx + rabbit habitat (ha) ===')
for k in order:
    if k in s.index:
        print(f'{k:34} {s[k]:>11,.0f} ha')
hab = s.get('Lynx + rabbit optimal (ecotone)', 0) + s.get('Lynx cover (scrub/forest)', 0)
print(f'\nEffective lynx habitat (cover + ecotone): {hab:,.0f} ha')
