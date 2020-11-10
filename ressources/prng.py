#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####### - Usefuls links
# https://cryptobook.nakov.com/secure-random-generators/secure-random-generators-csprng
# https://en.wikipedia.org/wiki/List_of_random_number_generators

import os
from .bytesManager import bytes_to_int, circularRotation, int_to_bytes, int_to_bits, bytes_needed
from ressources.utils import millerRabin

def xorshiftperso(evenOrodd=0,nBits:int=512):
    '''
    xorshift perso

    nBits : number of bits needed (e.g 2048 bits to output 2048 bits lenght's number).

    return even or odd number:
         - 0 odd
         - 1 even
    '''

    bytes=int(nBits/8)

    # Unpredictable random seed 
    state1,state2=os.urandom(bytes),os.urandom(bytes)


    a,b = bytes_to_int(state1),bytes_to_int(state2)
    
    a ^= bytes_to_int(circularRotation(state1,0,23))
    b ^= bytes_to_int(circularRotation(state2,1,17))

    # Generate full bytes of 1 of the size of the array
    size = int("0x" + "".join(["FF" for _ in range(0,nBits)]),16)
    # For n bits
    a &= size
    b &= size
    
    r=b+a


    if evenOrodd and r & 1 :
        # Bitwsing and with "-2" (number with all bits set to one except lowest one)
        # always kills just the LSB of your number and forces it to be even
        r&=-2
    elif not evenOrodd and not (r & 1):
        # Force the number to the next odd
        r|=1
    
    return r


def randomPrime(nBits:int=512,condition=True,k:int=1):
    """
    Generates prime numbers with bitlength nBits.
    Stops after the generation of k prime numbers.

    You can verify a condition with condition method.
    """
    
    # Generate random odd number of nBits
    maybe=xorshiftperso(0,nBits)
    b=k
    primes=[]

    while k>0:
        if millerRabin(maybe) and condition(maybe):
            primes.append(maybe)
            k-=1
        maybe=xorshiftperso(0,nBits)

    if b:
        return primes[0]
    else:
        return primes
    

def safePrime(nBits:int=1024):
    """
    A number p is a sage prime if both p and (p-1)/2 are prime.

    nBits: number of bits wanted for output prime number.

    Based on:
    https://eprint.iacr.org/2003/186.pdf

    The primes to be generated need to be 1024 bit to 2048 bit long for good cryptographical uses.
    """

    p_filter = lambda p : p % 3 == 2

    while 1:
        p = randomPrime(nBits,p_filter)

        if millerRabin(2*p+1):
            return p