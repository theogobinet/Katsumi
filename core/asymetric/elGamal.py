#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ressources.prng import safePrime
from ressources.utils import square_and_multiply, euclid
from random import randrange as rd

import ressources.bytesManager as bm
import ressources.interactions as it



# ElGamal encryption consists of three components: the key generator, the encryption algorithm, and the decryption algorithm.


def mapper(msg,pKey):
    """
    Reversible mapping function for msg using map.

    Based on the XOR property:
        C = A ^ B 
        C ^ B = A
    e.g: mapping a message M to an element m of G.
    """

    # B creation
    B=0
    for i,e in enumerate(pKey):
        j=int((i+1)%len(pKey))
        B+=e^pKey[j]

    return (msg ^ B)

#############################################
########### - Key Generation - ##############
#############################################


def findGen(p,q):
    """
    Easy way of selecting a random generator :
    select a random value h between 2 and p−1

    p: Safe prime
    q: Sophie Germain prime

    ---> g^q mod p is equal to 1

    ---> Since the ordrer of G is prime, any element of G (except 1) is a generator

    NB: g is assumed to be known by all attackers.
    """
    computed = square_and_multiply(rd(2,p-1),int((p-1)/q),p)

    # If it's not one, it's the gen !
    while computed == 1:
        computed = square_and_multiply(rd(2,p-1),int((p-1)/q),p)
    
    return computed

def key_gen(n:int=512):
    """
    ElGamal key generation.

    n: number of bits for safe prime generation.
    """
    s=safePrime(n)

    p,q=s[0],s[1] # safe_prime and Sophie Germain prime
    gen=findGen(p,q)

    # The description of the group is (g,q,p)
    # When p=2q+1, they are the exact same group as Gq.
    # This means, by using Gq, you don't have to worry about an adversary testing if certain numbers are quadratic residues or not.
    
    private_key = rd(1,q-1) # gcd(private_key,q) = 1

    h = square_and_multiply(gen,private_key,p)

    import base64
    to64 = lambda x : base64.b64encode(bm.int_to_bytes(x))

    private_key = to64(private_key)
    input(f"This is your private key Alice, keep it safe: {private_key}")

    # The public key consists of the values (G,q,g,h).
    public_key = (p,q,gen,h)
    it.writeVartoFile(public_key,"public_key")

    print(f"The public key : {public_key} has been generated and saved.")

    return None

        



#############################################
########### -   Encryption   - ##############
#############################################

def encrypt(msg,pKey=it.extractVarFromFile("public_key")):

    p,q,g,h = pKey[0],pKey[1],pKey[2],pKey[3]

    mapped = mapper(msg,pKey) # (G,q,g,h)

    y=rd(1,q-1)

    







#############################################
########### -   Decryption   - ##############
#############################################





