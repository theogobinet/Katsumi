#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ressources.multGroup as multGroup
import ressources.utils as ut
import ressources.interactions as it

import random as rd

#####################################################################
# Diffie–Hellman key exchange is a method of securely exchanging cryptographic keys over a public channel 
####################################################################

##### - Normal DH

# 1)
def agreement(n:int=2048,fountain=True):
    """
    Alice and Bob publicly agree to use a modulus p and a primitive root g modulo p.
    """

    if fountain:
        p,_ = it.extractSafePrimes(n,False)
    else:
        it.stockSafePrimes(n,1)
        return agreement(n,True)

    return (p,multGroup.primitiveRoot(p))

# 2) and 3)
def chooseAndSend(accord:tuple,secret=None,n:int=2048):
    """
    Choose a secret integer randomly and send a ciphered result to someone.

    n number of bits choosen for generating the integer randomly.
    """
    
    p,g = accord

    if not secret:
        i = rd.randrange(2,n)
        print(f"This is your secret integer, keep it safe: {i}")
    else:
        i = secret

    toSend = ut.square_and_multiply(g,i,p)

    print(f"Here's what to send to the other one: {toSend}")

    input("Is everything good ? (please tap enter for next)")

    return toSend

# 4) and 5)
def compute(accord:tuple,secret_int=None):

    if not secret_int:
        secret_int = it.getInt(rd.randrange(2,accord[0]),"your secret integer",False,accord[0])
    
    sended = it.getInt(rd.randrange(2,accord[0]),"his secret integer",False,accord[0])

    shared_secret = ut.square_and_multiply(sended,secret_int,accord[0])

    return shared_secret

# Only a and b are kept secret


# - ECDH 


# Here we'll use ECC https://en.wikipedia.org/wiki/Elliptic-curve_cryptography
# ECC requires a smaller key as compared to non-ECC cryptography to provide equivalent security 
# (a 256-bit ECC security has an equivalent security attained by 3072-bit RSA cryptography).

# To avoid these vulnerabilities, the Logjam authors recommend use of elliptic curve cryptography,
# for which no similar attack is known. Failing that, they recommend that the order, 
# p, of the Diffie–Hellman group should be at least 2048 bits.



