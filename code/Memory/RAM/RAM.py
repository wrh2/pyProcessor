"""
	Module for main memory

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from random import randrange

def RAM(dout0, dout1, dout2, din, we, addr0, addr1, addr2, clk):

	mem = [Signal(modbv(0)[16:]) for x in range(2**8)]

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
