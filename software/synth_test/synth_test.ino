#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include "lmx2592.h"

#define CHANNELA 0
#define CHANNELB 1
#define ON 1
#define OFF 0
#define ADC_BITS 16
#define CNV_DELAY 1
#define SCK_DELAY 1

// command structure
// [region][index][command]
#define SWITCH_CMD 'w'
#define FILT_CMD 'f'
#define POW_CMD 'p'
#define SYNTH_CMD 's'
#define OUTPUT_CMD 's'
#define DET_CMD 'd'
#define DBM_CMD 'b'
#define ATT_CMD 'a'
#define IQ_CMD 'q'
#define CMD_ERR 'E'

#define SWITCH_LOWFREQ LOW
#define SWITCH_HIGHFREQ HIGH
#define SW2_S21 LOW
#define SW2_S11 HIGH
#define ADC_AVG 32

// pins
const uint8_t LMX_LE = 14;
const uint8_t LMX_CE = 18;
const uint8_t LMX_AUX = 12;
const uint8_t LMX_POWEN = 32;

const uint8_t REFCLK_EN = 24;

const uint8_t SW_0 = 6;
const uint8_t SW_1 = 6;
const uint8_t SW_2 = PG_1;
const uint8_t SW_3 = 6;
const uint8_t SW_4 = 6;
const uint8_t SW_5 = 6;

const uint8_t I_0 = A18;
const uint8_t Q_0 = A19;
const uint8_t I_1 = A16;
const uint8_t Q_1 = A17;

const uint8_t FILT0_A = 38;
const uint8_t FILT0_B = 36;
const uint8_t FILT0_C = 34;
const uint8_t FILT0_AN = 37;
const uint8_t FILT0_BN = 39;
const uint8_t FILT0_CN = 40;

const uint8_t ATT_1 = 35;
const uint8_t ATT_2 = 33;
const uint8_t ATT_3 = 31;
const uint8_t ATT_4 = 29;
const uint8_t ATT_5 = 27;
const uint8_t ATT_6 = 25;

const uint8_t DET_0 = A3; // pin 23


int ADC_CNV_INPUT = PK_3; // LTC2323 pin 9, high defines sample phase, low starts conversion phase
int ADC_CNV_EN = PK_2; // LTC2323 conversion enable, high is enabled?
int ADC_SCK = PB_4; // LTC2323 pin 21, input spi clock
int ADC_CLKOUT = PK_0; // LTC2323 pin 17, output spi clock
int ADC_SD2 = PB_5; // LTC2323 pin 19, adc channel 1
int ADC_SD1 = PK_1; // LTC2323 pin 15, adc channel 1

// synth settings
const uint16_t MIN_N = 16;
const uint32_t FRAC_DENOM = 200000;
const float PFD = 100e6;
const float F_VCO_MIN = 3.55e9;
const float F_VCO_MAX = 7.1e9;
const uint32_t PRE_N = 2;

// ethernet stuff
byte mac[] = {0x00, 0x1A, 0xB6, 0x03, 0x0A, 0xB5};
IPAddress ip(192, 168, 1, 177);
unsigned int port = 8888;
EthernetUDP Udp;

// buffers for receiving and sending data
uint8_t packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet
uint8_t replyBuffer[UDP_TX_PACKET_MAX_SIZE]; // buffer to hold outgoing packet


float output_freq;

void ltc2323_init()
{
  pinMode(ADC_CNV_INPUT, OUTPUT);
  pinMode(ADC_CNV_EN, OUTPUT);
  pinMode(ADC_SCK, OUTPUT);
  pinMode(ADC_CLKOUT, INPUT_PULLUP);
  pinMode(ADC_SD2, INPUT_PULLUP);
  pinMode(ADC_SD1, INPUT_PULLUP);

  digitalWrite(ADC_CNV_EN, HIGH); // INVERTED
  digitalWrite(ADC_CNV_INPUT, LOW); // INVERTED
}

