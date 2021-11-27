# IMPORTS ##############################################################################################################

import matplotlib.pyplot as plt
from scipy.special import gamma
import scipy.optimize as opt
import matplotlib.cm as cm
import pandas as pd
from toolkit import *
from environment import Environment

# LOAD ENVIRONMENT #####################################################################################################

Env = Environment()

########################################################################################################################

cases = ['all', 'max', 'min']

# loop over sites and cases
for i, site in enumerate(Env.sites):
    z0 = Env.z0_sites[i]
    print(site)
    for j, case in enumerate(cases):
        print(case)
        A_org, k, f = load_data('data/' + case + '/sprog_afk.csv')
        G, uf_org = Env.geostrophic_wind(A_org, k)

        def spec_GDL(uf): return Env.GDL(G, uf, z0)

        uf = opt.fsolve(spec_GDL, uf_org)

        # log law
        u = np.multiply(np.divide(uf, k), np.log(Env.z_hub / z0))

        # weibull constants
        a = np.divide(u, gamma(1 + 1 / k))

        aep = Env.AEP(a, k, f)

        print(aep)

# # TASK 2 ###############################################################################################################
#
# # Tyme used two other methods for the extreme wind
#
# A, k = load_data('weibull.csv')[:2]
#
# # number of 10-min averages
# NU = np.array([60453, 46844, 46630, 65511, 106158, 89655, 85495, 120321, 136667, 155201, 120469, 65548])
# # number of independent events
# c_ie = 0.438 * NU
#
# alpha, beta = weibull_parameter_method(A, k, c_ie)
#
# U_T = alpha * np.log10(50) + beta
#
# # (A) EXTRAPOLATE TO SITES #############################################################################################
#
# G_T, uf_T_org = Env.geostrophic_wind2(U_T)
#
# aep_summary = np.zeros((2, ))
#
# for i, site in enumerate(Env.sites):
#     print(site)
#     z0 = Env.z0_sites[i]
#     wb_k = wb_k_case[0]
#     f = f_case[0]
#
#     def spec_GDL(uf): return Env.GDL(G_T, uf, z0)
#
#     uf_T = opt.fsolve(spec_GDL, uf_T_org)
#
#     # log law
#     u = np.multiply(uf_T / wb_k, np.log(Env.z_hub / z0))
#
#     # weibull constants
#     a = np.divide(u, gamma(1 + 1 / wb_k))
#
#     aep_summary[i] = Env.AEP(a, wb_k, f)
#
# print(aep_summary)