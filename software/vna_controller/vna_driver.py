import pdb
import time

import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
import zmq

from skrf.calibration import OnePort

from synth_client import zmq_synth 
from io_client import zmq_io 
from adc_client import ethernet_pru_adc
from vna_io_commands import * 
from synth_commands import *

ADC_RATE = 26e6
DECIMATION_RATE = 900

BB_FREQ = 500
IF_FREQ = 48.25e6 + BB_FREQ

SWITCH_TRIM = 8 # samples to discard to eliminate switching transient

ALL_PORTS = 3
PORT1 = SW_DUT_PORT1
PORT2 = SW_DUT_PORT2

DISABLE = 0 
ENABLE = 1 

DOUBLER_CUTOFF = 5e9

class eth_vna:
    def __init__(self, lo_synth, rf_synth, pru_adc, vna_io):
        self.lo_synth = lo_synth
        self.rf_synth = rf_synth
        self.pru_adc = pru_adc
        self.vna_io = vna_io
       
        self.lo_synth.set_pow_dac(200)
        self.rf_synth.set_pow_dac(200)

        self.rf_synth.set_pow_lmx(0)
        self.rf_synth.set_pow_lmx(0)

        self.vna_io.enable_mixer(status = MIXER_DISABLE)

        self.vna_io.set_switch(SW_DUT_RF, SW_DUT_PORT1)

        self.vna_io.adc_init(ADC1)
        self.vna_io.adc_init(ADC2)
        self.vna_io.adc_init(ADC3)
        self.vna_io.adc_init(ADC4)

        self.vna_io.sync_adcs()
        
        self.vna_io.enable_mixer()
        self.vna_io.set_multiplier(status = DISABLE)
        self.freq = np.float32(0)

        self.lo_to_rf_offset_ratio = 1 
   
    def _fit_freq(self, samples):
        # TODO - power weight phase around max frequency, +/- 10 Hz or so?
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
 
    
    def align_rf_lo_osc(self, align_freq):
        # estimate offset between RF and LO synths, store result in ppm
        self.lo_to_rf_offset_ratio = 1 
        print('estimating offset between rf and lo reference clocks')
        self.vna_io.set_switch(SW_DUT_RF, PORT1)
        
        rf_freq = align_freq
        lo_freq = rf_freq + IF_FREQ 
        doubler = False 

        if rf_freq > DOUBLER_CUTOFF:
            lo_freq = lo_freq / 2.0
            doubler = True
            self.vna_io.set_multiplier(status = ENABLE)
        else:
            self.vna_io.set_multiplier(status = DISABLE)


        self.lo_synth.set_freq(lo_freq)
        self.rf_synth.set_freq(rf_freq)

        self.lo_synth.wait_for_lock()
        self.rf_synth.wait_for_lock()

        self.lo_synth.level_pow(LO_CAL)
        self.rf_synth.level_pow(RF_CAL)

        time.sleep(.05)
       
        a1, b1, a2, b2 = pru_adc.grab_samples(paths = 4, number_of_samples = 2048)
        self.ref_samples = a1 
        self._update_rf_lo_offset_ratio(lo_freq, doubler)


    def _update_rf_lo_offset_ratio(self, lo_freq, doubler):
        # calculate the ratio of fref between RF and LO synths
        offset_freq = self._fit_freq(self.ref_samples) # assume no other strong signals, find frequency error in Hz

        if doubler:
            lo_freq = lo_freq * 2.0

        offset_freq += lo_freq * (self.lo_to_rf_offset_ratio - 1)

        # calculate the LO oscillator error in PPM for funsies
        offset_ppm = 1e6 * (((offset_freq + lo_freq) / (lo_freq)) - 1)
        print('offset of {} ppm with LO at {} Hz'.format(offset_ppm, lo_freq))

        # calculate a ratio to multiply the lo by to correct for the offset
        offset_ratio = (lo_freq + offset_freq) / (lo_freq)
        self.lo_to_rf_offset_ratio = offset_ratio


    def _grab_s_raw(self, navg = 4, rfport = PORT1):
        self.vna_io.set_switch(SW_DUT_RF, rfport)

        s_return_avg = 0
        s_thru_avg = 0
    
        for i in range(navg):
            a2, a1, b2, b1 = pru_adc.grab_samples(paths = 4, number_of_samples = 2048)
           
            if False:
                a1_rms = np.sqrt(np.mean(np.abs(a1)**2))
                a2_rms = np.sqrt(np.mean(np.abs(a2)**2))
                b1_rms = np.sqrt(np.mean(np.abs(b1)**2))
                b2_rms = np.sqrt(np.mean(np.abs(b2)**2))


                plt.subplot(5,1,1)
                plt.title('a1')
                plt.plot(np.real(a1))
                plt.plot(np.imag(a1))
                plt.legend(['I', 'Q'])
                plt.ylabel('adc value')

                plt.subplot(5,1,2)
                plt.title('b1')
                plt.plot(np.real(b1))
                plt.plot(np.imag(b1))
                plt.legend(['I', 'Q'])
                plt.ylabel('adc value')

                plt.subplot(5,1,3)
                plt.title('a2')
                plt.plot(np.real(a2))
                plt.plot(np.imag(a2))
                plt.legend(['I', 'Q'])
                plt.ylabel('adc value')

                plt.subplot(5,1,4)
                plt.title('b2')
                plt.plot(np.real(b2))
                plt.plot(np.imag(b2))
                plt.legend(['I', 'Q'])
                plt.ylabel('adc value')

                plt.subplot(5,1,5)
                plt.title('power spectrum')
                plt.ylabel('power (dB, normalized)')
                fs = ADC_RATE / DECIMATION_RATE 
                freqs = np.linspace(-fs/2, fs/2, 401)
                fpow = np.array([10 * np.log10(np.abs(self._goertzel(a1, f))) for f in freqs])
                fpow -= np.max(fpow)

                plt.plot(freqs, fpow)
                plt.xlabel('frequency (Hz)')

                #plt.subplot(4,1,4)
                #plt.title('b1/a1 ripple')
                #plt.plot(np.real(b1/a1) - np.mean(np.real(b1/a1)))
                #plt.plot(np.imag(b1/a1) - np.mean(np.imag(b1/a1)))
                plt.show()
                
                print("    max freq: {}".format(freqs[np.argmax(fpow)]))
                #pdb.set_trace()
 
            a1 = self._goertzel(a1, BB_FREQ)
            a2 = self._goertzel(a2, BB_FREQ)
            b1 = self._goertzel(b1, BB_FREQ)
            b2 = self._goertzel(b2, BB_FREQ)

                
            print('b1/a1: {}'.format(np.mean(b1/a1)))

            if rfport == PORT1:
                s_return_avg += np.mean(b1 / a1)
                s_thru_avg += np.mean(b2 / a1)
                self.ref_samples = a1

            else:
                s_return_avg += np.mean(b2 / a2)
                s_thru_avg += np.mean(b1 / a2)
                self.ref_samples = a2
        
        return s_return_avg/navg, s_thru_avg/navg

    def sweep(self, fstart, fstop, points, align_lo = False):
        sweep_freqs = np.linspace(fstart, fstop, points)

        sweep_s11 = 1j * np.zeros(points)
        sweep_s21 = 1j * np.zeros(points)
        sweep_s12 = 1j * np.zeros(points)
        sweep_s22 = 1j * np.zeros(points)


        for (fidx, f) in enumerate(sweep_freqs):
            lo_freq = (f + IF_FREQ) * self.lo_to_rf_offset_ratio
            doubler = False

            if lo_freq > DOUBLER_CUTOFF:
                lo_freq = lo_freq / 2.0
                doubler = True
                self.vna_io.set_multiplier(status = ENABLE)
            else:
                self.vna_io.set_multiplier(status = DISABLE)

            self.lo_synth.set_freq(lo_freq)
            self.rf_synth.set_freq(f)
            
            self.lo_synth.wait_for_lock()
            self.rf_synth.wait_for_lock()

            self.lo_synth.level_pow(LO_CAL)
            self.rf_synth.level_pow(RF_CAL)
           
            time.sleep(.01)

            #raw_input('press enter to continue')

            print('{}/{} measuring {} GHz '.format(fidx, points, f/1e9))

            s11, s21 = self._grab_s_raw(navg = 1, rfport = PORT1)
            pdb.set_trace()
            s22, s12 = self._grab_s_raw(navg = 1, rfport = PORT2)

            if align_lo:
                self._update_rf_lo_offset_ratio(lo_freq, doubler)

            print('s11: {} , mag {}'.format(s11, abs(s11)))
            
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
        sdrkit_load = rf.Network(f=sweep_freqs, s=-.0126*np.ones(points), z0=50) # 48.76 ohms, ignore 2 fF parallel cap

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

    synth_rf = zmq_synth(context, 'bbb', SYNTH_PORTS['rf'])
    synth_lo = zmq_synth(context, 'bbb', SYNTH_PORTS['demod'])
    vna_io = zmq_io(context, 'bbb', IO_PORT)
    pru_adc = ethernet_pru_adc('bbb', 10520)


    fstart = 2.00e9
    fstop = 15.00e9
    points = 27

    vna = eth_vna(synth_lo, synth_rf, pru_adc, vna_io)

    #vna.align_rf_lo_osc(fstart)

    data_dir = './meas/'
    filename = raw_input('enter a filename: ')
    sweep = vna.sweep(fstart, fstop, points, align_lo = False)
    sweep.plot_s_db()
    plt.show()
    sweep.write_touchstone(data_dir + filename)
    '''
    vna.slot_calibrate_oneport(fstart, fstop, points)

    while True:
        raw_input("connect dut, then press enter to continue")
        sweep = vna.sweep(fstart, fstop, points)
        sweep_cal = vna.cal_oneport.apply_cal(sweep)
        vna.plot_sparam(sweep_cal)
        sweep_cal.write_touchstone('vna_sweep_cal.s1p')
    '''
