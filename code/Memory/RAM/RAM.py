"""
	Module for main memory

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from random import randrange

def RAM(dout, din, we, addr, clk):

	mem = [Signal(modbv(0)[16:]) for x in range(16)]

	@always(clk.posedge)
	def write():
		if we:
			mem[int(addr)].next = din

	@always_comb
	def read():
		dout.next = mem[int(addr)]

	return write, read
