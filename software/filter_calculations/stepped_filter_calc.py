# worksheep to calculate stepped impedence microstrip filters
# references: pozar, microwave engineering, 4th edition
# currently configured to replicate example 8.6, page 425
# line length calculation in degrees works,
# physical line length calculations need improvement..

import numpy as np
import pdb

fcutoff = 2.5e9 # hz
z0 = 50 # ohms
c = 3e8
er = 4.2 #3.66

l = (c / fcutoff) / np.sqrt(er)

fstop = 4e9
stopatt = 20 # dB

d = .158e-2 #mil_to_meter(6.7) # meters substrate thickness
tand = .02
#ch = mil_to_meter(.5) # mil copper thickness

fnorm = fstop / fcutoff - 1

zmin = 20 # 
zmax = 120 # 80


def mil_to_meter(h):
    return ((h / 1000.) * 2.54) / 100.

def rad_to_len(d):
    return 1000 * l * d / (2 * np.pi)

# table 8.3 from pozar, page 404
N_maxflat = \
   [[1.0000], \
    [2.0000,1.0000], \
    [1.4142,1.4142,1.0000],\
    [1.0000,2.0000,1.0000,1.0000],\
    [0.7654,1.8478,1.8478,0.7654,1.0000],\
    [0.6180,1.6180,2.0000,1.6180,0.6180,1.0000],\
    [0.5176,1.4142,1.9318,1.9318,1.4142,0.5176,1.0000],\
    [0.4450,1.2470,1.8019,2.0000,1.8019,1.2470,0.4450,1.0000],\
    [0.3902,1.1111,1.6629,1.9615,1.9615,1.6629,1.1111,0.3902,1.0000],\
    [0.3473,1.0000,1.5321,1.8794,2.0000,1.8794,1.5321,1.0000,0.3473,1.0000],\
    [0.3129,0.9080,1.4142,1.7820,1.9754,1.9754,1.7820,1.4142,0.9080,0.3129,1.0000]]

N = 6 # TODO: determine filter order

for segment in range(N):
    bl = 0
    if segment % 2 == 0:
        bl = N_maxflat[N][segment] * zmin / z0
    else:
        bl = N_maxflat[N][segment] * z0 / zmax
    
    bl_deg = bl * 180.0 / np.pi
    print('{}, \t norm: {} \t bl (deg): {} \t len {} mm'.format(segment, N_maxflat[N][segment], bl_deg, rad_to_len(bl)))

# convert to length at 2.5 GHz
