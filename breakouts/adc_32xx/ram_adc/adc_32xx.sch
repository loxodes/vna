EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 5
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 7000 7200 2700 1250
U 5E9E6BF0
F0 "input_match_b" 50
F1 "adc_frontend_A.sch" 50
F2 "VCM" I R 9700 7850 50 
F3 "OUT_P" O R 9700 7700 50 
F4 "OUT_N" O R 9700 8000 50 
$EndSheet
Wire Wire Line
	9700 6100 10100 6100
Wire Wire Line
	9700 6400 10100 6400
Wire Wire Line
	9700 7700 10100 7700
Wire Wire Line
	9700 8000 10100 8000
Wire Wire Line
	9700 7850 9750 7850
Text Label 9750 7850 0    50   ~ 0
VCM
Wire Wire Line
	9700 6250 9800 6250
Text Label 9800 6250 0    50   ~ 0
VCM
Text Label 10000 7050 2    50   ~ 0
VCM
Wire Wire Line
	10000 7050 10100 7050
$Sheet
S 7000 9000 2650 900 
U 5ED11961
F0 "power" 50
F1 "power.sch" 50
F2 "EN" I R 9650 9200 50 
$EndSheet
Wire Wire Line
	10100 9200 9650 9200
$Sheet
S 7000 5600 2700 1250
U 5E9D5B60
F0 "input_match_A" 50
F1 "adc_frontend_A.sch" 50
F2 "VCM" I R 9700 6250 50 
F3 "OUT_P" O R 9700 6100 50 
F4 "OUT_N" O R 9700 6400 50 
$EndSheet
$Sheet
S 10100 5250 1650 4050
U 5E9D7371
F0 "adc" 50
F1 "adc.sch" 50
F2 "IN_A_P" I L 10100 6100 50 
F3 "IN_A_N" I L 10100 6400 50 
F4 "IN_B_N" I L 10100 8000 50 
F5 "IN_B_P" I L 10100 7700 50 
F6 "VCM" I L 10100 7050 50 
F7 "EN" O L 10100 9200 50 
$EndSheet
$EndSCHEMATC
