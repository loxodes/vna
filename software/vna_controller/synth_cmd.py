import socket 
import cmd
import numpy as np
import pdb
import struct

from synth_client import *

SYNTH = 'a'
IP = 'bbone'

class vna(cmd.Cmd):
    def preloop(self):
        context = zmq.Context()
        lo_port = SYNTH_PORTS[SYNTH]
        self.synth = zmq_synth(context, IP, SYNTH_PORTS[SYNTH])
        self.freq = np.float32(0)
    
    def do_att(self, line):
        '''att [value] dB'''
        self.synth.set_att(float(line))
    
    def do_freq(self, line):
        '''freq [value]'''
        self.synth.set_freq(float(line))

    def do_filt(self, line):
        '''freq [value]'''
        self.synth.set_freq(float(line))


    def do_pow(self, line):
        '''pow [0..63]'''
        self.synth.set_pow(float(line))

if __name__ == '__main__':
    vna().cmdloop()
