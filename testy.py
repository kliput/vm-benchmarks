#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright (c) Jakub Liput, Dominik Gawlik 2012
# Programy do badań nad wydajnością maszyn wirtualncych

import sys
import os
import os.path
import subprocess
import time
import glob
import re
import argparse

class Tests(object):
	def __init__(self):
		print 'program testowy rozpoczęty'
		self.null = open('/dev/null', 'w')
		self.tests = {
			'calloc':	self.t_calloc,
			'copy':		self.t_copy,
			'video':	self.t_video,
			'gcc':		self.t_gcc,
			'glmark':	self.t_glmark,
			'threads':	self.t_threads,
		}
		
	def t_calloc(self):
		print 'test alokacji pamięci'
		results = []
		
		block = 1024*1024*256 # 256MB
		blocks_count = 100000
		tests_count = 3
		
		for i in range(tests_count):
			out = subprocess.check_output(['./test_mem', 'calloc_many', str(block), str(blocks_count)])
			results.append(float(out))
		
		#print results
		
		# średnia z testów
		print '%.2f' % (reduce(lambda x, y: x + y, results) / len(results))

	def t_copy(self):
		print 'test kopiowania pliku'
		
		block_size = 1000*1000
		block_count = 512
		
		filename1 = 'zero.bin'
		filename2 = 'zero2.bin'
		
		subprocess.check_call(['dd', 'if=/dev/zero', 'of=%s' % filename1,
			'bs=%d' % block_size, 'count=%d' % block_count], stdout=self.null, stderr=self.null)
		
		start = time.time()
		subprocess.check_call(['cp', filename1, filename2], stdout=self.null, stderr=self.null)
		end = time.time()
		
		os.remove(filename1)
		os.remove(filename2)
		
		#print float(out)
		print '%.2f' % (end-start)

	def t_video(self):
		print 'test konwersji wideo'
		
		url = 'http://student.agh.edu.pl/~jliput/ps/projekt/pliki/input.flv'
		input_file = 'input.flv'
		output_file = 'output.mpg'
		
		try:
			subprocess.check_call(['which', 'ffmpeg'], stdout=self.null, stderr=self.null)
		except subprocess.CalledProcessError:
			print 'brak programu ffmpeg, próba instalacji za pomocą apt-get...'
			subprocess.check_call(['sudo', 'apt-get', '-qq', '-y', 'install', 'ffmpeg'])
		
		if not os.path.isfile(input_file):
			
			print 'brak wejściowego pliku wideo %s, próba pobrania...' % (input_file)
			subprocess.check_call(['wget', url], stdout=self.null, stderr=self.null)
			
			#raise Exception('brak wejściowego pliku wideo: %s', (input_file))
		
		start = time.time()
		subprocess.check_call(['ffmpeg', '-y', '-i', input_file, output_file], stdout=self.null, stderr=self.null)
		end = time.time()
		
		os.remove(output_file)
			
		print '%.2f' % (end-start)

	def t_gcc(self):
		print 'test niewielkiej kompilacji w GCC'
		
		name = 'rxvt-2.7.10'
		archive = '%s.tar.gz' % (name)
		
		url = 'http://pkgs.fedoraproject.org/repo/pkgs/rxvt/rxvt-2.7.10.tar.gz/302c5c455e64047b02d1ef19ff749141/rxvt-2.7.10.tar.gz'
		
		if not os.path.isfile(archive):
			print 'nie wykryto archiwum %s, nastąpi próba pobrania...' % (archive)
			subprocess.check_call(['wget', url], stdout=self.null, stderr=self.null)
		
		subprocess.check_call(['tar', '-zxvf', archive], stdout=self.null, stderr=self.null)
		
		orig_dir = os.getcwd()
		os.chdir(name)
		try:
			subprocess.check_call(['./configure'], stdout=self.null, stderr=self.null)
			
			start = time.time()
			subprocess.check_call(['make'], stdout=self.null, stderr=self.null)
			end = time.time()
			
		except Exception:
			os.chdir(orig_dir)
			raise
		
		os.chdir(orig_dir)
		
		subprocess.check_call(['rm', '-r', name], stdout=self.null, stderr=self.null);
		
		print '%.2f' % (end-start)
	
	def t_glmark(self):
		print 'test grafiki glmark2'
		
		try:
			subprocess.check_call(['which', 'glmark2'], stdout=self.null, stderr=self.null)
		except subprocess.CalledProcessError:
			print 'brak programu glmark2, próba instalacji za pomocą apt-get...'
			subprocess.check_call(['sudo', 'apt-get', '-qq', '-y', 'install', 'glmark2'])
		
		out = subprocess.check_output(['glmark2', '-b', 'build:use_vbo=true'], stderr=subprocess.STDOUT)
		
		print re.search(r'FPS: (\d+)', out).group(1)

	def t_threads(self):
		print 'test wielowątkowości'
		
		threads_num = 8;
		
		start = time.time()
		subprocess.check_call(['./test_threads', str(threads_num)], stdout=self.null, stderr=self.null)
		end = time.time()
		
		print '%.2f' % (end-start)
		
	
	def main(self, targets):
		try:
			subprocess.check_call(['make', 'all'], stdout=self.null, stderr=self.null)
		except OSError as e:
			print 'problem z budowaniem: %s' % (str(e))
			return 1
		
		if len(targets) == 0:
			targets = self.tests.keys()
		
		try:
			for t in targets:
				try:
					self.tests[t]()
				except (KeyError) as e:
					print 'brak testu: %s' % (t)
		except (Exception) as e:
			print 'problem z testem %s: %s' % (str(t), str(e))
			return 2
		
	
	def cleanup(self):
		self.null.close()
	
	def __del__(self):
		self.cleanup

if __name__ == '__main__':
	tests = Tests()
	
	if len(sys.argv) > 1:
		parser = argparse.ArgumentParser(description='Programy do przeprowadzania badań wydajności.')
		parser.add_argument('targets', metavar='test', type=str, nargs='+',
			help='testy do przeprowadzenia')

		e = tests.main(parser.parse_args().targets)
	else:
		e = tests.main([])
	
	tests.cleanup()
	print 'program testowy zakończony'
	exit(e)
	