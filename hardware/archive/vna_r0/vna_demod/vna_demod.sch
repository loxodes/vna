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
LIBS:lmx2594
LIBS:ltc5549
LIBS:ad9864
LIBS:conn_sma_2gnd
LIBS:conn_sma
LIBS:txco
LIBS:nb3n551
LIBS:hmc475
LIBS:trf37b73
LIBS:mounting_hole
LIBS:mounting_box
LIBS:vna_demod-cache
EELAYER 25 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 8
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
S 2350 1600 2250 1800
U 593C5AAD
F0 "lo_synth" 60
F1 "lo_synth.sch" 60
F2 "LO_A" O R 4600 1900 60 
F3 "LO_B" O R 4600 2100 60 
F4 "LO_C" O R 4600 2300 60 
F5 "LO_D" O R 4600 2500 60 
F6 "SYNTH_REF" I L 2350 2050 60 
F7 "LMX_MUXout" O L 2350 2750 60 
F8 "LMX_SDI" I L 2350 2900 60 
F9 "LMX_SCK" I L 2350 3000 60 
F10 "LMX_CSB" I L 2350 3100 60 
F11 "LMX_CE" I L 2350 3200 60 
$EndSheet
$Sheet
S 6300 1700 1000 1700
U 593C5AB7
F0 "demod_A" 60
F1 "demod.sch" 60
F2 "ADC_CLK" I L 6300 2850 60 
F3 "RF_IN" I R 7300 1900 60 
F4 "LO_IN" I L 6300 1900 60 
F5 "IF_LO_REF" I L 6300 2750 60 
F6 "MIX_X2" I R 7300 3100 60 
F7 "MIX_EN" I R 7300 3200 60 
F8 "AD_PE" I R 7300 2900 60 
F9 "AD_PD" I R 7300 2800 60 
F10 "AD_PC" I R 7300 2700 60 
F11 "AD_DOUTB" I R 7300 2600 60 
F12 "AD_DOUTA" I R 7300 2500 60 
F13 "AD_FS" I R 7300 2400 60 
F14 "AD_SYNCB" I R 7300 2300 60 
F15 "AD_CLKOUT" I R 7300 2200 60 
$EndSheet
$Sheet
S 9900 1550 1450 3900
U 593C6727
F0 "conn_power" 60
F1 "conn_power.sch" 60
F2 "RF_A" O L 9900 1900 60 
F3 "RF_B" O L 9900 2200 60 
F4 "RF_C" O L 9900 2500 60 
F5 "RF_D" O L 9900 2800 60 
F6 "SYNTH_REF" O L 9900 3700 60 
F7 "IF_REF" O L 9900 3800 60 
F8 "ADC_CLK" O L 9900 3900 60 
F9 "ADC_CLK_EN" O R 11350 3000 60 
F10 "IF_REF_EN" O R 11350 3150 60 
F11 "MIX_X2" O R 11350 3300 60 
F12 "MIX_EN" O R 11350 3450 60 
F13 "AD_DOUT_A" I R 11350 3750 60 
F14 "AD_DOUT_B" I R 11350 3850 60 
F15 "AD_DOUT_C" I R 11350 3950 60 
F16 "AD_DOUT_D" I R 11350 4050 60 
F17 "AD_DOUTB" I R 11350 4150 60 
F18 "AD_PE_A" I R 11350 4250 60 
F19 "AD_PE_B" I R 11350 4350 60 
F20 "AD_PE_C" I R 11350 4450 60 
F21 "AD_PE_D" I R 11350 4550 60 
F22 "AD_PC" O R 11350 4650 60 
F23 "AD_PD" O R 11350 4750 60 
F24 "AD_CLKOUT" I R 11350 4850 60 
F25 "AD_FS" I R 11350 4950 60 
F26 "AD_SYNCB" O R 11350 5050 60 
F27 "LMX_CE" O R 11350 2200 60 
F28 "LMX_CSB" O R 11350 2300 60 
F29 "LMX_SDI" O R 11350 2400 60 
F30 "LMX_SCK" O R 11350 2500 60 
F31 "LMX_MUXout" I R 11350 2600 60 
$EndSheet
Wire Wire Line
	6300 1900 4600 1900
