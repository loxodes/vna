# driver for ad9577 pll 
# http://www.analog.com/media/en/technical-documentation/data-sheets/AD9577.pdf

# 26 MHz crystal

# set synth ref to 100 MHz (CMOS, OUT2P and OUT2N)
# set if clock to 45.01 MHz (CMOS, OUT1N)
# enable ref out buffer 

from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO

# i2c hooked up to P9 19/20
CLK_REF_SEL = 'P8_8'
PLL_POW_EN = 'P8_14'

AD9577_I2C_ADDR = 0x7f

class ad577_synth:
    def __init__(self):
        self.io_init()
        self.ad9577_init()

    def ad9577_init(self):
        self.i2c.write8(0x40, 0x02) # enable i2c, set EnI2C on register C0

        self.i2c.write8(0x3A, 0xbf) # power down CH3, CMOS for all outputs on register DR1
        self.i2c.write8(0x3B, 0x01) # enable refout, se PDRefOut on DR2 to 1
    
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
        self.i2c.write8(0x18, 0x05) # set n to 85 in register BF3 (vco of 2210 MHz) 
        self.i2c.write8(0x25, 0x4d) # set v2 to 2, d2 to 13 on register BDV0

        # finish configuration
        self.i2c.write8(0x1F, 0x01) # force new acquisition by toggling NewAcq
        self.i2c.write8(0x1F, 0x00)

    def io_init(self):
        GPIO.setup(CLK_REF_SEL, GPIO.OUT)
        GPIO.setup(PLL_POW_EN, GPIO.OUT)

        GPIO.output(CLK_REF_SEL, GPIO.HIGH) # use crystal 
        GPIO.output(PLL_POW_EN, GPIO.HIGH)


        self.i2c = Adafruit_I2C(AD9577_I2C_ADDR)
