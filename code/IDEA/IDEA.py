"""
	High level implementation of IDEA encryption algorithm.
	This code is to help myself understand and explain the
	IDEA algorithm and the operations involved.

	Programmed by William Harringt
	ECE486 Final Project
"""
# for generating random numbers
from random import randint, randrange

#use MyHDL for binary representations and modulo behavior
from myhdl import *

def addition(a, b, width=16):
    """ make sure the arguments are modbv of length 4-bits """
    a = modbv(a)[width:]
    b = modbv(b)[width:]
    
    """ return the addition of the numbers, again make sure length is 4-bits """
    return modbv(a+b)[width:]

def inv_addition(a, width=16):
    """ make sure argument is modbv of length 4-bits """
    a = modbv(a)[width:]
    
    """ return the inverse in 4-bits """
    return modbv((~a)+1)[width:]

def multiply(a,b, width=16):
    """ make sure the arguments are modbv of length 4-bits """
    a = modbv(a, min=1, max=2**width)[width:]
    b = modbv(b, min=1, max=2**width)[width:]
    
    """ return the multiplication of the numbers, again make sure length is 4-bits """
    return modbv((a*b) % ((2**width)+1))[width:]

def inv_mult(a, width=16):
    a = modbv(a, min=1, max=2**width)[width:]
    
    """ Euler's totient theorem """
    return modbv((a**((2**width)-1)) % ((2**width) + 1))[width:]

def xor(a, b, width=16):
    return (a ^ b)[width:]

def rotate_left(a, numOfRot):
    # check that length is non-zero
    if(len(a)):
        result = a
        for i in range(numOfRot):
            # least significant bits                                                                                                                               
            LSB = result[len(result)-1:]
            # most significant bits                                                                                                                                
            MSB = result[len(result):len(result)-1]
            # MSB goes to the back                                                                                                                                 
            result = concat(modbv(LSB), modbv(MSB))
        return result   
    else:
        return 0

def separate_bits(bits, num):
    x = []
    for i in range(num):
        x.append(modbv(bits[(16*(i+1)):16*i]))
    return list(reversed(x))

def create_subkeys(key):
    # array for holding subkeys that will be created                                                                                                                       
    subkeys = []
    # aray for holding keys from each round                                                                                                                                
    round = []
    if(len(key)==0):
        return 0
    for i in range(7):
        round = separate_bits(key, 8)
        subkeys.append(round)
        key = rotate_left(key, 25)
    result = []
    for arr in subkeys:
        result += arr
    return result

def encrypt(arg, keys):
    x = arg
    for i in range(8):
        x = separate_bits(x, 4)
        print 'Round %d' % (i+1)
        print 'X = %x, %x, %x, %x' % (x[0], x[1], x[2], x[3])
	print 'SK = %x, %x, %x, %x, %x, %x' % (keys[0+(6*i)], keys[1+(6*i)], keys[2+(6*i)], keys[3+(6*i)], keys[4+(6*i)], keys[5+(6*i)])
        step1 = multiply(x[0], keys[0+(6*i)])
	print 'step1: %x multiply %x = %x' % (x[0], keys[0+(6*i)], step1)
        step2 = addition(x[1], keys[1+(6*i)])
	print 'step2: %x addition %x = %x' % (x[1], keys[1+(6*i)], step2)
        step3 = addition(x[2], keys[2+(6*i)])
	print 'step3: %x addition %x = %x' % (x[2], keys[2+(6*i)], step3)
        step4 = multiply(x[3], keys[3+(6*i)])
	print 'step4: %x multiply %x = %x' % (x[3], keys[3+(6*i)], step4)
        step5 = xor(step1, step3)
	print 'step5: %x xor %x = %x' % (step1, step3, step5)
        step6 = xor(step2, step4)
	print 'step6: %x xor %x = %x' % (step2, step4, step6)
        step7 = multiply(step5, keys[4+(6*i)])
	print 'step7: %x multiply %x = %x' % (step5, keys[4+(6*i)], step7)
        step8 = addition(step6, step7)
	print 'step8: %x addition %x = %x' % (step6, step7, step8)
        step9 = multiply(step8, keys[5+(6*i)])
	print 'step9: %x multiply %x = %x' % (step8, keys[7+(6*i)], step9)
        step10 = addition(step7, step9)
	print 'step10: %x addition %x = %x' % (step7, step9, step10)
        step11 = xor(step1, step9)
	print 'step11: %x xor %x = %x' % (step1, step9, step11)
        step12 = xor(step3, step9)
	print 'step12: %x xor %x = %x' % (step3, step9, step12)
        step13 = xor(step2, step10)
	print 'step13: %x xor %x = %x' % (step2, step10, step13)
        step14 = xor(step4, step10)
	print 'step14: %x xor %x = %x' % (step4, step10, step14)

        x = concat(step11, step12, step13, step14)
        if i == 7:
            x = concat(step11, step13, step12, step14)

    x = separate_bits(x, 4)
    print 'Output'
    print 'X: %x, %x, %x, %x' % (x[0], x[1], x[2], x[3])
    print 'SK: %x, %x, %x, %x' % (keys[48], keys[49], keys[50], keys[51])
    step1 = multiply(x[0], keys[48])
    step2 = addition(x[1], keys[49])
    step3 = addition(x[2], keys[50])
    step4 = multiply(x[3], keys[51])
    
    return concat(step1, step2, step3, step4)
