# horrible bit-banged beaglebone driver to control synth r1 boards
# ported over from energia program, synth_test.ino..

import time
from bbone_spi_bitbang import bitbang_spi
import Adafruit_BBIO.GPIO as GPIO

BIT0 = (1 << 0)
BIT1 = (1 << 1)
BIT2 = (1 << 2)
BIT3 = (1 << 3)
BIT4 = (1 << 4)
BIT5 = (1 << 5)
BIT6 = (1 << 6)
BIT7 = (1 << 7)
BIT8 = (1 << 8)
BIT9 = (1 << 9)
BIT10 = (1 << 10)
BIT11 = (1 << 11)
BIT12 = (1 << 12)
BIT13 = (1 << 13)
BIT14 = (1 << 14)
BIT15 = (1 << 15)
BIT16 = (1 << 16)
BIT17 = (1 << 17)
BIT18 = (1 << 18)
BIT19 = (1 << 19)
BIT20 = (1 << 20)
BIT21 = (1 << 21)
BIT22 = (1 << 22)
BIT23 = (1 << 23)

REG0_LD_EN 	= BIT13
REG0_FCAL_EN 	= BIT3
REG0_RESET 	= BIT1
REG0_MUXOUT_SEL = BIT2
REG46_MASH_ORDER_2 = 2
REG46_MASH_EN 	= BIT5
REG46_OUTA_PD 	= BIT6
REG46_OUTB_PD 	= BIT7

REG30_VCO_2X_EN = BIT0

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


LMX_REG_DEFAULTS = [0x0210, 0x0808, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x20b2, \ # 0-7
		    0x1000, 0x0082, 0x1058, 0x0008, 0x7000, 0x0000, 0x0000, 0x0000, \ # 7-15
		    0x0000, 0x0000, 0x0000, 0x0965, 0x0000, 0x0000, 0x0000, 0x8842, \ # 16-23
		    0x0509, 0x0000, 0x0000, 0x0000, 0x2924, 0x0084, 0x0034, 0x0001, \ # 24-31
		    0x4210, 0x4210, 0xc3d0, 0x0019, 0x0000, 0x4000, 0x0000, 0x8004, \ # 32-39
		    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x00c0, \ # 40-47 TODO: 46 only work
		    0x03fc, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, \ # 48-55
		    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x00af] \ # 56-64
LMX_REG_DEFAULTS[46] |= REG46_MASH_ORDER_2 | REG46_MASH_EN

MIN_N = 16
FRAC_DENOM = 200000
PFD = 100e6
F_VCO_MIN = 3.55e9
F_VCO_MAX = 7.1e9
PRE_N = 2

SYNTHA_PINS = { \
	'filta' = 'P9_42' \
	'filtb' = 'P8_39' \
	'filtc' = 'P8_33' \
	'lmx_pow_en' = 'P9_41' \
	'lmx_clk' = 'P9_31' \
	'lmx_ce' = 'P9_28' \
	'lmx_data' = 'P9_29' \
	'lmx_le' = 'P9_30' \
	'lmx_lock' = 'P8_13' \
	'ref_scl' = 'P9_19' \
	'ref_sda' = 'P9_20' \
	'ref_oe' = 'P9_26' \
	'att_1' = 'P9_24' \
	'att_2' = 'P9_22' \
	'att_3' = 'P9_18' \
	'att_4' = 'P9_16' \
	'att_5' = 'P9_14' \
	'att_6' = 'P9_12' \
	'rf_sw' = 'P8_19', \
	'power_det' = 'P9_40'}
	
SYNTHB_PINS = {
	'filta' = 'P9_11' \
	'filtb' = 'P9_13' \
	'filtc' = 'P9_15' \
	'lmx_pow_en' = 'P9_39' \
	'lmx_clk' = 'P9_31' \
	'lmx_ce' = 'P9_23' \
	'lmx_data' = 'P9_29' \
	'lmx_le' = 'P9_25' \
	'lmx_lock' = 'P9_27' \
	'ref_scl' = 'P9_19' \
	'ref_sda' = 'P9_20' \
	'ref_oe' = 'P9_21' \
	'att_1' = 'P8_18' \
	'att_2' = 'P8_16' \
	'att_3' = 'P8_14' \
	'att_4' = 'P8_12' \
	'att_5' = 'P8_10' \
	'att_6' = 'P8_8' \
	'rf_sw' = 'P8_31', \
	'power_det' = 'P9_39'}

RF_SW_LOWFREQ = GPIO.LOW
RF_SW_HIGHFREQ = GPIO.HIGH


