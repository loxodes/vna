import zmq
import pdb
import time
from vna_io_commands import *

import os
import matplotlib.pyplot as plt

# table of output power setting vs. frequency for 7 dBm output with a hmc311 following the synth
# currently done manually..

class zmq_io:
    def __init__(self, context, io_ip, io_port):
        self.sock = context.socket(zma.REQ)
        self.sock.connect("tcp://{}:{}".format(synth_ip, synth_port))
        
    def _eth_cmd(self, cmd, payload):
        self.sock.send(cmd + str(payload))
        reply = self.sock.recv()
        assert reply[COMMAND_INDEX] == cmd
        return reply[COMMAND_INDEX:]
   
    def set_switch(self, sw, state):
        self._eth_cmd(VNA_SW_CMD, str(sw) + str(state))

    def adc_init(self, adc):
        self._eth_cmd(ADC_INIT_CMD, adc)
    
    def enable_mixer(self, status = 1):
        self._eth_cmd(MIX_EN_CMD, status)

    def set_multiplier(self, status = 1):
        self._eth_cmd(MIX_MUL_CMD, status)

    def sync_adcs(self):
        self._eth_cmd(ADC_SYNC_CMD, payload = '')

if __name__ == '__main__':
    context = zmq.context()

    zmq_io = zmq_io(context, 'bbone', IO_PORT)

    zmq_io.set_switch(SW_DUT_RF, SW_DUT_PORT1)
    zmq_io.enable_mixer()
    zmq_io.adc_init(ALL_ADC)
    zmq_io.sync_adcs()
    
    raw_input('press enter to continue')
    context.destroy()

