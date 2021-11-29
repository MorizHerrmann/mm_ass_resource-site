# CLEAN DATA - MICROMETEOROLOGY | ASSIGNMENT 4 | WIND RESOURCE AND SITE ASSESSMENT #####################################

"""
Cleans data: expand timecode and remove invalid measurements (=999 or = 99.99)
param: org_data: original data file
param: out_name: path/name of output file
return: (save cleaned data = [year, month, day, hour, minute, wind speed, direction])
"""

# IMPORTS ##############################################################################################################

import numpy as np

# INPUTS ###############################################################################################################

org_data = 'data/sprogo.tsv'
out_name = 'data/sprogo.csv'

# LOAD DATA ############################################################################################################

data = np.loadtxt(org_data)
T = len(data)

########################################################################################################################

# new data format
datax = np.zeros((T, 7))

# transfer wind speed
datax[:, 5] = data[:, 1]

# expand time code
for t in range(T):
    tcode = data[t, 0]
    datax[t, 0] = int(round(tcode/1e8))                  # year
    datax[t, 1] = int(round(np.mod(tcode, 1e8) / 1e6))   # month
    datax[t, 2] = int(round(np.mod(tcode, 1e6) / 1e4))   # day
    datax[t, 3] = int(round(np.mod(tcode, 1e4) / 1e2))   # hour
    datax[t, 4] = int(np.mod(tcode, 1e2))                # minute

# combine directions
dir1 = data[:, 2]
dir2 = data[:, 3]

dir0 = np.zeros((T,))

for t in range(T):
    if (dir1[t] == 999) and (dir2[t] == 999):
        dir0[t] = 999
    elif (dir1[t] == 999) and (dir2[t] != 999):
        dir0[t] = dir2[t]
    elif (dir1[t] != 999) and (dir2[t] == 999):
        dir0[t] = dir1[t]
    else:
        dir0[t] = dir1[t]

datax[:, 6] = dir0

# remove error values
clean = datax
clean = clean[clean[:, 5] != 999, :]
clean = clean[clean[:, 5] != 99.99, :]
clean = clean[clean[:, 6] != 999, :]

# save
np.savetxt(out_name, clean)
