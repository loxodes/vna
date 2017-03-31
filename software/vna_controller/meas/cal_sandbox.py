from pylab import *
import skrf as rf
from skrf.calibration import OnePort
import pdb
c = 3e8

# load in some uncalibrated s1p measurements
cal_load = rf.Network('load.s1p')
cal_open = rf.Network('open.s1p')
cal_short = rf.Network('short.s1p')
vat3 = rf.Network('vat3.s1p')
#vat3r = rf.Network('vat3r.s1p')
#vat3_load = rf.Network('anne_load.s1p')
anne = rf.Network('anne.s1p')
barrel = rf.Network('barrel.s1p')

# create cal kit
f = rf.frequency.Frequency(cal_load.f[0], cal_load.f[-1], len(cal_load.f), unit='hz')
media = rf.media.Freespace(f)
sdrkit_open = media.line(42.35, 'ps', z0 = 50) ** media.open() # 42.35
sdrkit_short = media.line(26.91, 'ps', z0 = 50) ** media.short() 
# TODO: add parallel 2fF capacitance to load?
sdrkit_load = rf.Network(f=cal_load.f/1e9, s=-.0126*np.ones(len(cal_load.f)), z0=50)

# read in actual vat3+
vat3_mini = rf.Network('VAT-3+___PLus25degC.s2p')
pdb.set_trace()
mini_open = rf.media.Freespace(vat3_mini.frequency).open()
vat3_mini = rf.connect(vat3_mini, 0, mini_open, 0)

#sdrkit_open.write_touchstone('ideal_open.s1p')
#sdrkit_short.write_touchstone('ideal_short.s1p')
#sdrkit_load.write_touchstone('ideal_load.s1p')

my_ideals = [sdrkit_short, sdrkit_open, sdrkit_load]
my_measured = [cal_short, cal_open, cal_load]

cal = rf.OnePort(ideals = my_ideals, measured = my_measured)
cal.run()

source_match = cal.coefs_3term_ntwks['source match']
directivity = cal.coefs_3term_ntwks['directivity']
reflection_tracking = cal.coefs_3term_ntwks['reflection tracking']

if False:
    source_match.plot_s_db()
    directivity.plot_s_db()
    reflection_tracking.plot_s_db()




barrel_cal = cal.apply_cal(barrel)

anne_cal = cal.apply_cal(anne)
vat3_cal  = cal.apply_cal(vat3)
#barrel_cal.plot_s_db()
#barrel.plot_s_db()

'''
cal_open.plot_s_db()
cal_short.plot_s_db()
cal_load.plot_s_db()
plt.legend(['source match', 'directivity', 'reflection tracking', 'open (uncal)', 'short (uncal)', 'load (uncal)'])
title('one port calibration error terms and cal kit measurements')
show()





barrel_cal.plot_s_smith()
anne_cal.plot_s_smith()

title('smith chart of SF-SF50+ SMA barrel and ANNE-50L+ termination\n2 GHz to 10 GHz')
show()
'''
vat3_cal.frequency.unit = 'MHz'
plot_f = rf.frequency.Frequency(vat3_cal.f[0], vat3_cal.f[140], 140, unit='Hz')
pdb.set_trace()
vat3_cal.interpolate(plot_f).plot_s_smith()
vat3_mini.interpolate(plot_f).plot_s_smith()
title('|S11| of VAT-3+')
show()



barrel_cal.plot_s_db()
title('|S11| of SF-SF50+ SMA barrel')
show()

anne_cal.plot_s_db()
title('|S11| of ANNE-50L+ termination')
show()

barrel_cal.write_touchstone('postcal')
pdb.set_trace()



