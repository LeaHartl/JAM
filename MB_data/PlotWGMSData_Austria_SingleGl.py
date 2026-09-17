
#! /usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
from matplotlib.colors import TwoSlopeNorm

# plt.style.use('seaborn') 
# plot strips for all austrian MB glaciers
 
# get the data:
# file with yearly mb data:
wgms_mb = '/Users/leahartl/Desktop/WGMS/DOI-WGMS-FoG-2026-02-10/data/mass_balance.csv'
# band data:
wgms_bands = '/Users/leahartl/Desktop/WGMS/DOI-WGMS-FoG-2026-02-10/data/mass_balance_band.csv'

# Load data 
wgms_df = pd.read_csv(wgms_mb, encoding='unicode_escape')
wgms_bands = pd.read_csv(wgms_bands, encoding='unicode_escape')



# extract subset
HSG = wgms_df.loc[wgms_df['glacier_name']=='HALLSTAETTER G.']
HSG_bands = wgms_bands.loc[wgms_bands['glacier_name']=='HALLSTAETTER G.']

HSG = HSG[['year', 'annual_balance', 'winter_balance', 'summer_balance']]
HSG_bands = HSG_bands[['year', 'annual_balance', 'winter_balance', 'lower_elevation', 'upper_elevation']]
HSG_bands['elev'] = (HSG_bands['lower_elevation']+HSG_bands['upper_elevation'])/2
print(HSG)
print(HSG_bands)



fig1, ax1= plt.subplots(1, 1, figsize=(8, 6), sharex=True)
# ax1 = ax1.flatten()
colors = plt.cm.viridis(np.linspace(0, 1, len(HSG_bands.year.unique())))
# cmap = ListedColormap(colors)

for i, y in enumerate(HSG.year.unique()):
    sub1= HSG.loc[HSG.year == y]
    ax1.scatter(sub1.annual_balance, sub1.winter_balance, color=colors[i], label=y)

ax1.legend(loc='lower right', bbox_to_anchor=(1.12, 0.1))
ax1.set_ylabel('Specific winter mass balance (m w.e.)')
ax1.set_xlabel('Specific annual mass balance (m w.e.)')
ax1.set_title('Winter vs annual mass balance, Hallstätter Gletscher')
# ax1.vlines(0, 2100, 2950, color='k', linestyle='-')
ax1.grid('both')
fig1.savefig('HSG_scatter.png', dpi=200)
# ax1.set_ylim(2150, 2900)

fig, ax = plt.subplots(1, 1, figsize=(8, 6), sharex=True)
# ax = axs.flatten()
colors = plt.cm.viridis(np.linspace(0, 1, len(HSG_bands.year.unique())))
# cmap = ListedColormap(colors)
for i, y in enumerate(HSG_bands.year.unique()):
    sub = HSG_bands.loc[HSG_bands.year == y]

    ax.plot(sub.annual_balance, sub.elev, color=colors[i], label=y)

ax.legend(loc='lower right', bbox_to_anchor=(1.01, 0.1))
ax.set_xlabel('Specific mass balance (m w.e.)')
ax.set_ylabel('Elevation (m a.s.l.)')
ax.set_title('mass balance (elevation zones) Hallstätter Gletscher')
ax.vlines(0, 2100, 2950, color='k', linestyle='-')
ax.grid('both')
ax.set_ylim(2150, 2900)
fig.savefig('HSG_elevation.png', dpi=200)
plt.show()





stop


# stop# get mb range of all ref. glaciers
# lim_pos= MB_df.max().max()
# lim_neg= MB_df.min().min()
lim_pos= 2.000
lim_neg= -3.000

#set diverging color map and make norm so it is centered at zero.
cmap='RdBu'
divnorm = TwoSlopeNorm(vmin=lim_neg, vcenter=0, vmax=lim_pos)

# make figure/ subplots
fig, axs = plt.subplots(len(MB_df.columns), 1, figsize=(12, 6), sharex=True)
ax = axs.flatten()

for i, col in enumerate(MB_df.columns):
    ax[i].set_yticks([])
    dat = pd.to_numeric(MB_df[col])#.dropna())
    col = PatchCollection([
        Rectangle((y+0.5, 0), 1, 1,)
        for y in range(dat.index.values[0], dat.index.values[-1] + 1)
    ])
    col.set_array(dat.values)
    col.set_cmap(cmap)
    col.set_norm(divnorm)
    col.set_clim(lim_neg, lim_pos)
    cb = ax[i].add_collection(col)
    ax[i].set_ylim(0, 1)
    ax[i].set_xlim(1927,  2026)
    ax[i].annotate(glaciers[i],xy=(1930 ,0.2),xycoords='data')
    ax[i].set_facecolor('grey')

ax[-1].set_xlabel('Year')
# add colorbar
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
cbar = fig.colorbar(cb, cax=cbar_ax)
# add title
ax[0].set_title('Austrian mass balance glaciers, annual mass balance (m w.e.)')

plt.show()
fig.savefig('stripes_ATglaciers2024.png', bbox_inches='tight', dpi=200)





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

