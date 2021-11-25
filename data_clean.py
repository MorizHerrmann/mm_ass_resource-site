
import numpy as np

org_data = 'sprog.tsv'

data = np.loadtxt(org_data)

# new data format
T = len(data)
datax = np.zeros((T, 7))
datax[:, 5] = data[:, 1]

# expand time code
for t in range(T):
    tcode = data[t, 0]
    datax[t, 0] = round(tcode/1e8)                  # year
    datax[t, 1] = round(np.mod(tcode, 1e8) / 1e6)   # month
    datax[t, 2] = round(np.mod(tcode, 1e6) / 1e4)   # day
    datax[t, 3] = round(np.mod(tcode, 1e4) / 1e2)   # hour
    datax[t, 4] = np.mod(tcode, 1e2)                # minute

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

np.savetxt('sprog_clean.csv', clean)