uint32_t ltc2323_conv()
{
  uint32_t adc1 = 0;
  uint32_t adc2 = 0;
  // why do I need to pulse CNV_EN?...
  digitalWrite(ADC_CNV_EN, LOW);
  delayMicroseconds(CNV_DELAY);
  digitalWrite(ADC_CNV_EN, HIGH); // INVERTED

  digitalWrite(ADC_CNV_INPUT, HIGH);
  delayMicroseconds(CNV_DELAY);
  digitalWrite(ADC_CNV_INPUT, LOW);
  delayMicroseconds(CNV_DELAY);

  for (uint32_t i = 0; i < ADC_BITS; i++) {
    digitalWrite(ADC_SCK, HIGH);
    delayMicroseconds(SCK_DELAY);
    adc1 = adc1 << 1;
    adc2 = adc2 << 1;
    adc1 |= digitalRead(ADC_SD1) ^ 1;
    adc2 |= digitalRead(ADC_SD2) ^ 1;
    digitalWrite(ADC_SCK, LOW);
    delayMicroseconds(SCK_DELAY);
  }

  return adc1 | (adc2 << 16);

}


uint16_t spi_read_reg(uint8_t reg)
{

}
void spi_set_reg(uint8_t reg, uint32_t d)
{
  // so, a bunch of registers have default values that need to be maintained... wtf
  uint32_t LMX_REG_DEFAULTS[65] = { \
                                    0x0210, 0x0808, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x20b2, // 0-7
                                    0x1000, 0x0082, 0x1058, 0x0008, 0x7000, 0x0000, 0x0000, 0x0000, // 7-15
                                    0x0000, 0x0000, 0x0000, 0x0965, 0x0000, 0x0000, 0x0000, 0x8842, // 16-23
                                    0x0509, 0x0000, 0x0000, 0x0000, 0x2924, 0x0084, 0x0034, 0x0001, // 24-31
                                    0x4210, 0x4210, 0xc3d0, 0x0019, 0x0000, 0x4000, 0x0000, 0x8004, // 32-39
                                    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x00c0, // 40-47 TODO: 46 only works if blank..
                                    0x03fc, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, // 48-55
                                    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, // 56-63
                                    0x00af
                                  }; // 64

  LMX_REG_DEFAULTS[46] |= REG46_MASH_ORDER_2 | REG46_MASH_EN;

  d = d | LMX_REG_DEFAULTS[reg];

  digitalWrite(LMX_LE, LOW);
  SPI.transfer(reg);
  SPI.transfer((d >> 8) & 0xFF);
  SPI.transfer((d >> 0) & 0xFF);
  digitalWrite(LMX_LE, HIGH);
  delay(1);
}

void gpio_init()
{
  pinMode(SW_1, OUTPUT);
  digitalWrite(SW_1, SWITCH_LOWFREQ);
  pinMode(SW_2, OUTPUT);
  digitalWrite(SW_2, SW2_S11);

  pinMode(FILT0_A, OUTPUT);
  pinMode(FILT0_B, OUTPUT);
  pinMode(FILT0_C, OUTPUT);
  digitalWrite(FILT0_A, HIGH);
  digitalWrite(FILT0_B, HIGH);
  digitalWrite(FILT0_C, HIGH);

  pinMode(FILT0_AN, OUTPUT);
  pinMode(FILT0_BN, OUTPUT);
  pinMode(FILT0_CN, OUTPUT);
  digitalWrite(FILT0_AN, LOW);
  digitalWrite(FILT0_BN, LOW);
  digitalWrite(FILT0_CN, LOW);

  pinMode(ATT_1, OUTPUT);
  pinMode(ATT_2, OUTPUT);
  pinMode(ATT_3, OUTPUT);
  pinMode(ATT_4, OUTPUT);
  pinMode(ATT_5, OUTPUT);
  pinMode(ATT_6, OUTPUT);
  digitalWrite(ATT_1, LOW);
  digitalWrite(ATT_2, LOW);
  digitalWrite(ATT_3, LOW);
  digitalWrite(ATT_4, LOW);
  digitalWrite(ATT_5, LOW);
  digitalWrite(ATT_6, LOW);
}

