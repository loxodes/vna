EESchema Schematic File Version 4
LIBS:vna_mm_ref-cache
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
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
Text Notes 4650 1200 0    50   ~ 0
Goals:\n10 MHz input or internal OCXO\nthree 100 MHz outputs, one 10 MHz output\nenclosure & 3D model\nphase noise that doesn't limit the TI LMX2595\nsmt test points for loop filter reponse
$Sheet
S 7200 1750 1250 2900
U 5DBF0563
F0 "output_buffer" 50
F1 "output_buffer.sch" 50
F2 "REF_100MHZ_IN" I L 7200 3000 50 
F3 "FILTA" I L 7200 4350 50 
F4 "FILTB" I L 7200 4450 50 
F5 "SD1_100MHZ" I L 7200 4150 50 
F6 "SD2_100MHZ" I L 7200 4250 50 
$EndSheet
$Sheet
S 5200 1750 1250 2900
U 5DC1A65E
F0 "synth_100MHz" 50
F1 "synth_100MHz.sch" 50
F2 "100MHZ_OUT" O R 6450 3000 50 
F3 "10MHZ_IN" I L 5200 3000 50 
F4 "PLL_EN" I L 5200 4350 50 
F5 "LKD" O R 6450 3950 50 
$EndSheet
$Sheet
S 3100 1750 1250 2900
U 5DC3C92E
F0 "ref_sel" 50
F1 "ref_sel.sch" 50
F2 "10MHZ_OUT" O R 4350 3000 50 
F3 "REF_SEL" I L 3100 4350 50 
F4 "FILTA" I L 3100 4200 50 
F5 "FILTB" I L 3100 4100 50 
F6 "SD1_10MHZ" I L 3100 3800 50 
F7 "SD2_10MHZ" I L 3100 3900 50 
F8 "RELAY_EN" I L 3100 3650 50 
$EndSheet
$Sheet
S 3100 5350 1950 1600
U 5DC45DA8
F0 "power_conn" 50
F1 "power_conn.sch" 50
F2 "RELAY_EN" O R 5050 5500 50 
F3 "SD_PLLCLK" O R 5050 5800 50 
F4 "SD_REFOUT" O R 5050 5900 50 
F5 "FILTA_REF" U R 5050 6000 50 
F6 "FILTB_REF" U R 5050 6100 50 
F7 "REF_SEL" O R 5050 5600 50 
F8 "PLL_EN" O R 5050 6350 50 
F9 "SD2_OUTPUT" O R 5050 6600 50 
F10 "FILTA_OUT" U R 5050 6700 50 
F11 "FILTB_OUT" U R 5050 6800 50 
F12 "SD1_OUTPUT" O R 5050 6500 50 
F13 "LKD_IN" I R 5050 6250 50 
$EndSheet
Text Notes 2900 1600 0    50   ~ 0
8.5 mm zheight, 850 mA peak, 400 mA typical
Text Notes 5200 1600 0    50   ~ 0
5.5 mm zheight, 40 mA
Wire Wire Line
	4350 3000 5200 3000
Wire Wire Line
	6450 3000 7200 3000
Text Notes 7250 1600 0    50   ~ 0
40 mA
Wire Wire Line
	5200 4350 5050 4350
Text Label 5050 4350 2    50   ~ 0
PLL_EN
Text Label 6550 3950 0    50   ~ 0
LKD
Wire Wire Line
	6550 3950 6450 3950
Text Label 7100 4150 2    50   ~ 0
SD1_OUTPUT
Wire Wire Line
	7100 4150 7200 4150
Text Label 7100 4250 2    50   ~ 0
SD2_OUTPUT
Text Label 7100 4450 2    50   ~ 0
FILTB_OUT
Wire Wire Line
	7100 4450 7200 4450
Wire Wire Line
	7100 4350 7200 4350
Text Label 7100 4350 2    50   ~ 0
FILTA_OUT
Wire Wire Line
	7100 4250 7200 4250
Text Label 2850 3800 2    50   ~ 0
SD_PLLCLK
Text Label 2850 3900 2    50   ~ 0
SD_REFOUT
Text Label 2850 4200 2    50   ~ 0
FILTB_REF
Text Label 2850 4100 2    50   ~ 0
FILTA_REF
Text Label 2850 3650 2    50   ~ 0
RELAY_EN
Text Label 2850 4350 2    50   ~ 0
REF_SEL
Wire Wire Line
	2850 4350 3100 4350
Wire Wire Line
	2850 4200 3100 4200
Wire Wire Line
	2850 4100 3100 4100
Wire Wire Line
	2850 3900 3100 3900
Wire Wire Line
	2850 3800 3100 3800
Wire Wire Line
	2850 3650 3100 3650
Text Label 5200 6500 0    50   ~ 0
SD1_OUTPUT
Text Label 5200 6600 0    50   ~ 0
SD2_OUTPUT
Text Label 5200 6800 0    50   ~ 0
FILTB_OUT
Text Label 5200 6700 0    50   ~ 0
FILTA_OUT
Text Label 5200 6350 0    50   ~ 0
PLL_EN
Text Label 5200 6250 0    50   ~ 0
LKD
Text Label 5200 5500 0    50   ~ 0
RELAY_EN
Text Label 5200 5600 0    50   ~ 0
REF_SEL
Text Label 5200 5800 0    50   ~ 0
SD_PLLCLK
Text Label 5200 5900 0    50   ~ 0
SD_REFOUT
Text Label 5200 6100 0    50   ~ 0
FILTB_REF
Text Label 5200 6000 0    50   ~ 0
FILTA_REF
Wire Wire Line
	5050 5500 5200 5500
Wire Wire Line
	5050 5600 5200 5600
Wire Wire Line
	5050 6250 5200 6250
Wire Wire Line
	5050 6350 5200 6350
Wire Wire Line
	5050 6500 5200 6500
Wire Wire Line
	5050 6600 5200 6600
Wire Wire Line
	5050 6700 5200 6700
Wire Wire Line
	5050 6800 5200 6800
Wire Wire Line
	5050 6000 5200 6000
Wire Wire Line
	5050 6100 5200 6100
Wire Wire Line
	5050 5900 5200 5900
Wire Wire Line
	5050 5800 5200 5800
$EndSCHEMATC
