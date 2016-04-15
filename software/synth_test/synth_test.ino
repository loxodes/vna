#include <SPI.h>

#define BIT0 (1 << 0)
#define BIT1 (1 << 1)
#define BIT2 (1 << 2)
#define BIT3 (1 << 3)
#define BIT4 (1 << 4)
#define BIT5 (1 << 5)
#define BIT6 (1 << 6)
#define BIT7 (1 << 7)
#define BIT8 (1 << 8)
#define BIT9 (1 << 9)
#define BIT10 (1 << 10)
#define BIT11 (1 << 11)
#define BIT12 (1 << 12)
#define BIT13 (1 << 13)
#define BIT14 (1 << 14)
#define BIT15 (1 << 15)
#define BIT16 (1 << 16)
#define BIT17 (1 << 17)
#define BIT18 (1 << 18)
#define BIT19 (1 << 19)
#define BIT20 (1 << 20)
#define BIT21 (1 << 21)
#define BIT22 (1 << 22)
#define BIT23 (1 << 23)

#define REG0_LD_EN BIT13
#define REG0_FCAL_EN BIT3
#define REG0_RESET BIT1
#define REG0_MUXOUT_SEL BIT2
#define REG46_MASH_ORDER_2 2
#define REG46_MASH_EN BIT5
#define REG46_OUTA_PD BIT6
#define REG46_OUTB_PD BIT7
#define REG46_OUTA_POW BIT8

#define REG38_PLL_N 1
#define REG39_PFD_DLY_2 BIT9

#define REG36_CHDIV_DISTB_EN BIT11
#define REG36_CHDIV_DISTA_EN BIT10
#define REG36_CHDIV_SEG_SEL_1 BIT4
#define REG36_CHDIV_SEG_SEL_12 BIT5
#define REG36_CHDIV_SEG_SEL_123 BIT6
#define REG36_CHDIV_SEG3 0

#define REG35_CHDIV_SEG2 9
#define REG35_CHDIV_SEG3_EN BIT8
#define REG35_CHDIV_SEG2_EN BIT7
#define REG35_CHDIV_SEG1 2 
#define REG35_CHDIV_SEG1_EN BIT1

#define REG34_CHDIV_EN BIT5

#define REG48_OUTB_MUX_VCO BIT0
#define REG48_OUTB_MUX_DIV 0

#define REG10_MULT 7
#define REG11_PLL_R 4
#define REG12_PLL_R_PRE 0
#define REG47_OUTB_POW 0

#define REG31_VCO_DISTA_PD BIT9

#define CHANNELA 0
#define CHANNELB 1

#define ON 1
#define OFF 0

// command structure
// [region][index][command]
#define SWITCH_CMD 'w'
#define FILT_CMD 'f'
#define POW_CMD 'p'
#define SYNTH_CMD 's'
#define DET_CMD 'd'
#define ATT_CMD 'a'
#define IQ_CMD 'q'
#define CMD_ERR 'E'

const uint8_t LMX_LE = 18;
const uint8_t LMX_CE = 17;
const uint8_t LMX_AUX = 19;
const uint8_t LMX_LOCK0 = 8;
const uint8_t LMX_LOCK1 = 19;

const uint16_t MIN_N = 16;
const uint32_t FRAC_DENOM = 200000; 
const float PFD = 100e6;
const float F_VCO_MIN = 3.55e9;
const float F_VCO_MAX = 7.1e9;
const uint32_t PRE_N = 2;

const uint8_t DET_0 = 28;

const uint8_t SW_0 = 28;
const uint8_t SW_1 = 29;
const uint8_t SW_2 = 30;
const uint8_t SW_3 = 13;
const uint8_t SW_4 = 12;
const uint8_t SW_5 = 11;

const uint8_t I_0 = 23;
const uint8_t Q_0 = 24;
const uint8_t I_1 = 25;
const uint8_t Q_1 = 26;

const uint8_t FILT0_A = 31;
const uint8_t FILT0_B = 32;
const uint8_t FILT0_C = 33;
const uint8_t FILT1_A = 34;
const uint8_t FILT1_B = 35;
const uint8_t FILT1_C = 36;

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
    
    d = d | LMX_REG_DEFAULTS[reg];
    
    digitalWrite(LMX_LE, LOW);
    SPI.transfer(reg);
    SPI.transfer((d >> 8) & 0xFF);
    SPI.transfer((d >> 0) & 0xFF);
    digitalWrite(LMX_LE, HIGH);
    Serial.print("register:");
    Serial.print(reg);
    Serial.print(" value: ");
    Serial.println(d, HEX);
    delay(1);
}
void gpio_init()
{
//    pinMode(SW_0, OUTPUT); (use SW_0 as DET)
    pinMode(SW_1, OUTPUT);
    pinMode(SW_2, OUTPUT);
    pinMode(SW_3, OUTPUT);
    pinMode(SW_4, OUTPUT);
    pinMode(SW_5, OUTPUT);

    pinMode(FILT0_A, OUTPUT);
    pinMode(FILT0_B, OUTPUT);
    pinMode(FILT0_C, OUTPUT);
    pinMode(FILT1_A, OUTPUT);
    pinMode(FILT1_B, OUTPUT);
    pinMode(FILT1_C, OUTPUT); 
}
void lmx2592_init()
{
    pinMode(LMX_LE, OUTPUT);
    pinMode(LMX_CE, OUTPUT);
    pinMode(LMX_AUX, INPUT);

    digitalWrite(LMX_CE, HIGH);
    digitalWrite(LMX_LE, HIGH);
    delay(100);

    delay(10);
    spi_set_reg(0, REG0_RESET);
    
//    program registers with defaults?!
//    for(int i = 1; i < 65; i++) {
//      spi_set_reg(i, 0);
//    } 
      // 0x0F23
      // mash order 3, mash en, 
    spi_set_reg(46, REG46_MASH_ORDER_2 | REG46_MASH_EN | REG46_OUTA_PD);
    spi_set_reg(31, REG31_VCO_DISTA_PD);

//    spi_set_reg(12, 1 << REG12_PLL_R_PRE);
//    spi_set_reg(11, 1 << REG11_PLL_R);
//    spi_set_reg(10, 1 << REG10_MULT);
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
    }
}

