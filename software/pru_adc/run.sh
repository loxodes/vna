# compile and install device tree for pru with the following command:
#sudo dtc -O dtb -I dts -o /lib/firmware/PRU-ADC-R0-00A0.dtbo -b 0 -@ PRU-ADC-R0-00A0.dts

#for debian 7, add the following to /etc/rc.local: echo PRU-ADC-R0 > /sys/devices/bone_capemgr.?/slots
#for debian 8, add PRU-ADC-R0 to /etc/default/capemgr
# also, sudo /opt/tools/update_kernel.sh --lts-4_4 --bone-rt-channel

gcc adc_to_socket.c -lprussdrv -o adc_to_socket
pasm -b pru_adc.p
./adc_to_socket
