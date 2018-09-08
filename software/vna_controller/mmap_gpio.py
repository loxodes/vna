# mmap bit-banging io library

# inspired by:
# https://graycat.io/tutorials/beaglebone-io-using-python-mmap/
from mmap import mmap
import time, struct

class GPIO:
    def __init__(self):
        GPIO_offset = [0x44e07000, 0x4804c000, 0x481ac000, 0x481ae000]
        GPIO_size = 0xfff
        self.gpio_mem = []

        self.HIGH = True
        self.LOW = False

        with open("/dev/mem", "r+b" ) as f:
                for offset in GPIO_offset:
                        self.gpio_mem.append(mmap(f.fileno(), GPIO_size, offset=offset))

    
    def _read_reg(self, port, offset):
        return struct.unpack("<L", self.gpio_mem[port][offset:offset+4])[0]
   
    def _clear_bit(self, port, offset, bit, mask = True):
        reg = 0
        
        if mask:
            reg = self._read_reg(port, offset)
        self.gpio_mem[port][offset:offset+4] = struct.pack("<L", reg & ~(1 << bit))

    def _set_bit(self, port, offset, bit, mask = True):
        reg = 0

        if mask:
            reg = self._read_reg(port, offset)

        self.gpio_mem[port][offset:offset+4] = struct.pack("<L", reg | (1 << bit))

    def set_output(self, gpio):
        port = gpio[0]
        pin = gpio[1]
        GPIO_OE = 0x134
        self._clear_bit(port, GPIO_OE, pin)

    def set_input(self, gpio): 
        port = gpio[0]
        pin = gpio[1]
        GPIO_OE = 0x134
        GPIO_DATAOUT = 0x13C
        self._set_bit(port, GPIO_OE, pin)

    def set_value(self, gpio, value):
        port = gpio[0]
        pin = gpio[1]
        GPIO_SETDATAOUT = 0x194
        GPIO_CLEARDATAOUT = 0x190
        
        if value:
            self._set_bit(port, GPIO_SETDATAOUT, pin, mask = False)
        else:
            self._set_bit(port, GPIO_CLEARDATAOUT, pin, mask = False)

    def read_value(self, gpio):
        port = gpio[0]
        pin = gpio[1]
        GPIO_DATAIN = 0x138
        reg = self._read_reg(port, GPIO_DATAIN)
        value = reg & (1 << pin)
        return bool(value) 
    
    def __del__(self):
        for bank in self.gpio_mem:
            bank.close()

if __name__ == "__main__":

    gpio = GPIO()
    # (1,28) is port 1, pin 28
    gpio.set_output((1,28))
    gpio.set_input((1,18))
    try:
      while(True):
        gpio.set_value((1,28),1)
        time.sleep(.5)

        print('pin 14: {}'.format(gpio.read_value((1,18))))
        gpio.set_value((1,28),0)
        time.sleep(.5)
        print('pin 14: {}'.format(gpio.read_value((1,18))))


    except KeyboardInterrupt:
        del gpio
