# script to bit-bang ad9864 initialiation over SPI for fixed 45 MHz IF 
# (use bit-banged SPI, initialization adc initialization only happens once
# save the hardware SPI for more exciting things like controlling the synth)
# currently hardcoded for assuming 26 MHz ref and adc clk

import time
import pdb
from bbone_spi_bitbang import bitbang_spi

def ad9864_write_reg(spi, addr, val):
    payload = addr << 9 | val
    spi.transfer(payload, bits = 16)
    print('readback: ' + str(ad9864_read_reg(spi, addr)) + ' for val: ' + str(val))

def ad9864_read_reg(spi, addr):
    AD9864_READ_MASK = 1 << 15

    payload = addr << 9 | AD9864_READ_MASK;
    response = spi.transfer(payload, bits = 16)

    return response & 0xFF

def ad9864_init(spi):
    ad9864_write_reg(spi, 0x3F, 0x99) # software reset
    ad9864_write_reg(spi, 0x19, 0x87) # 4-wire SPI, 16 bit I/Q

    ad9864_write_reg(spi, 0x00, 0x77) # take ref out of standby

    # lc and rc resonator calibration
    ad9864_write_reg(spi, 0x3E, 0x47)
    ad9864_write_reg(spi, 0x38, 0x01)
    ad9864_write_reg(spi, 0x39, 0x0F)
    time.sleep(.001)    

    for i in range(5):
        ad9864_write_reg(spi, 0x1C, 0x03)
        ad9864_write_reg(spi, 0x00, 0x74)
        time.sleep(.006)
        r = ad9864_read_reg(spi, 0x1C)

        if r == 0:
            print('LC/RC calibration worked!')
            break

        ad9864_write_reg(spi, 0x1C, 0x00)
        print("LC/RC calibration failed, retrying..")

    ad9864_write_reg(spi, 0x38, 0x00)
    ad9864_write_reg(spi, 0x3E, 0x00)

    # lo synth configuration, set LO to 48.25 MHz
    ad9864_write_reg(spi, 0x00, 0x30) # enable everything but ck..
    ad9864_write_reg(spi, 0x08, 0x00)  
    ad9864_write_reg(spi, 0x09, 0x68) # LOR = 104 (so, fif = 250 kHz * (8 LOB + LOA)
    ad9864_write_reg(spi, 0x0A, 0x20) # LOA = 1
    ad9864_write_reg(spi, 0x0B, 0x18) # LOB = 24 (0x18)
    ad9864_write_reg(spi, 0x0C, 0x07) # normal LO charge pump current control


    # configure decimation
    ad9864_write_reg(spi, 0x07, 0x0e) # set decimation rate to 900, 60 * (M + 1) if K = 0, M = 14

    # configure SSI
    ad9864_write_reg(spi, 0x1A, 0x02) # (clkout freq = fclk / 2)
    ad9864_write_reg(spi, 0x18, 0x00) # take fs and clkout out of tristate


if __name__ == '__main__':
    # TODO: pick pins for spi..
    ADC_SPI_CS = "P9_16"
    ADC_SPI_MOSI = "P9_14"
    ADC_SPI_MISO = "P9_18"
    ADC_SPI_CLK = "P9_12"
    # spi clk, spi mosi and spi miso 
    
    spi = bitbang_spi(ADC_SPI_CS, ADC_SPI_MOSI, ADC_SPI_MISO, ADC_SPI_CLK)
    ad9864_init(spi)


