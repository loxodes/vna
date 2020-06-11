#!/usr/bin/env python3

# This file is Copyright (c) 2019 Arnaud Durand <arnaud.durand@unifr.ch>
# License: BSD

import os
import argparse

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex_boards.platforms import ecp5_evn
from litex.build.tools import write_to_file

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.integration import export

from litex.soc.cores.led import LedChaser
from litex.soc.cores.uart import UARTWishboneBridge
#from litehyperbus.core.hyperram_ddrx2 import HyperRAMX2
from litehyperbus.core.hyperbus import HyperRAM

from litescope import LiteScopeAnalyzer

from ddr_test import ADC3321_DMA

# CRG ----------------------------------------------------------------------------------------------

class _CRG(Module):
    def __init__(self, platform, sys_clk_freq, x5_clk_freq, clk_pins):
        self.clock_domains.cd_sys = ClockDomain()
        self.clock_domains.cd_hr2x = ClockDomain()
        self.clock_domains.cd_hr = ClockDomain()
        self.clock_domains.cd_hr2x_90 = ClockDomain()
        self.clock_domains.cd_hr_90 = ClockDomain()
        self.clock_domains.cd_adc_bitclk = ClockDomain()
        # # # 

        # clk / rst
        clk = clk12 = platform.request("clk12")
        rst_n = platform.request("rst_n")
        if x5_clk_freq is not None:
            clk = clk50 = platform.request("ext_clk50")
            self.comb += platform.request("ext_clk50_en").eq(1)
            platform.add_period_constraint(clk50, 1e9/x5_clk_freq)

        # add external clock for

        # - hr2x    : 2* sys_freq - I/O clock
        # - hr      : sys_freq    - core clock
        # - hr2x_90 : 2* sys_freq - phase shifted clock output to HyperRAM
        # - hr_90   : sys_freq    - phase shifted clock for SCLK

        # pll
        self.submodules.pll = pll = ECP5PLL()
        self.comb += pll.reset.eq(~rst_n)
        pll.register_clkin(clk, x5_clk_freq or 12e6)
        pll.create_clkout(self.cd_hr2x_90, sys_clk_freq*2, phase=90)
        pll.create_clkout(self.cd_hr2x, sys_clk_freq*2)


        # TODO: 
        # create differential LVDS output for clock signals
        # create clock input from ADC board, route to PLL
        # stuff those back out to outputs
        
        # clk / rst
        ADC_CLK_FREQ = 40e6
        
        ext_clk = clk_pins.clk_in
        platform.add_period_constraint(ext_clk, 1e9/ADC_CLK_FREQ)
        self.submodules.adcpll = adcpll = ECP5PLL()
        self.comb += adcpll.reset.eq(~rst_n)
        adcpll.register_clkin(ext_clk, ADC_CLK_FREQ)
        adcpll.create_clkout(self.cd_adc_bitclk, ADC_CLK_FREQ*3.5)



        self.specials += Instance("CLKDIVF",
                p_DIV     = "2.0",
                i_ALIGNWD = 0,
                i_CLKI    = self.cd_hr2x.clk,
                i_RST     = self.cd_hr2x.rst,
                o_CDIVX   = self.cd_hr.clk)

        self.specials += Instance("CLKDIVF",
                p_DIV     = "2.0",
                i_ALIGNWD = 0,
                i_CLKI    = self.cd_hr2x_90.clk,
                i_RST     = self.cd_hr2x_90.rst,
                o_CDIVX   = self.cd_hr_90.clk)

        self.comb += self.cd_sys.clk.eq(self.cd_hr.clk)

        self.specials += AsyncResetSynchronizer(self.cd_sys, ~rst_n)

# BaseSoC ------------------------------------------------------------------------------------------
class BaseSoC(SoCCore):
    mem_map = {
        "hyperram" : 0x20000000,
    }
    mem_map.update(SoCCore.mem_map)

    def __init__(self, sys_clk_freq=int(50e6), x5_clk_freq=None, toolchain="trellis", **kwargs):
        platform = ecp5_evn.Platform(toolchain=toolchain)
        clk_pins = platform.request("clk_output")
        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, clk_freq=sys_clk_freq, integrated_main_ram_size=0x8000, **kwargs)

        # CRG --------------------------------------------------------------------------------------
        crg = _CRG(platform, sys_clk_freq, x5_clk_freq, clk_pins)
        self.submodules.crg = crg

        # HyperRam ---------------------------------------------------------------------------------
        self.submodules.hyperram = HyperRAM(platform.request("hyperram"))
#        self.submodules.hyperram = HyperRAMX2(platform.request("hyperram"))
#        self.add_wb_slave(self.mem_map["hyperram"], self.hyperram.bus)
#        self.add_memory_region("hyperram", self.mem_map["hyperram"], 8*1024*1024)


        # ADC --------------------------------------------------------------------------------------
        trig_pad = platform.request("adc_trig", 0)
        self.submodules.adc = ADC3321_DMA(trig_pad)
        self.add_wb_master(self.adc.wishbone)
        self.add_csr("adc")

        # Leds -------------------------------------------------------------------------------------
        self.submodules.leds = LedChaser(
            pads         = Cat(*[platform.request("user_led", i) for i in range(8)]),
            sys_clk_freq = sys_clk_freq)
        self.add_csr("leds")

        # Wishbone Debug
        # added io to platform, serial_wb
        self.submodules.bridge = UARTWishboneBridge(platform.request("serial_wb",1), sys_clk_freq, baudrate=115200)
        self.add_wb_master(self.bridge.wishbone)


        self.add_csr("analyzer")
        analyzer_signals = [
            trig_pad,
            # self.hyperram.bus.stb,
            # self.hyperram.bus.ack,
            # self.hyperram.bus.we,
            # self.hyperram.pads.cs_n,
            # self.hyperram.pads.clk,
            # self.hyperram.rwds_copy,
            # self.hyperram.rwds_input,
            # self.hyperram.dq_copy,
        ]

        self.comb += [
            clk_pins.hr.eq(crg.cd_hr.clk),
            clk_pins.clk_out.eq(crg.cd_adc_bitclk.clk),
 #           clk_outputs.hr2x.eq(crg.cd_hr2x.clk),
 #           clk_outputs.hr90.eq(crg.cd_hr_90.clk),
 #           clk_outputs.hr2x90.eq(crg.cd_hr2x_90.clk),
        ]

        #t = Signal()
        #self.comb += [t.eq(clk_outputs.hr_p)]

        analyzer_depth = 256 # samples
        analyzer_clock_domain = "sys"
        self.submodules.analyzer = LiteScopeAnalyzer(analyzer_signals,
                                                     analyzer_depth,
                                                     clock_domain=analyzer_clock_domain)

# Build --------------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="LiteX SoC on ECP5 Evaluation Board")
    parser.add_argument("--build", action="store_true", help="Build bitstream")
    parser.add_argument("--load",  action="store_true", help="Load bitstream")
    parser.add_argument("--toolchain", default="trellis", help="Gateware toolchain to use, trellis (default) or diamond")
    builder_args(parser)
    soc_core_args(parser)
    parser.add_argument("--sys-clk-freq", default=40e6, help="System clock frequency (default=60MHz)")
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
