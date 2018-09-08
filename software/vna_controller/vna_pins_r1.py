# pins on vna r1 control board

class PINS(object):
    ### PRU
    # AD_DOUTD, pr1_pru1_pru_r31_0 
    # AD_DOUTC, pr1_pru1_pru_r31_1 
    # AD_DOUTB, pr1_pru1_pru_r31_2 
    # AD_DOUTA, pr1_pru1_pru_r31_3
    # AD_FS, pr1_pru1_pru_r31_4 
    # AD_CLKOUT, pr1_pru1_pru_r31_5 
    EXT_TRIG = (2,12) # pr1_pru1_pru_r31_6
    PORT_SEL_PRU = (2,13) # pr1_pru1_pru_r30_7
    PORT_SEL_GPIO = (2,4)
    TP1307 = (2,23)
    TP1308 = (2,25)
    EEPROM_WP = (2,5)
    
    ### EXT
    EXT_UART_MTX = (0,15)
    EXT_UART_MRX = (1,10)
    EXT_AIN0 = 'AIN5'
    EXT_AIN1 = 'AIN6'
    # EXT_SPI_CLK, SPI0_SCLK
    # EXT_SPI_MISO, SPI0_D0
    # EXT_SPI_MOSI, SPI0_D1
    # EXT_SPI_CS0, SPI0_CS0
    EXT_SPI_CS1 = (2,1)
    EXT_IO_0 = (1,29)
    EXT_IO_1 = (1,30)
    EXT_IO_2 = (1,31)
    EXT_IO_3 = (2,0)

    ### RF
    RF_3V3_EN = (1,8)
    MIX_X2 = (1,9)
    PLL_3V3_EN = (0,12)
    RF_AMP_EN = (0,13)
    RF_SYNTH_CS = (3,15)
    LO_SYNTH_CS = (3,16)
    RF_DAC_CS = (3,17)
    LO_SPI_CLK = (3,18)
    LO_SPI_SDI = (3,19)
    RF_SPI_CLK = (3,20)
    RF_SPI_SDI = (3,21)

    LO_AMP_EN = (0,19)
    RF_M5V_EN = (0,20)
    EXT_DEMOD_3V3_EN = (0,7)
    ADC_CLK_EN = (1,16)
    MIX_EN = (1,17)
    LO_BUF_AMP_EN = (1,27)
    LO_3V3_EN = (1,28)
    LO_PORT_SEL = (0,30)
    LO_DAC_CS = (0,31)
    
    LO_M5V_EN = (1,0)
    PLL_REF_SEL = (1,1)
    RF_FILT_SW_1 = (1,2)
    RF_FILT_SW_2 = (1,3)
    RF_SYNTH_CE = (1,4)
    RF_SYNTH_LOCK = (1,5)
    LO_SYNTH_LOCK = (1,6)
    LO_SYNTH_CE = (1,7)

    AD_SYNCB = (0,22)
    AD_PE_D = (0,23)
    AD_PE_C = (0,26)
    AD_PE_B = (0,27)
    AD_PE_A = (1,12)

    AD_PC = (1,13)
    AD_PD = (1,14)
    AD_DOUTB = (1,15)
