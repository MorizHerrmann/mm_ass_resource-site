# IMPORTS ##############################################################################################################

from environment import Environment
from toolkit import *

# LOAD ENVIRONMENT AND DATA ############################################################################################

Env = Environment()

a, k, f = load_akf('data/all/sprogo_akf.csv')

# COMPUTATION ##########################################################################################################

v_ave_sec_sprogo = np.multiply(a, gamma(1 + 1 / k))

v_ave_sec_nyborg = np.array([7.13674003, 7.08107011, 7.13914375, 7.82517134, 9.18316335, 8.23892537,
                             7.1780441, 7.92467852, 7.94748464, 8.00100587, 8.105415, 6.70802606])
v_ave_sec_korsor = np.array([6.25845442, 6.21060988, 6.2605201, 6.84956709, 8.01289655, 7.20437079,
                             8.20821134, 9.08004951, 9.10670449, 9.16926369, 9.29132604, 7.66022305])

v_ave_sprogo = np.sum(np.multiply(f, v_ave_sec_sprogo))
v_ave_nyborg = np.sum(np.multiply(f, v_ave_sec_nyborg))
v_ave_korsor = np.sum(np.multiply(f, v_ave_sec_korsor))

# OUTPUT ###############################################################################################################

print(f'V_ave - Sprogo: {v_ave_sprogo:.2f}')
print(f'V_ave - Nyborg: {v_ave_nyborg:.2f}')
print(f'V_ave - Korsor: {v_ave_korsor:.2f}')
