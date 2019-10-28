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
Goals:\n10 MHz input or internal OCXO\nthree 100 MHz outputs, one 10 MHz output\nenclosure & 3D model\nphase noise that doesn't limit the TI LMX2595\n 
$Sheet
S 7200 1750 1250 2900
U 5DBF0563
F0 "output_buffer" 50
F1 "output_buffer.sch" 50
F2 "REF_100MHZ_IN" I L 7200 3000 50 
$EndSheet
$Sheet
S 5200 1750 1250 2900
U 5DC1A65E
F0 "synth_100MHz" 50
F1 "synth_100MHz.sch" 50
$EndSheet
$Sheet
S 3100 1750 1250 2900
U 5DC3C92E
F0 "ref_sel" 50
F1 "ref_sel.sch" 50
$EndSheet
$Sheet
S 2750 5550 1950 1600
U 5DC45DA8
F0 "power_conn" 50
F1 "power_conn.sch" 50
$EndSheet
$EndSCHEMATC
