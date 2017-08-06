# horrible bit-banged beaglebone driver to control lmx2594 synths

import time
import pdb
import Adafruit_BBIO.GPIO as GPIO
from bbone_spi_hwiopy import hwiopy_spi
from bbone_spi_bitbang import bitbang_spi
import numpy as np

def _bit(n):
    return (1 << n)

REG0_RESET 	= _bit(1)
REG0_MUXOUT_LD_SEL = _bit(2)
REG0_FCAL_EN 	= _bit(3)


DEFAULT = 0

LMX_REG_DEFAULTS = {\
    0:0x2614, 1:0x0808, 2:0x0500, 3:0x0642, 4:0x0A43, 5:0x00C8, 6:0xC802, 7:0x00B2, \
    8:0x2000, 9:0x0604, 10:0x10D8, 11:0x0018, 12:0x5001, 13:0x4000, 14:0x1E70, 15:0x064F, \
    16:0x0080, 17:0x012C, 18:0x0064, 19:0x27B7, 20:0xE048, 21:0x0401, 22:0x0001, 23:0x007C, \
    24:0x071A, 25:0x0624, 26:0x0DB0, 27:0x0002, 28:0x0488, 29:0x318C, 30:0x318C, 31:0x43EC, \
    32:0x0393, 33:0x1E21, 34:0x0000, 35:0x0004, 36:0x005E, 37:0x0304, 38:0x0002, 39:0x9810, \
    40:0x0000, 41:0x0000, 42:0x0000, 43:0x0000, 44:0x0023, 45:0xC0C0, 46:0x07FC, 47:0x0300, \
    48:0x0300, 49:0x4180, 50:0x0000, 51:0x0080, 52:0x0820, 53:0x0000, 54:0x0000, 55:0x0000, \
    56:0x0000, 57:0x0020, 58:0x8001, 59:0x0001, 60:0x0000, 61:0x00A8, 62:0x0322, 63:0x0000, \
    64:0x1388, 65:0x0000, 66:0x01F4, 67:0x0000, 68:0x03E8, 69:0x0000, 70:0xC350, 71:0x0081, \
    72:0x0001, 73:0x003F, 74:0x0000, 75:0x0840, 76:0x000C, 77:0x0000, 78:0x0003, 79:0x0000, \
    80:0x0000, 81:0x0000, 82:0x0000, 83:0x0000, 84:0x0000, 85:0x0000, 86:0x0000, 87:0x0000, \
    88:0x0000, 89:0x0000, 90:0x0000, 91:0x0000, 92:0x0000, 93:0x0000, 94:0x0000, 95:0x0000, \
    96:0x0000, 97:0x0888, 98:0x0000, 99:0x0000, 100:0x0000, 101:0x0011, 102:0x0000, 103:0x0000, \
    104:0x0000, 105:0x0021, 106:0x0000, 107:0x0000, 108:0x0000, 109:0x0000, 110:0x0000, 111:0x0000, \
    112:0x0000}
LMX_REG_DEFAULTS = {\
    0:0x2614, 1:0x0808, 2:0x0500, 3:0x0642, 4:0x0A43, 5:0x00C8, 6:0xC802, 7:0x00B2, \
    8:0x2000, 9:0x0604, 10:0x10D8, 11:0x0018, 12:0x5001, 13:0x4000, 14:0x1E70, 15:0x064F, \
    16:0x0080, 17:0x012C, 18:0x0064, 19:0x27B7, 20:0xE048, 21:0x0401, 22:0x0001, 23:0x007C, \
    24:0x071A, 25:0x0624, 26:0x0DB0, 27:0x0002, 28:0x0488, 29:0x318C, 30:0x318C, 31:0x43EC, \
    32:0x0393, 33:0x1E21, 34:0x0000, 35:0x0004, 36:0x0000, 37:0x0304, 38:0x0002, 39:0x9810, \
    40:0x0000, 41:0x0000, 42:0x0000, 43:0x0000, 44:0x0023, 45:0xC0C0, 46:0x07FC, 47:0x0300, \
    48:0x0300, 49:0x4180, 50:0x0000, 51:0x0080, 52:0x0820, 53:0x0000, 54:0x0000, 55:0x0000, \
    56:0x0000, 57:0x0020, 58:0x8001, 59:0x0001, 60:0x0000, 61:0x00A8, 62:0x0322, 63:0x0000, \
    64:0x1388, 65:0x0000, 66:0x01F4, 67:0x0000, 68:0x03E8, 69:0x0000, 70:0xC350, 71:0x0081, \
    72:0x0001, 73:0x003F, 74:0x0000, 75:0x0800, 76:0x000C, 77:0x0000, 78:0x0003, 79:0x0000, \
    80:0x0000, 81:0x0000, 82:0x0000, 83:0x0000, 84:0x0000, 85:0x0000, 86:0x0000, 87:0x0000, \
    88:0x0000, 89:0x0000, 90:0x0000, 91:0x0000, 92:0x0000, 93:0x0000, 94:0x0000, 95:0x0000, \
    96:0x0000, 97:0x0888, 98:0x0000, 99:0x0000, 100:0x0000, 101:0x0011, 102:0x0000, 103:0x0000, \
    104:0x0000, 105:0x0021, 106:0x0000, 107:0x0000, 108:0x0000, 109:0x0000, 110:0x0000, 111:0x0000, \
    112:0x0000}
