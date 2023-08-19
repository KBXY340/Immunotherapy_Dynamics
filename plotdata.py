import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def generate_plot(csv_file, y_axis, conc_list, conc_i):
    '''Opens a csv file and saves the data in an np array. Assigns data to the x and y axes, and sets the axis labels.'''

    import csv
    with open(csv_file, "r") as file:
        data = list(csv.reader(file, delimiter = ','))

    npdata = np.array(data[1:], dtype = float)
    xdata = npdata[:, 0]
    ydata = npdata[:, 1]

    plt.xlabel("time")
    plt.ylabel(y_axis)
    plt.yscale("log")
    plt.plot(xdata, ydata, marker = 'o', label = concentrations[concentrations_index])
    plt.legend()



if __name__ == "__main__":

    df = pd.read_excel("reorganized_data.xlsx")

    counter = 0
    peptides = ["A2", "A8", "N4", "Q4", "Q7", "T4", "V4", "Y3"]
    peptides_index = 0
    concentrations = ["100nM", "10nM", "1nM", "1microM"]
    concentrations_index = 0

    for i in range(len(df.columns)-1):
        csv_filename = df.columns[i+1]
        csv = (df.iloc[:,[0,i+1]]).to_csv(csv_filename, index = False, header = False)
        print("column " + str(i+1) + " transfer complete. Please wait.")

        if counter % 4 == 0:
            plt.figure(peptides[peptides_index], dpi = 120)

            if peptides_index == 7:
                peptides_index = 0
            else:
                peptides_index += 1

            concentrations_index = 0


        y_axis = df.iloc[0,i+1]
        generate_plot(csv_filename, y_axis, concentrations, concentrations_index)

        counter += 1
        concentrations_index += 1

    print("All transfers complete.")
    plt.show(block = False)


