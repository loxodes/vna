import pdb
import time

import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
import zmq
import argparse

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

DOUBLER_CUTOFF = 4e9

DEFAULT_DATA_DIR = './meas/'

class eth_vna:
    def __init__(self, lo_synth, rf_synth, pru_adc, vna_io):
        self.lo_synth = lo_synth
        self.rf_synth = rf_synth
        self.pru_adc = pru_adc
        self.vna_io = vna_io
       
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

        self.vna_io.adc_attenuate(ALL_ADC, 1) 

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

        time.sleep(.5)
       
        a1, b1, a2, b2 = pru_adc.grab_samples(paths = 4, number_of_samples = 96)
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

    def _grab_s_raw(self, navg = 4, rfport = PORT1, rawplot = False):
        self.vna_io.set_switch(SW_DUT_RF, rfport)
        s_return_avg = 0
        s_thru_avg = 0
        sw_term_avg = 0

        for i in range(navg):
            a1, b1, a2, b2 = pru_adc.grab_samples(paths = 4, number_of_samples = 96)
           
            if rawplot:
                a1_rms = np.sqrt(np.mean(np.abs(a1)**2))
                a2_rms = np.sqrt(np.mean(np.abs(a2)**2))
                b1_rms = np.sqrt(np.mean(np.abs(b1)**2))
                b2_rms = np.sqrt(np.mean(np.abs(b2)**2))


                plt.subplot(5,1,1)
                plt.title('a1, {} rms'.format(a1_rms))
                plt.plot(np.real(a1))
                plt.plot(np.imag(a1))
                plt.legend(['I', 'Q'])
                plt.ylabel('adc value')

                plt.subplot(5,1,2)
                plt.title('b1, {} rms'.format(b1_rms))

                plt.plot(np.real(b1))
                plt.plot(np.imag(b1))
                plt.legend(['I', 'Q'])
                plt.ylabel('adc value')

                plt.subplot(5,1,3)
                plt.title('a2, {} rms'.format(a2_rms))
                plt.plot(np.real(a2))
                plt.plot(np.imag(a2))
                plt.legend(['I', 'Q'])
                plt.ylabel('adc value')

                plt.subplot(5,1,4)
                plt.title('b2, {} rms'.format(b2_rms))
                plt.plot(np.real(b2))
                plt.plot(np.imag(b2))
                plt.legend(['I', 'Q'])
                plt.ylabel('adc value')

                plt.subplot(5,1,5)
                plt.title('power spectrum')
                plt.ylabel('power (dB, normalized)')
                fs = ADC_RATE / DECIMATION_RATE 
                freqs = np.linspace(-fs/2, fs/2, 1601)
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
 
            a1_g = self._goertzel(a1, -BB_FREQ - 5)
            a2_g = self._goertzel(a2, -BB_FREQ - 5)
            b1_g = self._goertzel(b1, -BB_FREQ - 5)
            b2_g = self._goertzel(b2, -BB_FREQ - 5)

            if rfport == PORT1:
                print('b1/a1 (mean)    : {}'.format(np.mean(b1/a1)))
                print('b1/a1 (goertzel): {}'.format(b1_g/a1_g))
                print('a1: {}, b1: {}, b2: {}'.format(abs(a1_g), abs(b1_g), abs(b2_g)))
                s_return_avg += np.mean(b1_g/a1_g)
                s_thru_avg += np.mean(b2_g/a1_g)
                sw_term_avg += np.mean(a2_g/b2_g)

                self.ref_samples = a1

            else:
                print('b2/a2 (mean)    : {}'.format(np.mean(b2/a2)))
                print('b2/a2 (goertzel): {}'.format((b2_g/a2_g)))
                print('a2: {}, b2: {}, b1: {}'.format(abs(a2_g), abs(b2_g), abs(b1_g)))
                s_return_avg += np.mean(b2_g/a2_g)
                s_thru_avg += np.mean(b1_g/a2_g)
                sw_term_avg += np.mean(a1_g/b1_g)

                self.ref_samples = a2
        
        return s_return_avg/navg, s_thru_avg/navg, sw_term_avg/navg

    def sweep(self, fstart, fstop, points, navg = 1, align_lo = False, sw_terms = False, rawplot = False):
        sweep_freqs = np.linspace(fstart, fstop, points)

        sweep_s11 = 1j * np.zeros(points)
        sweep_s21 = 1j * np.zeros(points)
        sweep_s12 = 1j * np.zeros(points)
        sweep_s22 = 1j * np.zeros(points)

        sweep_fwd_sw = 1j * np.zeros(points) 
        sweep_rev_sw = 1j * np.zeros(points) 
    
        for (fidx, f) in enumerate(sweep_freqs):
            tfstart = time.time()
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
            
            tfstop = time.time()

            tlevels = time.time()
            self.lo_synth.level_pow(LO_CAL)
            self.rf_synth.level_pow(RF_CAL)
            tlevele = time.time()
            
            self.lo_synth.wait_for_lock()
            self.rf_synth.wait_for_lock()

            
            print('freq change time: {} seconds'.format(tfstop - tfstart))
            print('power level time: {} seconds'.format(tlevele - tlevels))
            #raw_input('press enter to continue')

            print('{}/{} measuring {} GHz '.format(fidx, points, f/1e9))
            print('measuring s11, s21')
            s11, s21, fwd_sw = self._grab_s_raw(navg = navg, rfport = PORT1, rawplot = rawplot)

            print('measuring s21, s22')
            s22, s12, rev_sw = self._grab_s_raw(navg = navg, rfport = PORT2, rawplot = rawplot)

            print('s11: {} , mag {}'.format(s11, abs(s11)))
            print('s22: {} , mag {}'.format(s22, abs(s22)))
            print('s21: {} , mag {}'.format(s21, abs(s21)))
            print('s12: {} , mag {}'.format(s12, abs(s12)))
            
            sweep_s11[fidx] = s11
            sweep_s12[fidx] = s12
            sweep_s21[fidx] = s21
            sweep_s22[fidx] = s22
            sweep_fwd_sw[fidx] = fwd_sw
            sweep_rev_sw[fidx] = rev_sw
        s11 = rf.Network(f=sweep_freqs/1e9, s=sweep_s11, z0=50)
        s12 = rf.Network(f=sweep_freqs/1e9, s=sweep_s12, z0=50)
        s21 = rf.Network(f=sweep_freqs/1e9, s=sweep_s21, z0=50)
        s22 = rf.Network(f=sweep_freqs/1e9, s=sweep_s22, z0=50)

        sw_fwd = rf.Network(f=sweep_freqs/1e9, s=sweep_fwd_sw, z0=50)
        sw_rev = rf.Network(f=sweep_freqs/1e9, s=sweep_rev_sw, z0=50)



        if sw_terms:
            return rf.network.four_oneports_2_twoport(s11, s12, s21, s22), sw_fwd, sw_rev

        else:
            return rf.network.four_oneports_2_twoport(s11, s12, s21, s22)

   
    def sdrkits_cal_oneport(self, sweep_freqs):
        # generate cal stardard for sdr-kits Female Rosenberger HochFrequenz .. economy SMA SOL cal kit
        # see http://sdr-kits.net/VNWA/Rosenberger_Female_Cal_Standards_rev4.pdf
        # load resistance of 48.76 ohms from box SN678
        f = rf.Frequency.from_f(sweep_freqs, unit='GHz') 
        media = rf.media.Media(f, 0, 50)
        sdrkit_open = media.line(42.35, 'ps', z0 = 50) ** media.open()
        sdrkit_short = media.line(26.91, 'ps', z0 = 50) ** media.short()
        sdrkit_load = rf.Network(f=sweep_freqs, s=-.0126*np.ones(points), z0=50) # 48.76 ohms, ignore 2 fF parallel cap

        return [sdrkit_short, sdrkit_open, sdrkit_load]

    def sdrkits_cal_twoport(self, sweep_freqs):
        oneport = sdrkits_cal_oneport(sweep_freqs)

        sdrkit_short = rf.two_port_reflect(oneport[0], oneport[0])
        sdrkit_open = rf.two_port_reflect(oneport[1], oneport[1])
        sdrkit_load = rf.two_port_reflect(oneport[2], oneport[2])

        media = rf.media.Media(f, 0, 50)
        sdrkit_thru = media.line(41.00, 'ps', z0 = 50)

        return [sdrkit_short, sdrkit_open, sdrkit_load, sdrkit_thru]

    def _sweep_oneport(self, fstart, fstop, points, navg, port):
        sw =  self.sweep(fstart, fstop, points, navg = navg)
        return rf.Network(f = sw.f/1e9, z0 = sw.z0, s = sw.s[:, port, port])

    def slot_measure_twoport(self, fstart, fstop, points, simultaneous = False, cal_dir = './cal_twoport/', navg = 4):
        sweep_freqs = np.linspace(fstart, fstop, points) / 1e9

        cal_short = None
        cal_load = None
        cal_open = None
    
        if simultaneous:
            raw_input("connect shorts, then press enter to continue")
            cal_short = self.sweep(fstart, fstop, points, navg = navg)
            raw_input("connect loads, then press enter to continue")
            cal_load = self.sweep(fstart, fstop, points, navg = navg)
            raw_input("connect opens, then press enter to continue")
            cal_open = self.sweep(fstart, fstop, points, navg = navg)
        else:

            raw_input("connect short to port 1, then press enter to continue")
            cal_short_1 = self._sweep_oneport(fstart, fstop, points, navg, 0)
            raw_input("connect short to port 2, then press enter to continue")
            cal_short_2 = self._sweep_oneport(fstart, fstop, points, navg, 1)

            raw_input("connect load to port 1, then press enter to continue")
            cal_load_1 = self._sweep_oneport(fstart, fstop, points, navg, 0)
            raw_input("connect load to port 2, then press enter to continue")
            cal_load_2 = self._sweep_oneport(fstart, fstop, points, navg, 1)

            raw_input("connect open to port 1, then press enter to continue")
            cal_open_1 = self._sweep_oneport(fstart, fstop, points, navg, 0)
            raw_input("connect open to port 2, then press enter to continue")
            cal_open_2 = self._sweep_oneport(fstart, fstop, points, navg, 1)

            # TODO: untangle units on frequency foor two port reflect, does not preserve GHz
            # todo: add additional thru for type N, then use chopinhalf to deembed n to sma adapters?
            cal_short = rf.two_port_reflect(cal_short_1, cal_short_2)
            cal_load = rf.two_port_reflect(cal_load_1, cal_load_2)
            cal_open = rf.two_port_reflect(cal_open_1, cal_open_2)



        raw_input("connect thru, then press enter to continue")
        cal_thru, sw_fwd, sw_rev = self.sweep(fstart, fstop, points, sw_terms = True, navg = navg)
        
        cal_short.write_touchstone(cal_dir + 'short.s2p')
        cal_open.write_touchstone(cal_dir + 'open.s2p')
        cal_load.write_touchstone(cal_dir + 'load.s2p')
        cal_thru.write_touchstone(cal_dir + 'thru.s2p')
        cal_load.write_touchstone(cal_dir + 'isolation.s2p')

        sw_fwd.write_touchstone(cal_dir + 'sw_fwd.s1p')
        sw_rev.write_touchstone(cal_dir + 'sw_rev.s1p')

    def measure_lmr16(self, fstart, fstop, points, cal_dir = './cal_twoport/'):
        sweep_freqs = np.linspace(fstart, fstop, points) / 1e9

        raw_input("connect reflect reflect")
        reflect_reflect = self.sweep(fstart, fstop, points)

        raw_input("connect match match")
        match_match, sw_fwd, sw_rev = self.sweep(fstart, fstop, points, sw_terms = True)

        raw_input("connect reflect match")
        reflect_match = self.sweep(fstart, fstop, points)

        raw_input("connect match reflect")
        match_reflect = self.sweep(fstart, fstop, points)

        raw_input("connect thru, then press enter to continue")
        thru = self.sweep(fstart, fstop, points)

        match_match.write_touchstone(cal_dir + 'match_match.s2p')
        reflect_reflect.write_touchstone(cal_dir + 'reflect_reflect.s2p')
        reflect_match.write_touchstone(cal_dir + 'reflect_match.s2p')
        match_reflect.write_touchstone(cal_dir + 'match_reflect.s2p')
        thru.write_touchstone(cal_dir + 'thru_lmr.s2p')

        sw_fwd.write_touchstone(cal_dir + 'lmr_sw_fwd.s1p')
        sw_rev.write_touchstone(cal_dir + 'lmr_sw_rev.s1p')
 
    def measure_trl(self, fstart, fstop, points, cal_dir = './cal_twoport/', navg = 4):
        sweep_freqs = np.linspace(fstart, fstop, points) / 1e9

        raw_input("connect reflect to port one")
        reflect_1 = self._sweep_oneport(fstart, fstop, points, navg, 0)
        raw_input("connect reflect to port two")
        reflect_2 = self._sweep_oneport(fstart, fstop, points, navg, 1)
        trl_reflect = rf.two_port_reflect(reflect_1, reflect_2)

        raw_input("connect thru")
        trl_thru, sw_fwd, sw_rev = self.sweep(fstart, fstop, points, navg = navg, sw_terms = True)

        raw_input("connect line")
        trl_line = self.sweep(fstart, fstop, points, navg = navg)

        raw_input("connect verification")
        trl_verification = self.sweep(fstart, fstop, points, navg = navg)

        trl_reflect.write_touchstone(cal_dir + 'trl_reflect.s2p')
        trl_thru.write_touchstone(cal_dir + 'trl_thru.s2p')
        trl_line.write_touchstone(cal_dir + 'trl_line.s2p')

        trl_verification.write_touchstone(cal_dir + 'trl_line_15mm.s2p')

        sw_fwd.write_touchstone(cal_dir + 'trl_sw_fwd.s1p')
        sw_rev.write_touchstone(cal_dir + 'trl_sw_rev.s1p')

   
  
    def plot_sparam(self, sweep):
        plt.subplot(1,2,1)
        sweep.plot_s_db()
        plt.subplot(1,2,2)
        sweep.plot_s_smith()
        plt.show()


