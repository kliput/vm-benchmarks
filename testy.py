#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright (c) Jakub Liput, Dominik Gawlik 2012
# Programy do badań nad wydajnością maszyn wirtualncych

import os
import subprocess

def t_calloc_many():
	print 'test alokacji pamieci'
	block = 1024*1024*256 # 256MB
	count = 1000000
	return subprocess.call(['./test_mem', 'calloc_many', str(block), str(count)])
	
def main():
	if os.system('make all') != 0:
		print 'problem z budowaniem'
		exit(1)
	
	targets = [t_calloc_many]
	
	for t in targets:
		if t() != 0:
			print 'problem z testem:', t
			break
	
	
	pass

if __name__ == '__main__':
	main()
	