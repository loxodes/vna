# run these commands on the beaglebone
# then, run vna_driver on the computer to start the VNA

cd ~/repos/vna/software/vna_controller
sudo python zmq_io_server.py &
sudo python zmq_synth_server.py --synth a &
sudo python zmq_synth_server.py --synth b &
cd ~/repos/vna/software/pru_adc
./run.sh
