#! /usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
from matplotlib.colors import TwoSlopeNorm

## adapted from: https://matplotlib.org/matplotblog/posts/warming-stripes/

# get data
data = pd.read_csv('/Users/leahartl/Desktop/JAM/Jam_mb_timeseries_2025.csv', sep= ',', na_values='****', decimal='.') 
print(data)
print(data[['S', 'B', 'b', 'bs', 'bw', 'ELA', 'Sc/S']].mean())


yr = data['Year'].str.strip().str[-4:].astype(int).values
print(yr)
print(data[['S','B','b','bs','bw','ELA']].mean())
mb = data.b
mb_w = data[['Year2', 'bw']]
mb_s = data[['Year2', 'bs']]

# clim = mb_w['bw'].mean()

# print(clim)
# mb_w['anom'] = mb_w['bw']-clim
# mb_w['anom_p'] = 100*mb_w['anom']/clim 

print(mb_w)

# print(data['bw']/data['bs'])

# get mb range
lim_pos= mb.max()
lim_neg= mb.min()

#set diverging color map and make norm so it is centered at zero.
# cmap='Reds_r'
cmap = plt.get_cmap("Reds_r")
rescale = lambda y: (mb - np.min(mb)) / (np.max(mb) - np.min(mb))
# divnorm = TwoSlopeNorm(vmin=lim_neg, vcenter=0, vmax=0)


q01=np.quantile(data['b'].values, 0.01)
q10=np.quantile(data['b'].values, 0.1)
q50=np.quantile(data['b'].values, 0.5)

q90=np.quantile(data['b'].values, 0.9)
q99=np.quantile(data['b'].values, 0.99)

# make figure
fig, ax = plt.subplots(1, 1, figsize=(10, 3))
# ax.bar(yr, mb, color=cmap(rescale(mb)))

print(mb)

# bb = data['b']*data['ba']
#for plot until 2003
# mb_w.loc[mb_w.Year2>2003] = np.nan
# mb_s.loc[mb_s.Year2>2003] = np.nan
# mb[2004-1989:] = np.nan
ax.set_xlim(1988, 2026)
# ax.bar(yr, mb_w.bw/1000, color='blue', alpha=0.4, label='b_w')
# ax.bar(yr, mb_s.bs/1000, color='red', alpha=0.4, label='b_s')
ax.bar(yr, mb/1000, color='k', label='b')

ax.legend()
# ax.bar(yr, mb, color='k')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('b: specific mass balance (m w.e.)', fontsize=12)
ax.grid(axis='y')
ax.set_facecolor('lightgrey')
ax.set_title('Jamtalferner (1989-2025)')


ax1 = ax.twinx()
ax1.plot(yr, mb.cumsum()/1000, label='b cumulative')
ax1.set_ylabel('cumulative mass balance (m w.e.)', fontsize=12)
ax1.legend(loc='lower left', bbox_to_anchor=(0.1, 0.0))

ax.tick_params(axis='both', which='major', labelsize=12)
ax1.tick_params(axis='both', which='major', labelsize=12)

# uncomment here to add lines for mean and quantiles
# ax.hlines(q01, 1989, 2023, linestyle='--')
# ax.hlines(q10, 1989, 2023, linestyle='--')
# ax.hlines(np.mean(mb), 1989, 2023)

# ax.annotate('Mittel', xy=(2024.7, np.mean(mb)*1.01),  xycoords='data', horizontalalignment='center',
#             fontweight='bold', color='C0'
#             )
# ax.annotate('q10', xy=(2024.3, q10*1.01),  xycoords='data', horizontalalignment='center',
#             fontweight='bold', color='C0'
#             )
# ax.annotate('q01', xy=(2024.3, q01*1.01),  xycoords='data', horizontalalignment='center',
#             fontweight='bold', color='C0'
#             )

fig.savefig('Jam_stripes_black_2025.png')
plt.show()
# stop
# cbar = fig.colorbar(cb)
# cbar.set_label('Annual mass balance (mm w.e.)', rotation=90)

# winter mb anom
# cmapW = plt.get_cmap("Blues")
# rescaleW = lambda y: (mb_w.anom_p - np.min(mb_w.anom_p)) / (np.max(mb_w.anom_p) - np.min(mb_w.anom_p))
# fig2, ax2 = plt.subplots(1, 1, figsize=(10, 4))
# ax2.bar(yr, mb_w.anom_p, color=cmapW(rescaleW(mb_w.anom_p)))
# # ax.bar(yr, mb, color='k')
# ax2.set_xlabel('Year')
# ax2.set_ylabel('winter mass balance anom. (% of timeseries mean)')
# ax2.grid(axis='y')
# ax2.set_facecolor('lightgrey')
# fig2.savefig('Jam_stripes_winter_2023.png')


#winter mb
# fig3, ax3 = plt.subplots(1, 1, figsize=(10, 4))
# ax3.bar(yr, (data['bw']/data['bs']).values, color='k')
# # ax.bar(yr, mb, color='k')
# ax3.set_xlabel('Year')
# ax3.set_ylabel('ratio w/s')
# ax3.grid(axis='y')
# ax3.set_facecolor('lightgrey')

#ratio
# cmapW = plt.get_cmap("Blues")
# rescaleW = lambda y: (mb_w.bw - np.min(mb_w.bw)) / (np.max(mb_w.bw) - np.min(mb_w.bw))
# fig2, ax2 = plt.subplots(1, 1, figsize=(10, 4))
# ax2.bar(yr, mb_w.bw, color=cmapW(rescaleW(mb_w.bw)))
# # ax.bar(yr, mb, color='k')
# ax2.set_xlabel('Year')
# ax2.set_ylabel('winter mass balance')
# ax2.grid(axis='y')
# ax2.set_facecolor('lightgrey')


plt.show()

# fig.savefig('Jam_stripes.png')


