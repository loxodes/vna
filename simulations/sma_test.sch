<Qucs Schematic 0.0.18>
<Properties>
  <View=46,-144,955,980,0.826447,0,0>
  <Grid=10,10,1>
  <DataSet=sma_test.dat>
  <DataDisplay=sma_test.dpl>
  <OpenDisplay=1>
  <Script=sma_test.m>
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
  <Pac P1 1 100 430 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 1 100 460 0 0 0 0>
  <.SP SP1 1 110 530 0 76 0 0 "log" 1 "100MHz" 1 "10GHz" 1 "200" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <Eqn Eqn1 1 300 540 -28 15 0 0 "dBS21=dB(S[2,1])" 1 "dBS11=dB(S[1,1])" 1 "yes" 0>
  <Pac P2 1 840 430 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 1 840 460 0 0 0 0>
  <MLIN MS3 1 510 350 -26 15 0 0 "Subst1" 1 ".35 mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <SUBST Subst1 1 130 100 -30 24 0 0 "3.66" 1 ".17 mm" 1 "70 um" 1 ".015" 1 "0.022e-6" 1 "0.15e-6" 1>
  <MLIN MS1 1 280 350 -26 15 0 0 "Subst1" 1 "2.3 mm" 1 "5 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MSTEP MS5 1 400 350 -26 17 0 0 "Subst1" 1 "2.3 mm" 1 ".35 mm" 1 "Hammerstad" 0 "Kirschning" 0>
  <MSTEP MS6 1 620 350 -26 17 0 0 "Subst1" 1 ".35 mm" 1 "2.3 mm" 1 "Hammerstad" 0 "Kirschning" 0>
  <MLIN MS4 1 720 350 -26 15 0 0 "Subst1" 1 "2.3 mm" 1 "5 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
</Components>
<Wires>
  <840 350 840 400 "" 0 0 0 "">
  <750 350 840 350 "" 0 0 0 "">
  <100 350 100 400 "" 0 0 0 "">
  <100 350 250 350 "" 0 0 0 "">
  <650 350 690 350 "" 0 0 0 "">
  <540 350 590 350 "" 0 0 0 "">
  <430 350 480 350 "" 0 0 0 "">
  <310 350 370 350 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
