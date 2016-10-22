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
LIBS:OSD335x
LIBS:74xx1g14
LIBS:conn_microsd
LIBS:lan8710a
LIBS:sn74lvc1g07
LIBS:controller-cache
EELAYER 25 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 4 4
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
L OSD3358 U201
U 6 1 57EDFCEA
P 2650 3100
F 0 "U201" H 2850 3350 60  0000 L CNN
F 1 "OSD3358" H 2850 3250 60  0000 L CNN
F 2 "" H 2650 3100 60  0001 C CNN
F 3 "" H 2650 3100 60  0001 C CNN
	6    2650 3100
	1    0    0    -1  
$EndComp
$Comp
L OSD3358 U201
U 5 1 57EDFD08
P 2350 5600
F 0 "U201" H 2550 5850 60  0000 L CNN
F 1 "OSD3358" H 2550 5750 60  0000 L CNN
F 2 "" H 2350 5600 60  0001 C CNN
F 3 "" H 2350 5600 60  0001 C CNN
	5    2350 5600
	1    0    0    -1  
$EndComp
$Comp
L OSD3358 U201
U 4 1 57EDFD87
P 6550 7100
F 0 "U201" H 6750 7350 60  0000 L CNN
F 1 "OSD3358" H 6750 7250 60  0000 L CNN
F 2 "" H 6550 7100 60  0001 C CNN
F 3 "" H 6550 7100 60  0001 C CNN
	4    6550 7100
	1    0    0    -1  
$EndComp
$Comp
L OSD3358 U201
U 8 1 57EE02B2
P 5700 2000
F 0 "U201" H 5900 2250 60  0000 L CNN
F 1 "OSD3358" H 5900 2150 60  0000 L CNN
F 2 "" H 5700 2000 60  0001 C CNN
F 3 "" H 5700 2000 60  0001 C CNN
	8    5700 2000
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B7C24
P 8250 6900
F 0 "R?" H 8280 6920 50  0000 L CNN
F 1 "DNP" H 8280 6860 50  0000 L CNN
F 2 "" H 8250 6900 50  0000 C CNN
F 3 "" H 8250 6900 50  0000 C CNN
	1    8250 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B7EBC
P 8250 9400
F 0 "R?" H 8280 9420 50  0000 L CNN
F 1 "100k" H 8280 9360 50  0000 L CNN
F 2 "" H 8250 9400 50  0000 C CNN
F 3 "" H 8250 9400 50  0000 C CNN
	1    8250 9400
	1    0    0    -1  
$EndComp
$Comp
L +3V3 #PWR?
U 1 1 580B7FB6
P 8250 6550
F 0 "#PWR?" H 8250 6400 50  0001 C CNN
F 1 "+3V3" H 8250 6690 50  0000 C CNN
F 2 "" H 8250 6550 50  0000 C CNN
F 3 "" H 8250 6550 50  0000 C CNN
	1    8250 6550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 580B80EC
P 8250 9750
F 0 "#PWR?" H 8250 9500 50  0001 C CNN
F 1 "GND" H 8250 9600 50  0000 C CNN
F 2 "" H 8250 9750 50  0000 C CNN
F 3 "" H 8250 9750 50  0000 C CNN
	1    8250 9750
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B81B2
P 8550 6900
F 0 "R?" H 8580 6920 50  0000 L CNN
F 1 "DNP" H 8580 6860 50  0000 L CNN
F 2 "" H 8550 6900 50  0000 C CNN
F 3 "" H 8550 6900 50  0000 C CNN
	1    8550 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B81B8
P 8550 9400
F 0 "R?" H 8580 9420 50  0000 L CNN
F 1 "100k" H 8580 9360 50  0000 L CNN
F 2 "" H 8550 9400 50  0000 C CNN
F 3 "" H 8550 9400 50  0000 C CNN
	1    8550 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B8207
P 8900 6900
F 0 "R?" H 8930 6920 50  0000 L CNN
F 1 "100k" H 8930 6860 50  0000 L CNN
F 2 "" H 8900 6900 50  0000 C CNN
F 3 "" H 8900 6900 50  0000 C CNN
	1    8900 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B820D
P 8900 9400
F 0 "R?" H 8930 9420 50  0000 L CNN
F 1 "DNP" H 8930 9360 50  0000 L CNN
F 2 "" H 8900 9400 50  0000 C CNN
F 3 "" H 8900 9400 50  0000 C CNN
	1    8900 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B826C
