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

    As a transitional measure, the use of RSA-based signature and confidentiality mechanisms with a key size of at least 2000 bits remain conform for the year 2023.

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

    # 4- Choosing e, part of the public key
    e = rd.randrange(1,carmichaelTotient)

    while not ut.coprime(e,carmichaelTotient):
        e = rd.randrange(1,carmichaelTotient)
        print(bm.hammingWeight(e))
        #e having a short bit-length and small Hamming weight results in more efficient encryption 
        #https://en.wikipedia.org/wiki/Hamming_weight

    # 5- Chossing d, modular multiplicative inverse of e modulo carmichaelTotient(n)
    d = multGroup.inv(e,carmichaelTotient) # Private Key exponent 

    #  p, q, and λ(n) must also be kept secret because they can be used to calculate d. In fact, they can all be discarded after d has been computed.
    del p,q,carmichaelTotient

    public_key,private_key = (n,e),d

    if saving:
        public_key = it.writeKeytoFile(public_key,"public_key",config.DIRECTORY_PROCESSING,".kpk")
        it.writeKeytoFile(private_key,"private_key",config.DIRECTORY_PROCESSING,".kpk")

    if Verbose:
        print(f"\nYour private key has been generated Bob, keep it safe and never distibute them !")
        print(f"\nThe public key has been generated, send this to your Alice : ",end="")

        it.prGreen(public_key)

    if not saving:
        return (public_key,private_key)


#############################################
############# - Encryption - ################
#############################################

def encrypt(M:bytes,pKey,saving:bool=False) -> int:
    """
    Encrypt a message M to make him sendable.
    """

    assert isinstance(M,bytes)

    n,e = pKey

    def process():
        print("coucou")

    # First, turn M into 
    Mint = bm.bytes_to_int(M)

    if Mint < n:
        # That's a short message
        m = Mint
        e = process(m)

    else:
        # M is a longer message, so it's divided into blocks
        print("cpoiu")

    if saving:
        e = it.writeKeytoFile(e,"encrypted",config.DIRECTORY_PROCESSING,".kat")

    return e

#############################################
############# - Decryption - ################
#############################################

