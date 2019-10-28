EESchema Schematic File Version 4
LIBS:vna_mm_ref-cache
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 4 5
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
L vna_mm:DOCAT U?
U 1 1 5DC43248
P 4550 6650
AR Path="/5DC43248" Ref="U?"  Part="1" 
AR Path="/5DC3C92E/5DC43248" Ref="U?"  Part="1" 
F 0 "U?" H 3700 7150 50  0000 L CNN
F 1 "DOCAT050F-010.0M" H 3700 7050 50  0000 L CNN
F 2 "" H 4550 6650 50  0001 C CNN
F 3 "http://www.conwin.com/datasheets/cx/cx275.pdf" H 4550 6650 50  0001 C CNN
	1    4550 6650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC4324E
P 4550 7250
AR Path="/5DC4324E" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC4324E" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 4550 7000 50  0001 C CNN
F 1 "GND" H 4555 7077 50  0000 C CNN
F 2 "" H 4550 7250 50  0001 C CNN
F 3 "" H 4550 7250 50  0001 C CNN
	1    4550 7250
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 7150 4550 7250
$Comp
L Connector:Conn_Coaxial J?
U 1 1 5DC43255
P 2800 1150
AR Path="/5DC43255" Ref="J?"  Part="1" 
AR Path="/5DC3C92E/5DC43255" Ref="J?"  Part="1" 
F 0 "J?" H 2728 1388 50  0000 C CNN
F 1 "Conn_Coaxial" H 2728 1297 50  0000 C CNN
F 2 "" H 2800 1150 50  0001 C CNN
F 3 " ~" H 2800 1150 50  0001 C CNN
	1    2800 1150
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC4325B
P 2800 1450
AR Path="/5DC4325B" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC4325B" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 2800 1200 50  0001 C CNN
F 1 "GND" H 2805 1277 50  0000 C CNN
F 2 "" H 2800 1450 50  0001 C CNN
F 3 "" H 2800 1450 50  0001 C CNN
	1    2800 1450
	1    0    0    -1  
$EndComp
Wire Wire Line
	2800 1350 2800 1450
$Comp
L vna_mm:TPS22918 U?
U 1 1 5DC43262
P 3550 4950
AR Path="/5DC43262" Ref="U?"  Part="1" 
AR Path="/5DC3C92E/5DC43262" Ref="U?"  Part="1" 
F 0 "U?" H 3550 5415 50  0000 C CNN
F 1 "TPS22918" H 3550 5324 50  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-23-6" H 3500 5500 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/tps22918.pdf" H 3550 5250 50  0001 C CNN
	1    3550 4950
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC43268
P 3550 5550
AR Path="/5DC43268" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC43268" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 3550 5300 50  0001 C CNN
F 1 "GND" H 3555 5377 50  0000 C CNN
F 2 "" H 3550 5550 50  0001 C CNN
F 3 "" H 3550 5550 50  0001 C CNN
	1    3550 5550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3550 5450 3550 5550
$Comp
L power:+3V3 #PWR?
U 1 1 5DC4326F
P 2700 4600
AR Path="/5DC4326F" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC4326F" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 2700 4450 50  0001 C CNN
F 1 "+3V3" H 2715 4773 50  0000 C CNN
F 2 "" H 2700 4600 50  0001 C CNN
F 3 "" H 2700 4600 50  0001 C CNN
	1    2700 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 4750 2700 4750
Wire Wire Line
	2700 4750 2700 4600
$Comp
L Device:C_Small C?
U 1 1 5DC43277
P 4950 5750
AR Path="/5DC43277" Ref="C?"  Part="1" 
AR Path="/5DC3C92E/5DC43277" Ref="C?"  Part="1" 
F 0 "C?" H 5042 5796 50  0000 L CNN
F 1 "2.2 uF" H 5042 5705 50  0000 L CNN
F 2 "" H 4950 5750 50  0001 C CNN
F 3 "~" H 4950 5750 50  0001 C CNN
	1    4950 5750
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C?
U 1 1 5DC4327D
P 5450 5750
AR Path="/5DC4327D" Ref="C?"  Part="1" 
AR Path="/5DC3C92E/5DC4327D" Ref="C?"  Part="1" 
F 0 "C?" H 5542 5796 50  0000 L CNN
F 1 "100 nF" H 5542 5705 50  0000 L CNN
F 2 "" H 5450 5750 50  0001 C CNN
F 3 "~" H 5450 5750 50  0001 C CNN
	1    5450 5750
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C?
U 1 1 5DC43283
P 5950 5750
AR Path="/5DC43283" Ref="C?"  Part="1" 
AR Path="/5DC3C92E/5DC43283" Ref="C?"  Part="1" 
F 0 "C?" H 6042 5796 50  0000 L CNN
F 1 "100 pF" H 6042 5705 50  0000 L CNN
F 2 "" H 5950 5750 50  0001 C CNN
F 3 "~" H 5950 5750 50  0001 C CNN
	1    5950 5750
	1    0    0    -1  