void clk_init()
{
  // TODO: init i2c
  pinMode(REFCLK_EN, OUTPUT);
  digitalWrite(REFCLK_EN, HIGH);
}

void lmx2592_init()
{
  pinMode(LMX_LE, OUTPUT);
  pinMode(LMX_CE, OUTPUT);
  pinMode(LMX_POWEN, OUTPUT);
  pinMode(LMX_AUX, INPUT);

  digitalWrite(LMX_CE, HIGH);
  digitalWrite(LMX_LE, HIGH);
  digitalWrite(LMX_POWEN, HIGH);

  delay(10);
  spi_set_reg(0, REG0_RESET);
  spi_set_reg(46, REG46_MASH_ORDER_2 | REG46_MASH_EN | REG46_OUTB_PD | (0 << REG46_OUTA_POW)); //  REG46_OUTA_PD
  spi_set_reg(31, REG31_VCO_DISTB_PD);
  spi_set_reg(12, 0x7001);
  spi_set_reg(11, 0x0018);
  spi_set_reg(10, 0x10d8);
  lmx2592_set_denom(FRAC_DENOM);
  spi_set_reg(0, REG0_LD_EN | REG0_FCAL_EN | REG0_MUXOUT_SEL);
  delay(10);
}

void lmx2592_set_denom(uint32_t denom)
{
  uint32_t denom_lsw = denom & 0xFFFF;
  uint32_t denom_msw = (denom >> 16) & 0xFFFF;

  spi_set_reg(40, denom_msw);
  spi_set_reg(41, denom_lsw);

}
void lmx2592_chan_power(uint8_t chan, uint8_t power)
{
  if (chan == CHANNELB) {
    spi_set_reg(47, (0x3F & power) << REG47_OUTB_POW);
    spi_set_reg(46, REG46_OUTA_PD);
  }
  else if (chan == CHANNELA) {
    spi_set_reg(46, REG46_OUTB_PD | (0x3F & power) << REG46_OUTA_POW);
  }
  delay(10);
}

float adl5902_get_int(float f)
{
  const float filt_freqs[9] = {500e6, 1e9, 2e9, 3e9, 4e9, 5e9, 6e9, 7e9, 8e9};
  const float cal_table[9] = {-30.4, -33.93, -35.73, -37.33, -40.46, -45.59, -48.31, -45.87, -45.11};

  // TODO: break this out into a function and don't copy/paste..
  if(f < filt_freqs[0]) {
    return cal_table[0];
  }
  if(f > filt_freqs[8]) {
    return cal_table[8];
  }
  
  for (uint32_t i = 1; i < 9; i++) {
    if (f < filt_freqs[i]) {
      return cal_table[i-1] + ((f - filt_freqs[i-1]) / (filt_freqs[i] - filt_freqs[i-1])) * (cal_table[i] - cal_table[i-1]);
    }
  }
  return -100;
}

float adl5902_get_slope(float f)
{
  const float filt_freqs[9] = {500e6, 1e9, 2e9, 3e9, 4e9, 5e9, 6e9, 7e9, 8e9};
  const float cal_table[9] = {43.6e-3, 48.6e-3, 48.6e-3, 48.1e-3, 45.1e-3, 39.3e-3, 33.1e-3, 34.7e-3, 31.6e-3};
  

  // TODO: break this out into a function and don't copy/paste..
  if(f < filt_freqs[0]) {
    return cal_table[0];
  }
  if(f > filt_freqs[8]) {
    return cal_table[8];
  }
  
  for (uint32_t i = 1; i < 9; i++) {
    if (f < filt_freqs[i]) {
      return cal_table[i-1] + ((f - filt_freqs[i-1]) / (filt_freqs[i] - filt_freqs[i-1])) * (cal_table[i] - cal_table[i-1]);
    }
  }
  return -100;
}

