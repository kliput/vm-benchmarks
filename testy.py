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
	
	iperf_server = 'localhost'
	
	def __init__(self):
		print 'program testowy rozpoczęty'
		self.null = open('/dev/null', 'w')
		self.tests = {
			'mem':			self.t_mem,
			'copy':			self.t_copy,
			'video':		self.t_video,
			'gcc':			self.t_gcc,
			'glmark':		self.t_glmark,
			'threads':		self.t_threads,
			'iperf':		self.t_iperf,
			'jumboframes':  self.t_jumboframes,
			'grep':			self.t_grep,
			'dd_small':		self.t_dd_small,
			'dd_large':		self.t_dd_large,
		}
		self.groups = {
			'g_basic': (
				self.t_mem,
				self.t_copy,
				self.t_video,
				self.t_gcc,
				self.t_glmark,
				self.t_threads,
				self.t_iperf,
			),
			'g_disk': (
				self.t_copy,
				self.t_grep,
				self.t_dd_small,
				self.t_dd_large,
			),
			'g_net': (
				self.t_iperf,
				self.t_jumboframes,
			),
		}
		
	def apt_check_install(self, pkg_name):
		try:
			subprocess.check_call(['dpkg', '-s', pkg_name], stdout=self.null, stderr=self.null)
		except subprocess.CalledProcessError:
			print 'brak pakietu %s, próba instalacji za pomocą apt-get...' % pkg_name
			subprocess.check_call(['sudo', 'apt-get', '-qq', '-y', 'install', pkg_name])

	def iperf_mbytes_parse(self, output):
		return re.search(r'((\d+\.)?(\d+)) MBytes\/sec', output).group(1)
	
	def t_iperf(self):
		print 'test wydajności tcp (MB/s)'
		
		out = subprocess.check_output(['iperf','-fM','-p10000','-c',self.iperf_server], stderr=subprocess.STDOUT)
		
		print self.iperf_mbytes_parse(out)
		
	def t_jumboframes(self):
		print 'test dużych pakietów tcp (MB/s)'
		
		out = subprocess.check_output(['iperf','-M9000','-p10000','-fM','-c',self.iperf_server], stderr=subprocess.STDOUT)
		
		print self.iperf_mbytes_parse(out)

	
	def t_mem(self):
		print 'test operacji na pamięci (s)'
		results = []
		
		block = 1024*1024*512 # 512MB
		blocks_count = 1
		tests_count = 3
		
		for i in range(tests_count):
			out = subprocess.check_output(['./test_mem', 'malloc_many', str(block), str(blocks_count)])
			results.append(float(out))
		
		#print results
		
		# średnia z testów
		print '%.2f' % (reduce(lambda x, y: x + y, results) / len(results))

		
	disk_block_size = '512MB'
	disk_block_count = 1
	
	disk_filename1 = 'zero.bin'
	disk_filename2 = 'zero2.bin'
	
	def disk_zero_file_create(self):
		subprocess.check_call(['dd', 'if=/dev/zero', 'of=%s' % self.disk_filename1,
			'bs=%s' % self.disk_block_size, 'count=%d' % self.disk_block_count],
			stdout=self.null, stderr=self.null)
	
	def disk_zero_file_delete(self):
		os.remove(self.disk_filename1)
		os.remove(self.disk_filename2)
		
	def t_copy(self):
		print 'test kopiowania pliku (s)'
		
		self.disk_zero_file_create()
		
		start = time.time()
		subprocess.check_call(['cp', self.disk_filename1, self.disk_filename2],
			stdout=self.null, stderr=self.null)
		end = time.time()
		
		self.disk_zero_file_delete()
		
		print '%.2f' % (end-start)

	def dd_test_generic(self, bs):
		self.disk_zero_file_create()
		
		start = time.time()
		subprocess.check_call(['dd', 'if=%s' % self.disk_filename1, 'of=%s' % self.disk_filename2,
			'bs=%d' % bs],
			stdout=self.null, stderr=self.null)
		end = time.time()
		
		self.disk_zero_file_delete()
		
		return end-start
		
		
	def t_dd_small(self):
		print 'test kopiowania małymi blokami - dd (s)'
		print '%.2f' % self.dd_test_generic(256)
		
	def t_dd_large(self):
		print 'test kopiowania większymi blokami - dd (s)'
		print '%.2f' % self.dd_test_generic(4096)
	
		
	def t_video(self):
		print 'test konwersji wideo (s)'
		
		url = 'http://student.agh.edu.pl/~jliput/ps/projekt/pliki/input.flv'
		input_file = 'input.flv'
		output_file = 'output.mpg'
		
		self.apt_check_install('ffmpeg')
		
		if not os.path.isfile(input_file):
			print 'brak wejściowego pliku wideo %s, próba pobrania...' % (input_file)
			subprocess.check_call(['wget', url], stdout=self.null, stderr=self.null)
			
		start = time.time()
		subprocess.check_call(['ffmpeg', '-y', '-i', input_file, output_file], stdout=self.null, stderr=self.null)
		end = time.time()
		
		os.remove(output_file)
			
		print '%.2f' % (end-start)

	def t_gcc(self):
		print 'test niewielkiej kompilacji w GCC (s)'
		
		name = 'rxvt-2.7.10'
		archive = '%s.tar.gz' % (name)
		
		url = 'http://pkgs.fedoraproject.org/repo/pkgs/rxvt/rxvt-2.7.10.tar.gz/302c5c455e64047b02d1ef19ff749141/rxvt-2.7.10.tar.gz'
		
		self.apt_check_install('libxt-dev')
		
		if not os.path.isfile(archive):
			print 'nie wykryto archiwum %s, nastąpi próba pobrania...' % (archive)
			subprocess.check_call(['wget', url], stdout=self.null, stderr=self.null)
		
		subprocess.check_call(['tar', '-zxvf', archive], stdout=self.null, stderr=self.null)
		
		orig_dir = os.getcwd()
		os.chdir(name)
		try:
			subprocess.check_call(['./configure'], stdout=self.null, stderr=self.null)
			
			start = time.time()
			out = subprocess.check_output(['make'], stderr=subprocess.STDOUT)
			end = time.time()
			
			if re.search(r'fatal error', out) == None:
				raise Exception('błąd make:\n%s' % (out))
			
		except Exception:
			os.chdir(orig_dir)
			raise
		
		os.chdir(orig_dir)
		
		subprocess.check_call(['rm', '-r', name], stdout=self.null, stderr=self.null);
		
		print '%.2f' % (end-start)
	
	def t_glmark(self):
		print 'test grafiki glmark2 (FPS)'
		
		self.apt_check_install('glmark2')
		
		out = subprocess.check_output(['glmark2', '-b', 'build:use_vbo=true'], stderr=subprocess.STDOUT)
		
		print re.search(r'FPS: (\d+)', out).group(1)

	def t_threads(self):
		print 'test wielowątkowości (s)'
		
		threads_num = 8;
		
		start = time.time()
		subprocess.check_call(['./test_threads', str(threads_num)], stdout=self.null, stderr=self.null)
		end = time.time()
		
		print '%.2f' % (end-start)
		
	def t_grep(self):
		print 'test wyszukiwania w pliku - grep (s)'
		
		file_name = 'plik.txt'
		words = 'lorem ipsum sit dolor amet'
		count = 8000000
		
		f = open(file_name, 'w+')
		f.write('\n'.join([words]*count))
		f.close()
		
		start = time.time()
		out = subprocess.check_output(['grep', '-c', words, file_name], stderr=subprocess.STDOUT)
		end = time.time()
		
		try:
			if int(out) != count:
				os.remove(file_name)
				raise Exception('znaleziono nieprawidłową liczba wyrazów: %s zamiast %i' % (out, count))
		except ValueError:
			os.remove(file_name)
			raise Exception('nieprawidłowe wyjście: %s' % (out))
		
		print '%.2f' % (end-start)
		
		os.remove(file_name)
	
	
	def main(self, targets):
		try:
			subprocess.check_call(['make', 'all'], stdout=self.null, stderr=self.null)
		except OSError as e:
			print 'problem z budowaniem: %s' % (str(e))
			return 1
		
		if len(targets) == 0:
			targets = self.tests.keys()
		
		
		for t in targets:
			try:
				if t.startswith('g_'):
					map(lambda t: t(), self.groups[t])
				else:
					self.tests[t]()
			except (KeyError) as e:
				print 'brak testu: %s' % (t)
			except (Exception) as e:
				print 'problem z testem %s: %s' % (str(t), str(e))
				#return 2
		
	
	def cleanup(self):
		self.null.close()
	
	def __del__(self):
		self.cleanup

if __name__ == '__main__':
	tests = Tests()
	
	parser = argparse.ArgumentParser(description='Programy do przeprowadzania badań wydajności.')
	parser.add_argument("--targets", help="testy do przeprowadzenia oddzielone przecinkami (bez spacji!)")
	
	parser.add_argument("--ip", help="ip serwera iperf do testów [domyślnie localhost]")
	
	p_args = parser.parse_args()
	
	targets = []
	if p_args.targets:
		targets = p_args.targets.split(',')
	
	if not p_args.ip:
		p_args.ip = 'localhost'
		
	tests.iperf_server = p_args.ip
	
	e = tests.main(targets)
	
	tests.cleanup()
	print 'program testowy zakończony'
	exit(e)
	