uint32_t calc_n(float f, float n_step, uint32_t div)
{
    return f / (n_step / div);
}

uint32_t calc_frac(float f, uint32_t n, float n_step, float frac_step, uint32_t div)
{
    return (f - n * (n_step / div)) / (frac_step / div);
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
    const uint32_t div2_options[N_DIV_RATIOS] = {0, 1, 2, 4, 8, 4, 8,  8,  8};
    const uint32_t div3_options[N_DIV_RATIOS] = {0, 0, 0, 0, 0, 1, 1,  4,  8};    
    if(f < F_VCO_MIN) {
        for(div_i = 0; div_i < N_DIV_RATIOS; div_i++) {
            Serial.print("i: ");\
            Serial.println(div_i);\
            if(f > F_VCO_MIN / div_ratios[div_i]) {
                div1 = div1_options[div_i];
                div2 = div2_options[div_i];
                div3 = div3_options[div_i];
                Serial.print("div1: ");\
                Serial.print(div1);
                Serial.print(" div2: ");
                Serial.print(div2);
                Serial.print(" div3: ");
                Serial.println(div3);
                break;
            }
        }

        n = calc_n(f, n_step, div_ratios[div_i]);
        frac = calc_frac(f, n, n_step, frac_step, div_ratios[div_i]);
    }
    else if (f > F_VCO_MAX) {
        // TODO: floatr is currently unsupported
        n = MIN_N;
        frac = 0;	
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
    // disable dividers if we're using VCO output directly	
    if(f > F_VCO_MIN) {
        Serial.println("using vco directly!");
        spi_set_reg(34, 0);
        spi_set_reg(35, 0);
        spi_set_reg(36, 0);
        spi_set_reg(48, REG48_OUTB_MUX_VCO);
    }

    else {
        uint32_t reg35 = REG35_CHDIV_SEG1_EN;
        uint32_t reg36 = REG36_CHDIV_DISTB_EN;
        Serial.println("using output dividers!");

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
            Serial.print("div1: ");
            Serial.println(div1_options[div_i]);
            reg35 |= 0;//div1_options[div_i] << REG35_CHDIV_SEG1;
            reg36 |= REG36_CHDIV_SEG_SEL_1;
        }

        spi_set_reg(34, REG34_CHDIV_EN);
        spi_set_reg(35, reg35);
        spi_set_reg(36, reg36);
        spi_set_reg(48, REG48_OUTB_MUX_DIV);

    }
        Serial.print("n: ");
        Serial.println(n);
        Serial.print("frac: ");
        Serial.println(frac);    
    // recalibrate vco
    spi_set_reg(0, REG0_LD_EN | REG0_FCAL_EN | REG0_MUXOUT_SEL);
}

void setup()
{
    Serial.begin(9600);
    Serial.println("starting!");
    SPI.begin();
    lmx2592_init();
    lmx2592_chan_power(CHANNELB, 15);
    lmx2592_set_denom(FRAC_DENOM);
    lmx2592_set_freq(3.450e9);
}


void loop()
{
  const uint8_t switches[6] =   {SW_0, SW_1, SW_2, SW_3, SW_4, SW_5};
  const uint8_t sw_state[2] =   {LOW, HIGH};
  uint8_t c_temp;
  float f_temp;
  uint16_t adc1, adc2;
  
  if (Serial.available() > 2) {
    uint8_t cmd = Serial.read();
    uint8_t idx = Serial.read();
    delay(50); // TODO: wait for an appropriate number of bytes for each command
    
    switch (cmd) {
      case SWITCH_CMD:
        c_temp = Serial.read();
        digitalWrite(switches[idx], sw_state[c_temp]);
        Serial.write(cmd);
        break;
        
      case FILT_CMD:
        c_temp = Serial.read();
        Serial.write(cmd);
        if(idx == CHANNELA) {
          digitalWrite(FILT0_A, (c_temp & 0x01 > 0));
          digitalWrite(FILT0_B, (c_temp & 0x02 > 0));
          digitalWrite(FILT0_C, (c_temp & 0x04 > 0));
        }
        else if(idx == CHANNELB) {
          digitalWrite(FILT1_A, (c_temp & 0x01 > 0));
          digitalWrite(FILT1_B, (c_temp & 0x02 > 0));
          digitalWrite(FILT1_C, (c_temp & 0x04 > 0));
        }
        break;
        
      case POW_CMD:
        c_temp = Serial.read();
        lmx2592_chan_power(idx, c_temp);
        break;
        
      case SYNTH_CMD:
        // TODO: write more commands? set power, etc..
        f_temp = Serial.parseFloat();
        lmx2592_set_freq(f_temp);
        Serial.write(cmd);
        break;
        
      case ATT_CMD:
        c_temp = Serial.read();
        // TODO set attenuator pins..
        Serial.write(CMD_ERR);
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
        Serial.write(adc1);
        Serial.write(adc2);
        Serial.write(cmd);
        break;
                                
      case DET_CMD:
        adc1 = analogRead(DET_0);
        Serial.write(adc1);
        Serial.write(cmd);
        break;
        
      default:
        Serial.write(CMD_ERR);
        break;
    }
    
    Serial.write('\n');    
  }
}
