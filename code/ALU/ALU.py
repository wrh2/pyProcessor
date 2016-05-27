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

def ALU(result, op, a, b, Z, E, P, N, rdy, clk, width=16):
	"""
	Module for Arithmetic Logic Unit

	:param input op: op code
	:param input a: operand A
	:param input b: operand B
	:param output result: result of operation
        """
	cycles = 0
	prop = Signal(modbv(0)[width:])

	@always_comb
	def ALU_logic():
		""" Logic for ALU """
		if op == 0x4:
			prop.next = modbv(a+b)[width:]
		if op == 0x5:
			prop.next = modbv(a-b)[width:]
		if op == 0x6:
			prop.next = modbv(a*b)[width:]
		if op == 0x7:
			prop.next = modbv(a%b)[width:]
		if op == 0x20:
			prop.next = modbv(a|b)[width:]
		if op == 0x28:
			prop.next = modbv(a&b)[width:]
		if op == 0x30:
			prop.next = modbv(a^b)[width:]

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

		if result.next < 0:
			N.next = bool(1)
		else:
			N.next = bool(0)

	def checkRdy():
		if rdy:
			rdy.next = bool(0)
		else:
			rdy.next = bool(1)

	@instance
	def ready():
		while True:
			yield prop
			checkRdy()
			# mult op
			if op == 0x6:
				cycles = 116 
			# add/sub/mod op
			elif op == 0x4 or op == 0x5 or op == 0x7:
				cycles = 8
			else:
				cycles = 1
			for i in range(cycles):
				yield clk.negedge
                	checkRdy()

	@instance
        def prop_delay():
		"""
                This function models the prop delay for the ALU.
		
		The ALU is essentially just a combination of
		combinational circuits that perform the operation.
		For instance, the add and subtract operations
		are performed with an adder-subtractor circuit
		that has a set propagation delay (Tpd) for each stage.
		This model is for a ripple-carry adder/subtractor.
		This means the total prop delay for an add/subtract operation
		is Tpd * number of bits.

		The worst case operation is multiplication.
		For multiplication, the delay is Tpd * (number of bits)^2

		Clock speed = 50MHz,
		Clock period = 20ns,
                Tpd = 9ns,
		number of bits = 16

		for mult, delay = ceiling((16*16*9)/20) = 116
		for add/sub, delay = ceiling(16*9) = 8
		"""
		while True:
			yield prop
			# mult op
			if op == 0x6:
				cycles = 116 
			# add/sub/mod op
			elif op == 0x4 or op == 0x5 or op == 0x7:
				cycles = 8
			else:
				cycles = 1

			for i in range(cycles):
				yield clk.negedge
			result.next = prop

	return instances()
