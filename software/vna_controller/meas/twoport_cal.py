from pylab import *
import skrf as rf
import pdb
c = 3e8


def create_sdrkits_ideal(skrf_f):
    # create ideal cal kit
     # load - 70 pH in series with 48.6 ohms
     # short - 8.073 mm w/ .00873 dB attenuation 
     # open - 12.7 mm w/ .0127 dB attenuation

    media = rf.media.Freespace(skrf_f)
    sdrkit_open = media.line(42.35, 'ps', z0 = 50) ** media.open() # 42.35
    sdrkit_short = media.line(26.91, 'ps', z0 = 50) ** media.short() 
    # TODO: add parallel 2fF capacitance to load?
    pdb.set_trace()
    sdrkit_load_p1 = rf.Network(f=skrf_f.f, s=(np.ones(len(skrf_f)) * -.0126 + 1j * 2.525e-12 * skrf_f.f), z0=50, f_unit = 'Hz')
    sdrkit_load_p2 = rf.Network(f=skrf_f.f, s=(np.ones(len(skrf_f)) * -.005 + 1j * 2.525e-12 * skrf_f.f), z0=50, f_unit = 'Hz')
    sdrkit_thru = media.line(41.00, 'ps', z0 = 50)  # open - 1.35 ps
 
    sdrkit_open = rf.two_port_reflect(sdrkit_open, sdrkit_open)
    sdrkit_short = rf.two_port_reflect(sdrkit_short, sdrkit_short)
    sdrkit_load = rf.two_port_reflect(sdrkit_load_p1, sdrkit_load_p2)
   
    ideals = [sdrkit_short, sdrkit_open, sdrkit_load, sdrkit_thru]
    return ideals

def create_kirkby(skrf_f):
    media = rf.media.Freespace(skrf_f)

    def calc_c(f, c):
        # see http://literature.cdn.keysight.com/litweb/pdf/5989-4840EN.pdf 
        sc = [1e-15, 1e-27, 1e-36, 1e-45]
        c = sc[0] * c[0] + sc[1] * c[1] * f + sc[2] * c[2] * (f**2) + sc[3] * c[3] * (f**3)
        return c

    open_female_c_18 = [110.012, 24.998, 169.988, -.001] # offset loss, .7 G ohms/s
    open_male_c_18 = [66.866, 25.142, 36.261, .06592]

    open_c = calc_c(skrf_f.f, open_female_c_18)
    open_z = 1.0 / (1j * 2 * np.pi * skrf_f.f * open_c)
    open_s = (open_z - 50) / (50 + open_z)

    # female short, delay 0 ps, 2.2 G Ohms/s
    # female thru, 80.084 ps, 3 G Ohms/s

    pdb.set_trace()
    kirkby_open = rf.Network(f=skrf_f.f, s=open_s, z0 = 50, f_unit = 'Hz')
    kirkby_short = media.short()
    kirkby_load = rf.Network(f=skrf_f.f, s=np.zeros(len(skrf_f)), z0=50, f_unit = 'Hz')
    kirkby_thru = media.line(80.084, 'ps', z0 = 50) # todo: add offset loss, 3 G Ohms/s?

    kirkby_open = rf.two_port_reflect(kirkby_open)
    kirkby_short = rf.two_port_reflect(kirkby_short)
    kirkby_load = rf.two_port_reflect(kirkby_load)


    ideals = [kirkby_short, kirkby_open, kirkby_load, kirkby_thru]
    return ideals
    


def plot_s2p_file(filename, cal_kit = None, show = True):
    s2p = rf.Network(filename)
    if cal_kit:
        s2p = cal_kit.apply_cal(s2p)

    s2p.plot_s_db()

    if show:
        plt.show()



def plot_error_terms(cal_kit):
    #source_match = cal.coefs_8term_ntwks['source match']
    source_match.plot_s_db()
    directivity.plot_s_db()
    reflection_tracking.plot_s_db()

def main():
    # load cal measurements 
    cal_load = rf.Network('../cal_twoport/load.s2p')
    cal_open = rf.Network('../cal_twoport/open.s2p')
    cal_short = rf.Network('../cal_twoport/short.s2p')
    cal_thru = rf.Network('../cal_twoport/thru.s2p')

    cal_iso = rf.Network('../cal_twoport/isolation.s2p')

    cal_sw_fwd = rf.Network('../cal_twoport/sw_fwd.s1p')
    cal_sw_rev = rf.Network('../cal_twoport/sw_rev.s1p')
 

    measured_cal = [cal_short, cal_open, cal_load, cal_thru]
    
    # create ideal cal networks, SLOT calibration
    ideal_cal = create_kirkby(cal_thru.frequency)#create_sdrkits_ideal(cal_thru.frequency)

    cal = rf.TwelveTerm(ideals = ideal_cal, measured = measured_cal, n_thrus = 1, isolation = cal_iso)

    #cal = rf.EightTerm(ideals = ideal_cal, measured = measured_cal, switch_terms = (cal_sw_rev, cal_sw_fwd))

    cal.run()

    barrel = rf.Network('8493A_thru.s2p')
    #e_lpf = rf.Network('/home/kleinjt/vna_presentation/data/e5701c/RAINBOW_LPF_ANNE.S1P')

    barrel_cal = cal.apply_cal(barrel)
    barrel_cal.plot_s_db()
    #e_lpf.plot_s_db()

    grid(True)
    title("$|S|$ of microstrip test board")

    show()

    title("$S$ of HMC311 test board from 2 GHz to 13 GHz") 
    barrel_cal.plot_s_smith()

    show()
    pdb.set_trace()

if __name__ == '__main__':
    main()


