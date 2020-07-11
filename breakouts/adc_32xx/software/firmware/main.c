#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <irq.h>
#include <uart.h>
#include <console.h>
#include <generated/csr.h>
#include <generated/mem.h>


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
	puts("wishbone                        - wishbone dma test");
	puts("adc                        	  - adc test");
}

static void reboot(void)
{
  	ctrl_reset_write(1);
}

static uint32_t adc_spi_read(uint16_t addr)
{
	while(adc_spi_status_read() != 1 << CSR_ADC_SPI_STATUS_DONE_OFFSET) {
		;
	}

	uint32_t spi_control_start = (24 << CSR_ADC_SPI_CONTROL_LENGTH_OFFSET) | (1 << CSR_ADC_SPI_CONTROL_START_OFFSET);
	adc_spi_cs_write(0);
	adc_spi_mosi_write((addr << 8) + (1 << 23) + (1 << 22));
	adc_spi_control_write(spi_control_start);

	adc_spi_cs_write(1);
	while(adc_spi_status_read() != 1 << CSR_ADC_SPI_STATUS_DONE_OFFSET) {
		;
	}

	uint32_t r = adc_spi_miso_read();
	return r & 0xFF;

}


static void adc_spi_write(uint16_t addr, uint8_t value)
{
	while(adc_spi_status_read() != 1 << CSR_ADC_SPI_STATUS_DONE_OFFSET) {
		;
	}

	uint32_t spi_control_start = (24 << CSR_ADC_SPI_CONTROL_LENGTH_OFFSET) | (1 << CSR_ADC_SPI_CONTROL_START_OFFSET);
	adc_spi_cs_write(0);

	uint32_t payload = (1 << 22) + (addr << 8) + value;

	adc_spi_mosi_write(payload);
	adc_spi_control_write(spi_control_start);

	adc_spi_cs_write(1);

	uint8_t r = adc_spi_read(addr);

	if(r != value) {
		printf("adc readback after write to %x failed!, expected %x got %x\n", addr, value, r);
	}
}

static void adc_init(void)
{
	// setup for 2-Wire (6x serialization)
	// Fs = 25 MSPS, Fbit = 150 MHz
	
	// soft reset
	adc_spi_write(0x06, 0x01);
	adc_spi_write(0x06, 0x00);
	// high pulse on reset, minimum duration 10 nanoseconds
	// max SPI SCLK 20 MHz
	// 0x01, default ok, dithering on both channels
	// 0x03, default ok, bits 0,1,2 on wire 0, bits 7,8,9 on wire 1
	// 0x04, default ok, do not flip output wires
	// 0x05, default ok, transmit on two output wires
	// 0x06, default ok, normal output (not a test pattern)
	// 0x07, default ok, bit 0 is lsb
	adc_spi_write(0x09, 0x01); // 0x09, set data format as offset binary
	// 0x0a, default ok, normal operation (not a test pattern)
	// 0x0b, default ok, normal operation (not a test pattern)
	// 0x0e, default ok
	// 0x0f, default ok
	// 0x13, default ok, >25 MSPS
	// 0x15, default ok, enable both channels and normal operation
	// 0x25, default ok, max LVDS swing
	// 0x27, default ok, no sample clock division
	// 0x41D, default ok, <100 MHz operation
	// 0x422, default ok, chopper enabled on ch a
	// 0x434, default ok, dithering on cha
	adc_spi_write(0x439, 0x08);
	// 0x439, write 0b1000 after reset for best performance on ch a
	// 0x51D, default ok, <100 MHz operation
	// 0x522, default ok, chopper enabled on ch b
	// 0x534, default ok, dithering on channel a
	adc_spi_write(0x539, 0x08);
	// 0x539, write 0b1000 after reset for best performance on ch b
	// 0x608, default ok, <100 MHz operation

	adc_spi_write(0x70A, 0x01);
	// 0x70A, 0b1, disable sysref buffer
}


static void adc_testpattern_en(void)
{
	adc_spi_write(0x06, 0x02);
	adc_spi_write(0x0a, 0x04);
	adc_spi_write(0x0b, 0x09<<4);


	// custom pattern:
	adc_spi_write(0x0e, 0x16);
	adc_spi_write(0x0f, 0x50); // 0x05

	// 0a
	// 0 - normal
	// 1 - all 0
	// 2 - all 1
	// 3 - alternate 010101 101010 
	// 4 - ramp, datasheet is incorrect, value increments every 4 samples (https://e2e.ti.com/support/data-converters/f/73/t/469423)
	// 5 - custom pattern
	// 9 - 8 point sine wave, [0, 599,2048,3496,4095,3496,2048,599]
	// 10 - Deskew pattern, data are AAAh
}

static void adc_testpattern_disable(void)
{
	adc_spi_write(0x06, 0x00);
	adc_spi_write(0x0a, 0x00);
	adc_spi_write(0x0b, 0x00);
}

static void adc_test(void)
{
	// capture a burst, 20 MSPS, a
	// provide a 20 MHz sample clock
	// read in data at .. 120 MHz
	//
	volatile unsigned int *dram_array = (unsigned int *)(ADC_SRAM_BASE);
	adc_init();
	adc_testpattern_en();

	adc_burst_size_write(1024);
	adc_base_write(ADC_SRAM_BASE);
	adc_offset_write(0);

	adc_start_write(1 << CSR_ADC_START_START_BURST_OFFSET);

	printf("waiting for ready!\n");
    while(!adc_ready_read())
    {
    	;
    }

	printf("memory readback!\n");
	for(uint16_t i=0; i<1024; i++) {
		printf("memory[%d]: %d\n", i, dram_array[i]);
	}

}

static void wishbone_test(void)
{
	printf("wishbone burst test...\n");
	volatile unsigned int *dram_array = (unsigned int *)(HYPERRAM_BASE);

	adc_burst_size_write(20);
	adc_base_write(HYPERRAM_BASE);
	adc_offset_write(0);

    adc_start_write(1 << CSR_ADC_START_START_BURST_OFFSET);

	printf("waiting for ready!\n");
    while(!adc_ready_read())
    {
    	;
    }

	printf("memory readback!\n");
	for(uint16_t i=0; i<30; i++) {
		printf("memory[%d]: %d\n", i, dram_array[i]);
	}
}

static void memory_test(void)
{
	// offset data in RAM from the start to avoid overwriting firmware..
	volatile uint32_t *dram_array = (unsigned int *)(HYPERRAM_BASE);

	int i;
	printf("memory test...\n");

	printf("writing memory to base %x!\n", dram_array);
	printf("HYPERRAM_BASE is %x!\n", HYPERRAM_BASE);
	for(i=0; i<500000; i++) {
		//#printf("writing memory, %d!\n", i);
		dram_array[i] = 0;
	}

	printf("memory readback!\n");
	for(i=0; i<500000; i++) {
		// 	printf("reading memory[%d] = %d\n", i, dram_array[i]);
		if(dram_array[i] == 0) {
			;
		}
		else {
			printf("pattern mismatch!, read %d expected %d\n", dram_array[i], i*4);
		}

	}
	printf("test complete!\n");
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
	else if(strcmp(token, "wishbone") == 0)
		wishbone_test();
	else if(strcmp(token, "adc") == 0)
		adc_test();
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
