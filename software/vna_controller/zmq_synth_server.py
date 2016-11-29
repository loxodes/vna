import zmq
import argparse
import pdb
import numpy as np

import synth_bbone
from synth_commands import *


SYNTH_PINS = {'a':synth_bbone.SYNTHA_PINS, 'b':synth_bbone.SYNTHB_PINS}


class zmq_synth_server:
    def __init__(self, context, synth, port):
        self.synth = synth
        self.context = context
        self.socket = context.socket(zmp.REP)
        self.socket.bind("tcp://*:{}".format(str(port)))
    
    def _set_freq(self, message):
        freq = float(message[1:])
        self.synth.set_freq(freq)
        return message[COMMAND_INDEX]

    def _set_filter_bank(self, message):
        freq = float(message[1:])
        self.synth.set_filter_bank(freq)
        return message[COMMAND_INDEX]

    def _set_attenuator(self, message):
        att = int(message[1:])
        self.synth.set_atteuator(att)
        return message[COMMAND_INDEX]

    def _set_power(self, message):
        power = int(message[1:])
        self.synth.set_pow(power)
        return message[COMMAND_INDEX]


    def run(self):
        self.command_handlers = {\
            FREQ_CMD : self._set_freq, \
            POW_CMD : self._set_power, \
            FILT_COMMAND : self._set_filter_bank, \
            ATT_CMD : self._set_attenuator}

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

    parser = argparse.ArgumentParser()
    parser.add_argument('--synth', help = 'synth (a/b)', default = 'a')
    args = parser.parse_args()

    context = zmq.Context()
    synth_name = args.synth
    
    pins = SYNTH_PINS[synth_name]
    port = SYNTH_PORTS[synth_name]

    synth = synth_bbone.synth_r1(pins)

    synth_server = ethernet_synth(context, synth, port)
    synth_server.run()
    synth_server.close()
    
    context.destroy()
