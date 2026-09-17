import numpy as np
import pandas as pd
import datetime as dt
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
# import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
# from shapely.geometry import Point
import glob


# MB vs elevation, annual
def plot_annual_seasonal_elevation(an, gl, yrs):# probesVK, probesMWK):

    fig, ax = plt.subplots(1, 1, figsize=(3, 8), sharey=True)

    yrs = np.arange(1989, 2026)

    clrs = cm.cividis(np.linspace(0, 0.9, len(yrs)))
    lns = []


    for j, y in enumerate(yrs):
        temp = an.loc[(an['year'] == y) & (an['glacier'] == gl)  & (an['measurement_type'] == 1)]
        # if len(temp)> 0:
        ln = ax.scatter(temp.mb_we/1000, temp.z_pos, color=clrs[j], s=28, edgecolor='k', linewidth=0.2, zorder=2, label=str(y))
        # temp2 = an.loc[(an['year'] == y) & (an['glacier'] == gl)  & (an['measurement_type'] == 2)]
        # if len(temp2)> 0:
        #     ax.scatter(temp.mb_we/1000, temp.z_pos, color=clrs[j], marker= 's', s=48, edgecolor='k', linewidth=0.2, zorder=2, label=str(y))
        
        ax.errorbar(temp.mb_we, temp.z_pos, xerr=temp.mb_error/1000, linestyle="None", color='k', linewidth=0.4, zorder=1)
        lns.append(ln)

        temp1 = an.loc[(an['year'] == y) & (an['glacier'] == gl)  & (an['measurement_type'] == 2)]
        print(temp1)
        ax.scatter(temp1.mb_we/1000, temp1.z_pos, color=clrs[j], s=28, edgecolor='k', marker='o', linewidth=0.2, zorder=2)
        # ax.errorbar(temp1.mb_we/1000, temp1.z_pos, xerr=temp1.mb_error/1000, linestyle="None", color='k', linewidth=0.4, zorder=1)
        print(y, print(temp.z_pos.min()))
        print(temp[['mb_we', 'measurement_type']])

    # temp22 = an.loc[(an['year'] == 2022) & (an['glacier'] == gl)]
    # ln = ax.scatter(temp22.mb_we, temp22.z_pos, color='red', s=32, edgecolor='k', linewidth=0.2, zorder=2, label=str(2022))
        
        

    ax.axvspan(0, 0, color='k', linewidth=2)
    ax.set_ylim(2380, 3150)
    ax.set_xlim(-6.300, 2.300)
    ax.set_xlabel('b (m w.e.)')
    ax.set_ylabel('elevation (m.a.s.l.)')
    ax.grid('both')
    ax.set_title('Annual point mass balance, ' + gl)


    # pt1 = Line2D([0], [0], marker='o', linestyle = 'None', label='stakes', color='k', markersize=8)
    # pt2 = Line2D([0], [0], marker='s', linestyle = 'None', label='pits', color='k', markersize=8)
    # # pt1_2 = Line2D([0], [0], marker='o', linestyle = 'None', label='probe points', color='k', markersize=4)
    # lns.append(pt1)    
    # lns.append(pt2)
    # # print(lns)


    fig.legend(handles=lns, loc='lower left', bbox_to_anchor=(0.9, 0.2), ncol=2)
    fig.savefig('/Users/leahartl/Desktop/JAM/annual_seasonal_elevation_'+gl+'.png', bbox_inches='tight', dpi=300)




def castdates_addname_gdf(df, epsg):
    df['date0'] = pd.to_datetime(df['date0'])
    df['date1'] = pd.to_datetime(df['date1'])
    df['name'] = df.index.astype(str)
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(x=df.x_pos, y=df.y_pos, crs={'init': 'epsg:'+epsg})
    )
    return(gdf)


