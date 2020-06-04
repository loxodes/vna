# driver for ad7984 adc

# https://www.analog.com/media/en/technical-documentation/data-sheets/AD7984.pdf

from migen import *
from migen.genlib.cdc import MultiReg

from litex.soc.interconnect.csr import *
from litedram.frontend.dma import LiteDRAMDMAWriter
from litedram.common import LiteDRAMNativePort


# X4 pin 10, SDI
# X4 pin 11, SCK
# X4 pin 12, SDO
# X4 pin 13, CNV

#    ("adc_test", 1,
#        Subsignal("sdi", Pins("C14")),
#        Subsignal("sck", Pins("D14")),
#        Subsignal("sdo", Pins("E14")),
#        Subsignal("cnv", Pins("D11")),
#        IOStandard("LVCMOS33")
#    ),


# TODO: slow down readback clock..
class AD7984Core(Module, AutoCSR):
    def __init__(self, dram_port, adc_pins):
        self._start = CSRStorage(fields=[CSRField("start_burst", size=1, offset=0, pulse=True)])
        self._ready = CSRStatus(8)
        self._base = CSRStorage(32)
        self._offset = CSRStorage(32)

        self.sample_index = Signal(11)
    
        SAMPLE_BUFFER = 1024
        ADC_BITS = 18

        base = Signal(dram_port.address_width)
        offset = Signal(dram_port.address_width)

        # determine the first significant bit of an byte address in memory
        shift = log2_int(dram_port.data_width//8)
        self.comb += [
            base.eq(self._base.storage[shift:]),
        ]
        self.dma = LiteDRAMDMAWriter(dram_port)
        self.submodules += self.dma



        # hook up pins of ADC 
        self.adc_sdi = Signal()
        self.adc_sck = Signal()
        self.adc_sdo = Signal()
        self.adc_cnv = Signal()
        
        self.comb += adc_pins.sdi.eq(self.adc_sdi)
        self.comb += adc_pins.sck.eq(self.adc_sck)
        self.comb += self.adc_sdo.eq(adc_pins.sdo)
        self.comb += adc_pins.cnv.eq(self.adc_cnv)

        adc_value = Signal(ADC_BITS)
        cnv_settle = Signal(10)

        self.comb += self.dma.sink.address.eq(base + self._offset.storage + self.sample_index)
        self.comb += self.dma.sink.data.eq(adc_value)
        #self.comb += self.dma.sink.data.eq(self.sample_index)


        # divide system clock by adc_clk_divisor * 2 
        self.cnv_strobe = Signal(12)
        cnv_clk_divisor = 1000

        self.sync += \
            If(self.cnv_strobe == 0,
                self.cnv_strobe.eq(cnv_clk_divisor - 1),
            ).Else(
                self.cnv_strobe.eq(self.cnv_strobe - 1),
            )


        # divide system 20 for spi clock
        self.spi_strobe = Signal(5)
        spi_clk_divisor = 10

        self.sync += \
            If(self.spi_strobe == 0,
                self.spi_strobe.eq(spi_clk_divisor - 1),
            ).Else(
                self.spi_strobe.eq(self.spi_strobe - 1),
            )


        self.adc_bit = Signal(5)

        adc_fsm = FSM(reset_state="INIT")
        self.submodules += adc_fsm 

        # wait for a start pulse
        adc_fsm.act("INIT",
            NextValue(self.sample_index, 0),
            self._ready.status.eq(1),

            If(self._start.fields.start_burst,
                NextState("CNV_PREPARE"),
            ),
        )

        # prepare for conversion
        adc_fsm.act("CNV_PREPARE",
            self.adc_cnv.eq(0),
            NextValue(self.adc_bit, 0),
            If(self.cnv_strobe == 0,
                If(self.sample_index == SAMPLE_BUFFER,
                    NextState("INIT"),
                ).Else(
                    NextState("CNV_START"),
                ),
            ).Else(
                NextState("CNV_PREPARE"),
            )
        )
        
        # start conversion 
        adc_fsm.act("CNV_START",
            self.adc_cnv.eq(1),
            NextValue(cnv_settle, 100), # max tcnv is 500 ns, max flck is ~50 MHz. so, 100 cycles should do it
            NextState("CNV_WAIT"),
        )

        # wait for conversion to end
        adc_fsm.act("CNV_WAIT",
            self.adc_cnv.eq(1),
            NextValue(cnv_settle, cnv_settle -1),
            # eventually, work off ready signal?
            #If(self.adc_sdo == 0,
            #    NextState("ACQ_INIT")
            #)

            If(cnv_settle == 0,
                NextState("ACQ_INIT"),
            ),
        )
       
        # start acquisition
        adc_fsm.act("ACQ_INIT",
            self.adc_cnv.eq(0),
            NextValue(self.adc_bit, 0),
            If(self.spi_strobe == 0,
                NextState("ACQ_CLKH"),
            ),
        ) 

        # capture ADC_BITS + 1 bits
        # read data on rising edg eof sck
        adc_fsm.act("ACQ_CLKH",
            self.adc_sck.eq(1),
            self.adc_cnv.eq(0),
            If(self.spi_strobe == 0,
                NextValue(adc_value, (adc_value << 1) + self.adc_sdo),
                NextState("ACQ_CLKL"),
            ),
        )

        adc_fsm.act("ACQ_CLKL",
            self.adc_sck.eq(0),
            self.adc_cnv.eq(0),
            If(self.spi_strobe == 0,
                If(self.adc_bit == ADC_BITS,
                    NextValue(self.sample_index, self.sample_index+1),
                    NextState("ACQ_END"),
                    self.dma.sink.valid.eq(1),
                ).Else(
                    NextState("ACQ_CLKH"),
                    NextValue(self.adc_bit, self.adc_bit + 1),

                )
            )

        )

        adc_fsm.act("ACQ_END",
            self.adc_cnv.eq(0),
            If(self.spi_strobe == 0,
                NextState("CNV_PREPARE"),
            ),
        )