$Sheet
S 6300 3650 1000 1700
U 593E9862
F0 "demod_B" 60
F1 "demod.sch" 60
F2 "ADC_CLK" I L 6300 4800 60 
F3 "RF_IN" I R 7300 3850 60 
F4 "LO_IN" I L 6300 3850 60 
F5 "IF_LO_REF" I L 6300 4700 60 
F6 "MIX_X2" I R 7300 5050 60 
F7 "MIX_EN" I R 7300 5150 60 
F8 "AD_PE" I R 7300 4850 60 
F9 "AD_PD" I R 7300 4750 60 
F10 "AD_PC" I R 7300 4650 60 
F11 "AD_DOUTB" I R 7300 4550 60 
F12 "AD_DOUTA" I R 7300 4450 60 
F13 "AD_FS" I R 7300 4350 60 
F14 "AD_SYNCB" I R 7300 4250 60 
F15 "AD_CLKOUT" I R 7300 4150 60 
$EndSheet
$Sheet
S 6300 5550 1000 1700
U 593ECBE8
F0 "demod_C" 60
F1 "demod.sch" 60
F2 "ADC_CLK" I L 6300 6700 60 
F3 "RF_IN" I R 7300 5750 60 
F4 "LO_IN" I L 6300 5750 60 
F5 "IF_LO_REF" I L 6300 6600 60 
F6 "MIX_X2" I R 7300 6950 60 
F7 "MIX_EN" I R 7300 7050 60 
F8 "AD_PE" I R 7300 6750 60 
F9 "AD_PD" I R 7300 6650 60 
F10 "AD_PC" I R 7300 6550 60 
F11 "AD_DOUTB" I R 7300 6450 60 
F12 "AD_DOUTA" I R 7300 6350 60 
F13 "AD_FS" I R 7300 6250 60 
F14 "AD_SYNCB" I R 7300 6150 60 
F15 "AD_CLKOUT" I R 7300 6050 60 
$EndSheet
$Sheet
S 6300 7500 1000 1700
U 593ECBFA
F0 "demod_D" 60
F1 "demod.sch" 60
F2 "ADC_CLK" I L 6300 8650 60 
F3 "RF_IN" I R 7300 7700 60 
F4 "LO_IN" I L 6300 7700 60 
F5 "IF_LO_REF" I L 6300 8550 60 
F6 "MIX_X2" I R 7300 8900 60 
F7 "MIX_EN" I R 7300 9000 60 
F8 "AD_PE" I R 7300 8700 60 
F9 "AD_PD" I R 7300 8600 60 
F10 "AD_PC" I R 7300 8500 60 
F11 "AD_DOUTB" I R 7300 8400 60 
F12 "AD_DOUTA" I R 7300 8300 60 
F13 "AD_FS" I R 7300 8200 60 
F14 "AD_SYNCB" I R 7300 8100 60 
F15 "AD_CLKOUT" I R 7300 8000 60 
$EndSheet
Wire Wire Line
	4600 2100 5550 2100
Wire Wire Line
	5550 2100 5550 3850
Wire Wire Line
	5550 3850 6300 3850
Wire Wire Line
	4600 2300 5350 2300
Wire Wire Line
	5350 2300 5350 5750
Wire Wire Line
	5350 5750 6300 5750
Wire Wire Line
	4600 2500 5000 2500
Wire Wire Line
	5000 2500 5000 7700
Wire Wire Line
	5000 7700 6300 7700
Wire Wire Line
	7300 1900 9900 1900
Wire Wire Line
	7300 3850 8450 3850
Wire Wire Line
	8450 3850 8450 2200
Wire Wire Line
	8450 2200 9900 2200
Wire Wire Line
	9900 2500 8600 2500
Wire Wire Line
	8600 2500 8600 5750
Wire Wire Line
	8600 5750 7300 5750
Wire Wire Line
	7300 7700 8750 7700
Wire Wire Line
	8750 7700 8750 2800
Wire Wire Line
	8750 2800 9900 2800
Text Label 7500 9000 0    60   ~ 0
MIX_EN
Text Label 7500 8900 0    60   ~ 0
MIX_X2
Wire Wire Line
	7500 8900 7300 8900
Wire Wire Line
	7300 9000 7500 9000
