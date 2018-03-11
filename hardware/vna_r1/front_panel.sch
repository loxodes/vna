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
LIBS:PocketBeagle
LIBS:txco
LIBS:trf37b73
LIBS:tps2065d
LIBS:tps2051
LIBS:tps793
LIBS:tps255xx
LIBS:tpd4s012
LIBS:tcm-63ax+
LIBS:sn74lvc1g07
LIBS:scbd-16-63
LIBS:rf_crossbar
LIBS:pwr_splitter
LIBS:pe43705
LIBS:pe42541
LIBS:pe42540
LIBS:pe42521
LIBS:pcm2900
LIBS:okr_t3-w12-c
LIBS:nc7wzu04
LIBS:nc7sv74kbx
LIBS:nb3n551
LIBS:mounting_hole
LIBS:mounting_box
LIBS:mga-82563
LIBS:max2605
LIBS:max510
LIBS:masw-008322-tr1000
LIBS:maam-011101
LIBS:maam-011100
LIBS:ltc5596
LIBS:ltc5549
LIBS:ltc2630
LIBS:ltc2323
LIBS:ltc2054cs5
LIBS:ltc1983
LIBS:ltc1566-1
LIBS:lt1819
LIBS:lt1567
LIBS:lmx2594
LIBS:lmx2592
LIBS:lmk61e2
LIBS:lan8710a
LIBS:hmc629
LIBS:hmc525
LIBS:hmc475
LIBS:hmc424
LIBS:hmc321
LIBS:hmc311sc70
LIBS:conn_sma_2gnd
LIBS:conn_sma
LIBS:conn_microsd
LIBS:cmm0511-qt-0g0t
LIBS:cat102
LIBS:boosterpack_ti
LIBS:ammp-6120
LIBS:adrf5040
LIBS:adp7158
LIBS:adm7150
LIBS:adl5902
LIBS:adl5380
LIBS:adf4355-3
LIBS:ad9864
LIBS:ad9577
LIBS:75451
LIBS:74xx1g14
LIBS:74hc04_full
LIBS:74hc04
LIBS:vdd_rf
LIBS:vdd_lo
LIBS:vdd_clk
LIBS:vna_r1-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 7 10
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
L CONN_SMA_2GND U1003
U 1 1 59CECE50
P 6600 1000
F 0 "U1003" H 6300 1200 60  0000 C CNN
F 1 "CONN_SMA_2GND" H 6800 1200 60  0000 C CNN
F 2 "vna_footprints:732511150_sma_thin" H 6600 1000 60  0001 C CNN
F 3 "" H 6600 1000 60  0000 C CNN
	1    6600 1000
	-1   0    0    -1  
$EndComp
$Comp
L GND #PWR0227
U 1 1 59CECE56
P 6600 1550
F 0 "#PWR0227" H 6600 1300 50  0001 C CNN
F 1 "GND" H 6600 1400 50  0000 C CNN
F 2 "" H 6600 1550 50  0001 C CNN
F 3 "" H 6600 1550 50  0001 C CNN
	1    6600 1550
	1    0    0    -1  
$EndComp
Text HLabel 5800 1000 0    60   Output ~ 0
DEMOD_1
$Comp
L CONN_SMA_2GND U1004
U 1 1 59CECE63
P 6600 2250
F 0 "U1004" H 6300 2450 60  0000 C CNN
F 1 "CONN_SMA_2GND" H 6800 2450 60  0000 C CNN
F 2 "vna_footprints:732511150_sma_thin" H 6600 2250 60  0001 C CNN
F 3 "" H 6600 2250 60  0000 C CNN
	1    6600 2250
	-1   0    0    -1  
$EndComp
$Comp
L GND #PWR0228
U 1 1 59CECE69
P 6600 2800
F 0 "#PWR0228" H 6600 2550 50  0001 C CNN
F 1 "GND" H 6600 2650 50  0000 C CNN
F 2 "" H 6600 2800 50  0001 C CNN
F 3 "" H 6600 2800 50  0001 C CNN
	1    6600 2800
	1    0    0    -1  
$EndComp
Text HLabel 5800 2250 0    60   Output ~ 0
DEMOD_2
$Comp
L CONN_SMA_2GND U1005
U 1 1 59CED22A
P 6600 3500
F 0 "U1005" H 6300 3700 60  0000 C CNN
F 1 "CONN_SMA_2GND" H 6800 3700 60  0000 C CNN
F 2 "vna_footprints:732511150_sma_thin" H 6600 3500 60  0001 C CNN
F 3 "" H 6600 3500 60  0000 C CNN
	1    6600 3500
	-1   0    0    -1  
$EndComp
$Comp
L GND #PWR0229
U 1 1 59CED230
P 6600 4050
F 0 "#PWR0229" H 6600 3800 50  0001 C CNN
F 1 "GND" H 6600 3900 50  0000 C CNN
F 2 "" H 6600 4050 50  0001 C CNN
F 3 "" H 6600 4050 50  0001 C CNN
	1    6600 4050
	1    0    0    -1  
$EndComp
Text HLabel 5800 3500 0    60   Output ~ 0
DEMOD_3
$Comp
L CONN_SMA_2GND U1006
U 1 1 59CED23D
P 6600 4750
F 0 "U1006" H 6300 4950 60  0000 C CNN
F 1 "CONN_SMA_2GND" H 6800 4950 60  0000 C CNN
F 2 "vna_footprints:732511150_sma_thin" H 6600 4750 60  0001 C CNN
F 3 "" H 6600 4750 60  0000 C CNN
	1    6600 4750
	-1   0    0    -1  
