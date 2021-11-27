# IMPORTS ##############################################################################################################

import numpy as np

# INPUT ################################################################################################################

base = 'data/'

file = base + 'all/sprog.csv'
out_file = 'sprog'
save = False

# LOAD DATA ############################################################################################################

data = np.loadtxt(file)

# for t in range(len(data)):
#     data[t, 0] = int(data[t, 0])

# find years
first_year = int(min(data[:, 0]))
last_year = int(max(data[:, 0]))
years = np.array([y for y in range(first_year, last_year + 1)])
n_years = len(years)

print(np.std(data[:, 5]))

# CALCULATE STATISTICS #################################################################################################

means = np.zeros((n_years, ))
stds = np.zeros((n_years, ))

for y in range(n_years):
    data_of_year = data[data[:, 0] == years[y], 5]
    means[y] = np.mean(data_of_year)
    stds[y] = np.std(data_of_year)

u_min = min(means)
u_max = max(means)

year_min = years[means == u_min]
year_max = years[means == u_max]

# SAVE MIN AND MAX YEAR ################################################################################################

data_min = data[data[:, 0] == year_min, :]
data_max = data[data[:, 0] == year_max, :]

print(np.std(means))

if save: np.savetxt(base + 'min/' + out_file + '_min.csv', data_min)
if save: np.savetxt(base + 'max/' + out_file + '_max.csv', data_max)
