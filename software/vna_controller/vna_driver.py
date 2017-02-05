import pdb
import time

import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
import zmq

from scipy.stats import circmean
from skrf.calibration import OnePort

from synth_client import zmq_synth 
from io_client import zmq_io 
from adc_client import ethernet_pru_adc
from vna_io_commands import * 
from synth_commands import *

ADC_RATE = 26e6
DECIMATION_RATE = 900

IF_FREQ = 45.000e6
SWITCH_TRIM = 8 # samples to discard to eliminate switching transient

ALL_PORTS = 3
PORT1 = SW_DUT_PORT1
PORT2 = SW_DUT_PORT2

ENABLE = True
DISABLE = False

class eth_vna:
    def __init__(self, lo_synth, rf_synth, pru_adc, vna_io):
        self.lo_synth = lo_synth
        self.rf_synth = rf_synth
        self.pru_adc = pru_adc
        self.vna_io = vna_io
        
        self.vna_io.set_switch(SW_DUT_RF, SW_DUT_PORT1)
        self.vna_io.adc_init(ALL_ADC)
        self.vna_io.sync_adcs()

        self.vna_io.enable_mixer()
        self.vna_io.set_multiplier(DISABLE)

        self.freq = np.float32(0)
   
    def _fit_freq(self, samples):
        # TODO: do this from some sort of fitting
        ref_freq = (ADC_RATE / DECIMATION_RATE) * (np.mean(np.diff(np.unwrap(np.angle(samples)))) / (2 * np.pi)) 
        return ref_freq

    def _goertzel(self, samples, freq, rate = ADC_RATE/DECIMATION_RATE):
        # generalized goertzel for arbitrary frequencies
        # see figure 4,  Goertzel algorithm generalized to non-integer multiples of fundamental frequency (Petr Sysel and Pavel Rajmic)
        # http://asp.eurasipjournals.springeropen.com/articles/10.1186/1687-6180-2012-56
        
        N = len(samples)
        k = N * (freq / rate)

        A = 2 * np.pi * k / N
        B = 2 * np.cos(A)
        C = np.exp(-1j * A)
        D = np.exp(-1j * 2 * np.pi * (k / N) * (N - 1))

        s0 = 0
        s1 = 0
        s2 = 0

        for i in range(N-2):
            s0 = samples[i] + B * s1 - s2
            s2 = s1
            s1 = s0

        s0 = samples[N-1] + B * s1 - s2
        y = s0 - s1 * C
        y = y * D
        return y
 
 
    def _grab_s_raw(self, navg = 1, rfport = PORT1):
        self.vna_io.set_switch(SW_DUT_RF, rfport)

        ref_freq = 0
        s_return_avg = 0
        s_thru_avg = 0

        for i in range(navg):
            a1, b1, a2, b2 = pru_adc.grab_samples(paths = 4, number_of_samples = 256)
            
            if port == PORT1:
                ref_freq = self._fit_freq(a1)
            elif port == PORT2:
                ref_freq = self._fit_freq(a2)
            else:
                print('unrecognized port!?')
                pdb.set_trace()
            
            a1_fit = self._goertzel(a1, ref_freq)
            b1_fit = self._goertzel(b1, ref_freq)
            a2_fit = self._goertzel(a2, ref_freq)
            b2_fit = self._goertzel(b2, ref_freq)
            
            if port == PORT1:
                s_return_avg += (b1_fit / a1_fit)
                s_thru_avg += (b1_fit / a2_fit)
            else:
                s_return_avg += (b2_fit / a2_fit)
                s_thru_avg += (b2_fit / a1_fit)

        return s_return_avg/navg, s_thru_avg/navg

    def sweep(self, fstart, fstop, points):
        sweep_freqs = np.linspace(fstart, fstop, points)

        sweep_s11 = 1j * np.zeros(points)
        sweep_s21 = 1j * np.zeros(points)
        sweep_s12 = 1j * np.zeros(points)
        sweep_s22 = 1j * np.zeros(points)

        
        for (fidx, f) in enumerate(sweep_freqs):
            self.rf_synth.set_freq(f)
            self.lo_synth.set_freq(f + IF_FREQ)
            self.lo_synth.level_pow()
            time.sleep(.05)

            print('{}/{} measuring {} GHz '.format(fidx, points, f/1e9))

            s11, s21 = self._grab_s_raw(navg = 4, rfport = PORT1)
            s22, s12 = self._grab_s_raw(navg = 4, rfport = PORT2)

            sweep_s11[fidx] = s11
            sweep_s21[fidx] = s21
            sweep_s12[fidx] = s12
            sweep_s22[fidx] = s22
        
        s11 = rf.Network(f=sweep_freqs/1e9, s=sweep_s11, z0=50)
        s21 = rf.Network(f=sweep_freqs/1e9, s=sweep_s21, z0=50)
        s22 = rf.Network(f=sweep_freqs/1e9, s=sweep_s22, z0=50)
        s12 = rf.Network(f=sweep_freqs/1e9, s=sweep_s12, z0=50)

        return rf.network.four_oneports_2_twoport(s11, s12, s21, s22)
   
    def sdrkits_cal_oneport(self, sweep_freqs):
        # generate cal stardard for sdr-kits Female Rosenberger HochFrequenz .. economy SMA SOL cal kit
        # see http://sdr-kits.net/VNWA/Rosenberger_Female_Cal_Standards_rev4.pdf
        # load resistance of 48.76 ohms from box SN678
        f = rf.Frequency.from_f(sweep_freqs, unit='GHz') 
        media = rf.media.Media(f, 0, 50)
        sdrkit_open = media.line(43.78, 'ps', z0 = 50) ** media.open()
        sdrkit_short = media.line(26.91, 'ps', z0 = 50) ** media.short()
        # TODO: add parallep capacitance to load?
        sdrkit_load = rf.Network(f=sweep_freqs, s=-.0126*np.ones(points), z0=50) # 48.76 ohms

        return [sdrkit_short, sdrkit_open, sdrkit_load]

    def sdrkits_cal_twoport(self, sweep_freqs):
        oneport = sdrkits_cal_oneport(sweep_freqs)

        media = rf.media.Media(f, 0, 50)
        sdrkit_thru = media.line(42.43, 'ps', z0 = 50)
        return [sdrkit_thru, oneport[0], oneport[1], oneport[2]]


    def ideal_cal_standard(self, sweep_freqs):
        ideal_open = rf.Network(f=sweep_freqs, s=np.ones(points), z0=50)
        ideal_short = rf.Network(f=sweep_freqs, s=-1*np.ones(points), z0=50)
        ideal_load = rf.Network(f=sweep_freqs, s=np.zeros(points), z0=50)
        return  [ideal_short, ideal_open, ideal_load]
    

    def slot_calibrate_oneport(self, fstart, fstop, points):
        sweep_freqs = np.linspace(fstart, fstop, points) / 1e9
        cal_kit = self.sdrkits_cal_oneport(sweep_freqs)

        raw_input("connect short, then press enter to continue")
        self.cal_short = self.sweep(fstart, fstop, points)
        raw_input("connect load, then press enter to continue")
        self.cal_load = self.sweep(fstart, fstop, points)
        raw_input("connect open, then press enter to continue")
        self.cal_open = self.sweep(fstart, fstop, points)

        #raw_input("connect thru, then press enter to continue")
        #self.cal_thru = self.sweep(fstart, fstop, points)
        self.cal_oneport = rf.OnePort(\
                ideals = cal_kit,\
                measured = [self.cal_short, self.cal_open, self.cal_load])        
                
        self.cal_oneport.run()
 
    def slot_calibrate_twoport(self, fstart, fstop, points):
        sweep_freqs = np.linspace(fstart, fstop, points) / 1e9
        cal_kit = self.generate_sdrkits_cal_standard(sweep_freqs)

        raw_input("connect short to port 1, then press enter to continue")
        self.cal_short_p1 = self.sweep(fstart, fstop, points)
        raw_input("connect load to port 1, then press enter to continue")
        self.cal_load_p1 = self.sweep(fstart, fstop, points)
        raw_input("connect open to port 1, then press enter to continue")
        self.cal_open_p1 = self.sweep(fstart, fstop, points)

        raw_input("connect short to port 2, then press enter to continue")
        self.cal_short_p2 = self.sweep(fstart, fstop, points)
        raw_input("connect load to port 2, then press enter to continue")
        self.cal_load_p2 = self.sweep(fstart, fstop, points)
        raw_input("connect open to port 2, then press enter to continue")
        self.cal_open_p2 = self.sweep(fstart, fstop, points)


        raw_input("connect thru, then press enter to continue")
        self.cal_thru = self.sweep(fstart, fstop, points)
        print('todo: finish writing two port calibration')
        pdb.set_trace()
        self.cal_twoport = rf.OnePort(\
                ideals = cal_kit,\
                measured = [self.cal_short, self.cal_open, self.cal_load])        
                
        self.cal_twoport.run()
    
   
    def plot_sparam(self, sweep):
        plt.subplot(1,2,1)
        sweep.plot_s_db()
        plt.subplot(1,2,2)
        sweep.plot_s_smith()
        plt.show()


if __name__ == '__main__':
    context = zmq.Context()

    synth_rf = zmq_synth(context, 'bbone', SYNTH_PORTS['a'])
    synth_lo = zmq_synth(context, 'bbone', SYNTH_PORTS['b'])
    vna_io = zmq_io(context, 'bbone', IO_PORT)
    pru_adc = ethernet_pru_adc('bbone', 10520)

    fstart = 2e9
    fstop = 5e9
    points = 16 

    vna = eth_vna(synth_rf, synth_lo, pru_adc, vna_io)
    vna.slot_calibrate_oneport(fstart, fstop, points)

    while True:
        raw_input("connect dut, then press enter to continue")
        sweep = self.sweep(fstart, fstop, points)
        sweep_cal = self.cal_oneport.apply_cal(sweep)
        vna.plot_sparam(sweep_cal)
        
    pdb.set_trace()

