"""
	Program Counter

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from random import randrange

def PC(output, value, en, load):
	"""
	Program counter module

        :param output output: output of the program counter
	:param input value: value to load into program counter
	:param input en: enable, control signal for incrementing counter
	:param input load: load, control signal for loading value into program counter  
        """

	# sensitivity list: enable, load
	@always(en, load)
	def update():
		""" updates the output of the PC """

		# check that enable is high
		if en:

			# check that load is high
			if load:

				# next output will be value
				output.next = value
			else:

				# otherwise, increment output by 4
				output.next += 0x4
				#output.next += 0x1
	return update

def pc_testbench():
        """
	Test bench for the program counter
	"""

	# initialize signals
	output = Signal(modbv(0)[32:])
	addr = Signal(modbv(0)[32:])
	load, en, clk = [Signal(bool(0)) for i in range(3)]

	# instantiate program counter
	pc_inst = PC(output, addr, en, load)

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

		# check to see if time divides evenly by 110
		# and that en.next is high
		if (now() % 110 ) == 0 and en.next:

			# bring load signal high
			load.next = bool(1)

			# generate random value to load to PC
			addr.next = modbv(randrange(2**32))[32:]

		# otherwise do nothing
		else:
			load.next = bool(0)
			addr.next = modbv(0)[32:]

	# output monitor for debugging purposes
	@instance
        def output_monitor():
                print "t(ns) output addr en"
                print "--------------------"
                while True:
			yield output
                        print "%d %s %s %d" % (now(), hex(output), hex(addr), en)

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
	simulate(2000)

if __name__ == '__main__':
	main()
