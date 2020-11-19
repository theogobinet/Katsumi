#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ressources.prng as prng
import ressources.utils as ut
import ressources.bytesManager as bm
import ressources.interactions as it
import ressources.multGroup as multGroup

import random as rd

#############
# ElGamal encryption consists of three components: the key generator, the encryption algorithm, and the decryption algorithm.

# Like most public key systems, the ElGamal cryptosystem is usually used as part of a hybrid cryptosystem where
# the message itself is encrypted using a symmetric cryptosystem and ElGamal is then used to encrypt only the symmetric key.
############

def generator(p:int,q:int):
    """
    Find a generator g such as g order's is q (Sophie Germain prime) with p = 2q + 1.

    Avoid commons attacks.
    """

    assert p == 2*q +1


    # Removing 0 and  1 to keep only legender symbol = 1 results
    qResidues = multGroup.quadraticsResidues(p)[2:]

    ################################################################
    ###################- Attacks protection's -#####################
    ################################################################

    # We must avoid g=2 because of Bleichenbacher's attack described
    # in "Generating ElGamal signatures without knowning the secret key",
    # 1996
    if 2 in qResidues:
        qResidues.remove(2)

    # Discard g if it divides (p-1)

    qResidues = [e for e in qResidues if (p-1)%e != 0 and (p-1) % multGroup.inv(e,p) != 0]

    # g^{-1} must not divide p-1 because of Khadir's attack
    # described in "Conditions of the generator for forging ElGamal
    # signature", 2011

    # Choose a random quadratic residues, thus is multiplicative order will be q.
    return rd.choice(qResidues)

#############################################
########### - Key Generation - ##############
#############################################


def key_gen(n:int=512,easyGenerator:bool=False,randomFunction=None,Verbose=False):
    """
    ElGamal key generation.

    n: number of bits for safe prime generation.

    easyGenerator: generate appropriated safe prime number according to quadratic residues properties.

    randomFunction: prng choosen for random prime number generation (default = randbits from secrets module).
    """

    if Verbose: print(f"Let's try to generate a safe prime number of {n} bits.")

    s = prng.safePrime(n,randomFunction,easyGenerator,Verbose)

    p,q=s[0],s[1] # safe_prime and Sophie Germain prime
    
    if Verbose:
        print(f"Let's find the generator for p: {p} , safe prime number.")

    if easyGenerator:
        # https://en.wikipedia.org/wiki/Quadratic_residue#Table_of_quadratic_residues
        if Verbose: print(f"Easy generator => gen = 12 (condition in prime generation) or (4,9) (for every prime)")
        gen = rd.choice([12,4,9])

    else:
        gen = generator(p,q)
    

    # The description of the group is (g,q,p)
    # When p=2q+1, they are the exact same group as Gq.
    # The prime order subgroup has no subgroups being prime.
    # This means, by using Gq, you don't have to worry about an adversary testing if certain numbers are quadratic residues or not.
    
    # The message space MUST be restrained to this prime order subgroup.

    x = rd.randrange(1,p-1) # gcd(x,p) = 1

    h = ut.square_and_multiply(gen,x,p)

    # The private key consists of the values (G,q,g,x).
    private_key = (p,q,gen,x)
    it.writeVartoFile(private_key,"private_key")

    print(f"\nYour private key has been generated Alice, keep it safe !")


    # The public key consists of the values (G,q,g,h).
    public_key = (p,q,gen,h)
    it.writeVartoFile(public_key,"public_key")

    print(f"\nThe public key : {public_key} has been generated too and saved.")

    return None

        
#############################################
########### -   Encryption   - ##############
#############################################

def encrypt(M:bytes,pKey):

    assert isinstance(M,bytes)

    p,g,h = pKey[0],pKey[2],pKey[3]

    def process(m):
        y = rd.randrange(1,p-1)

        # shared secret -> g^xy
        c1 = ut.square_and_multiply(g,y,p) 

        s = ut.square_and_multiply(h,y,p) 
        c2 = (m*s)%p

        return (c1,c2)

    if bm.bytes_to_int(M) <= p-1:
        # That's a short message
        m=bm.bytes_to_int(M)
        print(m)
        return process(m)

    else:
        # M is a longer message, so it's divided into blocks
        # You need to choose a different y for each block to prevent
        # from Eve's attacks.

        return [process(bm.bytes_to_int(elt)) for elt in bm.splitBytes(M,1)]

#############################################
########### -   Decryption   - ##############
#############################################

def decrypt(ciphertext,sK,asTxt=False):

    x,p = sK[-1],sK[0]

    def process(cipherT):
        c1,c2 = cipherT[0],cipherT[-1]

        s = ut.square_and_multiply(c1,x,p)
        #s1 = multGroup.inv(s,p)
        s1 = ut.square_and_multiply(c1,p-1-x,p)

        # This calculation produces the original message
        m = (c2 * s1) % p

        return bm.int_to_bytes(m)
    
    if isinstance(ciphertext,list):
        
        decrypted=[process(elt) for elt in ciphertext]

        r = bm.packSplittedBytes(decrypted)

    else:
        r = process(ciphertext)

    if asTxt:
        return r.decode()
    else:
        return r


#############################################################
################ - Logarithmic attack - #####################
#############################################################




