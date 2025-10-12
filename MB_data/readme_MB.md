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
