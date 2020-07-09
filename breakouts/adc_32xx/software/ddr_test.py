# https://m-labs.hk/migen/manual/reference.html#module-migen.genlib.fifo
#AsyncFIFO(width, depth)
# Read and write interfaces are accessed from different clock domains, named read and write. Use ClockDomainsRenamer to rename to other names.

# input clock domain, ADC bit clock
# output clock domain, system clock

ADC_BITS = 12
FIFO_DEPTH = 1024

from migen import *
from litex.soc.interconnect.csr import AutoCSR, CSRStorage, CSRStatus, CSRField

from migen.genlib.fifo import AsyncFIFO, SyncFIFO
from litex.soc.interconnect import wishbone

class ADC_ShiftReg(Module):
    def __init__(self, bits=int(ADC_BITS/2), bits_per_cycle=2):
        self.output = Signal(bits)
        self.input = Signal(bits_per_cycle)
        
        self.sync.adc_bitclk += [
            self.output.eq(Cat(self.output[bits_per_cycle:], self.input))]

class Pulser(Module):
    def __init__(self):
        self.output = Signal(1)
        self.input = Signal(1)

        state  = Signal(1)

        self.comb += self.output.eq(~state & self.input)
        self.sync.adc_bitclk += state.eq(self.input)

class ADC_DDR_PHY(Module):
    def __init__(self, i_din, rst):
        # GDDRX1_RX.SCLK.Centered Interface, Static Delay
        # see ECP5 High-Speed I/O Interface document, Figure 5.1.
        self.o_q = Signal(2)

        din_delay = Signal()

        self.specials += Instance("IDDRX1F",
            i_SCLK = ClockSignal("adc_bitclk"),
            i_D    = din_delay,
            i_RST  = rst, # resets on high
            o_Q0   = self.o_q[0],
            o_Q1   = self.o_q[1],
        )

        self.specials += Instance("DELAYG",
            p_DEL_MODE="USER_DEFINED",
            p_DEL_VALUE=0, # (25ps per tap, max 127)
            i_A=i_din,
            o_Z=din_delay
        )

class ADC_SampleBuffer(Module):
    def __init__(self):
        self.adc_dout0 = Signal(2)
        self.adc_dout1 = Signal(2)

        self.i_fclk = Signal()
        self.i_we = Signal()

        self.i_re = Signal()
        self.o_readable = Signal()
        self.o_dout = Signal(ADC_BITS)

        self.twos_complement = Signal(ADC_BITS)


        self.pulser = pulser = Pulser()
        self.comb += pulser.input.eq(self.i_fclk)
        self.submodules += pulser


        self.shiftreg0 = shiftreg0 = ADC_ShiftReg(bits_per_cycle=2)
        self.shiftreg1 = shiftreg1 = ADC_ShiftReg(bits_per_cycle=2)
        self.comb += shiftreg0.input.eq(self.adc_dout0)
        self.comb += shiftreg1.input.eq(self.adc_dout1)
        self.submodules += [shiftreg0, shiftreg1]

        # TODO: feed fifo with incrementing counter, see FIFO stuffer?
        # TODO: trigger off ADC WE, capture readable/adc input/etc..
        self.fifo = fifo = ClockDomainsRenamer({"write": "adc_bitclk", "read": "sys"})(AsyncFIFO(ADC_BITS, FIFO_DEPTH))
        self.comb += [
            fifo.we.eq(self.i_we & pulser.output),
            fifo.din.eq(Cat(shiftreg0.output, shiftreg1.output)),
            fifo.re.eq(self.i_re),
            self.o_readable.eq(fifo.readable),
            self.o_dout.eq(fifo.dout),
        ]
        self.submodules += fifo

        self.comb += self.twos_complement.eq(~fifo.din + 1)

        
class ADC_Frontend(Module):
    def __init__(self):
        self.i_re = Signal()
        self.i_we = Signal()
        self.o_readable = Signal()
        self.o_dout = Signal(ADC_BITS)

        self.i_din_0 = Signal()
        self.i_din_1 = Signal()
        self.i_dclk = Signal()
        self.i_fclk = Signal()

        self.adc_buffer = adc_buffer = ADC_SampleBuffer()
        self.submodules += adc_buffer

        self.comb += [
            adc_buffer.i_fclk.eq(self.i_fclk),
            adc_buffer.i_we.eq(self.i_we),
            adc_buffer.i_re.eq(self.i_re),
            self.o_readable.eq(adc_buffer.fifo.readable),
            self.o_dout.eq(adc_buffer.o_dout),
        ]


        # TODO: synchronize DDR PHY to clock with reset?
        adc_phy_0 = ADC_DDR_PHY(self.i_din_0, 0)
        adc_phy_1 = ADC_DDR_PHY(self.i_din_1, 0)
        self.submodules += [adc_phy_0, adc_phy_1]

        # invert bits, p/n lines are swapped into differential buffer
        self.comb += adc_buffer.adc_dout0.eq(~adc_phy_0.o_q)
        self.comb += adc_buffer.adc_dout1.eq(~adc_phy_1.o_q)

class FIFO_Stuffer(Module):
    def __init__(self):
        self.fifo = fifo = SyncFIFO(12, 1024)
        self.submodules += fifo
        counter = Signal(12)


        self.sync += [
            If(fifo.writable,
                fifo.we.eq(1),
                counter.eq(counter+1)
            )]

        self.comb += fifo.din.eq(counter)

