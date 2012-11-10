#include <stdlib.h>
#include <stdio.h>
#include <limits.h>

#include <pthread.h>

int thread_num = 0;
pthread_t* threads;
pthread_attr_t default_attr;

void print_usage() {
	puts("Użycie: ./test_threads <liczba_watkow>");
	exit(1);
}

void* foo(void* args) {
	int i;
	unsigned long j;
	
	for (i=0; i<INT_MAX; ++i) {
		j += i;
	}
	
	return 0;
}

int main(int argc, char* argv[]) {
	int i;
	
	if (argc < 2) {
		print_usage();
	}
	
	thread_num = atoi(argv[1]);
	
	pthread_attr_init(&default_attr);
	
	threads = malloc(sizeof(pthread_t)*thread_num);
	
	for (i=0; i<thread_num; ++i) {
		pthread_create(&threads[i], &default_attr, foo, 0);
	}

	for (i=0; i<thread_num; ++i) {
		pthread_join(threads[i], 0);
	}
	
	free(threads);
}


