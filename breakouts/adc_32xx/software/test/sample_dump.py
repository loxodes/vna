from litex.tools.litex_client import RemoteClient
import numpy as np
import matplotlib.pyplot as plt
import pdb

wb = RemoteClient()
wb.open()

ADC_SRAM_BASE = 0x30000000
nsamples = 512 

def rev_bits(x):
    rev = 0
    while x:
        rev <<= 1
        rev += x & 1
        x >>= 1
    return rev

if __name__ == '__main__':
    s = np.zeros(nsamples, dtype=np.uint16)

    for i in range(nsamples):
        s_i = int(wb.read(ADC_SRAM_BASE + i*4))
        #s_i_lsw = rev_bits(s_i & 0x3F)
        #s_i_msw = s_i >> 6
        #s_i = s_i_lsw + s_i_msw << 6
        s[i] = s_i
        

    wb.close()

    plt.plot(s)
    plt.show()

