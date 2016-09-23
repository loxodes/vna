// Loads a PRU text.bin (and optionally data.bin) file,
// executes it, and waits for completion.
//
// Usage:
// $ ./loader text.bin [data.bin]
//
// Compile with:
// gcc -o loader loader.c -lprussdrv
//
// Based on https://credentiality2.blogspot.com/2015/09/beaglebone-pru-gpio-example.html
// Based on http://www.righto.com/2016/08/pru-tips-understanding-beaglebones.html

#include <stdio.h>
#include <stdlib.h>
#include <prussdrv.h>
#include <pruss_intc_mapping.h>

#include <sys/mman.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <time.h>

#define PRU_NUM      0
#define PRUSS0_SHARED_DATARAM    4


static void *sharedMem;
static unsigned int *sharedMem_int;

int main(int argc, char **argv) {
  if (argc != 2 && argc != 3) {
    printf("Usage: %s loader text.bin [data.bin]\n", argv[0]);
    return 1;
  }

  prussdrv_init();
  if (prussdrv_open(PRU_EVTOUT_0) == -1) {
    printf("prussdrv_open() failed\n");
    return 1;
  }


  tpruss_intc_initdata pruss_intc_initdata = PRUSS_INTC_INITDATA;
  prussdrv_pruintc_init(&pruss_intc_initdata);

  printf("Executing program and waiting for termination\n");
  if (argc == 3) {
    if (prussdrv_load_datafile(0 /* PRU0 */, argv[2]) < 0) {
      fprintf(stderr, "Error loading %s\n", argv[2]);
      exit(-1);
    }
  }
  if (prussdrv_exec_program(0 /* PRU0 */, argv[1]) < 0) {
    fprintf(stderr, "Error loading %s\n", argv[1]);
    exit(-1);
  }

  // Wait for the PRU to let us know it's done
  prussdrv_pru_wait_event(PRU_EVTOUT_0);
  printf("All done\n");

prussdrv_map_prumem(PRUSS0_SHARED_DATARAM, &sharedMem);
  sharedMem_int = (unsigned int*) sharedMem;
  
  printf("0: %d\n", sharedMem_int[0]);
  printf("1: %d\n", sharedMem_int[1]);
  printf("2: %d\n", sharedMem_int[2]);
  printf("3: %d\n", sharedMem_int[3]);
  printf("4: %d\n", sharedMem_int[4]);
  printf("5: %d\n", sharedMem_int[4]);
  printf("6: %d\n", sharedMem_int[4]);

  prussdrv_pru_disable(0 /* PRU0 */);
  prussdrv_exit();


  return 0;
}
