CC=gcc
CFLAGS=-O2 -Wall -Wextra

all: test_mem

test_mem: test_mem.o test_lib.o test_lib.h
	$(CC) test_mem.o test_lib.o -o test_mem
	
test_mem.o: test_mem.c test_lib.h
	$(CC) -c test_mem.c -o test_mem.o
	
test_lib.o: test_lib.c test_lib.h
	$(CC) -c test_lib.c -o test_lib.o
