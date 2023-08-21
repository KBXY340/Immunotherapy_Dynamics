# DESCRIPTION
#
# Important: each time before running this script, make sure to run 'plotdata.py' to reset all csv files back to the original
#
# Purpose: this script is similar in function to 'plotdata.py' but reads directly from already existing csv files, calculates a rolling mean for each graphed line and replots the averaged graphs in the same manner as the raw data
#
# Commenting practice: all comments are written above its respective pieces of code. Every commented section is separated by other sections with new lines


# import libraries
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.interpolate import make_interp_spline as spline


def plot_avg(csv_file, conc, pep, axis, window):
    '''Opens a csv file and saves the rolling mean data in an np array. Assigns data to the x and y axes, smooths using scipy, and sets the axis labels.'''

    import csv
    with open(csv_file, "r") as file:
        data = list(csv.reader(file, delimiter = ','))

    npdata = np.array(data[window:], dtype = float)
    xdata = npdata[:, 0]
    ydata = npdata[:, 2]

    # used a built-in function of the scipy library
    x_y_spline = spline(xdata, ydata)

    smoothed_xdata = np.linspace(xdata.min(), xdata.max(), 500)
    smoothed_ydata = x_y_spline(smoothed_xdata)

    axis.plot(smoothed_xdata, smoothed_ydata, label = conc)
    axis.set_title(pep)
    axis.set_xlabel("Time")
    axis.set_yscale("log")
    axis.legend(loc="upper right")


if __name__ == "__main__":
    # list all the csv files saved in the folder and sort them based on their ASCII values
    file_list = sorted(os.listdir("csv_files"))

    # initialize variables
    counter = 0
    peptides = ["A2", "A8", "N4", "Q4", "Q7", "T4", "V4", "Y3"]
    peptides_index = 0
    concentrations = ["100nM", "10nM", "1nM", "1microM"]
    concentrations_index = 0
    rolling_window = 5

    for file in file_list:
        df = pd.read_csv("csv_files\\" + file)

        # add a new column to the csv files that takes the cytokine values column and computes a rolling mean
        df['rolling_avg'] = df.iloc[:,[1]].rolling(rolling_window).mean()
        df.to_csv("csv_files\\" + file, index = False, header = True)

        # set the y axis label as the second element of the header row
        y_axis = df.columns[1]

        # for the 0-th iteration and, thereafter, every 32 iterations (AKA 8 axes on one figure), create a new figure to graph the next 8 axes
        if counter % 32 == 0:
            fig, ax = plt.subplots(nrows=1, ncols=8, sharey = True)
            print("Current figure being created: " + str(counter / 32))

            # because 'sharey' is on, the y axis label need only be set for every 8 axes
            ax[peptides_index].set_ylabel(y_axis)

        plot_avg("csv_files\\" + file, concentrations[concentrations_index], peptides[peptides_index], ax[peptides_index], rolling_window)
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
            fig.savefig("averaged_figures\\" + y_axis + ".png", dpi=120)

    print("All plots complete. Figures saved in \'averaged_figures\' folder. Rolling averages updated in \'csv_files\' folder.")

    # UNCOMMENT BELOW TO SHOW FIGURES AFTER ALL PLOTTING HAS BEEN COMPLETED, ELSE FIGURES CAN BE VIEWED IN THE SPECIFIED FOLDER
    # plt.show(block = False)
