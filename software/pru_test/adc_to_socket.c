// Compile with:
// gcc -o loader loader.c -lprussdrv

// TODO: use interrupts or smarter polling to signal buffer is ready
// add socket dump of samples
// 
//
// Based on https://credentiality2.blogspot.com/2015/09/beaglebone-pru-gpio-example.html
// Based on http://www.righto.com/2016/08/pru-tips-understanding-beaglebones.html
// Based on https://groups.google.com/forum/#!topic/beagleboard/0a4tszlq2y0

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <prussdrv.h>
#include <pruss_intc_mapping.h>

#include <sys/mman.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <time.h>

#include "adc_shm.h"

#define PRU_NUM      0
#define PRUSS0_SHARED_DATARAM    4

#define TOTAL_SAMPLES 128 //7680000

// shared memory
// [ 32 bytes, config/misc ] [ 2048 bytes (512 samples) buffer 0 ] [ 2048 bytes (512 samples) buffer 1 ]

#define PRU_BIN "./memtest.bin"

static void *sharedMem;

static uint32_t *sharedMem_int;
//static uint16_t *sharedMem_sample;

int main(int argc, char **argv) {
  uint8_t target_buffer = 0;
  uint32_t i, t;

  printf("init pru..\n");
  prussdrv_init();
  if (prussdrv_open(PRU_EVTOUT_0) == -1) {
    printf("prussdrv_open() failed\n");
    return 1;
  }

  tpruss_intc_initdata pruss_intc_initdata = PRUSS_INTC_INITDATA;
  prussdrv_pruintc_init(&pruss_intc_initdata);

  prussdrv_map_prumem(PRUSS0_SHARED_DATARAM, &sharedMem);

  sharedMem_int = (unsigned int*) sharedMem;
 // sharedMem_sample = (int16_t*) sharedMem + ADC_BUF_OFFSET * 2;

  fprintf(stderr, "loading sample count to shared memory..\n");
  sharedMem_int[1] = TOTAL_SAMPLES;

  if (prussdrv_exec_program(PRU_NUM, PRU_BIN) < 0) {
    fprintf(stderr, "Error loading %s\n", PRU_BIN);
    exit(-1);
  }

  fprintf(stderr, "loaded adc reader.. waiting for PRU to initialize buffer status\n");

  fprintf(stderr, "%d %d: %d\n", target_buffer, ADC_BUF_STATUS_IDX, sharedMem_int[ADC_BUF_STATUS_IDX]);
  while(sharedMem_int[ADC_BUF_STATUS_IDX] != ADC_BUF_STATUS_EMPTY) {
    ;
  }

  fprintf(stderr, "\nbuffer is ready\n");
  uint32_t remaining_samples = TOTAL_SAMPLES;

  while(remaining_samples > 0) {

    //fprintf(stderr, "%d %d: %d\n", target_buffer, ADC_BUF_STATUS_IDX, sharedMem_int[ADC_BUF_STATUS_IDX]);
    if(sharedMem_int[ADC_BUF_STATUS_IDX] == target_buffer) {
        for(i = 0; i < ADC_BUF_LEN_SAMPLES; i++) {
            uint32_t mem_idx = ADC_BUF_OFFSET + ADC_BUF_LEN_SAMPLES * target_buffer + i;
            t = sharedMem_int[mem_idx];
            fprintf(stderr, "%d: %d\n", i, t);
        }
        remaining_samples -= ADC_BUF_LEN_SAMPLES;
        target_buffer ^= 1;
        printf("remaining samples: %d: new target: %d\n", remaining_samples, target_buffer);
    }
  }


  prussdrv_pru_wait_event(PRU_EVTOUT_0);
  printf("All done\n");
  
//  for(i = 0; i < TOTAL_SAMPLES; i++) {
//    fprintf(stderr, "%d: %d + j%d\n", i, sharedMem_sample[2*i], sharedMem_sample[2*i+1]);
//  }


  prussdrv_pru_clear_event(PRU_EVTOUT_0, PRU0_ARM_INTERRUPT);
  prussdrv_pru_disable(PRU_NUM);
  prussdrv_exit();


  return 0;
}
