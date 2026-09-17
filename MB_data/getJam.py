import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



# get data for these glaciers:
subset = ['JAMTAL F.']

# file with yearly mb data:
wgms_mb = '/Users/leahartl/Desktop/WGMS/DOI-WGMS-FoG-2025-02/data/mass_balance.csv'
# band data:
wgms_bands = '/Users/leahartl/Desktop/WGMS/DOI-WGMS-FoG-2025-02/data/mass_balance_band.csv'

# Load data 
wgms_df = pd.read_csv(wgms_mb, encoding='unicode_escape')
# extract subset
AT = wgms_df[wgms_df['glacier_name'].isin(subset)]

bands = pd.read_csv(wgms_bands, encoding='unicode_escape')

bands_jam = bands[bands['glacier_name'].isin(subset)]

print(AT[['year', 'annual_balance','ela_position', 'ela']])
print(bands_jam[['year', 'annual_balance', 'summer_balance', 'winter_balance']])


bands_jam.to_csv('check_data.csv')

stop
# print(annual)

def MB_bars(AT, subset):

    fig, ax = plt.subplots(3, 1, figsize=(12, 8))
    ax = ax.flatten()
    for i, g in enumerate(subset):
        gl = AT[(AT['glacier_name'] == g)]
        gl = gl[['year', 'annual_balance', 'summer_balance', 'winter_balance']]
        gl.set_index(gl['year'].astype(int), inplace=True)
        # gl.drop(columns=['YEAR'], inplace=True)
        print(g, gl)
        ax[i].plot(gl.index, gl.annual_balance, color='silver', label='annual mb')
        ax[i].plot(gl.index, gl.summer_balance, color='red', label='summer mb')
        ax[i].plot(gl.index, gl.winter_balance, color='blue', label='winter mb')
        ax[i].set_title(g)
        #ax[i].set_xlim([1950, 2024])

    plt.tight_layout()
    fig.savefig('timeseries_jamtal.png', bbox_inches='tight', dpi=200)

MB_bars(AT, subset)



def MB_bands(bands):

    fig, ax = plt.subplots(1, 1, figsize=(6, 8))
    # ax = ax.flatten()
    for i, y in enumerate(bands.year.unique()):
        tmp = bands.loc[bands['year']==y]
        # ax[0].scatter(tmp.annual_balance, tmp.upper_elevation, label=y)
        ax.scatter(tmp.winter_balance, tmp.upper_elevation, label=y)
        # ax[2].scatter(tmp.summer_balance, tmp.upper_elevation, label=y)

    ax.legend()
        # gl = AT[(AT['glacier_name'] == g)]
        # gl = gl[['year', 'annual_balance', 'summer_balance', 'winter_balance']]
    # bands.set_index(bands['year'].astype(int), inplace=True)


    # ax[0].plot(bands.index, bands.annual_balance, color='silver', label='annual mb')
    # ax[1].plot(bands.index, bands.summer_balance, color='red', label='summer mb')
    # ax[2].plot(bands.index, bands.winter_balance, color='blue', label='winter mb')
    # # ax.set_title(g)
    #     #ax[i].set_xlim([1950, 2024])

    plt.tight_layout()
    fig.savefig('timeseries_jamtal_bands.png', bbox_inches='tight', dpi=200)


MB_bands(bands_jam)
plt.show()

# fig, ax = plt.subplots(1, 1, figsize=(10, 7), sharex=True, sharey=True)
# # ax = ax.flatten()
# # for i, gl in enumerate(subset):
#     # print(gl)
#     # temp = AT[(AT['NAME'] == gl) & (AT['LOWER_BOUND'] == 9999)]
# # AT['NAME'].isin(subset)
# ax.scatter(JAM['annual_balance'].astype(float), JAM['winter_balance'].astype(float))
# # ax[i].set_title(gl)
# ax.grid('both')
# ax.set_ylabel('winter balance, mm w.e.')
# ax.set_xlabel('annual balance, mm w.e.')
# #ax[-1].set_visible(False)

