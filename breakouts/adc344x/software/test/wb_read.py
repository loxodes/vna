#!/usr/bin/env python3
from litex.tools.litex_client import RemoteClient
import time

wb = RemoteClient()
wb.open()

wb.write(0x82002800, 0x77)
time.sleep(1)
wb.write(0x82002800, 0)
time.sleep(1)
wb.write(0x82002800, 0x77)

#for i in range(6):
#    print(wb.read(0x08000000+4*i))


wb.close()
