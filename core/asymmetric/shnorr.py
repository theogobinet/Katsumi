#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ressources import utils as ut

#############
# Schnorr Signatures
# The standardized 64-byte Schnorr signature algorithm outlined in BIP-340 uses the same elliptic curce (secp256k1)
# as the traditional ECDSA signatures.
# In the Bitcoin specification of Schnorr signatures, the public key Q is 32 bytes and it can be converted from existing generated public keys by dropping the first byte (prefix).
#
# It's a multi-signature aggregation algorithm
# ==> The information of a single user is hidden in the multi-signature.
############

def schnorrTuple(nBits=256,r:int=2):
    """
    Find prime number p such as p = r*q + 1
    """
    from ressources import prng as prng

    while True:
        # For faster searching
        # Calculate rq +1 and (q-1)//r
        q = prng.randomPrime(nBits,prng.xorshiftperso)

        p1 = r * q + 1
        
        p2 = (q - 1) // r
        
        if ut.millerRabin(p1):
            return (q,p1)

        elif ut.millerRabin(p2):
            return (p2,q)

        else:
            continue









