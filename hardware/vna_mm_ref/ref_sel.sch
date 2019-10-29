EESchema Schematic File Version 4
LIBS:vna_mm_ref-cache
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
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
P 3300 8900
AR Path="/5DC43248" Ref="U?"  Part="1" 
AR Path="/5DC3C92E/5DC43248" Ref="U?"  Part="1" 
F 0 "U?" H 2450 9400 50  0000 L CNN
F 1 "DOCAT050F-010.0M" H 2450 9300 50  0000 L CNN
F 2 "" H 3300 8900 50  0001 C CNN
F 3 "http://www.conwin.com/datasheets/cx/cx275.pdf" H 3300 8900 50  0001 C CNN
	1    3300 8900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC4324E
P 3300 9500
AR Path="/5DC4324E" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC4324E" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 3300 9250 50  0001 C CNN
F 1 "GND" H 3305 9327 50  0000 C CNN
F 2 "" H 3300 9500 50  0001 C CNN
F 3 "" H 3300 9500 50  0001 C CNN
	1    3300 9500
	1    0    0    -1  
$EndComp
Wire Wire Line
	3300 9400 3300 9500
$Comp
L Connector:Conn_Coaxial J?
U 1 1 5DC43255
P 1400 4300
AR Path="/5DC43255" Ref="J?"  Part="1" 
AR Path="/5DC3C92E/5DC43255" Ref="J?"  Part="1" 
F 0 "J?" H 1328 4538 50  0000 C CNN
F 1 "Conn_Coaxial" H 1328 4447 50  0000 C CNN
F 2 "" H 1400 4300 50  0001 C CNN
F 3 " ~" H 1400 4300 50  0001 C CNN
	1    1400 4300
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC4325B
P 1400 4600
AR Path="/5DC4325B" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC4325B" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 1400 4350 50  0001 C CNN
F 1 "GND" H 1405 4427 50  0000 C CNN
F 2 "" H 1400 4600 50  0001 C CNN
F 3 "" H 1400 4600 50  0001 C CNN
	1    1400 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	1400 4500 1400 4600
$Comp
L vna_mm:TPS22918 U?
U 1 1 5DC43262
P 2300 7200
AR Path="/5DC43262" Ref="U?"  Part="1" 
AR Path="/5DC3C92E/5DC43262" Ref="U?"  Part="1" 
F 0 "U?" H 2300 7665 50  0000 C CNN
F 1 "TPS22918" H 2300 7574 50  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-23-6" H 2250 7750 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/tps22918.pdf" H 2300 7500 50  0001 C CNN
	1    2300 7200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC43268
P 2300 7800
AR Path="/5DC43268" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC43268" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 2300 7550 50  0001 C CNN
F 1 "GND" H 2305 7627 50  0000 C CNN
F 2 "" H 2300 7800 50  0001 C CNN
F 3 "" H 2300 7800 50  0001 C CNN
	1    2300 7800
	1    0    0    -1  
$EndComp
Wire Wire Line
	2300 7700 2300 7800
$Comp
L power:+3V3 #PWR?
U 1 1 5DC4326F
P 1450 6850
AR Path="/5DC4326F" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC4326F" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 1450 6700 50  0001 C CNN
F 1 "+3V3" H 1465 7023 50  0000 C CNN
F 2 "" H 1450 6850 50  0001 C CNN
F 3 "" H 1450 6850 50  0001 C CNN
	1    1450 6850
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 7000 1450 7000
Wire Wire Line
	1450 7000 1450 6850
$Comp
L Device:C_Small C?
U 1 1 5DC43277
P 3700 8000
AR Path="/5DC43277" Ref="C?"  Part="1" 
AR Path="/5DC3C92E/5DC43277" Ref="C?"  Part="1" 
F 0 "C?" H 3792 8046 50  0000 L CNN
F 1 "2.2 uF" H 3792 7955 50  0000 L CNN
F 2 "" H 3700 8000 50  0001 C CNN
F 3 "~" H 3700 8000 50  0001 C CNN
	1    3700 8000
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C?
U 1 1 5DC4327D
P 4200 8000
AR Path="/5DC4327D" Ref="C?"  Part="1" 
AR Path="/5DC3C92E/5DC4327D" Ref="C?"  Part="1" 
F 0 "C?" H 4292 8046 50  0000 L CNN
F 1 "100 nF" H 4292 7955 50  0000 L CNN
F 2 "" H 4200 8000 50  0001 C CNN
F 3 "~" H 4200 8000 50  0001 C CNN
	1    4200 8000
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C?
U 1 1 5DC43283
P 4700 8000
AR Path="/5DC43283" Ref="C?"  Part="1" 
AR Path="/5DC3C92E/5DC43283" Ref="C?"  Part="1" 
F 0 "C?" H 4792 8046 50  0000 L CNN
F 1 "100 pF" H 4792 7955 50  0000 L CNN
F 2 "" H 4700 8000 50  0001 C CNN
F 3 "~" H 4700 8000 50  0001 C CNN
	1    4700 8000
	1    0    0    -1  
