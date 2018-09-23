# misc vna io stuff 
# switches, multipliers, adc initialization...

# initialize ADC(s)
# set switches
# reset syncb


import zmq
import argparse
import pdb

from mmap_gpio import GPIO
from vna_pins_r1 import PINS
from vna_io_commands import *
from adc_bbone_init import *
from clk_synth_bbone import ad9577_synth

MIX_EN = PINS.MIX_EN
MIX_X2 = PINS.MIX_X2
ADC_CLK_EN = PINS.ADC_CLK_EN
V3_EN = PINS.PLL_3V3_EN
SW_PORT_SEL = PINS.PORT_SEL_PRU
SYNCB = PINS.AD_SYNCB
DEMOD_3V3_EN = PINS.EXT_DEMOD_3V3_EN
LO_BUF_AMP_EN = PINS.LO_BUF_AMP_EN
SW_MAP = {  SW_DUT_RF : SW_PORT_SEL}
            

class zmq_io_server:
    def __init__(self, context, port):
        self.command_handlers = {\
            VNA_SW_CMD: self._set_switch, \
            MIX_EN_CMD: self._enable_mixer, \
            MIX_MUL_CMD: self._set_multiplier, \
            ADC_INIT_CMD : self._init_adc, \
            ADC_SYNC_CMD: self._sync_adc,\
            ADC_ATTEN_CMD : self._attenuate_adc}

        # init socket stuff
        self.context = context
        self.socket = context.socket(zmq.REP)

        print('binding socket..')
        self.socket.bind("tcp://*:{}".format(str(port)))
        print('binding complete')
        
        # init io stuff
        self.gpio = GPIO()

        print('bringing up 3.3V rail')
        self.gpio.set_output(V3_EN)
        self.gpio.set_value(V3_EN, self.gpio.HIGH)

        print('initializing reference clocks')
        self.synth = ad9577_synth()
        self.synth.lo_powerdown()

        print('setting up IO')
        self.gpio.set_output(DEMOD_3V3_EN)
        self.gpio.set_output(MIX_EN)
        self.gpio.set_output(MIX_X2)
        self.gpio.set_output(SW_PORT_SEL)
        self.gpio.set_output(ADC_CLK_EN)
        self.gpio.set_output(LO_BUF_AMP_EN)
        self.gpio.set_output(SYNCB)

        print('setting default values')
        self.gpio.set_value(DEMOD_3V3_EN, self.gpio.HIGH)
        self.gpio.set_value(MIX_EN, self.gpio.LOW)
        self.gpio.set_value(MIX_X2, self.gpio.LOW)
        self.gpio.set_value(LO_BUF_AMP_EN, self.gpio.LOW)

        self.gpio.set_value(ADC_CLK_EN, self.gpio.HIGH)
        self.gpio.set_value(SYNCB, self.gpio.HIGH)

        self.gpio.set_value(SW_PORT_SEL, self.gpio.HIGH)

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
        self.gpio.set_value(SW_PORT_SEL, state)

        return message[COMMAND_INDEX]

    def _set_multiplier(self, message):
        mult_enable = int(message[1:])

        if mult_enable:

            print('enabling multiplier')
            self.gpio.set_value(MIX_X2,self.gpio.HIGH)
        else:
            self.gpio.set_value(MIX_X2,self.gpio.LOW)
       
        return message[COMMAND_INDEX]


    def _enable_mixer(self, message):
        mixer_enable = int(message[1:])
        print('enabling mixer')
        if mixer_enable:
            self.gpio.set_value(MIX_EN,self.gpio.HIGH)
            self.gpio.set_value(LO_BUF_AMP_EN, self.gpio.HIGH)
        else:
            self.gpio.set_value(MIX_EN,self.gpio.LOW)
            self.gpio.set_value(LO_BUF_AMP_EN, self.gpio.LOW)

        return message[COMMAND_INDEX]

    def _init_adc(self, message):
        self.gpio.set_value(MIX_EN, self.gpio.LOW)
        self.synth.lo_powerdown() 

        time.sleep(.45) 
        adc = int(message[1:])
        if adc == int(ALL_ADC):
            for s in self.adc_spis:
                ad9864_init(s)
        else:
            ad9864_init(self.adc_spis[adc])
        
        time.sleep(.05) 
        self.synth.lo_powerup() 
        return message[COMMAND_INDEX]
    

    def _attenuate_adc(self, message):
        adc = int(message[1:2])
        state = int(message[2:3])
         
        if adc == int(ALL_ADC):
            for s in self.adc_spis:
                ad9864_set_attenuation(s, state)
        else:
            ad9864_set_attenuation(self.adc_spis[adc], state)

        return message[COMMAND_INDEX]

    def _sync_adc(self, message):
        self.gpio.set_value(SYNCB,self.gpio.HIGH)
        self.gpio.set_value(SYNCB,self.gpio.LOW)
        time.sleep(.05)
        self.gpio.set_value(SYNCB,self.gpio.HIGH)
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
