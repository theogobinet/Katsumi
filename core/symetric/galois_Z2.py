#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

import ressources.utils as utils
import ressources.config as config
import ressources.bytesManager as bm
import ressources.interactions as it

from math import floor

#### Operations

def poly_mult_2(a:int , b:int):
    '''
        Return binary multplication in Z2
    '''

    def multbiggest(a, b):
        
        r = 0
        for i in range(a.bit_length()):

            # (a >> i) & 1 -> Correspond to the bit i

            if (a >> i) & 1:

                # Adding result of ith multiplication
                r ^= (b << i)
        return r

    if a.bit_length() >= b.bit_length():
        return multbiggest(a, b)
    else:
        return multbiggest(b, a)

def poly_mult_mod_2(a:int, b:int, mod:int):
    '''
        Return the modular multiplication in Z2
    '''
    config.WATCH_MULT_NUMBER += 1
    exTime = time.time()

    result = poly_mod_2(poly_mult_2(a, b), mod)

    config.WATCH_GLOBAL_MULT += time.time() - exTime

    return result
    

def poly_mod_2(a:int, mod:int):
    '''
        Return polynomial "a" mod "mod"
    '''

    def rec (a:int, mod:int, c:int, m:int, degM:int, fullBits:int):
        '''
            Recursive function to compute overflowed bits
        '''
        # For each bit in poly a
        for i in range(a.bit_length()):

            # (a >> i) & 1 -> Correspond to the bit i
            if (a >> i) & 1:
                # If current bit greater than mod degree's
                if i >= degM:
                    if not m[i]:
                        # mod without most significant bit, shifted of current deg(a) - deg(mod) 
                        m[i] = (mod & fullBits) << (i - degM)

                    rec(m[i], mod, c, m, degM, fullBits)        
                else:
                    c[i] += 1

    if a.bit_length() < mod.bit_length():
        return a
    else:
        c = [0 for _ in range (mod.bit_length())]

        # Initialization of X^i results in mod
        m = [0 for _ in range (a.bit_length())]

        # degree of mod
        degM = mod.bit_length() - 1

        # int representing mod degree's - 1 full of "1" bits
        fullBits = int("".join(["1" for i in range (degM - 1)]), 2)

        rec(a, mod, c, m, degM, fullBits)
        
        for i in range(len(c)):
            c[i] = c[i] % 2
        return  int("".join([str(x) for x in reversed(c)]),2)

#######
def poly_exp_mod_2(P:int,exp:int,mod:int):
    """
    General method for fast computation of polynomials powers of a number.
    
    P: Polynomial
    exp: exposant
    mod: polynial to be coungruent to
    """
    if mod == 1:
        return 0

    res=1
    P=poly_mod_2(P,mod)

    while (exp>0) :
        if(exp%2==1):
            res=poly_mult_mod_2(P,res,mod)
        
        # Deleting LSB
        exp=floor((exp/2))
        # Updating P
        P=poly_mult_mod_2(P,P,mod)

    return res
#######
def gen_GL_2(poly,degree):
    """Return generator of Galois Field's GF(p^degree) based on primitive polynomial poly in Zn."""
    # Order of multiplicative subgroup
    pn1=(2**degree)-1
    if utils.millerRabin(pn1):
        q=[pn1]
    else:
        q=utils.findPrimeFactors(pn1)

    config.ELEMENTS=[i for i in range(2**degree)]
    genList=config.ELEMENTS

    goodGen=None

    for gen in genList:

        # α(x)^(p^n-1) % f(x) == 1
        firstTest=poly_exp_mod_2(gen,pn1,poly)

        if firstTest == 1:
            isGood=True 
            for elt in q:
                # α(x)^((p^n-1)/q) % f(x) != 1, for all q that are prime factors of p^n-1
                secondTest=poly_exp_mod_2(gen,pn1/elt,poly)

                # DO NOT REPLACE WITH 'if secondTest', i don't know why but it doesn't work otherwise.
                if secondTest == 1:
                    isGood=False

            if isGood:
                goodGen=gen
                break

    return goodGen



