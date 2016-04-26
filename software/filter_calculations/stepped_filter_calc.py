# worksheet to calculate stepped impedance microstrip filters
# references: pozar, microwave engineering, 4th edition
# currently configured to replicate example 8.6, page 425
# line length calculation in degrees works,
# physical line length calculations need improvement..
# TODO: automatically generate openEMS simulation?

import numpy as np
import pdb

fcutoff = 2.5e9 # hz
z0 = 50 # ohms
c = 3e8
er = 4.2 #3.66$a
d = .158e-2 #mil_to_meter(6.7) # meters substrate thickness

fstop = 4e9
stopatt = 20 # dB

tand = .02
#ch = mil_to_meter(.5) # mil copper thickness

fnorm = fstop / fcutoff - 1

zmin = 20 # 
zmax = 120 # 80

# calculate effective dielectric constant of microstrip
def e_effective(er, w, d):
    ee = .5 *((er + 1) + (er - 1) / np.sqrt(1 + 12 * d / w))
    print('e effective: {}'.format(ee))
    return ee

# should be 11.3 mm
# pozar (3.197)
def calc_w(z0, d, er):
    A = (z0 / 60) * np.sqrt(.5 * (er + 1)) + ((er - 1) / (er + 1)) * (.23 + .11 / er)
    B = 377 * np.pi / (2 * z0 * np.sqrt(er))

    w1 = d * (8 * np.exp(A)) / (np.exp(2 * A) - 2)
    w2 = d * (2 / np.pi) * (B - 1 - np.log(2 * B - 1) + ((er - 1) / (2 * er)) * (np.log(B - 1) + .39 - .61 / er))
    
    if w1 / d < 2 and w1 > 0:
        print('w: {}'.format(w1 * 1000))
        return w1
    else:
        print('w: {}'.format(w2 * 1000))
        return w2

# calculate the physical length of a microstrip line
# given impedance and dielectric constant
def calc_len(z0, d, er, deg):
    w = calc_w(z0, d, er) 
    ee = e_effective(er, w, d)
    # calculate the wavelength at the effective dielectric constant
    l = (c / fcutoff) / np.sqrt(ee)
    
    # return length in mm 
    return 1000 * l * deg / (2 * np.pi)

# convert mils (thousands of inch) to meters
def mil_to_meter(h):
    return ((h / 1000.) * 2.54) / 100.

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

if __name__ == '__main__':
    for segment in range(N):
        bl = 0
        l = 0
        if segment % 2 == 0:
            bl = N_maxflat[N][segment] * zmin / z0
            l = calc_len(zmin, d, er, bl)
        else:
            bl = N_maxflat[N][segment] * z0 / zmax
            l = calc_len(zmax, d, er, bl)
       
        bl_deg = bl * 180.0 / np.pi


        print('{}, \t norm: {} \t bl (deg): {} \t len {} mm'.format(segment, N_maxflat[N][segment], bl_deg, l))

