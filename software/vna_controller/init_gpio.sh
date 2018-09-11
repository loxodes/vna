config-pin P9_20 gpio
config-pin P9_19 gpio
config-pin P8_46 pruin
config-pin P8_45 pruin
config-pin P8_44 pruin
config-pin P8_43 pruin
config-pin P8_42 pruin
config-pin P8_41 pruin
config-pin P8_40 pruout
# manually enable 3V3 PLL and RF 3V3 EN, because setting them with mmap_gpio is broken...? probably something related to i2c2?

#if [ -e /sys/class/gpio/gpio12 ]
#then
#    echo "gpio 12 already exists, not creating"
#else
#    echo 12 >/sys/class/gpio/export
#fi
#
#if [ -e /sys/class/gpio/gpio13 ]
#then
#    echo "gpio 13 already exists, not creating"
#else
#    echo 13 >/sys/class/gpio/export
#fi

#echo out >/sys/class/gpio/gpio12/direction
#echo out >/sys/class/gpio/gpio13/direction

#echo 1 >/sys/class/gpio/gpio12/value
#echo 1 >/sys/class/gpio/gpio13/value

# enable gpio banks 0-3
#sudo devmem2 0x44e00404 b 0x02
#sudo devmem2 0x44e000AC b 0x02
#sudo devmem2 0x44e000B0 b 0x02
#sudo devmem2 0x44e000B4 b 0x02 

