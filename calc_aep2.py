# CALCLATE ANNUAL ENERGY PRODUCTION - MICROMETEOROLOGY | ASSIGNMENT 4 | WIND RESOURCE AND SITE ASSESSMENT ##############

"""
This method computes the 'mean' geostrophic wind rose from the weibull parameters. From this the wind distribution
at the sites and the AEP is extrapolated
"""

# IMPORTS ##############################################################################################################

from toolkit import *
from environment import Environment

# LOAD ENVIRONMENT #####################################################################################################

Env = Environment()

########################################################################################################################

# initialize AEP for [sprogo, nyborg, korsor] x [all, max, min]
aep = np.zeros((3, 3))

# all years, most windiest year, least windiest year
cases = ['all', 'max', 'min']
# cases = ['all']

# loop over sites and cases
for j, case in enumerate(cases):
    print('\n' + case)

    # load weibull parameters and frequency of occurrance at Sprogo
    A_org, k, f = load_akf('data/' + case + '/sprogo_akf.csv')

    # calculate AEP at Sprogo
    aep_sprogo = Env.AEP(A_org, k, f)
    aep[0, j] = aep_sprogo                  # store it
    print(f'sprogo:\t{aep_sprogo:.3e}')     # print it

    # calculate geostrophic wind (constant) and friction velocity at Sprogo
    G, uf_org = Env.geostrophic_wind(A_org, k)

    for i, site in enumerate(Env.sites):

        # choose roughness length of site
        z0 = Env.z0_sites[i]

        # set up GDL for constant geostrophic wind with roughness length at site
        def spec_GDL(uf): return Env.GDL(G, uf, z0)

        # solve it for the friction velocity at site
        uf = opt.fsolve(spec_GDL, uf_org)

        # log law -> mean wind
        u = np.multiply(np.divide(uf, Env.karman), np.log(Env.z_hub / z0))

        # weibull scale parameter (assumption: constant scale parameter k)
        A = np.divide(u, gamma(1 + 1 / k))

        # calculate AEP
        aep_abs = Env.AEP(A, k, f)
        aep[i+1, j] = aep_abs               # store it
        print(site + f':\t{aep_abs:.5e}')   # print it

# print summary
print('\n\t\t\tSprogo\t\tNyborg\t\tKorsor')
print(f'absolute:\t{aep[0, 0]:.3e}\t{aep[1, 0]:.3e}\t{aep[2, 0]:.3e}')
print(f'relative:\t{aep[0, 0] / aep[0, 0]:.3f}\t\t{aep[1, 0] / aep[0, 0]:.3f}\t\t{aep[2, 0] / aep[0, 0]:.3f}')
