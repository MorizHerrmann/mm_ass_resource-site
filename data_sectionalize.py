# SECTIONALIZE DATA - MICROMETEOROLOGY | ASSIGNMENT 4 | WIND RESOURCE AND SITE ASSESSMENT ##############################

"""
Divide data into a number of directional sections
param: input_file: whole data set
param: out_name: path/name of output file (without extension)
param: S: number of sections
return: (save the sectionalized data, for each a file)
"""

# IMPORTS ##############################################################################################################

import numpy as np

# INPUT ################################################################################################################

base = 'data/'
case = 'all/'
site = 'sprogo'
input_file = base + case + site + '.csv'
out_name = base + case + site + '_sec/' + site
S = 12      # number of sections

# SPECIFY SECTIONS #####################################################################################################

sect_size = 360 / S
sect_angles = [s * sect_size for s in range(S + 1)]

# LOAD DATA ############################################################################################################

data = np.loadtxt(input_file)
T = len(data)

# ORDER DATA ###########################################################################################################

# create a matrix of the maximum dimension (many entries will be 0)
sections_np = np.zeros((T, 7, S + 1))
for t in range(T):
    for s, sect_angle in enumerate(sect_angles):
        if (sect_angle - 15 < data[t, 6]) and (data[t, 6] <= sect_angle + 15):
            sections_np[t, :, s] = data[t, :]

# convert matrix to a list of arrays where zeros are removed
section_list = []
for s in range(S + 1):
    section_list.append(sections_np[sections_np[:, 0, s] != 0, :, s])

# combine 0° and 360° sections
section_list[0] = np.concatenate((section_list[0], section_list[-1]))
section_list[-1] = []

# save it to files
for sec in range(S):
    np.savetxt(out_name + f'_{sec:0>2}.csv', section_list[sec])
