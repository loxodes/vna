# undertested script to calculate stepped impedance microstrip filters and generate kicad microwave shape files
# jtklein@alaska.edu, http://github.com/loxodes
# mit license

# references: pozar, microwave engineering, 4th edition

# to add to a filter to a KiCad layout, import the shape description .poly file using the microwave toolbar
# this only works for me using the default KiCad renderer (as in not OpenGL or cairo..)

# TODO: automatically generate openEMS simulation? (see pyopenems)
# TODO: plot estimated filter frequency response of filter? generate qucs schematics?

import numpy as np
import pdb

# generate a polygon shape file for the kicad microwave toolbar
def generate_stepped_filter_kicad_poly(l_seg, w_seg):
    total_length = sum(l_seg)
    max_width = max(w_seg)

    # normalize widths and lengths
    l_seg = np.array(l_seg) / total_length
    w_seg = np.array(w_seg) / max_width

    poly_points = []

    nsegs = len(l_seg)
    
    # add initial point
    poly_points.append((0, w_seg[0]/2))
   
    # step foward 
    for segment in range(nsegs - 1):
        x_coord = 0 + sum(l_seg[:segment + 1])
        y_coord = w_seg[segment] / 2
        poly_points.append((x_coord, y_coord))

        y_coord = w_seg[segment+1] / 2
        poly_points.append((x_coord, y_coord))

    # add end points
    x_coord = sum(l_seg)
    y_coord = w_seg[-1] / 2
    poly_points.append((x_coord, y_coord))
    y_coord = -w_seg[-1] / 2
    poly_points.append((x_coord, y_coord))

    # step backward through segments, add bottom line of points
    for segment in range(nsegs - 1, 0, -1):
        x_coord = 0 + sum(l_seg[:segment])
        y_coord = -w_seg[segment] / 2
        poly_points.append((x_coord, y_coord))

        y_coord = -w_seg[segment-1] / 2
        poly_points.append((x_coord, y_coord))
    
    # add final point to close the polygon
    poly_points.append((0, -w_seg[0]/2))
    poly_points.append((0, w_seg[0]/2))
    
    # create polygon file
    poly_file = 'Unit=MM\n'
    poly_file += 'XScale={}\n'.format(total_length)
    poly_file += 'YScale={}\n'.format(max_width)
    poly_file += '\n$COORD\n'
    for point in poly_points:
        poly_file += '{} {}\n'.format(point[0], point[1])
    poly_file += '\n$ENDCOORD\n'

    return poly_file

# calculate effective dielectric constant of microstrip
def e_effective(er, w, d):
    ee = .5 *((er + 1) + (er - 1) / np.sqrt(1 + 12 * d / w))
    return ee

# numerical approximation to calculate microstrip width
# TODO: fix this.. not matching simulations at high impedances
def calc_w(z0, d, er):
    A = (z0 / 60) * np.sqrt(.5 * (er + 1)) + ((er - 1) / (er + 1)) * (.23 + .11 / er)
    B = 377 * np.pi / (2 * z0 * np.sqrt(er))

   # w1 = d * (8 * np.exp(A)) / (np.exp(2 * A) - 2)
    w2 = d * (2 / np.pi) * (B - 1 - np.log(2 * B - 1) + ((er - 1) / (2 * er)) * (np.log(B - 1) + .39 - .61 / er))
    
   # print('w1: {}, w2: {}, d: {}, er: {}, z0: {}'.format(w1, w2, d, er, z0))
   # if A >= 1.52:
   #     return w1
   # else:
    return w2
    # return width in meters

# calculate the physical length of a microstrip line
# given impedance and dielectric constant
def calc_len(z0, d, er, deg):
    w = calc_w(z0, d, er) 
    ee = e_effective(er, w, d)
    # calculate the wavelength at the effective dielectric constant
    l = (c / fcutoff) / np.sqrt(ee)
    
    # return length in meters
    return l * deg / (2 * np.pi)

# convert mils (thousands of inch) to meters
def mil_to_meter(h):
    return ((h / 1000.) * 2.54) / 100.

# convert mm to thousands of an inch..
def m_to_mil(w):
    return ((w * 100) / 2.54) * 1000

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


# example usage, create a 2.5 GHz cutoff filter
if __name__ == '__main__':
    fcutoff = 2.5e9 # hz
    fstop = 4e9
    N = 6 # filter order, TODO: determine filter order automatically using stopband attenuation
    filename = 'stepped_filter.poly'

    z0 = 50 # ohms
    c = 3e8

    # stackup information, set for oshpark fr408 4-layer
    er = 3.66
    d = mil_to_meter(6.7) #.158e-2 #mil_to_meter(6.7) # meters substrate thickness
    tand = .0125 # fr408
    zmin = 15 # TODO: determine these from minimum and maximum trace widths
    zmax = 80 # 

    fnorm = fstop / fcutoff - 1
    l_seg = np.zeros(N)
    w_seg = np.zeros(N)
    print('50 ohm width: {}'.format(1000 * (calc_w(50, d, er))))
    
    # calculate filter segment sizes
    for segment in range(N):
        bl = 0
        l = 0
        w = 0
        if segment % 2 == 0:
            bl = N_maxflat[N][segment] * zmin / z0
            l = calc_len(zmin, d, er, bl)
            w = calc_w(zmin, d, er) 
        else:
            bl = N_maxflat[N][segment] * z0 / zmax
            l = calc_len(zmax, d, er, bl)
            w = calc_w(zmax, d, er) 
       
        bl_deg = bl * 180.0 / np.pi
        l_seg[segment] = l * 1000
        w_seg[segment] = w * 1000

        print('{}, \t norm: {} \t bl (deg): {} \t len {} mm \t w {} mm'.format(segment, N_maxflat[N][segment], bl_deg, l_seg[segment], w_seg[segment]))
    
    total_length = sum(l_seg)
    max_width = max(w_seg)

    print('total length: {} mm'.format(total_length))
    print('microstrip lengths: {}'.format(l_seg))
    print('microstrip widths: {}'.format(w_seg))

    # generate kicad polygon
    poly_str = generate_stepped_filter_kicad_poly(l_seg, w_seg)
    
    with open(filename, 'w') as f:
        f.write(poly_str)
