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
	ADD = modbv(0x0)[8:]
	SUB = modbv(0x1)[8:]
	MUL = modbv(0x2)[8:]
	OR = modbv(0x3)[8:]
        AND = modbv(0x4)[8:]
	XOR = modbv(0x4)[8:]
	instructions = [concat(ADD, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:]),
			concat(SUB, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:]),
			concat(MUL, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:]),
			concat(OR, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:]),
			concat(AND, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:]),
			concat(XOR, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:])]
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

