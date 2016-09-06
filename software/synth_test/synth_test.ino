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
#define ATT_CMD 'a'
#define IQ_CMD 'q'
#define CMD_ERR 'E'

#define SWITCH_LOWFREQ LOW
#define SWITCH_HIGHFREQ HIGH

// pins
const uint8_t LMX_LE = 14;
const uint8_t LMX_CE = 18;
const uint8_t LMX_AUX = 12;
const uint8_t LMX_POWEN = 32;

const uint8_t REFCLK_EN = 24;

const uint8_t SW_0 = 6;
const uint8_t SW_1 = 6;
const uint8_t SW_2 = 6;
const uint8_t SW_3 = 6;
const uint8_t SW_4 = 6;
const uint8_t SW_5 = 6;

const uint8_t I_0 = 26;
const uint8_t Q_0 = 28;
const uint8_t I_1 = 26;
const uint8_t Q_1 = 28;

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

const uint8_t DET_0 = A14; // pin 23


// TODO fix pins
int ADC_CNV_INPUT = 31; // LTC2323 pin 9, high defines sample phase, low starts conversion phase
int ADC_CNV_CLK_OUT = 32; // LTC2323 conversion clock output
int ADC_CNV_EN = 33; // LTC2323 conversion enable, high is enabled?
int ADC_SCK = 34; // LTC2323 pin 21, input spi clock
int ADC_CLKOUT = 35; // LTC2323 pin 17, output spi clock
int ADC_SD2 = 36; // LTC2323 pin 19, adc channel 1
int ADC_SD1 = 37; // LTC2323 pin 15, adc channel 1  

// synth settings
const uint16_t MIN_N = 16;
const uint32_t FRAC_DENOM = 200000; 
const float PFD = 100e6;
const float F_VCO_MIN = 3.55e9;
const float F_VCO_MAX = 7.1e9;
const uint32_t PRE_N = 2;

// ethernet stuff
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192,168,1,177);
unsigned int port = 8888;
EthernetUDP Udp;

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet
char replyBuffer[UDP_TX_PACKET_MAX_SIZE]; // buffer to hold outgoing packet 


float output_freq;

void ltc2323_init()
{
  pinMode(ADC_CNV_INPUT, OUTPUT);
  pinMode(ADC_CNV_CLK_OUT, INPUT_PULLUP);
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
  
//  digitalWrite(ADC_SCK, HIGH);

  digitalWrite(ADC_CNV_INPUT, HIGH);
  delayMicroseconds(CNV_DELAY);
  digitalWrite(ADC_CNV_INPUT, LOW);
  delayMicroseconds(CNV_DELAY);
  
  for(uint32_t i = 0; i < ADC_BITS; i++) {
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
      0x00af}; // 64
    
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

    pinMode(LMX_POWEN, INPUT);
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
    if(chan == CHANNELB) {
        spi_set_reg(47, (0x3F & power) << REG47_OUTB_POW);
        spi_set_reg(46, REG46_OUTA_PD);
    }
    else if(chan == CHANNELA) {
        spi_set_reg(46, REG46_OUTB_PD |(0x3F & power) << REG46_OUTA_POW);
    } 
}

float adl5902_get_int(float f)
{
  return -37;
}

float adl5902_get_slope(float f)
{
  return 47.5e-3;
}

