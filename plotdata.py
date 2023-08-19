import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def generate_plot(csv_file, conc, pep, axis):
    '''Opens a csv file and saves the data in an np array. Assigns data to the x and y axes, and sets the axis labels.'''

    import csv
    with open(csv_file, "r") as file:
        data = list(csv.reader(file, delimiter = ','))

    npdata = np.array(data[1:], dtype = float)
    xdata = npdata[:, 0]
    ydata = npdata[:, 1]

    axis.plot(xdata, ydata, marker = "o", label = conc)
    axis.set_title(pep)
    axis.set_xlabel("Time")
    axis.set_yscale("log")
    axis.legend(loc="upper right")





if __name__ == "__main__":

    df = pd.read_excel("reorganized_data.xlsx")

    counter = 0
    peptides = ["A2", "A8", "N4", "Q4", "Q7", "T4", "V4", "Y3"]
    peptides_index = 0
    concentrations = ["100nM", "10nM", "1nM", "1microM"]
    concentrations_index = 0

    for i in range(len(df.columns)-1):
        csv_filename = df.columns[i+1]
        csv = (df.iloc[:,[0,i+1]]).to_csv("csv_files\\" + csv_filename, index = False, header = False)
        print("column " + str(i+1) + " transfer complete. Please wait.")
        y_axis = df.iloc[0,i+1]

        if counter % 32 == 0:
            fig, ax = plt.subplots(nrows=1, ncols=8, sharey = True)
            ax[peptides_index].set_ylabel(y_axis)


        generate_plot("csv_files\\" + csv_filename, concentrations[ concentrations_index], peptides[peptides_index], ax[peptides_index])
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
            fig.savefig("figures\\" + y_axis + ".png", dpi=120)

    print("All transfers complete.")

    plt.show(block = False)


