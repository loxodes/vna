#sudo echo PRU-ADC-R0 > /sys/devices/bone_capemgr.?/slots
#sudo dtc -O dtb -I dts -o /lib/firmware/PRU-ADC-R0-00A0.dtbo -b 0 -@ PRU-ADC-R0-00A0.dts
gcc adc_to_socket.c -lprussdrv -o loader
pasm -b memtest.p
./loader memtest.bin
