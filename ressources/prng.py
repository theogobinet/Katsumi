#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####### - Usefuls links
# https://cryptobook.nakov.com/secure-random-generators/secure-random-generators-csprng
# https://en.wikipedia.org/wiki/List_of_random_number_generators

import os
from .bytesManager import bytes_to_int, circularRotation, int_to_bytes, int_to_bits, bytes_needed
from ressources.utils import millerRabin
from secrets import randbits, SystemRandom

def xorshiftperso(evenOrodd=0,nBits:int=512):
    '''
    xorshift perso

    nBits : number of bits needed (e.g 2048 bits to output 2048 bits lenght's number).

    return even or odd number:
         - 0 odd
         - 1 even
         - both
    '''
    assert nBits > 23 
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


def randomInt(evenOrodd:int=0,n:int=512):
    """
    Return a random integer using secrets module.
    
    For even or odd number:
         - 0 odd
         - 1 even
         - 2 both
    """
    r=randbits(n)

    if evenOrodd and r & 1 :
        # Bitwsing and with "-2" (number with all bits set to one except lowest one)
        # always kills just the LSB of your number and forces it to be even
        r&=-2
    elif not evenOrodd and not (r & 1):
        # Force the number to the next odd
        r|=1
    
    return r

def randomPrime(nBits:int=512,gen=randomInt,condition = lambda p : p == p,k:int=1):
    """
    Generates prime numbers with bitlength nBits.
    Stops after the generation of k prime numbers.

    You can verify a condition with condition method.
    """

    # Generate random odd number of nBits
    assert nBits > 0 and nBits < 4096

    maybe=gen(0,nBits)

    b=k
    primes=[]

    while k>0:
        if millerRabin(maybe) and condition(maybe):
            primes.append(maybe)
            k-=1
        maybe=gen(0,nBits)

    if b:
        return primes[0]
    else:
        return primes
    

def safePrime(nBits:int=1024):
    """
    The number 2p + 1 associated with a Sophie Germain prime is called a safe prime.
    In number theory, a prime number p is a Sophie Germain prime if 2p + 1 is also prime

    nBits: number of bits wanted for output prime number.

    Based on:
    https://eprint.iacr.org/2003/186.pdf

    The primes to be generated need to be 1024 bit to 2048 bit long for good cryptographical uses.

    Return (safe_prime,sophieGermain_prime) tuple's
    """

    p_filter = lambda p : p % 3 == 2

    while 1:
        sophieGermain_prime = randomPrime(nBits,randomInt,p_filter)
        safe_prime = 2 * sophieGermain_prime + 1
        if millerRabin(safe_prime):
            return (safe_prime,sophieGermain_prime)