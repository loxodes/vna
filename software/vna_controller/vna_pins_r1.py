# pins on vna r1 control board

class PINS(object):
    ### PRU
    # AD_DOUTD, pr1_pru1_pru_r31_0 
    # AD_DOUTC, pr1_pru1_pru_r31_1 
    # AD_DOUTB, pr1_pru1_pru_r31_2 
    # AD_DOUTA, pr1_pru1_pru_r31_3
    # AD_FS, pr1_pru1_pru_r31_4 
    # AD_CLKOUT, pr1_pru1_pru_r31_5 
    EXT_TRIG = "GPIO2_12" # pr1_pru1_pru_r31_6 
    PORT_SEL_PRU = "GPIO2_13" # pr1_pru1_pru_r30_7 
    PORT_SEL_GPIO = "GPIO2_4"
    TP1307 = "GPIO2_23"
    TP1308 = "GPIO2_25"
    EEPROM_WP = "GPIO2_5"
    
    ### EXT
    EXT_UART_MTX = 'GPIO0_15'
    EXT_UART_MRX = 'GPIO1_10'
    EXT_AIN0 = 'AIN5'
    EXT_AIN1 = 'AIN6'
    # EXT_SPI_CLK, SPI0_SCLK
    # EXT_SPI_MISO, SPI0_D0
    # EXT_SPI_MOSI, SPI0_D1
    # EXT_SPI_CS0, SPI0_CS0
    EXT_SPI_CS1 = 'GPIO2_1'
    EXT_IO_0 = 'GPIO1_29'
    EXT_IO_1 = 'GPIO1_30'
    EXT_IO_2 = 'GPIO1_31'
    EXT_IO_3 = 'GPIO2_0'

    ### RF
    RF_3V3_EN = 'GPIO1_8'
    MIX_X2 = 'GPIO1_9'
    PLL_3V3_EN = 'GPIO0_12'
    RF_AMP_EN = 'GPIO0_13'
    RF_SYNTH_CS = 'GPIO3_15'
    LO_SYNTH_CS = 'GPIO3_16'
    RF_DAC_CS = 'GPIO3_17'
    LO_SPI_CLK = 'GPIO3_18'
    LO_SPI_SDI = 'GPIO3_19'
    RF_SPI_CLK = 'GPIO3_20'
    RF_SPI_SDI = 'GPIO3_21'

    LO_AMP_EN = 'GPIO0_19'
    RF_M5V_EN = 'GPIO0_20'
    EXT_DEMOD_3V3_EN = 'GPIO0_7'
    ADC_CLK_EN = 'GPIO1_16'
    MIX_EN = 'GPIO1_17'
    LO_BUF_AMP_EN = 'GPIO1_27'
    LO_3V3_EN = 'GPIO1_28'
    LO_PORT_SEL = 'GPIO0_30'
    LO_DAC_CS = 'GPIO0_31'
    
    LO_M5V_EN = 'GPIO1_0'
    PLL_REF_SEL = 'GPIO1_1'
    RF_FILT_SW_1 = 'GPIO1_2'
    RF_FILT_SW_2 = 'GPIO1_3'
    RF_SYNTH_CE = 'GPIO1_4'
    RF_SYNTH_LOCK = 'GPIO1_5'
    LO_SYNTH_LOCK = 'GPIO1_6'
    LO_SYNTH_CE = 'GPIO1_7'

    AD_SYNCB = 'GPIO0_22'
    AD_PE_D = 'GPIO0_23'
    AD_PE_C = 'GPIO0_26'
    AD_PE_B = 'GPIO0_27'
    AD_PE_A = 'GPIO1_12'

    AD_PC = 'GPIO1_13'
    AD_PD = 'GPIO1_14'
    AD_DOUTB = 'GPIO1_15'
