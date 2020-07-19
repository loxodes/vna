#!/usr/bin/env python3

# This file is Copyright (c) 2019 Arnaud Durand <arnaud.durand@unifr.ch>
# License: BSD

import os
import argparse

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex_boards.platforms import ecp5_evn
from litex.build.generic_platform import Subsignal, Pins, IOStandard
from litex.build.tools import write_to_file

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.integration import export

from litex.soc.cores.spi import SPIMaster

from litex.soc.cores.led import LedChaser
from litex.soc.cores.uart import UARTWishboneBridge
#from litehyperbus.core.hyperram_ddrx2 import HyperRAMX2
from litehyperbus.core.hyperbus import HyperRAM

from litescope import LiteScopeAnalyzer

from ddr_test import ADC3321_DMA

# CRG ----------------------------------------------------------------------------------------------

class _CRG(Module):
    def __init__(self, platform, sys_clk_freq, x5_clk_freq):
        self.clock_domains.cd_sys = ClockDomain()
        # self.clock_domains.cd_hr2x = ClockDomain()
        # self.clock_domains.cd_hr = ClockDomain()
        # self.clock_domains.cd_hr2x_90 = ClockDomain()
        # self.clock_domains.cd_hr_90 = ClockDomain()
        self.clock_domains.cd_adc_bitclk = ClockDomain()
        self.clock_domains.cd_adc_sampleclk = ClockDomain()
        # # # 
        adc_clks = platform.request("adc_clks")

        # clk / rst
        clk = clk12 = platform.request("clk12")
        rst_n = platform.request("rst_n")
        if x5_clk_freq is not None:
            clk = clk50 = platform.request("ext_clk50")
            self.comb += platform.request("ext_clk50_en").eq(1)
            platform.add_period_constraint(clk50, 1e9/x5_clk_freq)


        # sysclk pll, also generate sample clock
        sampleclk_freq = 25e6
        self.submodules.pll = pll = ECP5PLL()
        self.comb += pll.reset.eq(~rst_n)
        pll.register_clkin(clk, x5_clk_freq or 12e6)
        pll.create_clkout(self.cd_sys, sys_clk_freq)
        pll.create_clkout(self.cd_adc_sampleclk, sampleclk_freq)
        self.comb += adc_clks.sclk.eq(~self.cd_adc_sampleclk.clk)
        self.specials += AsyncResetSynchronizer(self.cd_sys, ~rst_n)

        # bitclk pll
        bitclk_freq = 75e6
        self.submodules.bitclk_pll = bitclk_pll = ECP5PLL()
        platform.add_period_constraint(adc_clks.dclk, 1e9/bitclk_freq)

        self.comb += bitclk_pll.reset.eq(~rst_n)
        bitclk_pll.register_clkin(adc_clks.dclk, bitclk_freq)
        bitclk_pll.create_clkout(self.cd_adc_bitclk, bitclk_freq, phase = 200)#200)


