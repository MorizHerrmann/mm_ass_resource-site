
import numpy as np

# INPUT ################################################################################################################

input_file = 'data/all/korsor.csv'
out_name = 'data/all/korsor_sec/korsor'
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
