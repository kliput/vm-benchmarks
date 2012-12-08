#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <limits.h>
#include <memory.h>

#include "test_lib.h"

/*
 * Wyjście programu:
 *  - malloc_many: <czas_funkcji(sek>
 */

void test_calloc_many(size_t block_size, unsigned long count) {
	unsigned long i, j;
	char* mem;
	
	for (i=0; i<count; ++i) {
		mem = malloc(sizeof(char)*block_size);
		memset(mem, 0, block_size);
		free(mem);
	}
	
}

void print_usage() {
	puts("Uzycie: ./test_mem <test> [argumenty]\ttesty:\n"
			"\tcalloc_many <rozmiar_bloku_(b)> <liczba_blokow>"
		);
	exit(1);
}

int main(int argc, char* argv[]) {
	if (argc < 2) {
		print_usage();
	}
	
	if (!strcmp(argv[1], "malloc_many")) {
		double c_time;
		
		if (argc < 4) {
			puts("zbyt malo argumentow");
			print_usage();
		}
		
		unsigned long block_size = strtoul(argv[2], NULL, 0);
		unsigned long count = strtoul(argv[3], NULL, 0);
		
		if (block_size>SIZE_MAX || block_size<0) {
			puts("nieprawidlowy rozmiar blokow");
			print_usage();
		}
		
		if (count>ULONG_MAX || count<0) {
			puts("nieprawidlowa liczba blokow");
			print_usage();
		}
		
		EXEC_TIME(test_calloc_many(block_size, count), c_time);
		
		printf("%lf\n", c_time);

	} else {
		puts("nie ma takiego testu");
		print_usage();
	}
	
	return 0;
}
