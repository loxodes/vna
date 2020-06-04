#!/usr/bin/env python3

# This file is Copyright (c) 2018-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# This file is Copyright (c) 2018-2019 David Shah <dave@ds0.me>
# License: BSD

import argparse

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex_boards.platforms import versa_ecp5

from litex.build.lattice.trellis import trellis_args, trellis_argdict
from litex.build.tools import write_to_file

from litex.soc.cores.clock import *
from litex.soc.cores.gpio import *
from litex.soc.integration.soc_sdram import *
from litex.soc.integration.builder import *
from litex.soc.integration import export

from litex.soc.cores.uart import UARTWishboneBridge
from litex.soc.cores.spi import SPIMaster
from litescope import LiteScopeAnalyzer

from litedram.modules import MT41K64M16
from litedram.phy import ECP5DDRPHY
from litedram.frontend.dma import LiteDRAMDMAReader
from litedram.frontend.dma import LiteDRAMDMAWriter

from liteeth.phy.ecp5rgmii import LiteEthPHYRGMII
from liteeth.mac import LiteEthMAC

from memtest import MemtestCore
from dac7563 import DAC7563Core
from ad7984 import AD7984Core 

# CRG ----------------------------------------------------------------------------------------------

class _CRG(Module):
    def __init__(self, platform, sys_clk_freq):
        self.clock_domains.cd_init    = ClockDomain()
        self.clock_domains.cd_por     = ClockDomain(reset_less=True)
        self.clock_domains.cd_sys     = ClockDomain()
        self.clock_domains.cd_sys2x   = ClockDomain()
        self.clock_domains.cd_sys2x_i = ClockDomain(reset_less=True)

        # # #

        self.stop = Signal()

        # Clk / Rst
        clk100 = platform.request("clk100")
        rst_n  = platform.request("rst_n")
        platform.add_period_constraint(clk100, 1e9/100e6)

        # Power on reset
        por_count = Signal(16, reset=2**16-1)
        por_done  = Signal()
        self.comb += self.cd_por.clk.eq(ClockSignal())
        self.comb += por_done.eq(por_count == 0)
        self.sync.por += If(~por_done, por_count.eq(por_count - 1))

        # PLL
        self.submodules.pll = pll = ECP5PLL()
        pll.register_clkin(clk100, 100e6)
        pll.create_clkout(self.cd_sys2x_i, 2*sys_clk_freq)
        pll.create_clkout(self.cd_init, 25e6)
        self.specials += [
            Instance("ECLKSYNCB",
                i_ECLKI = self.cd_sys2x_i.clk,
                i_STOP  = self.stop,
                o_ECLKO = self.cd_sys2x.clk),
            Instance("CLKDIVF",
                p_DIV     = "2.0",
                i_ALIGNWD = 0,
                i_CLKI    = self.cd_sys2x.clk,
                i_RST     = self.cd_sys2x.rst,
                o_CDIVX   = self.cd_sys.clk),
            AsyncResetSynchronizer(self.cd_init, ~por_done | ~pll.locked | ~rst_n),
            AsyncResetSynchronizer(self.cd_sys,  ~por_done | ~pll.locked | ~rst_n)
        ]



# BaseSoC ------------------------------------------------------------------------------------------

