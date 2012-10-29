#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <limits.h>

#include "test_lib.h"

/*
 * Wyjście programu:
 *  - calloc: <czas_alokacji> <czas_zwalniania>
 */

void test_calloc_many(size_t block_size, unsigned long count) {
	unsigned long i;
	void* mem;
	
	for (i=0; i<count; ++i) {
		mem = calloc(sizeof(char), block_size);
		free(mem);
	}
	
}

/*
void test_free_many(int count, void* array[]) {
	int i;
	
	for (i=0; i<count; ++i) {
		free(array[i]);
	}
}
*/

void print_usage() {
	puts("Uzycie: ./test_mem <test> [argumenty]\ttesty:\n"
			"\tcalloc_many <rozmiar_bloku_(b)> <liczba_blokow>"
		);
	exit(1);
}

int main(int argc, char* argv[]) {
	if (argc < 1) {
		print_usage();
	}
	
	if (!strcmp(argv[1], "calloc_many")) {
		double c_time;
		//double f_time;
		
		if (argc < 3) {
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
		
		void** array = malloc(sizeof(void*)*count);
		
		EXEC_TIME(test_calloc_many(block_size, count), c_time);
		//EXEC_TIME(test_free_many(count, array), f_time);
		
		free(array);
		
// 		printf("%lf %lf\n", c_time, f_time);
		printf("%lf\n", c_time);
		
	} else {
		puts("nie ma takiego testu");
		print_usage();
	}
	
	return 0;
}
