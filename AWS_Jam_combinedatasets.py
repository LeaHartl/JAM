import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import glob

# script to merge the data provided by M Neuner. There are two csv files (one in each data_dir).
data_dir1 = 'ASCII_NLV_jam/'
data_dir2 = 'jamtal/'

fname1 = data_dir1+'All_Data.csv'
fname2 = data_dir2+'All_Data.csv'

# load data
filename = 'All_Data.csv'

data1 = pd.read_csv(fname1, index_col=0, parse_dates=True)
data2 = pd.read_csv(fname2, index_col=0, parse_dates=True)

# print some stuff to check it looks ok
print(data1.head())
print(data2.head())
print(data2.columns)

# merge the data on index with an "outer merge". This means the timestamp index must match
# and missing timestamps will be filled with nan values.
merged = pd.merge(data1, data2, left_index=True, right_index=True, how='outer')

# dictionary of parameter names - rename to more intuitive values.
cols = {"HS-60m": "Snowdepth",
        "LT-60m": "AirTemp",
        "LF-60m": "RelHum",
        "WG.Boe-h": "WindSpeedGust",
        "WG-h": "WindSpeed",
        "WR-60m": "WindDir",
        "N-60m": "Precip",
        "GS": "GlobalRadiation",
        "TS.000-60m": "TS_0",
        "TS.025-60m": "TS_025",
        "TS.050-60m": "TS_050",
        "TS.075-60m": "TS_075",

        "PYRANOMETER.UNTEN-60m": "SWout",
        "LS.unten-60m": "LWout",
        "PYRANOMETER.OBEN-60m": "SWin",
        "GERAETETEMPERATUR-h": "SensorTemp",
        "LS.oben-60m": "LWin"

        }

dataAll = merged.rename(columns=cols)



dataAll.to_csv('dataMerged.csv')

