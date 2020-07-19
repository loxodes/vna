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
    s = np.uint16(wb.read(ADC_SRAM_BASE, min(MAX_SAMPLES, nsamples)))

    while remaining_samples > 0:
        nsamples_to_read = min(remaining_samples, MAX_SAMPLES)
        s = np.append(s, wb.read(ADC_SRAM_BASE + len(s) * 4, nsamples_to_read))
        remaining_samples -= nsamples_to_read


    wb.close()
    plt.subplot(2,1,1)
    plt.plot(s)
    plt.subplot(2,1,2)
    plt.magnitude_spectrum(s - 2048, Fs=25e6, scale = 'dB')
    plt.show()


