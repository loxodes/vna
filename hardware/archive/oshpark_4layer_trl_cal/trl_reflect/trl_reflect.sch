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
LIBS:trl_reflect-cache
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
Text Notes 4750 3400 0    60   ~ 0
TRL calibration board\nreflect\n
$Comp
L CONN_SMA_2GND U101
U 1 1 59B47D70
P 4100 4450
F 0 "U101" H 3800 4650 60  0000 C CNN
F 1 "CONN_SMA_2GND" H 4150 4750 60  0000 C CNN
F 2 "vna_footprints:SMA_901-10512_6p7MIL_FR408_CPW_LAUNCH" H 4100 4450 60  0001 C CNN
F 3 "" H 4100 4450 60  0000 C CNN
	1    4100 4450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 59B47DA6
P 4050 5000
F 0 "#PWR01" H 4050 4750 50  0001 C CNN
F 1 "GND" H 4050 4850 50  0000 C CNN
F 2 "" H 4050 5000 50  0001 C CNN
F 3 "" H 4050 5000 50  0001 C CNN
	1    4050 5000
	1    0    0    -1  
$EndComp
Wire Wire Line
	4050 4900 4050 5000
Wire Wire Line
	4150 4900 4150 4950
Wire Wire Line
	4150 4950 4050 4950
Connection ~ 4050 4950
Wire Wire Line
	4500 4450 5250 4450
Text Notes 3900 4000 0    60   ~ 0
trace extends 5 mm past the end of the connector pads
$EndSCHEMATC
