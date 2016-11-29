# misc vna io stuff 
# switches, multipliers, adc initialization...

# initialize ADC(s)
# set switches
# reset syncb


import zmq
import argparse
import pdb

import Adafruit_BBIO.GPIO as GPIO

from vna_io_commands import *
from adc_bbone_init import *


MIX_EN = "P8_15"
MIX_X2 = "P8_17"

ALC_SW_1_1 = "P8_27"
ALC_SW_1_2 = "P8_29"

SW4_0_0 = "P8_28"
SW4_0_1 = "P8_30"

SYNCB = "P8_41"

SW2_0 = "P8_7"
SW2_1 = "P8_9"
SW2_2 = "P8_11"

SW_MAP = {  SW_DUT_RF : SW2_0, \
            SW_MULT_1 : SW2_1, \
            SW_AUX : SW2_2, \
            SW4_0 : SW4_0_0, \
            SW4_1 : SW4_0_1}
            

class zmq_io_server:
    def __init__(self, context, port):
        self.command_handlers = {\
            VNA_SW_CMD: self._set_switch, \
            MIX_EN_CMD: self._enable_mixer, \
            MIX_MUL_CMD: self._set_multiplier, \
            ADC_INIT_CMD : self._init_adc, \
            ADC_SYNC_CMD: self._sync_adc}

        # init socket stuff
        self.context = context
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(str(port)))

        # init io stuff
        GPIO.setup(MIX_EN, GPIO.OUT)
        GPIO.setup(MIX_X2, GPIO.OUT)
        GPIO.setup(ALC_SW_1_1, GPIO.OUT)
        GPIO.setup(ALC_SW_1_2, GPIO.OUT)
        GPIO.setup(SW4_0_0, GPIO.OUT)
        GPIO.setup(SW4_0_1, GPIO.OUT)
        GPIO.setup(SW2_0, GPIO.OUT)
        GPIO.setup(SW2_1, GPIO.OUT)
        GPIO.setup(SW2_2, GPIO.OUT)
        GPIO.setup(SYNCB, GPIO.OUT)

        GPIO.output(MIX_EN, GPIO.LOW)
        GPIO.output(MIX_X2, GPIO.LOW)

        self.adc_spi1 = bitbang_spi(ADC_SPI_CS1, ADC_SPI_MOSI, ADC_SPI_MISO, ADC_SPI_CLK)
        self.adc_spi2 = bitbang_spi(ADC_SPI_CS2, ADC_SPI_MOSI, ADC_SPI_MISO, ADC_SPI_CLK)
        self.adc_spi3 = bitbang_spi(ADC_SPI_CS3, ADC_SPI_MOSI, ADC_SPI_MISO, ADC_SPI_CLK)
        self.adc_spi4 = bitbang_spi(ADC_SPI_CS4, ADC_SPI_MOSI, ADC_SPI_MISO, ADC_SPI_CLK)

        self.adc_spis = [self.adc_spi1, self.adc_spi2, self.adc_spi3, self.adc_spi4]


    
    def _set_switch(self, message):
        sw = int(message[SW_IDX])
        state = int(message[SW_STATE])
        pin = SW_MAP[sw]
        GPIO.output(pin, state)

        return message[COMMAND_INDEX]

    def _set_multiplier(self, message):
        mult_enable = int(message[1:])

        if mult_enable:
            GPIO.output(MIX_X2,GPIO.HIGH)
        else:
            GPIO.output(MIX_X2,GPIO.LOW)
       
        return message[COMMAND_INDEX]


    def _enable_mixer(self, message):
        mixer_enable = int(message[1:])
        if mixer_enable:
            GPIO.output(MIX_EN,GPIO.HIGH)
        else:
            GPIO.output(MIX_EN,GPIO.LOW)

        return message[COMMAND_INDEX]

    def _init_adc(self, message):
        adc = int(message[1:])

        if adc == ALL_ADC:
            for s in self.adc_spis:
                ad9864_init(s)
        else:
            ad9864_init(adc_spis[adc])
            
        return message[COMMAND_INDEX]

    def _sync_adc(self, message):
        GPIO.output(SYNCB,GPIO.LOW)
        GPIO.output(SYNCB,GPIO.HIGH)
        GPIO.output(SYNCB,GPIO.LOW)

        return message[COMMAND_INDEX]


    def run(self):
        while True:
            message = self.socket.recv()
            command = message[COMMAND_INDEX]
            response = ''

            try:
                response = self.command_handlers[commands](message)

            except:
                print('unrecognized command')
                pdb.set_trace()
            
            socket.send(response)


if __name__ == '__main__':
    context = zmq.Context()
    synth_server = zmq_io_server(context, IO_PORT)
    synth_server.run()
    synth_server.close()
    
    context.destroy()
