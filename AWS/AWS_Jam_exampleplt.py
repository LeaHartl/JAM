import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.stats import circmean

# load data
filename = 'dataMerged.csv'
# error value is -777.0
data = pd.read_csv(filename, index_col=0, parse_dates=True, na_values=-777.0)

# RADIATION LW
# Correction with sensor temperature!
data['LWin_Cor'] = data['LWin']+5.67*10**-8 * (data['SensorTemp']+273.15)**4
data['LWout_Cor'] = data['LWout']+5.67*10**-8 * (data['SensorTemp']+273.15)**4
print(data.head())


def circular_mean(x):
    return round(np.rad2deg(circmean(np.deg2rad(x['WindDir'].values))),2)

# function to make a time series plot for some of teh parameters:
def timeseriesplot(df):
    # resample hourly data to daily and monthly values:
    # NO CHECKS FOR INCOMPLETE DAYS OR MONTHS - ADAPT AS NEEDED
    # daily means:
    df_mean = df.resample('d').mean()
    # monthly means:
    df_mnth = df.resample('m').mean()
    
    # optional additional resampling, uncomment as needed.
    # df_min = df.resample('d').min()
    # df_max = df.resample('d').max()
    # df_mnth_low = df_min.resample('m').mean()
    # df_mnth_high = df_max.resample('m').mean()
    # optional pivot table, useful for some kinds of visualizations
    # df_mnth['month'] = df_mnth.index.month
    # df_mnth['year'] = df_mnth.index.year
    # df_mnth_p = df_mnth.pivot(index='month', columns='year', values='AirTemp')

    # initialize a figrue with five subplots arranged underneath each other
    fig, ax = plt.subplots(5, 1, figsize=(12, 8), sharex=True)
    ax = ax.flatten()

    # air temperature
    ax[0].plot(df_mnth.index, df_mnth.AirTemp, c='k', label='monthly mean')
    ax[0].plot(df_mean.index, df_mean.AirTemp, c='k', linestyle='--', linewidth=0.5, label='daily mean')
    #ax[0].plot(df_mnth_low.index, df_mnth_low.AirTemp, c='b', label='daily low, monthly mean')
    #ax[0].plot(df_mnth_high.index, df_mnth_high.AirTemp, c='r', label='daily high, monthly mean')
    
    # ax[0].fill_between(df_mean.index, df_min.AirTemp, df_max.AirTemp, alpha=0.5, label='daily range')
    ax[0].set_title('Air temperature')
    ax[0].legend(loc='lower left')
    ax[0].set_ylabel('°C')
    ax[0].set_ylim([-25, 30])
    ax[0].grid('both')

    # relative humidity
    ax[1].plot(df_mean.index, df_mean.RelHum, c='k', linestyle='--', linewidth=0.5, label='Relative humidity')
    ax[1].plot(df_mnth.index, df_mnth.RelHum, c='k', linestyle='-', linewidth=1, label='monthly mean')
    ax[1].set_ylabel('%')
    ax[1].set_title('Relative humidity')
    # ax[1].legend(loc='lower left')
    ax[1].set_ylim([0, 100])
    ax[1].grid('both')

    # global radiation
    ax[2].plot(df_mnth.index, df_mnth.GlobalRadiation, c='k', label='monthly mean SW in')
    ax[2].plot(df_mean.index, df_mean.GlobalRadiation, c='k', linestyle='--', linewidth=0.5, label='daily mean SW in')
    ax[2].grid('both')
    # ax[2].legend()
    ax[2].set_ylabel('W/m^2')
    ax[2].set_title('Global Radiation')

    # wind speed
    ax[3].plot(df_mnth.index, df_mnth.WindSpeed, c='k', label='monthly mean wind speed')
    ax[3].plot(df_mean.index, df_mean.WindSpeed, c='k', linestyle='--', linewidth=0.5)
    # optiona: Gusts
    # ax[3].plot(df_mean.index, df_mean.WindSpeedGust, c='r', linestyle='--', linewidth=0.5, label='daily mean gust')
    ax[3].grid('both')
    ax[3].set_ylabel('m/s')
    # ax[3].set_ylim([0, 18])
    ax[3].set_title('Wind speed')


    # wind dir - circmean

    wdir = df.resample('d').apply(circular_mean)
    # circular mean:
    ax[4].scatter(wdir.index, wdir.values, c='k', label='daily mean wind direction', s=2)
    # non circular mean: uncomment to see how it compares
    # ax[4].scatter(df_mean.index, df_mean.WindDir, c='g', label='non-circular mean', s=2)
    ax[4].scatter(df.index, df.WindDir, c='r', label='wind direction, 1 h', s=0.005)
    ax[4].set_ylim(0, 360)
    ax[4].set_title('Wind direction')
    ax[4].legend()
    ax[4].grid('both')

    # save the figure to a folder called "figs" - adjust path and filename as needed!
    fig.savefig('figs/JAM_meteo_daily_monthly.png', bbox_inches='tight', dpi=300)

    return()



# function to plot precipitation and snow depth
def timeseries_precip(df):
    # resample hourly data to daily and monthly values:
    # NO CHECKS FOR INCOMPLETE DAYS OR MONTHS - ADAPT AS NEEDED
    # daily means:
    df_mean = df.resample('d').mean()
    # monthly means:
    df_mnth = df.resample('m').mean()

    # precip: make monthly and daily sums (!)
    df_mnth_pr = df[['Precip']].resample('m').sum()
    df_day_pr = df[['Precip']].resample('d').sum()
    
    # initialize a figrue with two subplots arranged underneath each other
    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    ax = ax.flatten()

    # precip
    ax[0].bar(df_mnth_pr.index, df_mnth_pr['Precip'], color='k', width=20)
    ax[0].set_title('Precipitation (monthly sum)')
    ax[0].set_ylabel('mm')
    ax[0].grid('both')

    ax[1].set_title('Snowdepth')
    # ax[1].legend(loc='upper left')
    ax[1].set_ylabel('cm')
    # ax[0].set_ylim([-25, 30])
    ax[1].grid('both')


    # snow depth
    ax[1].plot(df_mnth.index, df_mnth.Snowdepth, c='k', label='monthly mean')
    ax[1].plot(df_mean.index, df_mean.Snowdepth, c='k', linestyle='--', linewidth=0.5, label='daily mean')
    ax[1].set_title('Snowdepth')
    ax[1].legend(loc='upper left')
    ax[1].set_ylabel('cm')
    # ax[0].set_ylim([-25, 30])
    ax[1].grid('both')

    
    fig.savefig('figs/JAM_precip_snow.png', bbox_inches='tight', dpi=300)

    return()



# call the plotting functions
timeseriesplot(data)
timeseries_precip(data)




plt.show()









