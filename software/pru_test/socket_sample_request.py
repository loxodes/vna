from pylab import *
import socket
import sys
import pdb
import time
from scipy import signal
if __name__ == '__main__':
    SOCKET_ADC_PORT = 10520
    SOCKET_ADC_ADDR = 'bbone'
    NUMBER_OF_SAMPLES = 768 * 2

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    server_address = (SOCKET_ADC_ADDR, SOCKET_ADC_PORT)

    sock.connect(server_address)

    sock.sendall(np.uint32(NUMBER_OF_SAMPLES).tobytes())
    adc_buff_size = np.fromstring(sock.recv(4), dtype=np.uint32)[0]

    remaining_samples = NUMBER_OF_SAMPLES
    data = ''
    while(remaining_samples > 0):
        adc_buffer = sock.recv(adc_buff_size * 4, socket.MSG_WAITALL)
        print('received {} of {} bytes'.format(len(adc_buffer), adc_buff_size * 4))
        data += adc_buffer
        remaining_samples -= len(adc_buffer) / 4
        time.sleep(.05)

    sock.sendall(np.uint32(NUMBER_OF_SAMPLES).tobytes())
    samples = np.fromstring(data, dtype=np.int16)
    samples = samples[0::2] + 1j * samples[1::2]
    sock.close()
    

    fs = 26e6 / 900

    power_spectrum = 20 * log10(abs(fftshift(fft(samples, norm='ortho'))))
    freqs = fftshift(fftfreq(len(samples), d = 1/fs))
    
    plt.plot(freqs / 1000, power_spectrum - max(power_spectrum))
    plt.xlabel('frequency (kHz)')
    plt.ylabel('power (dB, relative to max)')
    plt.show()
    pdb.set_trace()
  

