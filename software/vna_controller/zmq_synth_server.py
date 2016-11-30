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
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(str(port)))
    
    def _set_freq(self, message):
        freq = float(message[1:])
        print('setting frequency to {} Hz'.format(freq))
        self.synth.set_freq(freq)
        return message[COMMAND_INDEX]

    def _set_filter_bank(self, message):
        freq = float(message[1:])
        print('setting filter bank for {} GHz'.format(freq/1e9))
        self.synth.set_filter_bank(freq)
        return message[COMMAND_INDEX]

    def _set_attenuator(self, message):
        att = float(message[1:])
        print('attenuator to {} dB'.format(att))
        self.synth.set_attenuator(att)
        return message[COMMAND_INDEX]

    def _set_power(self, message):
        power = int(message[1:])
        print('power level to {}'.format(power))
        self.synth.set_power(power)
        return message[COMMAND_INDEX]


    def run(self):
        self.command_handlers = {\
            FREQ_CMD : self._set_freq, \
            POW_CMD : self._set_power, \
            FILT_CMD : self._set_filter_bank, \
            ATT_CMD : self._set_attenuator}
        print('entering run loop')
        while True:
            print('waiting for command..')
            message = self.socket.recv()
            command = message[COMMAND_INDEX]
            print('received {} command, message: {}'.format(command, message))

            response = ''

            if command in self.command_handlers:
                response = self.command_handlers[command](message)
            
            else:
                print('unrecognized command')
                pdb.set_trace()
            
            self.socket.send(response)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--synth', help = 'synth (a/b)', default = 'a')
    args = parser.parse_args()

    context = zmq.Context()
    synth_name = args.synth
    
    pins = SYNTH_PINS[synth_name]
    port = SYNTH_PORTS[synth_name]

    synth = synth_bbone.synth_r1(pins)
    print('initializing synth')
    synth_server = zmq_synth_server(context, synth, port)
    print('running zmq server')
    synth_server.run()
    synth_server.close()
    
    context.destroy()
