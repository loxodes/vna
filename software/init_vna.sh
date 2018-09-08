sudo ./vna_controller/init_gpio.sh
sudo python ./vna_controller/clk_synth_bbone.py
sudo python ./vna_controller/adc_bbone_init.py
sudo python ./vna_controller/lo_enable.py
sudo ./pru_adc/init_pru.sh
sudo ./pru_adc/adc_to_socket

