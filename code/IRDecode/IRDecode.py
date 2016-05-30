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
	internal_op = Signal(modbv(0)[8:])
	internal_addr0 = Signal(modbv(0)[8:])
	internal_addr1 = Signal(modbv(0)[8:])
	internal_addr2 = Signal(modbv(0)[8:])

	@always(clk.posedge)
	def latch_instruction():
		internal_op.next = Ins[32:24]
		internal_addr0.next = Ins[24:16]
		internal_addr1.next = Ins[16:8]
		internal_addr2.next = Ins[8:0]

	@always(clk.posedge)
	def pass_on():

		# outputs
		op.next = internal_op
		Addr0.next = internal_addr0
		Addr1.next = internal_addr1
		Addr2.next = internal_addr2

		# branch if zero
		if internal_op == 0x8:
			BZ.next = bool(1)
		else:
			BZ.next = bool(0)

		# branch if equal
		if internal_op == 0x9:
			BEQ.next = bool(1)
                else:
			BEQ.next = bool(0)

		# branch is positive
		if internal_op == 0xA:
			BP.next = bool(1)
                else:
			BP.next = bool(0)

		# branch if negative
		if internal_op == 0xB:
			BN.next = bool(1)
                else:
			BN.next = bool(0)

		# jump
		if internal_op == 0xC:
			J.next = bool(1)
                else:
			J.next = bool(0)

		# halt
		if internal_op == 0xD:
			notHalt.next = bool(0)
                else:
			notHalt.next = bool(1)

		# no op
		if internal_op == 0xE:
			NOP.next = bool(1)
                else:
			NOP.next = bool(0)

	return instances()
