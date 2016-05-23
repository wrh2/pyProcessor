"""
	Simulation for application-specific processor

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from PC import PC
#from RAM import RAM
from regfile import regfile
from EEPROM import EEPROM, insert_program
from AND import logic_AND
from ALU import ALU
from IRDecode import IRDecode

content = insert_program()

def processor_testbench():
	""" Program counter signals """
	load, clk = [Signal(bool(0)) for i in range(2)]
	en = Signal(bool(0))
	output = Signal(modbv(0)[16:])

	""" ALU signals """
	Z, E, P, N = [Signal(bool(0)) for i in range(4)]
	result = Signal(modbv(0)[32:])
	rdy = Signal(bool(1))

	""" Instruction memory signals and instantiation """
	Ins = Signal(modbv(0)[60:])
	instruction_memory = EEPROM(Ins, output, clk, CONTENT=content)

	""" Instruction Reg/Decoder signals and instantiation """
	J, BEQ, BZ, BP, BN, NOP = [Signal(bool(0)) for i in range(6)]
	notHalt = Signal(bool(1))
	op_to_ALU = Signal(modbv(0)[12:])
	Addr0, Addr1, Addr2 = [Signal(modbv(0)[16:]) for i in range(3)]

	instruction_regdecode = IRDecode(Ins,
					J,
					BEQ,
					BZ,
					BP,
					BN,
					notHalt,
					NOP,
					op_to_ALU,
					Addr0, Addr1, Addr2, clk)

	""" main memory signals and instantiation """
	dout0, dout1, dout2 = [Signal(modbv(0)[32:]) for i in range(3)]
	we0 = Signal(bool(0))
	ram_inst = RAM(dout0, dout1, dout2,
		       result, Signal(0), Signal(0),
		       we0, Signal(0), Signal(0),
		       Addr0, Addr1, Addr2, clk)

	""" ALU instantiation """
	ALU_inst = ALU(result, op_to_ALU, dout1, dout2,
		       Z, E, P, N, rdy, clk)

	""" 4-way AND signals and instantiation """
	r0, r1, r2, r3 = [Signal(bool(0)) for i in range(4)]
	AND_inst = logic_AND(BZ, Z, BEQ, E, BP, P, BN, N,
			      r0, r1, r2, r3)

	""" Program counter instantiation """
	program_counter = PC(output, Addr0, rdy, load)

	""" for counting clock cycles """
	cycles = Signal(0)

	""" clock generator """
	@always(delay(10))
	def clkgen():
		clk.next = not clk

	""" clock cycle count """
	@always(clk.negedge)
	def clkcount():
		cycles.next += 1

	""" increment PC """
	@instance
	def inc_pc():
		while True:
			yield result
			en.next = bool(1)
			for i in range(1):
				yield clk.negedge
			en.next = bool(0)

	""" check for jump/branch """
	@always(result)
	def load_addr():
		load.next = r0 | r1 | r2 | r3 | J

	""" write back result to memory """
	@instance
	def write_back():
		while True:
			yield result
			we0.next = bool(1)
			for i in range(1):
				yield clk.negedge
			we0.next = bool(0)

	return instances()

def simulate(timesteps):
	tb = traceSignals(processor_testbench)
	sim = Simulation(tb)
	sim.run(timesteps)

def main():
	simulate(5000)

if __name__ == '__main__':
        main()