$EndComp
NoConn ~ 4000 5150
NoConn ~ 4000 4950
$Comp
L Device:L_Small L?
U 1 1 5DC4328B
P 4550 5300
AR Path="/5DC4328B" Ref="L?"  Part="1" 
AR Path="/5DC3C92E/5DC4328B" Ref="L?"  Part="1" 
F 0 "L?" H 4598 5346 50  0000 L CNN
F 1 "L_Small" H 4598 5255 50  0000 L CNN
F 2 "" H 4550 5300 50  0001 C CNN
F 3 "~" H 4550 5300 50  0001 C CNN
	1    4550 5300
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC43291
P 4950 5900
AR Path="/5DC43291" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC43291" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 4950 5650 50  0001 C CNN
F 1 "GND" H 4955 5727 50  0000 C CNN
F 2 "" H 4950 5900 50  0001 C CNN
F 3 "" H 4950 5900 50  0001 C CNN
	1    4950 5900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4950 5850 4950 5900
$Comp
L power:GND #PWR?
U 1 1 5DC43298
P 5450 5900
AR Path="/5DC43298" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC43298" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 5450 5650 50  0001 C CNN
F 1 "GND" H 5455 5727 50  0000 C CNN
F 2 "" H 5450 5900 50  0001 C CNN
F 3 "" H 5450 5900 50  0001 C CNN
	1    5450 5900
	1    0    0    -1  
$EndComp
Wire Wire Line
	5450 5900 5450 5850
Text Notes 4050 4650 0    50   ~ 0
760 mA turn on,\n340 mA steady state
Wire Wire Line
	4000 4750 4550 4750
Wire Wire Line
	4550 4750 4550 5200
Wire Wire Line
	4550 5400 4550 5550
$Comp
L power:GND #PWR?
U 1 1 5DC432A3
P 5950 5900
AR Path="/5DC432A3" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC432A3" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 5950 5650 50  0001 C CNN
F 1 "GND" H 5955 5727 50  0000 C CNN
F 2 "" H 5950 5900 50  0001 C CNN
F 3 "" H 5950 5900 50  0001 C CNN
	1    5950 5900
	1    0    0    -1  
$EndComp
Wire Wire Line
	5950 5850 5950 5900
Wire Wire Line
	4550 5550 4950 5550
Wire Wire Line
	4950 5550 4950 5650
Connection ~ 4550 5550
Wire Wire Line
	4550 5550 4550 6150
Wire Wire Line
	4950 5550 5450 5550
Wire Wire Line
	5450 5550 5450 5650
Connection ~ 4950 5550
Wire Wire Line
	5450 5550 5950 5550
Wire Wire Line
	5950 5550 5950 5650
Connection ~ 5450 5550
Wire Wire Line
	3100 5150 2700 5150
$Comp
L Device:R_Small R?
U 1 1 5DC432B5
P 2700 4950
AR Path="/5DC432B5" Ref="R?"  Part="1" 
AR Path="/5DC3C92E/5DC432B5" Ref="R?"  Part="1" 
F 0 "R?" H 2759 4996 50  0000 L CNN
F 1 "10k" H 2759 4905 50  0000 L CNN
F 2 "" H 2700 4950 50  0001 C CNN
F 3 "~" H 2700 4950 50  0001 C CNN
	1    2700 4950
	1    0    0    -1  
$EndComp
Wire Wire Line
	2700 5050 2700 5150
Wire Wire Line
	2700 4850 2700 4750
Connection ~ 2700 4750
Wire Wire Line
	2700 5150 2600 5150
