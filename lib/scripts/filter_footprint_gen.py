# uses kicadfpwriter from https://github.com/dlharmon/pyopenems
import kicadfpwriter
import numpy as np

def gen_stepped_lpf(name, pad_w, seg_widths, seg_lengths):
    g = kicadfpwriter.Generator(name)

    x = 0
    g.add_pad("1",pad_w/2.,0,pad_w,pad_w)

    for i in range(len(seg_lengths)):
        seg_points = []
        sw = seg_widths[i]
        sl = seg_lengths[i]

        seg_points.append([x,sw/2.])
        seg_points.append([x,-sw/2.])
        seg_points.append([x+sl,-sw/2.])
        seg_points.append([x+sl,sw/2.])
        seg_points.append([x,sw/2.])

        g.add_polygon(seg_points)

        x += sl
    
    g.add_pad("2",x-pad_w/2.,0,pad_w,pad_w)

    fp = g.finish()
    with open(name+".kicad_mod", "w") as f:
        f.write(fp)


def gen_siw_bpf(name, pad_w, siw_w, siw_l, taper_w, taper_l, via_w, via_d, via_s): 
    # pad_w, pad width (w for z0)
    # siw_w, width of the siw filter ground plane
    # siw_l, length of the siw section
    # taper_w, taper matching segment from pad_w to taper_w
    # taper_l, length of linear taper
    # via_w, center to center distance between via rows
    # via_d, via diameter
    # via_s, via to via spacing along a row (will be rounded down for integer number of vias along siw_l)
    g = kicadfpwriter.Generator(name)
    
    # create pad 1
    g.add_pad("1",pad_w/2.,0,pad_w,pad_w)

    x = 0
    # create taper1
    taper1_points = []
    taper1_points.append([x,pad_w/2.])
    taper1_points.append([x+taper_l,taper_w/2.])
    taper1_points.append([x+taper_l,-taper_w/2.])
    taper1_points.append([x,-pad_w/2.])
    taper1_points.append([x,pad_w/2.])
    g.add_polygon(taper1_points)
    x += taper_l

    # create siw 
    siw_points = []
    siw_points.append([x,siw_w/2.])
    siw_points.append([x+siw_l,siw_w/2.])
    siw_points.append([x+siw_l,-siw_w/2.])
    siw_points.append([x,-siw_w/2.])
    siw_points.append([x,siw_w/2.])
    g.add_polygon(siw_points)
    x += siw_l

    # create taper2
    taper2_points = []
    taper2_points.append([x,taper_w/2.])
    taper2_points.append([x+taper_l,pad_w/2.])
    taper2_points.append([x+taper_l,-pad_w/2.])
    taper2_points.append([x,-taper_w/2.])
    taper2_points.append([x,taper_w/2.])
    g.add_polygon(taper2_points)
    x += taper_l

    # create pad2 
    g.add_pad("2",x-pad_w/2.,0,pad_w,pad_w)

    # create ground vias
    n_vias = np.ceil(siw_l / via_s)
    via_locations = np.linspace(taper_l, taper_l + siw_l, n_vias)

    for via_x in via_locations:
        g.add_pad("3", via_x, via_w/2., shape="cir", diameter=via_d+.254, drill=via_d)
        g.add_pad("3", via_x, -via_w/2., shape="cir", diameter=via_d+.254, drill=via_d)


    fp = g.finish()
    with open(name+".kicad_mod", "w") as f:
        f.write(fp)

    
def main():
    wh = .18
    wl = 1.964
    wz = .54

    lpf_8ghz_l = np.array([105, 73.2, 144.49, 73.2, 105])*.0254
    lpf_8ghz_w = [wl, wh, wl, wh, wl]
    gen_stepped_lpf('stepped_lpf_8ghz_ro4350_10mil', wz, lpf_8ghz_w, lpf_8ghz_l)

    lpf_20ghz_l = np.array([32, 30, 46, 30.7, 46, 30.7, 46, 30, 32])*.0254
    lpf_20ghz_w = [wl, wh, wl, wh, wl, wh, wl, wh, wl]
    gen_stepped_lpf('stepped_lpf_20ghz_ro4350_10mil', wz, lpf_20ghz_w, lpf_20ghz_l)


    gen_siw_bpf('band_x2_siw_ro4350_10mil', wz, 5.75, 20.0, 2.5, 5.0, 5.25, .254, 1.0)
    
    # fr408, oshpark
    wz = .41
    wh = 6.78 * .0254
    wl = 62.4 * .0254

    lpf_8ghz_l = np.array([82.1,80.4,116.7,80.4,82.1])*.0254
    lpf_8ghz_w = [wl, wh, wl, wh, wl]
    gen_stepped_lpf('stepped_lpf_8ghz_fr408', wz, lpf_8ghz_w, lpf_8ghz_l)

    wh = 5.25 * .0254
    wl = 77.8 * .0254
    lpf_20ghz_l = np.array([26,23.5,38.2,24.3,38.2,23.5,26])*.0254
    lpf_20ghz_w = [wl, wh, wl, wh, wl, wh, wl]
    gen_stepped_lpf('stepped_lpf_20ghz_fr408', wz, lpf_20ghz_w, lpf_20ghz_l)
   
    gen_siw_bpf('band_x2_siw_fr408_6p7mil', wz, 6.25, 20.0, 2.5, 5.0, 5.75, .254, 1.0)


    #gen_siw_bpf('siw_6ghz_fr408_6p7mil', wz, 6.25, 20.0, 2.5, 5.0, 5.75, .254, 1.0)

if __name__ == '__main__':
    main()
