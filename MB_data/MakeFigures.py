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

# import fiona
# import geopandas as gpd
import json
import seaborn as seaborn
from shapely.geometry import Point


def makeMBPlot():
    # csv reader specs have to be adjusted for different file formats (mostly number of skiprows)
    data = pd.read_csv('DatenAndrea/jam_mb2024.txt', sep=',', skiprows=15, decimal='.', index_col=False,
                       names=['Hohenstufe', 'Flaeche', 'B', 'b'])
    
    # stop
    # remove lowest elev zone (erronously still contained in csv file.)
    data = data.loc[data['Hohenstufe'] != 2425]
    print(data)
    # data['b_wi'] = np.nan
    # data['b_so'] = np.nan
    # wb file usually sent by andrea as an excel table, needs to be converted.
    dataW = pd.read_csv('DatenAndrea/winterbilanz_jam_2023_24.csv', sep=',', skiprows=7, decimal='.', index_col=False,
                        names=['Hohenstufe', 'Flaeche', 'Sond', 'SHmean', 'b_wi', 'B', '1', '2', '3'])
    # Höhenstufe,Fläche,Anzahl Sondierungen,mittlere Schneehöhe,b_wi,Bilanz,,,
    # dataW.index=dataW.Hohenst|ufe
    dataW['Flaeche'] = dataW['Flaeche'].values /10e5
    dataW = dataW.loc[dataW.Hohenstufe > 0]
    # print(dataW)
    # print(dataW['b_wi'])
    # stop
    data['b_wi'] = dataW['b_wi'].values
    data['b_so'] = -1*data['b_wi'] + data['b']

    # print(data)
    # stop
    data1 = data.copy()
    data1.loc[len(data1.index)+1] = data.sum().values
    data1.loc[len(data1.index)+1] = data.mean().values

    
    data1.loc[data1.index[-2], 'Hohenstufe'] = 'sum'
    data1.loc[data1.index[-1], 'Hohenstufe'] = 'mean'
    # print(data1)
    data1[['Hohenstufe', 'b', 'b_wi', 'b_so']] = data1[['Hohenstufe', 'b', 'b_wi', 'b_so']].round(0).astype(str)
    data1['b']=data1['b'].str.replace('.0', '')
    data1['b_wi']=data1['b_wi'].str.replace('.0', '')
    data1['b_so']=data1['b_so'].str.replace('.0', '')
    data1['Hohenstufe']=data1['Hohenstufe'].str.replace('.0', '')
    print(data1)
    # stoi
    # main table, annual balance by elevation zones
    print(data1.astype(str).to_latex(index=False))
    
    #stop
    # for winter table:
    fortable=dataW[['Hohenstufe', 'Flaeche', 'Sond', 'SHmean', 'b_wi', 'B']]
    fortable['B'] = fortable['B'].astype(float) / 1
    fortable[['Hohenstufe', 'Sond', 'SHmean', 'b_wi', 'B']]=fortable[['Hohenstufe', 'Sond', 'SHmean', 'b_wi', 'B']].round(0)
    fortable['Flaeche'] = fortable['Flaeche'].round(3)
    fortable = fortable.replace(np.nan, 0)
    fortable[['Hohenstufe', 'Sond', 'SHmean', 'b_wi', 'B']] = fortable[['Hohenstufe', 'Sond', 'SHmean', 'b_wi', 'B']].astype(int)

    print(fortable.to_latex(index=False))
    # stop
    dataW =dataW[:-1]
    # ANPASSEN, an tabelle anfügen
    # print(dataW[['Hohenstufe', 'Flaeche', 'Sond', 'SHmean', 'b_wi', 'B']].mean())
    print(dataW.sum())
    print(dataW.mean())

    Area = data.Flaeche.sum()
    AreaW = dataW.Flaeche.sum()
    print('area', Area, 'area W', AreaW)
    print(data.Flaeche)
    print(dataW.Flaeche)
    # stop
    # ============ PLOT
    fig1, ax = plt.subplots(1,2, figsize=(8, 8), sharey=True)
    ax = ax.flatten()
    # =========== AX 1
    # PLOT AREA on AX 1
    ax[0].barh(data.Hohenstufe.values, data.Flaeche.values, 45, align='center', linewidth=1, alpha=1, color='grey')
    # set x axis properties
    ax[0].set_xlim(0, .4)
    ax[0].set_xticks(np.arange(0, 0.4, 0.1))
    ax[0].set_xlabel('Fläche [km$^2$]')

    # set y axis properties
    ax[0].set_yticks(data.Hohenstufe.values)
    ax[0].set_ylabel('Höhenstufen [m.a.s.l.]')

    # # ========= AX 2
    ax[1].yaxis.tick_right()
    ax[1].yaxis.set_label_position('right')
    # PLOT MB on ax2
    ax[1].plot(data.b.values, data.Hohenstufe.values, 'k', linewidth=2, label='spezifische Massenbilanz 2023/24')
    ax[1].plot(data.b_wi.values, data.Hohenstufe.values, 'b', label='spezifische Wintermassenbilanz')
    ax[1].plot(data.b_so.values, data.Hohenstufe.values, 'r', label='spezifische Sommermassenbilanz')
    # # set x axis properties
    ax[1].set_xlabel('Massenbilanz [kg/m$^2$]')
    ax[1].grid('both')


    # # PLOT STAKES POINTS
    # ax2.plot(ba_stakes, h_stakes, 'ko', mew=1.5, label='Massenbilanz an den Ablationspegeln')
    # for i in range(0, len(h_stakes)):
    # ax2.annotate('%s' % name_stakes[i], xy=(ba_stakes[i], h_stakes[i]), xytext=(5, -3),
    #  textcoords='offset points',  size=8)
    # PLOT PIT POINTS
    #ax2.plot(ba_pit, h, 'gs', label='Schaechte Herbst 2015')
    #for i in range(0, len(h)):
    #ax2.annotate('%s' % name[i], xy=(ba_pit[i], h[i]), xytext=(-5, 5), textcoords='offset points',  size=8)

    # PLOT a 0 LINE
    ax[1].axvline(0, color='k', linestyle='dashed')

    # # Plot the Legend
    # # plot the bar plot also on the ax2 but with 0 values just for the legend
    ax[1].barh(0, 0, 0, align='center', linewidth=1, alpha=1, color='grey', label='Flaeche der Hoehenstufen')
    ax[1].legend(bbox_to_anchor=(-0.7, 1), loc=2, prop={'size': 10})
    # remove white space
    plt.subplots_adjust(wspace=0, hspace=0)

    plt.savefig('mb_plot_2024.png', dpi=100)
    plt.show()