Text Label 7500 5150 0    60   ~ 0
MIX_EN
Text Label 7500 5050 0    60   ~ 0
MIX_X2
Wire Wire Line
	7500 5050 7300 5050
Wire Wire Line
	7300 5150 7500 5150
Text Label 7500 3200 0    60   ~ 0
MIX_EN
Text Label 7500 3100 0    60   ~ 0
MIX_X2
Wire Wire Line
	7500 3100 7300 3100
Wire Wire Line
	7300 3200 7500 3200
Text Label 7500 7050 0    60   ~ 0
MIX_EN
Text Label 7500 6950 0    60   ~ 0
MIX_X2
Wire Wire Line
	7500 6950 7300 6950
Wire Wire Line
	7300 7050 7500 7050
Wire Wire Line
	6300 8650 6150 8650
Text Label 6150 8650 2    60   ~ 0
ADC_CLK_D
Wire Wire Line
	6300 8550 6150 8550
Text Label 6150 8550 2    60   ~ 0
IF_LO_REF_D
Wire Wire Line
	6300 6700 6150 6700
Text Label 6150 6700 2    60   ~ 0
ADC_CLK_C
Wire Wire Line
	6300 6600 6150 6600
Text Label 6150 6600 2    60   ~ 0
IF_LO_REF_C
Wire Wire Line
	6300 4800 6150 4800
Text Label 6150 4800 2    60   ~ 0
ADC_CLK_B
Wire Wire Line
	6300 4700 6150 4700
Text Label 6150 4700 2    60   ~ 0
IF_LO_REF_B
Wire Wire Line
	6300 2850 6150 2850
Text Label 6150 2850 2    60   ~ 0
ADC_CLK_A
Wire Wire Line
	6300 2750 6150 2750
Text Label 6150 2750 2    60   ~ 0
IF_LO_REF_A
$Sheet
S 1600 6200 1450 2050
U 5940CD0A
F0 "clock_distro" 60
F1 "clock_distro.sch" 60
F2 "IF_LO_A" I R 3050 6700 60 
F3 "IF_LO_B" I R 3050 6800 60 
F4 "IF_LO_C" I R 3050 6900 60 
F5 "IF_LO_D" I R 3050 7000 60 
F6 "CLK_A" I R 3050 7250 60 
F7 "CLK_B" I R 3050 7350 60 
F8 "CLK_C" I R 3050 7450 60 
F9 "CLK_D" I R 3050 7550 60 
F10 "IF_LO_IN" I L 1600 6550 60 
F11 "ADC_CLK_IN" I L 1600 7300 60 
F12 "ADC_CLK_EN" I L 1600 7400 60 
F13 "IF_LO_EN" I L 1600 6650 60 
$EndSheet
Wire Wire Line
	2350 2050 2050 2050
Text Label 2050 2050 2    60   ~ 0
SYNTH_FREF
Text Label 9700 3700 2    60   ~ 0
SYNTH_FREF
Wire Wire Line
	9700 3700 9900 3700
Wire Wire Line
	7300 4350 7400 4350
NoConn ~ 7400 4350
Wire Wire Line
	7300 6250 7400 6250
Wire Wire Line
	7300 8200 7400 8200
NoConn ~ 7400 8200
NoConn ~ 7400 6250
Wire Wire Line
	7300 4250 7500 4250
Text Label 7500 4250 0    60   ~ 0
AD_SYNCB
Text Label 7500 2300 0    60   ~ 0
AD_SYNCB
Text Label 7500 6150 0    60   ~ 0
AD_SYNCB
Text Label 7500 8100 0    60   ~ 0
AD_SYNCB
Wire Wire Line
	7500 8100 7300 8100
Wire Wire Line
	7500 6150 7300 6150
Wire Wire Line
	7300 2300 7500 2300
Text Label 7500 2200 0    60   ~ 0
AD_CLKOUT
Wire Wire Line
	7500 2200 7300 2200
NoConn ~ 7400 4150
Wire Wire Line
	7400 4150 7300 4150
NoConn ~ 7400 6050
Wire Wire Line
	7400 6050 7300 6050
Wire Wire Line
	7300 8000 7400 8000
NoConn ~ 7400 8000
Wire Wire Line
	7300 8700 7500 8700