void adl5902_init()
{
  analogReadResolution(12);
  uint32_t i = 0;
  for (i = 0; i < 200; i++) {
    analogRead(DET_0);
  }
}
float adl5902_powerdet(float f)
{
  float ADC_REF = 3.3;
  float det_voltage, det_power;
  uint32_t ADC_STEPS = 4096;
  uint32_t DET_AVG = 16;
  
  float det_adc = 0;
  for(uint8_t i = 0; i < DET_AVG; i++) {
    det_adc += analogRead(DET_0);
  }
  det_adc /= DET_AVG;
  
  Serial.print("RAW ADC: ");
  Serial.print(det_adc);
  det_voltage = (ADC_REF / (float) ADC_STEPS) * det_adc;
  det_power = adl5902_get_int(f) + (det_voltage / adl5902_get_slope(f));
  return det_power;
}

uint32_t calc_n(float f, float n_step, uint32_t div)
{
  return f / (n_step / div);
}

uint32_t calc_frac(float f, uint32_t n, float n_step, float frac_step, uint32_t div)
{
  return (f - n * (n_step / div)) / (frac_step / div);
}

// set the filter bank automatically from output frequency
// if the output frequency is above the max vco frequency, brek the path
// to improve isolation from the vco doubler path
void set_filterbank(float f)
{

  const uint8_t FILTER_BANK_SIZE = 8;
  const float filter_bank_cutoffs[FILTER_BANK_SIZE] = {6.0e9, 4.4e9, 3.4e9, 2.25e9, 1.45e9, 1.0e9, 0.63e9, 0.0};
  uint8_t filt_i = 0;

  if (f > F_VCO_MAX) {
    digitalWrite(FILT0_A, HIGH);
    digitalWrite(FILT0_B, HIGH);
    digitalWrite(FILT0_C, HIGH);
    digitalWrite(FILT0_AN, HIGH);
    digitalWrite(FILT0_BN, HIGH);
    digitalWrite(FILT0_CN, HIGH);
  } else {
    if (f < filter_bank_cutoffs[0]) {
      for (filt_i = 1; filt_i < FILTER_BANK_SIZE; filt_i++) {
        if (f > filter_bank_cutoffs[filt_i]) {
          filt_i--;
          break;
        }
      }
    } else {
      filt_i = 7; // set bypass filter if frequency is above highest lowpass
    }

    digitalWrite(FILT0_A, ((filt_i & 0x01) > 0));
    digitalWrite(FILT0_B, ((filt_i & 0x02) > 0));
    digitalWrite(FILT0_C, ((filt_i & 0x04) > 0));
    digitalWrite(FILT0_AN, ((filt_i & 0x01) == 0));
    digitalWrite(FILT0_BN, ((filt_i & 0x02) == 0));
    digitalWrite(FILT0_CN, ((filt_i & 0x04) == 0));
  }
}

void set_path_switch(float f)
{
  if (f > F_VCO_MAX) {
    digitalWrite(SW_1, SWITCH_HIGHFREQ);
    lmx2592_chan_power(CHANNELB, 0);
  }
  else {
    digitalWrite(SW_1, SWITCH_LOWFREQ);
    lmx2592_chan_power(CHANNELA, 0);
  }
}

// set attenuator value, in dB
void set_att(float att_db)
{
  float ATT_STEP = .5;
  uint8_t att = att_db / ATT_STEP;
  digitalWrite(ATT_1, att & BIT5 ? HIGH : LOW);
  digitalWrite(ATT_2, att & BIT4 ? HIGH : LOW);
  digitalWrite(ATT_3, att & BIT3 ? HIGH : LOW);
  digitalWrite(ATT_4, att & BIT2 ? HIGH : LOW);
  digitalWrite(ATT_5, att & BIT1 ? HIGH : LOW);
  digitalWrite(ATT_6, att & BIT0 ? HIGH : LOW);
  delay(10);
}

