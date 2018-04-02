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
LIBS:conn_sma_2gnd
LIBS:trl_line-cache
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
L CONN_SMA_2GND U101
U 1 1 59B4A05A
P 2600 3850
F 0 "U101" H 2300 4050 60  0000 C CNN
F 1 "CONN_SMA_2GND" H 2650 4150 60  0000 C CNN
F 2 "vna_footprints:SMA_901-10512_6p7MIL_FR408_CPW_LAUNCH" H 2600 3850 60  0001 C CNN
F 3 "" H 2600 3850 60  0000 C CNN
	1    2600 3850
	1    0    0    -1  
$EndComp
$Comp
L CONN_SMA_2GND U102
U 1 1 59B4A095
P 4300 3850
F 0 "U102" H 4000 4050 60  0000 C CNN
F 1 "CONN_SMA_2GND" H 4350 4150 60  0000 C CNN
F 2 "vna_footprints:SMA_901-10512_6p7MIL_FR408_CPW_LAUNCH" H 4300 3850 60  0001 C CNN
F 3 "" H 4300 3850 60  0000 C CNN
	1    4300 3850
	-1   0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 59B4A10C
P 2600 4400
F 0 "#PWR01" H 2600 4150 50  0001 C CNN
F 1 "GND" H 2600 4250 50  0000 C CNN
F 2 "" H 2600 4400 50  0001 C CNN
F 3 "" H 2600 4400 50  0001 C CNN
	1    2600 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	2550 4300 2550 4350
Wire Wire Line
	2550 4350 2650 4350
Wire Wire Line
	2600 4350 2600 4400
Wire Wire Line
	2650 4350 2650 4300
Connection ~ 2600 4350
$Comp
L GND #PWR02
U 1 1 59B4A147
P 4300 4400
F 0 "#PWR02" H 4300 4150 50  0001 C CNN
F 1 "GND" H 4300 4250 50  0000 C CNN
F 2 "" H 4300 4400 50  0001 C CNN
F 3 "" H 4300 4400 50  0001 C CNN
	1    4300 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	4250 4300 4250 4350
Wire Wire Line
	4250 4350 4350 4350
Wire Wire Line
	4350 4350 4350 4300
Wire Wire Line
	4300 4350 4300 4400
Connection ~ 4300 4350
Wire Wire Line
	3600 3850 3900 3850
$Comp
L C_Small C101
U 1 1 5AC18D77
P 3500 3850
F 0 "C101" H 3510 3920 50  0000 L CNN
F 1 "C_Small" H 3510 3770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0402" H 3500 3850 50  0001 C CNN
F 3 "" H 3500 3850 50  0001 C CNN
	1    3500 3850
	0    1    1    0   
$EndComp
Wire Wire Line
	3000 3850 3400 3850
$EndSCHEMATC
