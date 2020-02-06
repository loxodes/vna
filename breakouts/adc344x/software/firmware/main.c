#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <irq.h>
#include <uart.h>
#include <console.h>
#include <generated/csr.h>
#include <generated/mem.h>


// build started from from litex fpga101 lab 4
// also see https://github.com/enjoy-digital/versa_ecp5

static void busy_wait(unsigned int ds)
{
	timer0_en_write(0);
	timer0_reload_write(0);
	timer0_load_write(CONFIG_CLOCK_FREQUENCY/10*ds);
	timer0_en_write(1);
	timer0_update_value_write(1);
	while(timer0_value_read()) timer0_update_value_write(1);
}


static char *readstr(void)
{
	char c[2];
	static char s[64];
	static int ptr = 0;

	if(readchar_nonblock()) {
		c[0] = readchar();
		c[1] = 0;
		switch(c[0]) {
			case 0x7f:
			case 0x08:
				if(ptr > 0) {
					ptr--;
					putsnonl("\x08 \x08");
				}
				break;
			case 0x07:
				break;
			case '\r':
			case '\n':
				s[ptr] = 0x00;
				putsnonl("\n");
				ptr = 0;
				return s;
			default:
				if(ptr >= (sizeof(s) - 1))
					break;
				putsnonl(c);
				s[ptr] = c[0];
				ptr++;
				break;
		}
	}

	return NULL;
}

static char *get_token(char **str)
{
	char *c, *d;

	c = (char *)strchr(*str, ' ');
	if(c == NULL) {
		d = *str;
		*str = *str+strlen(*str);
		return d;
	}
	*c = 0;
	d = *str;
	*str = c+1;
	return d;
}

static void prompt(void)
{
	printf("RUNTIME>");
}

static void help(void)
{
	puts("Available commands:");
	puts("help                            - this command");
	puts("reboot                          - reboot CPU");
	puts("memory                          - memory test");
	puts("coremem                         - memory core test");
	puts("spi                             - spi test");
	puts("led                             - led test");
}

static void reboot(void)
{
//asm("call r0");
}

static void core_memory_test(void)
{
	static unsigned int test_offset_bytes = 1048576;
	volatile unsigned int *dram_array = (unsigned int *)(MAIN_RAM_BASE + test_offset_bytes);
	uint32_t i, j;

	// set _base
	memory_test_base_write(test_offset_bytes);
	printf("sizeof unsigned int: %d\n", sizeof(unsigned int));	
	for(i=0; i<500000; i++) {
		memory_test_offset_write(i);
		memory_test_value_write(i);
		if(i % 10000 == 0) {
			printf("writing memory[%d] = %u\n", i, i);
		}
		memory_test_start_write(1);
		while(!memory_test_ready_read()) {
			;
		}
	}

	printf("finished writing memory\n");
	for(j=0; j<1000000; j+= 20000) {
		for(i=0; i<20; i++) {
			printf("memory[%d] = %u\n", i + j, dram_array[i+j]);
		}
	}

	printf("finished reading memory\n");

	/*
	// set memory[address] = value
	printf("memory value is %u!\n", dram_array[0]);
	printf("writing 0 to memory\n");
	memory_test_addr_write(test_offset / 128);
	memory_test_start_write(1);
	busy_wait(1);
	printf("waiting..\n");
	printf("memory value is %u!\n", dram_array[0]);
	printf("writing 1 to memory\n");
	memory_test_addr_write(test_offset / 128);
	memory_test_start_write(1);
	busy_wait(1);
	printf("waiting..\n");
	printf("memory value is %u!\n", dram_array[0]);
	*/
}

static void memory_test(void)
{
	// offset data in RAM from the start to avoid overwriting firmware..
	volatile unsigned int *dram_array = (unsigned int *)(MAIN_RAM_BASE + 1024 * 1024 * 2);

	int i;
	printf("memory test...\n");

	printf("writing memory to base %d!\n", &dram_array);

	for(i=0; i<100; i++) {
		printf("writing memory, %d!\n", i);
		dram_array[i] = i*4;
	}

	printf("memory readback!\n");
	for(i=0; i<100; i++) {
		printf("reading memory, %d!\n", i);
		if(dram_array[i] == i*4) {
		}
		else {
			printf("pattern mismatch!\n");
		}

	}
	printf("test complete!\n");
}

static void spi_test(void)
{
	int i;
	unsigned int spi_control_start = (8 << CSR_SPI_TEST_CONTROL_LENGTH_OFFSET) | (1 << CSR_SPI_TEST_CONTROL_START_OFFSET);
	spi_test_cs_write(1);

	printf("spi_test...\n");

	// send byte
	for(i=0; i<32; i++) {
		spi_test_mosi_write(i);
		spi_test_control_write(spi_control_start);
	}
	printf("spi test complete!");
}


static void led_test(void)
{
	int i;
	printf("led_test...\n");
	for(i=0; i<32; i++) {
		gpio_leds_out_write(i);
		busy_wait(1);
	}
}

static void console_service(void)
{
	char *str;
	char *token;

	str = readstr();
	if(str == NULL) return;
	token = get_token(&str);
	if(strcmp(token, "help") == 0)
		help();
	else if(strcmp(token, "reboot") == 0)
		reboot();
	else if(strcmp(token, "memory") == 0)
		memory_test();
	else if(strcmp(token, "coremem") == 0)
		core_memory_test();
	else if(strcmp(token, "led") == 0)
		led_test();
	else if(strcmp(token, "spi") == 0)
		spi_test();
	prompt();
}

int main(void)
{
	irq_setmask(0);
	irq_setie(1);
	uart_init();

	puts("\nCPU testing software built "__DATE__" "__TIME__"\n");
	help();
	prompt();

	while(1) {
		console_service();
	}

	return 0;
}