MIN_N = 36
FRAC_DENOM = 170000
PFD = 85e6
F_VCO_MIN = 7.5e9
F_VCO_MAX = 15e9

CHANNELA = 0
CHANNELB = 1
CHANNEL_BOTH = 2
CHANNEL_NONE = 3

# TODO: break this out into a better format..
# division to 6 covers down to 1.25 GHz, we only need to 2 GHz
div_ratios = [2, 4, 6]

PORT_SEL = 'P9_15'

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
    def __init__(self, pins):
        self.pins = pins

        if 'filta' in self.pins:
            self.rf_board = True
        else:
            self.rf_board = False

        self.io_init()

        self.current_channel = CHANNEL_BOTH
        self.current_freq = F_VCO_MAX
        self.current_filter = 0 
        self.channel_power = 0 

        self.lmx_init()


    def io_init(self):
        # configure spi pins
        self.spi = hwiopy_spi(self.pins['lmx_le'], self.pins['lmx_data'], self.pins['lmx_lock'], self.pins['lmx_clk'])

        # configure gpio pins
        GPIO.setup(self.pins['lmx_pow_en'], GPIO.OUT)
        GPIO.output(self.pins['lmx_pow_en'], GPIO.HIGH)

        GPIO.setup(self.pins['lmx_ce'], GPIO.OUT)
        GPIO.setup(self.pins['lmx_lock'], GPIO.IN)

        GPIO.setup(self.pins['lmx_lock'], GPIO.IN)

        if self.rf_board:
            GPIO.setup(self.pins['filta'], GPIO.OUT)
            GPIO.setup(self.pins['filtb'], GPIO.OUT)

            GPIO.setup(self.pins['-5v_en'], GPIO.OUT)
            GPIO.output(self.pins['-5v_en'], GPIO.HIGH)

            GPIO.setup(self.pins['amp_en'], GPIO.OUT)
            GPIO.output(self.pins['amp_en'], GPIO.HIGH) # disable 5V rail until DAC is tested, active low

            GPIO.setup(PORT_SEL, GPIO.OUT)

            GPIO.output(PORT_SEL, GPIO.HIGH)


            self.dac_spi = bitbang_spi(self.pins['dac_cs'], self.pins['dac_data'], None, self.pins['dac_sck'])
            self.set_power_dac(500)

        time.sleep(.1)
    

    def lmx_init(self):
        GPIO.output(self.pins['lmx_ce'], GPIO.HIGH)
       
        self.current_channel = CHANNEL_NONE

        if self.rf_board:
            GPIO.output(self.pins['amp_en'], GPIO.LOW)
            self.current_filter = 0

        time.sleep(.05)

        self._set_reg(0, REG0_RESET, defaults = False)
        self._set_reg(0, DEFAULT)
        
        # load in register values generated by TICS Pro
        for i in range(112,-1,-1):
            self._set_reg(i, DEFAULT)
 
        self.set_freq(2.15e9)

    def set_power_dac(self, power):
        # assuming 10 bit ltc2630
        # send write and update command
        self.dac_spi.transfer(0x03 << 20 | ((power & 0x3FF) << 6), bits = 24)

    def set_power_lmx(self, power):
        # TODO: convert to use macom vga/dac..
        # currently just output lmx2594 power units..

        self.channel_power = power & 0x3F

        r44 = 0
        r45 = 0
    

        # keep mux for channel A on VCO if we're outputting the vco..
        if self.current_freq > F_VCO_MIN:
            r45 = _bit(11) 
        
        if self.current_channel == CHANNEL_BOTH:
            # enable channel A, enable channel B
            print('both channels active!')
            r45 |= self.channel_power  # set channel B power
            r44 |= self.channel_power << 8 # set channel A power

        elif self.current_channel == CHANNELA:
            # enable channel A, disable channel B
            print('channel a active!')
            r44 |= _bit(7) # set OUTB_PD
            r44 |= self.channel_power << 8 # set channel A power

        elif self.current_channel == CHANNELB:
            # enable channel B, disable channel A
            print('channel b active!')
            r44 |= _bit(6) # set OUTA_PD
            r45 |= self.channel_power  # set channel B power

        else:
            # disable channels A and B
            print('both channels inactive!')
            r44 |= _bit(7) # set OUTB_PD
            r44 |= _bit(6) # set OUTA_PD

        self._set_reg(45, r45)
        self._set_reg(44, r44)

    # set filter bank from frequency
    def set_filter_bank(self, freq):
        fidx = 3

        for (i, fc) in enumerate(FILTER_BANK_CUTOFFS):
            if(freq > fc):
                fidx = np.mod(i - 1, FILTER_BANK_SIZE)
                break

        print('setting filter bank to index {}'.format(fidx)) 
        if fidx != self.current_filter:
            GPIO.output(self.pins['filta'], fidx & _bit(0))
            GPIO.output(self.pins['filtb'], fidx & _bit(1))

        self.current_filter = fidx 
        
        if fidx > 1:
            self.current_channel = CHANNELA
        else:
            self.current_channel = CHANNELB

    def _calc_n(self, f, n_step, div):
        return int(f / (n_step / div))
    
    def _calc_frac(self, f, n, n_step, frac_step, div):
        return int((f - n * (n_step / div)) / (frac_step / div))

    # set synth frequency
    def set_freq(self, freq):
        self.current_freq = freq
        n_step = PFD
        frac_step = n_step / FRAC_DENOM
        n = MIN_N

        f_vco = 0
        frac = 0
        
        if freq < F_VCO_MIN:
            for div_i in range(len(div_ratios)):
                if freq > F_VCO_MIN / div_ratios[div_i]:
                    break

            n = self._calc_n(freq, n_step, div_ratios[div_i])
            frac = self._calc_frac(freq, n, n_step, frac_step, div_ratios[div_i])
            f_vco = freq / div_ratios[div_i]

            print('set n to {}, frac to {}, div to {}'.format(n, frac, div_ratios[div_i]))

            self._set_reg(75, div_i << 6) # set vco divider value
            self._set_reg(46, 0) # set OUTB_MUX to divider
            self._set_reg(45, self.channel_power) # set OUTA_MUX to divider (preserve channel power) 

        else:
            n = self._calc_n(freq, n_step, 1)
            frac = self._calc_frac(freq, n, n_step, frac_step, 1)
            f_vco = freq


            print('set n to {}, frac to {}'.format(n, frac))

            # set mux to VCO
            self._set_reg(46, 1) # set OUTB_MUX to vco
            self._set_reg(45, _bit(11) | self.channel_power) # set OUTA_MUX to vco (preserve channel power)

        # load new n and frac registers 
        self._set_reg(36, n)
        self._set_reg(42, (frac >> 16) & 0xFFFF)
        self._set_reg(43, frac & 0xFFFF)

        # set PFD_DLY_SEL, assuming mash order 2
        if f_vco < 10e9:
            self._set_reg(37, 3 << 8)
        else:
            self._set_reg(37, 4 << 8)

       
        # recalibrate VCO
        self._set_reg(0, REG0_FCAL_EN)
        
        if self.rf_board:
            # update filter bank, enable only one output channel
            self.set_filter_bank(freq) 

        else:
            self.current_channel = CHANNEL_BOTH

        # update output channel
        self.set_power_lmx(self.channel_power)


    def wait_for_lock(self):
        # wait for pll lock
        while not GPIO.input(self.pins['lmx_lock']):
            print('waiting for lock..')

        
    def _set_reg(self, reg, d, defaults = True):
        if defaults:
            d = d | LMX_REG_DEFAULTS[reg]

        payload = reg << 16
        payload |= (d & 0xffff)

        #print('setting register {} to {:016b}'.format(reg, d))

        self.spi.transfer(payload, bits = 24)

    def _read_reg(self, reg):
        payload = (reg << 16) + (1 << 23)
        return self.spi.transfer(payload, bits = 24)

if __name__ == '__main__':
    rf_synth = synth_r1(RF_SYNTH_PINS)

    tstart = time.time()
    rf_synth.set_freq(2.045e9)
    tstop = time.time()
    
    rf_synth.set_power_lmx(0)


    print("time: " + str(tstop - tstart))
    pdb.set_trace()
