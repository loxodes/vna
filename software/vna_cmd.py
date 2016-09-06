import socket 
import cmd
import numpy as np
import pdb

VNAPORT = 8888
VNAIP = '192.168.1.177'

SWITCH_CMD = np.uint8(ord('w'))
FILT_CMD = np.uint8(ord('f'))
POW_CMD = np.uint8(ord('p'))
SYNTH_CMD = np.uint8(ord('s'))
DET_CMD = np.uint8(ord('d'))
ATT_CMD = np.uint8(ord('a'))
IQ_CMD = np.uint8(ord('q'))
CMD_ERR = np.uint8(ord('E'))

def eth_cmd(sock, values):
    args_str = ''.join([a.tobytes() for a in values])
    sock.sendto(args_str, (VNAIP, VNAPORT))
    return sock.recvfrom(1024)

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

    def do_iq(self, line):
        '''iq'''
        print eth_cmd(self.sock, [IQ_CMD])

    def do_det(self, line):
        '''det'''
        print eth_cmd(self.sock, [DET_CMD, np.uint8(0), np.uint8(0)])
    
if __name__ == '__main__':
    vna().cmdloop()
