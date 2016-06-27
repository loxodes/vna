<Qucs Schematic 0.0.18>
<Properties>
  <View=0,-120,800,800,1,0,0>
  <Grid=10,10,1>
  <DataSet=powersplit.dat>
  <DataDisplay=powersplit.dpl>
  <OpenDisplay=1>
  <Script=powersplit.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
</Symbol>
<Components>
  <Pac P1 1 130 390 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 1 130 420 0 0 0 0>
  <GND * 1 490 420 0 0 0 0>
  <R R2 1 410 310 -26 15 0 0 "5.6" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0>
  <.SP SP1 1 180 60 0 75 0 0 "log" 1 "100MHz" 1 "10GHz" 1 "200" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <R R1 1 300 310 -26 15 1 2 "5.6" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0>
  <R R6 1 290 440 -26 15 1 2 "64.9" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0>
  <R R7 1 290 540 -26 15 1 2 "60.4" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0>
  <GND * 1 260 440 0 0 0 0>
  <GND * 1 260 540 0 0 0 0>
  <GND * 1 360 620 0 0 0 0>
  <R R3 1 360 400 15 -26 0 1 "187" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0>
  <R R4 1 360 490 15 -26 0 1 "5.6" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0>
  <Pac P2 1 490 390 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Pac P3 1 360 590 18 -26 0 1 "3" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Eqn Eqn1 1 370 70 -28 15 0 0 "dBS21=dB(S[2,1])" 1 "dBS31=dB(S[3,1])" 1 "dBS11=dB(S[1,1])" 1 "yes" 0>
</Components>
<Wires>
  <130 310 130 360 "" 0 0 0 "">
  <130 310 270 310 "" 0 0 0 "">
  <330 310 360 310 "" 0 0 0 "">
  <360 520 360 540 "" 0 0 0 "">
  <360 430 360 440 "" 0 0 0 "">
  <360 310 380 310 "" 0 0 0 "">
  <360 310 360 370 "" 0 0 0 "">
  <360 440 360 460 "" 0 0 0 "">
  <320 440 360 440 "" 0 0 0 "">
  <360 540 360 560 "" 0 0 0 "">
  <320 540 360 540 "" 0 0 0 "">
  <440 310 490 310 "" 0 0 0 "">
  <490 310 490 360 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
  <Text 470 500 12 #000000 0 "Bessel low-pass filter\n1GHz cutoff, PI-type,\nimpedance matching 50 Ohm">
</Paintings>
