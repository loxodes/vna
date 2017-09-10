import hwiopy
import Adafruit_BBIO.GPIO as GPIO
import pdb

class hwiopy_spi:
   def __init__(self, spi_cs, spi_mosi, spi_miso, spi_clk):
        self.bbb = hwiopy.platforms.BBB()
        

        #self.spi_cs = self.bbb.create_pin(spi_cs[1:], 'gpio', 'spi_cs')
        self.spi_cs = spi_cs
        GPIO.setup(self.spi_cs, GPIO.OUT)  # P9_42 doesn't work with hiwiopy, probably a device map issue. just use BBIO on CS for now..
        self.spi_mosi = self.bbb.create_pin(spi_mosi[1:], 'gpio', 'spi_mosi')
#        self.spi_miso = self.bbb.create_pin(spi_miso[1:], 'gpio', 'spi_miso')
        self.spi_clk = self.bbb.create_pin(spi_clk[1:], 'gpio', 'spi_clk')
    
        #self.spi_cs.config('out')
        self.spi_mosi.config('out')
#        self.spi_miso.config('in')
        self.spi_clk.config('out')

        self.bbb.on_start()
        #self.spi_cs.methods['output_high_nocheck']()
        GPIO.output(self.spi_cs, GPIO.HIGH)

   def transfer(self, payload, bits = 8):
        #self.spi_cs.methods['output_low_nocheck']()
        GPIO.output(self.spi_cs, GPIO.LOW)
        
        self.spi_clk.methods['output_low_nocheck']()

        response = 0

        for i in range(bits):
            response = response << 1

            # data clocked in on clock rising edge
            if (payload >> (bits - (i + 1))) & 0x01:
                self.spi_mosi.methods['output_high_nocheck']()
            else:
                self.spi_mosi.methods['output_low_nocheck']()

            self.spi_clk.methods['output_high_nocheck']()
#            response |= self.spi_miso.methods['input_nocheck']()
            self.spi_clk.methods['output_low_nocheck']()

        #self.spi_cs.methods['output_high_nocheck']()

        GPIO.output(self.spi_cs, GPIO.HIGH)

        return response

