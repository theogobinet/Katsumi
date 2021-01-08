#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ressources.prng as prng
import ressources.utils as ut
import ressources.bytesManager as bm
import ressources.interactions as it
import ressources.multGroup as multGroup
import ressources.config as config

import random as rd

# The RSA algorithm involves four steps: key generation, key distribution, encryption, and decryption.

#############################################
########### - Key Generation - ##############
#############################################

def key_gen(size:int=2048,randomFunction=None,saving=False,Verbose=False):
    """
    RSA key generation.

    n: number of bits for safe prime generation.\n

    randomFunction: prng choosen for random prime number generation (default = randbits from secrets module).

    saving: True if you want to save the private key to a file.
    """

    # 1- Choose two distinct prime numbers p and q

    if Verbose: print(f"Let's try to generate two distinct prime numbers p and q of {size} bits.")

    p,q = prng.randomPrime(size//2,randomFunction,Verbose=Verbose),prng.randomPrime(size//2,randomFunction,Verbose=Verbose)

    # 2- Compute n = pq.
    n = p*q # new modulus

    # 3- Compute λ(n), where λ is Carmichael's totient function.
    # since p and q are prime, λ(p) = φ(p) = p − 1 and likewise λ(q) = q − 1. Hence λ(n) = lcm(p − 1, q − 1).
    carmichaelTotient = ut.lcm(p-1,q-1)

    e = rd.randrange(1,carmichaelTotient)

    while not ut.coprime(e,carmichaelTotient):
        e = rd.randrange(1,carmichaelTotient)
    
    #https://en.wikipedia.org/wiki/Hamming_weight






#############################################
############# - Encryption - ################
#############################################


#############################################
############# - Decryption - ################
#############################################