def genElts_2():
    """Generate the list of elements sorted by alpha^n."""
    # When you get the generator, use it to generate proper list of elements
    config.ALPHA_ELEMENTS=[]
    for expo in range(0,config.NBR_ELEMENTS):
        config.ALPHA_ELEMENTS.append(poly_exp_mod_2(config.GENERATOR,expo,config.IRRED_POLYNOMIAL))
    
    return True

def invertGalois2_alpha(A):
    """Inversion method with generator table."""
    A=int.from_bytes(A,"big")
    i=config.ALPHA_ELEMENTS.index(A)
    expo=2**config.DEGREE - 1 - i

    inv=poly_exp_mod_2(config.GENERATOR,expo,config.IRRED_POLYNOMIAL)
    inv=inv.to_bytes(bm.bytes_needed(inv),"big")
    d=int(config.DEGREE/8)

    return bm.zfill_b(inv,d)

def invertGalois2(toInv:object):
    """
    Invert given {array of bits, bytes, int} in GF()

    ! You need to initialize the Galois_Field before !
    ! You need to have a dictionary file available !

    Output: bytes
    
    """

    d=int(config.DEGREE/8)
    toInv=bm.mult_to_bytes(toInv)
    
    if config.GALOIS_WATCH or config.IN_CREATION:
        config.WATCH_INVERSION_NUMBER += 1
        exTime = time.time()

        # A(x) . A(x)^-1 congruent to 1 mod P(x)
        # where P(x) irreductible polynomial of given degree
        # A ^ p^n - 2 = inverted

        inv=poly_exp_mod_2(bm.bytes_to_int(toInv),config.NBR_ELEMENTS-2,config.IRRED_POLYNOMIAL)
        inv=inv.to_bytes(bm.bytes_needed(inv),"big")

        config.WATCH_GLOBAL_INVERSION += time.time() - exTime

    else:
        inv=config.INVERSIONS_BOX[bm.bytes_to_int(toInv)]

    return bm.zfill_b(inv,d)

def genInverses2():
    """Generates a list of elements and their respective inverses."""

    print("\n\t || Inverses are going to be generated || \n")
    config.IN_CREATION = True

    config.INVERSIONS_BOX = [invertGalois2(bm.int_to_bytes(elt)) for elt in config.ELEMENTS]
    it.writeVartoFile(config.INVERSIONS_BOX,"inversion_Sbox")

    config.IN_CREATION = False
    print("\n\t || Inverses are generated || \n")

def handleInvBox():

    if not it.isFileHere("inversion_Sbox.txt"):

        print("A necessary file for the substitution has been deleted from the system.\n")

        if it.query_yn("- Do you want to generate the inverse substitution box (No if you want to compute each time needed) ? "):
   
            import threading
            import time

            th=threading.Thread(target=genInverses2)
            
            # This thread dies when main thread (only non-daemon thread) exits.
            th.daemon = True

            th.start()
            time.sleep(2)

        else:
            config.GALOIS_WATCH = True
    
    else:

        config.INVERSIONS_BOX=it.extractVarFromFile("inversion_Sbox")

        if len(config.INVERSIONS_BOX) != config.NBR_ELEMENTS:
            it.rmFile("inversion_Sbox.txt")
            print("WARNING - Wrong Inversion Substition box ! \n")
            it.clear()
            handleInvBox()




def GF2(degree):
    """Initialize the Galois Field GF(p^degree) in Zn."""
    config.DEGREE=degree
    config.NBR_ELEMENTS = 2 ** degree
    config.IRRED_POLYNOMIAL = int.from_bytes(bm.bits_compactor(config.IRRED_POLYNOMIAL),"big")
    config.GENERATOR = gen_GL_2(config.IRRED_POLYNOMIAL,degree)

    handleInvBox()

    if config.IN_CREATION:
        import time
        start=time.time()

        while config.IN_CREATION:
            it.clear()
            print(" --- Wait for the creation please --- ")
            print((" --- Time elapsed : {:.1f} seconds").format(time.time()-start))
            time.sleep(1)



    