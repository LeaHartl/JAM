import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
from matplotlib.gridspec import GridSpec

import rasterio as rio
import rioxarray as rxr
import math
# script to process jamtalferner annual and summer mass balance. 
# adapted from Andrea F's matlab file by Lea H. & Anne H.(2025)

# current year:
curyear = 2026
# DEM file path:
raster = '/Users/leahartl/Desktop/JAM/JamDEM201718.tif'
# file with timeseries data:
ts_fn = '/Users/leahartl/Desktop/JAM/Jam_mb_timeseries.csv'
# file with winter MB data: 
winter_fn = '/Users/leahartl/Desktop/Jam2026/winter/winterbilanz_jam2026.csv'
#set overall winter balance value from winter files:
bwi = 0.918 # m w.e.

# outputfolder - save plots and tables to this directory
# make sure this directory exits
output = '/Users/leahartl/Desktop/Jam2026/results/'
# ouline directory - path to the folder with the MB geojson files:
outline_dir = '/Users/leahartl/Desktop/Jam2026/sommer/MB_shapes/'
# suffixes of geojson files for the different glacier parts
# this sets up the code to loop through the different glacier parts
sufs = ['_all', '_west', '_central', '_east']
# file with stake data:
stakesfn = '/Users/leahartl/Desktop/Jam2026/sommer/Pegel2026_elev_abl.geojson'
# anme of column in stakes file which contains ablation in m w.e.
param = 'abl_m_we'
# main outline - based on orthophoto of previous year
zones1fn = '/Users/leahartl/Desktop/Jam2026/sommer/MB_shapes/2026_all.geojson'

zones1 = gpd.read_file(zones1fn)
# reproject to crs with true area (don't use lat/lon to compute area)
print(zones1.crs)
zones1 = zones1.to_crs(epsg=31254)

#----------------------------#
# function to make the map figure
def makeMB_Map(zones, suffix, curyear, stakesfn, param, raster):
    cmap = 'RdYlBu'#'coolwarm_r'
    # adjust min, max values here if needed!
    vmin = -6.50
    vmax = 1.00

    # convert to m
    zones['mb'] = zones['mb']/100

    DEM = rxr.open_rasterio(raster)

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    divnorm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter = 0, vmax=vmax)

    zones.plot(ax=ax, column='mb', alpha=1, cmap=cmap, norm=divnorm, legend=False, zorder=1)
    CS = DEM.squeeze().plot.contour(ax=ax, colors='grey', levels=np.arange(2000, 3000, 50), linewidths=0.5)
    ax.clabel(CS, inline=1, fontsize=10)

    # plot stake values for the main run:
    if suffix == '_all':
        # load stakes:
        # stakes file with elevation and WW:
        stakes = gpd.read_file(stakesfn)
        # check that values have the right unit and are negative!
        stakes['melt'] = stakes[param].round(decimals=2)*-1 
        stakes.to_crs(epsg=31254, inplace=True)
        stakes.plot(column='melt', ax=ax, cmap=cmap, norm=divnorm, legend=False, label='WW [m w.e.]', edgecolor='k')

        for x, y, label, nm in zip(stakes.geometry.x, stakes.geometry.y, stakes['melt'], stakes['name']):
            if (nm == 2):
                xytext = (-30, 6)
            else:
                xytext = (-15, 8)
    
            ax.annotate(label, xy=(x, y), xytext=xytext, textcoords="offset points",
                bbox=dict(boxstyle="round,pad=0.1", fc="lightgrey", alpha=0.9))

    ax.set_xlim([-14500, -11300])
    ax.set_ylim([189900, 192000])

    ax.set_title('Spezifische Massenbilanz (m w.e.), 1. Oktober '+str(curyear-1)+' - 30. September '+str(curyear))
    ax.set_xlabel('')
    ax.set_ylabel('')

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.82, 0.13, 0.02, 0.7])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=divnorm)
    cbar = fig.colorbar(sm, cax=cbar_ax)
    cbar.set_label('m w.e.')
    cbar.ax.set_yscale('linear')

    fig.savefig(output+'MB_'+str(curyear)+'_map'+suffix+'.png', bbox_inches='tight', dpi=200)

