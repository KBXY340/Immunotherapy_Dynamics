# Immunotherapy_Dynamics
## About
All the code and data used for data reproduction and manipulation of the initial raw data provided in the paper: "Universal antigen encoding of T cell activation from high-dimensional cytokine dynamics" written by Sooraj R. Achar, François X. P. Bourassa, Thomas J. Rademaker, Angela Lee, Taisuke Kondo, Emanuel Salazar-Cavazos, John S. Davies, Naomi Taylor, Paul François, and Grégoire Altan-Bonnet.

## Important
Both "fitavg.py" and "plot_deriv.py" require the original output data in the csv files. **Before running or re-running _either_ script, ensure "plotdata.py" is run _first_ every time.** <br />
<br />
"plotdata.py" reads in an excel file; when downloading, keep "reorganized_data" as an excel file.

## Code Description
"reorganized_data.xlsx": contains all the initial data to be used in the data processing, formatted to specifically fit the use of the codes. <br />
"plotdata.py": reads in the excel file and converts each column to a separate csv file, then plots each csv file's contents. <br />
"fitavg.py": reads the existing csv files from "plotdata.py" and plots a rolling mean fit of each file. <br />
"plot_deriv.py": reads the existing csv files from "plotdata.py", smooths the data, and plots the derivative of the contents in each file.

