import Adafruit_BBIO.GPIO as GPIO

class bitbang_spi:
   def __init__(self, spi_cs, spi_mosi, spi_miso, spi_clk):
        self.spi_cs = spi_cs
        self.spi_mosi = spi_mosi
        self.spi_miso = spi_miso
        self.spi_clk = spi_clk

        GPIO.setup(spi_cs, GPIO.OUT)
        GPIO.setup(spi_mosi, GPIO.OUT)
        GPIO.setup(spi_clk, GPIO.OUT)
        GPIO.setup(spi_miso, GPIO.IN)
        GPIO.output(spi_cs, GPIO.HIGH)

   def transfer(self, payload, bits = 8):
        GPIO.output(self.spi_cs, GPIO.LOW)
        GPIO.output(self.spi_clk, GPIO.LOW)

        response = 0
        for i in range(bits):
            response = response << 1
            # data clocked in on clock rising edge
            GPIO.output(self.spi_mosi, (payload >> (bits - (i + 1))) & 0x01)
            GPIO.output(self.spi_clk, GPIO.HIGH)
            response |= GPIO.input(self.spi_miso)
            GPIO.output(self.spi_clk, GPIO.LOW)

        GPIO.output(self.spi_cs, GPIO.HIGH)

        return response


