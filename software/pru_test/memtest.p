; adc.p: move samples from ad9864 into shared ram
; pins: 
;   douta   - data output from adc  - P9.31, R31 0
;   fs      - frame sync            - P9.29, R31 1
;   clkout  - spi clk output        - P9.30, R31 2
; 

#define DOUTA 0
#define FS 1
#define CLKOUT 2

#define ADC_VAL r5
#define TMP r6
#define TMP_IDX r10
#define INREG 31
#define RADDR r7

#define BITS_PER_SAMPLE 16

; defines from http://www.embedded-things.com/bbb/understanding-bbb-pru-shared-memory-access/
#define CONST_PRUCFG         C4
#define CONST_PRUSHAREDRAM   C28
#define PRU0_CTRL            0x22000
#define CTPPR0               0x28
#define SHARED_RAM           0x100
 
  
.origin 0
.entrypoint TOP

; reads ADC, stores result in ADC_VAL (r5)
; uses TMP (r5) and TMP_IDX (r10) registers 

.macro READADC
    mov TMP_IDX, BITS_PER_SAMPLE 
    mov TMP, 0
 
    WBS r31, FS
    WBC r31, FS

    READBIT:
        WBC r31, CLKOUT
        AND TMP, r31, DOUTA
        OR ADC_VAL, ADC_VAL, TMP
        LSL ADC_VAL, ADC_VAL, 1
        SUB TMP_IDX, TMP_IDX, 1
        WBS r31, CLKOUT ; TODO: do I need to do this?
        QBNE READBIT, TMP_IDX, 0
.endm

TOP:
    LBCO    r0, CONST_PRUCFG, 4, 4          ; Enable OCP master port
    CLR     r0, r0, 4
    SBCO    r0, CONST_PRUCFG, 4, 4
    
    MOV     r0, SHARED_RAM                  ; Set C28 to point to shared RAM
    MOV     r1, PRU0_CTRL + CTPPR0
    SBBO    r0, r1, 0, 4
    
    MOV r2, 1
    SBCO r2, CONST_PRUSHAREDRAM, 0, 4

    MOV r2, 2
    SBCO r2, CONST_PRUSHAREDRAM, 4, 4

    MOV r2, 3
    SBCO r2, CONST_PRUSHAREDRAM, 8, 4

    READADC 
    SBCO ADC_VAL, CONST_PRUSHAREDRAM, 12, 4

    READADC 
    SBCO ADC_VAL, CONST_PRUSHAREDRAM, 16, 4

    READADC 
    SBCO ADC_VAL, CONST_PRUSHAREDRAM, 20, 4


    MOV r31.b0, 32 + 3
    HALT