$EndComp
$Comp
L GND #PWR0230
U 1 1 59CED243
P 6600 5300
F 0 "#PWR0230" H 6600 5050 50  0001 C CNN
F 1 "GND" H 6600 5150 50  0000 C CNN
F 2 "" H 6600 5300 50  0001 C CNN
F 3 "" H 6600 5300 50  0001 C CNN
	1    6600 5300
	1    0    0    -1  
$EndComp
Text HLabel 5800 4750 0    60   Output ~ 0
DEMOD_4
$Comp
L LED_Small D1003
U 1 1 59CEF1D8
P 9200 4900
F 0 "D1003" H 9150 5025 50  0000 L CNN
F 1 "RED" H 9025 4800 50  0000 L CNN
F 2 "LEDs:LED_0603" V 9200 4900 50  0001 C CNN
F 3 "" V 9200 4900 50  0001 C CNN
	1    9200 4900
	0    -1   -1   0   
$EndComp
$Comp
L R_Small R1003
U 1 1 59CEF1DE
P 9200 5150
F 0 "R1003" H 9230 5170 50  0000 L CNN
F 1 "1k" H 9230 5110 50  0000 L CNN
F 2 "Resistors_SMD:R_0402" H 9200 5150 50  0001 C CNN
F 3 "" H 9200 5150 50  0001 C CNN
	1    9200 5150
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR0231
U 1 1 59CEF1E4
P 9200 5300
F 0 "#PWR0231" H 9200 5050 50  0001 C CNN
F 1 "GND" H 9200 5150 50  0000 C CNN
F 2 "" H 9200 5300 50  0001 C CNN
F 3 "" H 9200 5300 50  0001 C CNN
	1    9200 5300
	1    0    0    -1  
$EndComp
Text HLabel 9200 4550 1    60   Input ~ 0
POWER_LED
Wire Wire Line
	6550 1450 6550 1500
Wire Wire Line
	6550 1500 6650 1500
Wire Wire Line
	6650 1500 6650 1450
Wire Wire Line
	6600 1500 6600 1550
Connection ~ 6600 1500
Wire Wire Line
	6200 1000 5800 1000
Wire Wire Line
	6550 2700 6550 2750
Wire Wire Line
	6550 2750 6650 2750
Wire Wire Line
	6650 2750 6650 2700
Wire Wire Line
	6600 2750 6600 2800
Connection ~ 6600 2750
Wire Wire Line
	6200 2250 5800 2250
Wire Wire Line
	6550 3950 6550 4000
Wire Wire Line
	6550 4000 6650 4000
Wire Wire Line
	6650 4000 6650 3950
Wire Wire Line
	6600 4000 6600 4050
Connection ~ 6600 4000
Wire Wire Line
	6200 3500 5800 3500
Wire Wire Line
	6550 5200 6550 5250
Wire Wire Line
	6550 5250 6650 5250
Wire Wire Line
	6650 5250 6650 5200
Wire Wire Line
	6600 5250 6600 5300
Connection ~ 6600 5250
Wire Wire Line
	6200 4750 5800 4750
Wire Wire Line
	9200 5250 9200 5300
Wire Wire Line
	9200 5000 9200 5050
Wire Wire Line
	9200 4800 9200 4550
$Comp
L Conn_01x07 J701
U 1 1 5AA5807C
P 9450 2800
F 0 "J701" H 9450 3200 50  0000 C CNN
F 1 "Conn_01x07" H 9450 2400 50  0000 C CNN
F 2 "Connect:Wafer_Horizontal20x5.8x7RM2.5-7" H 9450 2800 50  0001 C CNN
F 3 "" H 9450 2800 50  0001 C CNN
	1    9450 2800
	1    0    0    -1  
$EndComp
$Comp
L VDD_LO #SUPPLY0232
U 1 1 5AA67497
P 7700 5500
F 0 "#SUPPLY0232" H 7700 5500 45  0001 L BNN
F 1 "VDD_LO" H 7700 5650 45  0000 L BNN
F 2 "" H 7700 5500 60  0001 C CNN
F 3 "" H 7700 5500 60  0001 C CNN
	1    7700 5500
	1    0    0    -1  
$EndComp
$Comp
L VDD_RF #SUPPLY0233
U 1 1 5AA674C0
P 8050 5600
F 0 "#SUPPLY0233" H 8050 5600 45  0001 L BNN
F 1 "VDD_RF" H 8050 5750 45  0000 L BNN
F 2 "" H 8050 5600 60  0001 C CNN
F 3 "" H 8050 5600 60  0001 C CNN
	1    8050 5600
	1    0    0    -1  
$EndComp
$Comp
L -5V #PWR705
U 1 1 5AA674F7
P 8000 6250
F 0 "#PWR705" H 8000 6350 50  0001 C CNN
F 1 "-5V" H 8000 6400 50  0000 C CNN
F 2 "" H 8000 6250 50  0001 C CNN
F 3 "" H 8000 6250 50  0001 C CNN
	1    8000 6250
	1    0    0    -1  
$EndComp
$EndSCHEMATC