def loadPoints(pathStakes, gl, epsg):
    # dictionary to translate between original and pangaea column names
    namedict = {
    'Date/Time (begin of period)':'date0',
    'Date/Time (end of period)':'date1',
    'Name (stake, sounding, probing)': 'name',
    'Duration [days] (period length)': 'period',
    'Observer': 'source',
    'x [m] (x-position of stake, EPSG:'+epsg+')': 'x_pos',
    'y [m] (y-position of stake, EPSG:'+epsg+')': 'y_pos',
    'z [m] (elevation of stake)': 'z_pos',
    'QF date (quality identifier for date)': 'date_quality',
    'QF pos (quality identifier for position)': 'position_quality',
    'Dens snow/firn/ice [kg/m**3]': 'density',
    'QF rho (quality identifier for density)': 'density_quality',
    'QF pos (quality identifier for position)': 'position_quality',
    'MB point [mm w.e./kg/m**2]': 'mb_we',
    'QF measurement (quality identifier for stake ...)': 'measurement_quality',
    'Measurement type (type of mass balance observation)': 'measurement_type',
    'MB point unc [mm w.e.] (Uncertainty of point mass bal...)': 'mb_error',
    'Reading unc [mm w.e.] (Reading uncertainty of point ...)': 'reading_error',
    'Density unc [mm w.e.] (Density uncertainty of point ...)': 'density_error',
    'MB raw [cm] (raw mass balance measurement)': 'mb_raw',
    'QF (Flag to indicate whether the ...)': 'probe_flag'
    }


    an = pd.read_csv(pathStakes)
    an['glacier'] = gl
    an['year'] = pd.to_datetime(an['Date/Time (end of period)']).dt.year

    an_rn = an.rename(mapper=namedict, axis=1)
    #print(an_rn.head())
    an_rn = castdates_addname_gdf(an_rn, epsg)
    return(an_rn)


# read geojson
def makeplots(df, stakes_pits, vmin, vmax, cmap, what, yrcur):

    lns = []
    pts = []

    yrs = np.arange(1989, int(yrcur)+1)
    # adjust row and col number each year
    row = 6
    col = 7
    # print(an_rn)
    # an_rn['mb_we_cm'] = an_rn['mb_we']/10


    fig, ax = plt.subplots(row, col, figsize=(12, 10), sharey=True, sharex=True)
    ax = ax.flatten()

    #yrs = np.arange(1989, 1992)#2025)

    for i, y in enumerate(df['year'].values):#[-5:]):
        ax[i].set_title(str(y))
        print(y)

        f = df['fname'].loc[df['year']==y].values[0]
        shp = gpd.read_file(f)
        #print(shp.head())

        shp.to_crs(epsg=4326, inplace=True)

        shp['mb'] = shp['mb']/100
        #shp['dummydata'] = 1
        #shp_outline = shp.dissolve(by='dummydata')
    
        # stakes_pits.to_crs(epsg=4326, inplace=True)

        an_rn_temp = stakes_pits.loc[stakes_pits.year == y]
        an_rn_temp['mb_we'] = an_rn_temp['mb_we']/1000

        an_rn_temp.to_crs(epsg=4326, inplace=True)

        if len(shp) > 0:

            divnorm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter = 0, vmax=vmax)
            shp.plot(ax=ax[i], column='mb', alpha=1, cmap=cmap, norm=divnorm, legend=False, zorder=8)#, norm=norm_w)# zorder=i+1
            #shp_outline.boundary.plot(ax=ax[i], colors='k', zorder=20)
            an_rn_stks =an_rn_temp.loc[an_rn_temp.measurement_type==1]
            an_rn_pits =an_rn_temp.loc[an_rn_temp.measurement_type==2]
            # print(an_rn_stks[['mb_we', 'geometry']])
            # print(an_rn_pits[['mb_we', 'geometry']])
            # print(an_rn_stks.geometry.x.sum())
            if an_rn_stks.geometry.x.sum()>0:
                an_rn_stks.plot(ax=ax[i], column='mb_we', markersize=10, cmap=cmap, norm=divnorm, legend=False, edgecolor='k',  linewidth=0.5, zorder=100)#norm=divnorm, 
            if len(an_rn_pits)>0:
                an_rn_pits.plot(ax=ax[i], column='mb_we', markersize=10, marker = 's', cmap=cmap, norm=divnorm, legend=False, edgecolor='k', linewidth=0.5, zorder=100)#norm=divnorm, 

            fig.subplots_adjust(right=0.8)
            cbar_ax = fig.add_axes([0.85, 0.11, 0.02, 0.7])
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=divnorm)
            cbar = fig.colorbar(sm, cax=cbar_ax)
            cbar.set_label('Annual mass balance (m w.e.)')
            cbar.ax.set_yscale('linear')

                    # set tick params
            for a in ax:
                a.set_ylim([46.848, 46.871])
                a.set_xlim([10.14, 10.187])
                # a.set_yticks([47.47, 47.48, 47.49])
                # a.set_xticks([13.61, 13.62])
                a.tick_params(axis='both', labelsize=8)
                a.set_facecolor('grey')
                # a.set_xlabel('°')

            ax[-1].set_axis_off()
            ax[-2].set_axis_off()
            ax[-3].set_axis_off()
            ax[-4].set_axis_off()
            ax[-5].set_axis_off()



        fig.savefig('/Users/leahartl/Desktop/JAM/test_maps_subplots'+yrcur+'.png', dpi=300, bbox_inches='tight')



