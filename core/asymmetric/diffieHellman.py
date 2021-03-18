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
def agreement(n: int = 2048, fountain=True):
    """
    Alice and Bob publicly agree to use a modulus p and a primitive root g modulo p.
    """

    if fountain:
        p, _ = it.extractSafePrimes(n, False, Verbose=True)
        return (p, multGroup.primitiveRoot(p))

    it.stockSafePrimes(n, 1)
    return agreement(n, True)


# 2) and 3)
def chooseAndSend(
    accord: tuple, secret=None, n: int = 2048, saving=False, Verbose=False
):
    """
    Choose a secret integer randomly and send a ciphered result to someone.

    n number of bits choosen for generating the integer randomly.
    """

    p, g = accord

    if not secret:
        secret_integer = rd.randrange(2, n)
        if Verbose:
            print(f"This is your secret integer, keep it safe: {secret_integer}")
    else:
        secret_integer = secret

    toSend = ut.square_and_multiply(g, secret_integer, p)

    if saving:
        toSend = it.writeKeytoFile(toSend, "dH_sendable")

    if Verbose:
        print("Here's what to send to the other one: ", end="")
        it.prGreen(toSend)

    return secret_integer


# 4) and 5)
def compute(accord: tuple, L: list, saving=False):
    """
    accord <= common agreement
    L <= (secret_int, sended)
    """
    secret_int, sended = L

    shared_secret = ut.square_and_multiply(sended, secret_int, accord[0])

    if saving:
        return it.writeKeytoFile(shared_secret, "dH_shared_key")

    return shared_secret


# Only a and b are kept secret

# - ECDH
# Here we'll use ECC https://en.wikipedia.org/wiki/Elliptic-curve_cryptography
# ECC requires a smaller key as compared to non-ECC cryptography to provide equivalent security
# (a 256-bit ECC security has an equivalent security attained by 3072-bit RSA cryptography).

# To avoid these vulnerabilities, the Logjam authors recommend use of elliptic curve cryptography,
# for which no similar attack is known. Failing that, they recommend that the order,
# p, of the Diffie–Hellman group should be at least 2048 bits.
