# IMPORTS ##############################################################################################################

from toolkit import *
import os
import pandas as pd

# INPUTS ###############################################################################################################

data_file = 'data/all/sprogo.csv'
output_file = 'data/all/sprogo_ak.csv'

save = True

# COMPUTATION ##########################################################################################################

# find total number of measurements
data = np.loadtxt(data_file)

# fetch speed
u = data[:, 5]

# compute weibull parameters
a, k = find_weibull(u)

# BUNDLE AND SAVE DATA #################################################################################################

labels = ['A', 'k']
data = np.array([[a], [k]]).transpose()
print(data.shape)

df = pd.DataFrame(data, columns=labels)

if save: df.to_csv(output_file)
