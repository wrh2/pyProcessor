"""
	Implementation of Instruction Register/Decoder

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *

def IRDecode(Ins, J, BEQ, BZ, BP, BN, notHalt, NOP, op, Addr0, Addr1, Addr2, clk):
	"""
	Module for Instruction Register/Decoder
	"""
	@always(clk.posedge)
	def latch_instruction():
		# outputs
		op.next = Ins[32:24]
		Addr0.next = Ins[24:16]
		Addr1.next = Ins[16:8]
		Addr2.next = Ins[8:0]

		# branch if zero
		if op == 0x8:
			BZ.next = bool(1)
		else:
			BZ.next = bool(0)

		# branch if equal
		if op == 0x9:
			BEQ.next = bool(1)
                else:
			BEQ.next = bool(0)

		# branch is positive
		if op == 0xA:
			BP.next = bool(1)
                else:
			BP.next = bool(0)

		# branch if negative
		if op == 0xB:
			BN.next = bool(1)
                else:
			BN.next = bool(0)

		# jump
		if op == 0xC:
			J.next = bool(1)
                else:
			J.next = bool(0)

		# halt
		if op == 0xD:
			notHalt.next = bool(0)
                else:
			notHalt.next = bool(1)

		# no op
		if op == 0xE:
			NOP.next = bool(1)
                else:
			NOP.next = bool(0)

	return instances()
