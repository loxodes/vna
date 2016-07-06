// terrible bit-banged driver for ADC to test hardware..

#define ADC_BITS 16
#define CNV_DELAY 1
#define SCK_DELAY 1

int ADC_CNV_INPUT = 31; // LTC2323 pin 9, high defines sample phase, low starts conversion phase
int ADC_CNV_CLK_OUT = 32; // LTC2323 conversion clock output
int ADC_CNV_EN = 33; // LTC2323 conversion enable, high is enabled?
int ADC_SCK = 34; // LTC2323 pin 21, input spi clock
int ADC_CLKOUT = 35; // LTC2323 pin 17, output spi clock
int ADC_SD2 = 36; // LTC2323 pin 19, adc channel 1
int ADC_SD1 = 37; // LTC2323 pin 15, adc channel 1  
int DUTPORT_SW = 2; //
int S21_SW = LOW;
int S11_SW = HIGH;
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

void setup() {
  Serial.begin(9600);
  Serial.println("hello!");
  ltc2323_init();
  pinMode(DUTPORT_SW, OUTPUT);
  digitalWrite(DUTPORT_SW, S11_SW);
}

void loop() {
  int32_t sdo1 = 0;
  int32_t sdo2 = 0;
  uint32_t sample = ltc2323_conv();
  
  for(uint32_t i = 0; i < 64; i++) {
    uint32_t sample = ltc2323_conv();
    sdo1 += ((int16_t) (sample & 0xFFFF));
    sdo2 += ((int16_t) (sample >> 16));
  }
  
  sdo1 /= 64;
  sdo2 /= 64;

  
  Serial.print("1:");
  Serial.print(sdo1);
  Serial.print(" 2:");
  Serial.println(sdo2);
  
  delay(500);
}



