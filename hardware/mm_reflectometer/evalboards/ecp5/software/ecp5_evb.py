#!/usr/bin/env python3

#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2019 Arnaud Durand <arnaud.durand@unifr.ch>
# SPDX-License-Identifier: BSD-2-Clause

# Modified for custom ecp5 board, Jon Klein, 2021

import os
import argparse

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

import evb_platform

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.led import LedChaser
from litehyperbus.core.hyperbus import HyperRAM
from litex.soc.cores.spi_flash import ECP5SPIFlash
import sys


# CRG ----------------------------------------------------------------------------------------------

class _CRG(Module):
    def __init__(self, platform, sys_clk_freq):
        self.rst = Signal()
        self.clock_domains.cd_sys = ClockDomain()
        self.clock_domains.cd_usb_12 = ClockDomain()
        self.clock_domains.cd_usb_48 = ClockDomain()
        # # #

        # clk / rst
        clk = platform.request("clk48")
        rst_n = platform.request("rst_n")
    
        # pll
        self.submodules.pll = pll = ECP5PLL()
        self.comb += pll.reset.eq(~rst_n | self.rst)
        pll.register_clkin(clk, 48e6)
        pll.create_clkout(self.cd_sys, sys_clk_freq)

        # usb 12 MHz
        self.submodules.pll_12 = pll_12 = ECP5PLL()
        self.comb += pll_12.reset.eq(~rst_n | self.rst)
        pll_12.register_clkin(clk, 48e6)
        pll_12.create_clkout(self.cd_usb_12, int(12e6))

        # usb 48 MHz
        self.comb += self.cd_usb_48.clk.eq(clk)
        self.comb += self.cd_usb_48.rst.eq(~rst_n | self.rst)

# BaseSoC ------------------------------------------------------------------------------------------

class BaseSoC(SoCCore):
    def __init__(self, sys_clk_freq=int(48e6), x5_clk_freq=None, toolchain="trellis", **kwargs):
        platform = evb_platform.Platform(toolchain=toolchain)

        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, sys_clk_freq,
            ident          = "LiteX SOC on @loxodes ECP5 Evaluation Board",
            ident_version  = True,
            **kwargs)

        # CRG --------------------------------------------------------------------------------------
        crg = _CRG(platform, sys_clk_freq)
        self.submodules.crg = crg

        # HyperRam ---------------------------------------------------------------------------------
        self.mem_map["hyperram"] = 0x20000000
        self.submodules.hyperram = HyperRAM(platform.request("hyperram"))
        self.add_wb_slave(self.mem_map["hyperram"], self.hyperram.bus)
        self.add_memory_region("hyperram", self.mem_map["hyperram"], 8*1024*1024)

        # SPIFlash ---------------------------------------------------------------------------------
        self.submodules.spiflash = ECP5SPIFlash(
            pads         = platform.request("spiflash"),
            sys_clk_freq = sys_clk_freq,
            spi_clk_freq = 5e6,
        )
        self.add_csr("spiflash")

        # Wishbone  usb debug port
        # see https://gist.github.com/enjoy-digital/82ed88b77ef0b1e3e91b0592e44eaa14
        os.system("git clone https://github.com/litex-hub/valentyusb -b hw_cdc_eptri")
        sys.path.append("valentyusb")
        from valentyusb.usbcore.cpu import dummyusb, epfifo
        from valentyusb.usbcore import io as usbio
        usb_debug = True
        usb_pads = platform.request("usb_aux")
        usb_iobuf = usbio.IoBuf(usb_pads.d_p, usb_pads.d_n, usb_pads.pullup)
        self.submodules.usb = dummyusb.DummyUsb(usb_iobuf, debug=usb_debug)#epfifo.PerEndpointFifoInterface(usb_iobuf, debug=usb_debug)
        self.add_wb_master(self.usb.debug_bridge.wishbone)
        #self.register_mem("vexriscv_debug", 0xf00f0000, self.cpu.debug_bus, 0x100)
        # https://github.com/enjoy-digital/litex/issues/345
        # Leds -------------------------------------------------------------------------------------
        self.submodules.leds = LedChaser(
            pads         = platform.request_all("user_led"),
            sys_clk_freq = sys_clk_freq)
        self.add_csr("leds")

# Build --------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LiteX SoC on ECP5 Evaluation Board")
    parser.add_argument("--build",        action="store_true", help="Build bitstream")
    parser.add_argument("--load",         action="store_true", help="Load bitstream")
    parser.add_argument("--flash",        action="store_true", help="Flash bitstream")
    parser.add_argument("--toolchain",    default="trellis",   help="FPGA toolchain: trellis (default) or diamond")
    parser.add_argument("--sys-clk-freq", default=60e6,        help="System clock frequency (default: 60MHz)")
    builder_args(parser)
    soc_core_args(parser)
    args = parser.parse_args()

    soc = BaseSoC(toolchain=args.toolchain,
        sys_clk_freq = int(float(args.sys_clk_freq)),
        **soc_core_argdict(args))
    builder = Builder(soc, **builder_argdict(args))
    builder.build(run=args.build)

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(os.path.join(builder.gateware_dir, soc.build_name + ".svf"))

    if args.flash:
        prog = soc.platform.create_programmer()
        os.system("cp bit_to_flash.py build/evb_platform/gateware/")
        # use bits_to_flash from https://github.com/enjoy-digital/colorlite
        os.system("cd build/evb_platform/gateware && ./bit_to_flash.py evb_platform.bit evb_platform.flash.svf")
        prog.load_bitstream(os.path.join(builder.gateware_dir, soc.build_name + ".flash.svf"))

if __name__ == "__main__":
    main()
