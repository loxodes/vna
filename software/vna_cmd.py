import serial
import cmd
import numpy as np
import pdb

VNAPORT = '/dev/ttyACM0'

SWITCH_CMD = np.uint8(ord('w'))
FILT_CMD = np.uint8(ord('f'))
POW_CMD = np.uint8(ord('p'))
SYNTH_CMD = np.uint8(ord('s'))
DET_CMD = np.uint8(ord('d'))
ATT_CMD = np.uint8(ord('a'))
IQ_CMD = np.uint8(ord('q'))
CMD_ERR = np.uint8(ord('E'))

def ser_cmd(port, values):
    port.reset_input_buffer()
    args_str = ''.join([a.tobytes() for a in values])
    port.write(args_str)
    return port.readline()

class vna(cmd.Cmd):
    def preloop(self):
        self.ser = serial.Serial(VNAPORT, 9600)
        self.freq = np.float32(0)
    
    def do_att(self, line):
        '''att [0/1] [value]'''
        l = line.split()
        args = [ATT_CMD, np.uint8(l[0]), np.uint8(l[1])]
        print ser_cmd(self.ser, args)
    
    def do_freq(self, line):
        '''freq [0/1] [value]'''
        l = line.split()
        self.freq = int(float(l[1]))
        strfreq = str(self.freq/10) 
        args = [SYNTH_CMD, np.uint8(l[0])]
        args_str = ''.join([a.tobytes() for a in args]) + strfreq
        print('sending: {}'.format(args_str))
        self.ser.write(args_str)
        print self.ser.readline()

    def do_sw(self, line):
        '''sw [1..6] [0/1]'''
        l = line.split()
        args = [SWITCH_CMD, np.uint8(l[0]), np.uint8(l[1])]
        print ser_cmd(self.ser, args)

    def do_filt(self, line):
        '''filt [0/1] [1..8]'''
        l = line.split()
        args = [FILT_CMD, np.uint8(l[0]), np.uint8(l[1])]
        print ser_cmd(self.ser, args)

    def do_pow(self, line):
        '''pow [0/1] [0..63]'''
        l = line.split()
        args = [POW_CMD, np.uint8(l[0]), np.uint8(l[1])]
        print ser_cmd(self.ser, args)

    def do_iq(self, line):
        '''iq'''
        print ser_cmd(self.ser, [IQ_CMD])

    def do_det(self, line):
        '''det'''
        print ser_cmd(self.ser, [DET_CMD])
    
if __name__ == '__main__':
    vna().cmdloop()
