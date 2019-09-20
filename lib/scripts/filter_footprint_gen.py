# uses kicadfpwriter from https://github.com/dlharmon/pyopenems
import kicadfpwriter

def gen_stepped_lpf(name, pad_w, seg_widths, seg_lengths):
    # wh - width of high impedance segment
    # wl - width of low impedance segment
    # add pad
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
    # via_s, via to via spacing along a row
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
    # TODO: create vias..


    fp = g.finish()
    with open(name+".kicad_mod", "w") as f:
        f.write(fp)

    
def main():
    wh = .5
    wl = 3
    wz = 1

    lpf_8ghz_l = [1,2,1]
    lpf_8ghz_w = [wl, wz, wl]
    gen_stepped_lpf('stepped_lpf_8ghz_ro4350_10mil', wz, lpf_8ghz_w, lpf_8ghz_l)

    lpf_20ghz_l = [1,2,1]
    lpf_20ghz_w = [wl, wz, wl]
    gen_stepped_lpf('stepped_lpf_20ghz_ro4350_10mil', wz, lpf_20ghz_w, lpf_20ghz_l)


    gen_siw_bpf('band_x2_siw_ro4350_10mil', wz, 5.75, 20, 3, 5, 5.25, .254, 1)


if __name__ == '__main__':
    main()
