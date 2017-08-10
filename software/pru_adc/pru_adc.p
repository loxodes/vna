; Adc.p: move samples from ad9864 into shared ram
; pins:                                  bit 
;   douta 1 - data output from adc1 - R31 1  P8_46
;   douta 2 - data output from adc2 - R31 3  P8_44
;   douta 3 - data output from adc3 - R31 5  P8_42
;   douta 4 - data output from adc4 - R31 7  P8_40
;   fs      - frame sync            - R31 2  P8_43
;   clkout  - spi clk output        - R31 0  P8_45
;   syncb   - sync input,           - R30 4  P8_41

#include "adc_shm.h"

#define DOUTA1_MASK 0x02
#define DOUTA2_MASK 0x08
#define DOUTA3_MASK 0x20
#define DOUTA4_MASK 0x80

#define A1_SHIFT 1
#define A2_SHIFT 3
#define A3_SHIFT 5
#define A4_SHIFT 7


#define FS 2
#define CLKOUT 0
;#define SYNCB 4

#define ADC_VAL1 r20
#define ADC_VAL2 r21
#define ADC_VAL3 r22
#define ADC_VAL4 r23

#define TMP r6
#defIne TMP_IDX r10
#define SAMPLE_COUNTER r12
#define INREG 31
#define RADDR r7


; defines from http://www.embedded-things.com/bbb/understanding-bbb-pru-shared-memory-access/
#define CONST_PRUCFG         C4
#define CONST_PRUSHAREDRAM   C28
#define PRU1_CTRL            0x24000
#define CTPPR0               0x28
#define SHARED_RAM           0x100

#define BYTES_PER_SAMPLE 4

.origin 0
.entrypoint TOP

; reads ADCs, stores results in ADC_VAL1-4 (r20-23)
; uses TMP (r6) and TMP_IDX (r10) registers 
.macro READADC
    mov TMP_IDX, BITS_PER_SAMPLE 
    mov TMP, 0

    mov ADC_VAL1, 0
    mov ADC_VAL2, 0
    mov ADC_VAL3, 0
    mov ADC_VAL4, 0
 
    WBS r31, FS
    WBC r31, FS

    READBIT:
        WBC r31, CLKOUT

        LSL ADC_VAL1, ADC_VAL1, 1 
        LSL ADC_VAL2, ADC_VAL2, 1
        LSL ADC_VAL3, ADC_VAL3, 1
        LSL ADC_VAL4, ADC_VAL4, 1

        ; read in ADC 1 
        AND TMP, r31, DOUTA1_MASK 
        LSR TMP, TMP, A1_SHIFT; move douta for adc1 into first bit
        OR ADC_VAL1, ADC_VAL1, TMP

        ; read in ADC 2
        AND TMP, r31, DOUTA2_MASK 
        LSR TMP, TMP, A2_SHIFT
        OR ADC_VAL2, ADC_VAL2, TMP

        ; read in ADC 3
        AND TMP, r31, DOUTA3_MASK 
        LSR TMP, TMP, A3_SHIFT
        OR ADC_VAL3, ADC_VAL3, TMP

        ; read in ADC 4
        AND TMP, r31, DOUTA4_MASK 
        LSR TMP, TMP, A4_SHIFT
        OR ADC_VAL4, ADC_VAL4, TMP

        WBS r31, CLKOUT
        SUB TMP_IDX, TMP_IDX, 1
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
    MOV     r1, PRU1_CTRL + CTPPR0
    SBBO    r0, r1, 0, 4
   
    MOV r2, ADC_BUF_STATUS_EMPTY
    SBCO r2, CONST_PRUSHAREDRAM, ADC_BUF_STATUS_IDX, 4
   
    LBCO &SAMPLE_COUNTER, CONST_PRUSHAREDRAM, SAMPLE_COUNT_IDX, 4
   

    MOV TMP, 10000
    DELAY_US
  

    SHM_LOOP_TOP:
        MOV r15, ADC_BUF_LEN_SAMPLES 

        MOV r13, 0 
        SHM_BUF0:
            ; calculate next shm address in r14
            MOV r14, r13
            LSL r14, r14, 2
            ADD r14, r14, ADC_BUF_OFFSET 
            
            READADC
            SBCO ADC_VAL1, CONST_PRUSHAREDRAM, r14, BYTES_PER_SAMPLE 
            ADD r14, r14, BYTES_PER_SAMPLE 
            SBCO ADC_VAL2, CONST_PRUSHAREDRAM, r14, BYTES_PER_SAMPLE 
            ADD r14, r14, BYTES_PER_SAMPLE 
            SBCO ADC_VAL3, CONST_PRUSHAREDRAM, r14, BYTES_PER_SAMPLE 
            ADD r14, r14, BYTES_PER_SAMPLE 
            SBCO ADC_VAL4, CONST_PRUSHAREDRAM, r14, BYTES_PER_SAMPLE 
            
            ; loop ADC_BUF_LEN times..
            ADD r13, r13, 4 
            QBNE SHM_BUF0, r13, r15


        MOV r2, ADC_BUF_STATUS_BUF0
        SBCO r2, CONST_PRUSHAREDRAM, ADC_BUF_STATUS_IDX, 4

        MOV r13, 0 

        SHM_BUF1:
            ; calculate next shm address in r14
            MOV r14, r13
            ADD r14, r14, r15 ; target buffer 1
            LSL r14, r14, 2
            ADD r14, r14, ADC_BUF_OFFSET 
            
            READADC
            SBCO ADC_VAL1, CONST_PRUSHAREDRAM, r14, BYTES_PER_SAMPLE 
            ADD r14, r14, BYTES_PER_SAMPLE 
            SBCO ADC_VAL2, CONST_PRUSHAREDRAM, r14, BYTES_PER_SAMPLE 
            ADD r14, r14, BYTES_PER_SAMPLE 
            SBCO ADC_VAL3, CONST_PRUSHAREDRAM, r14, BYTES_PER_SAMPLE 
            ADD r14, r14, BYTES_PER_SAMPLE 
            SBCO ADC_VAL4, CONST_PRUSHAREDRAM, r14, BYTES_PER_SAMPLE 
           
            ; loop ADC_BUF_LEN times..
            ADD r13, r13, 4 
            QBNE SHM_BUF1, r13, r15

     

        MOV r2, ADC_BUF_STATUS_BUF1
        SBCO r2, CONST_PRUSHAREDRAM, ADC_BUF_STATUS_IDX, 4

        SUB SAMPLE_COUNTER, SAMPLE_COUNTER, r15 
        SUB SAMPLE_COUNTER, SAMPLE_COUNTER, r15 

        QBNE SHM_LOOP_TOP, SAMPLE_COUNTER, 0

        SBCO r2, CONST_PRUSHAREDRAM, 4, 4

    MOV r31.b0, 32 + 3

    HALT

