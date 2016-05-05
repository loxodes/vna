<Qucs Schematic 0.0.18>
<Properties>
  <View=-70,-244,1765,1334,0.930927,242,563>
  <Grid=10,10,1>
  <DataSet=filter_test.dat>
  <DataDisplay=filter_test.dpl>
  <OpenDisplay=1>
  <Script=filter_test.m>
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
  <Pac P1 1 80 420 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 1 80 460 0 0 0 0>
  <MSTEP MS3 1 360 340 -26 17 0 0 "Subst1" 1 "wz0" 1 "wzmin" 1 "Hammerstad" 0 "Kirschning" 0>
  <MLIN MS2 1 220 340 -26 15 0 0 "Subst1" 1 "wz0" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <Eqn Eqn1 1 290 810 -28 15 0 0 "dBS21=dB(S[2,1])" 1 "dBS11=dB(S[1,1])" 1 "yes" 0>
  <Pac P2 1 1650 420 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 1 1650 460 0 0 0 0>
  <MLIN MS1 1 1460 340 -26 15 0 0 "Subst1" 1 "wz0" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MSTEP MS5 1 590 340 -26 17 0 0 "Subst1" 1 "wzmin" 1 "wzmax" 1 "Hammerstad" 0 "Kirschning" 0>
  <MSTEP MS7 1 850 340 -26 17 0 0 "Subst1" 1 "wzmax" 1 "wzmin" 1 "Hammerstad" 0 "Kirschning" 0>
  <MSTEP MS9 1 1110 340 -26 17 0 0 "Subst1" 1 "wzmin" 1 "wzmax" 1 "Hammerstad" 0 "Kirschning" 0>
  <MSTEP MS11 1 590 530 -26 17 0 0 "Subst1" 1 "wzmin" 1 "wzmax" 1 "Hammerstad" 0 "Kirschning" 0>
  <MSTEP MS12 1 850 530 -26 17 0 0 "Subst1" 1 "wzmax" 1 "wzmin" 1 "Hammerstad" 0 "Kirschning" 0>
  <MSTEP MS15 1 1110 530 -26 17 0 0 "Subst1" 1 "wzmin" 1 "wz0" 1 "Hammerstad" 0 "Kirschning" 0>
  <.SP SP1 1 110 790 0 79 0 0 "log" 1 "100MHz" 1 "10GHz" 1 "2001" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <Eqn Eqn2 1 560 830 -23 15 0 0 "wz0=.35 m" 1 "wzmax=1.84 m" 1 "wzmin=.138 m" 1 "yes" 0>
  <Eqn Eqn3 1 730 830 -23 15 0 0 "l1=.35 m" 1 "l2=1.84 m" 1 "l3=.138 m" 1 "l4=.138 m" 1 "l5=.138 m" 1 "l6=.138 m" 1 "yes" 0>
  <MLIN MS4 1 470 340 -26 15 0 0 "Subst1" 1 "wzmin" 1 "l1" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MLIN MS6 1 710 340 -26 15 0 0 "Subst1" 1 "wzmax" 1 "l2" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MLIN MS8 1 980 340 -26 15 0 0 "Subst1" 1 "wzmin" 1 "l3" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MLIN MS13 1 470 530 -26 15 0 0 "Subst1" 1 "wzmin" 1 "l4" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MLIN MS10 1 700 530 -26 15 0 0 "Subst1" 1 "wzmax" 1 "l5" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <MLIN MS14 1 980 530 -26 15 0 0 "Subst1" 1 "wzmin" 1 "l6" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0>
  <SUBST Subst1 1 150 60 -30 24 0 0 "3.66" 1 ".17 mm" 1 ".018 mm" 1 ".0125" 1 "15.8e-9" 1 "0.15e-6" 1>
</Components>
<Wires>
  <80 450 80 460 "" 0 0 0 "">
  <250 340 330 340 "" 0 0 0 "">
  <80 340 80 390 "" 0 0 0 "">
  <80 340 190 340 "" 0 0 0 "">
  <1650 340 1650 390 "" 0 0 0 "">
  <1490 340 1650 340 "" 0 0 0 "">
  <1650 450 1650 460 "" 0 0 0 "">
  <500 340 560 340 "" 0 0 0 "">
  <390 340 440 340 "" 0 0 0 "">
  <880 340 950 340 "" 0 0 0 "">
  <1010 340 1080 340 "" 0 0 0 "">
  <1140 340 1210 340 "" 0 0 0 "">
  <1210 340 1210 490 "" 0 0 0 "">
  <280 490 1210 490 "" 0 0 0 "">
  <1140 530 1290 530 "" 0 0 0 "">
  <1290 340 1290 530 "" 0 0 0 "">
  <1290 340 1430 340 "" 0 0 0 "">
  <500 530 560 530 "" 0 0 0 "">
  <280 490 280 530 "" 0 0 0 "">
  <280 530 440 530 "" 0 0 0 "">
  <730 530 820 530 "" 0 0 0 "">
  <620 530 670 530 "" 0 0 0 "">
  <740 340 820 340 "" 0 0 0 "">
  <620 340 680 340 "" 0 0 0 "">
  <1010 530 1080 530 "" 0 0 0 "">
  <880 530 950 530 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
