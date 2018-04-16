EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
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
LIBS:74lvc1g32
LIBS:lm27762
LIBS:74lvc1g00
LIBS:adrf5020
LIBS:tps2051
LIBS:resistive_bridge
LIBS:lm2776
LIBS:max810
LIBS:vdd_clk
LIBS:vdd_lo
LIBS:vdd_rf
LIBS:lan8710a
LIBS:ad9577
LIBS:okr_t3-w12-c
LIBS:adp7158
LIBS:maam-011100
LIBS:ltc2054cs5
LIBS:ltc2630
LIBS:trf37b73
LIBS:nc7wzu04
LIBS:adrf5040
LIBS:lmx2594
LIBS:tps255xx
LIBS:tps2065d
LIBS:masw-008322-tr1000
LIBS:max510
LIBS:pe42541
LIBS:txco
LIBS:tps793
LIBS:tpd4s012
LIBS:tcm-63ax+
LIBS:sn74lvc1g07
LIBS:scbd-16-63
LIBS:rf_crossbar
LIBS:pwr_splitter
LIBS:pe43705
LIBS:pe42540
LIBS:pe42521
LIBS:pcm2900
LIBS:nc7sv74kbx
LIBS:nb3n551
LIBS:mounting_hole
LIBS:mounting_box
LIBS:mga-82563
LIBS:max2605
LIBS:maam-011101
LIBS:ltc5596
LIBS:ltc5549
LIBS:ltc2323
LIBS:ltc1983
LIBS:ltc1566-1
LIBS:lt1819
LIBS:lt1567
LIBS:lmx2592
LIBS:lmk61e2
LIBS:hmc629
LIBS:hmc525
LIBS:hmc475
LIBS:hmc424
LIBS:hmc321
LIBS:hmc311sc70
LIBS:conn_sma_2gnd
LIBS:conn_sma
LIBS:conn_microsd
LIBS:cmm0511-qt-0g0t
LIBS:cat102
LIBS:boosterpack_ti
LIBS:ammp-6120
LIBS:adm7150
LIBS:adl5902
LIBS:adl5380
LIBS:adf4355-3
LIBS:ad9864
LIBS:75451
LIBS:74xx1g14
LIBS:74hc04_full
LIBS:74hc04
LIBS:sky65013-70lf
LIBS:pat0510s-c-xdb-t10
LIBS:tp_rf
LIBS:hmc65xlp2e
LIBS:vna_r1_demod-cache
EELAYER 25 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 6
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
S 8950 3650 1150 2650
U 5AC62E41
F0 "demod_a" 60
F1 "demod.sch" 60
F2 "RF_IN" I L 8950 4000 60 
F3 "LO_IN" I L 8950 6100 60 
F4 "MIX_EN" I R 10100 5500 60 
F5 "MIX_X2" I R 10100 5600 60 
F6 "LO_AMP" I R 10100 5400 60 
$EndSheet
$Sheet
S 13450 3700 1150 2650
U 5AC63047
F0 "demod_b" 60
F1 "demod.sch" 60
F2 "RF_IN" I L 13450 4000 60 
F3 "LO_IN" I L 13450 6100 60 
F4 "MIX_EN" I R 14600 5500 60 
F5 "MIX_X2" I R 14600 5600 60 
F6 "LO_AMP" I R 14600 5400 60 
$EndSheet
$Sheet
S 4800 5400 1900 1750
U 5AC731FA
F0 "power_conn" 60
F1 "power_conn.sch" 60
F2 "LO_AMP_A" O R 6700 5950 60 
F3 "LO_AMP_B" O R 6700 6650 60 
F4 "MIX_EN_A" O R 6700 6050 60 
F5 "X2_EN_A" O R 6700 6150 60 
F6 "MIX_EN_B" O R 6700 6750 60 
F7 "X2_EN_B" O R 6700 6850 60 
$EndSheet
$Sheet
S 8950 1250 3850 1300
U 5AC73A4A
F0 "couplers" 60
F1 "couplers.sch" 60
F2 "CPL_FWD" O L 8950 2150 60 
F3 "CPL_REV" O R 12800 2150 60 
$EndSheet
$Sheet
S 8950 7450 1950 1650
U 5AC76B92
F0 "lo_split" 60
F1 "lo_split.sch" 60
F2 "LO_A" O L 8950 7850 60 
F3 "LO_B" O R 10900 7850 60 
$EndSheet
Wire Wire Line
	8950 6100 8700 6100
Wire Wire Line
	8700 6100 8700 7850
Wire Wire Line
	8700 7850 8950 7850
Wire Wire Line
	10900 7850 12400 7850
Wire Wire Line
	12400 7850 12400 6100
Wire Wire Line
	12400 6100 13450 6100
Wire Wire Line
	12800 2150 13100 2150
Wire Wire Line
	13100 2150 13100 4000
Wire Wire Line
	13100 4000 13450 4000
Wire Wire Line
	8950 2150 8700 2150
Wire Wire Line
	8700 2150 8700 4000
Wire Wire Line
	8700 4000 8950 4000
Wire Wire Line
	6700 5950 6850 5950
Wire Wire Line
	6700 6050 6850 6050
Wire Wire Line
	6700 6150 6850 6150
Wire Wire Line
	6700 6650 6850 6650
Wire Wire Line
	6700 6750 6850 6750
Wire Wire Line
	6700 6850 6850 6850
Text Label 6850 5950 0    60   ~ 0
LO_AMP_A
Text Label 6850 6050 0    60   ~ 0
MIX_EN_A
Text Label 6850 6150 0    60   ~ 0
X2_EN_A
Text Label 6850 6650 0    60   ~ 0
LO_AMP_B
Text Label 6850 6750 0    60   ~ 0
MIX_EN_B
Text Label 6850 6850 0    60   ~ 0
X2_EN_B
Text Label 14700 5400 0    60   ~ 0
LO_AMP_B
Text Label 14700 5500 0    60   ~ 0
MIX_EN_B
Text Label 14700 5600 0    60   ~ 0
X2_EN_B
Text Label 10200 5400 0    60   ~ 0
LO_AMP_A
Text Label 10200 5500 0    60   ~ 0
MIX_EN_A
Text Label 10200 5600 0    60   ~ 0
X2_EN_A
Wire Wire Line
	10100 5400 10200 5400
Wire Wire Line
	10100 5500 10200 5500
Wire Wire Line
	10100 5600 10200 5600
Wire Wire Line
	14600 5400 14700 5400
Wire Wire Line
	14600 5500 14700 5500
Wire Wire Line
	14600 5600 14700 5600
$EndSCHEMATC
