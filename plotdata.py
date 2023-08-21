# DESCRIPTION
#
# Important: Run this script before running any of the other scripts every time you wish to re-run the other ones to reset the csv file contents back to their original form
#
# Purpose: this script transfers the data from a single excel file to multiple csv files, then reads each csv file and creates 7 figures (one for each cytokine), each with 8 subplots (one for each peptide) on them, and has 4 lines (one for each concentration) on each subplot
#
# Note: All three scripts make use of the matplotlib.pyplot 'subplots' function. Subplot 'figure' is the large container that contains multiple subplots; Subplot 'axes' are the subplots on one figure (ex. 8 subplots on 1 figure means 8 axes)
#
# Commenting practice: all comments are written above its respective pieces of code. Every commented section is separated by other sections with new lines


# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def generate_plot(csv_file, conc, pep, axis):
    '''Opens a csv file and saves the data in an np array. Assigns data to the x and y axes, and sets the axis labels.'''

    import csv
    with open(csv_file, "r") as file:
        # reads in the csv file as a list of all the contents and assigns it to data
        data = list(csv.reader(file, delimiter = ','))

    # the first row in data is the header, so the actual data begins at index '1' to the end
    npdata = np.array(data[1:], dtype = float)

    # assigns all the rows of the 0-th column to xdata, and all the rows of the 1-st column to ydata
    xdata = npdata[:, 0]
    ydata = npdata[:, 1]

    # plots the data with conc legend on the specific matplotlib subplot axis of the current opened figure
    axis.plot(xdata, ydata, marker = "o", label = conc)
    axis.set_title(pep)
    axis.set_xlabel("Time")
    axis.set_yscale("log")
    axis.legend(loc="upper right")


if __name__ == "__main__":

    # used pandas to read the excel file into a pandas dataframe (df)
    df = pd.read_excel("reorganized_data.xlsx")

    # initialize variables
    counter = 0
    peptides = ["A2", "A8", "N4", "Q4", "Q7", "T4", "V4", "Y3"]
    peptides_index = 0
    concentrations = ["100nM", "10nM", "1nM", "1microM"]
    concentrations_index = 0

    # loop through all the columns of data in the file
    for i in range(len(df.columns)-1):
        csv_filename = df.columns[i+1]

        # read the 'time' column along with another single column each time the loop runs and save them to a csv file
        csv = (df.iloc[:,[0,i+1]]).to_csv("csv_files\\" + csv_filename, index = False, header = False)
        print("column " + str(i+1) + " transfer complete. Please wait.")

        # get the name of the cytokine that each column refers to and save it to be set as the y axis label
        y_axis = df.iloc[0,i+1]

        # for the 0-th iteration, and thereafter every 32 iterations (AKA 8 axes on one figure), create a new figure to graph the next 8 axes
        if counter % 32 == 0:
            fig, ax = plt.subplots(nrows=1, ncols=8, sharey = True)

            # because 'sharey' is on, the y axis label need only be set for every 8 axes
            ax[peptides_index].set_ylabel(y_axis)


        generate_plot("csv_files\\" + csv_filename, concentrations[ concentrations_index], peptides[peptides_index], ax[peptides_index])
        counter += 1
        concentrations_index += 1

        # for every 4 iterations, a new axes should be plotted on, hence incrementing peptides_index; but, after incrementing peptides_index 8 times, the axes should start back at '0' index because a new figure is created
        if counter % 4 == 0:
            if peptides_index == 7:
                peptides_index = 0
            else:
                peptides_index += 1

            concentrations_index = 0

        # for every 32 iterations (not considering 0-th), the current opened figure is saved into a folder
        if counter != 0 and counter % 32 == 0:
            fig.set_size_inches(18,8)
            fig.savefig("raw_figures\\" + y_axis + ".png", dpi=120)

    print("All transfers complete. Figures saved in \'raw_figures\' folder.")

    # UNCOMMENT BELOW TO SHOW FIGURES AFTER ALL PLOTTING HAS BEEN COMPLETED, ELSE FIGURES CAN BE VIEWED IN THE SPECIFIED FOLDER
    # plt.show(block = False)


