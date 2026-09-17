import numpy as np
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt
from matplotlib import cm
#import seaborn


gl = 'JAM'
# read stakes excel file (annual data)
fn = '/Users/leahartl/Desktop/JAM/Pegel_Jam.xlsx'
fnPts_Spring = '/Users/leahartl/Desktop/Jam2025/winter/sondierungen_20250426.shp'
pitname = 's01 18'
pitdensity = 369 #kg/m3

fnBands = '/Users/leahartl/Desktop/Jam2025/Bericht/table_MB.csv'
yr = 2025

def PointsAnnualWGMS(yr, fname, fpts, pitname, pitdensity):
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
    # balance in m w.e.!
    WGMS['balance'] = temp['mm_we_withsnowcorr_300kgm_3_fixed']/1000
    WGMS['±mwe'] = np.nan
    WGMS['density'] = np.nan
    WGMS['±density'] = np.nan
    WGMS['method'] = 'stake'
    WGMS['balance_code'] = 'annual'
    WGMS['remarks'] = 'assumed density of ice: 900kg/m3; assumed density of snow at stake positions during final measurements: 300 kg/m3'
    # print(WGMS)

    # pits: 
    pts = pd.DataFrame(columns=WGMS.columns)
    pt = gpd.read_file(fpts)
    # print(pt)
    pts['original_id'] = pt['name']
    pts['time_system'] = 'measured'
    pts['begin_date'] = str(yr-1)+'-10-01'
    pts['±days_begin'] = np.nan
    pts['end_date'] = str(yr)+'-04-26'
    pts['±days_end'] = 0
    pts['latitude'] = pt['lat']
    pts['longitude'] = pt['lon']
    pts['elevation'] = pt['Z_value']

    pts['balance'] = (pt['WW']/1000).round(decimals=3)
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

    WGMS.to_csv('/Users/leahartl/Desktop/Jam2025/Tabellen/mass_balance_point_'+str(yr)+'_JAM.csv', index=False)
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
    WGMS['area m2'] = temp['Fläche']*1e6
    WGMS['winter_balance'] = temp['b_wi']*1e-3
    WGMS['±mwe_wb'] = np.nan
    WGMS['summer_balance'] = temp['b_so']*1e-3
    WGMS['±mwe_sb'] = np.nan
    WGMS['annual_balance'] = temp['b']*1e-3
    WGMS['±mwe'] = np.nan
    WGMS['remarks'] = ''

    WGMS[['winter_balance', 'summer_balance', 'annual_balance']] = WGMS[['winter_balance', 'summer_balance', 'annual_balance']].astype(float).round(decimals=3)

    WGMS['glacier_name'] = 'JAMTAL F.'
    WGMS['glacier_id'] = 480
    WGMS['year'] = yr

    WGMS.to_csv('/Users/leahartl/Desktop/Jam2025/Tabellen/mass_balance_band_'+str(yr)+'_JAM.csv', index=False)
    


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

    WGMS['aar'] = 0/temp['Fläche'].values[0]*1e6

    WGMS['area m2'] = temp['Fläche'].values[0]*1e6
    WGMS['winter_balance'] = temp['b_wi'].values[0]*1e-3
    WGMS['±mwe_wb'] = np.nan
    WGMS['summer_balance'] = temp['b_so'].values[0]*1e-3
    WGMS['±mwe_sb'] = np.nan
    WGMS['annual_balance'] = temp['b'].values[0]*1e-3
    WGMS['±mwe'] = np.nan

    WGMS['investigators'] = 'Andrea Fischer (1, 2) | Lea Hartl (1) | Marcela V. Lauria (1)'
    WGMS['agencies'] = '1. Österreichische Akademie der Wissenschaften | 2. Verein Gletscher und Klima | 3. Hydrographischer Dienst der Abteilung Wasserwirtschaft des Amtes der Tiroler Landesregierung'
    WGMS['references'] = 'Fischer et al. (https://doi.org/10.1594/PANGAEA.818772)'
    WGMS['remarks'] = 'Funding provided by Hydrographischer Dienst der Abteilung Wasserwirtschaft des Amtes der Tiroler Landesregierung'

    WGMS[['winter_balance', 'summer_balance', 'annual_balance']] = WGMS[['winter_balance', 'summer_balance', 'annual_balance']].astype(float).round(decimals=3)

    WGMS['glacier_name'] = 'JAMTAL F.'
    WGMS['glacier_id'] = 480
    WGMS['year'] = yr
    WGMS['outline_id'] = np.nan
    print(WGMS)
    WGMS.to_csv('/Users/leahartl/Desktop/Jam2025/Tabellen/mass_balance_'+str(yr)+'_JAM.csv', index=False)
    


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
    pan['Saz'] = temp.Fläche.values
    pan['Baz'] = temp.balance.values
    pan['baz'] = temp.b.values
    pan['bsaz'] = temp.b_so.values
    pan['bwaz'] = temp.b_wi.values

    print(pan)

    pan.to_csv('/Users/leahartl/Desktop/Jam2025/Tabellen/pangaea_'+str(yr)+'_JAM.csv', index=False)
    

