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
points = gpd.read_file('/Users/leahartl/Desktop/Jam2025/winter/sondierungen_20250426.shp')
print(points)
# file with elevation zones for the current glacier area. use the same outline as for the annual MB
zones = gpd.read_file('/Users/leahartl/Desktop/Jam2025/sommer/MB_viole/JAM_mb_2025.geojson')
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
year = "2024_25"

zonmin = zones['elev'].min()
zonmax = zones['elev'].max()
# winterzones = np.arange(zonmin, zonmax + 1, 50)

# --- total area ----
total_area = np.sum(zones.geometry.area)

# make data frame for the zones
winter_df = zones[['elev', 'area']]
winter_df = winter_df.rename(columns={'elev': 'Höhenstufe', 'area': 'Fläche'})
winter_df = winter_df.sort_values(by='Höhenstufe')
print(winter_df)


# Compute zone assignment for each data point based on nearest 50m band
points['Höhenstufe'] = (
    np.round((points['Z_value'] - zonmin) / 50) * 50 + zonmin
)

# Aggregate sondierungen per zone
agg = points.groupby('Höhenstufe').agg(
    Anzahl_Sondierungen=('Z_value', 'count'),
    Mittlere_Schneehöhe=('SH', 'mean'),
    b_wi=('WW', 'mean')
).reset_index()

# Merge with zone table
winter_df = winter_df.merge(agg, on='Höhenstufe', how='left')#.fillna(0)
winter_df['Anzahl_Sondierungen'] = winter_df['Anzahl_Sondierungen'].fillna(0)
# fill empty values (if there were no probe points in a given elevation zone, 
# fill mean snow depth and WW with the value from the cloest zone)
winter_df['Mittlere_Schneehöhe'] = winter_df['Mittlere_Schneehöhe'].ffill().bfill()
winter_df['b_wi'] = winter_df['b_wi'].ffill().bfill()


# --- Bilanz ---
winter_df['Bilanz'] = winter_df['b_wi'] / 1000 * winter_df['Fläche']

winter_df['Anzahl_Sondierungen'] = winter_df['Anzahl_Sondierungen'].astype(int)
winter_df['Fläche'] = winter_df['Fläche'].round(decimals=0).astype(int)
winter_df['Mittlere_Schneehöhe'] = winter_df['Mittlere_Schneehöhe'].round(decimals=1)
winter_df['b_wi'] = winter_df['b_wi'].round(decimals=1)
winter_df['Bilanz'] = winter_df['Bilanz'].round(decimals=1)

print(winter_df)

forLatex = winter_df.copy()
forLatex['Höhenstufe'] = forLatex['Höhenstufe'].astype(int)
forLatex.index = forLatex['Höhenstufe']
forLatex.drop(columns=['Höhenstufe'], inplace=True)

forLatex['Fläche'] = (forLatex['Fläche']*1e-6)
forLatex['Fläche'] = forLatex['Fläche'].round(decimals=3)

forLatex['Anzahl_Sondierungen'] = forLatex['Anzahl_Sondierungen'].astype(int)
forLatex['Mittlere_Schneehöhe'] = forLatex['Mittlere_Schneehöhe'].astype(int)

forLatex['b_wi'] = forLatex['b_wi'].round(decimals=0).astype(int)
forLatex['Bilanz'] = forLatex['Bilanz'].round(decimals=0).astype(int)


# --- Gesamtbilanz ---
bwi = np.mean(points['WW'])   # in mm w.e.
B = bwi / 1000 * total_area # in m³ Wasser
B = np.round(B, decimals=1)

# --- Results summary ---
d1 = ['Höhenstufe', 'Fläche', 'Anzahl Sondierungen', 'Mittlere Schneehöhe',
      'b_wi', 'Bilanz']
d2 = ['m', 'm²', '', 'cm', 'mm w.e.', 'm³ Wasser']
d0 = ['Gesamtbilanz:', B, 'm³', 'b_wi Gesamt', bwi, 'mm w.e.',
      'Gesamtfläche:', total_area / 1e6, 'km²', 'Anzahl Sondierungen:', forLatex['Anzahl_Sondierungen'].sum()]
d00 = ['Winterbilanz', 'Jamtalferner', year]


# --- Write output files---
output_file = "/Users/leahartl/Desktop/Jam2025/winter/winterbilanz_jam2025.xlsx"
output_csv = "/Users/leahartl/Desktop/Jam2025/winter/winterbilanz_jam2025.csv"
latex_file = "/Users/leahartl/Desktop/Jam2025/winter/winterbilanz_jam2025_latex.txt"
output_fileIMG = "/Users/leahartl/Desktop/Jam2025/winter/winter_jam.png"

with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    pd.DataFrame([d00]).to_excel(writer, sheet_name=year, startrow=0, header=False, index=False)
    pd.DataFrame([d0]).to_excel(writer, sheet_name=year, startrow=2, header=False, index=False)
    pd.DataFrame([d1]).to_excel(writer, sheet_name=year, startrow=5, header=False, index=False)
    pd.DataFrame([d2]).to_excel(writer, sheet_name=year, startrow=6, header=False, index=False)
    winter_df.to_excel(writer, sheet_name=year, startrow=7, index=False)


print(f"Gesamtbilanz B = {B:.2f} m³ | b_wi = {bwi:.2f} mm w.e. | Fläche = {total_area/1_000_000:.3f} km²")
print('mittlere Schneehöhe_allesondierungen=', points['SH'].mean())


print(forLatex.to_latex())
forLatex.to_latex(latex_file)
winter_df.to_csv(output_csv)


# --- Plot ---
plt.figure(figsize=(8, 6))
plt.plot(
    winter_df['Bilanz'],
    winter_df['Höhenstufe'] + 25,
    '--rs',
    linewidth=2,
    markeredgecolor='k',
    markerfacecolor='g',
    markersize=5
)

plt.title(f"Winterbilanz Jamtalferner {year}")
plt.xlabel('Spezifische Winterbilanz [mm w.e.]')
plt.ylabel('Höhenzone [m]')
plt.tight_layout()
plt.savefig(output_fileIMG, dpi=300)
# plt.savefig('winter_jam.eps', format='eps')
plt.show()

