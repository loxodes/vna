from migen import *
from migen.fhdl import verilog

# so, NB6L295M latches data on the rising edge
# DAC7563SDSCR latches data on the falling edge

# add clock strobe to divide down spi clock

class _SPI_TX_Master(Module):
    def __init__(self, width, rising_data = False):
        # outputs
        self.sck = Signal()
        self.mosi = Signal()
        self.cs = Signal()
        self.ready = Signal()
        
        # inputs
        self.data_in = Signal(width)
        self.load = Signal()

        # internal
        self.data_reg = Signal(width)
        self.bit_count = Signal(5)
        
        # divide system clock by spi_clk_divisor * 2 
        self.spi_strobe = Signal(10)
        spi_clk_divisor = 20
        self.sync += \
            If(self.spi_strobe == 0,
                self.spi_strobe.eq(spi_clk_divisor - 1),
            ).Else(
                self.spi_strobe.eq(self.spi_strobe - 1),
            )

    
        # logic
        spifsm = FSM(reset_state="INIT")
        self.submodules += spifsm

        spifsm.act("INIT",
            self.cs.eq(1),
            self.sck.eq(0),
            self.ready.eq(1),
            NextValue(self.bit_count, 0),
            If(self.load,
                NextValue(self.data_reg, self.data_in),
                NextState("SETUP")
            ).Else(
                NextState("INIT")
            )
        )
       
        self.comb += self.mosi.eq(self.data_reg[0])

        spifsm.act("WAIT",
            self.cs.eq(1),
            self.sck.eq(0),
            If(self.spi_strobe == 0,
                NextState("DATA_CLKH")
            )
        )

        spifsm.act("SETUP",
            self.cs.eq(0),
            self.sck.eq(1),
            If(self.spi_strobe == 0,
                NextState("DATA_CLKH")
            )
        )

        spifsm.act("DATA_CLKH",
            self.cs.eq(0),
            self.sck.eq(1),
            If(self.spi_strobe == 0,
                NextState("DATA_CLKL")
            )
        )

        spifsm.act("DATA_CLKL",
            self.cs.eq(0),
            self.sck.eq(0),
            If(self.spi_strobe == 0,
                NextValue(self.data_reg, self.data_reg >> 1),
                NextValue(self.bit_count, self.bit_count +1),
                If(self.bit_count != width - 1,
                    NextState("DATA_CLKH")
                ).Else(
                    NextState("POST")
                )
            )

        )

        spifsm.act("POST",
            self.cs.eq(1),
            self.sck.eq(0),
            If(self.spi_strobe == 0,
                NextState("INIT")
            )
        )

def spi_test(dut):
    yield dut.data_in.eq(0x33)
    yield dut.load.eq(0)
    yield 
    yield dut.load.eq(1)
    yield
    yield dut.load.eq(0)
    for i in range(30):
        yield

    yield dut.data_in.eq(0x11)
    yield dut.load.eq(1)
    for i in range(30):
        yield



if __name__ == "__main__":
    dut = _SPI_TX_Master(10)
    run_simulation(dut, spi_test(dut), vcd_name="spi.vcd")
    verilog.convert(_SPI_TX_Master(10)).write("spi.v")
