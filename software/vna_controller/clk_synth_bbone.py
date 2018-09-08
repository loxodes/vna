# driver for ad9577 pll 
# http://www.analog.com/media/en/technical-documentation/data-sheets/AD9577.pdf

# 26 MHz crystal

# set synth ref to 85 MHz (CMOS, OUT2P and OUT2N)
# set if clock to 45 MHz (CMOS, OUT1N)
# enable ref out buffer 

import Adafruit_GPIO.I2C as I2C
import pdb
import time
from vna_pins_r1 import PINS 
from mmap_gpio import GPIO

# i2c hooked up to P9 19/20
CLK_REF_SEL = PINS.PLL_REF_SEL
PLL_POW_EN =  PINS.PLL_3V3_EN 

AD9577_I2C_ADDR = 0x40

class ad9577_synth:
    def __init__(self):
        self.io_init()
        time.sleep(.5)
        self.ad9577_init()

    def ad9577_init(self):
        self.i2c = I2C.Device(AD9577_I2C_ADDR, 1)
        self.i2c.write8(0x40, 0x02) # enable i2c, set EnI2C on register C0

        self.i2c.write8(0x3A, 0x3f) # enable CH2 and CH3, CMOS for all outputs on register DR1
        self.i2c.write8(0x3B, 0x00) # enable refout, set PDRefOut on DR2 to 0

        self.i2c.write8(0x11, 0x03) # power down CH0 and CH1
    
        # fpfd = 26 MHz
        # fout = fpfd * n / (v * d)
        # vco from 2.15 GHz to 2.55 GHz
        # n is 80 to 131
        # v from 2 to 6
        # d from 1 to 31

        # configure ppl1 (int mode)
        self.i2c.write8(0x18, 0x0a) # set n to 90 in register AF0 (vco of 2340 MHz)
        self.i2c.write8(0x22, 0x8d) # set v0 to 4, d0 to 13 on register ADV0
        self.i2c.write8(0x23, 0x8d) # set v1 to 4, d1 to 13 on register ADV1

        # configure pll2 (int mode)
        self.i2c.write8(0x1C, 0x05) # set n to 85 in register BF3 (vco of 2210 MHz) 
        self.i2c.write8(0x25, 0x4d) # set v2 to 2, d2 to 13 on register BDV0
        self.i2c.write8(0x26, 0x4d) # set v2 to 2, d2 to 13 on register BDV1

        # finish configuration

        self.i2c.write8(0x1F, 0x00)
        self.i2c.write8(0x1F, 0x01) # force new acquisition by toggling NewAcq
        self.i2c.write8(0x1F, 0x00)

    def io_init(self):
        gpio = GPIO()
        gpio.set_output(CLK_REF_SEL)
        gpio.set_output(PLL_POW_EN)

        gpio.set_value(CLK_REF_SEL, gpio.HIGH)
        gpio.set_value(PLL_POW_EN, gpio.HIGH)



if __name__ == '__main__':
    s = ad9577_synth()
