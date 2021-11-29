# CALCULATE WEIBULL PARAMETERS - MICROMETEOROLOGY | ASSIGNMENT 4 | WIND RESOURCE AND SITE ASSESSMENT ###################

"""
Calculate Weibull Parameters (A/a = scale, k = shape). Usually used for whole data, i.e. not sectionalized.
param: data_file: path/name of data
param: output_file: path/name of output file
return: (save A and k)
"""

# IMPORTS ##############################################################################################################

from toolkit import *
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

df = pd.DataFrame(data, columns=labels)

if save: df.to_csv(output_file)
