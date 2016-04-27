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
LIBS:74xx1g14
LIBS:adf4355-3
LIBS:adl5380
LIBS:adl5902
LIBS:adm7150
LIBS:boosterpack_ti
LIBS:cat102
LIBS:cmm0511-qt-0g0t
LIBS:conn_sma
LIBS:hmc311sc70
LIBS:hmc321
LIBS:hmc424
LIBS:hmc525
LIBS:hmc629
LIBS:lmk61e2
LIBS:lmx2592
LIBS:lt1567
LIBS:ltc1566-1
LIBS:ltc1983
LIBS:ltc5549
LIBS:maam-011101
LIBS:mga-82563
LIBS:mounting_box
LIBS:mounting_hole
LIBS:pcm2900
LIBS:pe42521
LIBS:pwr_splitter
LIBS:rf_crossbar
LIBS:scbd-16-63
LIBS:tcm-63ax+
LIBS:txco
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
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
L CONN_SMA U5
U 1 1 571E6007
P 3400 2550
F 0 "U5" H 3050 2750 60  0000 C CNN
F 1 "CONN_SMA" H 3250 2900 60  0000 C CNN
F 2 "vna_footprints:732511150_sma_thin" H 3400 2550 60  0001 C CNN
F 3 "" H 3400 2550 60  0000 C CNN
	1    3400 2550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 571E6056
P 3400 3150
F 0 "#PWR01" H 3400 2900 50  0001 C CNN
F 1 "GND" H 3400 3000 50  0000 C CNN
F 2 "" H 3400 3150 50  0000 C CNN
F 3 "" H 3400 3150 50  0000 C CNN
	1    3400 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 3000 3250 3100
Wire Wire Line
	3250 3100 3550 3100
Wire Wire Line
	3550 3100 3550 3000
Wire Wire Line
	3400 3100 3400 3150
Connection ~ 3400 3100
Wire Wire Line
	3350 3000 3350 3100
Connection ~ 3350 3100
Wire Wire Line
	3450 3000 3450 3100
Connection ~ 3450 3100
$Comp
L CONN_SMA U2
U 1 1 571E60B6
P 1750 2550
F 0 "U2" H 1400 2750 60  0000 C CNN
F 1 "CONN_SMA" H 1600 2900 60  0000 C CNN
F 2 "vna_footprints:732511150_sma_thin" H 1750 2550 60  0001 C CNN
F 3 "" H 1750 2550 60  0000 C CNN
	1    1750 2550
	-1   0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 571E60BC
P 1750 3150
F 0 "#PWR02" H 1750 2900 50  0001 C CNN
F 1 "GND" H 1750 3000 50  0000 C CNN
F 2 "" H 1750 3150 50  0000 C CNN
F 3 "" H 1750 3150 50  0000 C CNN
	1    1750 3150
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1900 3000 1900 3100
Wire Wire Line
	1900 3100 1600 3100
Wire Wire Line
	1600 3100 1600 3000
Wire Wire Line
	1750 3100 1750 3150
Connection ~ 1750 3100
Wire Wire Line
	1800 3000 1800 3100
Connection ~ 1800 3100
Wire Wire Line
	1700 3000 1700 3100
Connection ~ 1700 3100
Wire Wire Line
	2300 2550 2850 2550
Text Notes 7100 1000 0    60   ~ 0
1 cm after SMA connector for SLOT\n2 cm for through
$Comp
L CONN_SMA U6
U 1 1 571E6A7C
P 3350 3900
F 0 "U6" H 3000 4100 60  0000 C CNN
F 1 "CONN_SMA" H 3200 4250 60  0000 C CNN
F 2 "vna_footprints:732511150_sma_thin" H 3350 3900 60  0001 C CNN
F 3 "" H 3350 3900 60  0000 C CNN
	1    3350 3900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 571E6A82
P 3350 4500
F 0 "#PWR03" H 3350 4250 50  0001 C CNN
F 1 "GND" H 3350 4350 50  0000 C CNN
F 2 "" H 3350 4500 50  0000 C CNN
F 3 "" H 3350 4500 50  0000 C CNN
	1    3350 4500
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 4350 3200 4450
Wire Wire Line
	3200 4450 3500 4450
Wire Wire Line
	3500 4450 3500 4350
Wire Wire Line
	3350 4450 3350 4500
Connection ~ 3350 4450
Wire Wire Line
	3300 4350 3300 4450
Connection ~ 3300 4450
Wire Wire Line
	3400 4350 3400 4450
Connection ~ 3400 4450
$Comp
L CONN_SMA U3
U 1 1 571E6A91
P 1700 3900
F 0 "U3" H 1350 4100 60  0000 C CNN
F 1 "CONN_SMA" H 1550 4250 60  0000 C CNN
F 2 "vna_footprints:732511150_sma_thin" H 1700 3900 60  0001 C CNN
F 3 "" H 1700 3900 60  0000 C CNN
	1    1700 3900
	-1   0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 571E6A97
P 1700 4500
F 0 "#PWR04" H 1700 4250 50  0001 C CNN
F 1 "GND" H 1700 4350 50  0000 C CNN
F 2 "" H 1700 4500 50  0000 C CNN
F 3 "" H 1700 4500 50  0000 C CNN
	1    1700 4500
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1850 4350 1850 4450
Wire Wire Line
	1850 4450 1550 4450
Wire Wire Line
	1550 4450 1550 4350
Wire Wire Line
	1700 4450 1700 4500
Connection ~ 1700 4450
Wire Wire Line
	1750 4350 1750 4450
Connection ~ 1750 4450
Wire Wire Line
	1650 4350 1650 4450
Connection ~ 1650 4450
Wire Wire Line
	2250 3900 2800 3900
Text Notes 4650 3950 0    60   ~ 0
2x 7.5 mm + L
Text Notes 4450 2550 0    60   ~ 0
15 mm, 1 GHz to 5 GHz\n5 mm, 5 GHz to 15 GHz\n
$EndSCHEMATC
