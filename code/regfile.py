"""
	Register file

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from random import randrange

memory_image = []

def regfile(dout0, dout1, dout2,
	din0, din1, din2,
	we0, we1, we2, 
	addr0, addr1, addr2,
	clk, width=32):

	mem0 = [Signal(modbv(randrange(2**16)))[width:] for i in range(2**16)]
	mem1 = [Signal(modbv(randrange(2**16)))[width:] for i in range(2**16)]
	mem2 = [Signal(modbv(randrange(2**16)))[width:] for i in range(2**16)]

	@always(clk.posedge)
	def logic():
		if we0:
			mem0[addr0].next = din0
		dout0.next = mem0[addr0]
		if we1:
			mem1[addr1].next = din1
		dout1.next = mem1[addr1]
		if we2:
			mem2[addr2].next = din2
		dout2.next = mem2[addr2]
	return instances()

def regfile_testbench():
	din0, din1, din2 = [Signal(modbv(0)[32:]) for i in range(3)]
	dout0, dout1, dout2 = [Signal(modbv(0)[32:], delay=40) for i in range(3)]
	addr0, addr1, addr2 = [Signal(modbv(0)[16:]) for i in range(3)]
	we0, we1, we2, clk = [Signal(bool(0)) for i in range(4)]
	
	regf_inst = regfile(dout0, dout1, dout2,
		       din0, din1, din2,
		       we0, we1, we2,
		       addr0, addr1, addr2, clk)

	@always(delay(10))
	def clkgen():
		clk.next = not clk

	@always(clk.posedge)
	def stimulus():
		addr0.next = modbv(randrange(2**16))[16:]
		addr1.next = modbv(randrange(2**16))[16:]
		addr2.next = modbv(randrange(2**16))[16:]

	return instances()

def simulate(timesteps):
	tb = traceSignals(regfile_testbench)
	sim = Simulation(tb)
	sim.run(timesteps)

def main():
	simulate(2000)

if __name__ == '__main__':
	main()
