# Code to process AWS data from Jamtal provided by HD Tirol  

## step 1 -  convert .zrx files to a merged csv file(s)      
**AWS_Jam_zrxtocsv.py:**   
+ Opens all .zrx files in a given directory, merges the content and writes to a csv file
**AWS_Jam_combinedatasets.py:**   
+ Grabs the merged csv files from two directories
+ merges on the timestamp
+ renames the columns (contains a dictionary for the name changes!)
+ saves a new csv file with all parameters  

## step 2 - plot some data
**AWS_Jam_exampleplt.py:**
+ Loads the merged csv file produced earlier ("dataMerged.csv")
+ Makes a simple time series plot of air temperature, global radiation, rel. humidity, and windspeed, showing daily and monthly means. 
+ saves the plot to a folder called "figs"
**AWS_Jam_Radiationdata.py:**
+ Loads the merged csv file produced earlier ("dataMerged.csv")
+ makes two plots showing various radiation parameters
+ saves the plots to a folder called "figs"