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
Text Notes 3100 2100 0    60   ~ 0
CPW for OSH Park FR408\n.2 mm ground to trace spacing\n1 mm rf trace
$Comp
L CONN_SMA_2GND U101
U 1 1 577AF875
P 3350 2650
F 0 "U101" H 3050 2850 60  0000 C CNN
F 1 "CONN_SMA_2GND" H 3400 2950 60  0000 C CNN
F 2 "vna_footprints:SMA_CPW_1MM_.2MM" H 3350 2650 60  0001 C CNN
F 3 "" H 3350 2650 60  0000 C CNN
	1    3350 2650
	1    0    0    -1  
$EndComp
$Comp
L CONN_SMA_2GND U102
U 1 1 577AF8C4
P 4550 2650
F 0 "U102" H 4250 2850 60  0000 C CNN
F 1 "CONN_SMA_2GND" H 4600 2950 60  0000 C CNN
F 2 "vna_footprints:SMA_CPW_1MM_.2MM" H 4550 2650 60  0001 C CNN
F 3 "" H 4550 2650 60  0000 C CNN
	1    4550 2650
	-1   0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 577AF8DB
P 3350 3200
F 0 "#PWR01" H 3350 2950 50  0001 C CNN
F 1 "GND" H 3350 3050 50  0000 C CNN
F 2 "" H 3350 3200 50  0000 C CNN
F 3 "" H 3350 3200 50  0000 C CNN
	1    3350 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3300 3100 3300 3150
Wire Wire Line
	3300 3150 3400 3150
Wire Wire Line
	3400 3150 3400 3100
Wire Wire Line
	3350 3150 3350 3200
Connection ~ 3350 3150
$Comp
L GND #PWR02
U 1 1 577AF906
P 4550 3200
F 0 "#PWR02" H 4550 2950 50  0001 C CNN
F 1 "GND" H 4550 3050 50  0000 C CNN
F 2 "" H 4550 3200 50  0000 C CNN
F 3 "" H 4550 3200 50  0000 C CNN
	1    4550 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	4500 3100 4500 3150
Wire Wire Line
	4500 3150 4600 3150
Wire Wire Line
	4600 3150 4600 3100
Wire Wire Line
	4550 3150 4550 3200
Connection ~ 4550 3150
Wire Wire Line
	3750 2650 4150 2650
$Comp
L CONN_01X01 P101
U 1 1 577AFB68
P 3250 3950
F 0 "P101" H 3250 4050 50  0000 C CNN
F 1 "CONN_01X01" V 3350 3950 50  0000 C CNN
F 2 "" H 3250 3950 50  0000 C CNN
F 3 "" H 3250 3950 50  0000 C CNN
	1    3250 3950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 577AFBC3
P 3000 3950
F 0 "#PWR03" H 3000 3700 50  0001 C CNN
F 1 "GND" H 3000 3800 50  0000 C CNN
F 2 "" H 3000 3950 50  0000 C CNN
F 3 "" H 3000 3950 50  0000 C CNN
	1    3000 3950
	0    1    1    0   
$EndComp
Wire Wire Line
	3000 3950 3050 3950
$EndSCHEMATC
