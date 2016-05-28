"""
	Simple 4 way AND module

	Programmed by William Harrington
	ECE486 Final Project
"""
from myhdl import *

def logic_AND(a0, b0, a1, b1, a2, b2, a3, b3, r0, r1, r2, r3):

	@always_comb
	def logic():
		r0.next = a0 & b0
		r1.next = a1 & b1
		r2.next = a2 & b2
		r3.next = a3 & b3

	return instances()
