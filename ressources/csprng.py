#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####### - Usefuls links
# https://cryptobook.nakov.com/secure-random-generators/secure-random-generators-csprng
# https://en.wikipedia.org/wiki/List_of_random_number_generators

import os
from .bytesManager import bytes_to_int, circularRotation, int_to_bytes, int_to_bits, bytes_needed


def xorshiftperso(nBits:int=256):
    '''
    xorshift perso

    nBits : number of bits needed (e.g 256 bits to output 256 bits lenght's number).

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

    if bytes_needed(r) < bytes:
        return xorshiftperso(nBits)
    else:
        return r

    
    