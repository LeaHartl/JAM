import numpy as np
import pandas as pd
import datetime as dt
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.dates as mdates
# from matplotlib.lines import Line2D
# import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
# from shapely.geometry import Point
import glob
import Uncertainties as unc


def makeTableAnnual(yrs, fname, gl):

    stks_annual = []

    for yr in yrs:
        print(yr)
        temp = pd.read_excel(fname, str(yr), header=0)
        # print(temp)
        basics = pd.DataFrame(columns=['name'])
        basics['name'] = temp[temp.columns.values[0]]
        basics['x_pos'] = temp['X_coord']
        basics['y_pos'] = temp['Y_coord']
        basics['z_pos'] = temp['Z_value']

        # 4 stands for estimated from closest measurement
        basics['position_quality'] = 4

        # raw mass balance in cm ice is not available for the fixed dates because only the final
        # corrected values was documented.
        basics['mb_raw'] = np.nan 

        # mm WE value interpolated from last observation to end of hydrol. year.
        # this is always in the last column in the excel files. Make sure there are no
        # inconsistencies in the file to get the correct column!!
        basics['mb_we'] = temp[temp.columns.values[-1]].astype(float)#*10

        # deal with densities: the fixed date mb we value is derived based on a combination of ice and fresh snow densities.
        # exact density is unknown for the fixed dates:
        basics['density'] = np.nan
        # quality flag for ice & snow density combinatinon.
        # this is associated with ~10% raw mb uncertainty. we don't have raw uncertainty, so we will apply this to mb we value.
        basics['density_quality'] = 5
            
        # fixed start and end dates:
        basics['date0'] = int(str(yr-1)+'1001')
        basics['date1'] = int(str(yr)+'0930')

        basics['period'] = (pd.to_datetime(basics['date1'].astype(str), format='%Y%m%d') - pd.to_datetime(basics['date0'].astype(str), format='%Y%m%d')).dt.days

        # print(basics)
        stks_annual.append(basics)



    stks_annual = pd.concat(stks_annual)
    # aditional quality flags and uncertainty-related columns: 
    stks_annual['measurement_quality'] = 5 # 5 is for "reconstructed value (other reason)" to indicate extrapolation to fixed date
    stks_annual['measurement_type'] = 1 # 1 is for stake
    stks_annual['mb_error'] = np.nan # initialize column - this is filled in a later step in Uncertainties.py
    stks_annual['reading_error'] = np.nan # # initialize column - this is filled in a later step in Uncertainties.py
    stks_annual['density_error'] = np.nan # # initialize column - this is filled in a later step in Uncertainties.py
    stks_annual['date_quality'] = 1 # start date and end date exactly known for fixed date stakes.

    # set values for colums that always stay the same:
    stks_annual['source'] = 'AF' 

    stks_annual = stks_annual[['name', 'date0', 'date1', 'period', 'date_quality',
                                   'x_pos', 'y_pos', 'z_pos', 'position_quality', 'mb_raw', 'density',
                                   'density_quality', 'mb_we', 'measurement_quality', 'measurement_type',
                                   'mb_error', 'reading_error', 'density_error', 'source']]

    stks_annual = stks_annual.reset_index(drop=True)

    return (stks_annual)



