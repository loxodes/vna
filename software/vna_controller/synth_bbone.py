# horrible bit-banged beaglebone driver to control lmx2594 synths

import time
import pdb
import Adafruit_BBIO.GPIO as GPIO
from bbone_spi_hwiopy import hwiopy_spi
import numpy as np

def _bit(n):
    return (1 << n)

REG0_FCAL_EN 	= _bit(3)
REG0_RESET 	= _bit(1)
REG0_MUXOUT_SEL = _bit(2)

REG46_MASH_ORDER_2 = 2
REG46_MASH_EN 	= BIT5
REG46_OUTA_PD 	= BIT6
REG46_OUTB_PD 	= BIT7


REG38_PLL_N 	= 1
REG39_PFD_DLY_2 = BIT9

REG36_CHDIV_DISTB_EN = BIT11
REG36_CHDIV_DISTA_EN = BIT10
REG36_CHDIV_SEG_SEL_1 = BIT4
REG36_CHDIV_SEG_SEL_12 = BIT5
REG36_CHDIV_SEG_SEL_123 = BIT6
REG36_CHDIV_SEG3 = 0

REG35_CHDIV_SEG2 = 9
REG35_CHDIV_SEG3_EN = BIT8
REG35_CHDIV_SEG2_EN = BIT7
REG35_CHDIV_SEG1 = 2 
REG35_CHDIV_SEG1_EN = BIT1

REG34_CHDIV_EN = BIT5

REG48_OUTB_MUX_VCO = BIT0
REG48_OUTB_MUX_DIV = 0

REG10_MULT = 7
REG11_PLL_R = 4
REG12_PLL_R_PRE = 0
REG47_OUTB_POW = 0
REG46_OUTA_POW = 8

REG47_OUTA_MUX_DIV = 0
REG47_OUTA_MUX_VCO = BIT11


REG31_VCO_DISTA_PD = BIT9
REG31_VCO_DISTB_PD = BIT10
REG31_CHDIV_DIST_PD = BIT7


LMX_REG_DEFAULTS = [0x0210, 0x0808, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x20b2, \
		    0x1000, 0x0082, 0x1058, 0x0008, 0x7000, 0x0000, 0x0000, 0x0000, \
		    0x0000, 0x0000, 0x0000, 0x0965, 0x0000, 0x0000, 0x0000, 0x8842, \
		    0x0509, 0x0000, 0x0000, 0x0000, 0x2924, 0x0084, 0x0034, 0x0001, \
		    0x4210, 0x4210, 0xc3d0, 0x0019, 0x0000, 0x4000, 0x0000, 0x8004, \
		    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x00c0, \
		    0x03fc, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, \
		    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x00af] 

LMX_REG_DEFAULTS[46] |= REG46_MASH_ORDER_2 | REG46_MASH_EN

MIN_N = 16
FRAC_DENOM = 200000
PFD = 100e6
F_VCO_MIN = 7.5e9
F_VCO_MAX = 15e9
PRE_N = 2
ATT_STEP = .5

CHANNELA = 0
CHANNELB = 1

# TODO: break this out into a better format..
# division to 6 covers down to 1.25 GHz..
N_DIV_RATIOS = 3
div_ratios = [2, 4, 6]
div1_options = [1, 2, 3]
div2_options = [1, 1, 1]
div3_options = [1, 1, 1]



RF_SYNTH_PINS = { \
	'lmx_clk' : 'P9_31', \
	'lmx_ce' : 'P9_13', \
	'lmx_data' : 'P9_29', \
	'lmx_le' : 'P9_28', \
	'lmx_lock' : 'P9_11',\
        'lmx_pow_en' : 'P8_10',\
        'dac_cs' : 'P9_17',\
        'dac_data' : 'P9_21',\
        'dac_sck' : 'P9_22',\
        'amp_en' : 'P8_16',\
        '-5v_en' : 'P8_18',\
        'filta' : 'P9_25',\
        'filtb' : 'P9_23'}

	
DEMOD_SYNTH_PINS = {
	'lmx_clk' : 'P9_31', \
	'lmx_ce' : 'P9_41', \
	'lmx_data' : 'P9_29', \
	'lmx_le' : 'P9_42', \
	'lmx_lock' : 'P9_30',\
        'lmx_pow_en' : 'P8_12'}

