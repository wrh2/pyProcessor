from random import randrange
from myhdl import *
from RAM import RAM

def RAM_testbench():
        dout0, dout1, dout2 = [Signal(modbv(0)[16:]) for i in range(3)]
	addr0, addr1, addr2 = [Signal(modbv(0)[8:]) for i in range(3)]
	din = Signal(modbv(0)[16:])
	we, clk = [Signal(bool(0)) for i in range(2)]

	count = Signal(modbv(0)[4:])
	cycle = Signal(modbv(0)[4:])

	ram_inst = RAM(dout0, dout1, dout2, din, we, addr0, addr1, addr2, clk)

	@always(delay(10))
	def clkgen():
		clk.next = not clk

	@always(clk.posedge)
	def update():
		count.next += 1
		if count == 15:
			cycle.next += 1

	@always(clk.posedge)
	def stimulus():
		addr0.next = modbv(count.val)[16:]
		addr1.next = modbv(count.val)[16:]
		addr2.next = modbv(count.val)[16:]
		din.next = modbv(count.val)[16:]

		if cycle < 1:
			we.next = bool(1)
		if cycle >= 1:
			we.next = bool(0)

	return instances()

def simulate(timesteps):
	tb = traceSignals(RAM_testbench)
	sim = Simulation(tb)
	sim.run(timesteps)

def main():
	simulate(1000)

if __name__ == '__main__':
	main()
