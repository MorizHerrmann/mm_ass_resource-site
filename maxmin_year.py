# YEAR WITH LEAST AND MOST WIND - MICROMETEOROLOGY | ASSIGNMENT 4 | WIND RESOURCE AND SITE ASSESSMENT ##################

"""
Find year with least and most wind.
param: file: whole data set
param: out_file: name of output file (without extension)
param: save: if False only verbal output
return: (save max and min file, print the maximum and minimum yearly wind speed)
"""

# IMPORTS ##############################################################################################################

import numpy as np

# INPUT ################################################################################################################

base = 'data/'

file = base + 'all/sprogo.csv'
out_file = 'sprogo'
save = False

# LOAD DATA ############################################################################################################

data = np.loadtxt(file)

# find years
first_year = int(min(data[:, 0]))
last_year = int(max(data[:, 0]))

# years axis
years = np.array([y for y in range(first_year, last_year + 1)])
n_years = len(years)

# calculate means
means = np.zeros((n_years, ))
for y in range(n_years):
    data_of_year = data[data[:, 0] == years[y], 5]
    means[y] = np.mean(data_of_year)

# find corresponding years
u_min = min(means)
u_max = max(means)

year_min = years[means == u_min]
year_max = years[means == u_max]

# save min and max year
data_min = data[data[:, 0] == year_min, :]
data_max = data[data[:, 0] == year_max, :]

if save: np.savetxt(base + 'min/' + out_file + '_min.csv', data_min)
if save: np.savetxt(base + 'max/' + out_file + '_max.csv', data_max)
