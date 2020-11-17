#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ressources.prng import safePrime
import ressources.utils as ut
import ressources.bytesManager as bm
import ressources.interactions as it

import random as rd



#############
# ElGamal encryption consists of three components: the key generator, the encryption algorithm, and the decryption algorithm.

# Like most public key systems, the ElGamal cryptosystem is usually used as part of a hybrid cryptosystem where
# the message itself is encrypted using a symmetric cryptosystem and ElGamal is then used to encrypt only the symmetric key.
############

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
    Easy way of selecting a random generator of Z*p :
    select a random value h between 2 and p−1

    p: Safe prime
    q: Sophie Germain prime

    ---> g^q mod p is equal to 1

    ---> Since the ordrer of G is prime, any element of G (except 1) is a generator

    NB: g is assumed to be known by all attackers.
    """
    computed = ut.square_and_multiply(rd.randrange(2,p-1),int((p-1)/q),p)

    # If it's not one, it's the gen !
    while computed == 1:
        computed = ut.square_and_multiply(rd.randrange(2,p-1),int((p-1)/q),p)
    
    return computed

def key_gen(n:int=512,easyGenerator=False):
    """
    ElGamal key generation.

    n: number of bits for safe prime generation.
    """
    s=safePrime(n,easyGenerator)

    p,q=s[0],s[1] # safe_prime and Sophie Germain prime
    
    if easyGenerator:
        gen = 2
    else:
        gen=findGen(p,q)

    # The description of the group is (g,q,p)
    # When p=2q+1, they are the exact same group as Gq.
    # The prime order subgroup has no subgroups being prime.
    # This means, by using Gq, you don't have to worry about an adversary testing if certain numbers are quadratic residues or not.
    
    # The message space MUST be restrained to this prime order subgroup.

    x = rd.randrange(1,q-1) # gcd(x,q) = 1

    h = ut.square_and_multiply(gen,x,q)

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

def encrypt(M:bytes,pKey):

    assert isinstance(M,bytes)

    q,g,h = pKey[1],pKey[2],pKey[3]

    def process(m):
        y = rd.randrange(1,q-1)

        # shared secret -> g^xy
        s = ut.square_and_multiply(h,y,q) 
        c1 = ut.square_and_multiply(g,y,q) 
        c2 = (m*s)%q

        return (c1,c2)

    if bm.bytes_to_int(M) < q-1:
        # That's a short message
        m=bm.bytes_to_int(M)
        return process(m)

    else:
        # M is a longer message, so it's divided into blocks
        # You need to choose a different y for each block to prevent
        # from Eve's attacks.
        b = bm.bytes_needed(q-1)
        m = bm.splitBytes(M,b)

        return [process(bm.bytes_to_int(elt)) for elt in m]

#############################################
########### -   Decryption   - ##############
#############################################

def decrypt(ciphertext,sK):

    x,q = sK[-1],sK[1]

    def process(cipherT):
        c1,c2 = cipherT[0],cipherT[-1]

        s = ut.square_and_multiply(c1,x,q)
        s1 = ut.inv(s,q)

        # This calculation produces the original message
        m = c2 * s1

        return bm.int_to_bytes(m)
    
    if isinstance(ciphertext,list):
        
        decrypted=[process(elt) for elt in ciphertext]

        print(decrypted)
    
        return bm.packSplittedBytes(decrypted)
    else:
        return process(ciphertext)




