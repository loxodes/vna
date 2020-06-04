export TRELLIS=/usr/share/trellis
#litex_term --serial-boot --kernel soc_basesoc_versa_ecp5/software/bios/bios.bin /dev/ttyUSB1
litex_term --serial-boot --kernel firmware/firmware.bin /dev/ttyUSB3

