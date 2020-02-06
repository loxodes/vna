export TRELLIS=/usr/share/trellis
openocd -f $TRELLIS/misc/openocd/ecp5-versa5g.cfg -c "transport select jtag; init; svf soc_basesoc_versa_ecp5/gateware/top.svf; exit"
