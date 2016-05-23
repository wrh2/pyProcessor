"""
	Implementation of Instruction Register/Decoder

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from random import randrange

def IRDecode(Ins, J, BEQ, BZ, BP, BN, notHalt, NOP, op, Addr0, Addr1, Addr2, clk):
	"""
	Module for Instruction Register/Decoder

	:param input Ins: 60-bit instruction
	:param output J: output for detecting a Jump instruction
	:param output BEQ: output for detecting branch equal instruction
	:param output BZ: output for detecting branch zero instruction
	:param output BP: output for detecting branch positive instruction
	:param output BN: output for detecting branch negative instruction
	:param output notHalt: output for detecting halt instruction (active low)
	:param output op: 8-bit op code output that goes to ALU
	:param output Addr0: address of where result should go
	:param output Addr1: address of operand A for ALU
	:param output Addr2: address of operand B for ALU
	"""
	internal_op = Signal(modbv(0)[12:])
	internal_addr0 = Signal(modbv(0)[16:])
	internal_addr1 = Signal(modbv(0)[16:])
	internal_addr2 = Signal(modbv(0)[16:])
        internal_BZ = Signal(bool(0))
	internal_BEQ = Signal(bool(0))
	internal_BP = Signal(bool(0))
	internal_BN = Signal(bool(0))

	@always(clk.posedge)
	def latch_instruction():
		internal_op.next = Ins[60:48]
		internal_addr0.next = Ins[48:32]
		internal_addr1.next = Ins[32:16]
		internal_addr2.next = Ins[16:0]

	@always(clk.negedge)
	def pass_on():
		op.next = internal_op
		Addr0.next = internal_addr0
		Addr1.next = internal_addr1
		Addr2.next = internal_addr2

		# 12th bit set, control instruction
		if internal_op[12:8] == 0x8:
			BZ.next = bool(1)
		else:
			BZ.next = bool(0)

		if internal_op[12:8] == 0x9:
			BEQ.next = bool(1)
                else:
			BEQ.next = bool(0)

		if internal_op[12:8] == 0xA:
			BP.next = bool(1)
                else:
			BP.next = bool(0)

		if internal_op[12:8] == 0xB:
			BN.next = bool(1)
                else:
			BN.next = bool(0)

		if internal_op[12:8] == 0xC:
			J.next = bool(1)
                else:
			J.next = bool(0)

		if internal_op[12:8] == 0xD:
			NOP.next = bool(1)
                else:
			NOP.next = bool(0)

		if internal_op[12:8] == 0xE:
			notHalt.next = bool(0)
                else:
			notHalt.next = bool(1)

	return instances()

def IRDecode_testbench():
	""" initialize signals """
	Ins = Signal(modbv(randrange(2**60))[60:])
	J, BEQ, BZ, BP, BN, NOP = [Signal(bool(0)) for i in range(6)]
	notHalt = Signal(bool(1))
	op = Signal(modbv(0)[12:])
	Addr0, Addr1, Addr2 = [Signal(modbv(0)[16:]) for i in range(3)]
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
		Ins.next = modbv(randrange(2**60))[60:]
		if cycles > 20:
			Ins.next = modbv(randrange(2**48, 2**60))[60:]

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
	
