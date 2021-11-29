# CALCULATE AVERAGE WIND SPEED - MICROMETEOROLOGY | ASSIGNMENT 4 | WIND RESOURCE AND SITE ASSESSMENT ###################

"""
Calculate average wind speed from weibull parameters for Sprogo, and from mean wind speed of sections for Nyborg and
Korsor.
param: akf_file: path/file where weibull parameters and frequecny of occurrency is saved.
param: v_ave_sec_nyborg: average wind speed for each section at Nyborg
param: v_ave_sec_korsor: average wind speed for each section at Korsor
return: (print average wind speed at Sprogo, Nyborg and Korsor)
"""

# IMPORTS ##############################################################################################################

from environment import Environment
from toolkit import *

# INPUT ################################################################################################################

akf_file = 'data/all/sprogo_akf.csv'

v_ave_sec_nyborg = np.array([7.13674003, 7.08107011, 7.13914375, 7.82517134, 9.18316335, 8.23892537,
                             7.1780441, 7.92467852, 7.94748464, 8.00100587, 8.105415, 6.70802606])
v_ave_sec_korsor = np.array([6.25845442, 6.21060988, 6.2605201, 6.84956709, 8.01289655, 7.20437079,
                             8.20821134, 9.08004951, 9.10670449, 9.16926369, 9.29132604, 7.66022305])

# LOAD ENVIRONMENT AND DATA ############################################################################################

Env = Environment()

a, k, f = load_akf(akf_file)

# COMPUTATION ##########################################################################################################

# calculate average wind speed at Sprogo from weibull parameters
v_ave_sec_sprogo = np.multiply(a, gamma(1 + 1 / k))

# average mean wind speed of each section, weighted with its frequency of occurrence
v_ave_sprogo = np.sum(np.multiply(f, v_ave_sec_sprogo))
v_ave_nyborg = np.sum(np.multiply(f, v_ave_sec_nyborg))
v_ave_korsor = np.sum(np.multiply(f, v_ave_sec_korsor))

# OUTPUT ###############################################################################################################

print(f'V_ave - Sprogo: {v_ave_sprogo:.2f}')
print(f'V_ave - Nyborg: {v_ave_nyborg:.2f}')
print(f'V_ave - Korsor: {v_ave_korsor:.2f}')