class BaseSoC(SoCSDRAM):
    def __init__(self, sys_clk_freq=int(75e6), toolchain="diamond", integrated_rom_size=0x8000, **kwargs):
        platform = versa_ecp5.Platform(toolchain=toolchain)

        # SoCSDRAM ---------------------------------------------------------------------------------
        SoCSDRAM.__init__(self, platform, clk_freq=sys_clk_freq,
            integrated_rom_size=integrated_rom_size,
            **kwargs)

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform, sys_clk_freq)


        # https://github.com/enjoy-digital/litex/issues/234
        # https://github.com/enjoy-digital/litex/blob/master/litex/soc/cores/gpio.py
        # /repos/litex/litex-boards/litex_boards/official/platforms/versa_ecp5.py
        self.add_csr("gpio_leds")
        self.submodules.gpio_leds = GPIOOut(Cat([platform.request("user_led", i) for i in range(8)]))


        # add spi master, from ~/repos/litex/litex/litex/soc/cores
        self.add_csr("spi_test")
        spi_test = SPIMaster(platform.request("spi_test",1), 8, sys_clk_freq, int(sys_clk_freq/5))
        self.submodules.spi_test = spi_test

    
        self.add_csr("dac_test")
        dac_test = DAC7563Core(platform.request("dac_test",1))
        self.submodules.dac_test = dac_test

        # https://github.com/timvideos/litex-buildenv/wiki/LiteX-for-Hardware-Engineers litescope bridge
        # added io to platform, serial_wb
        self.submodules.bridge = UARTWishboneBridge(platform.request("serial_wb",1), sys_clk_freq, baudrate=115200)
        self.add_wb_master(self.bridge.wishbone)
        

        # DDR3 SDRAM -------------------------------------------------------------------------------
        if not self.integrated_main_ram_size:
            print("creating DDR3 SDRAM")
            self.submodules.ddrphy = ECP5DDRPHY(
                platform.request("ddram"),
                sys_clk_freq=sys_clk_freq)
            self.add_csr("ddrphy")
            self.add_constant("ECP5DDRPHY", None)
            self.comb += self.crg.stop.eq(self.ddrphy.init.stop)
            sdram_module = MT41K64M16(sys_clk_freq, "1:2")
            self.register_sdram(self.ddrphy,
                geom_settings   = sdram_module.geom_settings,
                timing_settings = sdram_module.timing_settings)

            self.add_csr("memory_test")
            memory_test = MemtestCore(self.sdram.crossbar.get_port())
            self.submodules.memory_test = memory_test
  
            self.add_csr("adc_test")
            adc_test = AD7984Core(self.sdram.crossbar.get_port(), platform.request("adc_test",1))
            self.submodules.adc_test = adc_test
      
            # litescope, track spi
            self.add_csr("analyzer")
            analyzer_signals = [
                dac_test.dac.dac_load,
                dac_test._load.fields.load,
                dac_test.dac.load,
                dac_test.dac.dac_cs,
                dac_test.dac.dac_sck,
                dac_test.dac.dac_sdi,
                dac_test.dac.dac_ready,
                dac_test.dac.state,
            ]

            analyzer_depth = 256 # samples
            analyzer_clock_domain = "sys"
            self.submodules.analyzer = LiteScopeAnalyzer(analyzer_signals,
                                                         analyzer_depth,
                                                         clock_domain=analyzer_clock_domain)



# EthernetSoC --------------------------------------------------------------------------------------

class EthernetSoC(BaseSoC):
    mem_map = {
        "ethmac": 0xb0000000,
    }
    mem_map.update(BaseSoC.mem_map)

    def __init__(self, toolchain="diamond", **kwargs):
        BaseSoC.__init__(self, toolchain=toolchain, integrated_rom_size=0x10000, **kwargs)

        self.submodules.ethphy = LiteEthPHYRGMII(
            self.platform.request("eth_clocks"),
            self.platform.request("eth"))
        self.add_csr("ethphy")
        self.submodules.ethmac = LiteEthMAC(phy=self.ethphy, dw=32,
            interface="wishbone", endianness=self.cpu.endianness)
        self.add_wb_slave(self.mem_map["ethmac"], self.ethmac.bus, 0x2000)
        self.add_memory_region("ethmac", self.mem_map["ethmac"], 0x2000, type="io")
        self.add_csr("ethmac")
        self.add_interrupt("ethmac")

        self.platform.add_period_constraint(self.ethphy.crg.cd_eth_rx.clk, 1e9/125e6)
        self.platform.add_period_constraint(self.ethphy.crg.cd_eth_tx.clk, 1e9/125e6)

# Build --------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LiteX SoC on Versa ECP5")
    parser.add_argument("--gateware-toolchain", dest="toolchain", default="trellis",
        help='gateware toolchain to use, trellis (default)')
    builder_args(parser)
    soc_sdram_args(parser)
    trellis_args(parser)
    parser.add_argument("--sys-clk-freq", default=75e6,
                        help="system clock frequency (default=75MHz)")
    parser.add_argument("--with-ethernet", action="store_true",
                        help="enable Ethernet support")
    args = parser.parse_args()

    cls = EthernetSoC if args.with_ethernet else BaseSoC
    soc = cls(toolchain=args.toolchain, sys_clk_freq=int(float(args.sys_clk_freq)), **soc_sdram_argdict(args))
    builder = Builder(soc, **builder_argdict(args))
    builder_kargs = {}
    if args.toolchain == "trellis":
        builder_kargs == trellis_argdict(args)
    
    vns = builder.build(**builder_kargs)
     
    csr_csv = export.get_csr_csv(soc.csr_regions, soc.constants)
    write_to_file("test/csr.csv", csr_csv)
    soc.analyzer.export_csv(vns, "test/analyzer.csv") # Export the current analyzer configuration


if __name__ == "__main__":
    main()
