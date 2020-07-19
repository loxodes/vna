from litex.tools.litex_client import RemoteClient
import numpy as np
import matplotlib.pyplot as plt
import pdb

wb = RemoteClient()
wb.open()

ADC_SRAM_BASE = 0x20000000
nsamples = 1024
MAX_SAMPLES = 128 

def rev_bits(x):
    rev = 0
    while x:
        rev <<= 1
        rev += x & 1
        x >>= 1
    return rev

if __name__ == '__main__':

    remaining_samples = nsamples - MAX_SAMPLES
    s = np.uint32(wb.read(ADC_SRAM_BASE, min(MAX_SAMPLES, nsamples)))

    while remaining_samples > 0:
        nsamples_to_read = min(remaining_samples, MAX_SAMPLES)
        s = np.append(s, wb.read(ADC_SRAM_BASE + len(s) * 4, nsamples_to_read))
        remaining_samples -= nsamples_to_read

    
    s_a = np.uint16([s_i & 0xFFF for s_i in s])
    s_b = np.uint16([s_i >> 16 for s_i in s])

    wb.close()
    plt.subplot(2,1,1)
    plt.plot(s_a)
    plt.plot(s_b)
    plt.subplot(2,1,2)
    plt.magnitude_spectrum(s_a - 2048, Fs=25e6, scale = 'dB')
    plt.magnitude_spectrum(s_b - 2048, Fs=25e6, scale = 'dB')
    plt.show()