void adl5902_init()
{
//  analogReference(INTERNAL2V5);
  analogReadResolution(12);
  uint32_t i = 0;
  for(i = 0; i < 200; i++) {
    analogRead(DET_0);
  }
}
float adl5902_powerdet(float f)
{
  float ADC_REF = 2.5;
  float det_voltage, det_power;
  uint32_t ADC_STEPS = 4096;
  float det_adc = analogRead(DET_0);
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
    
    if(f > F_VCO_MAX) {
        digitalWrite(FILT0_A, HIGH);
        digitalWrite(FILT0_B, HIGH);
        digitalWrite(FILT0_C, HIGH);
        digitalWrite(FILT0_AN, HIGH);
        digitalWrite(FILT0_BN, HIGH);
        digitalWrite(FILT0_CN, HIGH);
    } else {
       if(f < filter_bank_cutoffs[0]) {
         for(filt_i = 1; filt_i < FILTER_BANK_SIZE; filt_i++) {
            if(f > filter_bank_cutoffs[filt_i]) {
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
    if(f > F_VCO_MAX) {
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
    const uint32_t div_ratios[N_DIV_RATIOS] =   {2, 4, 8, 12,16,24,48,96, 128};
    const uint32_t div1_options[N_DIV_RATIOS] = {0, 0, 0, 0, 0, 0, 0,  0,  0}; // for some reason, div3 on seg1 doesn't work..
    const uint32_t div2_options[N_DIV_RATIOS] = {0, 1, 2, 4, 8, 4, 4,  8,  8};
    const uint32_t div3_options[N_DIV_RATIOS] = {0, 0, 0, 0, 0, 1, 2,  4,  8};
    output_freq = f;
    
    if(f < F_VCO_MIN) {
        for(div_i = 0; div_i < N_DIV_RATIOS; div_i++) {
            if(f > F_VCO_MIN / div_ratios[div_i]) {
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
        n = calc_n(f/2, n_step, 1);
        frac = calc_frac(f/2, n, n_step, frac_step, 1);	
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

    if(f > F_VCO_MAX) {
        spi_set_reg(30, REG30_VCO_2X_EN);        
    } 
    else {
        spi_set_reg(30, 0);
    }
    
    // disable dividers if we're using VCO output directly
   if(f > F_VCO_MIN) {
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

        if(div3 != 0) {
            reg35 |= REG35_CHDIV_SEG2_EN | REG35_CHDIV_SEG3_EN;
            reg35 |= div2_options[div_i] << REG35_CHDIV_SEG2;
            reg35 |= div1_options[div_i] << REG35_CHDIV_SEG1;

            reg36 |= div3_options[div_i] << REG36_CHDIV_SEG3;
            reg36 |= REG36_CHDIV_SEG_SEL_123;
        } else if(div2 != 0) {
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
    Ethernet.begin(mac, ip);
    Udp.begin(port);
    SPI.begin();
    clk_init();
    gpio_init();
    adl5902_init();
//    ltc2323_init();
    lmx2592_init();
    
    lmx2592_set_denom(FRAC_DENOM);
    lmx2592_set_freq(500e6);
    set_filterbank(500e6);
    set_path_switch(500e6);
    lmx2592_chan_power(CHANNELA, 0);
     
    float pow = adl5902_powerdet(output_freq);
    Serial.print("power: ");
    Serial.println(pow);
}

uint8_t get_char()
{
  while(Serial.available() == 0);
  return Serial.read();
}

void loop()
{
  const uint8_t switches[6] =   {SW_0, SW_1, SW_2, SW_3, SW_4, SW_5};
  const uint8_t sw_state[2] =   {LOW, HIGH};
  uint8_t c_temp;
  float f_temp;
  float output_power;
  uint32_t adc1, adc2;
  uint8_t cmd, idx;
  
  IPAddress remote;
  Serial.print("idx: ");
  Serial.print(idx);
  Serial.print(" ");

  int32_t packet_size = Udp.parsePacket();
  
  if(packet_size) {
    Udp.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);
    
    cmd = packetBuffer[0];
    idx = packetBuffer[1];
    
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
        if(idx == CHANNELA) {
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
      /*  
      case SYNTH_CMD:
        while(Serial.available() == 0);
        f_temp = Serial.parseFloat();
  
        Serial.print("freq: ");
        Serial.print(f_temp);
        Serial.print(" ");
        f_temp = (double) f_temp * (double) 10.00; // parse float uses an int internally, so we are limited to 10 hz resolution..    
        lmx2592_set_freq(f_temp);
        break;*/
  
     case OUTPUT_CMD:
        while(Serial.available() == 0);
        f_temp = Serial.parseFloat();
  
        Serial.print("freq: ");
        Serial.print(f_temp);
        Serial.print(" ");
        f_temp = (double) f_temp * (double) 10.00; // parse float uses an int internally, so we are limited to 10 hz resolution..    
  
        lmx2592_set_freq(f_temp);
        set_filterbank(f_temp);
        set_path_switch(f_temp);
        break;
       
      case ATT_CMD:
        c_temp = get_char();
        
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
        if(idx == CHANNELA) {
          adc1 = analogRead(I_0);
          adc2 = analogRead(Q_0);
        }
        else if(idx == CHANNELB) {
          adc1 = analogRead(I_1);
          adc2 = analogRead(Q_1);
        }
        else {
          adc1 = 0;
          adc2 = 0;
        }
        
        //((int32_t *) &replyBuffer[0]) = adc1;
        //((int32_t *) &replyBuffer[1]) = adc2;

        //Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
        //Udp.write(ReplyBuffer);
        //Udp.endPacket();
        
        Serial.print(adc1);
        Serial.print(adc2);
        break;
                                
      case DET_CMD:
        c_temp = packetBuffer[2];
        output_power = adl5902_powerdet(output_freq);
        Serial.print("det: ");
        Serial.print(output_power); 
        break;
        
      default:
        Serial.print(" unrecognized command ");
        Serial.write(CMD_ERR);
        break;
    }
  }  
  Serial.print(cmd);
  Serial.println(" - finished command");
 
}
