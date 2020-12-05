#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ressources.prng as prng
import ressources.utils as ut
import ressources.bytesManager as bm
import ressources.interactions as it
import ressources.multGroup as multGroup
import ressources.config as config

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


def key_gen(n:int=2048,primeFount=None,easyGenerator:bool=False,randomFunction=None,saving=False,Verbose=False):
    """
    ElGamal key generation.

    n: number of bits for safe prime generation.\n

    primeFount = prime number's fountain used, put tuple of primes into this variable.\n

    easyGenerator: generate appropriated safe prime number according to quadratic residues properties.\n

    randomFunction: prng choosen for random prime number generation (default = randbits from secrets module).
    """


    if not primeFount:

        if Verbose: print(f"Let's try to generate a safe prime number of {n} bits.")

        s = prng.safePrime(n,randomFunction,easyGenerator,Verbose)
        p,q = s # safe_prime and Sophie Germain prime
    
    else:
        primeFount = it.extractSafePrimes(n,False)
        s = primeFount
        p,q = s # safe_prime and Sophie Germain prime


    if Verbose: print(f"Let's find the generator for p: {p} , safe prime number.\n")

    # Generate an efficient description of a cyclic group G, of order q with generator g.
    if easyGenerator:
        # https://en.wikipedia.org/wiki/Quadratic_residue#Table_of_quadratic_residues
        if Verbose: print(f"Easy generator => gen = 12 (condition in prime generation) or (4,9) (for every prime)")

        gen = rd.choice([12,4,9])

    else:
        gen = generator(p,q)
    
    if Verbose: print(f"generator found : {gen}\n")
    

    # The description of the group is (g,q,p)
    # When p=2q+1, they are the exact same group as Gq.
    # The prime order subgroup has no subgroups being prime.
    # This means, by using Gq, you don't have to worry about an adversary testing if certain numbers are quadratic residues or not.
    
    # The message space MUST be restrained to this prime order subgroup.

    x = rd.randrange(1,p-1) # gcd(x,p) = 1

    h = ut.square_and_multiply(gen,x,p)

    # The private key consists of the values (G,x).
    private_key = (p,x)
    
    if saving:
        it.writeKeytoFile(private_key,"private_key",config.DIRECTORY_PROCESSING,".kpk")

    if Verbose:
        print(f"\nYour private key has been generated Alice, keep it safe !")


    # The public key consists of the values (G,q,g,h).
    # But we saved only (p,g,h) cause q = (p-1)//2

    public_key = (p,gen,h)
    
    if saving:
        public_key = it.writeKeytoFile(public_key,"public_key",config.DIRECTORY_PROCESSING,".kpk")

    if Verbose:
        print(f"\nThe public key '{public_key}' has been generated too.")
    
    if not saving:
        return (public_key,private_key)


def getSize(key:object="public_key"):
    """
    Return size of current key based on prime fount's.
    """

    sizes = [int(elt.split("_")[0]) for elt in it.whatInThere()]
    
    if isinstance(key,str):
        pK = it.extractKeyFromFile(key,config.DIRECTORY_PROCESSING,".kpk")
    else:
        pK = key

    bits = bm.bytes_needed(pK[0])*8

    return ut.closestValue(bits,sizes)

#############################################
########### -   Encryption   - ##############
#############################################

def encrypt(M:bytes,pKey,saving:bool=False):

    assert isinstance(M,bytes)

    p,g,h = pKey

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


    if saving:
        e = it.writeKeytoFile(e,"encrypted",config.DIRECTORY_PROCESSING,".kat")

    return e

#############################################
########### -   Decryption   - ##############
#############################################

def decrypt(ciphertext,sK:tuple,asTxt=False):

    p,x = sK

    def process(cipherT):
        c1,c2 = cipherT

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
################ - signature scheme - #######################
#############################################################

def signing(M:bytes,tupleOfKeys:tuple=None,verifying=None,saving:bool=False,Verbose:bool=False):
    """
    Signing a message M (bytes)
    tupleOfKeys <= (public_key,private_key)

    veriying: enter the tuple to verify.
    The signature is valid if and only if g^(H(m)) = (publicK)^s1 * s1^s2 mod p
    """

    from ..hashbased import hashFunctions as hashF

    # y choosed randomly between 1 and p-2 with condition than y coprime to p-1
    if not tupleOfKeys:
        tupleOfKeys = (it.extractKeyFromFile("public_key"),it.extractKeyFromFile("private_key"))
        
    p,g,h = tupleOfKeys[0] #public key
    p,x = tupleOfKeys[-1] #private key
    size = getSize(tupleOfKeys[0])

    # M = bm.fileToBytes(M)
    # M = "Blablabla".encode()

    if Verbose: print("Hashing in progress...")

    hm = 7
    # hm = hashF.sponge(M,size)
    # #base64 to int
    # hm = bm.bytes_to_int(bm.mult_to_bytes(hm))

    if Verbose: print("Hashing done.\n")

    if verifying :
        
        if not isinstance(verifying,tuple):
            b64data = verifying
            verifying = it.getIntKey(b64data[1:], b64data[0])

        s1,s2 = verifying

        if ((0 < s1 < p) and (0 < s2 < p-1)):

            test1 = ut.square_and_multiply(h,s1,p) * ut.square_and_multiply(s1,s2,p)
            test2 = ut.square_and_multiply(g,hm,p)

            print(test1,test2)

            if test1 == test2:
                return True
            else:
                return False
        else:
            raise ValueError

    else:
        import random as rd

        p1 = p-1

        # k= rd.randrange(2,p-2)

        # while not ut.coprime(k,p1):
        #     k = rd.randrange(1,p-2)

        k = 5

        if Verbose: print(f"Your secret integer is: {k}")

        s1 = ut.square_and_multiply(g,k,p)

        from ressources.multGroup import inv

        s2 = (inv(k,p1) * (hm - x*s1)) % p1

        # In the unlikely event that s2 = 0 start again with a different random k.

        if s2 == 0:
            if Verbose: print(f"Unlikely, s2 is equal to 0. Restart signing...")
            signing(M,tupleOfKeys,None,saving,Verbose)
        else:
            sign = (s1,s2)
            
            if saving:
                sign = it.writeKeytoFile(sign,"elG_signature")

            return sign


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
        

    






    