# function to make the tables
def makeMBTables(dataS, sumbalance, bquer, bw, bs, suffix, winter_fn):
    # load and add winter balance for the main run:
    if len(suffix) == 0:
        # load winter MB data file: 
        dataW = pd.read_csv(winter_fn, index_col=0)

        #Höhenstufe,Fläche,Anzahl_Sondierungen,Mittlere_Schneehöhe_m,b_wi_m,Bilanz_m3,Fläche_m2
        data = dataS.merge(dataW, left_on='elev', right_on='Höhenstufe')
        data = data[['Höhenstufe', 'Fläche', 'balance_m3', 'b_m', 'b_wi_m']]
        #data.rename(columns={'b_wi_m':'b_wi'})

        data['b_so_m'] = -1*data['b_wi_m'] + data['b_m']

        # for table:
        fortable = data[['Höhenstufe', 'Fläche', 'balance_m3', 'b_m', 'b_wi_m', 'b_so_']]

        dfZones = pd.DataFrame(columns=['Höhenstufe', 'Fläche_km2', 'balance_Bm3', 'b_m', 'b_wi_m', 'b_so_m'])
        dfZones.loc[0, 'Höhenstufe'] = np.nan
        dfZones.loc[0, 'Fläche_km2'] = data['Fläche'].sum()*1e-6
        dfZones.loc[0, 'balance'] = sumbalance
        dfZones.loc[0, 'b'] = bquer
        dfZones.loc[0, 'b_wi'] = bw
        dfZones.loc[0, 'b_so'] = bs

        fortable = pd.concat([fortable, dfZones])
        # print(fortable)

        fortable['Fläche'] = (fortable['Fläche']*1e-6).astype(float).round(decimals=3)
        fortable['balance'] = (fortable['balance']*1e-3).astype(float).round(decimals=3)
        fortable[['b_m', 'b_wi', 'b_so']] = fortable[['b', 'b_wi', 'b_so']].astype(float).round(decimals=0).astype(int)


    # for sub-parts only use annual balance:
    else:
        data = dataS
        data = data.rename(columns={'area': 'Fläche', 'elev': 'Höhenstufe'})
        fortable = data[['Höhenstufe', 'Fläche', 'balance_m3', 'b_m']]

        dfZones = pd.DataFrame(columns=['Höhenstufe', 'Fläche', 'balance_m3', 'b_m'])
        dfZones.loc[0, 'Höhenstufe'] = np.nan
        dfZones.loc[0, 'Fläche'] = data.Fläche.sum()
        dfZones.loc[0, 'balance_m3'] = sumbalance
        dfZones.loc[0, 'b_m'] = bquer

        fortable = pd.concat([fortable, dfZones])
        # print(fortable)

        fortable['Fläche_km2'] = (fortable['Fläche']*1e-6).astype(float).round(decimals=3)
        fortable['balance*1e-3'] = (fortable['balance_m3']*1e-3).astype(float).round(decimals=3)
        fortable['b_m'] = fortable['b_m'].round(decimals=3).astype(int)

    print(fortable.to_latex(index=False))
    fortable.to_latex(output+'table_MB'+suffix+'.txt', index=False)
    fortable.to_csv(output+'table_MB'+suffix+'.csv', index=False)

    return(fortable)

# make the plot of hypsometry and b y elevation zones for the report
def makeMBFig_main(data, sumbalance, bquer, bw, bs, suffix):
    # drop nan line: 
    data = data.dropna()
    print(data)

    # ============ PLOT
    fig, ax = plt.subplots(1,2, figsize=(8, 8), sharey=True)
    ax = ax.flatten()
    # =========== AX 1
    # PLOT AREA on AX 1
    ax[0].barh(data.Höhenstufe.values, data.Fläche.values, 45, align='center', linewidth=1, alpha=1, color='grey')
    # set x axis properties
    ax[0].set_xlim(0, .4)
    ax[0].set_xticks(np.arange(0, 0.4, 0.1))
    ax[0].set_xlabel('Fläche [km$^2$]', fontsize=12)
    # plt.show()

    # # set y axis properties
    # ax[0].set_yticks(data.Höhenstufe.values)
    ax[0].set_ylabel('Höhenstufen [m.a.s.l.]', fontsize=12)
 
    # # ========= AX 2
    ax[1].yaxis.tick_right()
    ax[1].yaxis.set_label_position('right')
    # PLOT MB on ax2
    ax[1].plot(data.b.values, data.Höhenstufe.values, 'k', linewidth=2, label='spezifische Massenbilanz '+str(curyear-1)+'/'+str(curyear))
    ax[1].plot(data.b_wi.values, data.Höhenstufe.values, 'b', label='spezifische Wintermassenbilanz')
    ax[1].plot(data.b_so.values, data.Höhenstufe.values, 'r', label='spezifische Sommermassenbilanz')
    # # set x axis properties
    ax[1].set_xlabel('Massenbilanz [m w.e.]', fontsize=12)
    ax[1].grid('both')

    # PLOT a 0 LINE
    ax[1].axvline(0, color='k', linestyle='dashed')

    # # Plot the Legend
    # # plot the bar plot also on the ax2 but with 0 values just for the legend
    ax[1].barh(0, 0, 0, align='center', linewidth=1, alpha=1, color='grey', label='Fläche der Höhenstufen')
    ax[1].legend(bbox_to_anchor=(-0.7, 1), loc=2, prop={'size': 10})
    # remove white space
    plt.subplots_adjust(wspace=0, hspace=0)

    fig.savefig(output+'MB_'+str(curyear)+'_elevationzones'+suffix+'.png', dpi=200, bbox_inches='tight')

