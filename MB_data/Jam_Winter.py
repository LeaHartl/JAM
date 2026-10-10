import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.dates as mdates
import rasterio as rio
import rioxarray as rxr
# script to process jamtalferner winter mass balance. 
# adapted from Andrea F's matlab file by Lea H. (2025)

# set file paths:
# probe points:
# this needs to have the contain the elevation of the points and the SWE values
points = gpd.read_file('/Users/leahartl/Desktop/Jam2026/winter/sondierungen_schacht_20260423.geojson')
points['elev'] = points['elev'].astype(float)
points['Schneehöhe_m'] = points['Schneehöhe_cm']/100
print(points)

# file with elevation zones for the current glacier area. use the same outline as for the annual MB
zones = gpd.read_file('/Users/leahartl/Desktop/Jam2026/sommer/MB_shapes/2026_all.geojson')
# reproject to crs with true area (don't use lat/lon to compute area)
zones = zones.to_crs(epsg=31254)
points = points.to_crs(epsg=31254)
# dissolve on elevation to get a file with elevation contour areas 
zones = zones.dissolve(by='elev')
zones = zones[['geometry']]
zones['elev'] = zones.index
# add area column
zones['area'] = zones.geometry.area
print(zones)

# set year here:
year = "2025_26"

zonmin = zones['elev'].min()
zonmax = zones['elev'].max()

# --- total area ----
total_area = np.sum(zones.geometry.area)

# make data frame for the zones
winter_df = zones[['elev', 'area']]
winter_df = winter_df.rename(columns={'elev': 'Höhenstufe', 'area': 'Fläche'})
winter_df = winter_df.sort_values(by='Höhenstufe')
print(winter_df)


# Compute zone assignment for each data point based on nearest 50m band
points['Höhenstufe'] = (
    np.round((points['elev'] - zonmin) / 50) * 50 + zonmin
)

# Aggregate sondierungen per zone
agg = points.groupby('Höhenstufe').agg(
    Anzahl_Sondierungen=('WW_m', 'count'),
    Mittlere_Schneehöhe_m=('Schneehöhe_m', 'mean'),
    b_wi_m=('WW_m', 'mean')
).reset_index()

# Merge with zone table
winter_df = winter_df.merge(agg, on='Höhenstufe', how='left')#.fillna(0)
winter_df['Anzahl_Sondierungen'] = winter_df['Anzahl_Sondierungen'].fillna(0)
# fill empty values (if there were no probe points in a given elevation zone, 
# fill mean snow depth and WW with the value from the cloest zone)
winter_df['Mittlere_Schneehöhe_m'] = winter_df['Mittlere_Schneehöhe_m'].ffill().bfill()
winter_df['b_wi_m'] = winter_df['b_wi_m'].ffill().bfill()


# --- Bilanz ---
winter_df['Bilanz_m3'] = winter_df['b_wi_m'] * winter_df['Fläche'] # / 1000. confirm that file is in m, otherwise convert to correct unit.

winter_df['Anzahl_Sondierungen'] = winter_df['Anzahl_Sondierungen'].astype(int)
winter_df['Fläche_m2'] = winter_df['Fläche'].round(decimals=0).astype(int)
winter_df['Mittlere_Schneehöhe_m'] = winter_df['Mittlere_Schneehöhe_m'].round(decimals=2)
winter_df['b_wi_m'] = winter_df['b_wi_m'].round(decimals=3)
winter_df['Bilanz_m3'] = winter_df['Bilanz_m3'].round(decimals=1)

print(winter_df)

forLatex = winter_df.copy()
forLatex['Höhenstufe'] = forLatex['Höhenstufe'].astype(int)
forLatex.index = forLatex['Höhenstufe']
forLatex.drop(columns=['Höhenstufe'], inplace=True)

forLatex['Fläche_km2'] = (forLatex['Fläche']*1e-6)
forLatex['Fläche_km2'] = forLatex['Fläche_km2'].round(decimals=3)

