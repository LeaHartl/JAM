#! /usr/bin/env python3
import numpy as np
import pandas as pd
import geopandas as gpd
import json
import matplotlib.pyplot as plt
# import seaborn as seaborn
from matplotlib.colors import ListedColormap
import matplotlib.dates as mdates
from matplotlib.lines import Line2D

import rasterio as rio
import rioxarray as rxr



# DEM
# raster = '/Users/leahartl/Desktop/JAM/JamDEM201718.tif'
# src = rio.open(raster)
# sondierungen: 
points = gpd.read_file('/Users/leahartl/Desktop/Jam2025/winter/sondierungen_20250426.shp')
print(points)
# file with elevation zones for the current glacier area. use the same outline as for the annual MB
# zones = gpd.read_file('/Users/leahartl/Desktop/JAM/Jamtal Outline Anne/2024/Jam_outline_2024_zones.shp')

outline = gpd.read_file('/Users/leahartl/Desktop/JAM/Jamtal Outline Anne/2024/Jam_outline_24.shp')
outline = outline.to_crs(points.crs)

contours = gpd.read_file('/Users/leahartl/Desktop/JAM/contour_poly_201718_50m.shp')
contours = contours.to_crs(points.crs)

# make a plot:
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
points.plot(ax=ax, column='SH', label='SH (cm)', legend=True, 
            legend_kwds={'location':'bottom', 'shrink':0.8, 'label':'Schneehöhe [cm]'})

outline.boundary.plot(ax=ax, color='k', linewidth=1)
contours.boundary.plot(ax=ax, colors='grey', linewidth=0.5)

# contours = gpd.read_file('/Users/leahartl/Desktop/Jam2025/ContourPoly_201718.shp')
# contours.to_crs(epsg=4326, inplace=True)
# contours.boundary.plot(ax=ax, linewidths=0.2, color='grey')

points.loc[points['name']=='s01 18'].plot(ax=ax, marker='*', color='red', markersize=24)

# ax.set_xlim([10.14, 10.19])
# ax.set_ylim([46.848, 46.868])

ax.set_xlim([-15000, -11000])
ax.set_ylim([189500, 192300])


Schacht = Line2D([0], [0], marker='*', linestyle='None', label='Schachtposition', color='red', markersize=8)
patchOutline = Line2D([0], [0], label='Gletschergrenze 2024', color='k', linewidth=1, linestyle='-')
hls = [Schacht, patchOutline]
fig.legend(handles=hls, loc='lower center', bbox_to_anchor=(0.4, 0.25), ncol=2)


plt.show()

fig.savefig('/Users/leahartl/Desktop/Jam2025/winter/sondierungen_20250426.png', bbox_inches='tight', dpi=200)

