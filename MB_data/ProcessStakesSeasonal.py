import numpy as np
import pandas as pd
import datetime as dt
import geopandas as gpd
# import rasterio
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
# from shapely.geometry import Point
import seaborn as seaborn
import glob
import rasterio
# import Uncertainties as unc


## set file paths, load data: 
#stake positions: 
stkpos = gpd.read_file('/Users/leahartl/Desktop/Jam2026/sommer/Pegel2026.geojson')
print(stkpos)
stkpos['name'] = stkpos['name'].astype(int)
# read "Pegelblaetter csv files"
fn = '/Users/leahartl/Desktop/Jam2026/sommer/pegelblätter/'
fls = glob.glob(fn+'/*.csv')

# make a df to sort the files and select:
df = pd.DataFrame(columns=['fln', 'stake'])
df['fln'] = fls
print(df)
# df['stake'] = df['fln'].str[58:-4]

df['stake'] = df['fln'].str.split('_').str[-1].str.strip('.csv')

#hacky workaround to replace string chars to ensure stake names are numeric
df['stake'] = df['stake'].str.replace('unten', '')
df['stake'] = df['stake'].str.replace('P', '')
df['stake'] = df['stake'].str.replace('2026', '30')
df['stake'] = df['stake'].str.replace('neu', '18')

df['stake'] = df['stake'].astype(int)
df = df.sort_values(by='stake')
print(df)

# only plot desired stakes

#df1 = df[~df['stake'].isin([0, 5, 6, 7, 8, 9, 13, 17, 182])]
df1 = df.copy()#[~df['stake'].isin([0, 5, 6, 7, 8, 9, 13, 17, 182])]
df1.index = df1.stake

# set year
yr = 2026

# prepare plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)

# set up line styles
LINE_STYLES = ['solid', 'dashed', 'dotted']#, 'dashdot', 'dotted']
NUM_STYLES = len(LINE_STYLES)

# deal with colors
my_cmap = ListedColormap(seaborn.color_palette('deep', 12).as_hex())
n = len(fls)
color = iter(my_cmap(np.linspace(0, 1, n)))


# get most recent coordinates
coords = pd.DataFrame(columns=['date', 'name', 'x', 'y'])
stks = []
abl = []
dates = []
xps = []
yps = []

for i, fl in enumerate(df1['fln'].values): 
    clr = next(color)
    dat = pd.read_csv(fl)
    dat['date'] = pd.to_datetime(dat['date'])
    dat.index = dat['date']

    stk = df1['stake'].values[i]
    #stks.append(stk)
    # abl.append()

    # get most recent x and y coordinates and gather in data frame
    # notnan = dat.dropna(subset=['x_pos', 'y_pos'],axis=0)
    #dates.append(notnan.index.values[-1])
    # xps.append(notnan.x_pos.values[-1])
    # yps.append(notnan.y_pos.values[-1])

    # get only current year
    sub = dat.loc[dat.index.year == yr]
    sub = sub[['stake_id', 'Abl. seit Herbst']]
    sub['Abl. seit Herbst'] = sub['Abl. seit Herbst'].astype(float)
    df1.loc[stk, 'abl_cmice'] = sub['Abl. seit Herbst'].values[-1]

    ax.plot(sub.index.values, sub['Abl. seit Herbst'].values, label=stk, color=clr, linestyle=LINE_STYLES[i%NUM_STYLES])
    ax.plot(sub.index.values, sub['Abl. seit Herbst'].values, marker='o', color=clr, linestyle=LINE_STYLES[i%NUM_STYLES])

ax.set_xticks(pd.date_range(start=str(yr)+'/6/1', periods=4, freq='ME'))
# set formatter
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax.set_ylabel('Ablation [cm Eis]')
ax.set_xlabel('Datum')
ax.set_ylim([0, 700])
ax.set_title('Ablationsverlauf an den Pegeln')
ax.grid(axis='y')
ax.legend()

print(df1)

stkpos = stkpos.merge(df1, left_on='name', right_index=True)
stkpos['abl_m_we'] = stkpos['abl_cmice']/100 * 900 /1000
stkpos['snowheight'] = 0
print(stkpos)

fig.savefig('/Users/leahartl/Desktop/Jam2026/sommer/seasonalablation_stakes'+str(yr)+'.png', dpi=200, bbox_inches='tight')
# plt.show()
# stop
# coords['date'] = dates
# coords['name'] = stks
# coords['X_coord'] = xps
# coords['Y_coord'] = yps
# # coords['mb_cm_ice_floating'] = np.nan
# # coords['mb_we_fixed_date'] = np.nan

# stakedata = pd.read_csv('/Users/leahartl/Desktop/Jam2025/sommer/summary2025/Sheet 2-Table 1.csv')

# coords = coords.merge(stakedata, left_on='name', right_on='P')
# coords = coords[['name', 'X_coord', 'Y_coord',  'mm_WE_nosnow_floating',  'mm_we_withsnowcorr_300kgm_3_fixed', 'snowheight_cm']]
# coords['snow_density_kgm3'] = 300
# gdf = gpd.GeoDataFrame(
#     coords, geometry=gpd.points_from_xy(coords.X_coord, coords.Y_coord), crs="EPSG:4326"
# )

# Open the DEM raster
raster = '/Users/leahartl/Desktop/JAM/JamDEM201718.tif'
src = rasterio.open(raster)
print(src.crs)
# reproject points to match raster
gdf = stkpos.to_crs(src.crs)

new_coords = gdf.get_coordinates().values
# extract the raster values
gdf['Z_value'] = [x[0] for x in src.sample(new_coords)]
gdf = gdf.to_crs(epsg=4326)
gdf['X_coord'] = gdf.geometry.x
gdf['Y_coord'] = gdf.geometry.y
# save to file:
gdf.to_file('/Users/leahartl/Desktop/Jam2026/sommer/Pegel2026_elev_abl.geojson')
print(gdf)
# open file that has elevation data (extracted from 2017/18 DEM file), rename cols and resave fro excl update
# gdf2 = gpd.read_file('/Users/leahartl/Desktop/Jam2025/sommer/Pegel2025.geojson')
# print(gdf2)

forcsv = gdf[['name', 'X_coord', 'Y_coord', 'Z_value', 'abl_m_we']]#'mm_WE_nosnow_floating', 'mm_we_withsnowcorr_300kgm_3_fixed']]
#forcsv = forcsv.rename(columns={"ele1": "Z_value", "mm_WE_nosn": "mm_WE_nosnow_floating", "mm_we_with": "mm_we_withsnowcorr_300kgm_3_fixed"})
print(forcsv)
forcsv.to_csv('/Users/leahartl/Desktop/Jam2026/sommer/stakes_2026_for_table.csv')
plt.show()




