EESchema Schematic File Version 5
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 13
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
Comment5 ""
Comment6 ""
Comment7 ""
Comment8 ""
Comment9 ""
$EndDescr
Text HLabel 4900 1600 0    60   Input ~ 0
SYNTH_OUT
Text HLabel 4900 2700 0    60   Input ~ 0
SYNC
$Comp
L power:GND #PWR0301
U 1 1 5AB94285
P 5850 1900
F 0 "#PWR0301" H 5850 1650 50  0001 C CNN
F 1 "GND" H 5850 1750 50  0000 C CNN
F 2 "" H 5850 1900 50  0001 C CNN
F 3 "" H 5850 1900 50  0001 C CNN
	1    5850 1900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0302
U 1 1 5ABBB807
P 5850 3000
F 0 "#PWR0302" H 5850 2750 50  0001 C CNN
F 1 "GND" H 5850 2850 50  0000 C CNN
F 2 "" H 5850 3000 50  0001 C CNN
F 3 "" H 5850 3000 50  0001 C CNN
	1    5850 3000
	1    0    0    -1  
$EndComp
Wire Wire Line
	5300 1600 5650 1600
Wire Wire Line
	5300 2700 5650 2700
Wire Wire Line
	4900 1600 5100 1600
Wire Wire Line
	5100 2700 4900 2700
$Comp
L Device:C_Small C302
U 1 1 5AC31626
P 5200 2700
F 0 "C302" H 5210 2770 50  0000 L CNN
F 1 "10 pF" H 5210 2620 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 5200 2700 50  0001 C CNN
F 3 "" H 5200 2700 50  0001 C CNN
	1    5200 2700
	0    1    1    0   
$EndComp
$Comp
L Device:C_Small C301
U 1 1 5AC31536
P 5200 1600
F 0 "C301" H 5210 1670 50  0000 L CNN
F 1 "10 pF" H 5210 1520 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 5200 1600 50  0001 C CNN
F 3 "" H 5200 1600 50  0001 C CNN
	1    5200 1600
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_Coaxial J301
U 1 1 5D641233
P 5850 1600
F 0 "J301" H 5950 1575 50  0000 L CNN
F 1 "Conn_Coaxial" H 5950 1484 50  0000 L CNN
F 2 "vna_mm:sw_edge_ro4350b_10mil" H 5850 1600 50  0001 C CNN
F 3 " ~" H 5850 1600 50  0001 C CNN
	1    5850 1600
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_Coaxial J302
U 1 1 5D64149F
P 5850 2700
F 0 "J302" H 5950 2675 50  0000 L CNN
F 1 "Conn_Coaxial" H 5950 2584 50  0000 L CNN
F 2 "Connector_Coaxial:SMA_Amphenol_132203-12_Horizontal" H 5850 2700 50  0001 C CNN
F 3 " ~" H 5850 2700 50  0001 C CNN
	1    5850 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	5850 1800 5850 1900
Wire Wire Line
	5850 3000 5850 2900
$EndSCHEMATC
