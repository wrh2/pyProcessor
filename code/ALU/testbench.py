from myhdl import *
from random import randrange
from ALU import ALU


def ALU_testbench():
	""" Initialize signals """
	a, b = [Signal(modbv(randrange(2**16))[16:]) for i in range(2)]
	result = Signal(modbv(0)[16:])
	op = Signal(modbv(0)[8:])
	clk = Signal(bool(0))
	cycles = Signal(0)
        Z, E, P, N = [Signal(bool(0)) for i in range(4)]
	rdy = Signal(bool(1))

	""" ALU instance """
	ALU_inst = ALU(result, op, a, b,
		       Z, E, P, N, clk)

	""" clock generator """
	@always(delay(10))
	def clkgen():
		clk.next = not clk

	""" clock cycle count """
	@always(clk.negedge)
	def clkcount():
		cycles.next += 1

	@always(result)
	def nextOp():
		# advance to next op
		op.next += 1

	""" stimulus for simulation """
	@always(rdy)
	def stimulus():
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
	simulate(1000)

if __name__ == '__main__':
	main()

