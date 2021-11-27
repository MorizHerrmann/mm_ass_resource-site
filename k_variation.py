########################################################################################################################

"""This method computes the 'mean' geostrophic wind rose from the weibull parameters. From this the wind distribution
at the sites is extrapolated"""

# IMPORTS ##############################################################################################################

from toolkit import *
from environment import Environment
import matplotlib.pyplot as plt

# LOAD ENVIRONMENT #####################################################################################################

Env = Environment()

########################################################################################################################

aep = np.zeros((3, 3))
aep_var = np.zeros((3, 3))

# cases = ['all', 'max', 'min']
cases = ['all']

# loop over sites and cases
for j, case in enumerate(cases):
    print('\n' + case)

    A_org, k, f = load_akf('data/' + case + '/sprog_afk.csv')
    aep_sprogo = Env.AEP(A_org, k, f)
    aep[0, j] = aep_sprogo
    aep_var[0, j] = aep_sprogo

    print(f'sprogo:\t{aep_sprogo:.3e}')

    for i, site in enumerate(Env.sites):

        z0 = Env.z0_sites[i]
        G, uf_org = Env.geostrophic_wind(A_org, k)

        def spec_GDL(uf): return Env.GDL(G, uf, z0)

        uf = opt.fsolve(spec_GDL, uf_org)

        # log law
        u = np.multiply(np.divide(uf, Env.karman), np.log(Env.z_hub / z0))

        # weibull constants
        A = np.divide(u, gamma(1 + 1 / k))
        A_var = np.divide(u, gamma(1 + 1 / (0.9 * k)))

        aep_abs = Env.AEP(A, k, f)
        aep_abs_var = Env.AEP(A, k * 0.9, f)

        aep[i+1, j] = aep_abs
        aep_var[i+1, j] = aep_abs_var

        print(site + f':\t{aep_abs:.3e}')
        print(site + f':\t{aep_abs_var:.3e} with 90% k')

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