class ADC3321_DMA(Module, AutoCSR):
    def __init__(self, adc_ctrl, adc_data):
        self.wishbone = wishbone.Interface()

        self._start = CSRStorage(fields=[CSRField("start_burst", size=1, offset=0, pulse=True)])
        self._ready = CSRStatus(8)
        self._burst_size = CSRStorage(16)
        self._base = CSRStorage(32)
        self._offset = CSRStorage(32) 


        words_count = Signal(16)
        pass_count = Signal(5)
        
        self.comb += [
            adc_ctrl.en_pwr.eq(1),
            adc_ctrl.pdn.eq(0),
            
        ]

        # FIFO 
        self.adc_frontend = adc_frontend = ADC_Frontend()
        self.comb += [
            adc_frontend.i_fclk.eq(adc_data.fclk),
            adc_frontend.i_dclk.eq(ClockSignal("adc_bitclk")),
            adc_frontend.i_din_0.eq(adc_data.da0),
            adc_frontend.i_din_1.eq(adc_data.da1),
        ]
        self.submodules += adc_frontend

        fsm = FSM(reset_state="ADC_RESET")
        self.submodules += fsm

        fsm.act("ADC_RESET",
            adc_ctrl.reset.eq(1),
            NextState("WAIT-FOR-TRIGGER"),
        )
        
        fsm.act("WAIT-FOR-TRIGGER",
            self._ready.status.eq(1),
            self.adc_frontend.i_we.eq(0),
            NextValue(words_count, 0),
            If(self._start.fields.start_burst,
                NextState("CLEAR-FIFO"),
            )
        )

        # TODO: clear fifo at end of read instead of before..
        fsm.act("CLEAR-FIFO",
            self.adc_frontend.i_re.eq(1),
            If(adc_frontend.o_readable == 0,
                NextState("WAIT-FOR-DATA"),
            )

        )

        fsm.act("WAIT-FOR-DATA",
            self.adc_frontend.i_we.eq(1),
            If(adc_frontend.o_readable,
                NextState("WRITE-DATA"),
            )
        )  

        self.comb +=[
            self.wishbone.adr.eq((self._base.storage >> 2) + (self._offset.storage>>2) + words_count),
            self.wishbone.dat_w.eq(adc_frontend.o_dout),
            self.wishbone.sel.eq(0b1111),
        ]

        fsm.act("WRITE-DATA",
            self.adc_frontend.i_we.eq(1),
            self.wishbone.stb.eq(1), # bring high for valid request
            self.wishbone.we.eq(1),  # true for write requests
            self.wishbone.cyc.eq(1), # true when transaction takes place
            
            If(self.wishbone.ack,
                NextValue(words_count, words_count+1),
                adc_frontend.i_re.eq(1),
                If(words_count == (self._burst_size.storage-1),
                    NextState("WAIT-FOR-TRIGGER"),
                    NextValue(pass_count, pass_count+1)
                ).Else(
                    NextState("WAIT-FOR-DATA"),
                )

            )
        )

def pulse_test(dut):
    yield dut.input.eq(0)
    yield
    yield
    yield
    yield dut.input.eq(1)
    yield
    yield
    yield
    yield
    yield dut.input.eq(0)
    yield
    yield
    yield
    yield
    yield dut.input.eq(1)
    yield
    yield
    yield
    yield
    yield dut.input.eq(0)
    yield
    yield
    yield
    
def shift_test(dut):
    for i in range(4):
        yield dut.input.eq(i)
        yield
    yield dut.input.eq(0)
    for i in range(12):
        yield
        
 
def fifo_stuffer_test(dut):
    yield
    yield
    yield
    yield
    yield dut.fifo.re.eq(1)
    yield
    yield dut.fifo.re.eq(0)
    yield
    yield
    yield
    yield dut.fifo.re.eq(1)
    yield
    yield dut.fifo.re.eq(0)
    yield
    yield
    yield
    yield

def c2bool(c):
    return {"-": 1, "_": 0}[c]

def adc_write_sample(dut, value):
    # TODO: break down value to i_din_o/1
    # see https://github.com/litex-hub/litehyperbus/blob/master/test/test_hyperbus.py for better example on how to structure testing?

    yield dut.i_din_0.eq(1)
    yield dut.i_din_1.eq(1)

    adc_clk = "___--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__-"
    fclk    = "__-_______________________________________________-_____________________"
    we      = "___---------------------------------------------------------------------"
    re      = "________________________________________________________________________"
    
    for i in range(len(adc_clk)):
        yield dut.i_re.eq(c2bool(re[i]))
        yield dut.i_we.eq(c2bool(we[i]))
        yield dut.i_fclk.eq(c2bool(fclk[i]))  
        yield       



# def adc_read_sample(dut, value):
#     pass
#         self.i_din_0 = Signal(2)
#         self.i_din_1 = Signal(2) 


#         self.i_fclk = Signal()
#         self.i_we = Signal()

#         self.i_re = Signal()
#         self.o_readable = Signal()
#         self.o_dout = Signal()

def adc_samplebuffer_test(dut):
    yield from adc_write_sample(dut, 1)
    yield from adc_write_sample(dut, 1)
    yield from adc_write_sample(dut, 1)
    yield dut.i_re.eq(1)
    yield
    yield
    yield
    yield
    yield
    yield

    # sample_values = [0x0f, 0x0a]

    # for s in sample_values:
    #     yield from adc_sample(dut, s)

    # for s in sample_values:
    #     yield from read_sample(dut, s)

    
if __name__ == '__main__':
    dut = Pulser()
    run_simulation(dut, shift_test(dut), vcd_name="pulser_test.vcd")
    
