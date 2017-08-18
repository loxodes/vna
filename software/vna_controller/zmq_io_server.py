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
from clk_synth_bbone import ad9577_synth

MIX_EN = "P8_28"
MIX_X2 = "P8_27"
IF_REF_PWRDN = "P8_29"
ADC_CLK_EN = "P8_30"

V3_EN = "P8_12"




SW_PORT_SEL = "P9_15"
SYNCB = "P8_41"

SW_MAP = {  SW_DUT_RF : SW_PORT_SEL}
            

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

        print('binding socket..')
        self.socket.bind("tcp://*:{}".format(str(port)))
        print('binding complete')
        
        print('initializing reference clocks')
        synth = ad9577_synth()

        # init io stuff
        print('setting up IO')
        GPIO.setup(MIX_EN, GPIO.OUT)
        GPIO.setup(MIX_X2, GPIO.OUT)
        GPIO.setup(SW_PORT_SEL, GPIO.OUT)
        GPIO.setup(SYNCB, GPIO.OUT)
        GPIO.setup(V3_EN, GPIO.OUT)


        GPIO.setup(IF_REF_PWRDN, GPIO.OUT)
        GPIO.setup(ADC_CLK_EN, GPIO.OUT)

        print('setting default values')
        GPIO.output(V3_EN,GPIO.HIGH)
        GPIO.output(MIX_EN, GPIO.LOW)
        GPIO.output(MIX_X2, GPIO.LOW)

        GPIO.output(ADC_CLK_EN, GPIO.HIGH)

        GPIO.output(SW_PORT_SEL, GPIO.LOW)

        GPIO.output(SYNCB, GPIO.HIGH)

        print('initalizing ADCs')
        self.adc_spi1 = bitbang_spi(ADC_SPI_CS1, ADC_SPI_MOSI, ADC_SPI_MISO, ADC_SPI_CLK)
        self.adc_spi2 = bitbang_spi(ADC_SPI_CS2, ADC_SPI_MOSI, ADC_SPI_MISO, ADC_SPI_CLK)
        self.adc_spi3 = bitbang_spi(ADC_SPI_CS3, ADC_SPI_MOSI, ADC_SPI_MISO, ADC_SPI_CLK)
        self.adc_spi4 = bitbang_spi(ADC_SPI_CS4, ADC_SPI_MOSI, ADC_SPI_MISO, ADC_SPI_CLK)
        self.adc_spis = [self.adc_spi1, self.adc_spi2, self.adc_spi3, self.adc_spi4]

        for s in self.adc_spis:
            ad9864_tristate_miso(s)

        print('init complete')

    
    def _set_switch(self, message):
        #sw = message[SW_IDX]
        state = int(message[SW_STATE])
        #pin = SW_MAP[sw]
        GPIO.output(SW_PORT_SEL, state)

        return message[COMMAND_INDEX]

    def _set_multiplier(self, message):
        mult_enable = int(message[1:])

        if mult_enable:

            print('enabling multiplier')
            GPIO.output(MIX_X2,GPIO.HIGH)
        else:
            GPIO.output(MIX_X2,GPIO.LOW)
       
        return message[COMMAND_INDEX]


    def _enable_mixer(self, message):
        mixer_enable = int(message[1:])
        print('enabling mixer')
        if mixer_enable:
            GPIO.output(MIX_EN,GPIO.HIGH)
        else:
            GPIO.output(MIX_EN,GPIO.LOW)

        return message[COMMAND_INDEX]

    def _init_adc(self, message):
        GPIO.output(MIX_EN, GPIO.LOW)
        GPIO.output(IF_REF_PWRDN, GPIO.HIGH)

        adc = int(message[1:])
        if adc == int(ALL_ADC):
            for s in self.adc_spis:
                ad9864_init(s)
        else:
            ad9864_init(self.adc_spis[adc])
            
        GPIO.output(IF_REF_PWRDN, GPIO.LOW)
        return message[COMMAND_INDEX]

    def _sync_adc(self, message):
        GPIO.output(SYNCB,GPIO.HIGH)
        GPIO.output(SYNCB,GPIO.LOW)
        time.sleep(.05)
        GPIO.output(SYNCB,GPIO.HIGH)
        return message[COMMAND_INDEX]


    def run(self):
        print('entering run loop')
        while True:
            print('waiting for command')
            message = self.socket.recv()
            command = message[COMMAND_INDEX]
            print('received {} command, message: {}'.format(command, message))
            response = ''

            if command in self.command_handlers:
                response = self.command_handlers[command](message)
            else:
                print('unrecognized command: {}'.format(command))
                pdb.set_trace()
            
            self.socket.send(response)


if __name__ == '__main__':
    context = zmq.Context()
    print('creating context')
    synth_server = zmq_io_server(context, IO_PORT)
    print('initializing io server')
    synth_server.run()
    print('waiting for connections on port: {}'.format(IO_PORT))
    synth_server.close()
    
    context.destroy()
