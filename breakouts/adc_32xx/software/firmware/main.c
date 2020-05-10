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
}

static void reboot(void)
{
//asm("call r0");
}

static void memory_test(void)
{
	// offset data in RAM from the start to avoid overwriting firmware..
	volatile unsigned int *dram_array = (unsigned int *)(HYPERRAM_BASE);

	int i;
	printf("memory test...\n");

	printf("writing memory to base %d!\n", &dram_array);

	for(i=0; i<HYPERRAM_SIZE/4; i++) {
		//#printf("writing memory, %d!\n", i);
		dram_array[i] = i*4;
	}

	printf("memory readback!\n");
	for(i=0; i<HYPERRAM_SIZE/4; i++) {
		//printf("reading memory, %d!\n", i);
		if(dram_array[i] == i*4) {
		}
		else {
			printf("pattern mismatch!\n");
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
