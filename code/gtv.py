"""
	Programming utilities that I made for use
	on the ECE486 final project

	Programmed by William Harrington
	ECE486 Final Project
"""
from random import randrange
from myhdl import *

def generate_cases():
	""" 
	Function creates csv file with interesting test
	cases for the ALU.

	This however ended up not being used in the final product.
	"""
	operations = [0, 1, 2]
	operands = [(2**16-1, 1), (0, 1), (2**16-1, 2**16-1)]

	f = open('test_vectors.csv', 'w')
	f.write('# [0]op, [1]rand1, [2] rand2\n')
	for i, j in zip(range(len(operations)), range(len(operands))):
        	f.write(hex(operations[i]) \
                	+ ', ' + hex(operands[j][0]) \
                	+ ', ' + hex(operands[j][1]) + '\n')
	f.close()

def generate_hex(fname):
	"""
	This function creates .hex file with
	random hex values that can be placed into
	instruction memory to test the processor

	:param input fname: filename
	"""
	ADD = modbv(0x4)[12:]
	SUB = modbv(0x5)[12:]
	MUL = modbv(0x6)[12:]
	MOD = modbv(0x7)[12:]
	instructions = [concat(ADD, modbv(randrange(2**48-1))[48:]),
			concat(SUB, modbv(randrange(2**48-1))[48:]),
			concat(MUL, modbv(randrange(2**48-1))[48:]),
			concat(MOD, modbv(randrange(2**48-1))[48:]),
			concat(ADD, modbv(randrange(2**48-1))[48:]),
			concat(SUB, modbv(randrange(2**48-1))[48:]),
			concat(MUL, modbv(randrange(2**48-1))[48:]),
			concat(MOD, modbv(randrange(2**48-1))[48:]),
			concat(ADD, modbv(randrange(2**48-1))[48:]),
			concat(SUB, modbv(randrange(2**48-1))[48:]),
			concat(MUL, modbv(randrange(2**48-1))[48:]),
			concat(MOD, modbv(randrange(2**48-1))[48:]),
			concat(ADD, modbv(randrange(2**48-1))[48:]),
			concat(SUB, modbv(randrange(2**48-1))[48:]),
			concat(MUL, modbv(randrange(2**48-1))[48:]),
			concat(MOD, modbv(randrange(2**48-1))[48:])]
	f = open(fname, 'w')
	for i in instructions:
		f.write(hex(i)+'\n')
	f.close()

def str2hex(string):
	""" returns hex from string """
	return int(string, 16)

def array2hex(array):
	""" 
        converts array of non-hex values into
	array of hex values

	:param input array: array to convert
	"""
	newArray = []
	for element in array:
		newArray.append(str2hex(element))
	return newArray

