#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####### - Usefuls links
# https://cryptobook.nakov.com/secure-random-generators/secure-random-generators-csprng
# https://en.wikipedia.org/wiki/List_of_random_number_generators

import os
from .bytesManager import bytes_to_int, circularRotation, bytes_needed
from ressources.utils import millerRabin
from secrets import randbits

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



def randomPrime(nBits:int=512,gen=randomInt,condition = lambda p : p == p,k:int=1,Verbose=False):
    """
    Generates prime numbers with bitlength nBits.
    Stops after the generation of k prime numbers.

    You can verify a condition with condition method.
    """

    # Generate random odd number of nBits
    assert nBits >= 8 and nBits <= 4096

    def find(Verbose:bool):
        maybe=gen(0,nBits)

        if Verbose:
            print("Finding one who respect given condition(s).")

        while not condition(maybe):
            maybe=gen(0,nBits)

        if Verbose:
            print("Found !")
        return maybe
    
    maybe = find(Verbose)

    b=k
    primes=[]

    while k>0:

        if millerRabin(maybe):
            primes.append(maybe)
            k-=1

        maybe = find(Verbose)

    if b:
        return primes[0]
    else:
        return primes
    

def safePrime(nBits:int=1024,randomFunction=None,easyGenerator=False,Verbose=False):
    """
    The number 2p + 1 associated with a Sophie Germain prime is called a safe prime.
    In number theory, a prime number p is a Sophie Germain prime if 2p + 1 is also prime

    nBits: number of bits wanted for output prime number.

    Based on:
    https://eprint.iacr.org/2003/186.pdf

    The primes to be generated need to be 1024 bit to 2048 bit long for good cryptographical uses.

    Return (safe_prime,sophieGermain_prime) tuple's
    """
    if easyGenerator:
        if Verbose:
            print("Easy generator choosen.")
        p_filter = lambda p : p % 3 == 2 and (p % 12 == 1 or p % 12 == 11)# p = 1 mod 12 make 11 as primitive root
    else:
        p_filter = lambda p : p % 3 == 2
        
    while 1:

        if randomFunction == None:
            randomFunction = randomInt

        sophieGermain_prime = randomPrime(nBits,randomFunction,p_filter,1)
        safe_prime = 2 * sophieGermain_prime + 1
        #bits = bytes_needed(safe_prime)*8

        if Verbose:
            print(f"Sophie Germain Prime {sophieGermain_prime} candidate's.")

        #if bits >= nBits and millerRabin(safe_prime):
        if millerRabin(safe_prime):
            return (safe_prime,sophieGermain_prime)
        else:
            if Verbose:
                print(f"But 2 * him + 1 doesn't seem to be prime...\n")
            continue




def genSafePrimes(n:int,L:list,nBits:int,randomFunction=None,easyGenerator=False,Verbose=False):
    """
    Generate n tuples of distincts safe primes number's and append them into a list L.
    """

    for _ in range(n):
        s = safePrime(nBits,randomFunction,easyGenerator,Verbose)
        if s not in L:
            L.append(s)
        else:
            continue

