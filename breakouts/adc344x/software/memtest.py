from migen import *
from migen.genlib.cdc import MultiReg

from litex.soc.interconnect.csr import *
from litedram.frontend.dma import LiteDRAMDMAWriter
from litedram.common import LiteDRAMNativePort



# https://logs.timvideos.us/%23litex/%23litex.2019-06-02.log.html
# https://github.com/enjoy-digital/litex/blob/master/litex/soc/interconnect/csr.py
# https://github.com/enjoy-digital/litedram/blob/master/litedram/frontend/bist.py#L131

class MemtestCore(Module, AutoCSR):
    def __init__(self, dram_port):
        self._ready = CSRStatus(8)
        self._value = CSRStorage(32)
        self._base = CSRStorage(32)
        self._offset = CSRStorage(32)

        self._start = CSRStorage(fields=[CSRField("start", size=1, offset=0, pulse=True)])
        
        base = Signal(dram_port.address_width)
        offset = Signal(dram_port.address_width)

        # determine the first significant bit of an byte address in memory
        shift = log2_int(dram_port.data_width//8)

        self.comb += [
            base.eq(self._base.storage[shift:]),
        ]

        self.dma = LiteDRAMDMAWriter(dram_port)
        self.submodules += self.dma

        fsm = FSM(reset_state="IDLE")
        self.submodules += fsm

        fsm.act("IDLE",
            self._ready.status.eq(1),
            If(self._start.fields.start,
                NextState("RUN"),
            )
        )

        fsm.act("RUN",
            self.dma.sink.valid.eq(1),
            self._ready.status.eq(0),
            If(self.dma.sink.ready,
                NextState("IDLE"),
            ),
        )

        self.comb += self.dma.sink.address.eq(base + self._offset.storage)
        self.comb += self.dma.sink.data.eq(self._value.storage)
        #self.comb += self.dma.sink.data.eq(0)
