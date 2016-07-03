"""
	pyProcessor Module

	Programmed by William Harrington
	github.com/wrh2
	wrh2.github.io
"""

import os.path
from random import randrange
from myhdl import *

class pyProcessor:
	def __init__(self, instructions='program.hex', mem_image='memory_image.hex'):
		self.instructions = instructions
		self.instruction_memory = self.__insert_program(instructions)
		self.main_memory = self.__initialize_memory(mem_image)
		self.wb_instructions = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0xF]

	def __insert_program(self, fname):
		""" creates content for EEPROM """
		if os.path.isfile(fname):
			with open(fname) as f:
				content = [modbv(int(x, 16))[32:] for x in f.readlines()]
			return content
		else:
			raise ValueError('Program file %s not found' % fname)

	def __initialize_memory(self, fname):
		""" creates content for RAM """
		if os.path.isfile(fname):
			with open(fname) as f:
				content = [modbv(int(x, 16))[32:] for x in f.readlines()]
			f.close()
			msb = [y[32:16] for y in content]
			lsb = [y[16:] for y in content]
			content = []
			for x,y in zip(msb,lsb):
				content.append(x)
				content.append(y)
			return content
		else:
			raise ValueError('Memory image %s not found' % fname)

	def __PC(self, output, value,
		en, load):
		"""
		Program counter module

        	:param output output: output of the program counter
		:param input value: value to load into program counter
		:param input en: enable, control signal for incrementing counter
		:param input load: load, control signal for loading value into program counter  
	        """

		# sensitivity list: enable, load
		@always(en, load)
		def update():
			""" updates the output of the PC """

			# check that enable is high
			if en:

				# check that load is high
				if load:

					# next output will be value
					output.next = value
				else:

					# otherwise, increment output by 4
					#output.next += 0x4

					# increment by 1
					output.next += 0x1
		return update

	def __EEPROM(self, dout, addr,
		     clk, width=32):
		"""
	        Module for EEPROM. Address space of 2^16 and
		each address contains 32 bits. The most significant 8 bits
		are the op code and the remaining 24 are the address of
		operands A and B and where the result of the op goes.

		:param input addr: address of memory location
		:param output dout: data output for given address
		"""
		mem = [Signal(x) for x in self.instruction_memory]

		# sensitive to positive edge of clock
	    	@always(clk.posedge)
		def read():

			# output data at memory location
			dout.next = mem[int(addr)]

		return read

	def __IRDecode(self, Ins, J,
		       BEQ, BZ, BP,
		       BN, notHalt, NOP,
		       op, Addr0, Addr1,
		       Addr2, clk):
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

	def __ANDgate(self, a0, b0,
		      a1, b1, a2,
		      b2, a3, b3,
		      r0, r1, r2,
		      r3):
		@always_comb
		def logic():
			r0.next = a0 & b0
			r1.next = a1 & b1
			r2.next = a2 & b2
			r3.next = a3 & b3

		return instances()


	def __RAM(self, dout0, dout1,
		  dout2, din, we,
		  addr0, addr1, addr2,
		  clk):

		mem = [Signal(x) for x in self.main_memory]
		[mem.append(Signal(modbv(0)[16:])) for i in range((2**8)-len(mem))]

		@always(clk.posedge)
		def write():
			if we:
				mem[int(addr0)].next = din

		@always(clk.posedge)
		def read():
			dout0.next = mem[int(addr0)]
			dout1.next = mem[int(addr1)]
			dout2.next = mem[int(addr2)]

		return write, read

	def __ALU(self, result, op,
		a, b, Z,
		E, P, N,
		width=16):

		addition = Signal(modbv(0)[width:], delay=20)
		subtraction = Signal(modbv(0)[width:], delay=20)
		multiplication = Signal(modbv(0)[width:], delay=20)
		normalOR = Signal(modbv(0)[width:], delay=20)
		normalAND = Signal(modbv(0)[width:], delay=20)
		exclusiveOR = Signal(modbv(0)[width:], delay=20)
		LOAD = Signal(modbv(0)[width:], delay=20)
		STORE = Signal(modbv(0)[width:], delay=20)
		BZ = Signal(modbv(0)[width:], delay=20)
		BEQ = Signal(modbv(0)[width:], delay=20)
		BP = Signal(modbv(0)[width:], delay=20)
		BN = Signal(modbv(0)[width:], delay=20)
		JMP = Signal(modbv(0)[width:], delay=20)
		HALT = Signal(modbv(0)[width:], delay=20)
		NOP = Signal(modbv(0)[width:], delay=20)
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
				LOAD.next = modbv(a)[width:]
			if op == 0x7:
				STORE.next = modbv(a)[width:]
			if op == 0x8:
				BZ.next = modbv(0x8)[width:]
			if op == 0x9:
				BEQ.next = modbv(0x9)[width:]
			if op == 0xA:
				BP.next = modbv(0xA)[width:]
			if op == 0xB:
				BN.next = modbv(0xB)[width:]
			if op == 0xC:
				JMP.next = modbv(0xC)[width:]
			if op == 0xD:
				HALT.next = modbv(0xD)[width:]
			if op == 0xE:
				NOP.next = modbv(0xE)[width:]
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

		@always(LOAD)
		def output_LOAD():
			result.next = LOAD

		@always(STORE)
		def output_STORE():
			result.next = STORE

		@always(BZ)
		def output_BZ():
			result.next = BZ

		@always(BEQ)
		def output_BEQ():
			result.next = BEQ

		@always(BP)
		def output_BP():
			result.next = BP
	
		@always(BN)
		def output_BN():
			result.next = BN

		@always(JMP)
		def output_JMP():
			result.next = JMP

		@always(HALT)
		def output_HALT():
			result.next = HALT

		@always(NOP)
		def output_NOP():
			result.next = NOP

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

		return instances()

	def __testbench(self):
		""" Program counter signals """
		load, clk = [Signal(bool(0)) for i in range(2)]
		en = Signal(bool(0))
		output = Signal(modbv(0)[16:])

		""" ALU signals """
		Z, E, P, N = [Signal(bool(0)) for i in range(4)]
		result = Signal(modbv(0)[16:])

		""" Instruction memory signals and instantiation """
		Ins = Signal(modbv(0)[32:])
		instruction_memory = self.__EEPROM(Ins, output, clk)

		""" Instruction Reg/Decoder signals and instantiation """
		J, BEQ, BZ, BP, BN, NOP = [Signal(bool(0)) for i in range(6)]
		notHalt = Signal(bool(1))
		Addr0, Addr1, Addr2 = [Signal(modbv(0)[8:]) for i in range(3)]
		op_to_ALU = Signal(modbv(0)[8:], delay=20)

		instruction_regdecode = self.__IRDecode(Ins, J, BEQ,
						BZ, BP, BN,
						notHalt, NOP, op_to_ALU,
						Addr0, Addr1, Addr2,
						clk)

		""" main memory signals and instantiation """
		dout0, dout1, dout2 = [Signal(modbv(0)[16:]) for i in range(3)]
		we0 = Signal(bool(0))
		ram_inst = self.__RAM(dout0, dout1, dout2,
				      result, we0, Addr0,
				      Addr1, Addr2, clk)

		""" ALU instantiation """
		ALU_inst = self.__ALU(result, op_to_ALU, dout1, dout2,
			       Z, E, P, N)

		""" 4-way AND signals and instantiation """
		r0, r1, r2, r3 = [Signal(bool(0)) for i in range(4)]
		AND_inst = self.__ANDgate(BZ, Z, BEQ,
					  E, BP, P,
					  BN, N, r0,
					  r1, r2, r3)

		""" Program counter instantiation """
		program_counter = self.__PC(output, Addr0, en, load)

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
				if op_to_ALU in self.wb_instructions:
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

	def simulate(self, timesteps=1000):
		output = self.__testbench		

		# get trace on signals
		tb = traceSignals(output)

		# run simulation
		sim = Simulation(tb)
		sim.run(timesteps)