# plot the individual pieces of the glacier (like Vernagtferner reports)
def makeMBPlot_v2(zones, zones1, data, sumbalance, bquer, sumstats, suffix):
    # drop last line
    data = data.dropna()

    # ============ PLOT
    fig = plt.figure(figsize=(6, 7))

    gs = GridSpec(2, 1, height_ratios=[1, 4])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    zones1.dissolve(by='elev').plot(ax=ax1, color='grey')
    zones.dissolve(by='elev').plot(ax=ax1, color='red')

    ax1.set_xlim([-14500, -11200])
    ax1.set_ylim([189900, 192000])
    
    # ax.set_title('Massenbilanz (m w.e.), 1. Oktober 2024 - 30. September 2025')
    ax1.set_xticks([])
    ax1.set_yticks([])

    # =========== AX 1
    # PLOT AREA on AX 1
    ax2.barh(data.Höhenstufe.values, data.Fläche.values, 45, align='center', linewidth=1, alpha=1, color='grey', label='Fläche [km$^2$]')
    # # set x axis properties
    ax2.set_xlim(0.4, 0)
    ax2.legend(loc='lower left')
    ax2.yaxis.tick_right()
    ax2.set_xlabel('Fläche [km$^2$]', fontsize=12, color='grey')

    ax22 = ax2.twiny()
    ax22.plot(data.balance*1e-2, data.Höhenstufe.values, linewidth=1, alpha=1, color='k',label='B [10$^5$ m$^3$]')
    ax22.plot(data.b*1e-3, data.Höhenstufe.values, linewidth=1, alpha=1, color='r', label='b [m w.e.]')
    ax22.legend()
    ax22.set_xlabel('B [10$^5$ m$^3$], b [m w.e.]', fontsize=12)
    ax22.set_ylabel('Höhenstufen [m.a.s.l.]', fontsize=12)
    ax22.yaxis.set_label_position('right')
    ax22.yaxis.tick_right()
    ax22.set_ylim(2420, 3120)
    ax22.set_xlim(-7, 0)

    fig.savefig(output+'MB_2025_elevationzones_v2'+suffix+'.png', dpi=200, bbox_inches='tight')

# make stripes plot and add new data to the csv file
def StripesPlot(sumstats, curyear, ts_fn):
    # get the older data
    data = pd.read_csv(ts_fn, sep=',', decimal='.')

    st = pd.DataFrame(columns=data.columns)
    st.loc[0, :] = sumstats

    data = pd.concat([data, st])
    data[['ba', 'b', 'bw', 'bs']] = data[['ba', 'b', 'bw', 'bs']].astype(float).round(decimals=0).astype(int)
    data[['Sc', 'Sa', 'S', 'B']] = data[['Sc', 'Sa', 'S', 'B']].astype(float).round(decimals=3)
    data[['Ba']] = data[['Ba']].astype(float).round(decimals=1)

    data.to_csv(output+'Jam_mb_timeseries_'+str(curyear)+'.csv')
    print(data)
    print(data[['S', 'B', 'b', 'bs', 'bw', 'Sc/S']].mean())

    yr = data['Year'].str.strip().str[-4:].astype(int).values

    mb = data.b
    mb_w = data[['Year2', 'bw']]
    mb_s = data[['Year2', 'bs']]

    # make figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.set_xlim(1988, curyear+1)
    ax.bar(yr, mb_w.bw, color='blue', alpha=0.4, label='b_w')
    ax.bar(yr, mb_s.bs, color='red', alpha=0.4, label='b_s')
    ax.bar(yr, mb, color='k', label='b')
    ax.legend()
    # ax.bar(yr, mb, color='k')
    ax.set_xlabel('Year')
    ax.set_ylabel('Spezifische Massenbilanz (mm w.e.)')
    ax.grid(axis='y')
    ax.set_facecolor('lightgrey')
    ax.set_title('Jamtalferner (1989-'+str(curyear)+')')

    fig.savefig(output+'Jam_stripes_'+str(curyear)+'.png', bbox_inches='tight', dpi=200)

