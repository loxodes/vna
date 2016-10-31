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

#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#include <sys/mman.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <time.h>

#include "adc_shm.h"

#define PRU_NUM      0
#define PRUSS0_SHARED_DATARAM    4
#define SAMPLE_PORT 10520
#define MAX_SAMPLE_BUFFER 768000

// shared memory
// [ 32 bytes, config/misc ] [ 2048 bytes (512 samples) buffer 0 ] [ 2048 bytes (512 samples) buffer 1 ]

#define PRU_BIN "./memtest.bin"

static void *sharedMem;

static uint32_t *sharedMem_int;
static int16_t *sharedMem_sample;


// launch adc program on PRU, stuff nsamples into ADC *sample_buffer
int grab_samples_pru(uint32_t nsamples, int16_t *sample_buffer)
{
  uint8_t target_buffer = 0;
  uint32_t i;
  uint32_t sample_idx = 0;

  //printf("init pru..\n");
  prussdrv_init();
  if (prussdrv_open(PRU_EVTOUT_0) == -1) {
    printf("prussdrv_open() failed\n");
    return 1;
  }

  tpruss_intc_initdata pruss_intc_initdata = PRUSS_INTC_INITDATA;
  prussdrv_pruintc_init(&pruss_intc_initdata);

  prussdrv_map_prumem(PRUSS0_SHARED_DATARAM, &sharedMem);

  sharedMem_int = (unsigned int*) sharedMem;
  sharedMem_sample = (int16_t*) sharedMem + ADC_BUF_OFFSET / sizeof(int16_t);

  //fprintf(stderr, "loading sample count to shared memory..\n");
  sharedMem_int[1] = nsamples;

  if (prussdrv_exec_program(PRU_NUM, PRU_BIN) < 0) {
    fprintf(stderr, "Error loading %s\n", PRU_BIN);
    exit(-1);
  }

//  fprintf(stderr, "loaded adc reader.. waiting for PRU to initialize buffer status\n");

//  fprintf(stderr, "%d %d: %d\n", target_buffer, ADC_BUF_STATUS_IDX, sharedMem_int[ADC_BUF_STATUS_IDX]);
  while(sharedMem_int[ADC_BUF_STATUS_IDX] != ADC_BUF_STATUS_EMPTY) {
    ;
  }

//  fprintf(stderr, "\nbuffer is ready\n");
  uint32_t remaining_samples = nsamples;

  while(remaining_samples > 0) {

    //fprintf(stderr, "%d %d: %d\n", target_buffer, ADC_BUF_STATUS_IDX, sharedMem_int[ADC_BUF_STATUS_IDX]);
    if(sharedMem_int[ADC_BUF_STATUS_IDX] == target_buffer) {
        for(i = 0; i < ADC_BUF_LEN_SAMPLES; i++) {
            uint32_t mem_idx = (ADC_BUF_LEN_SAMPLES * target_buffer + i) * 2;
            sample_buffer[sample_idx++] = sharedMem_sample[mem_idx];
            sample_buffer[sample_idx++] = sharedMem_sample[mem_idx+1];
            //fprintf(stderr, "%d, %d: %d + j%d\n", i, mem_idx, sharedMem_sample[mem_idx], sharedMem_sample[mem_idx+1]);
        }
        remaining_samples -= ADC_BUF_LEN_SAMPLES;
        target_buffer ^= 1;
        //printf("remaining samples: %d: new target: %d\n", remaining_samples, target_buffer);
    }
  }


  prussdrv_pru_wait_event(PRU_EVTOUT_0);
  printf("All done\n");

  prussdrv_pru_clear_event(PRU_EVTOUT_0, PRU0_ARM_INTERRUPT);
  prussdrv_pru_disable(PRU_NUM);
  prussdrv_exit();
   
}

int main(int argc, char **argv) {
  uint32_t i;
  uint32_t number_of_samples;
  int16_t sample_buffer[2 * MAX_SAMPLE_BUFFER]; 

  int32_t socket_desc , client_sock , c;
  struct sockaddr_in server , client;

  socket_desc = socket(AF_INET , SOCK_STREAM , 0);
  printf("created socket\n");
  i = 1;
  setsockopt(socket_desc, SOL_SOCKET, SO_REUSEADDR, &i, sizeof(i));
  server.sin_family = AF_INET;
  server.sin_addr.s_addr = INADDR_ANY;
  server.sin_port = htons(SAMPLE_PORT);

  if( bind(socket_desc, (struct sockaddr *)&server, sizeof(server)) < 0 ) {
    printf("bind failed\n");
    return 1;
  }

  printf("bind complete\n");

  listen(socket_desc, 3);
  while(1) {  
      //printf("waiting for incoming connections..");

      c = sizeof(struct sockaddr_in);
      client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c);

      if (client_sock < 0) {
        printf("socket accept failed!\n");
        return 1;
      }
      //printf("accepted connection!\n");

      recv(client_sock, &number_of_samples, sizeof(number_of_samples), MSG_WAITALL);
      
      grab_samples_pru(number_of_samples, sample_buffer);

      //for(i = 0; i < number_of_samples; i++) {
      //printf("[%d] %d +%dj\n", i, sample_buffer[2*i], sample_buffer[2*i+1]);
      //}
     
      i = ADC_BUF_LEN_SAMPLES;
      write(client_sock, &i, sizeof(i));
      for(i = 0; i < number_of_samples / ADC_BUF_LEN_SAMPLES; i++) {
        //printf("sending %d bytes..\n", ADC_BUF_LEN_SAMPLES * 2 * 2);
        write(client_sock, sample_buffer + i * 2 * ADC_BUF_LEN_SAMPLES, ADC_BUF_LEN_SAMPLES * 4);
      }

      recv(client_sock, &number_of_samples, sizeof(number_of_samples), MSG_WAITALL);
      close(client_sock);
  }
  close(client_sock);
  close(socket_desc);
  return 0;
}
