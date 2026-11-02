import numpy as np
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt
from matplotlib import cm

# script to generate different table formats for data submissions to WGMS and pangaea dataset.
# WGMS format uses glacier-wide data, data per elevation band, and point scale data (stake values, probe points, and snow pits)

# set up paths to input files
# glacier name abbreviation
gl = 'JAM'
# hydrological year
yr = 2026

## to get the stake data:
# read stake data from summary excel file with annual stake data (this can be adapted to use another version of the data.
# it needs lat,lon coordinates, elevation, and the annual stake value.)
fn = '/Users/leahartl/Desktop/JAM/Pegel_Jam.xlsx'


## to get probe and pit point data for the winter mass balance:
# shapefile with spring probe points:
fnPts_Spring = '/Users/leahartl/Desktop/Jam2026/winter/sondierungen_schacht_20260423.geojson'
# identify snow pit name in the file. this may have to be adapted if there are separate files for
# probe points and pits, or some other data format is used.
pitname = 'SCHACHT! 29'
# set spring snow pit density (hardcoded value)
pitdensity = 363 #kg/m3
# set date of spring survey (if table is for floating date format and no correction was applied, otherwise adapt!)
springdate = '2026-04-23'
# this is an output table from the main mass balance script.
fnBands = '/Users/leahartl/Desktop/Jam2026/results/table_MB_all.csv'
# -----


def PointsAnnualWGMS(yr, fname, fpts, pitname, pitdensity, springdate):
    # stakes:
    temp = pd.read_excel(fname, str(yr), header=0)
    print(temp)

    WGMS = pd.DataFrame(columns=['glacier_name', 'glacier_id', 'year'])

    WGMS['original_id'] = temp['name'].values
        
    WGMS['time_system'] = 'fixed'
    WGMS['begin_date'] = str(yr-1)+'-10-01'
    WGMS['±days_begin'] = 0
    WGMS['end_date'] = str(yr)+'-09-30'
    WGMS['±days_end'] = 0
    WGMS['latitude'] = temp['Y_coord']
    WGMS['longitude'] = temp['X_coord']
    WGMS['elevation'] = temp['Z_value']
    # balance in m w.e.! check file to ensure the correct column name is used here.
    WGMS['balance'] = temp['mm_we']/1000
    WGMS['±mwe'] = np.nan
    WGMS['density'] = np.nan
    WGMS['±density'] = np.nan
    WGMS['method'] = 'stake'
    WGMS['balance_code'] = 'annual'
    WGMS['remarks'] = 'assumed density of ice: 900kg/m3; no snow at stake positions during final measurements'

    # pits:
    pts = pd.DataFrame(columns=WGMS.columns)
    pt = gpd.read_file(fpts)

    pts['original_id'] = pt['name']
    pts['time_system'] = 'measured'
    pts['begin_date'] = str(yr-1)+'-10-01'
    pts['±days_begin'] = np.nan
    pts['end_date'] = springdate
    pts['±days_end'] = 0
    pts['latitude'] = pt['lat']
    pts['longitude'] = pt['lon']
    pts['elevation'] = pt['elev']

    pts['balance'] = pt['WW_m'].round(decimals=0).astype(int)
    pts['±mwe'] = np.nan
    pts['density'] = np.nan
    pts['±density'] = np.nan
    pts['method'] = 'probe'
    pts['balance_code'] = 'winter'

    pts.loc[pts['original_id'] == pitname, 'method'] = 'pit'

    pts['remarks'] = 'density measured at snow pit; same density assumed for probe points.'

    # merge stakes (annual) and pits/probes (winter)
    WGMS = pd.concat([WGMS, pts])

    WGMS['glacier_name'] = 'JAMTAL F.'
    WGMS['glacier_id'] = 480
    WGMS['year'] = yr

    WGMS.to_csv('/Users/leahartl/Desktop/Jam2026/Tabellen/mass_balance_point_'+str(yr)+'_JAM.csv', index=False)
    # print(WGMS)


