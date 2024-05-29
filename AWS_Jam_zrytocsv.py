import pandas as pd
import numpy as np
import glob


# function to load the .zrx files provided by M. Neuner. 
def readfile(f):

    ds = pd.read_csv(f, skiprows=[0,1,2,3], encoding='unicode_escape', sep = ' ')#skiprows=[0,2,3], 
    # get parameter name 
    par = f[21:-10]
    print(par)

    ds.columns=['TIMESTAMP', par]
    # set date as index and fix the format. Time is in UTC (checked)
    ds.set_index('TIMESTAMP', inplace=True)
    ds.index = pd.to_datetime(ds.index, format='%Y%m%d%H%M%S', errors='coerce')

    # convert accidental strings in numeric values
    ds = ds.astype(float)

    return(ds)


# function to load the SECOND SET OF .zrx files provided by M. Neuner. Note that these have
# an additional header line compared to the first set.
def readfile2(f):

    ds = pd.read_csv(f, skiprows=[0,1,2,3,4], encoding='unicode_escape', sep = ' ')#skiprows=[0,2,3], 
    # get parameter name 
    par = f[14:-10]
    # print(par)
    ds.columns=['TIMESTAMP', par]
    # set date as index and fix the format. Time is in UTC (checked)
    ds.set_index('TIMESTAMP', inplace=True)
    ds.index = pd.to_datetime(ds.index, format='%Y%m%d%H%M%S', errors='coerce')

    # convert accidental strings in numeric values
    ds = ds.astype(float)

    return(ds)


# make list of all .zrx files in the data directory
# set name of directory with the zrx files to be combined (uncomment as needed or adjust)
#data_dir = 'ASCII_NLV_jam/'
data_dir = 'jamtal/'
fls = glob.glob(data_dir+'*.zrx')

srs = []

# call "read file" function, load all zrx files and append to list of series
# the header format is not consistent between the files!
for f in fls:
    if data_dir =='jamtal/':
        dat = readfile2(f)
    if data_dir =='ASCII_NLV_jam/':
        dat = readfile(f)
    srs.append(dat)

# turn list into dataframe and export to csv
df = pd.concat(srs, axis=1)
df.to_csv(data_dir+'All_Data.csv')

