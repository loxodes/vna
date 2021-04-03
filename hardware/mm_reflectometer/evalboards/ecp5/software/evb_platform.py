#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2019 Arnaud Durand <arnaud.durand@unifr.ch>
# SPDX-License-Identifier: BSD-2-Clause

# Modified for custom ecp5 board, Jon Klein, 2021

from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform
from litex.build.lattice.programmer import OpenOCDJTAGProgrammer

import os

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk48",  0, Pins("L16"), IOStandard("LVCMOS33")),
    ("rst_n",  0, Pins("M16"),  IOStandard("LVCMOS33")),

    # Leds
    ("user_led", 0, Pins("A3"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("A4"), IOStandard("LVCMOS33")),

    # Serial
    ("serial", 0,
        Subsignal("rx", Pins("A2"), IOStandard("LVCMOS33")),
        Subsignal("tx", Pins("B3"), IOStandard("LVCMOS33")),
    ),

    # SPIFlash
    ("spiflash", 0,
        Subsignal("cs_n", Pins("N8"), IOStandard("LVCMOS33")),
        Subsignal("mosi",   Pins("T8"), IOStandard("LVCMOS33")),
        Subsignal("miso",   Pins("T7"), IOStandard("LVCMOS33")),
        Subsignal("wp",     Pins("M7"), IOStandard("LVCMOS33")),
        Subsignal("hold",   Pins("N7"), IOStandard("LVCMOS33")),
    ),
    ("spiflash4x", 0,
        Subsignal("cs_n", Pins("N8"),          IOStandard("LVCMOS33")),
        Subsignal("dq",   Pins("T8 T7 M7 N7"), IOStandard("LVCMOS33")),
    ),

    ("hyperram", 0,
        Subsignal("clk_p",   Pins("N5")),
        Subsignal("clk_n",   Pins("N6")),
        Subsignal("rst_n", Pins("N3")),
        Subsignal("dq",    Pins("P4 R3 P5 T4 P6 R5 M5 M6")),
        Subsignal("cs_n",  Pins("R4")),
        Subsignal("rwds",  Pins("P3")),
        IOStandard("LVCMOS18")
    ),
    
    ("usb_aux", 0,
        Subsignal("d_p", Pins("M11")),
        Subsignal("d_n", Pins("N11")),
        Subsignal("pullup", Pins("P12")),
        IOStandard("LVCMOS33")
    ),

    ("adc", 0,
        Subsignal("cs_n", Pins("A15"), IOStandard("LVCMOS33")),
        Subsignal("sck",   Pins("A14"), IOStandard("LVCMOS33")),
        Subsignal("mosi",   Pins("A13"), IOStandard("LVCMOS33")),
    ),

    ("dac", 0,
        Subsignal("clr_n", Pins("B11"), IOStandard("LVCMOS33")),
        Subsignal("sync_n",   Pins("B10"), IOStandard("LVCMOS33")),
        Subsignal("sclk",   Pins("A10"), IOStandard("LVCMOS33")),
        Subsignal("mosi",   Pins("A12"), IOStandard("LVCMOS33")),
        Subsignal("vout_en",   Pins("A11"), IOStandard("LVCMOS33")),
    ),

    ]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("PMOD1",
        "None",  # (no pin 0)
        "K1",    #  1
        "J3",    #  2
        "F2",    #  3
        "E3",    #  4
        "None",  #  5 GND
        "None",  #  6 VCCIO0
        "K2",    #  7 
        "K3",    #  8 
        "E1",    #  9 
        "F3",    # 10 
        "None",  # 11 GND
        "None",  # 12 VCCIO0
    ),



 ]

# Platform -----------------------------------------------------------------------------------------

class Platform(LatticePlatform):
    default_clk_name   = "clk48"
    default_clk_period = 1e9/48e6

    def __init__(self, toolchain="trellis", **kwargs):
        LatticePlatform.__init__(self, "LFE5U-25F-8BG256", _io, _connectors, toolchain=toolchain, **kwargs)

    def request(self, *args, **kwargs):
        return LatticePlatform.request(self, *args, **kwargs)

    def create_programmer(self):
        return OpenOCDJTAGProgrammer("openocd_evn_ecp5.cfg")

    def do_finalize(self, fragment):
        LatticePlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk48",  loose=True), 1e9/48e6)
