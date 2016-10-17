"""
	High level implementation of IDEA encryption algorithm.
	This code is to help myself understand and explain the
	IDEA algorithm and the operations involved.

	Programmed by William Harringt
	ECE486 Final Project
"""
from myhdl import *

def addition(a, b, width=16):   
     return modbv(a+b)[width:]

def inv_addition(a, width=16):
    a = modbv(a)[width:]
    return modbv((~a)+1)[width:]

def multiply(a,b, width=16):
    if a == 0:
        a = 2**16
    if b == 0:
        b = 2**16
    return modbv((a*b) % ((2**width)+1))[width:]

def inv_mult(a, width=16):
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

def create_subkeys(key, encrypt=True):
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
    if encrypt:
        return result[:52]
    else:
        buff = []
        reverse_subkeys = list(reversed(result[:52]))
        for j in range(len(reverse_subkeys)):
            if (j != 0) and (j % 6 == 0):
                buff.append(reverse_subkeys[j-6:j])
            if j == (len(reverse_subkeys) - 1):
                buff.append(reverse_subkeys[j-3:j+1])
        result = []
        for k in range(len(buff)):
            if k == 0:
                result.append(inv_mult(buff[k][3]))
                result.append(inv_addition(buff[k][2]))
                result.append(inv_addition(buff[k][1]))
                result.append(inv_mult(buff[k][0]))
                result.append(buff[k][5])
                result.append(buff[k][4])
            elif k >= 1 and k <= 7:
                result.append(inv_mult(buff[k][3]))
                result.append(inv_addition(buff[k][1]))
                result.append(inv_addition(buff[k][2]))
                result.append(inv_mult(buff[k][0]))
                result.append(buff[k][5])
                result.append(buff[k][4])
            else:
                result.append(inv_mult(buff[k][3]))
                result.append(inv_addition(buff[k][2]))
                result.append(inv_addition(buff[k][1]))
                result.append(inv_mult(buff[k][0]))
        return result

def encrypt(arg, keys, verbose=False):
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
        if verbose:
            print 'Round %d' % (i+1)
            print 'X = %x, %x, %x, %x' % (x[0], x[1], x[2], x[3])
            print 'SK = %x, %x, %x, %x, %x, %x' % (keys[0+(6*i)], keys[1+(6*i)], keys[2+(6*i)], keys[3+(6*i)], keys[4+(6*i)], keys[5+(6*i)])
            print 'step1: %x multiply %x = %x' % (x[0], keys[0+(6*i)], step1)
            print 'step2: %x addition %x = %x' % (x[1], keys[1+(6*i)], step2)
            print 'step3: %x addition %x = %x' % (x[2], keys[2+(6*i)], step3)
            print 'step4: %x multiply %x = %x' % (x[3], keys[3+(6*i)], step4)
            print 'step5: %x xor %x = %x' % (step1, step3, step5)
            print 'step6: %x xor %x = %x' % (step2, step4, step6)
            print 'step7: %x multiply %x = %x' % (step5, keys[4+(6*i)], step7)
            print 'step8: %x addition %x = %x' % (step6, step7, step8)
            print 'step9: %x multiply %x = %x' % (step8, keys[5+(6*i)], step9)
            print 'step10: %x addition %x = %x' % (step7, step9, step10)
            print 'step11: %x xor %x = %x' % (step1, step9, step11)
            print 'step12: %x xor %x = %x' % (step3, step9, step12)
            print 'step13: %x xor %x = %x' % (step2, step10, step13)
            print 'step14: %x xor %x = %x' % (step4, step10, step14)

        x = concat(step11, step12, step13, step14)

    x = separate_bits(x, 4)
    step1 = multiply(x[0], keys[48])
    step2 = addition(x[2], keys[49])
    step3 = addition(x[1], keys[50])
    step4 = multiply(x[3], keys[51])

    if verbose:
        print 'Output'
        print 'X: %x, %x, %x, %x' % (x[0], x[1], x[2], x[3])
        print 'SK: %x, %x, %x, %x' % (keys[48], keys[49], keys[50], keys[51])
        print 'step1: %x multiply %x = %x' % (x[0], keys[48], step1)
        print 'step2: %x addition %x = %x' % (x[1], keys[49], step2)
        print 'step3: %x addition %x = %x' % (x[2], keys[50], step3)
        print 'step4: %x multiply %x = %x' % (x[3], keys[51], step4)
    
    return concat(step1, step2, step3, step4)
