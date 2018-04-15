files = ['thru_0201_10pf_accup.s2p','thru_0402_10pf_accup.s2p','thru_barrel.s2p','thru_tee_BLM15GG471_10pf_220nf.s2p','thru_thru.s2p']

from pylab import *
from skrf import Network

for f in files:
    net = Network(f)
    net.plot_s_db()

plt.show()
