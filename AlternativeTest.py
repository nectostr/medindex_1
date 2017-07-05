from scipy import stats
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

# Getting the data from conver excel format
# !!!
# pdata Pandas data frame
# !!!
pdata = pd.read_csv('data_1_try.csv', delimiter=',')

# Creating consts for inusage
# !!!
# AMOUNT_OF_ANALYSIS Integer
# ALPHA Float --Confidence interval inside math value (1 - conf_int)
# HIGHEST_EXPECTED_VALUE Float
# !!!
AMOUNT_OF_ANALYSIS = 10
ALPHA = 0.05
HIGHEST_EXPECTED_VALUE = 1000


# Creating lists for interim calculations
# !!!
# low_face_of_interval Float[]
# high_face_of_interval Float[]
# minimum_deviation Float[]
# maximum_deviation Float[]
# average_deviation Float[]
# !!!
high_face_of_interval = []
low_face_of_interval = []
minimum_deviation = []
maximum_deviation = []
average_deviation = []


# !!!! Counting part !!!!


# Main cicle for passing each of paramentr in analysis
for k in range(0,AMOUNT_OF_ANALYSIS):

    # Printing the name of analysis
    print(pdata.columns[2*k+1][0:pdata.columns[2*k+1].find('_')])


    # Renew reusable objects
    # !!!
    # average_deviation_value Float
    # amount_of_valid_analysis Integer
    # !!!
    list_of_сurrent_deviation = []
    average_deviation_value = 0
    amount_of_valid_analysis = 0

    # For each analysis in column
    for i in range(len(pdata)):

        # Getting pare of values from all-data format
        # !!!
        # first_value String
        # second_value = String
        # !!!
        first_value = pdata.iloc[i,k*2+1]
        second_value = pdata.iloc[i,k*2+2]

        # Converting this values to float to dicard unusable data
        try:
            first_value = float(first_value)
            second_value = float(second_value)
        except ValueError:
            pass

        # Checking if the data is valid - not empty and clearly converted
        if isinstance(first_value, float) \
                and not math.isnan(first_value) \
                and isinstance(second_value, float) \
                and not math.isnan(second_value):

            # Counting deviation
            # !!!
            # deviation Float
            # !!!
            deviation = first_value-second_value

            # Adding deviation value to list
            list_of_сurrent_deviation.append(deviation)

            # Summuraise with other deviations for future average counting
            average_deviation_value += deviation

            # Increment amount of valid analysis
            amount_of_valid_analysis += 1

    # Checking if there is any valid analysis
    if amount_of_valid_analysis != 0:

        # Finishing avarage value counting
        average_deviation_value /= amount_of_valid_analysis

        # Creating and counting mathematical auxilary data by using \
        # python numpy and stats math library
        # !!!
        # sigma Float --Standard deviation
        # z Float --Dependent on type and amount of data сoefficient
        # SE Float --Precounting for reusable value
        # !!!
        sigma = np.std(list_of_сurrent_deviation)
        z = abs(stats.norm.ppf(ALPHA/2))
        SE = z * sigma/math.sqrt(amount_of_valid_analysis)

        # Counting low and high face of an interval for current analysis
        low_face_of_interval.append(average_deviation_value - SE)
        high_face_of_interval.append(average_deviation_value + SE)

        # Preparing minimum, maximum and average values for counting
        average_deviation.append(0)
        minimum_deviation.append(HIGHEST_EXPECTED_VALUE)
        maximum_deviation.append(-HIGHEST_EXPECTED_VALUE)

        # Checking if value falls into сonfidence interval \
        # and if not counting the average, minimum and maximum deviation
        for i in list_of_сurrent_deviation:
            if i > high_face_of_interval[k]:
                average_deviation[k] += i - high_face_of_interval[k]
                if i - high_face_of_interval[k] > maximum_deviation[k]:
                    maximum_deviation[k] = i - high_face_of_interval[k]
            elif i < low_face_of_interval[k]:
                average_deviation[k] += low_face_of_interval[k] - i
                if low_face_of_interval[k] - i < minimum_deviation[k]:
                    minimum_deviation[k] = i - low_face_of_interval[k]

            # If value falls into interval \
            # amount of valid for countinue counting decreases
            else: amount_of_valid_analysis -= 1

        # Finishing average value counting
        average_deviation[k] /= amount_of_valid_analysis

        # Printing asked values
        print(minimum_deviation[k], ' ', average_deviation[k], ' ', maximum_deviation[k])
        print()

    # Protective data flooding 0 if there was no valid data
    else:
        minimum_deviation.append(0)
        maximum_deviation.append(0)
        low_face_of_interval.append(0)
        high_face_of_interval.append(0)
        average_deviation.append(0)


# !!!! Drawing part !!!!

# Converting average values to valid type fro comfortable printing
# !!!
# x nparray
# y nparray
# upper_error nparray
# lower_error nparray
# asymmetric_error list
# !!
x = np.asarray([average_deviation[0],0])

# Creating fake y values for good-looking drawing
y = np.asarray([0, 0])

# Preparing data for drawing interval from minimum to maximum deviation
lower_error = np.asarray(average_deviation[0]) - np.asarray(minimum_deviation[0])
upper_error = np.asarray(maximum_deviation[0]) - np.asarray(average_deviation[0])
asymmetric_error = [lower_error, upper_error]

# Drawing by using special matplotlab type of drawing points with strange lines
plt.errorbar(x, y, xerr=asymmetric_error, fmt='o', color='red', markersize='1', ecolor = 'blue')

# Show drawned picture
plt.show()