import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# load data
filename = 'dataMerged.csv'
# error value is -777.0
data = pd.read_csv(filename, index_col=0, parse_dates=True, na_values=-777.0)

# RADIATION LW
# Correction with sensor temperature!
data['LWin_Cor'] = data['LWin']+5.67*10**-8 * (data['SensorTemp']+273.15)**4
data['LWout_Cor'] = data['LWout']+5.67*10**-8 * (data['SensorTemp']+273.15)**4


# function to make the plot:
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

    # initialize a figrue with four subplots arranged underneath each other
    fig, ax = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
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

    # save the figure to a folder called "figs" - adjust path and filename as needed!
    fig.savefig('figs/JAM_meteo_daily_monthly.png', bbox_inches='tight', dpi=300)

    return()


# call the plotting function and save the figure
timeseriesplot(data)



plt.show()









