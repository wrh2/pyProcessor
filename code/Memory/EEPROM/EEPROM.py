"""
	Module for EEPROM that will be instruction memory for program

	Programmed by William Harrington
	ECE486 Final Project
"""
from PC import PC
from myhdl import *
from random import randrange
from gtv import *

def insert_program(fname='program.hex'):
	""" creates content for EEPROM """
	generate_hex(fname)
	with open(fname) as f:
		content = [x.strip('\n') for x in f.readlines()]
	content = [x.strip('L') for x in content]
	return content

content = insert_program()

def EEPROM(dout, addr, clk, CONTENT=content, width=32):
	"""
        Module for EEPROM. Address space of 2^16 and
	each address contains 32 bits. The most significant 8 bits
	are the op code and the remaining 24 are the address of
	operands A and B and where the result of the op goes.

	:param input addr: address of memory location
	:param output dout: data output for given address
	"""
	
	mem = [Signal(modbv(int(x, 16))[width:]) for x in CONTENT]

	# sensitive to positive edge of clock
    	@always(clk.posedge)
	def read():

		# output data at memory location
		dout.next = mem[int(addr)]

	return read
