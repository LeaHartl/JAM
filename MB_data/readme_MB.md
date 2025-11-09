# Code to process Jamtal mass balance data and produce figures

## winter mass balance     
**sondierungen.py:**   
+ Processes .gpx files of snow depth probing, saves them as shapefile     
+ makes an example map showing the probing data on the glacier

## process stake data and shapefiles     
**ProcessStakes_JAM_annual.py:**	
+ reads data from excel file of annual stake values (needs to exist), 1989-current	
+ formats to csv table with additional information, as for MWK and VK in ESSD paper	
+ calls on Uncertainties.py to produce uncertainy information	

**ProcessShapefiles_JAM.py:**	
+ loads .geojson files containing elevation and MB information (1989-present), folder needs to exist	
+ makes various plots from this	



## for MB report

**Jam_Winter.py**	
+ loads the shapefile of probe points produced in sondierungen.py		
+ loads elevation zones	
+ produces winter massbalance output per elevation zones and saves to tables (excel, csv, latex)	

**Jam_Sommer.py**	
+ loads the shapefile of MB isolines and elevations zones produces in GIS 	
+ processes the file to make MB per elevations zones	
+ saves	MB output to tables (text, latex)
+ makes a map plot of the iso zones for the report	

+ loads winter mass balance output produced with Jam_Winter.py	
+ makes elevation zones plot for the report
+ makes plots and tables for individual glacier parts (adjust for changing file names in the file)

**MakeClimPlot_Bericht.py**		
+ makes the climate plot and tables using Galtür data pulled from Geosphere API and daily data for Jamtal provided by HD.
+ makes latex table of excel with Regenmesser data. Needs to be adjusted depending on what that file looks like. 

