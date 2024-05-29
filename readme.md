# Code to process AWS data from Jamtal

## step 1 -  convert .zrx files to a merged csv file(s)      
**AWS_Jam_zrxtocsv.py:**   
+ Opens all .zrx files in a given directory, merges the content and writes to a csv file       
**AWS_Jam_combinedatasets.py:**   
+ Grabs the merged csv files from two directories
+ Merges on the timestamp
+ Renames the columns (contains a dictionary for the name changes!)
+ Saves a new csv file with all parameters  

## step 2 - plot some data
**AWS_Jam_exampleplt.py:**
+ Loads the merged csv file produced earlier ("dataMerged.csv")
+ Makes a simple time series plot of air temperature, global radiation, rel. humidity, and windspeed, showing daily and monthly means. 
+ Makes another time series plot of monthly precip sums and snow depth.
+ Saves the plots to a folder called "figs"         
**AWS_Jam_Radiationdata.py:**
+ Loads the merged csv file produced earlier ("dataMerged.csv")
+ Makes two plots showing various radiation parameters
+ Saves the plots to a folder called "figs"