Connection ~ 2700 5150
$Comp
L Device:C_Small C?
U 1 1 5DC432C1
P 3450 1150
AR Path="/5DC432C1" Ref="C?"  Part="1" 
AR Path="/5DC3C92E/5DC432C1" Ref="C?"  Part="1" 
F 0 "C?" V 3221 1150 50  0000 C CNN
F 1 "C_Small" V 3312 1150 50  0000 C CNN
F 2 "" H 3450 1150 50  0001 C CNN
F 3 "~" H 3450 1150 50  0001 C CNN
	1    3450 1150
	0    1    1    0   
$EndComp
$Comp
L Device:C_Small C?
U 1 1 5DC432C7
P 3800 1400
AR Path="/5DC432C7" Ref="C?"  Part="1" 
AR Path="/5DC3C92E/5DC432C7" Ref="C?"  Part="1" 
F 0 "C?" H 3708 1354 50  0000 R CNN
F 1 "C_Small" H 3708 1445 50  0000 R CNN
F 2 "" H 3800 1400 50  0001 C CNN
F 3 "~" H 3800 1400 50  0001 C CNN
	1    3800 1400
	-1   0    0    1   
$EndComp
Text Notes 3450 750  0    50   ~ 0
TODO: 100 MHZ BPF?\nTODO: ESD?
Wire Wire Line
	3000 1150 3350 1150
Wire Wire Line
	5050 6650 5250 6650
Text Notes 2500 3400 0    50   ~ 0
TODO:\nFIND LOW ADDITIVE PHASE NOISE CLOCK SWITCH, HIGH ISOLATION..\nPROVIDE 2X 10 MHZ OUTPUTS
Text Notes 5900 1900 0    50   ~ 0
CDCLV1104 BUFFER?\n4:1 (3 outputs 10 MHz, 2 ouputs 100 MHz)\nSI5330x?\nICS8305L
Text Notes 3350 1400 0    118  ~ 0
Use small signal relay for 10 MHz input reference?
$Comp
L Interface:LTC6957xDD-3 U?
U 1 1 5DC432D3
P 5550 2300
AR Path="/5DC432D3" Ref="U?"  Part="1" 
AR Path="/5DC3C92E/5DC432D3" Ref="U?"  Part="1" 
F 0 "U?" H 4800 3000 50  0000 L CNN
F 1 "LTC6957xDD-3" H 4800 2900 50  0000 L CNN
F 2 "Package_DFN_QFN:DFN-12-1EP_3x3mm_P0.45mm_EP1.66x2.38mm" H 5550 1650 50  0001 C CNN
F 3 "https://www.analog.com/media/en/technical-documentation/data-sheets/6957fb.pdf" H 5550 2300 50  0001 C CNN
	1    5550 2300
	1    0    0    -1  
$EndComp
Text HLabel 10050 3250 2    50   Output ~ 0
10MHZ_OUT
Text HLabel 2600 5150 0    50   Input ~ 0
INT_REF_EN
Text HLabel 2550 5500 0    50   Input ~ 0
REF_SEL
$Comp
L Connector:Conn_Coaxial J?
U 1 1 5DC47C76
P 8050 3850
F 0 "J?" H 7978 4088 50  0000 C CNN
F 1 "Conn_Coaxial" H 7978 3997 50  0000 C CNN
F 2 "" H 8050 3850 50  0001 C CNN
F 3 " ~" H 8050 3850 50  0001 C CNN
	1    8050 3850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC47C7C
P 8050 4150
F 0 "#PWR?" H 8050 3900 50  0001 C CNN
F 1 "GND" H 8055 3977 50  0000 C CNN
F 2 "" H 8050 4150 50  0001 C CNN
F 3 "" H 8050 4150 50  0001 C CNN
	1    8050 4150
	-1   0    0    -1  
$EndComp
Wire Wire Line
	8050 4050 8050 4150
$Comp
L Connector:Conn_Coaxial J?
U 1 1 5DC47C83
P 8050 5350
F 0 "J?" H 7978 5588 50  0000 C CNN
F 1 "Conn_Coaxial" H 7978 5497 50  0000 C CNN
F 2 "" H 8050 5350 50  0001 C CNN
F 3 " ~" H 8050 5350 50  0001 C CNN
	1    8050 5350
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC47C89
P 8050 5650
F 0 "#PWR?" H 8050 5400 50  0001 C CNN
F 1 "GND" H 8055 5477 50  0000 C CNN
F 2 "" H 8050 5650 50  0001 C CNN
F 3 "" H 8050 5650 50  0001 C CNN
	1    8050 5650
	-1   0    0    -1  
$EndComp
Wire Wire Line
	8050 5550 8050 5650
$EndSCHEMATC