def makeTablePits_fixed(yrs, folder_pits, gl):
    fls1 = glob.glob(folder_pits+'/Schacht*.shp')
    pits_annual = []
    dfpits = pd.DataFrame(columns=['fname', 'year'])
    dfpits['fname'] = fls1
    dfpits['year'] = dfpits['fname'].str[-8:-4].astype(int)
    dfpits.sort_values(by=['year'], inplace=True)
    print(dfpits)

    for y in dfpits['year']:
        f = dfpits.loc[dfpits['year']==y, 'fname'].values[0]
        print(f)
        temp = gpd.read_file(f)
        print(temp.crs)
        temp.to_crs(epsg=4326, inplace=True)
        temp['Jahr'] = y
        print(temp)
        # stop
        basics = pd.DataFrame(columns=['name'])
        if 'Schachtnum' in temp.columns:
            basics['name'] = temp['Schachtnum']
        else:
            basics['name'] = 'NN'
        basics['x_pos'] = temp.geometry.x
        basics['y_pos'] = temp.geometry.y
        
        if 'z' in temp.columns:
            basics['z_pos'] = temp['z'].apply(pd.to_numeric, errors='coerce')
        else:
            basics['z_pos'] = temp['RASTERVALU'].apply(pd.to_numeric, errors='coerce')
        
        basics['position_quality'] = 2 # 2 stands for measured by handheld GPS - see swiss file

        # temp['position_quality'] = np.nan
        # temp.loc[temp['Jahr'].astype(int)< 2009, 'position_quality'] = 4 # 4 stands for "estimated from previous measurements" as per the swiss file. Here it is estimated from subsequent measurements.
        # temp.loc[temp['Jahr'].astype(int)>= 2009, 'position_quality'] = 2 # 2 stands for measured by handheld GPS - see swiss file

        # basics['position_quality'] = temp['position_quality']

        basics['density'] = np.nan
        # print(basics)

        # FIXED DATE SPRING: get mb we value extrapolated to fixed date value for SPRING
        basics['density_quality'] = 3 # 3 stands for estimated from nearby measured snow density - see swiss file
        
        # fixed start and end dates:
        basics['date0'] = int(str(y-1)+'1001')
        basics['date1'] = int(str(y)+'0930')

        basics['period'] = (pd.to_datetime(basics['date1'].astype(str), format='%Y%m%d') - pd.to_datetime(basics['date0'].astype(str), format='%Y%m%d')).dt.days


        basics['date_quality'] = 1 # for start and end date exactly known (see swiss docs)
        basics['mb_raw'] = np.nan
        if 'Wasserwert' in temp.columns:
            basics['mb_we'] = temp['Wasserwert'].apply(pd.to_numeric, errors='coerce')
        else:
            basics['mb_we'] = temp['ww_mm'].apply(pd.to_numeric, errors='coerce')
        basics['mb_we'] = basics['mb_we']
        basics['measurement_quality'] = 5 # 5 is for "reconstructed value (other reason)" - using this to indicate extrapolation to fixed date.
        
        pits_annual.append(basics)
    pits_annual = pd.concat(pits_annual)

    # set values for colums that always stay the same:
    # source: who provided the data?
    pits_annual['source'] = 'AF' 

    # snow pit mass balance cannot be negative
    # pits_annual.loc[pits_annual['mb_we'] < 0, 'mb_we'] = np.nan

    pits_annual['measurement_type'] = 2 # 2 is for snow pit and probing
        
    pits_annual['mb_error'] = np.nan # not sure
    pits_annual['reading_error'] = np.nan # not sure
    pits_annual['density_error'] = np.nan # not sure

    pitdata = pits_annual[['name', 'date0', 'date1', 'period', 'date_quality', 'x_pos',
                      'y_pos', 'z_pos', 'position_quality', 'mb_raw', 'density', 'density_quality',
                      'mb_we', 'measurement_quality', 'measurement_type', 'mb_error', 'reading_error',
                      'density_error', 'source']]

    pitdata.dropna(subset=['mb_we'], inplace=True)
    pitdata = pitdata.reset_index(drop=True)
    return(pitdata)




