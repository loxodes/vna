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

if __name__ == '__main__':
    i2c = I2C.Device(AD9577_I2C_ADDR, 1)
    i2c.write8(0x11, 0x00) # enable CH0 and CH1
