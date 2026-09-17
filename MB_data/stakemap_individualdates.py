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
import glob


# set some file paths:
# stakes with elevation and WW: 
stakesAnnual = gpd.read_file('/Users/leahartl/Desktop/Jam2025/sommer/Pegel2025.geojson')
stakesAnnual['melt'] = (stakesAnnual['mm_we_withsnowcorr_300kgm_3_fixed']/10).round(decimals=0).astype(int)
# contourlines 2017/18 DEM: 
contours = gpd.read_file('/Users/leahartl/Desktop/JAM/contour_poly_201718_50m.shp')
raster = '/Users/leahartl/Desktop/JAM/JamDEM201718.tif'

# get data for individual readings:
# read "Pegelblaetter csv files"
fn = '/Users/leahartl/Desktop/Jam2025/Pegelblaetter/'
fls = glob.glob(fn+'/*.csv')

# make a df to sort the files and select:
df = pd.DataFrame(columns=['fln', 'stake'])
df['fln'] = fls

df['stake'] = df['fln'].str[58:-4]
df['stake'] = df['stake'].str.replace('unten', '')
# this is a workaround to have 18_neu as a numeric value (182)
df['stake'] = df['stake'].str.replace('_neu', '2')
df['stake'] = df['stake'].astype(int)
df = df.sort_values(by='stake')
print(df)

# only plot desired stakes
# fix 18 neu (182) in 2026
df1 = df[~df['stake'].isin([0, 5, 6, 7, 8, 9, 13, 17, 182])]

print(df1)
# set year
yr = 2025


collect = []

for i, fl in enumerate(df1['fln'].values): 

    dat = pd.read_csv(fl)
    dat['date'] = pd.to_datetime(dat['date'])
    dat.index = dat['date']

    stk = df1['stake'].values[i]

    # get only current year
    sub = dat.loc[dat.index.year == yr]
    sub = sub[['stake_id', 'Abl. seit Herbst', 'x_pos', 'y_pos']]
    sub['Abl. seit Herbst'] = sub['Abl. seit Herbst'].astype(float)

    # interpolate missing coordinate values to nearest measurement:
    sub['x_pos'] = sub['x_pos'].ffill()
    sub['y_pos'] = sub['y_pos'].ffill()

    sub['x_pos'] = sub['x_pos'].bfill()
    sub['y_pos'] = sub['y_pos'].bfill()

    # collect data from all stakes:
    collect.append(sub)

df_all = pd.concat(collect)
print(df_all)


# make a plot for each day of measurements:
def makeplots(df_all, raster):

    outline2023 = gpd.read_file('/Users/leahartl/Desktop/Jam2023/outlines/Jamtalferner/jam22_sentinel_okt23.shp')
    outline2023.to_crs(epsg=31254, inplace=True)
    # make sure crs is ok!
    DEM = rxr.open_rasterio(raster)

    for day in df_all.index.unique():
        data = df_all.loc[df_all.index == day]
        print(data)

        stakes = gpd.GeoDataFrame(
                data, geometry=gpd.points_from_xy(data.x_pos, data.y_pos), crs="EPSG:4326"
                )
        stakes.to_crs(epsg=31254, inplace=True)
        stakes['melt_cm'] = (stakes['Abl. seit Herbst']*-1).round(decimals=0).astype(int)
    
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        outline2023.boundary.plot(ax=ax, color='k')
        CS = DEM.squeeze().plot.contour(ax=ax, colors='grey', levels=np.arange(2000, 3000, 50), linewidths=0.5)
        ax.clabel(CS, inline=1, fontsize=10)

        stakes.to_crs(epsg=31254, inplace=True)
        stakes.plot(ax=ax, color='red', legend=False, label='Eis [cm]', edgecolor='k')

        ax.set_xlim([-14500, -11300])
        ax.set_ylim([189900, 192000])
        ax.set_title('Cumuulative ice surface change, '+str(yr-1)+' Oct 01 -'+day.strftime('%Y %b %d')+' [cm]')

        for x, y, label, nm in zip(stakes.geometry.x, stakes.geometry.y, stakes['melt_cm'], stakes['stake_id']):
            if (nm == 1):
                #print('yes')
                xytext = (400, 8)
            if (nm == 11):
                xytext = (-30, 8)
            else:
                xytext = (-15, 8)
            
            ax.annotate(label, xy=(x, y), xytext=xytext, textcoords="offset points",
                bbox=dict(boxstyle="round,pad=0.1", fc="lightgrey", alpha=0.9))



        fig.savefig('/Users/leahartl/Desktop/Jam2025/sommer/figures_ablesungen/karte_CM_'+day.strftime('%Y_%m_%d')+'_COR.png', bbox_inches='tight', dpi=200)

        # plt.show()

        # stop

makeplots(df_all, raster)
# fig.savefig('sondierungen_20250426.png', bbox_inches='tight', dpi=200)

