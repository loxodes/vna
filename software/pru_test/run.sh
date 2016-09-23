#sudo echo PRU-ADC-R0 > /sys/devices/bone_capemgr.?/slots
gcc loader.c -lprussdrv -o loader
pasm -b memtest.p
./loader memtest.bin
