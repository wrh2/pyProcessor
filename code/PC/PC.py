"""
	Program Counter

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *
from random import randrange

def PC(output, value, en, load):
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
				output.next += 0x4
	return update
