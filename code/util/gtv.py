"""
	Programming utilities that I made for use
	on the ECE486 final project

	Programmed by William Harrington
	ECE486 Final Project
"""
from random import randrange
from myhdl import *
from IDEA import *

def generate_instructions(fname):
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
	XOR = modbv(0x5)[8:]
	JMP = modbv(0xC)[8:]
	instructions = [concat(ADD, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:]),
			concat(SUB, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:]),
			concat(MUL, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:]),
			concat(OR, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:]),
			concat(AND, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:]),
			concat(XOR, modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:], modbv(randrange(2**8))[8:]),
			concat(JMP, modbv(0x0)[8:], modbv(0x0)[8:], modbv(0x0)[8:])]
	f = open(fname, 'w')
	for i in range(10):
		for i in instructions:
			f.write((hex(i)).strip('L')+'\n')
	f.close()

def generate_memory_image(fname='memory_image.hex'):
	plaintext = [modbv(0x20822C1109510840)[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:],
		     modbv(randrange(2**64))[64:]]
	
	key = modbv(0x7802c45144634a43fa10a15c405a4a42)[128:]
	subkeys = create_subkeys(key)

	f = open(fname, 'w')
	for i in range(len(subkeys)):
		if i+1 < len(subkeys):
			f.write(hex(subkeys[i]).strip('L') + (hex(subkeys[i+1]).strip('0x')).strip('L') + '\n')
	for x in plaintext:
		f.write((hex(x[64:32])).strip('L')+'\n')
		f.write((hex(x[32:])).strip('L')+'\n')
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