# BandsAnnualPangaea(yr, fnBands)

GlacierwideAnnualWGMS(yr, fnBands)

PointsAnnualWGMS(yr, fn, fnPts_Spring, pitname, pitdensity)

BandsAnnualWGMS(yr, fnBands)





######Older versions ########

# ## import .txt files JAM, reformat
# def readMBtxtJAM(fname, gl, nr, yr, fname_wi, sheet):
#     df = pd.read_csv(fname, delim_whitespace=True, skiprows=0, names=['Zone', 'Flaeche[km^2]', 'B[10^3m^3]', 'b[mm]'])
#     # pick out only the rows where "zone" column contains numeric values.
#     elev = df.loc[df.Zone.str.isnumeric()]
#     elev.sort_values(by=['Zone'], ascending=False,  inplace=True)
#     elev.Zone = elev.Zone.astype(int)
#     elev['b[mm]'] = elev['b[mm]'].astype(int)
#     elev['Flaeche[km^2]'] = elev['Flaeche[km^2]'].astype(float)
#     elev['altitude zone'] = [str(z-25)+'-'+str(z+25) for z in elev['Zone'].values]
#     elev['LOWER_BOUNDARY_OF_ALTITUDE_INTERVAL'] = elev['Zone']-25
#     elev['UPPER_BOUNDARY_OF_ALTITUDE_INTERVAL'] = elev['Zone']+25
#     elev['POLITICAL_UNIT'] = 'AT'
#     elev['GLACIER_NAME'] = gl
#     elev['WGMS_ID'] = str(nr)
#     elev['YEAR'] = yr
#     elev['SPECIFIC_WINTER_BALANCE_UNCERTAINTY'] = np.nan
#     elev['SPECIFIC_SUMMER_BALANCE_UNCERTAINTY'] = np.nan
#     elev['SPECIFIC_ANNUAL_BALANCE_UNCERTAINTY'] = np.nan
#     elev['REMARKS'] = np.nan

#     # get winter balance from file
#     b_wi = readWBxlsJam(fname_wi, sheet)
#     #print(b_wi)

#     # merge winter balance column with main dataframe
#     elev = elev.merge(b_wi, on='Zone')
#     elev = elev.rename(columns={'Flaeche[km^2]': 'ALTITUDE_INTERVAL_AREA', 'b[mm]': 'SPECIFIC_ANNUAL_BALANCE', 'b_wi': 'SPECIFIC_WINTER_BALANCE'})
#     elev['SPECIFIC_SUMMER_BALANCE'] =  elev['SPECIFIC_ANNUAL_BALANCE'].astype(int) - elev['SPECIFIC_WINTER_BALANCE'].astype(int)

#     elev2 = elev[['POLITICAL_UNIT', 'GLACIER_NAME', 'WGMS_ID', 'YEAR', 'LOWER_BOUNDARY_OF_ALTITUDE_INTERVAL',
#                   'UPPER_BOUNDARY_OF_ALTITUDE_INTERVAL', 'ALTITUDE_INTERVAL_AREA', 'SPECIFIC_WINTER_BALANCE',
#                   'SPECIFIC_WINTER_BALANCE_UNCERTAINTY', 'SPECIFIC_SUMMER_BALANCE', 'SPECIFIC_SUMMER_BALANCE_UNCERTAINTY',
#                   'SPECIFIC_ANNUAL_BALANCE', 'SPECIFIC_ANNUAL_BALANCE_UNCERTAINTY', 'REMARKS']]