// sets the output power, measured power level error
float set_pow_dbm(float p, float f)
{
  float pdiff, att;
  uint8_t channel = f > F_VCO_MAX ? CHANNELB : CHANNELA;
  const float MAX_ATT = 30;
  set_att(MAX_ATT);
  Serial.println("starting dbm command");
  Serial.print("target power: ");
  Serial.println(p);
  
  lmx2592_chan_power(channel, 0);

  pdiff = adl5902_powerdet(output_freq) - p;
  Serial.print("initial pdiff: ");
  Serial.println(pdiff);
  
  if(pdiff > 0) {
    att = MAX_ATT;    
  }
  else if(-pdiff > MAX_ATT) {
    att = 0;
  }
  else {
    att = MAX_ATT + pdiff;
  }
  Serial.print("setting att: ");
  Serial.println(att);
  set_att(att);

  pdiff = adl5902_powerdet(output_freq) - p;
  Serial.print("new pdiff: ");
  Serial.println(pdiff);
  
  if(-pdiff > att){
    for(uint8_t pidx = 0; pidx < 62; pidx++) {
      lmx2592_chan_power(channel, pidx);
      pdiff = adl5902_powerdet(output_freq) - p;
      Serial.print("pow pdiff: ");
      Serial.print(pidx);
      Serial.print(", ");
      Serial.println(pdiff);
      if(pdiff > 0) {
        lmx2592_chan_power(channel, pidx+1);
        pdiff = adl5902_powerdet(output_freq) - p;
        break;
      }
    }
  }

  set_att(min(att + pdiff, MAX_ATT));
  pdiff = adl5902_powerdet(output_freq) - p;
  Serial.print("final pdiff: ");
  Serial.println(pdiff);
  return pdiff;
}
void lmx2592_set_freq(float f)
{
  float n_step = PFD * PRE_N;
  float frac_step = n_step / FRAC_DENOM;
  uint8_t div1 = 1;
  uint8_t div2 = 1;
  uint8_t div3 = 1;

  uint16_t n = MIN_N;
  uint32_t frac = 0;
  uint32_t div_i = -1;

  const uint16_t N_DIV_RATIOS = 11;
  const uint32_t div_ratios[N_DIV_RATIOS] =   {2, 4, 8, 12, 16, 24, 48, 96, 128};
  const uint32_t div1_options[N_DIV_RATIOS] = {0, 0, 0, 0, 0, 0, 0,  0,  0}; // for some reason, div3 on seg1 doesn't work..
  const uint32_t div2_options[N_DIV_RATIOS] = {0, 1, 2, 4, 8, 4, 4,  8,  8};
  const uint32_t div3_options[N_DIV_RATIOS] = {0, 0, 0, 0, 0, 1, 2,  4,  8};
  output_freq = f;

  if (f < F_VCO_MIN) {
    for (div_i = 0; div_i < N_DIV_RATIOS; div_i++) {
      if (f > F_VCO_MIN / div_ratios[div_i]) {
        div1 = div1_options[div_i];
        div2 = div2_options[div_i];
        div3 = div3_options[div_i];
        break;
      }
    }

    n = calc_n(f, n_step, div_ratios[div_i]);
    frac = calc_frac(f, n, n_step, frac_step, div_ratios[div_i]);
  }
  else if (f > F_VCO_MAX) {
    n = calc_n(f / 2, n_step, 1);
    frac = calc_frac(f / 2, n, n_step, frac_step, 1);
  }
  else {
    n = calc_n(f, n_step, 1);
    frac = calc_frac(f, n, n_step, frac_step, 1);

  }

  uint32_t frac_lsw = frac & 0xFFFF;
  uint32_t frac_msw = (frac >> 16) & 0xFFFF;

  // load frac and n registers
  spi_set_reg(38, (n << REG38_PLL_N));

  spi_set_reg(44, frac_msw);
  spi_set_reg(45, frac_lsw);

  if (f > F_VCO_MAX) {
    spi_set_reg(30, REG30_VCO_2X_EN);
  }
  else {
    spi_set_reg(30, 0);
  }

  // disable dividers if we're using VCO output directly
  if (f > F_VCO_MIN) {
    spi_set_reg(34, 0);
    spi_set_reg(35, 0);
    spi_set_reg(36, 0);
    spi_set_reg(48, REG48_OUTB_MUX_VCO);
    spi_set_reg(47, REG47_OUTA_MUX_VCO);

    // enable B to bypass filter bank, disable A buffer
    spi_set_reg(31, REG31_CHDIV_DIST_PD);
  }

  else {
    uint32_t reg35 = REG35_CHDIV_SEG1_EN;
    uint32_t reg36 = REG36_CHDIV_DISTA_EN;

    if (div3 != 0) {
      reg35 |= REG35_CHDIV_SEG2_EN | REG35_CHDIV_SEG3_EN;
      reg35 |= div2_options[div_i] << REG35_CHDIV_SEG2;
      reg35 |= div1_options[div_i] << REG35_CHDIV_SEG1;

      reg36 |= div3_options[div_i] << REG36_CHDIV_SEG3;
      reg36 |= REG36_CHDIV_SEG_SEL_123;
    } else if (div2 != 0) {
      reg35 |= REG35_CHDIV_SEG2_EN;
      reg35 |= div2_options[div_i] << REG35_CHDIV_SEG2;
      reg35 |= div1_options[div_i] << REG35_CHDIV_SEG1;
      reg36 |= REG36_CHDIV_SEG_SEL_12;
    } else {
      reg35 |= 0;//div1_options[div_i] << REG35_CHDIV_SEG1;
      reg36 |= REG36_CHDIV_SEG_SEL_1;
    }

    spi_set_reg(31, REG31_VCO_DISTB_PD);
    spi_set_reg(34, REG34_CHDIV_EN);
    spi_set_reg(35, reg35);
    spi_set_reg(36, reg36);
    spi_set_reg(48, REG48_OUTB_MUX_DIV);
    spi_set_reg(47, REG47_OUTA_MUX_DIV);
  }
  // recalibrate vco
  spi_set_reg(0, REG0_LD_EN | REG0_FCAL_EN | REG0_MUXOUT_SEL);
}

