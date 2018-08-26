# mmap bit-banging io library

# inspirted by:
# https://graycat.io/tutorials/beaglebone-io-using-python-mmap/
from mmap import mmap
import time, struct

class GPIO:
    def __init__(self):
        GPIO_offset = [0x44307000, 0x4804c000, 0x481ac000, 0x481ae000]
        GPIO_size = 0xfff
        self.gpio_mem = []
        with open("/dev/mem", "r+b" ) as f:
                for offset in GPIO_offset:
                        self.gpio_mem.append(mmap(f.fileno(), GPIO_size, offset=offset))


    def set_output(self, gpio):
        port = gpio[0]
        pin = gpio[1]
        GPIO_OE = 0x134
        reg = struct.unpack("<L", self.gpio_mem[port][GPIO_OE:GPIO_OE+4])[0]
        self.gpio_mem[port][GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg & ~(1 << pin))


    def set_value(self, gpio, value):
        port = gpio[0]
        pin = gpio[1]
        GPIO_SETDATAOUT = 0x194
        GPIO_CLEARDATAOUT = 0x190
        
        if value:
            self.gpio_mem[port][GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", (1 << pin))
        else:
            self.gpio_mem[port][GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", (1 << pin))

    def read_value(self, port, pin):
        return True


if __name__ == "__main__":

    gpio = GPIO()
    # (1,28) is port 1, pin 28
    gpio.set_output((1,28))

    try:
      while(True):
        gpio.set_value((1,28),1)
        gpio.set_value((1,28),0)


    except KeyboardInterrupt:
        for bank in gpio.gpio_mem:
            bank.close()
