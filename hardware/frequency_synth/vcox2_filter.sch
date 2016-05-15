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
LIBS:conn_sma_2gnd
LIBS:frequency_synth-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 8 10
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
L EMI_FILTER FI801
U 1 1 572C4EB0
P 5000 3350
F 0 "FI801" H 5150 3500 50  0000 C CNN
F 1 "LFCN-8400+" H 5400 3202 50  0000 C CNN
F 2 "vna_footprints:FV1206" H 5000 3350 50  0001 C CNN
F 3 "" H 5000 3350 50  0000 C CNN
	1    5000 3350
	1    0    0    -1  
$EndComp
$Comp
L EMI_FILTER FI802
U 1 1 572C4F49
P 6850 3350
F 0 "FI802" H 7000 3500 50  0000 C CNN
F 1 "HFCN-5500+" H 7250 3202 50  0000 C CNN
F 2 "vna_footprints:FV1206" H 6850 3350 50  0001 C CNN
F 3 "" H 6850 3350 50  0000 C CNN
	1    6850 3350
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR0176
U 1 1 572C4FB4
P 5000 3700
F 0 "#PWR0176" H 5000 3450 50  0001 C CNN
F 1 "GND" H 5000 3550 50  0000 C CNN
F 2 "" H 5000 3700 50  0000 C CNN
F 3 "" H 5000 3700 50  0000 C CNN
	1    5000 3700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR0177
U 1 1 572C4FCC
P 6850 3700
F 0 "#PWR0177" H 6850 3450 50  0001 C CNN
F 1 "GND" H 6850 3550 50  0000 C CNN
F 2 "" H 6850 3700 50  0000 C CNN
F 3 "" H 6850 3700 50  0000 C CNN
	1    6850 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	6850 3700 6850 3600
Wire Wire Line
	5000 3600 5000 3700
Wire Wire Line
	4550 3350 4350 3350
Wire Wire Line
	7300 3350 7450 3350
$Comp
L C_Small C801
U 1 1 572C5009
P 6050 3350
F 0 "C801" H 6060 3420 50  0000 L CNN
F 1 "10 pF" H 6060 3270 50  0000 L CNN
F 2 "Capacitors_SMD:C_0402" H 6050 3350 50  0001 C CNN
F 3 "" H 6050 3350 50  0000 C CNN
	1    6050 3350
	0    1    1    0   
$EndComp
Wire Wire Line
	5450 3350 5950 3350
Wire Wire Line
	6150 3350 6400 3350
Text HLabel 4350 3350 0    60   Input ~ 0
VCOX2FILT_IN
Text HLabel 7450 3350 2    60   Input ~ 0
VCOX2FILT_OUT
$Comp
L GND #PWR0178
U 1 1 572C575D
P 6050 4100
F 0 "#PWR0178" H 6050 3850 50  0001 C CNN
F 1 "GND" H 6050 3950 50  0000 C CNN
F 2 "" H 6050 4100 50  0000 C CNN
F 3 "" H 6050 4100 50  0000 C CNN
	1    6050 4100
	1    0    0    -1  
$EndComp
Text HLabel 6050 4000 1    60   Input ~ 0
GND
Wire Wire Line
	6050 4000 6050 4100
Text Notes 3850 2900 0    60   ~ 0
filter path for the vco doubler (highpass filter for fc/2 rejection, lowpass for harmonics)
$EndSCHEMATC
