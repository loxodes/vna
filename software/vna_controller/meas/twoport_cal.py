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
    sdrkit_load = rf.Network(f=skrf_f.f, s=-.0126, z0=50, f_unit = 'Hz')
    sdrkit_thru = media.line(40.85, 'ps', z0 = 50)  # open - 1.35 ps
 
    sdrkit_open = rf.two_port_reflect(sdrkit_open, sdrkit_open)
    sdrkit_short = rf.two_port_reflect(sdrkit_short, sdrkit_short)
   
    ideals = [sdrkit_thru, sdrkit_short, sdrkit_open, sdrkit_load]
    return ideals



def plot_s2p_file(filename, cal_kit = None, show = True):
    s2p = rf.Network('short2.s2p')
    if cal_kit:
        s2p = cal_kit.apply_cal(s2p)

    s2p.plot_s_db()

    if show:
        plt.show()

    # so, Etr is zero - reverse transmission tracking



def plot_error_terms(cal_kit):
    #source_match = cal.coefs_8term_ntwks['source match']
    source_match.plot_s_db()
    directivity.plot_s_db()
    reflection_tracking.plot_s_db()

def main():
    # load cal measurements 
    cal_load1 = rf.Network('load1.s2p')
    cal_open1 = rf.Network('open1.s2p')
    cal_short1 = rf.Network('short1.s2p')

    cal_load2 = rf.Network('load2.s2p')
    cal_open2 = rf.Network('open2.s2p')
    cal_short2 = rf.Network('short2.s2p')

    cal_load = rf.two_port_reflect(cal_load1, cal_load2)
    cal_open = rf.two_port_reflect(cal_open1, cal_open2)
    cal_short = rf.two_port_reflect(cal_short1, cal_short2)
    cal_thru = rf.Network('thru.s2p')

    measured_cal = [cal_thru, cal_short, cal_open, cal_load]
    
    # create ideal cal networks, SLOT calibration
    ideal_cal = create_sdrkits_ideal(cal_thru.frequency)

    cal = rf.calibration.SOLT(ideals = ideal_cal, measured = measured_cal)
    cal.run()
    
    #plot_error_terms(cal)
    
    # plot some measurements 
    plot_s2p_file('barrel_anne.s2p', cal_kit = cal)


if __name__ == '__main__':
    main()


