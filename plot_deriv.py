# DESCRIPTION
#
# Important: each time before running this script, make sure to run 'plotdata.py' to reset all csv files back to the original
#
# Purpose: this script reads from existing csv files and takes the derivative of the raw data and plots a smoothed version
#
# Commenting practice: all comments are written above its respective pieces of code. Every commented section is separated by other sections with new lines


# import libraries
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.interpolate import make_interp_spline as spline


def derivative(xdata, ydata):
    # the new y values are calculated by the slope equation (rise/run)
    yprime = np.diff(ydata)/np.diff(xdata)

    # initialize a list to store the new x values
    xprime = []

    # for every datapoint in the new y values, calculated a corresponding x value; the midpoint between adjascent original x values was chosen
    for i in range(len(yprime)):
        x_mid = (xdata[i+1] + xdata[i]) / 2
        xprime = np.append(xprime, x_mid)

    return xprime, yprime


def plot_graph(xdata, ydata, conc, pep, axis):
    # smooth the data before plotting for clearer analysis
    x_y_spline = spline(xdata, ydata)

    smoothed_xdata = np.linspace(xdata.min(), xdata.max(), 500)
    smoothed_ydata = x_y_spline(smoothed_xdata)

    axis.plot(smoothed_xdata, smoothed_ydata, label = conc)
    axis.set_title(pep)
    axis.set_xlabel("Time")
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
    ax_outer_i = 0
    ax_inner_i = 0
    miny = 1000
    maxy = -1000

    import csv
    for csv_file in file_list:

        with open("csv_files\\" + csv_file, "r") as file:
            data = list(csv.reader(file, delimiter = ','))

            # extract only the header row
            header = np.array(data[0])

            npdata = np.array(data[1:], dtype = float)
            xdata = npdata[:, 0]
            ydata = npdata[:, 1]

        # save the y axis label as the second element of the extracted header row
        y_axis = header[1]

        # for the 0-th iteration and, thereafter, every 32 iterations (AKA 8 axes on one figure), create a new figure to graph the next 8 axes; to see the lines better, the subplots are divided into 4 plots on the first row and 4 plots on the second row
        if counter % 32 == 0:
            fig, ax = plt.subplots(nrows=2, ncols=4, figsize=(18,6))
            print("Current figure being created: " + str(counter / 32))

            # for figures with subplots across more than 1 row, the axes indices are referred to like nested lists
            ax[ax_outer_i][ax_inner_i].set_ylabel(y_axis)

        xprime, yprime = derivative(xdata, ydata)

        # for each iteration, find the minimum and maximum y values of the current yprime list; keep swapping if new mins and maxes are found
        if np.min(yprime) < miny:
            miny = np.min(yprime)
        if np.max(yprime) > maxy:
            maxy = np.max(yprime)


        plot_graph(xprime, yprime, concentrations[concentrations_index], peptides[peptides_index], ax[ax_outer_i][ax_inner_i])
        counter += 1
        concentrations_index += 1

        if counter % 4 == 0:
            # for 4 lines in one plot, need only set the y scale limits once; attempts to set the y limits to the most min and max y values found from the past 4 iterations
            ax[ax_outer_i][ax_inner_i].set_ylim(bottom = miny, top = maxy)

            # if the index of the peptides list reaches the end, that means a new figure will be created, thus both indices for the nested list returns to 0
            if peptides_index == 7:
                peptides_index = 0
                ax_outer_i = 0
                ax_inner_i = 0
            else:
                peptides_index += 1

            concentrations_index = 0
            ax_inner_i += 1
            # min and max y values are restored back to initialized numbers because have to start from the beginning for the next 4 lines (can't carryover mins and maxes from previous subplots)
            miny = 1000
            maxy = -1000

        # for every 16 iterations (AKA the top 4 row of subplots), the inner index of the nested list must return to 0 to reference the first subplot of the second row
        if counter % 16 == 0:
            ax_inner_i = 0

            # for every 16 iterations that are not iterations of 32 (AKA not the end of the figure, only the end of the first row on the same figure), the outer axes index must be 1 to reference the bottom row of subplots
            if counter % 32 != 0:
                ax_outer_i = 1
            # if it is iterations of 32, then outer index must return to 0 as well since a new figure is being created
            else:
                ax_outer_i = 0

        # for every 32 iterations (not considering 0-th), the current opened figure is saved into a folder
        if counter != 0 and counter % 32 == 0:
            fig.set_size_inches(18,15)
            fig.savefig("derivative_figures\\" + y_axis + ".png", dpi=120)

    print("All transfers complete. Figures saved in \'derivative_figures\' folder.")

    # UNCOMMENT BELOW TO SHOW FIGURES AFTER ALL PLOTTING HAS BEEN COMPLETED, ELSE FIGURES CAN BE VIEWED IN THE SPECIFIED FOLDER
    # plt.show(block = False)