# compute MB data: 
def mainMassBalance(zones, bw):
    # add area
    zones['area'] = zones.geometry.area

    zonmin = zones['elev'].min()
    zonmax = zones['elev'].max()

    # --- total area ----
    total_area = np.sum(zones.geometry.area)
    # number of zones
    zone_nr = len(zones['elev'].unique())

    # make data frame for the zones
    summer_df = zones[['mb', 'elev', 'area']]
    # summer_df = summer_df.rename(columns={'elev': 'Höhenstufe', 'area': 'Fläche'})
    summer_df = summer_df.sort_values(by='elev')
    summer_df['balance_m3'] = summer_df['area'] * summer_df['mb'] / 100.0 # m³ - mb in zones file is in cm!!

    # compute some summary values
    datmax = summer_df.shape[0]
    sumbalance = summer_df['balance_m3'].sum()
    bquer = (sumbalance / total_area) * 1000.0  # mm

    # --- Akkumulation / Ablation ---
    acc_mask = summer_df['balance_m3'] > 0
    abl_mask = summer_df['balance_m3'] < 0
    no_mask = summer_df['balance_m3'] == 0

    accarea = np.sum(summer_df['area'][acc_mask])
    ablarea = np.sum(summer_df['area'][abl_mask])
    noarea = np.sum(summer_df['area'][no_mask])

    accb = np.sum(summer_df['balance_m3'][acc_mask])
    ablb = np.sum(summer_df['balance_m3'][abl_mask])
    nob = np.sum(summer_df['balance_m3'][no_mask])

    # all in mm!
    bquerabl = (ablb / ablarea) * 1000.0 if ablarea != 0 else float('nan')
    bqueracc = (accb / accarea) * 1000.0 if accarea != 0 else float('nan')
    SczuS = accarea / total_area if total_area != 0 else float('nan')

    # Define zones
    zone_bins = np.arange(zones['elev'].min(), zones['elev'].max()+50, 50)

    # Aggregate sums by zone
    zone_stats = summer_df.groupby('elev', as_index=False).agg({'balance_m3': 'sum', 'area': 'sum'})

    # Reindex to include all class zones (some may be missing in data)
    zone_stats = zone_stats.set_index('elev').reindex(zone_bins, fill_value=0).reset_index()

    # Compute mean balance (mm)
    zone_stats['b_m'] = (zone_stats['balance_m3'] / zone_stats['area']) #* 1000.0
    print(zone_stats)
    # summer balance: 
    bs = bquer - bw

    sumstats = [str(curyear-1)+'/'+str(curyear), accarea/10**6, accb/10**3, bqueracc, ablarea/10**6, ablb/10**3, bquerabl,
            curyear, total_area/10**6, sumbalance/10**6, bquer, bs, bw, '****', SczuS]


    return(zone_stats, sumbalance, sumstats, bs, bquer)


# ------ run the functions -------_

for suffix in sufs:
    # set additional values:
    # specific winter mass balance (output of Jam_winter.py):
    if suffix == '_all':
        bw = bwi
    else:
        bw = np.nan

    # load file with elevation and mass balance values (QGIS output):
    # zones = gpd.read_file('/Users/leahartl/Desktop/Jam2025/sommer/MB_viole/JAM_mb_2025_1.geojson')
    zonesfn = outline_dir+str(curyear)+suffix+'.geojson'
    zones = gpd.read_file(zonesfn)
    # reproject to crs with true area (don't use lat/lon to compute area)
    zones = zones.to_crs(epsg=31254)


    zone_stats, sumbalance, sumstats, bs, bquer = mainMassBalance(zones, bw)

    # # make map plot for report
    if suffix == '_all':
        print('main run ', str(curyear))
        makeMB_Map(zones, suffix, curyear, stakesfn, param, raster)
        # # make the tables
        dfZones = makeMBTables(zone_stats, sumbalance, bquer, bw, bs, suffix, winter_fn)
        print(dfZones)
        stop
        makeMBFig_main(dfZones, sumbalance, bquer, bw, bs, suffix)
        StripesPlot(sumstats, curyear, ts_fn)
        makeMBPlot_v2(zones, zones1, dfZones, sumbalance, bquer, sumstats, suffix)

    else:
        print('partial run ', suffix, str(curyear))
        dfZones = makeMBTables(zone_stats, sumbalance, bquer, bw, bs, suffix, winter_fn)
        makeMBPlot_v2(zones, zones1, dfZones, sumbalance, bquer, sumstats, suffix)



plt.show()


