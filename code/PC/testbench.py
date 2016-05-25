"""
	Program Counter

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from random import randrange
from PC import PC

def pc_testbench():
        """
	Test bench for the program counter
	"""

	# initialize signals
	output = Signal(modbv(0)[32:])
	addr = Signal(modbv(0)[32:])
	load, en, clk = [Signal(bool(0)) for i in range(3)]
	count = Signal(modbv(0)[32:])

	# instantiate program counter
	pc_inst = PC(output, addr, en, load)

	# clock generator
	@always(delay(10))
	def clkgen():
		clk.next = not clk

	# count clock cycles
	@always(clk.negedge)
	def update():
		count.next += 1

	# enable signal generator
	@always(delay(20))
	def engen():
		en.next = not en

	# stimulus for DUT
	@always(en.posedge)
	def stimulus():

		# test jump functionality
		if ((count > 5) and (randrange(2))):

			# bring load signal high
			load.next = bool(1)

			# generate random value to load to PC
			x = randrange(2**4)
			while((x % 4) != 0):
				x = randrange(2**4)
			addr.next = modbv(x)[32:]

		# otherwise do nothing
		else:
			load.next = bool(0)
			addr.next = modbv(0)[32:]

	# output monitor for debugging purposes
	@instance
        def output_monitor():
                print "t(ns)\t cycle\t output\t addr\t en\t load"
                print "---------------------------------------------"
                while True:
			yield en.posedge
                        print "%d\t %d\t %s\t %s\t %d\t %d" % (now(), count, hex(output), hex(addr), en, load)

	return instances()

def simulate(timesteps):
	"""
	Function for running simulation

	:param input timesteps: amount of steps for simulation
	"""

        # get trace on signals
	tb = traceSignals(pc_testbench)

	# run simulation
	sim = Simulation(tb)
	sim.run(timesteps)

def main():
	# call simulation for 2000 steps
	simulate(1000)

if __name__ == '__main__':
	main()
