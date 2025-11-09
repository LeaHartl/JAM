import numpy as np
import pandas as pd
import geopandas as gpd
# import json
import matplotlib.pyplot as plt
import seaborn as seaborn
from matplotlib.colors import ListedColormap
import matplotlib.dates as mdates
from pandas.tseries.offsets import DateOffset
import matplotlib.ticker as mticker
import datetime as dt

import json
import seaborn as seaborn
from shapely.geometry import Point
# old reports used this file.
# klima = '/Users/leahartl/Desktop/JAM/klima.csv'

fn_Jam_temp = '/Users/leahartl/Desktop/Jam2025/[EXT]_AW__Jamtal_Totalisator_&_Stationsdaten/LT115451.csv'
fn_Jam_pcpn = '/Users/leahartl/Desktop/Jam2025/[EXT]_AW__Jamtal_Totalisator_&_Stationsdaten/N115451.csv'

curyear = 2025

def day_of_water_year(some_date):
    some_date = some_date.replace(tzinfo=None)
    # Get the date of the previous October 1st
    water_year_start_date = dt.datetime(some_date.year + some_date.month // 10 - 1, 10, 1)   
    # Return the number of days since then
    return (some_date - water_year_start_date).days + 1


# Function to check leap year
def is_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def seasonStats(summer):
    sumStats = summer[['tl_mittel', 't_normal']].mean()
    sumStats['rr'] = summer['rr'].sum()
    sumStats['rr_normal'] = summer['rr_normal'].sum()
    sumStats['t_dev'] = sumStats['tl_mittel'] - sumStats['t_normal']
    sumStats['rr_dev'] = sumStats['rr'] - sumStats['rr_normal']
    sumStats['rr_dev_perc'] = 100*(sumStats['rr'] - sumStats['rr_normal']) / sumStats['rr_normal']

    sumStats = sumStats[['tl_mittel', 't_normal', 't_dev', 'rr', 'rr_normal', 'rr_dev', 'rr_dev_perc']]

    return(sumStats)


def readHDdata(fname, param, skip):
    out = pd.read_csv(fname, delimiter=';', skiprows=skip, na_values='Lücke',
                      names=['date', param], encoding='unicode_escape', decimal=',')
    out[param] = pd.to_numeric(out[param])

    out.set_index('date', inplace=True)
    # print(out)
    out.index = pd.to_datetime(out.index, format='%d.%m.%Y %H:%M:%S   ')


    if param == 'N':
        monthly = out.resample('ME').sum()
    if param == 'T':
        monthly = out.resample('ME').mean()
    # print(out)

    return (out, monthly)


def loadData(curyear):
    # hardcoded link to geosphere data hub:
    url = 'https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-1d?parameters=tl_mittel%2Crr&start=1980-01-01T00%3A00%3A00.000Z&end='+str(curyear)+'-11-01T00%3A00%3A00.000Z&station_ids=28&output_format=csv&filename=Messstationen+Tagesdaten+v2+Datensatz_20251003_20251101'
    # print(url)
    station_df = pd.read_csv(url)
    station_df.index = pd.to_datetime(station_df['time'])

    # add water year
    station_df['WY'] = station_df.index.year
    station_df['WY'].loc[station_df.index.month >= 10] += 1
    # add day of year
    station_df['doy'] = station_df.index.dayofyear
    station_df['doy'] = station_df.index.dayofyear

    # replace negative pcpn values with nan
    station_df.loc[station_df['rr'] < 0, 'rr'] = np.nan

    # no leap years
    station_df = station_df[~((station_df.index.month == 2) & (station_df.index.day == 29))]
    # add day of water year
    station_df['wday'] = station_df.index.to_series().apply(day_of_water_year)

    # get the subset of the data that you want for your normals:
    normal_period = station_df.loc[(station_df['WY'] >= 1991) & (station_df['WY'] <= 2020)]
    # group by day of year and average
    normal_values = normal_period[['wday', 'tl_mittel']].groupby('wday').mean()

    # if year is not a leap year, remove feb 29 (day of wy 152)
    if not pd.to_datetime(str(curyear)+'-10-01').is_leap_year:
        normal_values = normal_values.loc[normal_values.index!=152]

    cur_year = station_df.loc[station_df['WY'] == curyear]
    cur_year['t_normal'] = normal_values['tl_mittel'].values
    cur_year['t_dev'] = cur_year['tl_mittel'] - cur_year['t_normal']

    # monthly data
    normal_period_M = normal_period[['tl_mittel', 'rr']].resample('ME').mean()
    normal_period_M['rr'] = normal_period['rr'].resample('ME').sum()

    normal_monthly = normal_period_M[['tl_mittel', 'rr']].groupby(normal_period_M.index.month).mean()
    normal_monthly = normal_monthly.reindex([10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    cur_yearM = station_df[['WY', 'tl_mittel']].loc[station_df['WY'] == curyear].resample('ME').mean()
    cur_yearM['rr'] = station_df['rr'].loc[station_df['WY'] == curyear].resample('ME').sum()


    cur_yearM['t_normal'] = normal_monthly['tl_mittel'].values
    cur_yearM['t_dev'] = cur_yearM['tl_mittel'] - cur_yearM['t_normal']

    cur_yearM['rr_normal'] = normal_monthly['rr'].values
    cur_yearM['rr_dev'] = cur_yearM['rr'] - cur_yearM['rr_normal']
    cur_yearM['rr_dev_perc'] = 100*(cur_yearM['rr'] - cur_yearM['rr_normal']) / cur_yearM['rr_normal']

    cur_yearM = cur_yearM[['tl_mittel', 't_normal', 't_dev', 'rr', 'rr_normal', 'rr_dev', 'rr_dev_perc']]

    summer = cur_yearM.loc[(cur_yearM.index.month>=5) & (cur_yearM.index.month<=9)]
    winter = cur_yearM.loc[(cur_yearM.index.month>=10) | (cur_yearM.index.month<=4)]

    sumStats = seasonStats(summer)
    winStats = seasonStats(winter)
    hydroYearStats = seasonStats(cur_yearM)

    stats = pd.DataFrame(index=['Winter', 'Sommer', 'hydrolog. Jahr'], columns=['tl_mittel', 't_normal', 't_dev', 'rr', 'rr_normal', 'rr_dev', 'rr_dev_perc'])
    stats.loc['Winter', :] = winStats.values
    stats.loc['Sommer', :] = sumStats.values
    stats.loc['hydrolog. Jahr', :] = hydroYearStats.values

    stats.columns = ['tl_mittel', 't_normal', 't_dev', 'rr', 'rr_normal', 'rr_dev', 'rr_dev_perc']

    # prepare summary table of monthly values for the report:
    cur_yearM1 = cur_yearM.copy()
    cur_yearM1.index = cur_yearM1.index.strftime('%B')
    climtable = pd.concat([cur_yearM1, stats])
    climtable[['tl_mittel', 't_normal', 't_dev']] = climtable[['tl_mittel', 't_normal', 't_dev']].astype(float).round(decimals=1)
    climtable[['rr', 'rr_normal', 'rr_dev', 'rr_dev_perc']] = climtable[['rr', 'rr_normal', 'rr_dev', 'rr_dev_perc']].round(decimals=0).astype(int)

    print(climtable)
    # save to latex
    climtable.to_latex('/Users/leahartl/Desktop/Jam2025/Bericht/klima_galtuer.txt')

    return(cur_year, cur_yearM, climtable)


def makeClimFig(cur_year, cur_yearM, dailyJam, monthlyJam, curyear):

    fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    ax = ax.flatten()
    ax[0].plot(dailyJam.index.values, dailyJam['T'].values, color='k', linewidth=1, label='AWS Jamtalhütte')

    ax[0].plot(cur_year.index, cur_year['t_normal'], color='grey', label='Galtür, Klimamittel 1991-2020')
    ax[0].plot(cur_year.index, cur_year['tl_mittel'], color='grey', linewidth=0.5)

    ax[0].fill_between(cur_year.index, cur_year['t_normal'], cur_year['tl_mittel'], 
                       where=(cur_year['tl_mittel'] >= cur_year['t_normal']), color='red', alpha=0.3, label='positive T. Abweichung 2025, Galtür')
    ax[0].fill_between(cur_year.index, cur_year['t_normal'], cur_year['tl_mittel'], 
                       where=(cur_year['tl_mittel'] < cur_year['t_normal']), color='blue', alpha=0.3, label='negative T. Abweichung 2025, Galtür')

    # this sets the formating of the dates for the axis labels
    myFmt = mdates.DateFormatter('%Y-%b')

    ax[0].set_xlim(pd.to_datetime(str(curyear-1)+'-10-01'), pd.to_datetime(str(curyear)+'-09-30'))

    ax[0].xaxis.set_major_formatter(myFmt)
    ax[0].set_xticks(ax[0].get_xticks(), ax[0].get_xticklabels(), rotation=45, fontsize=12)#, ha='right')
    ax[0].set_yticks(ax[0].get_yticks(), ax[0].get_yticklabels(), fontsize=12)

    ax[0].grid('both')
    ax[0].legend()
    ax[0].set_ylabel('Lufttemperatur Tagesmittel (°C)', fontsize=12)

    ax[1].bar(monthlyJam.index - pd.DateOffset(days=22), monthlyJam['N'], color='skyblue',  width=7, label='AWS Jamtalhütte, monatlicher Niederschlag 2024/25')
    ax[1].bar(cur_yearM.index - pd.DateOffset(days=15), cur_yearM['rr'], color='k',  width=7, label='Galtür, monatlicher Niederschlag 2024/25')
    ax[1].bar(cur_yearM.index - pd.DateOffset(days=8), cur_yearM['rr_normal'], color='grey', width=7, label='Galtür, Klimamittel 1991-2020')
    
    ax[1].set_xlim(pd.to_datetime(str(curyear-1)+'-10-01'), pd.to_datetime(str(curyear)+'-09-30'))

    ax[1].xaxis.set_major_formatter(myFmt)
    ax[1].set_xticks(ax[1].get_xticks(), ax[1].get_xticklabels(), rotation=45, fontsize=12)#, ha='right')
    ax[1].set_yticks(ax[1].get_yticks(), ax[1].get_yticklabels(), fontsize=12)

    ax[1].grid('both')
    ax[1].legend()
    ax[1].set_ylabel('Niederschlagssumme (mm)', fontsize=12)

    ax[0].text(pd.to_datetime(str(curyear)+'-09-10'), 22, 'a', fontsize=10,
               bbox=dict(boxstyle="square,pad=0.3",fc="lightgrey", ec="grey", lw=2))
    ax[1].text(pd.to_datetime(str(curyear)+'-09-10'), 325, 'b', fontsize=10,
               bbox=dict(boxstyle="square,pad=0.3",fc="lightgrey", ec="grey", lw=2))

    fig.savefig('/Users/leahartl/Desktop/Jam2025/Bericht/ClimFig_'+str(curyear)+'.png', dpi=200, bbox_inches='tight')


# make Jam table: 
def makeJamTable(outT, outN, climtable, curyear):
    dailyJam = outT.loc[outT.index > str(curyear-1)+'-10-01'].resample('D').mean()
    dailyJam['N'] = outN.loc[outN.index > str(curyear-1)+'-10-01'].resample('D').sum()
    # extract current year:
    dailyJam = dailyJam.loc[(dailyJam.index >= pd.to_datetime(str(curyear-1)+'-10-01')) & (dailyJam.index < pd.to_datetime(str(curyear)+'-10-01'))]
    
    # make monthly values:
    monthlyJam = dailyJam.resample('M').mean()
    monthlyJam['N'] = dailyJam['N'].resample('M').sum()

    winter = (dailyJam.index >= pd.to_datetime(str(curyear-1)+'-10-01')) & (dailyJam.index < pd.to_datetime(str(curyear)+'-05-01'))
    sommer = (dailyJam.index >= pd.to_datetime(str(curyear)+'-05-01')) & (dailyJam.index < pd.to_datetime(str(curyear)+'-10-01'))
    
    statsJam = pd.DataFrame(index=['Winter', 'Sommer', 'hydrolog. Jahr'], columns=['T', 'N'])
    statsJam.loc['Winter', 'N'] = dailyJam['N'].loc[winter].sum()
    statsJam.loc['Sommer', 'N'] = dailyJam['N'].loc[sommer].sum()
    statsJam.loc['Winter', 'T'] = dailyJam['T'].loc[winter].mean()
    statsJam.loc['Sommer', 'T'] = dailyJam['T'].loc[sommer].mean()
    
    statsJam.loc['hydrolog. Jahr', 'N'] = dailyJam['N'].sum()
    statsJam.loc['hydrolog. Jahr', 'T'] = dailyJam['T'].mean()

    fortable = pd.concat([monthlyJam, statsJam])
    fortable['difT_Jam_Galt'] = fortable['T'].values - climtable['tl_mittel'].values
    fortable['difN_Jam_Galt'] = fortable['N'].values - climtable['rr'].values

    fortable.index = climtable.index

    fortable[['T', 'difT_Jam_Galt']] = fortable[['T', 'difT_Jam_Galt']].astype(float).round(decimals=1)
    fortable[['N', 'difN_Jam_Galt']] = fortable[['N', 'difN_Jam_Galt']].round(decimals=0).astype(int)

    print(fortable)
    # save to latex
    fortable.to_latex('/Users/leahartl/Desktop/Jam2025/Bericht/klima_jam.txt')

    # stop
    return(dailyJam, monthlyJam)

    

# load Totalisator file and print to latex version: 
def Regenmesser():
    fn = '/Users/leahartl/Desktop/Jam2025/Totalisator2025.xlsx'
    regen = pd.read_excel(fn, index_col=0, header=1, usecols=[0,1,2,3,4,5,6,7])
    regen.index=regen.index.strftime('%d.%m.%Y')
    print(regen)
    regen.to_latex('/Users/leahartl/Desktop/Jam2025/Bericht/Regenmesser.txt', float_format="%.2f")


Regenmesser()


stop
# load the Galtür data, compute normals and deviations, make table for the report
cur_year, cur_yearM, climtable = loadData(curyear)

# load HD data for Jamtalhütte AWS (ask HD to send this data)
outN, monthlyN = readHDdata(fn_Jam_pcpn, 'N', 24)
outT, monthlyT = readHDdata(fn_Jam_temp, 'T', 24)






# # make the first climate table for the report
# makeJamTable(outT, outN, climtable, curyear)

# # make the temp and precip plot and the second table
# makeClimFig(cur_year, cur_yearM, dailyJam, monthlyJam, curyear)


plt.show()

