# driver for ad9577 pll 
# http://www.analog.com/media/en/technical-documentation/data-sheets/AD9577.pdf

# 26 MHz crystal

# set synth ref to 85 MHz (CMOS, OUT2P and OUT2N)
# set if clock to 45 MHz (CMOS, OUT1N)
# enable ref out buffer 

from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
import pdb
import time
from vna_pins_r1 import PINS 

# i2c hooked up to P9 19/20
CLK_REF_SEL = PINS.PLL_REF_SEL
PLL_POW_EN = PINS.PLL_3V3_EN 

AD9577_I2C_ADDR = 0x40

class ad9577_synth:
    def __init__(self):
        self.io_init()
        time.sleep(.5)
        self.ad9577_init()

    def ad9577_init(self):
        self.i2c = Adafruit_I2C(AD9577_I2C_ADDR)
        self.i2c.write8(0x40, 0x02) # enable i2c, set EnI2C on register C0

        self.i2c.write8(0x3A, 0xbf) # power down CH3, CMOS for all outputs on register DR1
        self.i2c.write8(0x3B, 0x00) # enable refout, set PDRefOut on DR2 to 0
    
        # fpfd = 26 MHz
        # fout = fpfd * n / (v * d)
        # vco from 2.15 GHz to 2.55 GHz
        # n is 80 to 131
        # v from 2 to 6
        # d from 1 to 31

        # configure ppl1 (int mode)
        self.i2c.write8(0x18, 0x0a) # set n to 90 in register AF0 (vco of 2340 MHz)
        self.i2c.write8(0x22, 0x8d) # set v0 to 4, d0 to 13 on register ADV0
        self.i2c.write8(0x23, 0x8d) # set v1 to 4, d1 to 13 on register ADV0

        # configure pll2 (int mode)
        self.i2c.write8(0x1C, 0x05) # set n to 85 in register BF3 (vco of 2210 MHz) 
        self.i2c.write8(0x25, 0x4d) # set v2 to 2, d2 to 13 on register BDV0

        # finish configuration

        self.i2c.write8(0x1F, 0x00)
        self.i2c.write8(0x1F, 0x01) # force new acquisition by toggling NewAcq
        self.i2c.write8(0x1F, 0x00)

    def io_init(self):
        GPIO.setup(CLK_REF_SEL, GPIO.OUT)
        GPIO.setup(PLL_POW_EN, GPIO.OUT)

        GPIO.output(CLK_REF_SEL, GPIO.HIGH) # HIGH uses crystal, LOW is ext ref, LVCMOS 26 MHz
        GPIO.output(PLL_POW_EN, GPIO.HIGH)



if __name__ == '__main__':
    s = ad9577_synth()
    #print('TODO: change if synth to 48.25 MHz?)
    pdb.set_trace()
