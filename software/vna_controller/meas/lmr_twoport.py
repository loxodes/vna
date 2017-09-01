from pylab import *
import skrf as rf
import pdb
c = 3e8


def create_sdrkits_ideal(skrf_f):
    # create ideal cal kit
    media = rf.media.Freespace(skrf_f)
    sdrkit_open = media.line(42.35, 'ps', z0 = 50) ** media.open() # 42.35
    sdrkit_short = media.line(26.91, 'ps', z0 = 50) ** media.short() 
    # TODO: add parallel 2fF capacitance to load?
    sdrkit_load = rf.Network(f=skrf_f.f, s=(np.ones(len(skrf_f)) * -.0126), z0=50, f_unit = 'Hz')
    sdrkit_thru = media.line(41.00, 'ps', z0 = 50)  # open - 1.35 ps
 
    sdrkit_open = rf.two_port_reflect(sdrkit_open, sdrkit_open)
    sdrkit_short = rf.two_port_reflect(sdrkit_short, sdrkit_short)
    sdrkit_load = rf.two_port_reflect(sdrkit_load, sdrkit_load)
   
    ideals = [sdrkit_short, sdrkit_open, sdrkit_load, sdrkit_thru]
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
    lmr_mm = rf.Network('../cal_twoport/match_match.s2p')
    lmr_mr = rf.Network('../cal_twoport/match_reflect.s2p')
    lmr_rm = rf.Network('../cal_twoport/reflect_match.s2p')
    lmr_rr = rf.Network('../cal_twoport/reflect_reflect.s2p')

    lmr_thru = rf.Network('../cal_twoport/thru.s2p')

    cal_sw_fwd = rf.Network('../cal_twoport/sw_fwd.s1p')
    cal_sw_rev = rf.Network('../cal_twoport/sw_rev.s1p')
 
    measured_cal = [lmr_thru, lmr_mm, lmr_rr, lmr_rm, lmr_mr]
    
    media = rf.media.Freespace(lmr_thru.frequency)
    sdrkit_thru = media.line(41.00, 'ps', z0 = 50)  # open - 1.35 ps


    cal = rf.calibration.LMR16(measured_cal, [sdrkit_thru], ideal_is_reflect = False, switch_terms = (cal_sw_fwd, cal_sw_rev))
    cal.run()

    barrel = rf.Network('lmr_barrelvat3.s2p')
    barrel_cal = cal.apply_cal(barrel)
    barrel_cal.plot_s_db()

    grid(True)
    title("$|S|$ of Omni-Spectra 20600-10, 10 dB attenuator") 

    show()
    barrel_cal.plot_s_smith()

    show()
    pdb.set_trace()

if __name__ == '__main__':
    main()


