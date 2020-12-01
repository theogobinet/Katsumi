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
    Find a generator g such as g order is q (Sophie Germain prime) with p = 2q + 1.
    That's a generator for Gq. Not Zp* and any other subgroup. Very important point.

    Avoid commons attacks.
    """
    assert p == 2*q +1

    while 1:

        # Choose a random quadratic residues, thus is multiplicative order will be q.
        # Without 0 and 1 to keep only legender symbol = 1 results
        
        e = rd.randrange(2,p)
        g = ut.square_and_multiply(e,e,p)



        # We must avoid g=2 because of Bleichenbacher's attack described
        # in "Generating ElGamal signatures without knowning the secret key",
        # 1996

        if g in (1,2):
            continue

        #Discard g if it divides p-1
        elif (p-1) % g == 0:
            continue


        # g^{-1} must not divide p-1 because of Khadir's attack
        # described in "Conditions of the generator for forging ElGamal
        # signature", 2011

        elif (p-1) % multGroup.inv(g,p) == 0:
            continue

        # Found a good candidate
        return g


def isEasyGeneratorPossible(s:tuple):
    """
    Return True is it's possible to generate easly a generator.
    """
    # Control if easy generator is possible 
    p_filter = lambda p : p % 3 == 2 and (p % 12 == 1 or p % 12 == 11)

    p,_ = s
    
    if p_filter(p):
        easyGenerator = True
    else:
        easyGenerator = False

    return easyGenerator

#############################################
########### - Key Generation - ##############
#############################################


def key_gen(n:int=2048,primeFount=None,easyGenerator:bool=False,randomFunction=None,Verbose=False):
    """
    ElGamal key generation.

    n: number of bits for safe prime generation.\n

    primeFount = prime number's fountain used, put tuple of primes into this variable.\n

    easyGenerator: generate appropriated safe prime number according to quadratic residues properties.\n

    randomFunction: prng choosen for random prime number generation (default = randbits from secrets module).
    """

    import ressources.config as config

    if not primeFount:

        if Verbose: print(f"Let's try to generate a safe prime number of {n} bits.")

        s = prng.safePrime(n,randomFunction,easyGenerator,Verbose)
        p,q = s # safe_prime and Sophie Germain prime
    
    else:
        primeFount = it.extractSafePrimes(n,False)
        s = primeFount
        p,q = s # safe_prime and Sophie Germain prime


    if Verbose: print(f"Let's find the generator for p: {p} , safe prime number.")

    # Generate an efficient description of a cyclic group G, of order q with generator g.
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
    it.writeVartoFile(private_key,"private_key",config.DIRECTORY_PROCESSING)

    print(f"\nYour private key has been generated Alice, keep it safe !")


    # The public key consists of the values (G,q,g,h).
    public_key = (p,q,gen,h)
    it.writeVartoFile(public_key,"public_key",config.DIRECTORY_PROCESSING)

    print(f"\nThe public key has been generated too and saved.")

    return None


def getSize():
    """
    Return size of current key based on prime fount's.
    """
    from ressources import config as config 

    sizes = [int(elt.split("_")[0]) for elt in it.whatInThere()]
    
    pK = it.extractVarFromFile("public_key",config.DIRECTORY_PROCESSING)

    bits = bm.bytes_needed(pK[0])*8

    return ut.closestValue(bits,sizes)

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

        e = process(m)

    else:
        # M is a longer message, so it's divided into blocks
        # You need to choose a different y for each block to prevent
        # from Eve's attacks.

        e = [process(bm.bytes_to_int(elt)) for elt in bm.splitBytes(M,1)]

    import ressources.config as config

    it.writeVartoFile(e,"encrypted",config.DIRECTORY_PROCESSING)

    return e

#############################################
########### -   Decryption   - ##############
#############################################

def decrypt(ciphertext,sK,asTxt=False):

    x,p = sK[-1],sK[0]

    def process(cipherT):
        c1,c2 = cipherT

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


def delog(publicKey,encrypted=None,asTxt=False,method=1):
    """
    Retrieve private key with publicKey.
    And if you get the encrypted message, thus you can decrypt them.
    """

    def dlog_get_x(publicKey):
        """
        Find private key using discrete logarithmic method.
        """
        
        # PublicKey format : (p,q,gen,h)
        p,q,g,h = publicKey

        x = ut.discreteLog(g,h,p,method)

        # Same format as private key
        return (p,q,g,x)

    private_Key = dlog_get_x(publicKey)

    if encrypted == None:
        return private_Key

    else:
        return decrypt(encrypted,private_Key,asTxt)
        

    






    


