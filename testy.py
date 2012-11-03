#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright (c) Jakub Liput, Dominik Gawlik 2012
# Programy do badań nad wydajnością maszyn wirtualncych

import os
import subprocess
import time

null = open('/dev/null', 'w')

def t_calloc_many():
	global null
	
	print 'test alokacji pamieci'
	results = []
	
	block = 1024*1024*256 # 256MB
	blocks_count = 100000
	tests_count = 3
	
	
	for i in range(tests_count):
		out = subprocess.check_output(['./test_mem', 'calloc_many', str(block), str(blocks_count)])
		results.append(float(out))
	
	#print results
	
	print '%.2f' % (reduce(lambda x, y: x + y, results) / len(results))

def t_copy():
	global null
	
	print 'test kopiowania pliku'
	
	block_size = 1000*1000
	block_count = 512
	
	filename1 = 'zero.bin'
	filename2 = 'zero2.bin'
	
	subprocess.check_call(['dd', 'if=/dev/zero', 'of=%s' % filename1,
		'bs=%d' % block_size, 'count=%d' % block_count], stdout=null, stderr=null)
	
	#out = subprocess.check_output(['/usr/bin/time', '-f', '%e',
		#'cp', filename1, filename2], stderr=subprocess.STDOUT)

	start = time.time()
	subprocess.check_call(['cp', filename1, filename2], stdout=null, stderr=null)
	end = time.time()
	
	os.remove(filename1)
	os.remove(filename2)
	
	#print float(out)
	print '%.2f' % (end-start)

def t_video():
	global null
	
	print 'test konwersji wideo'
	
	#null = open("NUL","w")
	
	input_file = 'input.flv'
	output_file = 'output.mpg'
	
	start = time.time()
	subprocess.check_call(['ffmpeg', '-y', '-i', input_file, output_file], stdout=null, stderr=null)
	end = time.time()
	
	#null.close()
	
	os.remove(output_file)
		
	print '%.2f' % (end-start)

def main():
	try:
		subprocess.check_call(['make', 'all'])
	except OSError as e:
		print 'problem z budowaniem: %s' % (str(e))
		return 1
	
	# TODO mapa i do argumentów
	targets = [t_calloc_many, t_copy, t_video]
	#targets = [t_video]
	
	try:
		for t in targets:
			t()
	except OSError as e:
		print 'problem z testem %s: %s' % (str(t), str(e))
		return 2
		
	pass

if __name__ == '__main__':
	e = main()
	null.close()
	exit(e)
	