# BaseSoC ------------------------------------------------------------------------------------------
class BaseSoC(SoCCore):
    mem_map = {
        "hyperram" : 0x20000000,
        "adc_sram" : 0x30000000,
    }
    mem_map.update(SoCCore.mem_map)

    def _add_extentions(self, platform):
        platform.add_extension([
            ("serial_wb", 1,
                Subsignal("rx", Pins("E9")),
                Subsignal("tx", Pins("D9")),
                IOStandard("LVCMOS33")
            ),

            ("debug_pins", 1,
                Subsignal("dbg1", Pins("B6")),
                Subsignal("dbg2", Pins("C9")),
                Subsignal("dbg3", Pins("D10")),
                IOStandard("LVCMOS33")
            ),

            ("adc_data", 0,
                Subsignal("da0", Pins("A4")), # INVERTED
                Subsignal("da1", Pins("B5")), # INVERTED
                Subsignal("db0", Pins("E4")), # INVERTED
                Subsignal("db1", Pins("C3")), # INVERTED
                Subsignal("fclk", Pins("A3")), # INVERTED
                Subsignal("sysref", Pins("E5")), # INVERTED
                IOStandard("LVDS")
            ),

            ("adc_spi", 1,
                Subsignal("clk",   Pins("C6")),
                Subsignal("mosi", Pins("C7")),
                Subsignal("cs_n",    Pins("E8")),
                Subsignal("miso",  Pins("D8")),
                IOStandard("LVCMOS33")
            ),

            ("adc_ctrl", 0,
                Subsignal("en_pwr",  Pins("A7")),
                Subsignal("pdn",  Pins("C8")),
                Subsignal("reset",  Pins("B8")),
                IOStandard("LVCMOS33")
            ),

            ("adc_clks", 0,
                Subsignal("dclk", Pins("C4")), # INVERTED...
                Subsignal("sclk", Pins("F4")), # INVERTED
                IOStandard("LVDS")
            ),

            ("hyperram", 0,
                Subsignal("clk",   Pins("B13")),
                Subsignal("rst_n", Pins("C15")),
                Subsignal("dq",    Pins("D11 C12 E11 B12 E12 C13 D13 D12")),
                Subsignal("cs_n",  Pins("B15")),
                Subsignal("rwds",  Pins("B20")),
                IOStandard("LVCMOS33")
            ),
        ])

    def __init__(self, sys_clk_freq=int(50e6), x5_clk_freq=None, toolchain="trellis", **kwargs):
        from litex.build.generic_platform import Subsignal, Pins, IOStandard
        platform = ecp5_evn.Platform(toolchain=toolchain)
        self._add_extentions(platform)

        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, clk_freq=sys_clk_freq, integrated_main_ram_size=0x8000, **kwargs)

        # CRG --------------------------------------------------------------------------------------
        crg = _CRG(platform, sys_clk_freq, x5_clk_freq)
        self.submodules.crg = crg

        # HyperRam ---------------------------------------------------------------------------------
        self.submodules.hyperram = HyperRAM(platform.request("hyperram"))
        #self.submodules.hyperram = HyperRAMX2(platform.request("hyperram"))

        self.add_wb_slave(self.mem_map["hyperram"], self.hyperram.bus)
        self.add_memory_region("hyperram", self.mem_map["hyperram"], 8*1024*1024)

        # ADC RAM
        self.add_ram("adc_sram", self.mem_map["adc_sram"], 8*4*4096)

        # ADC --------------------------------------------------------------------------------------
        adc_ctrl = platform.request("adc_ctrl", 0)
        adc_data = platform.request("adc_data", 0)

        self.add_csr("adc")
        self.submodules.adc = ADC3321_DMA(adc_ctrl, adc_data)
        self.add_wb_master(self.adc.wishbone)


        # Leds -------------------------------------------------------------------------------------
        self.submodules.leds = LedChaser(
            pads         = Cat(*[platform.request("user_led", i) for i in range(8)]),
            sys_clk_freq = sys_clk_freq)
        self.add_csr("leds")

        # ADC SPI bus ------------------------------------------------------------------------------
        # max SPI frequency is 20 MHz
        self.add_csr("adc_spi")
        self.submodules.adc_spi = SPIMaster(platform.request("adc_spi",1), 24, sys_clk_freq, int(sys_clk_freq/80), with_csr=True)

        # Wishbone Debug
        # added io to platform, serial_wb
        self.submodules.bridge = UARTWishboneBridge(platform.request("serial_wb",1), sys_clk_freq, baudrate=3000000)
        self.add_wb_master(self.bridge.wishbone)
        self.add_csr("analyzer")
        analyzer_signals = [
 #           self.adc.adc_frontend.adc_buffer.adc_dout0,
 #           self.adc.adc_frontend.adc_buffer.adc_dout1,
 #           self.adc.adc_frontend.adc_buffer.i_fclk,
           self.adc.adc_frontend_a.i_we,
#            self.adc.adc_frontend.i_re,
#            self.adc.adc_frontend.o_readable,
 #           self.adc.adc_frontend.adc_buffer.o_dout,
 #           self.adc.adc_frontend.adc_buffer.pulser.output,
 #           self.adc.adc_frontend.adc_buffer.fifo.din,
 #           self.adc.adc_frontend.o_dout,
        ]

        #t = Signal()
        #self.comb += [t.eq(clk_outputs.hr_p)]

        analyzer_depth = 512 # samples
        analyzer_clock_domain = "sys"
        self.submodules.analyzer = LiteScopeAnalyzer(analyzer_signals,
                                                     analyzer_depth,
                                                     clock_domain=analyzer_clock_domain)


        # put pulser on pin..
        debug_pins  = platform.request("debug_pins")
        self.comb += debug_pins.dbg1.eq(self.adc.adc_frontend_a.adc_buffer.pulser.output)
        

# Build --------------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="LiteX SoC on ECP5 Evaluation Board")
    parser.add_argument("--build", action="store_true", help="Build bitstream")
    parser.add_argument("--load",  action="store_true", help="Load bitstream")
    parser.add_argument("--toolchain", default="trellis", help="Gateware toolchain to use, trellis (default) or diamond")
    builder_args(parser)
    soc_core_args(parser)
    parser.add_argument("--sys-clk-freq", default=60e6, help="System clock frequency (default=60MHz)")
    parser.add_argument("--x5-clk-freq",  type=int,     help="Use X5 oscillator as system clock at the specified frequency")
    args = parser.parse_args()

    soc = BaseSoC(toolchain=args.toolchain,
        sys_clk_freq = int(float(args.sys_clk_freq)),
        x5_clk_freq  = args.x5_clk_freq,
        **soc_core_argdict(args))
    builder = Builder(soc, **builder_argdict(args))
    vns = builder.build(run=args.build)

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(os.path.join(builder.gateware_dir, soc.build_name + ".svf"))

    csr_csv = export.get_csr_csv(soc.csr_regions, soc.constants)
    write_to_file("test/csr.csv", csr_csv)
    soc.analyzer.export_csv(vns, "test/analyzer.csv") # Export the current analyzer configuration

if __name__ == "__main__":
    main()
