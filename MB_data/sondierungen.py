#! /usr/bin/env python3
import numpy as np
import pandas as pd
import fiona
import geopandas as gpd
import json
import matplotlib.pyplot as plt
# import seaborn as seaborn
from matplotlib.colors import ListedColormap
import matplotlib.dates as mdates
# from geopandas import GeoDataFrame
from shapely.geometry import Point
import gpxpy
import gpxpy.gpx

# set file name:
# gpx file from lea's garmin inreach:
gpx_file = '/Users/leahartl/Desktop/Jam2025/winter/GPS_alles/explore.gpx'
gpx_martin = '/Users/leahartl/Desktop/Jam2025/winter/GPS_Martin/Wegpunkte_26-APR-25.gpx'

# parse GPX waypoints for day inlcuding and after a specific day. return as geodataframe:
#[easier to export as .shp from Qgis!]
def convertGPX(fn, date, wer):
    # open and parse gpx file
    f = open(fn, 'r')
    gpx = gpxpy.parse(f)

    # convert to DF:
    nms = []
    tms = []
    lat = []
    lon = []
    for waypoint in gpx.waypoints:
        # uncomment for reality check
        # print('waypoint {0} -> ({1},{2},{3})'.format(waypoint.name, waypoint.time, waypoint.latitude, waypoint.longitude))
        nms.append(waypoint.name)
        tms.append(waypoint.time)
        lat.append(waypoint.latitude)
        lon.append(waypoint.longitude)

    df = pd.DataFrame(columns=['name', 'time', 'lat', 'lon'])
    df['name'] = nms
    df['time'] = tms
    df['lat'] = lat
    df['lon'] = lon

    df.index = pd.to_datetime(df['time'])

    # extract data for specific day:
    day = date
    subset = df.loc[df.index>=day]
    # make geometry
    subset['geometry'] = gpd.points_from_xy(subset.lon, subset.lat, crs="EPSG:4326")
    # drop extry colume
    subset.drop(columns=['time'], inplace=True)
    subset['wer'] = wer

    return (subset)

# get gpx data:
gpxdf = convertGPX(gpx_file, '2025-04-26', 'Lea')
gpxdf_Ma = convertGPX(gpx_martin, '2025-04-26', 'Martin')


both = pd.concat([gpxdf, gpxdf_Ma], ignore_index=False)
print(both)

# write to csv if needed
# gpxdf.to_csv('GPS_Lea_sondierungen_20250426.csv')
# both.to_csv('GPS_LeaMartin_sondierungen_20250426.csv')


# load csv file - exported from excel/numbers, contains gps waypoint names and snow depth from probing:
csvfile = '/Users/leahartl/Desktop/Jam2025/winter/GPS_LeaMartin_sondierungen_20250426_SH.csv'
data = pd.read_csv(csvfile)
data.drop(columns='geometry', inplace=True)

data_gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.lon, data.lat), crs="EPSG:4326")
data_gdf['WW'] = data_gdf['SH']*10*0.369
print(data_gdf)

# save to new shape file
data_gdf.to_file("sondierungen_20250426.shp")
data_gdf.loc[data_gdf['name']=='s01 18'].to_file("schacht_20250426.shp")


# make a plot:
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
data_gdf.plot(ax=ax, column='WW', legend=True, label='WW [mm w.e.]')

outline = gpd.read_file('/Users/leahartl/Desktop/Jam2023/outlines/Jamtalferner/jam22_sentinel_okt23.shp')
outline.to_crs(epsg=4326, inplace=True)
outline.boundary.plot(ax=ax)

contours = gpd.read_file('/Users/leahartl/Desktop/Jam2025/ContourPoly_201718.shp')
contours.to_crs(epsg=4326, inplace=True)
contours.boundary.plot(ax=ax, linewidths=0.2, color='grey')

data_gdf.loc[data_gdf['name']=='s01 18'].plot(ax=ax, marker='*', color='red', markersize=24)

ax.set_xlim([10.14, 10.19])
ax.set_ylim([46.848, 46.868])


plt.show()

fig.savefig('sondierungen_20250426.png', bbox_inches='tight', dpi=200)

