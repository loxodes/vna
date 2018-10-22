import zmq
import numpy as np
import pdb
from synth_commands import *

import os
import matplotlib.pyplot as plt

SWITCH_PATH1 = 1
SWITCH_PATH0 = 0

# lookup table for -20 dBm at output of vna port on vna rf board
RF_TABLE_FREQ = [2e9,2.5e9,3e9,3.5e9,4e9,4.5e9,5e9,5.5e9,6e9,6.5e9,7e9,7.5e9,8e9,8.5e9,9e9,9.5e9,10e9,10.5e9,11.0e9,11.5e9,12.0e9,12.5e9,13.0e9,13.5e9,14e9]
RF_TABLE_LMX =  [6,  6,    7,  7,    8,  10,   20, 25,   30, 50,   50, 50,   50, 50,   50, 50,   50,  50,    50,    50,    50,    50,    50,    50,    50]
RF_TABLE_DAC =  [0,  0,    0,  0,    0,  0,     0,   0,     0,   0,     0,   0,     0,   0,     0,   0,     0,     0,      0,      0,      0,      0,      0,      0,      0]


LO_TABLE_FREQ = [2e9, 16e9]
LO_TABLE_LMX = [50, 50]
LO_TABLE_DAC = None

class zmq_synth:
    def __init__(self, context, synth_ip, synth_port):
        self.sock = context.socket(zmq.REQ)
        self.sock.connect("tcp://{}:{}".format(synth_ip, synth_port))
        
        self.freq = np.float32(0)
        self.pow_cal = False   

    def _eth_cmd(self, cmd, payload):
        self.sock.send(cmd + str(payload))
        reply = self.sock.recv()
        assert reply[COMMAND_INDEX] == cmd
        return reply[COMMAND_INDEX:]
   
    def set_freq(self, f):
        self.freq = int(f)
        self._eth_cmd(FREQ_CMD, f)

    def wait_for_lock(self):
        self._eth_cmd(WAIT_CMD, '')

    def set_filt(self, f):
        self.freq = int(f)
        self._eth_cmd(FILT_CMD, f)

    def set_pow_lmx(self, power):
        self._eth_cmd(LMX_POW_CMD, int(power))
         
    def set_pow_dac(self, dac):
        self._eth_cmd(DAC_POW_CMD, int(dac))
   
    # hacked open-loop amplitude control...
    def level_pow(self, cal):
        if cal == LO_CAL:
            freqs = LO_TABLE_FREQ
            pow_lmx = LO_TABLE_LMX 
            pow_dac = LO_TABLE_DAC 
            print('LO cal: ')
        
        elif cal == RF_CAL:
            freqs = RF_TABLE_FREQ
            pow_lmx = RF_TABLE_LMX
            pow_dac = RF_TABLE_DAC
            print('RF cal: ')

        else:
            freqs = None
            pow_lmx = None
            pow_dac = None

        if pow_lmx:
            pow_setting = int(np.interp(self.freq, freqs, pow_lmx))
            self.set_pow_lmx(pow_setting)
            print('pow: {}'.format(pow_setting))
        
        if pow_dac:
            dac_setting = int(np.interp(self.freq, freqs, pow_dac))
            #self.set_pow_dac(dac_setting)
            print('dac: {}'.format(dac_setting))
            print('bypassing DAC power leveling..')
        

if __name__ == '__main__':
    context = zmq.Context()

    lo_port = SYNTH_PORTS['a']
    rf_port = SYNTH_PORTS['b']

    RF_IP = 'bbone'
    LO_IP = 'bbone'
    print('connecting to LO synth')
    lo_synth = zmq_synth(context, LO_IP, lo_port)

    print('connected, changing frequency')
    lo_synth.set_freq(2.2e9);
    lo_synth.level_pow(LO_CAL);
    lo_synth.set_att(5);


    pdb.set_trace()
