import serial
import cmd
import np

VNAPORT = '/dev/ttyUSB0'

SWITCH_CMD = np.uint8(ord('w'))
FILT_CMD = np.uint8(ord('f'))
POW_CMD = np.uint8(ord('p'))
SYNTH_CMD = np.uint8(ord('s'))
DET_CMD = np.uint8(ord('d'))
ATT_CMD = np.uint8(ord('a'))
IQ_CMD = np.uint8(ord('q'))
CMD_ERR = np.uint8(ord('E'))

def ser_cmd(port, values):
    args_str = ''.join([a.tobytes() for a in values])
    ser.write(args_str)
    return ser.readline()

class vna(cmd.Cmd):
    def preloop(self):
        self.ser = serial.Serial(VNAPORT, 9600)
        self.freq = np.float32(0)
    
    def do_att(self, line):
        '''att [0/1] [value]'''
        l = line.split()
        args = [ATT_CMD, np.uint8(l[0]), np.uint8(l[1])]
        ser_cmd(self.ser, args)

    def do_freq(self, line):
        '''freq [0/1] [value]'''
        l = line.split()
        self.freq = np.float32(l[1])
        args = [FREQ_CMD, np.uint8(l[0]), self.freq]
        ser_cmd(self.ser, args)

    def do_sw(self, line):
        '''sw [1..6] [0/1]'''
        l = line.split()
        args = [SWITCH_CMD, np.uint8(l[0]), np.uint8(l[1])]
        ser_cmd(self.ser, args)

    def do_filt(self, line):
        '''filt [0/1] [1..8]'''
        l = line.split()
        args = [FILT_CMD, np.uint8(l[0]), np.uint8(l[1])]
        ser_cmd(self.ser, args)

    def do_pow(self, line):
        '''pow [0/1] [0..63]'''
        l = line.split()
        args = [POW_CMD, np.uint8(l[0]), np.uint8(l[1])]
        ser_cmd(self.ser, args)

    def do_iq(self, line):
        '''iq'''
        iq = ser_cmd(self.ser, [IQ_CMD])

    def do_det(self, line):
        '''det'''
        det = ser_cmd(self.ser, [DET_CMD])

if __name__ == '__main__':
    vna().cmdloop()

