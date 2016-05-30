"""
	Module for main memory

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from random import randrange
from gtv import *

def initialize_memory(fname='memory_image.hex'):
	generate_memory_image()
	with open(fname) as f:
		content = [modbv(int(x, 16))[32:] for x in f.readlines()]
	f.close()
	msb = [y[32:16] for y in content]
	lsb = [y[16:] for y in content]
	content = []
	for x,y in zip(msb,lsb):
		content.append(x)
		content.append(y)
	return content

memory_image = initialize_memory()

def RAM(dout0, dout1, dout2, din, we, addr0, addr1, addr2, clk, IMAGE=memory_image):

	mem = [Signal(x) for x in CONTENT]
	[mem.append(Signal(modbv(0)[16:])) for i in range((2**16)-len(mem))]

	@always(clk.posedge)
	def write():
		if we:
			mem[int(addr0)].next = din

	@always_comb
	def read():
		dout0.next = mem[int(addr0)]
		dout1.next = mem[int(addr1)]
		dout2.next = mem[int(addr2)]

	return write, read
