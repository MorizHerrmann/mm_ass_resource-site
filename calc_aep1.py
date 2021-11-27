########################################################################################################################

"""This method extrapolates for each 10 minute average the geostrophic wind and extrapolates from that the wind at the
sites. The parameters A and B of the GDL are not suited for that, but for long term averages (at least a year).
So give calc_ape2.py a chance."""

# IMPORTS ##############################################################################################################

from toolkit import *
from environment import Environment

# LOAD ENVIRONMENT #####################################################################################################

Env = Environment()

# ALL YEARS WITH SPROGO ################################################################################################

aep_all_sprogo_abs = Env.AEP(*load_akf('data/all/sprog_afk.csv'))
aep_all_nyborg_abs = Env.AEP(*load_akf('data/all/nyborg_afk.csv'))
aep_all_korsor_abs = Env.AEP(*load_akf('data/all/korsor_afk.csv'))

aep_all_sprogo_rel = aep_all_sprogo_abs / aep_all_sprogo_abs
aep_all_nyborg_rel = aep_all_nyborg_abs / aep_all_sprogo_abs
aep_all_korsor_rel = aep_all_korsor_abs / aep_all_sprogo_abs

print('\t\t\tSprogo\t\tNyborg\t\tKorsor')
print(f'absolute:\t{aep_all_sprogo_abs:.3e}\t{aep_all_nyborg_abs:.3e}\t{aep_all_korsor_abs:.3e}')
print(f'relative:\t{aep_all_sprogo_rel:.3f}\t\t{aep_all_nyborg_rel:.3f}\t\t{aep_all_korsor_rel:.3f}')

# ALL / MAX / MIN WITHOUT SPROGO #######################################################################################

cases = ['all', 'max', 'min']

aep_abs = np.zeros((2, 3))
aep_rel = np.zeros((2, 3))

for i, site in enumerate(Env.sites):
    for j, case in enumerate(cases):
        akf = load_akf('data/' + case + '/' + site + '_afk.csv')
        aep = Env.AEP(*akf)
        aep_abs[i, j] = aep
        aep_rel[i, j] = aep_abs[i, j] / aep_abs[i, 0]

print(f'\nyears\tNyborg\t\t\t\tKorsor')
print(f'all\t\t{aep_abs[0, 0]:.3e}\t{aep_rel[0, 0]:.3f}\t{aep_abs[1, 0]:.3e}\t{aep_rel[1, 0]:.3f}')
print(f'min\t\t{aep_abs[0, 1]:.3e}\t{aep_rel[0, 1]:.3f}\t{aep_abs[1, 1]:.3e}\t{aep_rel[1, 1]:.3f}')
print(f'max\t\t{aep_abs[0, 2]:.3e}\t{aep_rel[0, 2]:.3f}\t{aep_abs[1, 2]:.3e}\t{aep_rel[1, 2]:.3f}')
