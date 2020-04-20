EESchema Schematic File Version 4
LIBS:vna_mm_synth-cache
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 12 12
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 3000 3350 0    118  ~ 0
UCD9081
$Comp
L vna_mm:LTC2937 U?
U 1 1 5D7103A1
P 5450 3850
F 0 "U?" H 5450 4981 50  0000 C CNN
F 1 "LTC2937" H 5450 4890 50  0000 C CNN
F 2 "" H 5450 3850 50  0001 C CNN
F 3 "" H 5450 3850 50  0001 C CNN
	1    5450 3850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5D711A50
P 5450 4900
F 0 "#PWR?" H 5450 4650 50  0001 C CNN
F 1 "GND" H 5455 4727 50  0000 C CNN
F 2 "" H 5450 4900 50  0001 C CNN
F 3 "" H 5450 4900 50  0001 C CNN
	1    5450 4900
	1    0    0    -1  
$EndComp
Wire Wire Line
	5400 4800 5400 4850
Wire Wire Line
	5400 4850 5450 4850
Wire Wire Line
	5500 4850 5500 4800
Wire Wire Line
	5450 4850 5450 4900
Connection ~ 5450 4850
Wire Wire Line
	5450 4850 5500 4850
$EndSCHEMATC
