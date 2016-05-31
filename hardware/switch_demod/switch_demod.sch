EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:74hc04
LIBS:74hc04_full
LIBS:74xx1g14
LIBS:adf4355-3
LIBS:adl5380
LIBS:adl5902
LIBS:adm7150
LIBS:boosterpack_ti
LIBS:cat102
LIBS:cmm0511-qt-0g0t
LIBS:conn_sma
LIBS:conn_sma_2gnd
LIBS:hmc311sc70
LIBS:hmc321
LIBS:hmc424
LIBS:hmc525
LIBS:hmc629
LIBS:lmk61e2
LIBS:lmx2592
LIBS:lt1567
LIBS:lt1819
LIBS:ltc1566-1
LIBS:ltc1983
LIBS:ltc2323
LIBS:ltc5549
LIBS:maam-011101
LIBS:mga-82563
LIBS:mounting_box
LIBS:mounting_hole
LIBS:nc7sv74kbx
LIBS:pcm2900
LIBS:pe42521
LIBS:pwr_splitter
LIBS:rf_crossbar
LIBS:scbd-16-63
LIBS:tcm-63ax+
LIBS:tps793
LIBS:txco
LIBS:switch_demod-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 9
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 9350 2050 950  2550
U 574CB4A6
F0 "panel connectors" 60
F1 "connectors_rf.sch" 60
F2 "DUT_PORT1" B L 9350 2500 60 
F3 "DUT_PORT2" B L 9350 4050 60 
$EndSheet
$Sheet
S 6150 3550 900  850 
U 574CB4CD
F0 "switch_input_spdt" 60
F1 "switch_input_spdt.sch" 60
F2 "SW_RF2" I R 7050 4050 60 
F3 "SW_RF1" I R 7050 3850 60 
F4 "SW_RFC" I L 6150 4050 60 
$EndSheet
$Sheet
S 8100 2050 900  900 
U 574CB530
F0 "splitter_input" 60
F1 "splitter_input.sch" 60
F2 "RF1" I L 8100 2500 60 
F3 "RF2" I L 8100 2750 60 
F4 "RFC" I R 9000 2500 60 
$EndSheet
$Sheet
S 4050 3650 1300 900 
U 574CB5B8
F0 "demod" 60
F1 "demod.sch" 60
F2 "DEMOD_RF" I R 5350 4050 60 
F3 "DEMOD_LO" I L 4050 4050 60 
F4 "Q_P" I R 5350 4250 60 
F5 "Q_M" I R 5350 4350 60 
F6 "I_P" I L 4050 4250 60 
F7 "I_M" I L 4050 4350 60 
$EndSheet
$Sheet
S 2250 2150 1400 900 
U 574CB5C7
F0 "splitter_lo" 60
F1 "splitter_lo.sch" 60
F2 "RF1" I R 3650 2500 60 
F3 "RF2" I R 3650 2750 60 
F4 "RFC" I L 2250 2500 60 
$EndSheet
$Sheet
S 4100 2150 1150 900 
U 574CB629
F0 "attenuator" 60
F1 "attenuator.sch" 60
$EndSheet
$Sheet
S 4050 4800 1300 2100
U 574CB69A
F0 "adc" 60
F1 "adc.sch" 60
F2 "ADC_SCK" I L 4050 6000 60 
F3 "ADC_SDO2" I L 4050 6100 60 
F4 "ADC_CLKOUT" I L 4050 6200 60 
F5 "ADC_SDO1" I L 4050 6300 60 
F6 "ADC_CONV" I L 4050 6400 60 
F7 "ADC_CONV_CLK_OUT" I L 4050 6500 60 
F8 "ADC_VIO_EXT" I L 4050 6600 60 
F9 "ADC_I_M" I L 4050 5100 60 
F10 "ADC_Q_M" I R 5350 5100 60 
F11 "ADC_I_P" I L 4050 5200 60 
F12 "ADC_Q_P" I R 5350 5200 60 
F13 "ADC_CONV_CLK_IN" I L 4050 6700 60 
$EndSheet
$Sheet
S 750  4850 1000 2100
U 574CB6B0
F0 "connectors_control_pow" 60
F1 "connectors_control_pow.sch" 60
$EndSheet
Wire Wire Line
	9000 2500 9350 2500
Wire Wire Line
	7050 3850 7500 3850
Wire Wire Line
	7500 3850 7500 2750
Wire Wire Line
	7500 2750 8100 2750
Wire Wire Line
	9350 4050 7050 4050
Wire Wire Line
	6150 4050 5350 4050
Wire Wire Line
	3650 2750 3800 2750
Wire Wire Line
	3800 2750 3800 4050
Wire Wire Line
	3800 4050 4050 4050
Wire Wire Line
	4050 4250 3800 4250
Wire Wire Line
	3800 4250 3800 5200
Wire Wire Line
	3800 5200 4050 5200
Wire Wire Line
	4050 5100 4050 5050
Wire Wire Line
	4050 5050 3900 5050
Wire Wire Line
	3900 5050 3900 4350
Wire Wire Line
	3900 4350 4050 4350
Wire Wire Line
	5350 4350 5500 4350
Wire Wire Line
	5500 4350 5500 5100
Wire Wire Line
	5500 5100 5350 5100
Wire Wire Line
	5350 4250 5600 4250
Wire Wire Line
	5600 4250 5600 5200
Wire Wire Line
	5600 5200 5350 5200
Wire Wire Line
	2250 2500 2050 2500
Wire Wire Line
	2050 2500 2050 5200
Wire Wire Line
	2050 5200 1800 5200
$EndSCHEMATC