if __name__ == '__main__':
    context = zmq.Context()

    parser = argparse.ArgumentParser(description='Vector network analyzer driver.')
    parser.add_argument('--cal', action='store_true', help='collect two port calibration sweeps (SLOT)')
    parser.add_argument('--trl', action='store_true', help='collect TRL calibration sweeps')
    parser.add_argument('--lmr', action='store_true', help='collect two port calibration sweeps (LMR-16)')
    parser.add_argument('--swterms', action='store_true', help='save switch terns')
    parser.add_argument('--rawplot', action='store_true', help='plot raw a/b samples')
    parser.add_argument('--simultaneous', action='store_true', help='collect SOLT cal measurements from both ports simultaneously')
    parser.add_argument('--points', type=int, default=261, help='number of points in sweep')
    parser.add_argument('--navg', type=int, default=1, help='number averages')
    parser.add_argument('--fstart', type=float, default=2e9, help='sweep start frequency (Hz)')
    parser.add_argument('--fstop', type=float, default=15e9, help='sweep stop frequency (Hz)')
    args = parser.parse_args()


    vna_io = zmq_io(context, 'bbb', IO_PORT)
    synth_rf = zmq_synth(context, 'bbb', SYNTH_PORTS['rf'])
    synth_lo = zmq_synth(context, 'bbb', SYNTH_PORTS['demod'])
    pru_adc = ethernet_pru_adc('bbb', 10520)
    vna = eth_vna(synth_lo, synth_rf, pru_adc, vna_io)

    fstart = args.fstart
    fstop = args.fstop
    points = args.points

    if args.cal:
        vna.slot_measure_twoport(fstart, fstop, points, simultaneous = args.simultaneous)
    elif args.lmr:
        vna.measure_lmr16(fstart, fstop, points)
    elif args.trl:
        vna.measure_trl(fstart, fstop, points)

    else:
        filename = raw_input('enter a filename: ')
        tstart = time.time()
        sweep = vna.sweep(fstart, fstop, points, navg = args.navg, rawplot = args.rawplot)

        sweep.write_touchstone(DEFAULT_DATA_DIR + filename)

        tend = time.time()

        print('sweep duration: {}'.format(tend - tstart))
        vna.plot_sparam(sweep)