Text Label 7500 8700 0    60   ~ 0
AD_PE_D
Text Label 7500 6750 0    60   ~ 0
AD_PE_C
Text Label 7500 4850 0    60   ~ 0
AD_PE_B
Text Label 7500 2900 0    60   ~ 0
AD_PE_A
Wire Wire Line
	7500 2900 7300 2900
Wire Wire Line
	7500 4850 7300 4850
Text Label 7500 6650 0    60   ~ 0
AD_PD
Text Label 7500 6550 0    60   ~ 0
AD_PC
Text Label 7500 8600 0    60   ~ 0
AD_PD
Text Label 7500 8500 0    60   ~ 0
AD_PC
Text Label 7500 4750 0    60   ~ 0
AD_PD
Text Label 7500 4650 0    60   ~ 0
AD_PC
Text Label 7500 2800 0    60   ~ 0
AD_PD
Text Label 7500 2700 0    60   ~ 0
AD_PC
Wire Wire Line
	7500 2700 7300 2700
Wire Wire Line
	7500 2800 7300 2800
Wire Wire Line
	7500 4650 7300 4650
Wire Wire Line
	7500 4750 7300 4750
Wire Wire Line
	7500 6550 7300 6550
Wire Wire Line
	7500 6650 7300 6650
Wire Wire Line
	7500 6750 7300 6750
Wire Wire Line
	7300 8500 7500 8500
Wire Wire Line
	7500 8600 7300 8600
Text Label 7500 8400 0    60   ~ 0
AD_DOUTB
Wire Wire Line
	7500 8400 7300 8400
Text Label 7500 6450 0    60   ~ 0
AD_DOUTB
Wire Wire Line
	7500 6450 7300 6450
Text Label 7500 4550 0    60   ~ 0
AD_DOUTB
Wire Wire Line
	7500 4550 7300 4550
Text Label 7500 2600 0    60   ~ 0
AD_DOUTB
Wire Wire Line
	7500 2600 7300 2600
Text Label 7500 2400 0    60   ~ 0
AD_FS
Wire Wire Line
	7500 2400 7300 2400
Text Label 7500 8300 0    60   ~ 0
AD_DOUTA_D
Wire Wire Line
	7500 8300 7300 8300
Text Label 7500 6350 0    60   ~ 0
AD_DOUTA_C
Text Label 7500 4450 0    60   ~ 0
AD_DOUTA_B
Text Label 7500 2500 0    60   ~ 0
AD_DOUTA_A
Wire Wire Line
	7500 2500 7300 2500
Wire Wire Line
	7500 4450 7300 4450
Wire Wire Line
	7500 6350 7300 6350
Text Label 11550 3450 0    60   ~ 0
MIX_EN
Text Label 11550 3300 0    60   ~ 0
MIX_X2
Text Label 11550 5050 0    60   ~ 0
AD_SYNCB
Text Label 11550 4450 0    60   ~ 0
AD_PE_C
Text Label 11550 4750 0    60   ~ 0
AD_PD
Text Label 11550 4650 0    60   ~ 0
AD_PC
Text Label 11550 4150 0    60   ~ 0
AD_DOUTB
Text Label 11550 3950 0    60   ~ 0
AD_DOUTA_C
Text Label 11550 3750 0    60   ~ 0
AD_DOUTA_A
Text Label 11550 4250 0    60   ~ 0
AD_PE_A
Text Label 11550 4950 0    60   ~ 0
AD_FS
Text Label 11550 4850 0    60   ~ 0
AD_CLKOUT
Text Label 11550 3850 0    60   ~ 0
AD_DOUTA_B
Text Label 11550 4350 0    60   ~ 0
AD_PE_B
Text Label 11550 4050 0    60   ~ 0
AD_DOUTA_D
Text Label 11550 4550 0    60   ~ 0
AD_PE_D
Wire Wire Line
	9700 3800 9900 3800
Wire Wire Line
	9700 3900 9900 3900
