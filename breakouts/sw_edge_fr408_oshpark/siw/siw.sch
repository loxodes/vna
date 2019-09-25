EESchema Schematic File Version 4
EELAYER 30 0
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
L synth_lib:band_pass_filter FL101
U 1 1 5D880627
P 4950 2550
F 0 "FL101" H 4950 2865 50  0000 C CNN
F 1 "band_pass_filter" H 4950 2774 50  0000 C CNN
F 2 "vna_footprints:band_x2_siw_fr408_6p7mil" H 4850 2700 50  0001 C CNN
F 3 "" H 4850 2700 50  0001 C CNN
	1    4950 2550
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_Coaxial J101
U 1 1 5D880968
P 3900 2550
F 0 "J101" H 3828 2788 50  0000 C CNN
F 1 "Conn_Coaxial" H 3828 2697 50  0000 C CNN
F 2 "vna_mm:sw_edge_oshpark_4layer" H 3900 2550 50  0001 C CNN
F 3 " ~" H 3900 2550 50  0001 C CNN
	1    3900 2550
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 5D881799
P 3900 3100
F 0 "#PWR0101" H 3900 2850 50  0001 C CNN
F 1 "GND" H 3905 2927 50  0000 C CNN
F 2 "" H 3900 3100 50  0001 C CNN
F 3 "" H 3900 3100 50  0001 C CNN
	1    3900 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 3100 3900 2750
Wire Wire Line
	4100 2550 4350 2550
$Comp
L power:GND #PWR0102
U 1 1 5D88200B
P 4950 3100
F 0 "#PWR0102" H 4950 2850 50  0001 C CNN
F 1 "GND" H 4955 2927 50  0000 C CNN
F 2 "" H 4950 3100 50  0001 C CNN
F 3 "" H 4950 3100 50  0001 C CNN
	1    4950 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	4950 3100 4950 3000
$Comp
L power:GND #PWR0103
U 1 1 5D882482
P 5850 3100
F 0 "#PWR0103" H 5850 2850 50  0001 C CNN
F 1 "GND" H 5855 2927 50  0000 C CNN
F 2 "" H 5850 3100 50  0001 C CNN
F 3 "" H 5850 3100 50  0001 C CNN
	1    5850 3100
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_Coaxial J102
U 1 1 5D88288F
P 5850 2550
F 0 "J102" H 5950 2525 50  0000 L CNN
F 1 "Conn_Coaxial" H 5950 2434 50  0000 L CNN
F 2 "vna_mm:sw_edge_oshpark_4layer" H 5850 2550 50  0001 C CNN
F 3 " ~" H 5850 2550 50  0001 C CNN
	1    5850 2550
	1    0    0    -1  
$EndComp
Wire Wire Line
	5550 2550 5650 2550
Wire Wire Line
	5850 2750 5850 3100
$EndSCHEMATC