class synth_r1:
    def __init__(self, pins, enable_ref_clk = True):
	self.pins = pins



        self.io_init()
        self.set_attenuator(0)
        self.set_filter_bank(0)
        if enable_ref_clk:
            self.clk_init()
        self.lmx_init()

    def lmx_init(self):
        GPIO.output(self.pins['lmx_pow_en'], GPIO.HIGH)
        GPIO.output(self.pins['lmx_ce'], GPIO.HIGH)

        time.sleep(.01)
	self._set_reg(0, REG0_RESET)
	self._set_reg(46, REG46_MASH_ORDER_2 | REG46_MASH_EN | REG46_OUTB_PD | (0 << REG46_OUTA_POW))
	self._set_reg(31, REG31_VCO_DISTB_PD)
	self._set_reg(12, 0x7001)
	self._set_reg(11, 0x0018)
	self._set_reg(10, 0x10d8)
	self._set_reg(40, FRAC_DENOM & 0xffff)
	self._set_reg(41, (FRAC_DENOM >> 16) & 0xffff)
	self._set_reg(0, REG0_LD_EN | REG0_FCAL_EN | REG0_MUXOUT_SEL)

	time.sleep(.01)
    
    def lmx_chan_pow(self, chan, power):
        self.current_channel = chan
        self.channel_power = power
        # TODO: finish porting c  
      if (chan == CHANNELB) {
                  spi_set_reg(47, (0x3F & power) << REG47_OUTB_POW);
                      spi_set_reg(46, REG46_OUTA_PD);
                        }
        else if (chan == CHANNELA) {
                    spi_set_reg(46, REG46_OUTB_PD | (0x3F & power) << REG46_OUTA_POW);
                      }
          delay(10);

    def _calc_n(self, f, n_step, div):
        # TODO verify floating point stuff..
        return f / (n_step / div)
    
    def _calc_frac(self, f, n, n_step, frac_step, div):
        return (f - n * (n_step / div)) / (frac_step / div)


    def clk_init(self):
        GPIO.output(self.pins['ref_oe'], GPIO.HIGH)

    def io_init(self):
        # configure spi pins
        self.spi = bitbang_spi(self.pins['lmx_le'], self.pins['lmx_data'], self.pins['lmx_lock'], self.pins['lmx_clk'])
        
        # configure gpio pins
        GPIO.setup(self.pins['filta'], GPIO.OUT)
        GPIO.setup(self.pins['filtb'], GPIO.OUT)
        GPIO.setup(self.pins['filtc'], GPIO.OUT)

        GPIO.setup(self.pins['lmx_pow_en'], GPIO.OUT)
        GPIO.setup(self.pins['lmx_ce'], GPIO.OUT)
        
        GPIO.setup(self.pins['ref_oe'], GPIO.OUT)
        GPIO.output(self.pins['ref_oe'], GPIO.LOW)

        GPIO.setup(self.pins['att_1'], GPIO.OUT)
        GPIO.setup(self.pins['att_2'], GPIO.OUT)
        GPIO.setup(self.pins['att_3'], GPIO.OUT)
        GPIO.setup(self.pins['att_4'], GPIO.OUT)
        GPIO.setup(self.pins['att_5'], GPIO.OUT)
        GPIO.setup(self.pins['att_6'], GPIO.OUT)

        GPIO.setup(self.pins['rf_sw'], GPIO.OUT)
    
        # TODO: setup i2c

        # set sane initial pin values


    def set_attenuator(self, att):
        GPIO.output(self.pins['att_1'], GPIO.HIGH)
        GPIO.output(self.pins['att_2'], GPIO.HIGH)
        GPIO.output(self.pins['att_3'], GPIO.HIGH)
        GPIO.output(self.pins['att_4'], GPIO.HIGH)
        GPIO.output(self.pins['att_5'], GPIO.HIGH)
        GPIO.output(self.pins['att_6'], GPIO.HIGH)



    def set_filter_bank(self, freq):
        GPIO.output(self.pins['filta'], GPIO.HIGH)
        GPIO.output(self.pins['filtb'], GPIO.HIGH)
        GPIO.output(self.pins['filtc'], GPIO.HIGH)

        GPIO.output(self.pins['rf_sw'], RF_SW_LOWFREQ)



    def _set_reg(self, reg, d):
        d = d | LMX_REG_DEFAULTS[reg]

        payload = reg << 16
        payload |= (d & 0xffff)

        spi.transfer(payload, bits = 24)

    def _read_reg(self, reg):
        payload = (reg << 16) + (1 << 23)
        return spi.transfer(payload, bits = 24)
	
