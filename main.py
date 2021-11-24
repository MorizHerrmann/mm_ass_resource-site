# IMPORTS ##############################################################################################################

import numpy as np
import matplotlib.pyplot as plt

# INPUTS ###############################################################################################################

z0_water = 0.02e-2  # [m] roughness length over water
z0_land = 3e-2      # [m] roughness length over lande
z_hub = 110         # [m] hub height

T = 365.25 * 24     # [hours]
u_rated = 12.5      # [m/s] rated wind speed
u_cutout = 25       # [m/s] cut out wind speed
p_rated = 6e6       # [W] rated power

# FUNCTIONS ############################################################################################################
