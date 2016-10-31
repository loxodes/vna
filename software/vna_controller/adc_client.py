from pylab import *
import socket
import sys
import pdb
import time
from scipy import signal

class ethernet_pru_adc:
    def __init__(self, adc_addr, adc_port):
        self.adc_addr = adc_addr
        self.adc_port = adc_port

    def grab_samples(self, paths = 2, number_of_samples = 2048):
        t1 =  time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        server_address = (self.adc_addr, self.adc_port)

        sock.connect(server_address)

        sock.sendall(np.uint32(number_of_samples).tostring())
        adc_buff_size = np.fromstring(sock.recv(4), dtype=np.uint32)[0]

        remaining_samples = number_of_samples 
        data = ''
        while(remaining_samples > 0):
            adc_buffer = sock.recv(adc_buff_size * 4, socket.MSG_WAITALL)
            #print('received {} of {} bytes'.format(len(adc_buffer), adc_buff_size * 4))
            data += adc_buffer
            remaining_samples -= len(adc_buffer) / 4

        sock.sendall(np.uint32(number_of_samples).tostring())
        samples = np.fromstring(data, dtype=np.int16)
        samples = samples[0::2] + 1j * samples[1::2]
        sock.close()
        
        t2 = time.time()
        #print("grabbing samples took {} seconds".format(t2 - t1))

        return np.split(samples, paths)
           
    def calc_power_spectrum(self, samples):
        fs = 26e6 / 900 # ad9864 adc clock of 26 MHz, decimation rate of 900

        power_spectrum = 20 * log10(abs(fftshift(fft(samples, norm='ortho'))))
        freqs = fftshift(fftfreq(len(samples), d = 1/fs))

        return power_spectrum, freqs

    def plot_power_spectrum(self, power_spectrum, freqs, show_plot = True):
        plt.plot(freqs / 1000, power_spectrum)
        plt.xlabel('frequency (kHz)')
        plt.ylabel('power (dB, relative to max)')
        if show_plot:
            plt.show()

if __name__ == '__main__':
    adc = ethernet_pru_adc('bbone', 10520)
    path1, path2 = adc.grab_samples(paths=2)
    series = np.append(path1, path2)
    path1 = path1 * hamming(len(path1))
    path2 = path2 * hamming(len(path1))
    subplot(2,1,1)
    plt.plot(path1)
    plt.plot(path2)
    subplot(2,1,2)
    plt.plot(series)
    plt.show()
    #pows, freqs = adc.calc_power_spectrum(path1)
    #adc.plot_power_spectrum(pows, freqs)
    pdb.set_trace()


