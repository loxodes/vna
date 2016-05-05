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
LIBS:txco
LIBS:tcm-63ax+
LIBS:scbd-16-63
LIBS:rf_crossbar
LIBS:pwr_splitter
LIBS:pe42521
LIBS:pcm2900
LIBS:mounting_hole
LIBS:mounting_box
LIBS:mga-82563
LIBS:maam-011101
LIBS:ltc5549
LIBS:ltc1983
LIBS:ltc1566-1
LIBS:lt1567
LIBS:lmx2592
LIBS:lmk61e2
LIBS:hmc629
LIBS:hmc525
LIBS:hmc424
LIBS:hmc321
LIBS:hmc311sc70
LIBS:conn_sma
LIBS:cmm0511-qt-0g0t
LIBS:cat102
LIBS:boosterpack_ti
LIBS:adm7150
LIBS:adl5902
LIBS:adl5380
LIBS:adf4355-3
LIBS:74xx1g14
LIBS:74hc04
LIBS:74hc04_full
LIBS:frequency_synth-cache
EELAYER 25 0
EELAYER END
$Descr A3 16535 11693
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
S 1100 2800 1550 1250
U 572AD2A7
F0 "frequency_synth" 60
F1 "synth.sch" 60
F2 "RFOUTB" I R 2650 3300 60 
F3 "RFOUTA" I R 2650 3500 60 
F4 "LMX_CE" I L 1100 3100 60 
F5 "LMX_CSB" I L 1100 3200 60 
F6 "LMX_MUX" I L 1100 3300 60 
F7 "LNX_SDI" I L 1100 3400 60 
F8 "LMX_SCK" I L 1100 3500 60 
F9 "GND" I L 1100 3850 60 
F10 "SYNTH_3V3" I L 1100 3750 60 
$EndSheet
$Sheet
S 3200 2800 1700 1250
U 572AD2AC
F0 "filter bank" 60
F1 "filter_bank.sch" 60
F2 "FILT_RFOUT" I R 4900 3300 60 
F3 "FILT_RFIN" I L 3200 3300 60 
F4 "FILT_5V" I L 3200 3750 60 
F5 "GND" I L 3200 3850 60 
F6 "FILT_CTLA" I R 4900 3700 60 
F7 "FILT_CTLB" I R 4900 3800 60 
F8 "FILT_CTLC" I R 4900 3900 60 
$EndSheet
$Sheet
S 7350 2800 1800 1250
U 572AE3BA
F0 "attenuator" 60
F1 "attenuator.sch" 60
F2 "ATT_A1" I R 9150 3500 60 
F3 "ATT_A2" I R 9150 3600 60 
F4 "ATT_A3" I R 9150 3700 60 
F5 "ATT_A4" I R 9150 3800 60 
F6 "ATT_A5" I R 9150 3900 60 
F7 "ATT_A6" I R 9150 4000 60 
F8 "ATT_5V" I L 7350 3800 60 
F9 "GND" I L 7350 3900 60 
F10 "ATT_RFIN" I L 7350 3300 60 
F11 "ATT_RFOUT" I R 9150 3300 60 
$EndSheet
$Sheet
S 9600 2800 1850 1250
U 572AFD9E
F0 "amplifier" 60
F1 "amplifier.sch" 60
F2 "AMP_RFIN" I L 9600 3300 60 
F3 "AMP_RFOUT" I R 11450 3300 60 
F4 "AMP_5V" I L 9600 3800 60 
F5 "GND" I L 9600 3900 60 
$EndSheet
$Sheet
S 5350 3100 1500 800 
U 572B02EC
F0 "switch" 60
F1 "switch.sch" 60
F2 "SW_RF2" I L 5350 3300 60 
F3 "SW_RF1" I L 5350 3450 60 
F4 "SW_RFC" I R 6850 3300 60 
F5 "SW_CTRL" I R 6850 3700 60 
F6 "GND" I L 5350 3800 60 
F7 "SW_5V" I L 5350 3700 60 
$EndSheet
$Sheet
S 11850 2800 1850 1200
U 572B07EB
F0 "power detector" 60
F1 "powerdetect.sch" 60
F2 "DET_IN" I L 11850 3300 60 
F3 "DET_OUT" I R 13700 3300 60 
F4 "GND" I L 11850 3900 60 
F5 "VDET" I L 11850 3600 60 
F6 "DET_5V" I L 11850 3800 60 
$EndSheet
$Sheet
S 14150 2800 1800 1200
U 572B07F0
F0 "connectors, microcontroller, psu" 60
F1 "connectors_mcu.sch" 60
$EndSheet
$Sheet
S 3450 4550 1450 850 
U 572B09F0
F0 "vco double output filter" 60
F1 "vcox2_filter.sch" 60
F2 "VCOX2FILT_IN" I L 3450 4900 60 
F3 "VCOX2FILT_OUT" I R 4900 4900 60 
F4 "GND" I L 3450 5150 60 
$EndSheet
Wire Wire Line
	2650 3300 3200 3300
Wire Wire Line
	4900 3300 5350 3300
$EndSCHEMATC