#     df2 = df.loc[~df.Zone.str.isnumeric()]
#     #print(df2)
#     summary = pd.DataFrame(columns=df2.Zone, index=['value'])
#     #summary.loc['unit', :] = df2['B[10^3m^3]'].values
#     summary.loc['value', :] = df2['Flaeche[km^2]'].values
#     summary.drop(columns=['Zone'], inplace=True)
#     #print(summary)
#     return(elev2, summary)

# def makeSummaries(summary, gl, nr, yr, inv, agency):
#     # print(summary)
#     summary2 = pd.DataFrame(index = summary.index, columns=['POLITICAL_UNIT', 'GLACIER_NAME', 'WGMS_ID', 'YEAR', 'TIME_MEASUREMENT_SYSTEM',
#                                      'BEGINNING_OF_SURVEY_PERIOD', 'END_OF_WINTER_SEASON', 'END_OF_SURVEY_PERIOD',   
#                                      'ELA_PREFIX', 'EQUILIBRIUM_LINE_ALTITUDE', 'ELA_UNCERTAINTY', 'MIN_NUMBER_OF_MEASUREMENT_SITES_IN_ACCUMULATION_AREA',
#                                      'MAX_NUMBER_OF_MEASUREMENT_SITES_IN_ACCUMULATION_AREA', 'MIN_NUMBER_OF_MEASUREMENT_SITES_IN_ABLATION_AREA',
#                                      'MAX_NUMBER_OF_MEASUREMENT_SITES_IN_ABLATION_AREA', 'ACCUMULATION_AREA', 'ACCUMULATION_AREA_UNCERTAINTY', 'ABLATION_AREA',
#                                      'ABLATION_AREA_UNCERTAINTY', 'ACCUMULATION_AREA_RATIO', 'INVESTIGATOR', 'SPONSORING_AGENCY',
#                                      'REFERENCE', 'REMARKS'])
#     summary2['POLITICAL_UNIT'] = str('AT')
#     summary2['GLACIER_NAME'] = gl
#     summary2['WGMS_ID'] = str(nr)
#     summary2['YEAR'] = yr
#     summary2['BEGINNING_OF_SURVEY_PERIOD'] = str(yr-1)+'1001'
#     summary2['END_OF_WINTER_SEASON'] = str(yr)+'0430'
#     summary2['END_OF_SURVEY_PERIOD'] = str(yr)+'0930'
#     summary2['ACCUMULATION_AREA'] = summary['Sc='].astype(float).values
#     summary2['ABLATION_AREA'] = summary['Sa='].astype(float).values
#     summary2['ACCUMULATION_AREA_RATIO'] = summary['Sc/S='].astype(float).values

#     summary2 = summary2[['POLITICAL_UNIT', 'GLACIER_NAME', 'WGMS_ID', 'YEAR', 'TIME_MEASUREMENT_SYSTEM',
#                          'BEGINNING_OF_SURVEY_PERIOD', 'END_OF_WINTER_SEASON', 'END_OF_SURVEY_PERIOD', 
#                          'ELA_PREFIX', 'EQUILIBRIUM_LINE_ALTITUDE', 'ELA_UNCERTAINTY', 'MIN_NUMBER_OF_MEASUREMENT_SITES_IN_ACCUMULATION_AREA',
#                          'MAX_NUMBER_OF_MEASUREMENT_SITES_IN_ACCUMULATION_AREA', 'MIN_NUMBER_OF_MEASUREMENT_SITES_IN_ABLATION_AREA',
#                          'MAX_NUMBER_OF_MEASUREMENT_SITES_IN_ABLATION_AREA', 'ACCUMULATION_AREA', 'ACCUMULATION_AREA_UNCERTAINTY', 'ABLATION_AREA',
#                          'ABLATION_AREA_UNCERTAINTY', 'ACCUMULATION_AREA_RATIO', 'INVESTIGATOR', 'SPONSORING_AGENCY',
#                          'REFERENCE', 'REMARKS']]
#     summary2['INVESTIGATOR'] = inv
#     summary2['SPONSORING_AGENCY'] = agency
#     # summary2['EQUILIBRIUM_LINE_ALTITUDE'] = 

#     # print(summary2)
#     return(summary2)