def glacierwide():
    glacierwide = pd.read_csv('/Users/leahartl/Desktop/JAM/Jam_mb_timeseries.csv')
    # print(glacierwide)
    # print(MB[['YEAR', 'WINTER_BALANCE']])
    # MB[['YEAR', 'WINTER_BALANCE', 'SUMMER_BALANCE', 'ANNUAL_BALANCE']] = MB[['YEAR', 'WINTER_BALANCE', 'SUMMER_BALANCE', 'ANNUAL_BALANCE']] / 1000
    MB = glacierwide[['Year', 'bw', 'bs', 'b']]
    print(MB)
    MB['Year1'] = MB['Year'].str[-4:].astype(int) 
    print(MB)
    # MB.loc[-1] = [2024,  1963, -3985, -2022]

    # stop
    fig, ax3 = plt.subplots(1,1, figsize=(10, 4))
    ax3.set_title('Glacier wide mass balance, JAM')
    ax3.bar(MB.Year1.astype(int).values, MB.bw/1000, color='blue', alpha=0.4, label='b_winter')
    ax3.bar(MB.Year1.astype(int).values, MB.bs/1000, color='red', alpha=0.4, label='b_summer')
    ax3.bar(MB.Year1.astype(int).values, MB.b/1000, color='k', label='b_annual')

    ax3.legend(loc='lower left', bbox_to_anchor=(0.3, -0.2), ncol=3)
    ax3.set_ylabel('m w.e.')
    ax3.set_xlim(1988, 2025)
    ax3.set_ylim(-5, 2.5)
    ax3.grid('both')
    ax3.set_xticks(np.arange(1988, 2026, 2))

    fig.savefig('/Users/leahartl/Desktop/JAM/barplot_jam.png', dpi=300, bbox_inches='tight')

    


# path1 = 'olderdata/'
# fls1 = glob.glob(path1+'/*.shp')

path1 = '/Users/leahartl/Desktop/LTER/AGM/JAM/shapes2'
fls1 = glob.glob(path1+'/*.geojson')


dfAnnual = pd.DataFrame(columns=['fname', 'year'])
dfAnnual['fname'] = fls1


# print(dfAnnual)
# dfAnnual['year1'] = dfAnnual['fname'].str[10:12]#.astype(int) 
dfAnnual['year'] = dfAnnual['fname'].str[-12:-8].astype(int) 
dfAnnual['type'] = 'annual'
 
dfAnnual.sort_values(by=['year'], inplace=True)
# print(dfAnnual)


pathAnnualPoint_JAM = '/Users/leahartl/Desktop/JAM/Jam_MB_annual_2025.csv'
pts_JAM = loadPoints(pathAnnualPoint_JAM, 'JAM', '4326')
print(pts_JAM)

cmap_s = 'RdYlBu'#'coolwarm_r'
vmin_s = -6.00
vmax_s = 2.00

makeplots(dfAnnual, pts_JAM, vmin_s, vmax_s, cmap_s, 'annual', '2025')
plt.show()

stop
# make scatter plot of annual MB vs elevation:
plot_annual_seasonal_elevation(pts_JAM, 'JAM', np.arange(1989, 2026))
# glacierwide()
plt.show()
stop

plt.show()

