#!/usr/bin/env python3
# -*- coding: utf-8 -*-

######################################################################
# Digital Signature - https://en.wikipedia.org/wiki/Digital_signature
######################################################################

from numpy.lib.arraysetops import isin
from . import hashFunctions as hashF
from ressources import multGroup as multG
from ressources import utils as ut
from ressources import interactions as it
from ressources import bytesManager as bm
from ressources import config as config

def elG_signing(M,tupleOfKeys=None,verifSign=None,saving=False,Verbose:bool=False):
    """
    Signing a message M.
    tupleOfKeys <= (public_key,private_key)

    verifSign: enter the tuple to verify.
    The signature is valid if and only if g^(H(m)) = (publicK)^s1 * s1^s2 mod p
    """
    from core.asymmetric import elGamal as elG
    
    # If keys are not generated, then generate one with 2048 bits.
    if not it.isFileHere("public_key.kpk",config.DIRECTORY_PROCESSING) or not it.isFileHere("public_key.kpk",config.DIRECTORY_PROCESSING):
        if Verbose: print(f"\nOne key is at least missing. Generating now...")
        elG.key_gen(primeFount=True)

    
    M = bm.fileToBytes(M)
    
    if Verbose: print("Hashing in progress...")
    hm = hashF.sponge(M,elG.getSize())
    if Verbose: print("Hashing done.\n")

    # y choosed randomly between 1 and p-2 with condition than y coprime to p-1
    if tupleOfKeys:
        p,_,g,x = tupleOfKeys[-1] #private key
        _,_,_,h = tupleOfKeys[0] #public key
    else:
        p,_,g,x = it.extractKeyFromFile("private_key")
        _,_,_,h = it.extractKeyFromFile("public_key")

    if verifSign :
        
        if not isinstance(verifSign,tuple):
            b64data = verifSign
            verifSign = it.getIntKey(b64data[1:], b64data[0])

        s1,s2 = verifSign

        if Verbose:
            print(f"s1 = {s1} \n s2 = {s2}")
            print(f"p = {p}")

        if ((0 < s1 < p) and (0 < s2 < p-1)):

            test1 = ut.square_and_multiply(h,s1,p) * ut.square_and_multiply(s1,s2,p)
            test2 = ut.square_and_multiply(g,hm,p)

            if test1 == test2:
                return True
            else:
                return False
        else:
            raise ValueError

    else:
        import random as rd

        p1 = p-1

        k= rd.randrange(2,p-2)

        while not ut.coprime(k,p1):
            k = rd.randrange(1,p-2)

        if Verbose: print(f"Your secret integer is: {k}")

        s1 = ut.square_and_multiply(g,k,p)

        inv = multG.inv(k,p1)
        #base64 to int
        hm = bm.bytes_to_int(bm.mult_to_bytes(hm))

        s2 = (inv * (hm - x*s1)) % p1

        # In the unlikely event that s2 = 0 start again with a different random k.

        if s2 == 0:
            if Verbose: print(f"Unlikely, s2 is equal to 0. Restart signing...")
            elG_signing(M,None,saving,Verbose)
        else:
            sign = (s1,s2)
            
            if saving:
                sign = it.writeKeytoFile(sign,"elG_signature")

            return sign