# def readWBxlsJam(fname, sheet):
#     df = pd.read_excel(fname, sheet, header=None)#, names=['zone', 'Saz', 'BaZ', 'baZ', 'bwaZ', 'bsaZ'])
#     df2 = df.iloc[5:, :]
#     df2.rename(columns=df2.iloc[0], inplace=True)
#     df2 = df2.iloc[2:, :]
#     df2 = df2.rename(columns={'Höhenstufe': 'Zone'})
#     df2.dropna(subset=['Zone'], inplace=True)
#     df2.Zone = df2.Zone.astype(int)
#     df2.b_wi = df2.b_wi.astype(float).round(decimals=0).astype(int)
#     # print(df2)
#     # stop

#     return(df2[['Zone', 'b_wi']])


# ## import .txt files HSG, reformat
# def readMBtxtHSG(fname, fname2, gl, nr, yr):
#     df = pd.read_csv(fname, delim_whitespace=True, encoding='latin-1', skiprows=25,
#                     names=['Zone', 'Flaeche[km^2]', 'B[10^3m^3]', 'b[mm]'], skipfooter=15)
#     # sort descending
#     elev = df.copy()
#     elev.Zone = elev.Zone.astype(int)
#     elev.sort_values(by=['Zone'], ascending=False,  inplace=True)

#     elev['altitude zone'] = [str(z-25)+'-'+str(z+25) for z in elev['Zone'].values]
#     elev['LOWER_BOUNDARY_OF_ALTITUDE_INTERVAL'] = elev['Zone']-25
#     elev['UPPER_BOUNDARY_OF_ALTITUDE_INTERVAL'] = elev['Zone']+25
#     elev['POLITICAL_UNIT'] = 'AT'
#     elev['GLACIER_NAME'] = gl
#     elev['WGMS_ID'] = nr
#     elev['YEAR'] = int(yr)
#     elev['SPECIFIC_WINTER_BALANCE_UNCERTAINTY'] = np.nan
#     elev['SPECIFIC_SUMMER_BALANCE_UNCERTAINTY'] = np.nan
#     elev['SPECIFIC_ANNUAL_BALANCE_UNCERTAINTY'] = np.nan
#     elev['REMARKS'] = np.nan

#     # # get winter balance from file
#     b_wi = readWBtxtHSG(fname2)
#     # # merge winter balance column with main dataframe
#     elev = elev.merge(b_wi, on='Zone')
#     # # rename columns to match WGMS table 
#     elev = elev.rename(columns={'Flaeche[km^2]': 'ALTITUDE_INTERVAL_AREA', 'b[mm]': 'SPECIFIC_ANNUAL_BALANCE', 'b_wi': 'SPECIFIC_WINTER_BALANCE'})
#     # compute summer balance
#     elev['SPECIFIC_SUMMER_BALANCE'] = elev['SPECIFIC_ANNUAL_BALANCE'] - elev['SPECIFIC_WINTER_BALANCE']
#     # make new DF with column order to match wgms table
#     elev2 = elev[['POLITICAL_UNIT', 'GLACIER_NAME', 'WGMS_ID', 'YEAR', 'LOWER_BOUNDARY_OF_ALTITUDE_INTERVAL',
#                   'UPPER_BOUNDARY_OF_ALTITUDE_INTERVAL', 'ALTITUDE_INTERVAL_AREA', 'SPECIFIC_WINTER_BALANCE',
#                   'SPECIFIC_WINTER_BALANCE_UNCERTAINTY', 'SPECIFIC_SUMMER_BALANCE', 'SPECIFIC_SUMMER_BALANCE_UNCERTAINTY',
#                   'SPECIFIC_ANNUAL_BALANCE', 'SPECIFIC_ANNUAL_BALANCE_UNCERTAINTY', 'REMARKS']]

#     # load file again to extract summary info
#     df2 = pd.read_csv(fname, delim_whitespace=True, encoding='latin-1', skiprows=1, skipfooter=30)
#     df2.columns = ['val', 'unit']
#     #print(df2)
#     summary = pd.DataFrame(columns=[df2.index], index=['val'])
#     summary.iloc[0, :] = df2['val'].values
#     #print(summary)
#     return(elev2, summary)


# ## import .txt files HSG, reformat
# def readWBtxtHSG(fname):
#     df = pd.read_csv(fname, delim_whitespace=True, encoding='latin-1', skiprows=23,
#                     names=['Zone', 'Flaeche[km^2]', 'B[10^3m^3]', 'b_wi'], skipfooter=15)
#     elev = df.copy()
#     elev.Zone = elev.Zone.astype(int)
#     elev.sort_values(by=['Zone'], ascending=False,  inplace=True)
#     return(elev[['Zone', 'b_wi']])




