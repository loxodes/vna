# jon klein
# tdr gateware

# this is my first attempt at HDL in awhile and my first time using migen
# copying from this is probably a bad idea

# mit license

from migen import *
from migen.fhdl import verilog
from spi import _SPI_TX_Master


class DacController(Module):
    def __init__(self):
        # DAC7563SDSCR dual DAC
        # VoutA - cmp ref
        # VoutB - trig voltage
        # inputs
        self.dac_a = Signal(12)
        self.dac_b = Signal(12)


        self.load = Signal(1)

        # outputs
        self.dac_sdi = Signal(1)
        self.dac_cs = Signal(1)
        self.dac_sck = Signal(1)
        self.dac_clr = Signal(1)
        self.ready = Signal(1)

        # internal
        self.dac_ready = Signal(1)
        self.dac_load = Signal(1)
        self.dac_b_reg = Signal(12)
        self.dac_reg = Signal(24)

        self.state = Signal(3)

        self.startup_delay = Signal(10)


        # hardcode clr to 0
        self.comb += self.dac_clr.eq(0)

        # load dac over spi
        dac_spi = _SPI_TX_Master(24, rising_data = False)
        self.submodules += dac_spi
        self.comb += [
                self.dac_cs.eq(dac_spi.cs),
                self.dac_sck.eq(dac_spi.sck),
                self.dac_sdi.eq(dac_spi.mosi),
                dac_spi.data_in.eq(self.dac_reg),
                dac_spi.load.eq(self.dac_load),
                self.dac_ready.eq(dac_spi.ready)] 


        dacfsm = FSM(reset_state="STARTUP")
        self.submodules += dacfsm
        
        
        dacfsm.act("STARTUP",
            self.state.eq(0),
            NextValue(self.startup_delay, 1000),
            NextState("INIT"),
        )



        dacfsm.act("INIT",
            self.state.eq(1),
            NextValue(self.dac_reg, Cat(0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
            NextValue(self.startup_delay, self.startup_delay - 1),
            If(self.startup_delay == 0,
                NextState("INIT_LOAD"),
            )
            # enabe internal ref, set dac gain to 2
            # [x x][1 1 1][x x x][x....x 1] enable internal ref
        )

        dacfsm.act("INIT_LOAD",
            self.state.eq(2),
            NextState("INIT_WAIT"),
            self.dac_load.eq(1)
        )

        dacfsm.act("INIT_WAIT",
          self.state.eq(3),
          If(self.dac_ready,
                NextState("WAIT_CMD"),
            ).Else(
                NextState("INIT_WAIT"),
            )
        )

        dacfsm.act("WAIT_CMD",
            self.state.eq(4),
            self.ready.eq(1),
            If(self.load,
                NextState("LOAD_DACA"),
                NextValue(self.dac_b_reg, self.dac_b[::-1]),
                NextValue(self.dac_reg, Cat(0, 0, 0, 0, 0, 0, 0, 0, self.dac_a[::-1], 0, 0, 0, 0))
            ).Else(
                NextState("WAIT_CMD")
            )
        )
        

        dacfsm.act("LOAD_DACA",
            self.state.eq(5),
            If(self.dac_ready,
                NextState("WAIT_DACA"),
                self.dac_load.eq(1)
            ).Else(
                NextState("LOAD_DACA"),
            )
        )

        dacfsm.act("WAIT_DACA",
            self.state.eq(6),
            If(self.dac_ready,
                NextState("LOAD_DACB"),
                # [x x][0 0 0][0 0 1][12 bits data, x, x, x, x] # update dac b
                NextValue(self.dac_reg, Cat(0, 0, 0, 0, 0, 0, 0, 1, self.dac_b_reg, 0, 0, 0, 0))

            ).Else(
                NextState("WAIT_DACA"),
            )
        )

        dacfsm.act("LOAD_DACB",
            self.state.eq(7),
            If(self.dac_ready,
                NextState("WAIT_DACB"),
                self.dac_load.eq(1)
            ).Else(
                NextState("LOAD_DACB"),
            )
        )

        dacfsm.act("WAIT_DACB",
            self.state.eq(7),
            If(self.dac_ready,
                NextState("WAIT_CMD"),
            ).Else(
                NextState("WAIT_DACB"),
            )
        )



def dac_test(dut):
    for i in range(130):
        yield

    yield [dut.dac_a.eq(0x03), dut.dac_b.eq(0x777), dut.load.eq(1)]
    yield
    yield [dut.dac_a.eq(0x0), dut.dac_b.eq(0x0), dut.load.eq(0)]
    for i in range(130):
        yield

if __name__ == '__main__':
    dac_dut = DacController()
    run_simulation(dac_dut, dac_test(dac_dut), vcd_name="dac.vcd")
    verilog.convert(DacController()).write("dac.v")

