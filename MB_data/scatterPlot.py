
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib import cm
import scipy
from scipy.stats import norm
plt.rcParams['savefig.dpi'] = 300


#https://github.com/lilianschuster/glacier_climate_plots/blob/main/extreme_glacier_mb_distribution_plots/mass_balance_distribution_extremes.ipynb
# load the data
data = pd.read_csv('/Users/leahartl/Desktop/JAM/Jam_mb_timeseries.csv', sep= ',', na_values='****', decimal='.') 
# print(data)
# stop
yr = data['Year'].str.strip().str[-4:].astype(int).values
print(yr)
data = data[['b', 'bw', 'bs']]
data.index = yr

print(data)
data['bw_anom'] = data['bw'] - data['bw'].mean()
data['bs_anom'] = data['bs'] - data['bs'].mean()
data['b_anom'] = data['b'] - data['b'].mean()

data['bw_anom_p'] = 100*(data['bw']) / data['bw'].mean()
data['bs_anom_p'] = 100*(data['bs']) / data['bs'].mean()
data['b_anom_p'] = 100*(data['b']) / data['b'].mean()


print(data.bw_anom.min())
print(data.bw_anom.idxmin())

print(data.bw_anom.max())
print(data.bw_anom.idxmax())


# fig, ax = plt.subplots(1, 1, figsize=(8, 6))
# ax.scatter(data['bw_anom_p'], data['bs_anom_p'], c='k')
# ax.scatter(data.loc[2022, 'bw_anom_p'], data.loc[2022, 'bs_anom_p'], c='r', label='2022')
# ax.scatter(data.loc[2018, 'bw_anom_p'], data.loc[2018, 'bs_anom_p'], c='m', label='2018')
# ax.scatter(data.loc[2003, 'bw_anom_p'], data.loc[2003, 'bs_anom_p'], c='orange', label='2003')


# ax.annotate('2022', xy=(data.loc[2022, 'bw_anom_p'], data.loc[2022, 'bs_anom_p']),  xycoords='data')
# ax.annotate('2003', xy=(data.loc[2003, 'bw_anom_p'], data.loc[2003, 'bs_anom_p']),  xycoords='data')
# ax.annotate('2018', xy=(data.loc[2018, 'bw_anom_p'], data.loc[2018, 'bs_anom_p']),  xycoords='data')

# # xmin = data['bw_anom_p'].min()-5
# # xmax = (data['bw_anom_p'].min()-5)*-1
# # ymin = data['bs_anom_p'].min()-5
# # ymax = (data['bs_anom_p'].min()-5)*-1
# # # ax.vlines(0, ymin=ymin, ymax=ymax, color='k', linewidth=1)
# # # ax.hlines(0, xmin=xmin, xmax=xmax, color='k', linewidth=1)
# # ax.set_xlim([xmin, xmax])
# # ax.set_ylim([ymin, ymax])
# ax.set_xlabel('anomaly b winter (% of normal)')
# ax.set_ylabel('anomaly b summer (% of normal)')
# ax.set_title('Jamtalferner: specific mb anomalies (base: time series mean, 1989-2022)')
# ax.grid('both')

# # ax.annotate('snowy winter,\ncool summer', xy=(600, 2000),  xycoords='data', horizontalalignment='right',
# #             # xytext=(100, 2000), textcoords='data',
# #             # arrowprops=dict(facecolor='black', shrink=0.05),
# #             # horizontalalignment='left', verticalalignment='top',
# #             fontweight='bold'
# #             )
# # ax.annotate('snowy winter,\nhot summer', xy=(600, -2000),  xycoords='data', horizontalalignment='right',
# #             # xytext=(100, -2000), textcoords='data',
# #             # arrowprops=dict(facecolor='black', shrink=0.05),
# #             # horizontalalignment='left', verticalalignment='top',
# #             fontweight='bold'
# #             )
# # ax.annotate('dry winter,\nhot summer', xy=(-600, -2000),  xycoords='data', horizontalalignment='left',
# #             fontweight='bold'
# #             # xytext=(-100, -2000), textcoords='data',horizontalalignment='left'
# #             # arrowprops=dict(facecolor='black', shrink=0.05),
# #             # horizontalalignment='left', verticalalignment='top',
# #             )
# # ax.annotate('dry winter,\ncool summer', xy=(-600, 2000),  xycoords='data', horizontalalignment='left',
# #             # xytext=(-100, -2000), textcoords='data',horizontalalignment='left'
# #             # arrowprops=dict(facecolor='black', shrink=0.05),
# #             # horizontalalignment='left', verticalalignment='top',
# #             fontweight='bold'
# #             )