$EndComp
NoConn ~ 2750 7400
NoConn ~ 2750 7200
$Comp
L Device:L_Small L?
U 1 1 5DC4328B
P 3300 7550
AR Path="/5DC4328B" Ref="L?"  Part="1" 
AR Path="/5DC3C92E/5DC4328B" Ref="L?"  Part="1" 
F 0 "L?" H 3348 7596 50  0000 L CNN
F 1 "L_Small" H 3348 7505 50  0000 L CNN
F 2 "" H 3300 7550 50  0001 C CNN
F 3 "~" H 3300 7550 50  0001 C CNN
	1    3300 7550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC43291
P 3700 8150
AR Path="/5DC43291" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC43291" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 3700 7900 50  0001 C CNN
F 1 "GND" H 3705 7977 50  0000 C CNN
F 2 "" H 3700 8150 50  0001 C CNN
F 3 "" H 3700 8150 50  0001 C CNN
	1    3700 8150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3700 8100 3700 8150
$Comp
L power:GND #PWR?
U 1 1 5DC43298
P 4200 8150
AR Path="/5DC43298" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC43298" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 4200 7900 50  0001 C CNN
F 1 "GND" H 4205 7977 50  0000 C CNN
F 2 "" H 4200 8150 50  0001 C CNN
F 3 "" H 4200 8150 50  0001 C CNN
	1    4200 8150
	1    0    0    -1  
$EndComp
Wire Wire Line
	4200 8150 4200 8100
Text Notes 2800 6900 0    50   ~ 0
760 mA turn on,\n340 mA steady state
Wire Wire Line
	2750 7000 3300 7000
Wire Wire Line
	3300 7000 3300 7450
Wire Wire Line
	3300 7650 3300 7800
$Comp
L power:GND #PWR?
U 1 1 5DC432A3
P 4700 8150
AR Path="/5DC432A3" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC432A3" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 4700 7900 50  0001 C CNN
F 1 "GND" H 4705 7977 50  0000 C CNN
F 2 "" H 4700 8150 50  0001 C CNN
F 3 "" H 4700 8150 50  0001 C CNN
	1    4700 8150
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 8100 4700 8150
Wire Wire Line
	3300 7800 3700 7800
Wire Wire Line
	3700 7800 3700 7900
Connection ~ 3300 7800
Wire Wire Line
	3300 7800 3300 8400
Wire Wire Line
	3700 7800 4200 7800
Wire Wire Line
	4200 7800 4200 7900
Connection ~ 3700 7800
Wire Wire Line
	4200 7800 4700 7800
Wire Wire Line
	4700 7800 4700 7900
Connection ~ 4200 7800
Wire Wire Line
	1850 7400 1450 7400
$Comp
L Device:R_Small R?
U 1 1 5DC432B5
P 1450 7200
AR Path="/5DC432B5" Ref="R?"  Part="1" 
AR Path="/5DC3C92E/5DC432B5" Ref="R?"  Part="1" 
F 0 "R?" H 1509 7246 50  0000 L CNN
F 1 "10k" H 1509 7155 50  0000 L CNN
F 2 "" H 1450 7200 50  0001 C CNN
F 3 "~" H 1450 7200 50  0001 C CNN
	1    1450 7200
	1    0    0    -1  
$EndComp
Wire Wire Line
	1450 7300 1450 7400
Wire Wire Line
	1450 7100 1450 7000
Connection ~ 1450 7000
Wire Wire Line
	1450 7400 1350 7400
Connection ~ 1450 7400
$Comp
L Device:C_Small C?
U 1 1 5DC432C1
P 2050 4300
AR Path="/5DC432C1" Ref="C?"  Part="1" 
AR Path="/5DC3C92E/5DC432C1" Ref="C?"  Part="1" 
F 0 "C?" V 1821 4300 50  0000 C CNN
F 1 "C_Small" V 1912 4300 50  0000 C CNN
F 2 "" H 2050 4300 50  0001 C CNN
F 3 "~" H 2050 4300 50  0001 C CNN
	1    2050 4300
	0    1    1    0   
