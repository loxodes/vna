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
        while True:
            try:
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
                samples = 1j * samples[1::2] + samples[0::2]
                sock.close()
                
                t2 = time.time()
                break

            except:
                import subprocess
                print('restarting ADC server..')
                ssh = subprocess.Popen(["ssh", "debian@bbb", "/home/debian/restart_adc_server"])
                print('adc connection failed! restarting')
                time.sleep(1)

        # de-interleave samples.. there is probably a more pythonic way of doing this
        if paths == 1:
            return samples[0::4]
        elif paths == 2:
            return samples[0::4], samples[1::4]
        elif paths == 4:
            return samples[0::4], samples[1::4], samples[2::4], samples[3::4]
        else:
            print('unrecognized number of paths..')
            pdb.set_trace()
           
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
    adc = ethernet_pru_adc('bbb', 10520)
    path1, path2, path3, path4 = adc.grab_samples(paths=4, number_of_samples = 1024)
    subplot(4,1,1)
    plt.plot(np.real(path1))
    plt.plot(np.imag(path1))
    subplot(4,1,2)
    plt.plot(np.real(path2))
    plt.plot(np.imag(path2))
    subplot(4,1,3)
    plt.plot(np.real(path3))
    plt.plot(np.imag(path3))
    subplot(4,1,4)
    plt.plot(np.real(path4))
    plt.plot(np.imag(path4))
    plt.show()
    #pows, freqs = adc.calc_power_spectrum(path1)
    #adc.plot_power_spectrum(pows, freqs)
    pdb.set_trace()


