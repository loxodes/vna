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
Sheet 5 9
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L PWR_SPLITTER U501
U 1 1 574CDAE3
P 6000 3400
F 0 "U501" H 5600 3800 60  0000 C CNN
F 1 "PWR_SPLITTER" H 5850 3900 60  0000 C CNN
F 2 "vna_footprints:PS1608" H 6000 3400 60  0001 C CNN
F 3 "" H 6000 3400 60  0000 C CNN
	1    6000 3400
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR053
U 1 1 574CDAE4
P 5950 4000
F 0 "#PWR053" H 5950 3750 50  0001 C CNN
F 1 "GND" H 5950 3850 50  0000 C CNN
F 2 "" H 5950 4000 50  0000 C CNN
F 3 "" H 5950 4000 50  0000 C CNN
	1    5950 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	5950 3850 5950 4000
Wire Wire Line
	5400 3400 4750 3400
Wire Wire Line
	6550 3250 7150 3250
Wire Wire Line
	6550 3550 7150 3550
Text HLabel 7150 3250 2    60   Input ~ 0
RF1
Text HLabel 7150 3550 2    60   Input ~ 0
RF2
Text HLabel 4750 3400 0    60   Input ~ 0
RFC
$EndSCHEMATC
