#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ressources.prng import safePrime
from ressources.utils import square_and_multiply, euclid, inv
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

    un,deux,trois=pKey[0],pKey[1],pKey[2]
    B=un^deux^trois

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
    
    x = rd(1,q-1) # gcd(x,q) = 1

    h = square_and_multiply(gen,x,p)

    # The private key consists of the values (G,q,g,x).
    private_key = (p,q,gen,x)
    it.writeVartoFile(private_key,"private_key")

    print(f"Your private key has been generated Alice, keep it safe !")


    # The public key consists of the values (G,q,g,h).
    public_key = (p,q,gen,h)
    it.writeVartoFile(public_key,"public_key")

    print(f"The public key : {public_key} has been generated too and saved.")

    return None

        



#############################################
########### -   Encryption   - ##############
#############################################

def encrypt(msg,pKey):

    p,q,g,h = pKey[0],pKey[1],pKey[2],pKey[3]

    #mapped = mapper(msg,pKey) # (p,q,g,h)

    y=rd(1,q-1)

    # In Zq
    #shared secret -> g^xy
    s=square_and_multiply(h,y,q)
    c1=square_and_multiply(g,y,q)
    c2=(msg*s)%q

    return (c1,c2)


#############################################
########### -   Decryption   - ##############
#############################################

def decrypt(ciphertext,sK):

    x,q=sK[-1],sK[1]

    c1,c2=ciphertext[0],ciphertext[-1]

    first = square_and_multiply(c1,x,q)
    inverse = inv(first,q)[0]

    m = (c2 * inverse) % q

    m = (square_and_multiply(c1,sK[0]-1-x,q)*c2)%q

    print("m : ",m)

    # c2/c1^x = (h^y.m)/(g^y)^x =(g^xy . m)/ g^xy = m
    return m




