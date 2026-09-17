import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# script to explore the radiation parameters available for JAM AWS

# load data
filename = 'dataMerged.csv'
# error value is -777.0
data = pd.read_csv(filename, index_col=0, parse_dates=True, na_values=-777.0)

# RADIATION LW
# Correction with sensor temperature!
data['LWin_Cor'] = data['LWin']+5.67*10**-8 * (data['SensorTemp']+273.15)**4
data['LWout_Cor'] = data['LWout']+5.67*10**-8 * (data['SensorTemp']+273.15)**4

# subset data to keep only the relevant columns
radpars = data[['SWin', 'SWout', 'LWin', 'LWout', 'LWin_Cor', 'LWout_Cor', 'SensorTemp', 'GlobalRadiation']]

radpars['Glob_SWin'] = radpars['GlobalRadiation'] / radpars['SWin']

print(radpars.head())


# functions to make the plots:
def timeseriesplot_SW(df):
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

    # initialize a figrue with subplots arranged underneath each other
    fig, ax = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    ax = ax.flatten()

    # global radiation
    ax[0].plot(df_mnth.index, df_mnth.GlobalRadiation, c='k', label='monthly mean')
    ax[0].plot(df_mean.index, df_mean.GlobalRadiation, c='k', linestyle='--', linewidth=0.5, label='daily mean')
    ax[0].grid('both')
    # ax[2].legend()
    ax[0].set_ylabel('W/m^2')
    ax[0].set_title('Global Radiation ("GS")')

    ax[1].plot(df_mnth.index, df_mnth.SWin, c='k', label='monthly mean in')
    ax[1].plot(df_mnth.index, df_mnth.SWout, c='grey', label='monthly mean out')
    ax[1].plot(df_mean.index, df_mean.SWin, c='k', linestyle='--', linewidth=0.5, label='daily mean in')
    ax[1].plot(df_mean.index, df_mean.SWout, c='grey', linestyle='--', linewidth=0.5, label='daily mean out')
    ax[1].grid('both')
    ax[1].legend()
    ax[1].set_ylabel('unit ? ')
    ax[1].set_title('SW in ("PYRANOMETER.OBEN")')

    # Ratio global rad - SW in
    ax[2].plot(df.index, df['Glob_SWin'], c='k', linestyle='--', linewidth=0.5)
    ax[2].grid('both')
    ax[2].set_title('Ratio  GS / PYRANOMETER.oben')
    # ax[2].plot(df_mean.index, df_mean.WindSpeed, c='k', linestyle='--', linewidth=0.5)
    # # optiona: Gusts
    # # ax[3].plot(df_mean.index, df_mean.WindSpeedGust, c='r', linestyle='--', linewidth=0.5, label='daily mean gust')
    # ax[3].grid('both')
    # ax[3].set_ylabel('m/s')
    # # ax[3].set_ylim([0, 18])
    # ax[3].set_title('Wind speed')

    # save the figure to a folder called "figs" - adjust path and filename as needed!
    fig.savefig('figs/JAM_radiation_SW.png', bbox_inches='tight', dpi=300)

    return()


# function to make the plot:
def timeseriesplot_LW(df):
    # resample hourly data to daily and monthly values:
    # NO CHECKS FOR INCOMPLETE DAYS OR MONTHS - ADAPT AS NEEDED
    # daily means:
    df_mean = df.resample('d').mean()
    # monthly means:
    df_mnth = df.resample('m').mean()

    # initialize a figrue with subplots arranged underneath each other
    fig, ax = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
    ax = ax.flatten()

    # LW radiation
    ax[0].plot(df_mnth.index, df_mnth.LWin, c='k', label='monthly mean incoming')
    ax[0].plot(df_mean.index, df_mean.LWin, c='k', linestyle='--', linewidth=0.5, label='daily mean in')
    ax[0].grid('both')
    ax[0].legend()
    ax[0].set_ylabel('W/m^2')
    ax[0].set_title('Longwave in ("LS.oben")')


    ax[1].plot(df_mnth.index, df_mnth.LWout, c='k', label='monthly mean outgoing')
    ax[1].plot(df_mean.index, df_mean.LWout, c='k', linestyle='--', linewidth=0.5, label='daily mean out')
    ax[1].grid('both')
    # ax[2].legend()
    ax[1].set_ylabel('W/m^2')
    ax[1].set_title('Longwave out("LS.unten")')

    # LW corr
    ax[2].plot(df_mnth.index, df_mnth.LWin_Cor, c='k', label='monthly mean in')
    ax[2].plot(df_mean.index, df_mean.LWin_Cor, c='k', linestyle='--', linewidth=0.5, label='daily mean in')
    ax[2].grid('both')
    ax[2].legend()
    ax[2].set_ylabel('W/m^2')
    ax[2].set_title('Longwave rad. incoming, corrected with sensortemp.')

    ax[3].plot(df_mnth.index, df_mnth.LWout_Cor, c='k', label='monthly mean out')
    ax[3].plot(df_mean.index, df_mean.LWout_Cor, c='k', linestyle='--', linewidth=0.5, label='daily mean out')
    ax[3].grid('both')
    ax[3].legend()
    ax[3].set_ylabel('W/m^2')
    ax[3].set_title('Longwave rad. outgoing, corrected with sensortemp.')
    
    # save the figure to a folder called "figs" - adjust path and filename as needed!
    fig.savefig('figs/JAM_radiation_LW.png', bbox_inches='tight', dpi=300)


# call the plotting function and save the figure
timeseriesplot_SW(radpars)

timeseriesplot_LW(radpars)



plt.show()