# # ax.legend()
# plt.show()
# fig.savefig('scatter_Anomalies_percentage.png')

# stop

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
ax.scatter(data['bw_anom'], data['bs_anom'], c='k')
ax.scatter(data.loc[2024, 'bw_anom'], data.loc[2024, 'bs_anom'], c='lime', label='2024')
print(data.loc[2024, 'bw_anom'], data.loc[2024, 'bs_anom'])
ax.scatter(data.loc[2023, 'bw_anom'], data.loc[2023, 'bs_anom'], c='b', label='2023')
ax.scatter(data.loc[2022, 'bw_anom'], data.loc[2022, 'bs_anom'], c='r', label='2022')
ax.scatter(data.loc[2018, 'bw_anom'], data.loc[2018, 'bs_anom'], c='m', label='2018')
ax.scatter(data.loc[2003, 'bw_anom'], data.loc[2003, 'bs_anom'], c='orange', label='2003')

ax.annotate('2024', xy=(data.loc[2024, 'bw_anom'], data.loc[2024, 'bs_anom']),  xycoords='data')
ax.annotate('2023', xy=(data.loc[2023, 'bw_anom'], data.loc[2023, 'bs_anom']),  xycoords='data')
ax.annotate('2022', xy=(data.loc[2022, 'bw_anom'], data.loc[2022, 'bs_anom']),  xycoords='data')
ax.annotate('2003', xy=(data.loc[2003, 'bw_anom'], data.loc[2003, 'bs_anom']),  xycoords='data')
ax.annotate('2018', xy=(data.loc[2018, 'bw_anom'], data.loc[2018, 'bs_anom']),  xycoords='data')

xmin = data['bw_anom'].min()-50
xmax = (data['bw_anom'].max()+50)
ymin = data['bs_anom'].min()-100
ymax = (data['bs_anom'].min()-100)*-1
ax.vlines(0, ymin=ymin, ymax=ymax, color='k', linewidth=1)
ax.hlines(0, xmin=xmin, xmax=xmax, color='k', linewidth=1)
ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
ax.set_xlabel('anomaly b winter (mm w.e.)')
ax.set_ylabel('anomaly b summer (mm w.e.)')
ax.set_title('Jamtalferner: specific mb anomalies (base: time series mean, 1989-2024)')
ax.grid('both')

ax.annotate('snowy winter,\ncool summer', xy=(600, 2000),  xycoords='data', horizontalalignment='right',
            # xytext=(100, 2000), textcoords='data',
            # arrowprops=dict(facecolor='black', shrink=0.05),
            # horizontalalignment='left', verticalalignment='top',
            fontweight='bold'
            )
ax.annotate('snowy winter,\nhot summer', xy=(600, -2000),  xycoords='data', horizontalalignment='right',
            # xytext=(100, -2000), textcoords='data',
            # arrowprops=dict(facecolor='black', shrink=0.05),
            # horizontalalignment='left', verticalalignment='top',
            fontweight='bold'
            )
ax.annotate('dry winter,\nhot summer', xy=(-600, -2000),  xycoords='data', horizontalalignment='left',
            fontweight='bold'
            # xytext=(-100, -2000), textcoords='data',horizontalalignment='left'
            # arrowprops=dict(facecolor='black', shrink=0.05),
            # horizontalalignment='left', verticalalignment='top',
            )
ax.annotate('dry winter,\ncool summer', xy=(-600, 2000),  xycoords='data', horizontalalignment='left',
            # xytext=(-100, -2000), textcoords='data',horizontalalignment='left'
            # arrowprops=dict(facecolor='black', shrink=0.05),
            # horizontalalignment='left', verticalalignment='top',
            fontweight='bold'
            )


# ax.legend()
plt.show()
fig.savefig('scatter_Anomalies.png')


