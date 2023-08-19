import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


def plot_avg(csv_file, conc, pep, axis, window):
    '''Opens a csv file and saves the rolling mean data in an np array. Assigns data to the x and y axes, and sets the axis labels.'''

    import csv
    with open(csv_file, "r") as file:
        data = list(csv.reader(file, delimiter = ','))

    npdata = np.array(data[window:], dtype = float)
    xdata = npdata[:, 0]
    ydata = npdata[:, 2]

    axis.plot(xdata, ydata, label = conc)
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
    rolling_window = 5

    for file in file_list:
        df = pd.read_csv("csv_files\\" + file)
        df['rolling_avg'] = df.iloc[:,[1]].rolling(rolling_window).mean()
        df.to_csv("csv_files\\" + file, index = False, header = True)
        y_axis = df.columns[1]

        if counter % 32 == 0:
            fig, ax = plt.subplots(nrows=1, ncols=8, sharey = True)
            ax[peptides_index].set_ylabel(y_axis)

        plot_avg("csv_files\\" + file, concentrations[concentrations_index], peptides[peptides_index], ax[peptides_index], rolling_window)
        counter += 1
        concentrations_index += 1

        if counter % 4 == 0:
            if peptides_index == 7:
                peptides_index = 0
            else:
                peptides_index += 1

            concentrations_index = 0

        if counter != 0 and counter % 32 == 0:
            fig.set_size_inches(18,8)
            fig.savefig("averaged_figures\\" + y_axis + ".png", dpi=120)

    print("All transfers complete. Figures saved in \'averaged_figures\' folder.")

    plt.show(block = False)