def BandsAnnualWGMS(yr, fname):
    # load file with band values:
    temp = pd.read_csv(fname)
    # drop nan row with summary values
    temp = temp.dropna()
    print(temp) 

    WGMS = pd.DataFrame(columns=['glacier_name', 'glacier_id', 'year'])
    WGMS['lower_elevation'] = temp.Höhenstufe - 25
    WGMS['upper_elevation'] = temp.Höhenstufe + 25
    WGMS['area m2'] = temp['Fläche_km2']*1e6
    WGMS['winter_balance'] = temp['b_wi_m']#*1e-3
    WGMS['±mwe_wb'] = np.nan
    WGMS['summer_balance'] = temp['b_so_m']#*1e-3
    WGMS['±mwe_sb'] = np.nan
    WGMS['annual_balance'] = temp['b_m']#*1e-3
    WGMS['±mwe'] = np.nan
    WGMS['remarks'] = ''

    WGMS[['winter_balance', 'summer_balance', 'annual_balance']] = WGMS[['winter_balance', 'summer_balance', 'annual_balance']].astype(float).round(decimals=3)

    WGMS['glacier_name'] = 'JAMTAL F.'
    WGMS['glacier_id'] = 480
    WGMS['year'] = yr

    WGMS.to_csv('/Users/leahartl/Desktop/Jam2026/Tabellen/mass_balance_band_'+str(yr)+'_JAM.csv', index=False)
    


def GlacierwideAnnualWGMS(yr, fname):
    # load file with band values:
    temp = pd.read_csv(fname)
    # keep only last row with the summary values:
    temp = temp.loc[temp.Höhenstufe.isna()]
    print(temp) 


    WGMS = pd.DataFrame(columns=['glacier_name','glacier_id', 'outline_id', 'year'], index=[0])
   
    WGMS['time_system'] = 'fixed'
    WGMS['begin_date'] = str(yr-1)+'-10-01'
    WGMS['±days_begin'] = np.nan
    WGMS['midseason_date'] = str(yr)+'-04-30'
    WGMS['±days_mid'] = np.nan
    WGMS['end_date'] = str(yr)+'-09-30'
    WGMS['±days_end'] = np.nan
    WGMS['ela_position'] = 'above'
    WGMS['ela'] = np.nan
    WGMS['±ela_m'] = np.nan

    WGMS['aar'] = 0/temp['Fläche_km2'].values[0]*1e6

    WGMS['area m2'] = temp['Fläche_km2'].values[0]*1e6
    WGMS['winter_balance'] = temp['b_wi_m'].values[0]#*1e-3
    WGMS['±mwe_wb'] = np.nan
    WGMS['summer_balance'] = temp['b_so_m'].values[0]#*1e-3
    WGMS['±mwe_sb'] = np.nan
    WGMS['annual_balance'] = temp['b_m'].values[0]#*1e-3
    WGMS['±mwe'] = np.nan

    WGMS['investigators'] = 'Marcela V. Lauria (1) | Lea Hartl (1) | Andrea Fischer (1, 2)'
    WGMS['agencies'] = '1. Österreichische Akademie der Wissenschaften | 2. Verein Gletscher und Klima | 3. Hydrographischer Dienst der Abteilung Wasserwirtschaft des Amtes der Tiroler Landesregierung'
    WGMS['references'] = 'Fischer et al. (https://doi.org/10.1594/PANGAEA.818772)'
    WGMS['remarks'] = 'Funding provided by Hydrographischer Dienst der Abteilung Wasserwirtschaft des Amtes der Tiroler Landesregierung'

    WGMS[['winter_balance', 'summer_balance', 'annual_balance']] = WGMS[['winter_balance', 'summer_balance', 'annual_balance']].astype(float).round(decimals=3)

    WGMS['glacier_name'] = 'JAMTAL F.'
    WGMS['glacier_id'] = 480
    WGMS['year'] = yr
    WGMS['outline_id'] = np.nan
    print(WGMS)
    WGMS.to_csv('/Users/leahartl/Desktop/Jam2026/Tabellen/mass_balance_'+str(yr)+'_JAM.csv', index=False)
    


def BandsAnnualPangaea(yr, fname):
    # load file with band values:
    temp = pd.read_csv(fname)
    print(temp)
    summary = temp.loc[temp.Höhenstufe.isna()]
    # drop nan row with summary values
    temp = temp.dropna()

    pan = pd.DataFrame(columns=['date_begin', 'date_end'])
    pan['lower_elevation'] = temp.Höhenstufe - 25
    pan['upper_elevation'] = temp.Höhenstufe + 25
    pan['date_begin'] = yr - 1
    pan['date_end'] = yr
    pan['Saz'] = temp.Fläche_km2.values
    pan['Baz'] = temp.balance_m3.values
    pan['baz'] = temp.b_m.values
    pan['bsaz'] = temp.b_so_m.values
    pan['bwaz'] = temp.b_wi_m.values

    print(pan)

    pan.to_csv('/Users/leahartl/Desktop/Jam2026/Tabellen/pangaea_'+str(yr)+'_JAM.csv', index=False)
    

BandsAnnualPangaea(yr, fnBands)

GlacierwideAnnualWGMS(yr, fnBands)

PointsAnnualWGMS(yr, fn, fnPts_Spring, pitname, pitdensity, springdate)

BandsAnnualWGMS(yr, fnBands)


