"""
	Simple 4 way AND module

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from random import randrange

def logic_AND(a0, b0, a1, b1, a2, b2, a3, b3, r0, r1, r2, r3):
	"""
	Module for comparator

	:param input a: 4 bit wide input to compare with b
	:param input b: 4 bit wide input to compare with a
	"""

	@always_comb
	def compare_logic():
		"""
		Simple comparison of each pair of inputs (ai, bi)
		where i is an element of range(4) (i.e. 0,1..,3)
		"""
		r0.next = a0 & b0
		r1.next = a1 & b1
		r2.next = a2 & b2
		r3.next = a3 & b3

	return instances()

def AND_testbench():
	""" Initialize signals """
	a0, a1, a2, a3, b0, b1, b2, b3 = [Signal(bool(0)) for i in range(8)]
	r0, r1, r2, r3 = [Signal(bool(0)) for i in range(4)]
	clk = Signal(bool(0))
	cycles = Signal(0)

	""" comparator instance """
	AND_inst = logic_AND(a0, b0, a1, b1, a2, b2, a3, b3, r0, r1, r2, r3)

	""" clock generator """
	@always(delay(10))
	def clkgen():
		clk.next = not clk

	""" clock cycle count """
	@always(clk.negedge)
	def clkcount():
		cycles.next += 1

	""" stimulus for simulation """
	@always(clk.posedge)
	def stimulus():
		# generate random values to compare
		a0.next, a1.next, a2.next, a3.next = [bool(randrange(2)) for i in range(4)]
		b0.next, b1.next, b2.next, b3.next = [bool(randrange(2)) for i in range(4)]

	""" output monitor for debugging purposes """
	@instance
	def output_monitor():
		# only examining first pair of signals
		print 'cycles a0 b0 r0'
		print '---------------'
		while True:
			yield clk.negedge
			print '%s %d %d %d' % (cycles, a0, b0, r0)

	return instances()

def simulate(timesteps):
	tb = traceSignals(AND_testbench)
	sim = Simulation(tb)
	sim.run(timesteps)

def main():
	simulate(200)

if __name__ == '__main__':
	main()
