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

cases = ['all', 'least windiest', 'most windiest']

wb_A_all, wb_k_all, f_all = load_data('weibull.csv')
wb_A_min, wb_k_min, f_min = load_data('weibull_min.csv')
wb_A_max, wb_k_max, f_max = load_data('weibull_max.csv')

wb_A_case = [wb_A_all, wb_A_min, wb_A_max]
wb_k_case = [wb_k_all, wb_k_min, wb_k_max]
f_case = [f_all, f_min, f_max]

G_all, uf_org_all = Env.geostrophic_wind(wb_A_all, wb_k_all)
G_min, uf_org_min = Env.geostrophic_wind(wb_A_min, wb_k_min)
G_max, uf_org_max = Env.geostrophic_wind(wb_A_max, wb_k_max)

G_case = [G_all, G_min, G_max]
uf_org_case = [uf_org_all, uf_org_min, uf_org_max]

z0_nyb = np.array([*[Env.z0_water] * 6, *[Env.z0_land] * 6])
z0_kor = np.array([*[Env.z0_land] * 6, *[Env.z0_water] * 6])

sites = ['nyborg', 'korsor']
z0_site = [z0_nyb, z0_kor]

aep_summary = np.zeros((2, 3))
aep_rel = np.zeros((2, 3))

for i, site in enumerate(sites):
    print(site)
    z0 = z0_site[i]

    for j, case in enumerate(cases):
        print(case)
        G = G_case[j]
        wb_k = wb_k_case[j]
        uf_org = uf_org_case[j]
        f = f_case[j]

        def spec_GDL(uf): return Env.GDL(G, uf, z0)

        uf = opt.fsolve(spec_GDL, uf_org)

        # for i in range(len(uf)):
        #   print('Direction : ', i*30, '-', (i+1)*30, '\nu* : ',uf[i])

        # log law
        u = np.multiply(uf / wb_k, np.log(Env.z_hub / z0))

        # weibull constants
        wb_A = np.divide(u, gamma(1 + 1 / wb_k))

        aep_summary[i, j] = Env.AEP(wb_A, wb_k, f)
        aep_rel[i, j] = aep_summary[i, j] / aep_summary[i, 0]

# TASK 2 ###############################################################################################################

# Tyme used two other methods for the extreme wind

A, k = load_data('weibull.csv')[:2]

# number of 10-min averages
NU = np.array([60453, 46844, 46630, 65511, 106158, 89655, 85495, 120321, 136667, 155201, 120469, 65548])
# number of independent events
c_ie = 0.438 * NU

alpha, beta = weibull_parameter_method(A, k, c_ie)

U_T = alpha * np.log10(50) + beta

# (A) EXTRAPOLATE TO SITES #############################################################################################

G_T, uf_T_org = Env.geostrophic_wind2(U_T)

aep_summary = np.zeros((2, ))

for i, site in enumerate(sites):
    print(site)
    z0 = z0_site[i]
    wb_k = wb_k_case[0]
    f = f_case[0]

    def spec_GDL(uf): return Env.GDL(G_T, uf, z0)

    uf_T = opt.fsolve(spec_GDL, uf_T_org)

    # log law
    u = np.multiply(uf_T / wb_k, np.log(Env.z_hub / z0))

    # weibull constants
    wb_A = np.divide(u, gamma(1 + 1 / wb_k))

    aep_summary[i] = Env.AEP(wb_A, wb_k, f)

print(aep_summary)