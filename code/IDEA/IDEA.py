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
        step1 = multiply(x[0], keys[0+(6*i)])
        step2 = addition(x[1], keys[1+(6*i)])
        step3 = addition(x[2], keys[2+(6*i)])
        step4 = multiply(x[3], keys[3+(6*i)])
        step5 = xor(step1, step3)
        step6 = xor(step2, step4)
        step7 = multiply(step5, keys[4+(6*i)])
        step8 = addition(step6, step7)
        step9 = multiply(step8, keys[5+(6*i)])
        step10 = addition(step7, step9)
        step11 = xor(step1, step9)
        step12 = xor(step3, step9)
        step13 = xor(step2, step10)
        step14 = xor(step4, step10)

        x = concat(step11, step12, step13, step14)
        if i == 7:
            x = concat(step11, step13, step12, step14)

    x = separate_bits(x, 4)
    step1 = multiply(x[0], keys[48])
    step2 = addition(x[1], keys[49])
    step3 = addition(x[2], keys[50])
    step4 = multiply(x[3], keys[51])
    
    return concat(step1, step2, step3, step4)
