# WEIBULL PARAMETER METHOD - MICROMETEOROLOGY | ASSIGNMENT 4 | WIND RESOURCE AND SITE ASSESSMENT #######################

"""
find extreme wind speed with weibull parameter method (not reliable)
param: whole_data: path/name of file with all data
param: akf_file: path/name of file with weibull parameters and frequencies for all sections
param: ak_file: path/name of file with weibull parameters over all sections
return: (print extreme winds of each sections and all sections)
"""

# IMPORTS ##############################################################################################################

from toolkit import *
import numpy as np

# INPUTS ###############################################################################################################

whole_data = 'data/all/sprogo.csv'
akf_file = 'data/all/sprogo_akf.csv'
ak_file = 'data/all/sprogo_ak.csv'

# LOAD DATA ############################################################################################################

data = np.loadtxt(whole_data)
a_sec, k_sec, f_sec = load_akf(akf_file)
a, k = load_ak(ak_file)

N = len(data)

# PER SECTION ##########################################################################################################

# number of 10-min averages
N_sec = f_sec * N

# number of independent events
c_ie_sec = 0.438 * N_sec
print(c_ie_sec)

beta_sec = np.multiply(a_sec, np.power(np.log10(c_ie_sec), 1 / k_sec))
alpha_sec = np.divide(np.multiply(a_sec, np.power(np.log10(c_ie_sec), 1 / (k_sec - 1))), k_sec)
U50_sec = alpha_sec * np.log(50) + beta_sec

print(f'Maximal Wind per section:')
print(U50_sec)

# NO SECTIONS ##########################################################################################################

c_ie = 0.438 * N

beta = a * np.log10(c_ie) ** (1/k)
alpha = a / k * np.log10(c_ie) ** (1/(k-1))

U50 = alpha * np.log(50) + beta

print(f'\nMaximal wind over all: {U50[0]:.2f}')
