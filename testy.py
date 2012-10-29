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
	blocks_count = 100000#0
	tests_count = 10
	
	
	for i in range(tests_count):
		p = subprocess.Popen(['./test_mem', 'calloc_many', str(block), str(blocks_count)], 
			stdout=subprocess.PIPE)
		out, err = p.communicate()
		results.append(float(out))
	
	#print results
	
	print reduce(lambda x, y: x + y, results) / len(results)
	
	return err
	
def main():
	if os.system('make all') != 0:
		print 'problem z budowaniem'
		exit(1)
	
	targets = [t_calloc_many]
	
	for t in targets:
		t()
		# TODO
		#if t() != 0:
			#print 'problem z testem:', t
			#break
	
	
	pass

if __name__ == '__main__':
	main()
	