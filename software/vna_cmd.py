import socket 
import cmd
import numpy as np
import pdb
import struct

VNAPORT = 8888
VNAIP = '192.168.1.177'

SWITCH_CMD = np.uint8(ord('w'))
FILT_CMD = np.uint8(ord('f'))
POW_CMD = np.uint8(ord('p'))
DBM_CMD = np.uint8(ord('b'))
SYNTH_CMD = np.uint8(ord('s'))
DET_CMD = np.uint8(ord('d'))
ATT_CMD = np.uint8(ord('a'))
IQ_CMD = np.uint8(ord('q'))
CMD_ERR = np.uint8(ord('E'))

def eth_cmd(sock, values):
    args_str = ''.join([a.tobytes() for a in values])
    sock.sendto(args_str, (VNAIP, VNAPORT))
    rval = sock.recvfrom(1024)
    assert rval[0][0] == args_str[0]
    return rval[0][1:]

class vna(cmd.Cmd):
    def preloop(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.freq = np.float32(0)
    
    def do_att(self, line):
        '''att [0/1] [value]'''
        l = line.split()
        args = [ATT_CMD, np.uint8(l[0]), np.uint8(l[1])]
        print eth_cmd(self.sock, args)
    
    def do_freq(self, line):
        '''freq [0/1] [value]'''
        l = line.split()
        self.freq = int(float(l[1]))
        freq = int(self.freq/10)

        print freq
        args = [SYNTH_CMD, np.uint8(l[0]), \
                np.uint8(freq & 0xff), np.uint8((freq >> 8) & 0xff), np.uint8((freq >> 16) & 0xff), np.uint8((freq >> 24) & 0xff)]
        print('sending: {}'.format(args))
        print eth_cmd(self.sock, args)

    def do_sw(self, line):
        '''sw [1..6] [0/1]'''
        l = line.split()
        args = [SWITCH_CMD, np.uint8(l[0]), np.uint8(l[1])]
        print eth_cmd(self.sock, args)

    def do_filt(self, line):
        '''filt [0/1] [1..8]'''
        l = line.split()
        args = [FILT_CMD, np.uint8(l[0]), np.uint8(l[1])]
        print eth_cmd(self.sock, args)

    def do_pow(self, line):
        '''pow [0/1] [0..63]'''
        l = line.split()
        args = [POW_CMD, np.uint8(l[0]), np.uint8(l[1])]
        print eth_cmd(self.sock, args)

    def do_dbm(self, line):
        '''dbm [+10..-30]'''
        l = line.split()
        args = [DBM_CMD, np.int8(l[0])]
        print args
        print eth_cmd(self.sock, args)


    def do_iq(self, line):
        '''iq'''
        iq = eth_cmd(self.sock, [IQ_CMD])
        adc1 = struct.unpack("<h", iq[0:2])[0]
        adc2 = struct.unpack("<h", iq[2:4])[0]
        adc1 = 1e3 * 3.3 * ((adc1 - 2048)/4096.0) # convert to mV
        adc2 = 1e3 * 3.3 * ((adc2 - 2048)/4096.0) # convert to mV
        print("adc1: {}, adc2: {}".format(adc1, adc2))

    def do_det(self, line):
        '''det'''
        det_val = eth_cmd(self.sock, [DET_CMD, np.uint8(0), np.uint8(0)])
        print("power: " + str(struct.unpack("<h", det_val)[0]/4))
if __name__ == '__main__':
    vna().cmdloop()
