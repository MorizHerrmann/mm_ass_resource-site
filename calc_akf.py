# IMPORTS ##############################################################################################################

from toolkit import *
import os
import pandas as pd

# INPUTS ###############################################################################################################

base = 'data/all/'
site = 'sprogo'

whole_data_file = base + site + '.csv'
sect_dir = base + site + '_sec/'

output_file = base + site + '_afk.csv'

save = True

# COMPUTATION ##########################################################################################################

# find total number of measurements
whole_data = np.loadtxt(whole_data_file)
T = len(whole_data)

# find number of sections
S = len(os.listdir(sect_dir))

# initialize result
a_list = np.zeros((S,))     # weibull scale parameter
k_list = np.zeros((S,))     # weibull shape parameter
f_list = np.zeros((S,))     # frequency of occurrence

for sec, file in enumerate(os.listdir(sect_dir)):
    print(file)

    # load data
    data = np.loadtxt(sect_dir + file)

    # determine frequency of occurrence
    f_list[sec] = len(data) / T

    # fetch speed
    u = data[:, 5]

    # compute weibull parameters
    a, k = find_weibull(u)

    a_list[sec] = a
    k_list[sec] = k

# BUNDLE AND SAVE DATA #################################################################################################

labels = ['A', 'k', 'f']
data = np.array([a_list, k_list, f_list]).transpose()

df = pd.DataFrame(data, columns=labels)

if save: df.to_csv(output_file)
