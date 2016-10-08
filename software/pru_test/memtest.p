; Adc.p: move samples from ad9864 into shared ram
; pins: 
;   douta   - data output from adc  - P9.31, R31 0
;   fs      - frame sync            - P9.29, R31 1
;   clkout  - spi clk output        - P9.30, R31 2
; 

#include "adc_shm.h"

#define DOUTA 0
#define FS 1
#define CLKOUT 2

#define ADC_VAL r5
#define TMP r6
#defIne TMP_IDX r10
#define SAMPLE_COUNTER r12
#define INREG 31
#define RADDR r7


; defines from http://www.embedded-things.com/bbb/understanding-bbb-pru-shared-memory-access/
#define CONST_PRUCFG         C4
#define CONST_PRUSHAREDRAM   C28
#define PRU0_CTRL            0x22000
#define CTPPR0               0x28
#define SHARED_RAM           0x100

#define BYTES_PER_SAMPLE 4

.origin 0
.entrypoint TOP

; reads ADC, stores result in ADC_VAL (r5)
; uses TMP (r6) and TMP_IDX (r10) registers 
.macro READADC
    mov TMP_IDX, BITS_PER_SAMPLE 
    mov TMP, 0
    mov ADC_VAL, 0
 
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

; delay approximately TMP microseconds, uses and clears TMP, TMP_IDX
.macro DELAY_US
    DELAY_LOOP_OUTER:
       ADD TMP, TMP, 0 
        MOV TMP_IDX, 98
        DELAY_LOOP_INNER:
            SUB TMP_IDX, TMP_IDX, 1,  
            QBNE DELAY_LOOP_INNER, TMP_IDX, 0
        SUB TMP, TMP, 1
        QBNE DELAY_LOOP_OUTER, TMP, 0
.endm

TOP:
    LBCO    r0, CONST_PRUCFG, 4, 4          ; Enable OCP master port
    CLR     r0, r0, 4
    SBCO    r0, CONST_PRUCFG, 4, 4
    
    MOV     r0, SHARED_RAM                  ; Set C28 to point to shared RAM
    MOV     r1, PRU0_CTRL + CTPPR0
    SBBO    r0, r1, 0, 4
   
    MOV r2, ADC_BUF_STATUS_EMPTY
    SBCO r2, CONST_PRUSHAREDRAM, ADC_BUF_STATUS_IDX, 4
   
    LBCO &SAMPLE_COUNTER, CONST_PRUSHAREDRAM, SAMPLE_COUNT_IDX, 4
   
    MOV TMP, 15000
    DELAY_US
  
    SHM_LOOP_TOP:
        MOV r13, ADC_BUF_LEN_SAMPLES
        MOV r15, ADC_BUF_LEN_SAMPLES 
        SHM_BUF0:
            ; calculate next shm address in r14
            MOV r14, r13
            ADD r14, r14, ADC_BUF_OFFSET 
            LSL r14, r14, 2
            
            READADC
            MOV r2, r13
            SBCO r2, CONST_PRUSHAREDRAM, ADC_VAL, BYTES_PER_SAMPLE 
            
            ; loop ADC_BUF_LEN times..
            SUB r13, r13, 1 
            QBNE SHM_BUF0, r13, 0

        MOV r2, ADC_BUF_STATUS_BUF0
        SBCO r2, CONST_PRUSHAREDRAM, ADC_BUF_STATUS_IDX, 4

        MOV TMP, 7000
        DELAY_US
        
        MOV r13, ADC_BUF_LEN_SAMPLES
        SHM_BUF1:
            ; calculate next shm address in r14
            MOV r14, r13
            ADD r14, r14, ADC_BUF_OFFSET 
            ADD r14, r14, r15 ; target buffer 1
            LSL r14, r14, 2
            
            ; save current sample index to shm buffer
            ; (replace with ADC value..)
            READADC
            MOV r2, r13
            SBCO r2, CONST_PRUSHAREDRAM, ADC_VAL, BYTES_PER_SAMPLE 
            
            ; loop ADC_BUF_LEN times..
            SUB r13, r13, 1 
            QBNE SHM_BUF1, r13, 0

     
        MOV r2, ADC_BUF_STATUS_BUF1
        SBCO r2, CONST_PRUSHAREDRAM, ADC_BUF_STATUS_IDX, 4

        MOV TMP, 7000 
        DELAY_US

        SUB SAMPLE_COUNTER, SAMPLE_COUNTER, r15 
        SUB SAMPLE_COUNTER, SAMPLE_COUNTER, r15 

        QBNE SHM_LOOP_TOP, SAMPLE_COUNTER, 0


        SBCO r2, CONST_PRUSHAREDRAM, 4, 4

    MOV r31.b0, 32 + 3
    HALT

