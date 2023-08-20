import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.interpolate import make_interp_spline as spline


def derivative(xdata, ydata):
    yprime = np.diff(ydata)/np.diff(xdata)
    xprime = []

    for i in range(len(yprime)):
        x_mid = (xdata[i+1] + xdata[i]) / 2
        xprime = np.append(xprime, x_mid)

    return xprime, yprime


def plot_graph(xdata, ydata, conc, pep, axis):
    x_y_spline = spline(xdata, ydata)

    smoothed_xdata = np.linspace(xdata.min(), xdata.max(), 500)
    smoothed_ydata = x_y_spline(smoothed_xdata)

    axis.plot(smoothed_xdata, smoothed_ydata, label = conc)
    axis.set_title(pep)
    axis.set_xlabel("Time")
    axis.set_yscale("log")
    axis.legend(loc="upper right")


if __name__ == "__main__":

    file_list = sorted(os.listdir("csv_files"))

    counter = 0
    peptides = ["A2", "A8", "N4", "Q4", "Q7", "T4", "V4", "Y3"]
    peptides_index = 0
    concentrations = ["100nM", "10nM", "1nM", "1microM"]
    concentrations_index = 0

    import csv
    for csv_file in file_list:

        with open("csv_files\\" + csv_file, "r") as file:
            data = list(csv.reader(file, delimiter = ','))
            header = np.array(data[0])
            npdata = np.array(data[1:], dtype = float)
            xdata = npdata[:, 0]
            ydata = npdata[:, 1]

        y_axis = header[1]

        if counter % 32 == 0:
            fig, ax = plt.subplots(nrows=1, ncols=8, sharey = True)
            ax[peptides_index].set_ylabel(y_axis)

        xprime, yprime = derivative(xdata, ydata)

        plot_graph(xprime, yprime, concentrations[concentrations_index], peptides[peptides_index], ax[peptides_index])
        counter += 1
        concentrations_index += 1

        if counter % 4 == 0:
            if peptides_index == 7:
                peptides_index = 0
            else:
                peptides_index += 1

            concentrations_index = 0

        if counter != 0 and counter % 32 == 0:
            fig.set_size_inches(20,8)
            fig.savefig("derivative_figures\\" + y_axis + ".png", dpi=120)

    plt.show(block = False)