P 9200 6900
F 0 "R?" H 9230 6920 50  0000 L CNN
F 1 "100k" H 9230 6860 50  0000 L CNN
F 2 "" H 9200 6900 50  0000 C CNN
F 3 "" H 9200 6900 50  0000 C CNN
	1    9200 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B8272
P 9200 9400
F 0 "R?" H 9230 9420 50  0000 L CNN
F 1 "DNP" H 9230 9360 50  0000 L CNN
F 2 "" H 9200 9400 50  0000 C CNN
F 3 "" H 9200 9400 50  0000 C CNN
	1    9200 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B8C79
P 9500 6900
F 0 "R?" H 9530 6920 50  0000 L CNN
F 1 "100k" H 9530 6860 50  0000 L CNN
F 2 "" H 9500 6900 50  0000 C CNN
F 3 "" H 9500 6900 50  0000 C CNN
	1    9500 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B8C7F
P 9500 9400
F 0 "R?" H 9530 9420 50  0000 L CNN
F 1 "DNP" H 9530 9360 50  0000 L CNN
F 2 "" H 9500 9400 50  0000 C CNN
F 3 "" H 9500 9400 50  0000 C CNN
	1    9500 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B8C85
P 9800 6900
F 0 "R?" H 9830 6920 50  0000 L CNN
F 1 "100k" H 9830 6860 50  0000 L CNN
F 2 "" H 9800 6900 50  0000 C CNN
F 3 "" H 9800 6900 50  0000 C CNN
	1    9800 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B8C8B
P 9800 9400
F 0 "R?" H 9830 9420 50  0000 L CNN
F 1 "DNP" H 9830 9360 50  0000 L CNN
F 2 "" H 9800 9400 50  0000 C CNN
F 3 "" H 9800 9400 50  0000 C CNN
	1    9800 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B8C91
P 10150 6900
F 0 "R?" H 10180 6920 50  0000 L CNN
F 1 "DNP" H 10180 6860 50  0000 L CNN
F 2 "" H 10150 6900 50  0000 C CNN
F 3 "" H 10150 6900 50  0000 C CNN
	1    10150 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B8C97
P 10150 9400
F 0 "R?" H 10180 9420 50  0000 L CNN
F 1 "100k" H 10180 9360 50  0000 L CNN
F 2 "" H 10150 9400 50  0000 C CNN
F 3 "" H 10150 9400 50  0000 C CNN
	1    10150 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B8C9D
P 10450 6900
F 0 "R?" H 10480 6920 50  0000 L CNN
F 1 "DNP" H 10480 6860 50  0000 L CNN
F 2 "" H 10450 6900 50  0000 C CNN
F 3 "" H 10450 6900 50  0000 C CNN
	1    10450 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B8CA3
P 10450 9400
F 0 "R?" H 10480 9420 50  0000 L CNN
F 1 "100k" H 10480 9360 50  0000 L CNN
F 2 "" H 10450 9400 50  0000 C CNN
F 3 "" H 10450 9400 50  0000 C CNN
	1    10450 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B95B3
P 10900 6900
F 0 "R?" H 10930 6920 50  0000 L CNN
F 1 "DNP" H 10930 6860 50  0000 L CNN
F 2 "" H 10900 6900 50  0000 C CNN
F 3 "" H 10900 6900 50  0000 C CNN
	1    10900 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B95B9
P 10900 9400
F 0 "R?" H 10930 9420 50  0000 L CNN
F 1 "100k" H 10930 9360 50  0000 L CNN
F 2 "" H 10900 9400 50  0000 C CNN
F 3 "" H 10900 9400 50  0000 C CNN
	1    10900 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B95C5
P 11200 6900
F 0 "R?" H 11230 6920 50  0000 L CNN
F 1 "DNP" H 11230 6860 50  0000 L CNN
F 2 "" H 11200 6900 50  0000 C CNN
F 3 "" H 11200 6900 50  0000 C CNN
	1    11200 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B95CB
P 11200 9400
F 0 "R?" H 11230 9420 50  0000 L CNN
F 1 "100k" H 11230 9360 50  0000 L CNN
F 2 "" H 11200 9400 50  0000 C CNN
F 3 "" H 11200 9400 50  0000 C CNN
	1    11200 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B95D1
P 11550 6900
F 0 "R?" H 11580 6920 50  0000 L CNN
F 1 "DNP" H 11580 6860 50  0000 L CNN
F 2 "" H 11550 6900 50  0000 C CNN
F 3 "" H 11550 6900 50  0000 C CNN
	1    11550 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B95D7