def makeStakePlot():
    stks = pd.read_csv('Pegel2024_forplot.csv', sep=',')
    stks.index = stks['Pegel']
    # print(stks)
    stks.drop('Pegel', axis=1, inplace=True)
    stks = stks.T
    #print(stks)
    # stks.drop('6', axis=1, inplace=True)
    # stks.drop('8', axis=1, inplace=True)
    # stks.drop('15oben', axis=1, inplace=True)
    stks.drop(['5', '6', '7', '8', '9', '13', '15oben'], axis=1, inplace=True)
    stks = stks.astype(float)#, inplace=True)
    stks = stks.rename(columns={'15unten': '15'})
    stks.index = pd.to_datetime(stks.index, dayfirst=True)#format='%d.%m.%y')
    print(stks)
    # stop
    LINE_STYLES = ['solid', 'dashed', 'dotted']#, 'dashdot', 'dotted']
    NUM_STYLES = len(LINE_STYLES)
    fig = plt.figure(figsize=(10,8))
    # my_cmap = ListedColormap(seaborn.cubehelix_palette(12, start=.1, rot=1, dark=0, light=.7).as_hex())
    my_cmap = ListedColormap(seaborn.color_palette('deep',12).as_hex())
    n = len(stks.columns)
    color=iter(my_cmap(np.linspace(0,1,n)))
    ax = fig.add_subplot(111)


    stksInt = stks.interpolate(method='time', axis=0)
    print(stksInt)
    stksInt = stksInt.astype(float)#,
    print(stksInt)
    for i, c in enumerate(stks.columns):
        clr=next(color)
        ax.plot(stksInt.index.values, stksInt[c].values, label = c, color=clr, linestyle=LINE_STYLES[i%NUM_STYLES])
        ax.plot(stks.index.values, stks[c].values, marker= 'o', color=clr, linestyle=LINE_STYLES[i%NUM_STYLES])

    # ax.annotate(c, xy=(stksT[c].mean(), stksT[c].values.mean()), color=c,
    #       xycoords="data",
    #       va="center", ha="center",
    #       bbox=dict(boxstyle="round", fc="w"))
    ax.set_xticks(pd.date_range(start='2024/7/1', periods=3, freq='M'))
    # set monthly locator
    #ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    # set formatter
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    ax.set_ylabel('Ablation [cm Eis]')
    ax.set_xlabel('Datum')
    ax.set_ylim([0, 600])
    ax.set_title('Ablationsverlauf an den Pegeln')
    ax.grid(axis='y')

    # set font and rotation for date tick labels
    ax.legend(bbox_to_anchor=(1.12, 0.9), prop={'size': 10})
    plt.savefig('stakes_plot_2024.jpg', format='jpg', dpi=100)
    plt.show()


