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

def EEPROM(dout, addr, clk, CONTENT=content, width=60):
	"""
        Module for EEPROM. Memory contains 2^32 addresses and
	each address contains 40 bits. The most significant 8 bits
	are the op code and the remaining 32 are two 16-bit chunks
	the represent the address of the operand in memory.

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

def pc_with_rom_testbench():
	"""
	Test bench for ROM that uses PC for addresses
	"""

	# initialize signals
	output, addr, load_addr = [Signal(0) for i in range(3)]
	dout = Signal(modbv(0)[32:])
	load, clk = [Signal(bool(0)) for i in range(2)]
	en = Signal(bool(1))

	# instantiate program counter and ROM
	pc_inst = PC(output, load_addr, en, load)
	mem_inst = EEPROM(dout, output, clk)

	# clock generator
	@always(delay(10))
	def clkgen():
		clk.next = not clk

	# enable signal generator
	@always(delay(20))
	def engen():
		en.next = not en

	# stimulus for DUT
	@always(clk.posedge)
	def stimulus():

		# check if output is 0x20
		# since 0x24 is last location
		# we will want to reset PC
		if output == 0x20:

			# bring load signal on PC high
			# which will reset PC by
			# loading in 0 (load_addr)
			load.next = bool(1)

		# otherwise
		else:
			# keep load low
			load.next = bool(0)

	# output monitor for debugging purposes
	@instance
        def output_monitor():
                print "t(ns) | PC  | Dout"
                print "-----------------------------------"
                while True:
                        yield en.posedge
			print "%s    | %s | %s" % (now(), hex(output), hex(dout))

	return instances()

def simulate(timesteps):
	"""
	Function for running simulation

	:param input timesteps: amount of steps for simulation
	"""

	# get a trace on the signals
	tb = traceSignals(pc_with_rom_testbench)

	# run simulation
	sim = Simulation(tb)
	sim.run(timesteps)

def main():
	# call simulation for 2000 steps
	simulate(2000)

if __name__ == '__main__':
	main()
		
