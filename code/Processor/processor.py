"""
	Simulation for application-specific processor

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from PC import PC
from RAM import RAM, initialize_memory
from EEPROM import EEPROM, insert_program
from AND import logic_AND
from ALU import ALU
from IRDecode import IRDecode

content = insert_program()
memory_image = initialize_memory()

wb_instructions = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0xF]

def processor_testbench():
	""" Program counter signals """
	load, clk = [Signal(bool(0)) for i in range(2)]
	en = Signal(bool(0))
	output = Signal(modbv(0)[16:])

	""" ALU signals """
	Z, E, P, N = [Signal(bool(0)) for i in range(4)]
	result = Signal(modbv(0)[16:])

	""" Instruction memory signals and instantiation """
	Ins = Signal(modbv(0)[32:])
        #InsTri = TristateSignal(modbv(0)[32:])
	#Ins = InsTri.driver()
	instruction_memory = EEPROM(Ins, output, clk, CONTENT=content)

	""" Instruction Reg/Decoder signals and instantiation """
	J, BEQ, BZ, BP, BN, NOP = [Signal(bool(0)) for i in range(6)]
	notHalt = Signal(bool(1))
	Addr0, Addr1, Addr2 = [Signal(modbv(0)[8:]) for i in range(3)]
	op_to_ALU = Signal(modbv(0)[8:], delay=20)

	#opTri = TristateSignal(modbv(0)[8:])
	#opDrive = opTri.driver()
	#Addr0Tri, Addr1Tri, Addr2Tri = [TristateSignal(modbv(0)[8:]) for i in range(3)]
	#Addr0 = Addr0Tri.driver()
	#Addr1 = Addr1Tri.driver()
	#Addr2 = Addr2Tri.driver()

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
	dout0, dout1, dout2 = [Signal(modbv(0)[16:]) for i in range(3)]
	#dout0Tri, dout1Tri, dout2Tri = [TristateSignal(modbv(0)[16:]) for i in range(3)]
	#dout0 = dout0Tri.driver()
	#dout1 = dout1Tri.driver()
	#dout2 = dout2Tri.driver()
	we0 = Signal(bool(0))
	ram_inst = RAM(dout0, dout1, dout2, result, we0, Addr0, Addr1, Addr2, clk, IMAGE=memory_image)

	""" ALU instantiation """
	ALU_inst = ALU(result, op_to_ALU, dout1, dout2,
		       Z, E, P, N)

	""" 4-way AND signals and instantiation """
	r0, r1, r2, r3 = [Signal(bool(0)) for i in range(4)]
	AND_inst = logic_AND(BZ, Z, BEQ, E, BP, P, BN, N,
			      r0, r1, r2, r3)

	""" Program counter instantiation """
	program_counter = PC(output, Addr0, en, load)

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
	#		for x in range(len(content)):
			yield result
			if notHalt:
				en.next = bool(1)
				for i in range(1):
					yield delay(10)
				en.next = bool(0)
	#		print 'last instruction reached'
	#		yield result
	#		raise StopSimulation

	""" check for jump/branch """
	@always_comb
	def load_addr():
		load.next = r0 | r1 | r2 | r3 | J

	""" write back result to memory """
	@instance
	def write_back():
		while True:
			yield result
			if op_to_ALU in wb_instructions:
				we0.next = bool(1)
				for i in range(1):
					yield clk.negedge
				we0.next = bool(0)

	#@always(notHalt.negedge)
	#def halt_op():
	#	print 'HALT!'
	#	raise StopSimulation

	#@always(opTri)
	#def read_opDrive():
	#	op_to_ALU.next = opTri

	return instances()

def simulate(timesteps):
	tb = traceSignals(processor_testbench)
	sim = Simulation(tb)
	sim.run(timesteps)

def main():
	simulate(2000)

if __name__ == '__main__':
        main()
