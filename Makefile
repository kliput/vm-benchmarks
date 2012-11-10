CC=gcc
CFLAGS=-O2 -Wall -Wextra

all: test_mem test_threads

test_mem: test_mem.o test_lib.o test_lib.h
	$(CC) test_mem.o test_lib.o -o test_mem
	
test_threads: test_threads.o
	$(CC) test_threads.o -lpthread -o test_threads
	
test_mem.o: test_mem.c test_lib.h
	$(CC) -c test_mem.c -o test_mem.o

test_threads.o: test_threads.c
	$(CC) -c test_threads.c -o test_threads.o
	
test_lib.o: test_lib.c test_lib.h
	$(CC) -c test_lib.c -o test_lib.o
