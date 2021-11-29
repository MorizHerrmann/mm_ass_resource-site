# VARIATION OF K - MICROMETEOROLOGY | ASSIGNMENT 4 | WIND RESOURCE AND SITE ASSESSMENT #################################

"""
What happens if the weibull shape parameter k is not constant at Sprogo, Nyborg and Korsor? This program calculates the
annual energy production for 10% lower k and shows the variation.
"""

# IMPORTS ##############################################################################################################

from toolkit import *
from environment import Environment
import matplotlib.pyplot as plt

# LOAD ENVIRONMENT #####################################################################################################

Env = Environment()

# CALCULATE AEP FOR 10% LOWER K ########################################################################################

# initialize result format
aep = np.zeros((3, 3))
aep_var = np.zeros((3, 3))

# specify analyzed years
# cases = ['all', 'max', 'min']
cases = ['all']

# loop over sites and cases
for j, case in enumerate(cases):
    print('\n' + case)

    # load weibull parameters and frequency at Sprogo (original k)
    A_org, k, f = load_akf('data/' + case + '/sprogo_akf.csv')

    # calculate AEP at sprogo with original k
    aep_sprogo = Env.AEP(A_org, k, f)
    aep[0, j] = aep_sprogo                  # store it
    aep_var[0, j] = aep_sprogo              # store it
    print(f'sprogo:\t{aep_sprogo:.3e}')     # print it

    # calculate geotrophic wind and friction velocity at Sprogo (original k)
    G, uf_org = Env.geostrophic_wind(A_org, k)

    # loop over each site
    for i, site in enumerate(Env.sites):

        # choose roughness length of site
        z0 = Env.z0_sites[i]

        # set up GDL for constant geostrophic wind at site
        def spec_GDL(uf): return Env.GDL(G, uf, z0)

        # solve for friction velocity at site
        uf = opt.fsolve(spec_GDL, uf_org)

        # log law
        u = np.multiply(np.divide(uf, Env.karman), np.log(Env.z_hub / z0))

        # weibull scale parameter with original k
        A = np.divide(u, gamma(1 + 1 / k))

        # weibull scale parameter with increased k
        A_var = np.divide(u, gamma(1 + 1 / (0.9 * k)))

        # corresponding annual energy production
        aep_abs = Env.AEP(A, k, f)
        aep_abs_var = Env.AEP(A, k * 0.9, f)
        aep[i+1, j] = aep_abs                               # store it
        aep_var[i+1, j] = aep_abs_var                       # store it
        print(site + f':\t{aep_abs:.3e}')                   # print it
        print(site + f':\t{aep_abs_var:.3e} with 90% k')    # print it

# print summary
print('\n\t\t\tNyborg\t\tKorsor')
print(f'original:\t{aep[1, 0]:.3e}\t{aep[2, 0]:.3e}')
print(f'90% k:\t\t{aep_var[1, 0]:.3e}\t{aep_var[2, 0]:.3e}')
print(f'rel. diff:\t{(aep_var[1, 0]/aep[1, 0]-1)*100:.2f}%\t\t{(aep_var[2, 0]/aep[2, 0]-1)*100:.2f}%')

# SCHEMATIC ############################################################################################################

k_list = np.linspace(min(k) * 0.9, 1.1 * max(k))
y_list = gamma(1 + 1 / k_list)
y_list = y_list / np.mean(y_list[(min(k) <= k_list) & (k_list <= max(k))])

plt.figure(0)
plt.plot(k_list, y_list)
plt.plot([min(k), min(k)], [min(y_list), max(y_list)], 'k--')
plt.plot([max(k), max(k)], [min(y_list), max(y_list)], 'k--')
plt.xlabel('Weibull shape parameter k')
plt.ylabel('c * Gamma(1 + 1/k)')
plt.grid(alpha=0.4)
plt.tight_layout()
plt.savefig('figures/k_var.pdf')
