from myhdl import *
from random import randrange
from IRDecode import IRDecode


def IRDecode_testbench():
	""" initialize signals """
	Ins = Signal(concat(modbv(randrange(2**4))[8:],
		     	    modbv(randrange(2**4))[8:],
			    modbv(randrange(2**4))[8:],
			    modbv(randrange(2**4))[8:]))
	J, BEQ, BZ, BP, BN, NOP = [Signal(bool(0)) for i in range(6)]
	notHalt = Signal(bool(1))
	op = Signal(modbv(0)[8:])
	Addr0, Addr1, Addr2 = [Signal(modbv(0)[8:]) for i in range(3)]
	clk = Signal(bool(0))
	cycles = Signal(0)

	""" IRDecode inst """
	ird_inst = IRDecode(Ins, J, BEQ, BZ, BP, BN, notHalt, NOP, op, Addr0, Addr1, Addr2, clk)

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
		Ins.next = concat(modbv(randrange(2**4))[8:],
		     	    modbv(randrange(2**4))[8:],
			    modbv(randrange(2**4))[8:],
			    modbv(randrange(2**4))[8:])
		#if cycles > 20:
		#	Ins.next = modbv(randrange(2**48, 2**60))[60:]

	""" output monitor for debugging purposes """
	@instance
	def output_monitor():
		print 'cycles Ins op addr0 addr1 addr2'
		print '-------------------------------'
		while True:
			yield clk.negedge
			print '%s %x %x %x %x %x' % (cycles, Ins, op, Addr0, Addr1, Addr2)

	return instances()

def simulate(timesteps):
	tb = traceSignals(IRDecode_testbench)
	sim = Simulation(tb)
	sim.run(timesteps)

def main():
	simulate(500)

if __name__ == '__main__':
	main()

