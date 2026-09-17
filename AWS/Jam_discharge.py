import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# file path discharge
file_path_Discharge = 'klara/IGF_MA_Daten/Discharge.csv'
# Read the dataset
Discharge = pd.read_csv(file_path_Discharge, delimiter='\t')

# Combine the datetime columns into a single datetime object
# timestamp_Discharge = [pd.Timestamp(int(row['YY']), int(row['MM']), int(row['DD']), int(row['HH']), int(row['MN'])) for _, row in file_data_Discharge.iterrows()]
Discharge['datetime'] = Discharge['YY'].astype(str) + Discharge['MM'].astype(str) + Discharge['DD'].astype(str) +' '+Discharge['HH'].astype(str) +':'+ Discharge['MN'].astype(str)
Discharge.index = pd.to_datetime(Discharge['datetime'], format='%Y%m%d %H:%M')
# ensure the values are floats:
Discharge['Stat1']=Discharge['Stat1'].astype(float)
Discharge = Discharge[['Stat1']]

# resample to daily mean values
discharge_daily = Discharge.resample('d').mean()

# file path AWS data:
# load data
filename = 'dataMerged.csv'
# error value is -777.0
data = pd.read_csv(filename, index_col=0, parse_dates=True, na_values=-777.0)
# we only want precip and snow for this plot:
data = data[['Precip', 'Snowdepth']]
#resample to daily:
data_daily = data.resample('d').mean()
# overwrite precip column with daily sum:
data_daily['Precip'] = data['Precip'].resample('d').sum()

# merge the two data frames: 
merged = pd.merge(discharge_daily, data_daily, left_index=True, right_index=True, how='outer')
# cut off years without discharge data:
merged = merged.loc[(merged.index >= '2018-10-01') & (merged.index <= '2022-09-30')]

# print to check it looks ok
print(merged.head())

fig, ax = plt.subplots(4, 1, figsize=(12, 8), sharex=True, height_ratios=[2, 1, 1, 1])
ax = ax.flatten()

# ax[0].set_title('Precipitation')
ax[0].bar(merged.index, merged.Precip, width=1, color='k', label='Precipitation, daily sum')
ax[0].set_ylabel('[mm]')
merged_sum_mnth = merged['Precip'].resample('m').sum()
ax[0].legend()
# ax0 = ax[0].twinx()
ax[1].step(merged_sum_mnth.index, merged_sum_mnth.values, color='k', label='Precipitation, monthly sum')
ax[1].set_ylabel('[mm]')
ax[1].legend()
#ax[1].yaxis.label.set_color('k')

# ax[2].set_title('Snow height')
rol = merged.rolling(30, center=True).mean()
ax[2].plot(merged.index, merged.Snowdepth, label='Snow height, daily mean', color='k', linewidth=0.5)
ax[2].plot(rol.index, rol.Snowdepth, label='30 day rolling mean', color='grey')
ax[2].legend()
ax[2].set_ylabel('[cm]')

# ax[3].set_title('Discharge')
ax[3].plot(merged.index, merged.Stat1, color='k', linewidth=0.5, label='Discharge, daily mean')
ax[3].plot(rol.index, rol.Stat1, color='grey', label='30 day rolling mean')
ax[3].set_ylabel('[$m^3/s$]')
ax[3].legend()

ax[0].set_xlim(pd.to_datetime(['2018-10-01', '2022-09-30']))
for a in ax:
    a.grid('both')

fig.savefig('figs/DischargePlot.png', dpi=200, bbox_inches='tight')
plt.show()