def align_yaxis(ax1, ax2):
    ## adapted from https://stackoverflow.com/a/54355867/9830710
    y_lims = np.array([ax.get_ylim() for ax in [ax1, ax2]])

    # force 0 to appear on both axes, comment if don't need
    y_lims[:, 0] = y_lims[:, 0].clip(None, 0)
    y_lims[:, 1] = y_lims[:, 1].clip(0, None)

    # normalize both axes
    y_mags = (y_lims[:,1] - y_lims[:,0]).reshape(len(y_lims),1)
    y_lims_normalized = y_lims / y_mags

    # find combined range
    y_new_lims_normalized = np.array([np.min(y_lims_normalized), np.max(y_lims_normalized)])

    # denormalize combined range to get new axes
    new_lim1, new_lim2 = y_new_lims_normalized * y_mags
    ax1.set_ylim(new_lim1)
    ax2.set_ylim(new_lim2)


def readHDdata(fname, param, skip):
    out = pd.read_csv(fname, delimiter=';', skiprows=skip, na_values='Lücke',
                      names=['date', param], encoding='unicode_escape', decimal=',')
    out[param] = pd.to_numeric(out[param])

    out.set_index('date', inplace=True)
    print(out)
    out.index = pd.to_datetime(out.index, format='%d.%m.%Y %H:%M:%S   ')


    if param == 'N':
        monthly = out.resample('M').sum()
    if param == 'T':
        monthly = out.resample('M').mean()
    # print(out)

    return (out, monthly)


