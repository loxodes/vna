from migen import *
from migen.genlib.cdc import MultiReg

from litex.soc.interconnect.csr import *

from dac import DacController

#    ("dac_test", 1,
#        Subsignal("ldac", Pins("A12")),
#        Subsignal("clr", Pins("A13")),
#        Subsignal("sync", Pins("B13")),
#        Subsignal("sclk", Pins("C13")),
#        Subsignal("din", Pins("D13")),
#        Subsignal("a", Pins("E13")),
#        Subsignal("b", Pins("A14")),
#        IOStandard("LVCMOS33")
#    ),

class DAC7563Core(Module, AutoCSR):
    def __init__(self, dac_pins):
        self._ready = CSRStatus(8)
        self._value_a = CSRStorage(16)
        self._value_b = CSRStorage(16)
        self._output_en = CSRStorage(8)
        self._load = CSRStorage(fields=[CSRField("load", size=1, offset=0, pulse=True)])
        
        self.dac = dac = DacController()
        self.submodules += dac
        
        # hardcode clr and ldac to 0 for serial mode
        self.comb += dac_pins.clr.eq(0)
        self.comb += dac_pins.ldac.eq(0)

        # hook up outputs from module
        self.comb += self._ready.status.eq(dac.ready)
        self.comb += dac_pins.din.eq(dac.dac_sdi)
        self.comb += dac_pins.sync.eq(dac.dac_cs)
        self.comb += dac_pins.sclk.eq(dac.dac_sck)

        # hook up inputs to dac
        self.comb += dac.dac_a.eq(self._value_a.storage[:11])
        self.comb += dac.dac_b.eq(self._value_b.storage[:11])
        self.comb += dac.load.eq(self._load.fields.load)
        
        # hook up a/b enable
        self.comb += dac_pins.a.eq(self._output_en.storage[0])    
        self.comb += dac_pins.b.eq(self._output_en.storage[0])    



