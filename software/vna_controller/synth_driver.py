import socket 
import numpy as np
import pdb
import struct
import time
import skrf as rf
from skrf.calibration import OnePort
import os
import matplotlib.pyplot as plt

SWITCH_PATH1 = 1
SWITCH_PATH0 = 0

SWITCH_CMD = np.uint8(ord('w'))
FILT_CMD = np.uint8(ord('f'))
POW_CMD = np.uint8(ord('p'))
DBM_CMD = np.uint8(ord('b'))
SYNTH_CMD = np.uint8(ord('s'))
DET_CMD = np.uint8(ord('d'))
ATT_CMD = np.uint8(ord('a'))
IQ_CMD = np.uint8(ord('q'))
CMD_ERR = np.uint8(ord('E'))

# table of output power setting vs. frequency for 7 dBm output with a hmc311 following the synth
# currently done manually..
HMC311_7DBM_TABLE_POW = [14, 8, 12, 8, 6, 1, 5, 10, 31, 31, 31]
HMC311_7DBM_TABLE_FREQ = [250e6, 500e6, 1e9, 2e9, 2.5e9, 3e9, 3.5e9, 4e9, 5e9, 6e9, 7e9]

class ethernet_synth:
    def __init__(self, synth_ip, synth_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = synth_port
        self.ip = synth_ip
        self.freq = np.float32(0)
        self.pow_cal = False   

    def _eth_cmd(self, values):
        args_str = ''.join([a.tobytes() for a in values])
        self.sock.sendto(args_str, (self.ip, self.port))
        rval = self.sock.recvfrom(1024)
        assert rval[0][0] == args_str[0]
        return rval[0][1:]
   
    def set_freq(self, f):
        self.freq = int(f)
        freq = int(self.freq/10)
        args = [SYNTH_CMD, np.uint8(0), \
                np.uint8(freq & 0xff), np.uint8((freq >> 8) & 0xff), np.uint8((freq >> 16) & 0xff), np.uint8((freq >> 24) & 0xff)]
        self._eth_cmd(args)

    def set_sw(self, switch, path):
        args = [SWITCH_CMD, np.uint8(switch), np.uint8(path)]
        self._eth_cmd(args)

    def set_filt(self, path, bank = 0):
        args = [FILT_CMD, np.uint8(bank), np.uint8(path)]
        self._eth_cmd(args)

    def set_pow(self, path, power):
        self.channel_power = power
        args = [POW_CMD, np.uint8(path), np.uint8(power)]
        self._eth_cmd(args)
    
    # hacked open-loop amplitude control until power detect board arrives
    # control LO for 7 dBm (optimum power into mixer)
    # leave RF synth uncontrolled, amplitude variation is controlled during calibration
    def level_pow(self, freqs = HMC311_7DBM_TABLE_FREQ, pows = HMC311_7DBM_TABLE_POW):
        pow_setting = int(np.interp(self.freq, freqs, pows))
        self.set_pow(0, pow_setting) # TODO: this assumes freq < F_VCO_MAX, always picks path 0..
        
    def set_att(self, att):
        args = [ATT_CMD, np.uint8(0), np.uint8(att/.5)]
        self._eth_cmd(args)

if __name__ == '__main__':
    LOPORT = 8888
    RFPORT = 8888
    RF_IP = '192.168.1.177'
    LO_IP = '192.168.1.178'

    lo_synth = ethernet_synth(LO_IP, LO_PORT)

    
    lo_synth.set_freq(2.2e9);
    pdb.set_trace()