forLatex['Anzahl_Sondierungen'] = forLatex['Anzahl_Sondierungen'].astype(int)
forLatex['Mittlere_Schneehöhe_m'] = forLatex['Mittlere_Schneehöhe_m'].round(decimals=3)

forLatex['b_wi_m'] = forLatex['b_wi_m'].round(decimals=3)
forLatex['Bilanz_m3'] = forLatex['Bilanz_m3'].round(decimals=0).astype(int)
forLatex = forLatex[['Anzahl_Sondierungen', 'Mittlere_Schneehöhe_m', 'b_wi_m', 'Bilanz_m3', 'Fläche_km2']]

# --- Gesamtbilanz ---
bwi = np.mean(points['WW_m'])   # in m w.e.
B = bwi  * total_area # in m³ Wasser
B = np.round(B, decimals=1)

print(bwi, B)
#stop

# --- Results summary ---
d1 = ['Höhenstufe', 'Fläche', 'Anzahl Sondierungen', 'Mittlere Schneehöhe',
      'b_wi', 'Bilanz']
d2 = ['m', 'm²', '', 'm', 'm w.e.', 'm³ Wasser']
d0 = ['Gesamtbilanz:', B, 'm³', 'b_wi Gesamt', bwi, 'mm w.e.',
      'Gesamtfläche:', total_area / 1e6, 'km²', 'Anzahl Sondierungen:', forLatex['Anzahl_Sondierungen'].sum()]
d00 = ['Winterbilanz', 'Jamtalferner', year]

# stop

# # --- Write output files---
# output_file = "/Users/leahartl/Desktop/Jam2025/winter/winterbilanz_jam2025.xlsx"
output_csv = "/Users/leahartl/Desktop/Jam2026/winter/winterbilanz_jam2026.csv"
latex_file = "/Users/leahartl/Desktop/Jam2026/winter/winterbilanz_jam2026_latex.txt"
output_fileIMG = "/Users/leahartl/Desktop/Jam2026/winter/winter_jam.png"

# with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
#     pd.DataFrame([d00]).to_excel(writer, sheet_name=year, startrow=0, header=False, index=False)
#     pd.DataFrame([d0]).to_excel(writer, sheet_name=year, startrow=2, header=False, index=False)
#     pd.DataFrame([d1]).to_excel(writer, sheet_name=year, startrow=5, header=False, index=False)
#     pd.DataFrame([d2]).to_excel(writer, sheet_name=year, startrow=6, header=False, index=False)
#     winter_df.to_excel(writer, sheet_name=year, startrow=7, index=False)


print(f"Gesamtbilanz B = {B:.2f} m³ | b_wi = {bwi:.3f} m w.e. | Fläche = {total_area/1_000_000:.3f} km²")
print('mittlere Schneehöhe_allesondierungen [m]=', points['Schneehöhe_m'].mean())


print(forLatex.to_latex())

forLatex.to_latex(
    latex_file,
    formatters={
        'Mittlere_Schneehöhe_m': '{:.3f}'.format,
        'b_wi_m': '{:.3f}'.format,
        'Fläche_km2': '{:.3f}'.format
    }
)
winter_df.to_csv(output_csv)


# --- Plot ---
plt.figure(figsize=(8, 6))
plt.plot(
    winter_df['Bilanz_m3'],
    winter_df['Höhenstufe'] + 25,
    '--rs',
    linewidth=2,
    markeredgecolor='k',
    markerfacecolor='g',
    markersize=5
)

plt.title(f"Winterbilanz Jamtalferner {year}")
plt.xlabel('Winterbilanz [m$^{3}$ Wasser]')
plt.ylabel('Höhenzone [m]')
plt.tight_layout()
plt.savefig(output_fileIMG, dpi=300)
# plt.savefig('winter_jam.eps', format='eps')
plt.show()