void setup()
{
  Serial.begin(9600);
  SPI.begin();
  gpio_init();
  adl5902_init();
  ltc2323_init();
  delay(10);
  clk_init();
  lmx2592_init();

  
  lmx2592_set_denom(FRAC_DENOM);
  lmx2592_set_freq(500e6);
  set_filterbank(500e6);
  set_path_switch(500e6);
//  lmx2592_chan_power(CHANNELA, 0);

  float pow = adl5902_powerdet(output_freq);
  Serial.print("power: ");
  Serial.println(pow);

  Ethernet.begin(mac, ip);
  Udp.begin(port);
}

uint8_t get_char()
{
  while (Serial.available() == 0);
  return Serial.read();
}

void loop()
{
  const uint8_t switches[6] =   {SW_0, SW_1, SW_2, SW_3, SW_4, SW_5};
  const uint8_t sw_state[2] =   {LOW, HIGH};
  uint8_t c_temp;
  int8_t p_temp;
  int16_t i_temp;
  float f_temp;
  float output_power;
  int32_t adc1, adc2;
  int16_t adc1_avg, adc2_avg;
  uint32_t adc_tmp;
  uint64_t freq_long;
  uint8_t cmd, idx;
  uint8_t reply_buffer_size;

  IPAddress remote;

  int32_t packet_size = Udp.parsePacket();

  if (packet_size) {
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    reply_buffer_size = 1;
    cmd = packetBuffer[0];
    idx = packetBuffer[1];
    replyBuffer[0] = cmd;
    
    switch (cmd) {
      case SWITCH_CMD:
        c_temp = packetBuffer[2];
        digitalWrite(switches[idx], sw_state[c_temp]);
        Serial.print("state: ");
        Serial.print(c_temp);
        Serial.print("idx: ");
        Serial.print(idx);
        Serial.print(" ");
        break;

      case FILT_CMD:
        c_temp = packetBuffer[2];
        // TODO: write filter path command,
        // TODO: add filter selection to freq command
        if (idx == CHANNELA) {
          digitalWrite(FILT0_A, ((c_temp & 0x01) > 0));
          digitalWrite(FILT0_B, ((c_temp & 0x02) > 0));
          digitalWrite(FILT0_C, ((c_temp & 0x04) > 0));
          digitalWrite(FILT0_AN, ((c_temp & 0x01) == 0));
          digitalWrite(FILT0_BN, ((c_temp & 0x02) == 0));
          digitalWrite(FILT0_CN, ((c_temp & 0x04) == 0));

        }
        break;

      case POW_CMD:
        c_temp = packetBuffer[2];
        lmx2592_chan_power(idx, c_temp);
        Serial.print("pow: ");
        Serial.print(c_temp);
        Serial.print("chan: ");
        Serial.print(idx);
        Serial.print(" ");
        break;
        
      case DBM_CMD:
        p_temp = packetBuffer[1];
        if(p_temp > 127) { // this is a terrible idea
          p_temp ^= 0xFF;
          p_temp += 1;
          p_temp = -p_temp;
        }
        set_pow_dbm(p_temp, output_freq);
        reply_buffer_size = 4;
        replyBuffer[1] = adc1_avg & 0xff; // measured power (dBm * 4)
        replyBuffer[1] = adc1_avg & 0xff; // attenuator setting (raw index)
        replyBuffer[1] = adc1_avg & 0xff; // power setting (raw index)
        
        break;
        
      case OUTPUT_CMD:
        freq_long = packetBuffer[2] + (packetBuffer[3] << 8) + (packetBuffer[4] << 16) + (packetBuffer[5] << 24);
        f_temp = freq_long;
        f_temp = (double) f_temp * (double) 10.00; // parse float uses an int internally, so we are limited to 10 hz resolution..

        Serial.print("freq: ");
        Serial.print(f_temp);
        Serial.print(" ");

        lmx2592_set_freq(f_temp);
        set_filterbank(f_temp);
        set_path_switch(f_temp);
        break;

      case ATT_CMD:
        c_temp = packetBuffer[2];
        digitalWrite(ATT_1, c_temp & BIT5 ? HIGH : LOW);
        digitalWrite(ATT_2, c_temp & BIT4 ? HIGH : LOW);
        digitalWrite(ATT_3, c_temp & BIT3 ? HIGH : LOW);
        digitalWrite(ATT_4, c_temp & BIT2 ? HIGH : LOW);
        digitalWrite(ATT_5, c_temp & BIT1 ? HIGH : LOW);
        digitalWrite(ATT_6, c_temp & BIT0 ? HIGH : LOW);
        Serial.print("att: ");
        Serial.print(c_temp);
        Serial.print("chan: ");
        Serial.print(idx);
        Serial.print(" ");
        break;

      case IQ_CMD:
        adc_tmp = ltc2323_conv(); // one conversion lag 
        adc1 = 0;
        adc2 = 0;
        
        for(c_temp = 0; c_temp < ADC_AVG; c_temp++) {
              adc_tmp = ltc2323_conv(); // do a few conversions to work the cruft out..
              adc1 += (int16_t) (adc_tmp & 0xffff);
              adc2 += (int16_t) ((adc_tmp >> 16) & 0xffff);
        }

        adc1_avg = adc1 /= ADC_AVG;
        adc2_avg = adc2 /= ADC_AVG;


        
        reply_buffer_size = 5;
 
        Serial.print("adc1: ");
        Serial.print(adc1_avg);
        Serial.print(" adc2: ");
        Serial.print(adc2_avg);
        Serial.print(" ");
        
        replyBuffer[1] = adc1_avg & 0xff;
        replyBuffer[2] = (adc1_avg >> 8) & 0xff;
        replyBuffer[3] = adc2_avg & 0xff;
        replyBuffer[4] = (adc2_avg >> 8) & 0xff;
  
        break;

      case DET_CMD:
        c_temp = packetBuffer[2];
        output_power = adl5902_powerdet(output_freq);
        i_temp = output_power * 4;
        Serial.print("det: ");
        Serial.print(output_power);
        reply_buffer_size = 3;
        replyBuffer[1] = i_temp & 0xff;
        replyBuffer[2] = (i_temp >> 8) & 0xff;
        
        break;

      default:
        Serial.print(" unrecognized command ");
        Serial.write(CMD_ERR);
        break;
    }
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(replyBuffer, reply_buffer_size);
    Udp.endPacket();
    Serial.print(cmd);
    Serial.println(" - finished command");
  }


}