def writetofile(dat, what, gl, forheader, y):
    if what == 'annual':
        # header1 = '# Mass Balance; '+forheader+' annual fixed date'
        fn = 'out/Vorlage_'+gl+'_MB_annual_'+y+'.csv'
        fnex = 'out/Vorlage_'+gl+'_MB_annual_'+y
    if what == 'seasonal':
        # header1 = '# Mass Balance; '+forheader+' winter fixed date'
        fn = 'out/Vorlage_'+gl+'_MB_winter_'+y+'.csv'
        fnex = 'out/Vorlage_'+gl+'_MB_winter_'+y
    if what == 'period':
        # header1 = '# Mass Balance; '+forheader+' intermediate'
        fn = 'out/Vorlage_'+gl+'_MB_intermediate_'+y+'.csv'
        fnex = 'out/Vorlage_'+gl+'_MB_intermediate_'+y

    print(dat.head())

    dat['Date/Time (begin of period)'] = pd.to_datetime(dat['date0'], format='%Y%m%d')#.astype(str)#+ ' ' +dat['time0'].astype(str)
    # dat['Date/Time (begin of period)'] = pd.to_datetime(dat['Date/Time (begin of period)'],errors='coerce')

    dat['Date/Time (begin of period)'] = dat['Date/Time (begin of period)'].dt.strftime('%Y-%m-%d')


    dat['Date/Time (end of period)'] = pd.to_datetime(dat['date1'], format='%Y%m%d')#.astype(str)#+ ' ' +dat['time1'].astype(str)
    # dat['Date/Time (end of period)'] = pd.to_datetime(dat['Date/Time (end of period)'], errors='coerce')
    # dat = dat.loc[dat['Date/Time (end of period)'].dt.year == int(y)]
    dat['Date/Time (end of period)'] = dat['Date/Time (end of period)'].dt.strftime('%Y-%m-%d')
    print(dat.tail())
    

    dat = dat.rename(columns={"name": 'Name (stake, sounding, probing)', "period": "Duration [days] (period length)", "source":"Observer"})
    dat = dat.rename(columns={"x_pos": "x [m] (x-position of stake, EPSG:4326)", "y_pos": "y [m] (y-position of stake, EPSG:4326)", "z_pos":"z [m] (elevation of stake)"})
    dat = dat.rename(columns={"date_quality": "QF date (quality identifier for date)", "position_quality": "QF pos (quality identifier for position)", "density":"Dens snow/firn/ice [kg/m**3]"})
    dat = dat.rename(columns={"density_quality": "QF rho (quality identifier for density)", "position_quality": "QF pos (quality identifier for position)", "density":"Dens snow/firn/ice [kg/m**3]"})
    dat = dat.rename(columns={"mb_we": "MB point [mm w.e./kg/m**2]", "measurement_quality": "QF measurement (quality identifier for stake ...)", "measurement_type'":"Measurement type (type of mass balance observation)"})
    dat = dat.rename(columns={"mb_error": "MB point unc [mm w.e.] (Uncertainty of point mass bal...)", "reading_error": "Reading unc [mm w.e.] (Reading uncertainty of point ...)", "density_error":"Density unc [mm w.e.] (Density uncertainty of point ...)"})
    dat = dat.rename(columns={"mb_raw": "MB raw [cm] (raw mass balance measurement)"})
    

    dat = dat.drop(['date0', 'date1'], axis=1)
    dat = dat[['Name (stake, sounding, probing)', 'Date/Time (begin of period)', 'Date/Time (end of period)',
       'Duration [days] (period length)',
       'QF date (quality identifier for date)',
       'x [m] (x-position of stake, EPSG:4326)',
       'y [m] (y-position of stake, EPSG:4326)', 'z [m] (elevation of stake)',
       'QF pos (quality identifier for position)', 
       'MB raw [cm] (raw mass balance measurement)',
       'Dens snow/firn/ice [kg/m**3]',
       'QF rho (quality identifier for density)', 'MB point [mm w.e./kg/m**2]',
       'QF measurement (quality identifier for stake ...)', 'measurement_type',
       'MB point unc [mm w.e.] (Uncertainty of point mass bal...)',
       'Reading unc [mm w.e.] (Reading uncertainty of point ...)',
       'Density unc [mm w.e.] (Density uncertainty of point ...)', 'Observer',
       ]]
    #dat.index=dat["Name (stake, sounding, probing)"]
    print(dat.head())

    dat.to_csv(fn, index=False)
    dat.to_excel(fnex+'.xlsx', index = False)



gl = 'JAM'
# read stakes excel file (annual data)
fn = '/Users/leahartl/Desktop/LTER/AGM/JAM/Pegel_Jam.xlsx'
yrs = np.arange(1989, 2025)



# pits: available for 1989-2016
yrsPITS = []

folder_pits = '/Users/leahartl/Desktop/LTER/AGM/JAM/Shapefiles Schneeschächte Jamtalferner'

# # are these fall or spring pits?? assuming fall but not sure. 
pits_fixed_annual = makeTablePits_fixed(yrs, folder_pits, gl)
print(pits_fixed_annual)


stks_annual = makeTableAnnual(yrs, fn, gl)

# concatenate annual stakes and pits:
data_annual = pd.concat([stks_annual, pits_fixed_annual])

# fixed date annual with uncertainties:
data_annual_u = unc.uncertainties(data_annual, 'annual')
print(data_annual_u)


writetofile(data_annual_u, 'annual', gl, 'Jamtalferner', '2005')