P 11550 9400
F 0 "R?" H 11580 9420 50  0000 L CNN
F 1 "100k" H 11580 9360 50  0000 L CNN
F 2 "" H 11550 9400 50  0000 C CNN
F 3 "" H 11550 9400 50  0000 C CNN
	1    11550 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B95DD
P 11850 6900
F 0 "R?" H 11880 6920 50  0000 L CNN
F 1 "DNP" H 11880 6860 50  0000 L CNN
F 2 "" H 11850 6900 50  0000 C CNN
F 3 "" H 11850 6900 50  0000 C CNN
	1    11850 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B95E3
P 11850 9400
F 0 "R?" H 11880 9420 50  0000 L CNN
F 1 "100k" H 11880 9360 50  0000 L CNN
F 2 "" H 11850 9400 50  0000 C CNN
F 3 "" H 11850 9400 50  0000 C CNN
	1    11850 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B95FD
P 12150 6900
F 0 "R?" H 12180 6920 50  0000 L CNN
F 1 "DNP" H 12180 6860 50  0000 L CNN
F 2 "" H 12150 6900 50  0000 C CNN
F 3 "" H 12150 6900 50  0000 C CNN
	1    12150 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B9603
P 12150 9400
F 0 "R?" H 12180 9420 50  0000 L CNN
F 1 "100k" H 12180 9360 50  0000 L CNN
F 2 "" H 12150 9400 50  0000 C CNN
F 3 "" H 12150 9400 50  0000 C CNN
	1    12150 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B9609
P 12450 6900
F 0 "R?" H 12480 6920 50  0000 L CNN
F 1 "DNP" H 12480 6860 50  0000 L CNN
F 2 "" H 12450 6900 50  0000 C CNN
F 3 "" H 12450 6900 50  0000 C CNN
	1    12450 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B960F
P 12450 9400
F 0 "R?" H 12480 9420 50  0000 L CNN
F 1 "100k" H 12480 9360 50  0000 L CNN
F 2 "" H 12450 9400 50  0000 C CNN
F 3 "" H 12450 9400 50  0000 C CNN
	1    12450 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B9615
P 12800 6900
F 0 "R?" H 12830 6920 50  0000 L CNN
F 1 "100k" H 12830 6860 50  0000 L CNN
F 2 "" H 12800 6900 50  0000 C CNN
F 3 "" H 12800 6900 50  0000 C CNN
	1    12800 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B961B
P 12800 9400
F 0 "R?" H 12830 9420 50  0000 L CNN
F 1 "DNP" H 12830 9360 50  0000 L CNN
F 2 "" H 12800 9400 50  0000 C CNN
F 3 "" H 12800 9400 50  0000 C CNN
	1    12800 9400
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B9621
P 13100 6900
F 0 "R?" H 13130 6920 50  0000 L CNN
F 1 "DNP" H 13130 6860 50  0000 L CNN
F 2 "" H 13100 6900 50  0000 C CNN
F 3 "" H 13100 6900 50  0000 C CNN
	1    13100 6900
	1    0    0    -1  
$EndComp
$Comp
L R_Small R?
U 1 1 580B9627
P 13100 9400
F 0 "R?" H 13130 9420 50  0000 L CNN
F 1 "100k" H 13130 9360 50  0000 L CNN
F 2 "" H 13100 9400 50  0000 C CNN
F 3 "" H 13100 9400 50  0000 C CNN
	1    13100 9400
	1    0    0    -1  
$EndComp
Wire Wire Line
	8250 6550 8250 6800
Wire Wire Line
	8250 7000 8250 9300
Wire Wire Line
	8250 9500 8250 9750
Wire Wire Line
	8550 7000 8550 9300
Wire Wire Line
	8900 7000 8900 9300
Wire Wire Line
	9200 7000 9200 9300
Wire Wire Line
	8250 6650 13100 6650
Wire Wire Line
	8550 6650 8550 6800
Connection ~ 8250 6650
Wire Wire Line
	8900 6650 8900 6800
Connection ~ 8550 6650
Wire Wire Line
	9200 6650 9200 6800
Connection ~ 8900 6650
Wire Wire Line
	8550 9500 8550 9650
Wire Wire Line
	8250 9650 13100 9650
Connection ~ 8250 9650
Wire Wire Line
	8900 9650 8900 9500
