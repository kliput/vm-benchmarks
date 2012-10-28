#include <stdlib.h>
#include <stdio.h>

#include "test_lib.h"

/*
 * Wyjście programu:
 *  - calloc: <czas_alokacji> <czas_zwalniania>
 */

void test_calloc_many(int block_size, int count, void* array[]) {
	int i;
	
	for (i=0; i<count; ++i) {
		array[i] = calloc(sizeof(char), (size_t)block_size);
	}
	
}

void test_free_many(int count, void* array[]) {
	int i;
	
	for (i=0; i<count; ++i) {
		free(array[i]);
	}
}

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
		double f_time;
		
		if (argc < 3) {
			puts("malo arg");
			print_usage();
		}
		
		int block_size = atoi(argv[2]);
		int count = atoi(argv[3]);
		
		void** array = malloc(sizeof(void*)*count);
		
		EXEC_TIME(test_calloc_many(block_size, count, array), c_time);
		EXEC_TIME(test_free_many(count, array), f_time);
		
		free(array);
		
		printf("%lf %lf\n", c_time, f_time);
		
	} else {
		puts("nie ma takiego testu");
		print_usage();
	}
	
	return 0;
}
