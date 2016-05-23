"""
	Implementation of Arithmetic Logic Unit module

	The ALU internally has a ripple carry adder/subtractor
	but this isn't actually modelled below. Instead, an
	equivalent propagation delay is implemented before
	the output changes based on the given operation.

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from random import randrange

def ALU(result, op, a, b, Z, E, P, N, rdy, clk, width=16):
	"""
	Module for Arithmetic Logic Unit

	:param input op: op code
	:param input a: operand A
	:param input b: operand B
	:param output result: result of operation
        """
	cycles = 0
	prop = Signal(modbv(0)[width:])

	@always_comb
	def ALU_logic():
		""" Logic for ALU """
		if op == 0x4:
			prop.next = modbv(a+b)[width:]
		if op == 0x5:
			prop.next = modbv(a-b)[width:]
		if op == 0x6:
			prop.next = modbv(a*b)[width:]
		if op == 0x7:
			prop.next = modbv(a%b)[width:]
		if op == 0x20:
			prop.next = modbv(a|b)[width:]
		if op == 0x28:
			prop.next = modbv(a&b)[width:]
		if op == 0x30:
			prop.next = modbv(a^b)[width:]

	@always_comb
	def checkConditions():
		if a == b:
			E.next = bool(1)
		else:
			E.next = bool(0)

		if result.next == 0:
			Z.next = bool(1)
		else:
			Z.next = bool(0)

		if result.next > 0:
			P.next = bool(1)
		else:
			P.next = bool(0)

		if result.next < 0:
			N.next = bool(1)
		else:
			N.next = bool(0)

	def checkRdy():
		if rdy:
			rdy.next = bool(0)
		else:
			rdy.next = bool(1)

	@instance
	def ready():
		while True:
			yield prop
			checkRdy()
			# mult op
			if op == 0x6:
				cycles = 116 
			# add/sub/mod op
			elif op == 0x4 or op == 0x5 or op == 0x7:
				cycles = 8
			else:
				cycles = 1
			for i in range(cycles):
				yield clk.negedge
                	checkRdy()

	@instance
        def prop_delay():
		"""
                This function models the prop delay for the ALU.
		
		The ALU is essentially just a combination of
		combinational circuits that perform the operation.
		For instance, the add and subtract operations
		are performed with an adder-subtractor circuit
		that has a set propagation delay (Tpd) for each stage.
		This model is for a ripple-carry adder/subtractor.
		This means the total prop delay for an add/subtract operation
		is Tpd * number of bits.

		The worst case operation is multiplication.
		For multiplication, the delay is Tpd * (number of bits)^2

		Clock speed = 50MHz,
		Clock period = 20ns,
                Tpd = 9ns,
		number of bits = 16

		for mult, delay = ceiling((16*16*9)/20) = 116
		for add/sub, delay = ceiling(16*9) = 8
		"""
		while True:
			yield prop
			# mult op
			if op == 0x6:
				cycles = 116 
			# add/sub/mod op
			elif op == 0x4 or op == 0x5 or op == 0x7:
				cycles = 8
			else:
				cycles = 1

			for i in range(cycles):
				yield clk.negedge
			result.next = prop

	return instances()

def ALU_testbench():
	""" Initialize signals """
	a, b = [Signal(modbv(randrange(2**16))[16:]) for i in range(2)]
	result = Signal(modbv(0)[16:])
	op = Signal(modbv(0x4)[8:])
	clk = Signal(bool(0))
	cycles = Signal(0)
        Z, E, P, N = [Signal(bool(0)) for i in range(4)]
	rdy = Signal(bool(0), delay=2)

	""" ALU instance """
	ALU_inst = ALU(result, op, a, b,
		       Z, E, P, N, rdy, clk)

	""" clock generator """
	@always(delay(10))
	def clkgen():
		clk.next = not clk

	""" clock cycle count """
	@always(clk.negedge)
	def clkcount():
		cycles.next += 1

	""" stimulus for simulation """
	@always(result)
	def stimulus():
		# advance to next op
		op.next += 1

		# generate random operands
		a.next = modbv(randrange(2**16))[16:]
                b.next = modbv(randrange(2**16))[16:]

	""" output monitor for debugging purposes """
	@instance
	def output_monitor():
		print 'cycles op a b result'
		print '-------------------'
		while True:
			yield result
			print '%s %x %x %x %x' % (cycles, op, a, b, result)

	return instances()

def simulate(timesteps):
	"""
	Function for running simulation

	:param input timesteps: amount of steps for simulation
	"""

	# get a trace on the signals
	tb = traceSignals(ALU_testbench)

	# run simulation
	sim = Simulation(tb)
	sim.run(timesteps)

def main():
	simulate(5000)

if __name__ == '__main__':
	main()
