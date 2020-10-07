import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# This class is helpful for printing out the data output in the console but is not nessecary for the program
class RainfallData:
    month = 0
    rainfall = 0

    def __init__(self, month, rainfall):
        self.month = monthsDictionary[month]
        self.rainfall = float(rainfall)

    def __str__(self):
        return 'Month: {} Rainfall: {} mm'.format(self.month, self.rainfall)


# Lookup dictionary for the class Rainfall Data to help convert numbers to strings i.e 1 = January, 2 = February etc
monthsDictionary = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}

# This loop converts the csv file given to a more readable file (data wise) separated by 1 comma
with open('heathrowdata.csv', 'r') as csv_file:
    csv_file.readline()
    csv_file.readline()
    my_list = []
    for line in csv_file:
        line = ",".join(line.split())
        line_split = line.split(",")
        rainfall_data = RainfallData(line_split[1], line_split[5])
        my_list.append(rainfall_data)

avg_y_points = []
avg_plus_std_y_points = []
avg_minus_std_y_points = []
for month in monthsDictionary.values():
    rainfall_data_for_month = [*(filter(lambda r: r.month == month, my_list))]
    # NOTE FOR FUTURE SELF: you can wrap lambda functions in list to make it do the same thing
    #  e.g list(filter(lambda...))
    rainfall_array = [*map(lambda rd: rd.rainfall, rainfall_data_for_month)]
    # print(rainfall_data_for_month)
    # print(rainfall_array)
    std = (np.std(np.array(rainfall_array, dtype='f')))
    avg = (np.average(np.array(rainfall_array)))
    sr = (avg + std) - (avg - std)
    avg_y_points.append(avg)
    avg_plus_std_y_points.append(avg + std)
    avg_minus_std_y_points.append(avg - std)
    print(
        '{}:  (Average:{} (mm), Standard Deviation:{} (mm), Upper Bound:{} (mm), Lower Bound:{} (mm), 1 Sigma Range:{} (mm)'.format(
            month, round(avg, 3), round(float(std), 3), round((std + avg), 3), round((avg - std), 3), round(sr, 3)))
    # avg = average value, std = standard deviation, sr = the 1 sigma range (range between avg+std and avg-std)
months_ints = [*range(1, 13)]
print(months_ints)

plot1, = plt.plot(months_ints, avg_y_points, 'kP')  # Black plus marker
plot2, = plt.plot(months_ints, avg_plus_std_y_points, 'm_')  # Magenta horizontal line
plot3, = plt.plot(months_ints, avg_minus_std_y_points, 'm_')
plt.title('Rainfall data for Heathrow 1948-2017 by month')
plt.xlabel('Months')
plt.ylabel('Rainfall (mm)')
plt.grid()
plt.xticks(months_ints)
plt.legend([plot1, plot2], ["Mean value", "1 Sigma range"])
plt.show()