$EndComp
$Comp
L Device:C_Small C?
U 1 1 5DC432C7
P 2300 4750
AR Path="/5DC432C7" Ref="C?"  Part="1" 
AR Path="/5DC3C92E/5DC432C7" Ref="C?"  Part="1" 
F 0 "C?" H 2208 4704 50  0000 R CNN
F 1 "C_Small" H 2208 4795 50  0000 R CNN
F 2 "" H 2300 4750 50  0001 C CNN
F 3 "~" H 2300 4750 50  0001 C CNN
	1    2300 4750
	-1   0    0    1   
$EndComp
Text Notes 2050 3900 0    50   ~ 0
TODO: 100 MHZ BPF?\nTODO: ESD?
Wire Wire Line
	1600 4300 1950 4300
Wire Wire Line
	3800 8900 4000 8900
Text Notes 1600 1400 0    118  ~ 0
Use small signal relay for 10 MHz input reference?\n1-1462051-1 , 62 mA, DRV8833CRTER as driver?\n
$Comp
L Interface:LTC6957xDD-3 U?
U 1 1 5DC432D3
P 12050 4850
AR Path="/5DC432D3" Ref="U?"  Part="1" 
AR Path="/5DC3C92E/5DC432D3" Ref="U?"  Part="1" 
F 0 "U?" H 11300 5550 50  0000 L CNN
F 1 "LTC6957xDD-3" H 11300 5450 50  0000 L CNN
F 2 "Package_DFN_QFN:DFN-12-1EP_3x3mm_P0.45mm_EP1.66x2.38mm" H 12050 4200 50  0001 C CNN
F 3 "https://www.analog.com/media/en/technical-documentation/data-sheets/6957fb.pdf" H 12050 4850 50  0001 C CNN
	1    12050 4850
	1    0    0    -1  
$EndComp
Text HLabel 13350 3400 2    50   Output ~ 0
10MHZ_OUT
Text HLabel 1350 7400 0    50   Input ~ 0
INT_REF_EN
Text HLabel 4450 2100 0    50   Input ~ 0
REF_SEL
$Comp
L Connector:Conn_Coaxial J?
U 1 1 5DC47C83
P 13650 5000
AR Path="/5DC47C83" Ref="J?"  Part="1" 
AR Path="/5DC3C92E/5DC47C83" Ref="J?"  Part="1" 
F 0 "J?" H 13578 5238 50  0000 C CNN
F 1 "Conn_Coaxial" H 13578 5147 50  0000 C CNN
F 2 "" H 13650 5000 50  0001 C CNN
F 3 " ~" H 13650 5000 50  0001 C CNN
	1    13650 5000
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC47C89
P 13650 5300
AR Path="/5DC47C89" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DC47C89" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 13650 5050 50  0001 C CNN
F 1 "GND" H 13655 5127 50  0000 C CNN
F 2 "" H 13650 5300 50  0001 C CNN
F 3 "" H 13650 5300 50  0001 C CNN
	1    13650 5300
	-1   0    0    -1  
$EndComp
Wire Wire Line
	13650 5200 13650 5300
$Comp
L Driver_Motor:DRV8837C U?
U 1 1 5DB6D5DA
P 6150 2600
F 0 "U?" H 6150 2011 50  0000 C CNN
F 1 "DRV8837C" H 6150 1920 50  0000 C CNN
F 2 "Package_SON:WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm" H 6150 1750 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/drv8837c.pdf" H 6150 2600 50  0001 C CNN
	1    6150 2600
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DB81A9D
P 6550 6200
AR Path="/5DB81A9D" Ref="#PWR?"  Part="1" 
AR Path="/5DC3C92E/5DB81A9D" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 6550 5950 50  0001 C CNN
F 1 "GND" H 6555 6027 50  0000 C CNN
F 2 "" H 6550 6200 50  0001 C CNN
F 3 "" H 6550 6200 50  0001 C CNN
	1    6550 6200
	-1   0    0    -1  
$EndComp
Wire Wire Line
	6550 6150 6550 6200
$Comp
L vna_mm:1-1462051-1 K?
U 1 1 5DB84685
P 6500 5650
F 0 "K?" H 6450 6217 50  0000 C CNN
F 1 "1-1462051-1" H 6450 6126 50  0000 C CNN
F 2 "Relay_SMD:Relay_SPDT_AXICOM_HF3Series_50ohms_Pitch1.27mm" H 6050 6200 50  0001 L CNN
F 3 "https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=108-98000&DocType=SS&DocLang=EN" V 6050 5650 50  0001 C CNN
	1    6500 5650
	-1   0    0    -1  
$EndComp
$EndSCHEMATC