# cutoff frequency of paths through filter bank, in Hz
FILTER_BANK_CUTOFFS = [15.0e9, 7.2e9, 4.5e9, 2.50e9]
FILTER_BANK_SIZE = 4

class synth_r1:
    def __init__(self, pins, enable_ref_clk = True, rf_board = False):
        self.pins = pins

        self.io_init()

        if enable_ref_clk:
            self.clk_init()
        
        self.lmx_init()

        self.current_channel = None
        self.current_freq = None
        self.current_filter = None
        self.channel_power = 0 

    def io_init(self):
        # configure spi pins
        self.spi = hwiopy_spi(self.pins['lmx_le'], self.pins['lmx_data'], self.pins['lmx_lock'], self.pins['lmx_clk'])

        # configure gpio pins
        GPIO.setup(self.pins['lmx_pow_en'], GPIO.OUT)
        GPIO.setup(self.pins['lmx_ce'], GPIO.OUT)
        GPIO.setup(self.pins['lmx_lock'], GPIO.IN)

        if self.rf_board:
            GPIO.setup(self.pins['filta'], GPIO.OUT)
            GPIO.setup(self.pins['filtb'], GPIO.OUT)

            GPIO.setup(self.pins['-5v_en'], GPIO.OUT)
            GPIO.setup(self.pins['amp_en'], GPIO.OUT)

            self.dac_spi = hwiopy_spi(self.pins['dac_cs'], self.pins['dac_data'], None, self.pins['dac_sck'])
    

    def lmx_init(self):
        GPIO.output(self.pins['lmx_pow_en'], GPIO.HIGH)
        GPIO.output(self.pins['lmx_ce'], GPIO.HIGH)
        
        if self.rf_board:
            GPIO.output(self.pins['-5v_en'], GPIO.HIGH)
            time.sleep(.01)
            GPIO.output(self.pins['amp_en'], GPIO.HIGH)


        time.sleep(.1)

        self._set_reg(0, REG0_RESET)
        self._set_reg(46, REG46_MASH_ORDER_2 | REG46_MASH_EN | REG46_OUTB_PD | (0 << REG46_OUTA_POW))
        self._set_reg(31, REG31_VCO_DISTB_PD)
        self._set_reg(12, 0x7001)
        self._set_reg(11, 0x0018)
        self._set_reg(10, 0x10d8) 
        self._set_reg(40, (FRAC_DENOM >> 16) & 0xffff)
        self._set_reg(41, FRAC_DENOM & 0xffff)
        self._set_reg(0, REG0_LD_EN | REG0_FCAL_EN | REG0_MUXOUT_SEL)

        time.sleep(.1)
   


    def set_power(self, power):
        # TODO: convert to use macom vga/dac..
        self.channel_power = power

        if self.current_channel == CHANNELA:
            self._set_reg(46, REG46_OUTB_PD | (0x3F & power) << REG46_OUTA_POW)
        else:
            self._set_reg(47, (0x3F & power) << REG47_OUTB_POW)
            self._set_reg(46, REG46_OUTA_PD)


    # set filter bank from frequency
    def set_filter_bank(self, freq):
        # TODO: verify filter indicies
        fidx = 4

        for (i, fc) in enumerate(FILTER_BANK_CUTOFFS):
            if(freq > fc):
                fidx = np.mod(i - 1, FILTER_BANK_SIZE)
                break

        print('setting filter bank to index {}'.format(fidx)) 
        if fidx != self.current_filter:
            GPIO.output(self.pins['filta'], fidx & _bit(0))
            GPIO.output(self.pins['filtb'], fidx & _bit(1))

        self.current_filter = fidx 

    def _calc_n(self, f, n_step, div):
        return int(f / (n_step / div))
    
    def _calc_frac(self, f, n, n_step, frac_step, div):
        return int((f - n * (n_step / div)) / (frac_step / div))

    # set synth frequency
    def set_freq(self, freq):
        # TODO: convert for lmx2594
        self.current_freq = freq

        n_step = PFD * PRE_N
        frac_step = n_step / FRAC_DENOM
        n = MIN_N

        frac = 0
        div1 = 1
        div2 = 1
        div3 = 1

        if freq < F_VCO_MIN:
            for div_i in range(N_DIV_RATIOS):
                if freq > F_VCO_MIN / div_ratios[div_i]:
                    div1 = div1_options[div_i]
                    div2 = div2_options[div_i]
                    div3 = div3_options[div_i]
                    break

            n = self._calc_n(freq, n_step, div_ratios[div_i])
            frac = self._calc_frac(freq, n, n_step, frac_step, div_ratios[div_i])

            reg35 = REG35_CHDIV_SEG1_EN
            reg36 = REG36_CHDIV_DISTA_EN
        

            if div3 != 0:
              reg35 |= REG35_CHDIV_SEG2_EN | REG35_CHDIV_SEG3_EN
              reg35 |= div2_options[div_i] << REG35_CHDIV_SEG2
              reg35 |= div1_options[div_i] << REG35_CHDIV_SEG1

              reg36 |= div3_options[div_i] << REG36_CHDIV_SEG3
              reg36 |= REG36_CHDIV_SEG_SEL_123

            elif div2 != 0:
              reg35 |= REG35_CHDIV_SEG2_EN
              reg35 |= div2_options[div_i] << REG35_CHDIV_SEG2
              reg35 |= div1_options[div_i] << REG35_CHDIV_SEG1
              reg36 |= REG36_CHDIV_SEG_SEL_12

            else:
              reg35 |= 0
              reg36 |= REG36_CHDIV_SEG_SEL_1

            self._set_reg(30, 0)
            self._set_reg(31, REG31_VCO_DISTB_PD)
            self._set_reg(34, REG34_CHDIV_EN)
            self._set_reg(35, reg35)
            self._set_reg(36, reg36)
            self._set_reg(48, REG48_OUTB_MUX_DIV)
            self._set_reg(47, REG47_OUTA_MUX_DIV)

        elif freq > F_VCO_MAX:
            n = self._calc_n(freq/2, n_step, 1)
            frac = self._calc_frac(freq/2, n, n_step, frac_step, 1)

            # enable vco doubler
            self._set_reg(30, REG30_VCO_2X_EN)

            # disable output dividers
            self._set_reg(34, 0)
            self._set_reg(35, 0)
            self._set_reg(36, 0)
            self._set_reg(47, REG47_OUTA_MUX_VCO)
            self._set_reg(48, REG48_OUTB_MUX_VCO)

            # enable channel b, bypass filter bank, disable a buffer
            self._set_reg(31, REG31_CHDIV_DIST_PD)

        else:
            n = self._calc_n(freq, n_step, 1)
            frac = self._calc_frac(freq, n, n_step, frac_step, 1)

            # disable vco doubler
            self._set_reg(30, 0)

            # disable output dividers
            self._set_reg(34, 0)
            self._set_reg(35, 0)
            self._set_reg(36, 0)
            self._set_reg(47, REG47_OUTA_MUX_VCO)
            self._set_reg(48, REG48_OUTB_MUX_VCO)

            # enable channel b, bypass filter bank, disable a buffer
            self._set_reg(31, REG31_CHDIV_DIST_PD)



        # load new n and frac registers 
        self._set_reg(38, (n << REG38_PLL_N))
        self._set_reg(44, (frac >> 16) & 0xFFFF)
        self._set_reg(45, frac & 0xFFFF)
        
        # recalibrate VCO
        self._set_reg(0, REG0_LD_EN | REG0_FCAL_EN | REG0_MUXOUT_SEL)
        
        # update filter bank
        self.set_filter_bank(freq) 

        # update output channel..
        self.set_power(self.channel_power)


    def wait_for_lock(self):
        # wait for pll lock
        while not GPIO.input(self.pins['lmx_lock']):
            print('waiting for lock..')

        
    def _set_reg(self, reg, d):
        d = d | LMX_REG_DEFAULTS[reg]

        payload = reg << 16
        payload |= (d & 0xffff)
        self.spi.transfer(payload, bits = 24)

    def _read_reg(self, reg):
        payload = (reg << 16) + (1 << 23)
        return self.spi.transfer(payload, bits = 24)

if __name__ == '__main__':
    rf_synth = synth_r1(RF_SYNTH_PINS)

    time.sleep(.1)
    rf_synth.set_power(0)

    tstart = time.time()
    rf_synth.set_freq(2.045e9)
    tstop = time.time()

    print("time: " + str(tstop - tstart))
    pdb.set_trace()
