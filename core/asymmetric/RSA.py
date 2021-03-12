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


def key_gen(size: int = 2048,
            randomFunction=None,
            saving=False,
            Verbose=False):
    """
    RSA key generation.

    n: number of bits for safe prime generation.\n

    randomFunction: prng choosen for random prime number generation (default = randbits from secrets module).

    As a transitional measure, the use of RSA-based signature and confidentiality mechanisms with a key size of at least 2000 bits remain conform for the year 2023.

    saving: True if you want to save the private key to a file.
    """

    sizeB = size // 2

    # 1- Choose two distinct prime numbers p and q

    if Verbose:
        print(
            f"Let's try to generate two distinct prime numbers p and q of {size} bits."
        )

    p, q = prng.randomPrime(sizeB, randomFunction,
                            Verbose=Verbose), prng.randomPrime(sizeB,
                                                               randomFunction,
                                                               Verbose=Verbose)

    # 2- Compute n = pq.
    n = p * q  # new modulus

    # 3- Compute λ(n), where λ is Carmichael's totient function.
    # since p and q are prime, λ(p) = φ(p) = p − 1 and likewise λ(q) = q − 1. Hence λ(n) = lcm(p − 1, q − 1).
    carmichaelTotient = ut.lcm(p - 1, q - 1)

    # 4- Choosing e, part of the public key
    e = rd.randrange(1, carmichaelTotient)

    while not ut.coprime(
            e, carmichaelTotient) or bm.hammingWeight(e) > (0.995 * sizeB):
        e = rd.randrange(1, carmichaelTotient)
        #e having a short bit-length and small Hamming weight results in more efficient encryption
        #https://en.wikipedia.org/wiki/Hamming_weight

    # 5- Chossing d, modular multiplicative inverse of e modulo carmichaelTotient(n)
    d = multGroup.inv(e, carmichaelTotient)  # Private Key exponent

    #  p, q, and λ(n) must also be kept secret because they can be used to calculate d. In fact, they can all be discarded after d has been computed.
    del p, q, carmichaelTotient

    public_key, private_key = (n, e), (n, d)

    if saving:
        public_key = it.writeKeytoFile(public_key, "public_key",
                                       config.DIRECTORY_PROCESSING, ".kpk")
        it.writeKeytoFile(private_key, "private_key",
                          config.DIRECTORY_PROCESSING, ".kpk")

    if Verbose:
        print(
            "\nYour private key has been generated Bob, keep it safe and never distibute them !"
        )
        print("\nThe public key has been generated, send this to your Alice: ",
              end="")

        it.prGreen(public_key)

    if not saving:
        return (public_key, private_key)


#############################################
############# - Encryption - ################
#############################################


def encrypt(M: bytes, publicKey, saving: bool = False):
    """
    Encrypt a message M to make him sendable.
    """

    assert isinstance(M, bytes)

    n, e = publicKey

    def process(m):
        return ut.square_and_multiply(m, e, n)

    # First, turn M into int
    Mint = bm.bytes_to_int(M)

    if Mint < n:
        # That's a short message
        m = Mint
        e = process(m)

    else:
        # M is a longer message, so it's divided into blocks
        size = (it.getKeySize(publicKey) // 8) - 1

        e = [process(bm.bytes_to_int(elt)) for elt in bm.splitBytes(M, size)]

    if saving:
        e = it.writeKeytoFile(e, "encrypted", config.DIRECTORY_PROCESSING,
                              ".kat")

    return e


#############################################
############# - Decryption - ################
#############################################


def decrypt(c, privateKey: tuple, asTxt=False):
    """
    Decryption of given ciphertext 'c' with secret key 'privateKey'. 
    Return bytes/bytearray or txt if asTxt set to 'True'.
    """

    n, d = privateKey

    def process(cipherT):
        un = ut.square_and_multiply(cipherT, d, n)
        return bm.mult_to_bytes(un)

    if isinstance(c, list):

        decrypted = [process(elt) for elt in c]

        r = bm.packSplittedBytes(decrypted)

    else:
        r = process(c)

    if asTxt:
        return r.decode()
    else:
        return r


#############################################################
################ - Signature scheme - #######################
#############################################################


def signing(M: bytes,
            privateK: tuple = None,
            saving: bool = False,
            Verbose: bool = False):
    """
    Signing the message (M).
    You need to attach this signature to the message. 
    """

    assert isinstance(M, bytes)

    from ..hashbased import hashFunctions as hashF

    if not privateK:
        privateK = it.extractKeyFromFile("private_key")

    size = it.getKeySize(privateK)  # Get key size

    if Verbose:
        print("Hashing in progress...")

    hm = hashF.sponge(M, size)
    #base64 to int
    hm = bm.bytes_to_int(bm.mult_to_bytes(hm))

    if Verbose:
        print(f"hm = {hm}")
        print("Hashing done.\n")

    # raises it to the power of d (modulo n)
    # same thing as decrypting
    n, d = privateK
    sign = ut.square_and_multiply(hm, d, n)

    if saving:
        sign = it.writeKeytoFile(sign, "RSA_signature")

    return sign


def verifying(M: bytes, sign: int, pK: tuple = None):
    """
    Verify given signature of message M with corresponding public key's.
    """

    assert isinstance(M, bytes) or isinstance(M, bytearray)

    from ..hashbased import hashFunctions as hashF

    if not pK:
        pK = it.extractKeyFromFile("public_key")

    size = it.getKeySize(pK)

    hm = hashF.sponge(M, size)
    # base64 to int
    hm = bm.bytes_to_int(bm.mult_to_bytes(hm))

    # If the signature is in base64
    if not isinstance(sign, int):
        sign = it.getIntKey(sign)

    n, e = pK
    # raises the signature to the power of e (modulo n)
    # (as when encrypting a message)
    if sign > n:
        print("Signature > modulus")

    test = ut.square_and_multiply(sign, e, n)

    if test == (hm % n):
        return True
    else:
        return False
