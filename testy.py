#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright (c) Jakub Liput, Dominik Gawlik 2012
# Programy do badań nad wydajnością maszyn wirtualncych

import os
import subprocess

def t_calloc_many():
	print 'test alokacji pamieci'
	results = []
	
	block = 1024*1024*256 # 256MB
	blocks_count = 100000
	tests_count = 3
	
	
	for i in range(tests_count):
		out = subprocess.check_output(['./test_mem', 'calloc_many', str(block), str(blocks_count)])
		results.append(float(out))
	
	#print results
	
	print reduce(lambda x, y: x + y, results) / len(results)

def t_copy():
	print 'test kopiowania pliku'
	
	block_size = 1000*1000
	block_count = 512
	
	filename1 = 'zero.bin'
	filename2 = 'zero2.bin'
	
	subprocess.check_call(['dd', 'if=/dev/zero', 'of=%s' % filename1,
		'bs=%d' % block_size, 'count=%d' % block_count], stderr=subprocess.STDOUT)
	
	#out = subprocess.check_output(['echo', 'Jozek'])
	
	out = subprocess.check_output(['/usr/bin/time', '-f', '%e',
		'cp', filename1, filename2], stderr=subprocess.STDOUT)
	
	os.remove(filename1)
	os.remove(filename2)
	
	print float(out)

	

def main():
	try:
		subprocess.check_call(['make', 'all'])
	except OSError as e:
		print 'problem z budowaniem: %s' % (str(e))
		exit(1)
	
	# TODO mapa i do argumentów
	targets = [t_calloc_many, t_copy]
	#targets = [t_copy]
	
	try:
		for t in targets:
			t()
	except OSError as e:
		print 'problem z testem %s: %s' % (str(t), str(e))
		exit(2)
		
	pass

if __name__ == '__main__':
	main()
	