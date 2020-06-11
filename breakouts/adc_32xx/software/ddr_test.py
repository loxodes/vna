# https://m-labs.hk/migen/manual/reference.html#module-migen.genlib.fifo
#AsyncFIFO(width, depth)
# Read and write interfaces are accessed from different clock domains, named read and write. Use ClockDomainsRenamer to rename to other names.

# input clock domain, ADC bit clock
# output clock domain, system clock

ADC_BITS = 12
FIFO_DEPTH = 128

from migen import *
from litex.soc.interconnect.csr import AutoCSR, CSRStorage, CSRStatus, CSRField

from migen.genlib.fifo import AsyncFIFO, SyncFIFO
from litex.soc.interconnect import wishbone

class ADC_ShiftReg(Module):
    def __init__(self, bits=ADC_BITS):
        self.output = Signal(bits)
        self.input = Signal(2)
        
        self.sync += [
            self.output.eq(Cat(self.input,self.output[:-2]))]

class Pulser(Module):
    def __init__(self):
        self.output = Signal(1)
        self.input = Signal(1)
        
        self.state = Signal()
        
        self.comb += [
            self.output.eq(self.input & (self.state))
        ]
        self.sync += [
            self.state.eq(~self.input)
        ]

class ADC_Frontend(Module):
    def __init__(self, FIFO_DEPTH=1024, ADC_BITS=12):
        self.din = Signal(2)
        self.frame = Signal()
        
        pulser = Pulser()
        pulser.input.eq(self.frame)
        self.submodules += pulser
        
        shiftreg = ADC_ShiftReg()
        shiftreg.sync.eq(pulser.output)
        shiftreg.input.eq(self.din)
        
        # https://m-labs.hk/migen/manual/reference.html#module-migen.genlib.fifo
        # see https://github.com/enjoy-digital/litex/blob/master/litex/build/lattice/common.py,  wrappers for DDR
        fifo = AsyncFIFO(ADC_BITS, FIFO_DEPTH)
        fifo.din.eq()
        fifo.we.eq(pulser.output)
        fifo.din.eq(shiftreg.output)
        self.submodules += fifo

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
    def __init__(self, trigger_pad):
        self.wishbone = wishbone.Interface()

        self._start = CSRStorage(fields=[CSRField("start_burst", size=1, offset=0, pulse=True)])
        self._ready = CSRStatus(8)
        self._burst_size = CSRStorage(16)
        self._base = CSRStorage(32)
        self._offset = CSRStorage(32) 

        delay_count = Signal(8)
        words_count = Signal(16)
        pass_count = Signal(5)
        
        # set up clock domains for FIFO input/output
        # set up PHY
        # set up clock input

        # upon triggering,
        # clear out FIFO (discard FIFO_DEPTH bytes?)


        # FIFO 
        adc_frontend = FIFO_Stuffer()#ADC_Frontend()
        self.submodules += adc_frontend

        fsm = FSM(reset_state="WAIT-FOR-TRIGGER")
        self.submodules += fsm
        self.comb += trigger_pad.eq(words_count==15)

        fsm.act("WAIT-FOR-TRIGGER",
            self._ready.status.eq(1),
            NextValue(words_count, 0),
            If(self._start.fields.start_burst,
                NextState("WAIT-FOR-DATA"),
                NextValue(delay_count, 1),
            )
        )

        fsm.act("WAIT-FOR-DATA",
            NextValue(delay_count, delay_count-1),
#            If(adc_frontend.fifo.readable,
            If(delay_count == 0,
                NextState("WRITE-DATA"),
            )
        )  

        self.comb +=[
            self.wishbone.adr.eq((self._base.storage >> 2) + (self._offset.storage>>2) + words_count),
            self.wishbone.dat_w.eq(pass_count),#dc_frontend.fifo.dout),
            self.wishbone.sel.eq(0b1111),
        ]

        fsm.act("WRITE-DATA",
            self.wishbone.stb.eq(1), # bring high for valid request
            self.wishbone.we.eq(1),  # true for write requests
            self.wishbone.cyc.eq(1), # true when transaction takes place
            
            If(self.wishbone.ack,
                NextValue(words_count, words_count+1),
                adc_frontend.fifo.re.eq(1),
                If(words_count == (self._burst_size.storage-1),
                    NextState("WAIT-FOR-TRIGGER"),
                    NextValue(pass_count, pass_count+1)
                ).Else(
                    NextState("WAIT-FOR-DATA"),
                    NextValue(delay_count, 1),

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


if __name__ == '__main__':
    dut = FIFO_Stuffer()
    run_simulation(dut, fifo_stuffer_test(dut), vcd_name="fifostuff.vcd")
    

# create shift register
# inputs: d0, d1
# load in two at a time,
# 
# turn frame sync to pulse
#
# async fifo, 12 bit, latch in shift register output on frame sync pulse
#  