Connection ~ 8550 9650
Wire Wire Line
	9200 9650 9200 9500
Connection ~ 8900 9650
Wire Wire Line
	9500 7000 9500 9300
Wire Wire Line
	9800 7000 9800 9300
Wire Wire Line
	10150 7000 10150 9300
Wire Wire Line
	10450 7000 10450 9300
Wire Wire Line
	9800 6650 9800 6800
Wire Wire Line
	10150 6650 10150 6800
Wire Wire Line
	10450 6650 10450 6800
Wire Wire Line
	9800 9500 9800 9650
Connection ~ 9500 9650
Wire Wire Line
	10150 9650 10150 9500
Connection ~ 9800 9650
Wire Wire Line
	10450 9650 10450 9500
Connection ~ 10150 9650
Connection ~ 9500 6650
Connection ~ 9200 6650
Connection ~ 9800 6650
Connection ~ 10150 6650
Connection ~ 9200 9650
Wire Wire Line
	9500 9500 9500 9650
Wire Wire Line
	9500 6650 9500 6800
Wire Wire Line
	10900 7000 10900 9300
Wire Wire Line
	11200 7000 11200 9300
Wire Wire Line
	11550 7000 11550 9300
Wire Wire Line
	11850 7000 11850 9300
Wire Wire Line
	11200 6650 11200 6800
Connection ~ 10900 6650
Wire Wire Line
	11550 6650 11550 6800
Connection ~ 11200 6650
Wire Wire Line
	11850 6650 11850 6800
Connection ~ 11550 6650
Wire Wire Line
	11200 9500 11200 9650
Connection ~ 10900 9650
Wire Wire Line
	11550 9650 11550 9500
Connection ~ 11200 9650
Wire Wire Line
	11850 9650 11850 9500
Connection ~ 11550 9650
Wire Wire Line
	12150 7000 12150 9300
Wire Wire Line
	12450 7000 12450 9300
Wire Wire Line
	12800 7000 12800 9300
Wire Wire Line
	13100 7000 13100 9300
Wire Wire Line
	12450 6650 12450 6800
Wire Wire Line
	12800 6650 12800 6800
Wire Wire Line
	13100 6650 13100 6800
Wire Wire Line
	12450 9500 12450 9650
Connection ~ 12150 9650
Wire Wire Line
	12800 9650 12800 9500
Connection ~ 12450 9650
Wire Wire Line
	13100 9650 13100 9500
Connection ~ 12800 9650
Connection ~ 12150 6650
Connection ~ 11850 6650
Connection ~ 12450 6650
Connection ~ 12800 6650
Connection ~ 11850 9650
Wire Wire Line
	12150 9500 12150 9650
Wire Wire Line
	12150 6650 12150 6800
Connection ~ 10450 9650
Wire Wire Line
	10900 9500 10900 9650
Connection ~ 10450 6650
Wire Wire Line
	10900 6650 10900 6800
Wire Wire Line
	7750 8600 8250 8600
Connection ~ 8250 8600
NoConn ~ 7750 8700
NoConn ~ 7750 8800
NoConn ~ 7750 8900
NoConn ~ 7750 9000
Wire Wire Line
	7750 8500 8550 8500
Connection ~ 8550 8500
Wire Wire Line
	7750 8400 8900 8400
Connection ~ 8900 8400
Wire Wire Line
	7750 8300 9200 8300
Connection ~ 9200 8300
Wire Wire Line
	7750 8200 9500 8200
Connection ~ 9500 8200
Wire Wire Line
	7750 8100 9800 8100
Connection ~ 9800 8100
Wire Wire Line
	7750 8000 10150 8000
Connection ~ 10150 8000
Wire Wire Line
	7750 7900 10450 7900
Connection ~ 10450 7900
Wire Wire Line
	7750 7800 10900 7800
Connection ~ 10900 7800
Wire Wire Line
	7750 7700 11200 7700
Connection ~ 11200 7700
Wire Wire Line
	7750 7600 11550 7600
Connection ~ 11550 7600
Wire Wire Line
	7750 7500 11850 7500
Connection ~ 11850 7500
Wire Wire Line
	7750 7400 12150 7400
Connection ~ 12150 7400
Wire Wire Line
	7750 7300 12450 7300
Connection ~ 12450 7300
Wire Wire Line
	7750 7200 12800 7200
Connection ~ 12800 7200
Wire Wire Line
	7750 7100 13100 7100
Connection ~ 13100 7100
$EndSCHEMATC