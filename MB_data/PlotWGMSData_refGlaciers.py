
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
wgms_mb = '/Users/leahartl/Desktop/WGMS/DOI-WGMS-FoG-2025-02/data/mass_balance.csv'
# band data:
wgms_bands = '/Users/leahartl/Desktop/WGMS/DOI-WGMS-FoG-2025-02/data/mass_balance_band.csv'

# Load data 
wgms_df = pd.read_csv(wgms_mb, encoding='unicode_escape')



# extract subset
AT = wgms_df[wgms_df['country']=='AT']
AT = AT[['glacier_name', 'year', 'annual_balance']]
print(AT)
print(AT.glacier_name.unique())
todrop = ['FILLECK K.', 'HOCHKOENIG', 'KLOSTERTALER N', 'LANGTALER F.', 'OCHSENTALER G.',
          'STUBACHER WEISSSEE K.', 'VERMUNT G.', 'HOCHJOCH F.', 'STUBACHER SONNBLICK K.']
AT = AT[~AT['glacier_name'].isin(todrop)]
print(AT.glacier_name.unique())

# df = df.drop(df[df.score < 50].index)
#Collect data and put into dataframe
MB_df = pd.DataFrame(columns=AT.glacier_name.unique(), index=range(1945, 2025))
glaciers = []
for gl in AT.glacier_name.unique():
    data = AT.loc[AT.glacier_name == gl]
    yr = data["year"].values
    mb = data["annual_balance"].values

    # this does not work when csv files have missing years.
    # MB_df.loc[yr[0]:yr[-1], wgmsid] = mb

    # need loop because some have missing years.
    for i, yy in enumerate(yr):
        MB_df.loc[yy, gl] = mb[i]

    # get glacier names and add to list
    glaciers.append(gl)
    print('collected ', gl)

print(MB_df)
# get mb range of all ref. glaciers
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
    dat = pd.to_numeric(MB_df[col].dropna())
    col = PatchCollection([
        Rectangle((y+0.5, 0), 1, 1,)
        for y in range(dat.index.values[0], dat.index.values[-1] + 1)
    ])
    col.set_array(dat.values)
    col.set_cmap(cmap)
    col.set_norm(divnorm)
    col.set_clim(lim_neg, lim_pos)
    cb= ax[i].add_collection(col)
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

