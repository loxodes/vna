
// configures AD9864 IF digitizer
// sampling with beaglebone pru (see /software/pru_test)
// max2605 VCO tune to ~45.15 MHz
// 26 MHz xco input
// 45 MHz IF
// 

#include <SPI.h>


const int ADC_SPI_CLK = 7; // P1_5,  pc
const int ADC_SPI_DAT = 15; // P1_6, pd
const int ADC_SPI_EN = 12; //P5_2. pe
const int ADC_SPI_RB = 14; //P1_7, doutb
// douta, syncb, fs, clkout connected to beaglebone

#define AD9864_READ_MASK ((1 << 15))

void ad9864_write_reg(uint8_t addr, uint8_t value)
{
  uint16_t payload = addr << 9 | value;
  digitalWrite(ADC_SPI_EN, LOW);
  SPI.transfer(payload);
  digitalWrite(ADC_SPI_EN, HIGH);
}

uint8_t ad9864_read_reg(uint8_t addr)
{
  uint16_t payload = addr << 9 | AD9864_READ_MASK;
  digitalWrite(ADC_SPI_EN, LOW);
  uint16_t response = SPI.transfer(payload);
  digitalWrite(ADC_SPI_EN, HIGH);
  return response & 0xFF;
}

void ad9864_init()
{
  uint8_t r;
  
  pinMode(ADC_SPI_CLK, OUTPUT);
  pinMode(ADC_SPI_DAT, OUTPUT);
  pinMode(ADC_SPI_EN, OUTPUT);
  pinMode(ADC_SPI_RB, INPUT_PULLUP);
  digitalWrite(ADC_SPI_EN, HIGH);
  
  // init
  ad9864_write_reg(0x3F, 0x99); // software reset
  ad9864_write_reg(0x19, 0x87); // 4-wire SPI, 16 bit I/Q
  ad9864_write_reg(0x00, 0x55); // take ref, gc, cko out of standby. leave ck off

// configure clock synth (bypass vco, use 26 MHz crystal osc)
//  ad9864_write_reg(0x01, 0x0C);
//  ad9864_write_reg(0x10, 0x00); // ???
//  ad9864_write_reg(0x11, 0x38); // ???
//  ad9864_write_reg(0x12, 0x00); // ???
//  ad9864_write_reg(0x13, 0x3C); // ???
//  ad9864_write_reg(0x14, 0x03); // ???
  delayMicroseconds(1000); // TODO: how long to wait for CLK SYN output to settle?
  
  // lc and rc resonator calibration
  ad9864_write_reg(0x3E, 0x47);
  ad9864_write_reg(0x38, 0x01);
  ad9864_write_reg(0x39, 0x0F);

  for(uint8_t i = 0; i < 5; i++) {
    ad9864_write_reg(0x1C, 0x03);
    ad9864_write_reg(0x00, 0x44);
    delayMicroseconds(6000);
    r = ad9864_read_reg(0x1C);
    if(r == 0) {
     break;  
    }
    ad9864_write_reg(0x1C, 0x00);
    Serial.println("LC/RC calibration failed, retrying..");
  }

  ad9864_write_reg(0x38, 0x00);
  ad9864_write_reg(0x3E, 0x00);

  // lo synth configuration, set LO to 48.25 MHz
  ad9864_write_reg(0x00, 0x10); // enable everything but clk synth
  ad9864_write_reg(0x08, 0x00); // 
  ad9864_write_reg(0x09, 0x68); // LOR = 104 (so, fif = 250 kHz * (8 LOB + LOA)
  ad9864_write_reg(0x0A, 0xA0); // LOA = 1 
  ad9864_write_reg(0x0B, 0x18); // LOB = 24
  ad9864_write_reg(0x0C, 0x03); // normal LO charge pump current control, Ipump = .625 mA

  // disable agc
  ad9864_write_reg(0x03, 0x00); //
  ad9864_write_reg(0x04, 0x00); // 
  ad9864_write_reg(0x05, 0x00); // 
  ad9864_write_reg(0x06, 0x00); //
   
  // configure decimation
  ad9864_write_reg(0x07, 0x0E); // set decimation rate to 900, 60 * (M + 1) if K = 0, M = 14
  
  // configure SSI
  ad9864_write_reg(0x1A, 0x08); // (clkout freq = fclk / 8)
  ad9864_write_reg(0x18, 0x00); // take fs and clkout out of tristate
}

void setup() {
  Serial.begin(9600);
  SPI.begin();

  
  ad9864_init();
}

void loop() {
  ;
  
}