Text Label 9700 3800 2    60   ~ 0
IF_REF
Text Label 9700 3900 2    60   ~ 0
ADC_CLK
Text Label 1450 6550 2    60   ~ 0
IF_REF
Text Label 1450 7300 2    60   ~ 0
ADC_CLK
Text Label 1450 7400 2    60   ~ 0
ADC_CLK_EN
Text Label 1450 6650 2    60   ~ 0
IF_REF_EN
Text Label 11550 3000 0    60   ~ 0
ADC_CLK_EN
Text Label 11550 3150 0    60   ~ 0
IF_REF_EN
Text Label 3300 7000 0    60   ~ 0
IF_LO_REF_D
Text Label 3300 7550 0    60   ~ 0
ADC_CLK_D
Text Label 3300 6700 0    60   ~ 0
IF_LO_REF_A
Text Label 3300 7250 0    60   ~ 0
ADC_CLK_A
Text Label 3300 6800 0    60   ~ 0
IF_LO_REF_B
Text Label 3300 7350 0    60   ~ 0
ADC_CLK_B
Text Label 3300 6900 0    60   ~ 0
IF_LO_REF_C
Text Label 3300 7450 0    60   ~ 0
ADC_CLK_C
Text Notes 3200 7700 0    60   ~ 0
26 MHz, 3.3Vpp square wave
Text Notes 3150 6550 0    60   ~ 0
45 MHz or so sine wave, -10 dBm
Text Notes 1600 8750 0    60   ~ 0
45 MHz or so sine wave, -10 dBm
Wire Wire Line
	3050 6700 3300 6700
Wire Wire Line
	3300 6800 3050 6800
Wire Wire Line
	3050 6900 3300 6900
Wire Wire Line
	3300 7000 3050 7000
Wire Wire Line
	3050 7250 3300 7250
Wire Wire Line
	3300 7350 3050 7350
Wire Wire Line
	3050 7450 3300 7450
Wire Wire Line
	3300 7550 3050 7550
Wire Wire Line
	1450 6550 1600 6550
Wire Wire Line
	1450 6650 1600 6650
Wire Wire Line
	1450 7300 1600 7300
Wire Wire Line
	1450 7400 1600 7400
Text Label 11550 2200 0    60   ~ 0
LMX_CE
Text Label 11550 2300 0    60   ~ 0
LMX_CSB
Text Label 11550 2400 0    60   ~ 0
LMX_SDI
Text Label 11550 2500 0    60   ~ 0
LMX_SCK
Text Label 11550 2600 0    60   ~ 0
LMX_MUXout
Wire Wire Line
	11350 2200 11550 2200
Wire Wire Line
	11550 2300 11350 2300
Wire Wire Line
	11350 2400 11550 2400
Wire Wire Line
	11550 2500 11350 2500
Wire Wire Line
	11350 2600 11550 2600
Wire Wire Line
	11550 3000 11350 3000
Wire Wire Line
	11350 3150 11550 3150
Wire Wire Line
	11550 3300 11350 3300
Wire Wire Line
	11350 3450 11550 3450
Wire Wire Line
	11350 3750 11550 3750
Wire Wire Line
	11550 3850 11350 3850
Wire Wire Line
	11350 3950 11550 3950
Wire Wire Line
	11550 4050 11350 4050
Wire Wire Line
	11350 4150 11550 4150
Wire Wire Line
	11550 4250 11350 4250
Wire Wire Line
	11350 4350 11550 4350
Wire Wire Line
	11550 4450 11350 4450
Wire Wire Line
	11350 4550 11550 4550
Wire Wire Line
	11550 4650 11350 4650
Wire Wire Line
	11350 4750 11550 4750
Wire Wire Line
	11550 4850 11350 4850
Wire Wire Line
	11350 4950 11550 4950
Wire Wire Line
	11550 5050 11350 5050
Text Label 2050 3200 2    60   ~ 0
LMX_CE
Text Label 2050 3100 2    60   ~ 0
LMX_CSB
Text Label 2050 2900 2    60   ~ 0
LMX_SDI
Text Label 2050 3000 2    60   ~ 0
LMX_SCK
Text Label 2050 2750 2    60   ~ 0
LMX_MUXout
Wire Wire Line
	2050 3200 2350 3200
Wire Wire Line
	2350 3100 2050 3100
Wire Wire Line
	2050 3000 2350 3000
Wire Wire Line
	2350 2900 2050 2900
Wire Wire Line
	2050 2750 2350 2750
$EndSCHEMATC