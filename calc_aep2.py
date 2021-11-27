########################################################################################################################

"""This method computes the 'mean' geostrophic wind rose from the weibull parameters. From this the wind distribution
at the sites is extrapolated"""

# IMPORTS ##############################################################################################################

from toolkit import *
from environment import Environment

# LOAD ENVIRONMENT #####################################################################################################

Env = Environment()

########################################################################################################################

aep = np.zeros((3, 3))

# cases = ['all', 'max', 'min']
cases = ['all']

# loop over sites and cases
for j, case in enumerate(cases):
    print('\n' + case)

    A_org, k, f = load_akf('data/' + case + '/sprogo_akf.csv')
    aep_sprogo = Env.AEP(A_org, k, f)
    aep[0, j] = aep_sprogo

    print(f'sprogo:\t{aep_sprogo:.3e}')

    for i, site in enumerate(Env.sites):

        z0 = Env.z0_sites[i]
        G, uf_org = Env.geostrophic_wind(A_org, k)

        def spec_GDL(uf): return Env.GDL(G, uf, z0)

        uf = opt.fsolve(spec_GDL, uf_org)

        # log law
        u = np.multiply(np.divide(uf, Env.karman), np.log(Env.z_hub / z0))
        print(u)

        # weibull constants
        A = np.divide(u, gamma(1 + 1 / k))

        aep_abs = Env.AEP(A, k, f)

        aep[i+1, j] = aep_abs

        print(site + f':\t{aep_abs:.5e}')

print('\n\t\t\tSprogo\t\tNyborg\t\tKorsor')
print(f'absolute:\t{aep[0, 0]:.3e}\t{aep[1, 0]:.3e}\t{aep[2, 0]:.3e}')
print(f'relative:\t{aep[0, 0] / aep[0, 0]:.3f}\t\t{aep[1, 0] / aep[0, 0]:.3f}\t\t{aep[2, 0] / aep[0, 0]:.3f}')