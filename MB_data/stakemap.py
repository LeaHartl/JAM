#! /usr/bin/env python3
import numpy as np
import pandas as pd
import geopandas as gpd
import json
import matplotlib.pyplot as plt
# import seaborn as seaborn
from matplotlib.colors import ListedColormap
import matplotlib.dates as mdates
# from geopandas import GeoDataFrame
from shapely.geometry import Point
import rasterio as rio
import rioxarray as rxr
from rasterio.plot import show


# set file paths:
# stakes with elevation and WW: 
stakes = gpd.read_file('/Users/leahartl/Desktop/Jam2025/sommer/Pegel_Jam_2025_ele.shp')
stakes['melt'] = (stakes['mm_we_with']*-1).round(decimals=0).astype(int)
# contourlines 2017/18 DEM: 
contours = gpd.read_file('/Users/leahartl/Desktop/JAM/contour_poly_201718_50m.shp')

raster = '/Users/leahartl/Desktop/JAM/JamDEM201718.tif'


# make a plot:
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
# data_gdf.plot(ax=ax, column='WW', legend=True, label='WW [mm w.e.]')


DEM = rxr.open_rasterio(raster)
print(DEM.shape)
CS = DEM.squeeze().plot.contour(ax=ax, colors='grey', levels=np.arange(2000, 3000, 50), linewidths=0.5)
ax.clabel(CS, inline=1, fontsize=10)

        # ax.contour(DEM.squeeze())


outline2023 = gpd.read_file('/Users/leahartl/Desktop/Jam2023/outlines/Jamtalferner/jam22_sentinel_okt23.shp')
outline2023.to_crs(epsg=31254, inplace=True)
outline2023.boundary.plot(ax=ax, color='k')

# contours.to_crs(epsg=31254, inplace=True)
# contours.boundary.plot(ax=ax, linewidths=0.2, color='grey')

stakes.to_crs(epsg=31254, inplace=True)
stakes.plot(column='melt', ax=ax, cmap= 'Reds_r', legend=False, label='WW [mm w.e.]', edgecolor='k')

for x, y, label, nm in zip(stakes.geometry.x, stakes.geometry.y, stakes['melt'], stakes['name']):
    # print (nm)
    # stop
    if (nm == 1):
        print('yes')
        xytext = (400, 8)
    if (nm == 11):
        xytext = (-30, 8)
    else:
        xytext = (-15, 8)
    
    ax.annotate(label, xy=(x, y), xytext=xytext, textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.1", fc="lightgrey", alpha=0.9))



# ax.set_xlim([10.142, 10.186])
# ax.set_ylim([46.848, 46.868])

ax.set_xlim([-14500, -11300])
ax.set_ylim([189900, 192000])
ax.set_title('Annual point mass balance 2024/25 (fixed date, mm w.e.)')

fig.savefig('/Users/leahartl/Desktop/Jam2025/sommer/karte_annual_fixedate.png', bbox_inches='tight', dpi=200)

plt.show()

# fig.savefig('sondierungen_20250426.png', bbox_inches='tight', dpi=200)