# # fig.tight_layout()
# # # fig.savefig('WinterVAnnual.png')
# # fig, ax = plt.subplots(3, 3, figsize=(10, 7), sharex=True, sharey=True)
# # ax = ax.flatten()
# # for i, gl in enumerate(subset):
# #     # print(gl)
# #     # temp = AT[(AT['NAME'] == gl) & (AT['LOWER_BOUND'] == 9999)]
# # # AT['NAME'].isin(subset)
# #     ax[i].scatter(temp['ANNUAL_BALANCE'].astype(float), temp['SUMMER_BALANCE'].astype(float))
# #     ax[i].set_title(gl)
# #     ax[i].grid('both')
# #     ax[i].set_ylabel('summer balance, mm w.e.')
# #     ax[i].set_xlabel('annual balance, mm w.e.')
# # #ax[-1].set_visible(False)

# # fig.tight_layout()
# # fig.savefig('SummerVAnnual.png')

# # fig, ax = plt.subplots(3, 3, figsize=(10, 7), sharex=True, sharey=True)
# # ax = ax.flatten()
# # for i, gl in enumerate(subset2):
# #     # print(gl)
# #     temp = AT[(AT['NAME'] == gl) & (AT['LOWER_BOUND'] == 9999)]
# # # AT['NAME'].isin(subset)
# #     ax[i].scatter(temp['WINTER_BALANCE'].astype(float), temp['SUMMER_BALANCE'].astype(float))
# #     ax[i].set_title(gl)
# #     ax[i].grid('both')
# #     ax[i].set_ylabel('summer balance, mm w.e.')
# #     ax[i].set_xlabel('Winter balance, mm w.e.')
# # #ax[-1].set_visible(False)

# # fig.tight_layout()
# plt.show()
# stop

# fig.savefig('Auswahl2.png')

# stop

# fig, ax = plt.subplots(4, 3, figsize=(10, 7), sharex=True, sharey=True)
# ax = ax.flatten()
# for i, gl in enumerate(subset):
#     print(gl)
#     temp = AT[(AT['NAME'] == gl) & (AT['LOWER_BOUND'] == 9999)]
# # AT['NAME'].isin(subset)
#     ax[i].bar(temp['YEAR'].astype(int), temp['ANNUAL_BALANCE'].astype(float))
#     ax[i].set_title(gl)
#     ax[i].grid('both')
#     ax[i].set_ylabel('mm w.e.')
# ax[-1].set_visible(False)

# fig.tight_layout()
# fig.savefig('Auswahl.png')

# fig, ax = plt.subplots(7, 3, figsize=(10, 7), sharex=True, sharey=True)
# ax = ax.flatten()
# for i, gl in enumerate(AT['NAME'].unique()):
#     temp = AT[(AT['NAME'] == gl) & (AT['LOWER_BOUND'] == 9999)]
#     ax[i].bar(temp['YEAR'].astype(int), temp['ANNUAL_BALANCE'].astype(float))
#     ax[i].set_title(gl)
#     ax[i].grid('both')
#     ax[i].set_ylabel('mm w.e.')

# fig.tight_layout()
# fig.savefig('Alle.png')

# for i, gl in enumerate(AT['NAME'].unique()):
#     fig, ax = plt.subplots(1, 1, figsize=(10, 7))
#     temp = AT[(AT['NAME'] == gl) & (AT['LOWER_BOUND'] == 9999)]
#     ax.bar(temp['YEAR'].astype(int), temp['ANNUAL_BALANCE'].astype(float))
#     ax.set_title(gl)
#     ax.grid('both')
#     ax.set_ylabel('mm w.e.')
#     fig.tight_layout()
#     fig.savefig(gl.replace("/", "")+'.png')
#     plt.close(fig)

# plt.show()