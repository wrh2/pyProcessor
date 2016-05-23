from myhdl import *
from PC import PC
from EEPROM import EEPROM

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
