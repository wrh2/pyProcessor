"""
	Implementation of Arithmetic Logic Unit module

	The ALU internally has a ripple carry adder/subtractor
	but this isn't actually modelled below. Instead, an
	equivalent propagation delay is implemented before
	the output changes based on the given operation.

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from random import randrange

def ALU(result, op, a, b, Z, E, P, N, rdy, width=16):
	addition = Signal(modbv(0)[width:], delay=20)
	subtraction = Signal(modbv(0)[width:], delay=20)
	multiplication = Signal(modbv(0)[width:], delay=700)
	normalOR = Signal(modbv(0)[width:], delay=20)
	normalAND = Signal(modbv(0)[width:], delay=20)
	exclusiveOR = Signal(modbv(0)[width:], delay=20)
	mod_mult = Signal(modbv(0)[width:], delay=700)

	@always_comb
	def ALU_logic():
		""" Logic for ALU """
		if op == 0x0:
			addition.next = modbv(a+b)[width:]
		if op == 0x1:
			subtraction.next = modbv(a-b)[width:]
		if op == 0x2:
			multiplication.next = modbv(a*b)[width:]
		if op == 0x3:
			normalOR.next = modbv(a|b)[width:]
		if op == 0x4:
			normalAND.next = modbv(a&b)[width:]
		if op == 0x5:
			exclusiveOR.next = modbv(a^b)[width:]
		if op == 0x6:
			result.next = modbv(0x6)[width:]
		if op == 0x7:
			result.next = modbv(0x7)[width:]
		if op == 0x8:
			result.next = modbv(0x8)[width:]
		if op == 0x9:
			result.next = modbv(0x9)[width:]
		if op == 0xA:
			result.next = modbv(0xA)[width:]
		if op == 0xB:
			result.next = modbv(0xB)[width:]
		if op == 0xC:
			result.next = modbv(0xC)[width:]
		if op == 0xD:
			result.next = modbv(0xD)[width:]
		if op == 0xE:
			result.next = modbv(0xE)[width:]
		if op == 0xF:
			mod_mult.next = modbv((a*b) % ((2**width)+1))[width:]

	@always(addition)
	def output_add():
		result.next = addition

	@always(subtraction)
	def output_sub():
		result.next = subtraction

	@always(multiplication)
	def output_mult():
		result.next = multiplication

	@always(multiplication)
	def output_mult():
		result.next = multiplication

	@always(normalOR)
	def output_normOR():
		result.next = normalOR

	@always(normalAND)
	def output_normAND():
		result.next = normalAND

	@always(exclusiveOR)
	def output_xOR():
		result.next = exclusiveOR

	@always(mod_mult)
	def output_modmult():
		result.next = mod_mult

	@always_comb
	def checkConditions():
		if a == b:
			E.next = bool(1)
		else:
			E.next = bool(0)

		if result.next == 0:
			Z.next = bool(1)
		else:
			Z.next = bool(0)

		if result.next > 0:
			P.next = bool(1)
		else:
			P.next = bool(0)

		if (op == 0x0) and (a+b < 0):
			N.next = bool(1)
		elif (op == 0x1) and (a-b < 0):
			N.next = bool(1)
		elif (op == 0x2) and (a*b < 0):
			N.next = bool(1)
		else:
			N.next = bool(0)

	@instance
	def nextOp():
		while True:
			yield result
			rdy.next = not rdy
			yield a,b,op
			yield delay(5)
			rdy.next = not rdy
	
	return instances()