# HSG = {'glacier': 'HALLSTÄTTER GLETSCHER',
#        'INVESTIGATOR': 'Kay Helfricht, Klaus Reingruber',
#        'SPONSORING_AGENCY': 'Land Oberösterreich, Energie AG'}
# JAM = {'glacier': 'JAMTAL F.',
#        'INVESTIGATOR': 'Andrea Fischer',
#        'SPONSORING_AGENCY': 'Hydrographischer Dienst der Abteilung Wasserwirtschaft des Amtes der Tiroler Landesregierung'}




# jamdata, jamsummary = readMBtxtJAM('jam_mb2022_final.txt', 'JAMTAL F.', 480, 2022, 'winterbilanz_jam.xls', '2021_22')
# jamOverview = makeSummaries(jamsummary, 'JAMTAL F.', 480, 2022, JAM['INVESTIGATOR'], JAM['SPONSORING_AGENCY'])

# jamdata21, jamsummary21 = readMBtxtJAM('jam_mb2021m2425_2.txt', 'JAMTAL F.', 480, 2021, 'winterbilanz_jam2021.xls', '2020_21')
# jamOverview21 = makeSummaries(jamsummary21, 'JAMTAL F.', 480, 2021, JAM['INVESTIGATOR'], JAM['SPONSORING_AGENCY'])
# print(jamOverview21)
# print(jamdata21)


# hsgdata, hsgsummary = readMBtxtHSG('hg_mb_HGMB22_auswertung.txt', 'hg_wb_HGWB22_FJ_auswertung.txt', 'HALLSTÄTTER GLETSCHER', np.nan, 2022)
# hsgOverview = makeSummaries(hsgsummary, 'HALLSTÄTTER GLETSCHER', np.nan, 2022, HSG['INVESTIGATOR'], HSG['SPONSORING_AGENCY'])

# both = pd.concat([jamdata, hsgdata])
# overviewBoth = pd.concat([jamOverview, hsgOverview])
# print(overviewBoth)

# both.to_csv('output_wgms_MB.csv', index=False)
# overviewBoth.to_csv('output_wgms_Overview.csv', index=False)
# with pd.ExcelWriter('output.xlsx') as writer:  
#     overviewBoth.to_excel(writer, sheet_name='E - MASS BALANCE OVERVIEW', index=False)
#     both.to_excel(writer, sheet_name='EE - MASS BALANCE', index=False)
    



# stop 
# # optional:
# # combine with WGMS

# wgms_ov = '/Users/leahartl/Desktop/DOI-WGMS-FoG-2021-05/WGMS-FoG-2021-05-E-MASS-BALANCE-OVERVIEW.csv'
# wgms_mb = '/Users/leahartl/Desktop/DOI-WGMS-FoG-2021-05/WGMS-FoG-2021-05-EE-MASS-BALANCE.csv'

# wgms_df = pd.read_csv(wgms_mb, encoding='unicode_escape')
# wgms_ov = pd.read_csv(wgms_ov, encoding='unicode_escape')

# JAM = wgms_df[wgms_df['NAME'] == 'JAMTAL F.']
# JAM_ov = wgms_ov[wgms_ov['NAME'] == 'JAMTAL F.']
# JAM_ov.to_csv('JAM_WGMS_overview_1989_2020.csv', index=False)
# JAM_ov.drop(columns=['PUB_IN_MBB', 'PUB_IN_FOG'], inplace=True)
# # print(JAM_ov.columns)
# # print(jamOverview21.columns)

# jamdata.columns = JAM.columns
# jamdata21.columns = JAM.columns
# JAM_update = pd.concat([jamdata21, jamdata])

# jamOverview.columns = JAM_ov.columns
# jamOverview21.columns = JAM_ov.columns
# jamOverview21['ELA'] = 3097
# jamOverview['ELA'] = np.nan
# JAM_overview_update = pd.concat([jamOverview21, jamOverview])


# print(JAM_update)
# print(JAM_overview_update)

# JAM_update.to_csv('JAM_Hoehenstufen_WGMSformat_2122.csv', index=False)
# JAM_overview_update.to_csv('JAM_Overview_WGMSformat_2122.csv', index=False)

# JAM.to_csv('JAM_Hoehenstufen_WGMS_1989_2020.csv', index=False)