# use this if only monthly data available
def makeKlimaPlot():
    clim = pd.read_csv('klima/klima.csv')

    # in past years we also had daily data, lines dealing with those are commented out.
    LTmonatJam = readHDdata('klima/LT115451.dat', 'T', 20)
    #LTJam = readHDdata('Bericht/meteo/LT115451.csv', 'T', 20)
    NmonatJam = readHDdata('klima/N115451.dat', 'N', 20)

    LTmonatGal = readHDdata('klima/LT101949.dat', 'T', 27)
    NmonatGal = readHDdata('klima/N101949.dat', 'N', 27)
    print(NmonatGal)
    print(LTmonatGal)
    print(NmonatJam)
    print(LTmonatJam)

    # NmonatGal = NmonatGal.loc[NmonatGal.index > '2023-02-01']


    ix = pd.date_range('15/10/2022', periods=12, freq=DateOffset(months=1))
    N_monat = pd.DataFrame(index=ix)

    # N_monat['NGal'] = NGal.resample('M').sum()[:-1].values

    # GALTÜR 
    N_monat['klima_Gal_N'] = clim.Klima_NS.values
    # N_monat['NGal'] = np.nan
    N_monat['NGal'] = NmonatGal.values[:-1]
    
    N_monat['anom_Gal_N'] = N_monat['NGal'].values-N_monat['klima_Gal_N'].values
    
    N_monat['TGal'] = LTmonatGal.values[:-1]

    # N_monat['TGal'] = TGal.resample('M').mean()[:-1].values
    N_monat['klima_Gal_T'] = clim.Klima_T_1951_2000.values
    N_monat['anom_Gal_T'] = N_monat['TGal'].values-N_monat['klima_Gal_T'].values


    # JAM
    N_monat['T_Jam'] = LTmonatJam.values[:-1]

    N_monat['N_Jam'] = NmonatJam.values[:-1]


    print(N_monat)

    N_monat['T_Jam_Gal'] = N_monat['T_Jam'].values - N_monat['TGal'].values
    N_monat['N_Jam_Gal'] = N_monat['N_Jam'].values - N_monat['NGal'].values

    print(N_monat)

    # Galtür Table

    Monat_Gal = N_monat[['TGal', 'klima_Gal_T', 'anom_Gal_T', 'NGal', 'klima_Gal_N', 'anom_Gal_N']].round(1)
    Monat_Gal.index = ['Oktober', 'November', 'Dezember', 'Januar', 'Februar', 'März', 'April',
                       'Mai', 'Juni', 'Juli', 'August', 'September']
    dfGal = pd.DataFrame(index=['Sommer', 'Winter', 'hydrolog. Jahr'], columns=['TGal', 'klima_Gal_T', 'anom_Gal_T', 'NGal', 'klima_Gal_N', 'anom_Gal_N'])
    for c in ['TGal', 'klima_Gal_T', 'anom_Gal_T']:
        dfGal.loc['Sommer', c] = Monat_Gal[c][7:].mean().round(1)
        dfGal.loc['Winter', c] = Monat_Gal[c][:7].mean().round(1)
        print('winter', Monat_Gal[c][:7])
        dfGal.loc['hydrolog. Jahr', c] = Monat_Gal[c].mean().round(1)
    for c in ['NGal', 'klima_Gal_N', 'anom_Gal_N']:
        dfGal.loc['Sommer', c] = Monat_Gal[c][7:].sum().round(0).astype(int)
        dfGal.loc['Winter', c] = Monat_Gal[c][:7].sum().round(0).astype(int)
        dfGal.loc['hydrolog. Jahr', c] = Monat_Gal[c].sum().round(0).astype(int)

    # Monat_Gal = Monat_Gal.append(dfGal)
    Monat_Gal = pd.concat([Monat_Gal, dfGal], ignore_index=True)
    Monat_Gal['NGal'] = Monat_Gal['NGal'].astype(float).round(0).astype(int)
    Monat_Gal['anom_Gal_N'] = Monat_Gal['anom_Gal_N'].astype(float).round(0).astype(int)
    
    Monat_Gal.index = ['Oktober', 'November', 'Dezember', 'Januar', 'Februar', 'März', 'April',
                       'Mai', 'Juni', 'Juli', 'August', 'September', 'Sommer', 'Winter', 'hydrolog. Jahr']
    # print(dfGal)
    print(Monat_Gal.astype(str).to_latex())

    

    # JAM Table
    Monat_Jam = N_monat[['T_Jam', 'N_Jam', 'T_Jam_Gal', 'N_Jam_Gal']].round(1)
    Monat_Jam.index = ['Oktober', 'November', 'Dezember', 'Januar', 'Februar', 'März', 'April',
                       'Mai', 'Juni', 'Juli', 'August', 'September']

    dfJam = pd.DataFrame(index=['Sommer', 'Winter', 'hydrolog. Jahr'], columns=['T_Jam', 'N_Jam', 'T_Jam_Gal', 'N_Jam_Gal'])
    dfJam.loc['Sommer', 'T_Jam'] = Monat_Jam['T_Jam'][7:].mean().round(1)
    dfJam.loc['Sommer', 'T_Jam_Gal'] = Monat_Jam['T_Jam_Gal'][7:].mean().round(1)
    dfJam.loc['Winter', 'T_Jam'] = Monat_Jam['T_Jam'][:7].mean().round(1)
    dfJam.loc['Winter', 'T_Jam_Gal'] = Monat_Jam['T_Jam_Gal'][:7].mean().round(1)
    dfJam.loc['hydrolog. Jahr', 'T_Jam'] = Monat_Jam['T_Jam'].mean().round(1)
    dfJam.loc['hydrolog. Jahr', 'T_Jam_Gal'] = Monat_Jam['T_Jam_Gal'].mean().round(1)

    dfJam.loc['Sommer', 'N_Jam'] = Monat_Jam['N_Jam'][7:].sum().round(1)
    dfJam.loc['Sommer', 'N_Jam_Gal'] = Monat_Jam['N_Jam_Gal'][7:].sum().round(1)
    dfJam.loc['Winter', 'N_Jam'] = Monat_Jam['N_Jam'][:7].sum().round(1)
    dfJam.loc['Winter', 'N_Jam_Gal'] = Monat_Jam['N_Jam_Gal'][:7].sum().round(1)
    dfJam.loc['hydrolog. Jahr', 'N_Jam'] = Monat_Jam['N_Jam'].sum().round(1)
    dfJam.loc['hydrolog. Jahr', 'N_Jam_Gal'] = Monat_Jam['N_Jam_Gal'].sum().round(1)

    # Monat_Jam = Monat_Jam.append(dfJam)
    Monat_Jam = pd.concat([Monat_Jam, dfJam], ignore_index=False)
    Monat_Jam['N_Jam'] = Monat_Jam['N_Jam'].astype(float).round(0)#.astype(int)
    Monat_Jam['N_Jam_Gal'] = Monat_Jam['N_Jam_Gal'].astype(float).round(0)#.astype(int)

    # remove trailing zeros after rounding precip columns - hacky, be careful.
    
    Monat_Jam.loc[~Monat_Jam['N_Jam'].isna()]['N_Jam'] = Monat_Jam.loc[~Monat_Jam['N_Jam'].isna()]['N_Jam'].astype(int)
    Monat_Jam.loc[~Monat_Jam['N_Jam_Gal'].isna()]['N_Jam_Gal'] = Monat_Jam.loc[~Monat_Jam['N_Jam_Gal'].isna()]['N_Jam_Gal'].astype(int)

    Monat_Jam['N_Jam'] = Monat_Jam['N_Jam'].astype(str).str.replace('.0', '')
    Monat_Jam['N_Jam_Gal'] = Monat_Jam['N_Jam_Gal'].astype(str).str.replace('.0', '')
    print(Monat_Jam)
    print(Monat_Jam.astype(str).to_latex(index=True))


    # Make figures
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111)
    # ax.bar(ix, clim.Klima_NS.values, 15, align='center', alpha=1, color='grey')
    ax.bar(ix, N_monat['anom_Gal_N'].values, 15, align='center', alpha=1, color='grey')
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.set_ylabel('Abweichung Niederschlag [mm]', color='grey')
    ax.tick_params(axis='y', labelcolor='grey')
    ax2 = ax.twinx()
    # ax2.plot(ix, clim.Klima_T_1951_2000.values, color='r')
    ax2.plot(ix, N_monat['anom_Gal_T'].values, color='r')
    align_yaxis(ax, ax2)
    ax2.set_ylabel('Abweichung Temperatur [°C]', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax.axhline(0, color='k', linestyle='solid')
    ax2.set_xticks(ix)
    ax2.tick_params(axis='x', which='minor', bottom=False)
    ax2.set_xticklabels(clim.Monat.values)
    ax.set_title('Station Galtür - Abweichung 2022/23 vom langjährigen Mittel 1951-2000')
    plt.savefig('klima_plot_2023_Abweichungen.jpg', format='jpg', dpi=100)
  
    fig2 = plt.figure(figsize=(10, 7))
    ax = fig2.add_subplot(111)  
    ax.bar(ix, clim.Klima_NS.values, 15, align='center', alpha=1, color='grey', label='Klimamittel Galtür NS')
    ax.bar(ix, N_monat['N_Jam'].values, 20, align='center', alpha=0.3, color='k', label='JTH NS')
    # ax.plot(ix, clim.Klima_NS.values, 15, align='center', alpha=1, color='grey')
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.set_ylabel('Niederschlag [mm]', color='grey')
    ax.tick_params(axis='y', labelcolor='grey')
    ax2 = ax.twinx()
    ax2.plot(ix, N_monat['T_Jam'].values, color='r', label='JTH LT (monatlich)')
    ax2.plot(ix, clim.Klima_T_1951_2000.values, color='r', alpha=0.5, label='Klimamittel Galtür LT (monatlich)')
    # ax2.plot(LTJam.index.values, LTJam['T'].values, color='r', linestyle='--', linewidth=0.5, label='JTH LT (täglich)')
    align_yaxis(ax, ax2)
    ax2.set_ylabel('Temperatur [°C]', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax.axhline(0, color='k', linestyle='solid')
    ax2.set_xticks(ix)
    ax2.tick_params(axis='x', which='minor', bottom=False)
    ax2.set_xticklabels(clim.Monat.values)
    ax.set_title('Station JTH: Messungen 2022/23 (Vergleich Klimamittel Galtür)')
    ax.legend()
    ax2.legend(loc="lower right")
    plt.savefig('klima_plot_2023_JTH.jpg', format='jpg', dpi=100)



# use this if daily data available
def makeKlimaPlot_dailydata():
    year = '2023'
    clim = pd.read_csv('Klima/klima.csv')

    LTdailyJam, LTmonatJam = readHDdata('Klima/LT115451.csv', 'T', 20)
    NdailyJam, NmonatJam = readHDdata('Klima/N115451.csv', 'N', 20)

    LTdailyGal, LTmonatGal = readHDdata('Klima/LT101949.csv', 'T', 27)
    NdailyGal, NmonatGal = readHDdata('Klima/N101949.csv', 'N', 27)

    print(NdailyGal)
    print(LTdailyGal)
    print(NdailyJam)
    print(LTdailyJam)


    print(NmonatGal)
    print(LTmonatGal)
    print(NmonatJam)
    print(LTmonatJam)

    # NmonatGal = NmonatGal.loc[NmonatGal.index > '2023-02-01']

    ix = pd.date_range('15/10/'+year, periods=12, freq=DateOffset(months=1))
    N_monat = pd.DataFrame(index=ix)

    # N_monat['NGal'] = NGal.resample('M').sum()[:-1].values

    # GALTÜR 
    N_monat['klima_Gal_N'] = clim.Klima_NS.values
    # N_monat['NGal'] = np.nan
    N_monat['NGal'] = NmonatGal.values[:-1]
    
    N_monat['anom_Gal_N'] = N_monat['NGal'].values-N_monat['klima_Gal_N'].values
    
    N_monat['TGal'] = LTmonatGal.values[:-1]

    # N_monat['TGal'] = TGal.resample('M').mean()[:-1].values
    N_monat['klima_Gal_T'] = clim.Klima_T_1951_2000.values
    N_monat['anom_Gal_T'] = N_monat['TGal'].values-N_monat['klima_Gal_T'].values

    # JAM
    N_monat['T_Jam'] = LTmonatJam.values[:-1]
    N_monat['N_Jam'] = NmonatJam.values[:-1]

    N_monat['T_Jam_Gal'] = N_monat['T_Jam'].values - N_monat['TGal'].values
    N_monat['N_Jam_Gal'] = N_monat['N_Jam'].values - N_monat['NGal'].values

    # Galtür Table
    Monat_Gal = N_monat[['TGal', 'klima_Gal_T', 'anom_Gal_T', 'NGal', 'klima_Gal_N', 'anom_Gal_N']].round(1)
    Monat_Gal.index = ['Oktober', 'November', 'Dezember', 'Januar', 'Februar', 'März', 'April',
                       'Mai', 'Juni', 'Juli', 'August', 'September']
    dfGal = pd.DataFrame(index=['Sommer', 'Winter', 'hydrolog. Jahr'], columns=['TGal', 'klima_Gal_T', 'anom_Gal_T', 'NGal', 'klima_Gal_N', 'anom_Gal_N'])
    for c in ['TGal', 'klima_Gal_T', 'anom_Gal_T']:
        dfGal.loc['Sommer', c] = Monat_Gal[c][7:].mean().round(1)
        dfGal.loc['Winter', c] = Monat_Gal[c][:7].mean().round(1)
        print('winter', Monat_Gal[c][:7])
        dfGal.loc['hydrolog. Jahr', c] = Monat_Gal[c].mean().round(1)
    for c in ['NGal', 'klima_Gal_N', 'anom_Gal_N']:
        dfGal.loc['Sommer', c] = Monat_Gal[c][7:].sum().round(0).astype(int)
        dfGal.loc['Winter', c] = Monat_Gal[c][:7].sum().round(0).astype(int)
        dfGal.loc['hydrolog. Jahr', c] = Monat_Gal[c].sum().round(0).astype(int)

    # Monat_Gal = Monat_Gal.append(dfGal)
    Monat_Gal = pd.concat([Monat_Gal, dfGal], ignore_index=True)
    Monat_Gal['NGal'] = Monat_Gal['NGal'].astype(float).round(0).astype(int)
    Monat_Gal['anom_Gal_N'] = Monat_Gal['anom_Gal_N'].astype(float).round(0).astype(int)
    
    Monat_Gal.index = ['Oktober', 'November', 'Dezember', 'Januar', 'Februar', 'März', 'April',
                       'Mai', 'Juni', 'Juli', 'August', 'September', 'Sommer', 'Winter', 'hydrolog. Jahr']
    # print(dfGal)
    print(Monat_Gal.astype(str).to_latex())


    # JAM Table
    Monat_Jam = N_monat[['T_Jam', 'N_Jam', 'T_Jam_Gal', 'N_Jam_Gal']].round(1)
    Monat_Jam.index = ['Oktober', 'November', 'Dezember', 'Januar', 'Februar', 'März', 'April',
                       'Mai', 'Juni', 'Juli', 'August', 'September']

    dfJam = pd.DataFrame(index=['Sommer', 'Winter', 'hydrolog. Jahr'], columns=['T_Jam', 'N_Jam', 'T_Jam_Gal', 'N_Jam_Gal'])
    dfJam.loc['Sommer', 'T_Jam'] = Monat_Jam['T_Jam'][7:].mean().round(1)
    dfJam.loc['Sommer', 'T_Jam_Gal'] = Monat_Jam['T_Jam_Gal'][7:].mean().round(1)
    dfJam.loc['Winter', 'T_Jam'] = Monat_Jam['T_Jam'][:7].mean().round(1)
    dfJam.loc['Winter', 'T_Jam_Gal'] = Monat_Jam['T_Jam_Gal'][:7].mean().round(1)
    dfJam.loc['hydrolog. Jahr', 'T_Jam'] = Monat_Jam['T_Jam'].mean().round(1)
    dfJam.loc['hydrolog. Jahr', 'T_Jam_Gal'] = Monat_Jam['T_Jam_Gal'].mean().round(1)

    dfJam.loc['Sommer', 'N_Jam'] = Monat_Jam['N_Jam'][7:].sum().round(1)
    dfJam.loc['Sommer', 'N_Jam_Gal'] = Monat_Jam['N_Jam_Gal'][7:].sum().round(1)
    dfJam.loc['Winter', 'N_Jam'] = Monat_Jam['N_Jam'][:7].sum().round(1)
    dfJam.loc['Winter', 'N_Jam_Gal'] = Monat_Jam['N_Jam_Gal'][:7].sum().round(1)
    dfJam.loc['hydrolog. Jahr', 'N_Jam'] = Monat_Jam['N_Jam'].sum().round(1)
    dfJam.loc['hydrolog. Jahr', 'N_Jam_Gal'] = Monat_Jam['N_Jam_Gal'].sum().round(1)

    # Monat_Jam = Monat_Jam.append(dfJam)
    Monat_Jam = pd.concat([Monat_Jam, dfJam], ignore_index=False)
    Monat_Jam['N_Jam'] = Monat_Jam['N_Jam'].astype(float).round(0)#.astype(int)
    Monat_Jam['N_Jam_Gal'] = Monat_Jam['N_Jam_Gal'].astype(float).round(0)#.astype(int)

    # remove trailing zeros after rounding precip columns - hacky, be careful.
    
    Monat_Jam.loc[~Monat_Jam['N_Jam'].isna()]['N_Jam'] = Monat_Jam.loc[~Monat_Jam['N_Jam'].isna()]['N_Jam'].astype(int)
    Monat_Jam.loc[~Monat_Jam['N_Jam_Gal'].isna()]['N_Jam_Gal'] = Monat_Jam.loc[~Monat_Jam['N_Jam_Gal'].isna()]['N_Jam_Gal'].astype(int)

    Monat_Jam['N_Jam'] = Monat_Jam['N_Jam'].astype(str).str.replace('.0', '')
    Monat_Jam['N_Jam_Gal'] = Monat_Jam['N_Jam_Gal'].astype(str).str.replace('.0', '')
    # print(Monat_Jam)
    print(Monat_Jam.astype(str).to_latex(index=True))



    # Make figures
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111)
    # ax.bar(ix, clim.Klima_NS.values, 15, align='center', alpha=1, color='grey')
    ax.bar(ix, N_monat['anom_Gal_N'].values, 15, align='center', alpha=1, color='grey')
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.set_ylabel('Abweichung Niederschlag [mm]', color='grey')
    ax.tick_params(axis='y', labelcolor='grey')
    ax2 = ax.twinx()
    # ax2.plot(ix, clim.Klima_T_1951_2000.values, color='r')
    ax2.plot(ix, N_monat['anom_Gal_T'].values, color='r')
    align_yaxis(ax, ax2)
    ax2.set_ylabel('Abweichung Temperatur [°C]', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax.axhline(0, color='k', linestyle='solid')
    ax2.set_xticks(ix)
    ax2.tick_params(axis='x', which='minor', bottom=False)
    ax2.set_xticklabels(clim.Monat.values)
    ax.set_title('Station Galtür - Abweichung 2023/24 vom langjährigen Mittel 1951-2000')
    plt.savefig('klima_plot_2024_Abweichungen.jpg', format='jpg', dpi=100)
  
    fig2 = plt.figure(figsize=(10, 7))
    ax = fig2.add_subplot(111)  
    ax.bar(ix, clim.Klima_NS.values, 15, align='center', alpha=1, color='grey', label='Klimamittel Galtür NS')
    ax.bar(ix, N_monat['N_Jam'].values, 20, align='center', alpha=0.3, color='k', label='JTH NS')
    # ax.plot(ix, clim.Klima_NS.values, 15, align='center', alpha=1, color='grey')
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.set_ylabel('Niederschlag [mm]', color='grey')
    ax.tick_params(axis='y', labelcolor='grey')
    ax2 = ax.twinx()
    ax2.plot(ix, N_monat['T_Jam'].values, color='r', label='JTH LT (monatlich)')
    ax2.plot(ix, clim.Klima_T_1951_2000.values, color='r', alpha=0.5, label='Klimamittel Galtür LT (monatlich)')
    ax2.plot(LTdailyJam.index.values, LTdailyJam['T'].values, color='r', linestyle='--', linewidth=0.5, label='JTH LT (täglich)')
    align_yaxis(ax, ax2)
    ax2.set_ylabel('Temperatur [°C]', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax.axhline(0, color='k', linestyle='solid')
    ax2.set_xticks(ix)
    ax2.tick_params(axis='x', which='minor', bottom=False)
    ax2.set_xticklabels(clim.Monat.values)
    ax.set_title('Station JTH: Messungen 2023/24 (Vergleich Klimamittel Galtür)')
    ax.legend()
    ax2.legend(loc="lower right")
    plt.savefig('klima_plot_2024_JTH.jpg', format='jpg', dpi=100)



def makeStakeMap():
    pits= gpd.read_file('FS2023.shp')
    # pd.DataFrame({'longitude': [10.148485], 'latitude': [46.853544]})
    # pit2022point['title'] = 'JS II'
    # geometry = gpd.points_from_xy(pit2022point.longitude, pit2022point.latitude, crs="EPSG:4326")
    # pits = gpd.GeoDataFrame(pit2022point, geometry=geometry)

    # pits = gpd.read_file('Bericht/Jam_Schaechte.json')
    # pits = pits[['title', 'geometry']]
    # pits = pits.to_crs(epsg=31257)
    # pits = pits.loc[pits['title'].isin(['JS II', 'JS VI', 'JS VII'])]
    print(pits)
    pits = pits.to_crs(epsg=4326)

    df = pd.read_csv('coordinates2023_2.csv')
    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
    stakes = gpd.GeoDataFrame(df[['name']], geometry=geometry)
    stakes.crs = {'init': 'epsg:4326'}
    stakes = stakes.to_crs(epsg=4326)
    stakes = stakes.loc[stakes.name != '15oben']
    #print(stakes)

    pits_stakes = pd.concat([stakes, pits])
    pits_stakes = pits_stakes[['name', 'geometry']]
    pits_stakes['stake_id'] = pits_stakes['name'].fillna('JS2')
    print(pits_stakes, pits_stakes.crs)
    pits_stakes.to_file('JAM_PegelSchacht2023.shp') 

    GG = gpd.read_file('data_andrea/GIS/jam22_sentinel_okt23.shp')
    GG['new_column'] = 0
    GG = GG.dissolve(by='new_column')
    GG = GG.to_crs(epsg=4326)
    print(GG.crs)

    GG22 = gpd.read_file('data_andrea/GIS/jam22_sentinel_sep_22.shp')
    GG22['new_column'] = 0
    GG22 = GG22.dissolve(by='new_column')
    GG22 = GG22.to_crs(epsg=4326)
    # GG.to_file('Gletschergrenze_Update2020.shp') 
    


    # contours = gpd.read_file('daten/cont_18_50.shp')
    # contours = contours.to_crs(epsg=31257)
    # print(contours.crs, GG.crs)

    fig, ax = plt.subplots(1, 1, figsize=(10,7))

    GG.plot(ax=ax, color='grey', alpha=0.3, label='Grenze Oktober 2023')
    GG22.boundary.plot(ax=ax, color='k', linewidth=1, label='Grenze September 2022')
    GG.boundary.plot(ax=ax, color='grey', label='Grenze Oktober 2023')
    pits.plot(ax=ax, marker='s', color='g', label='Schächte')
    for x, y in zip(pits.geometry.x, pits.geometry.y):
        ax.annotate('FS2023', xy=(x, y), xytext=(3, 3), textcoords="offset points")

    stakes.plot(ax=ax, marker='o', color='g', label='Pegel')
    for x, y, name in zip(stakes.geometry.x, stakes.geometry.y, stakes.name):
        ax.annotate(name, xy=(x, y), xytext=(3, 3), textcoords="offset points")

    #contours.plot(ax=ax, color='k', linewidth=0.5)
    # ax.set_ylim([189900, 192100])
    # ax.set_xlim([135500, 138800])
    ax.legend()
    plt.savefig('Pegelplan2023.jpg', format='jpg', dpi=100)
    plt.show()


# makeStakePlot()
makeMBPlot()
# makeKlimaPlot_dailydata()

# makeStakeMap()
plt.show()




