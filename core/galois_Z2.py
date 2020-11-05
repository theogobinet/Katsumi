#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import floor
from core.utils import millerR, primeFactors
import core.config as config
from core.bytesManager import bits_compactor, bits_extractor, bytes_to_int, zfill_b, bytes_needed, int_to_bytes

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
    return (poly_mod_2(poly_mult_2(a, b), mod))
    

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

    if millerR(pn1):
        q=[pn1]
    else:
        q=primeFactors(pn1)[0]

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


def lookUpInverse2(key:object):
    """
    Invert given {array of bits, bytes, int} in GF()

    ! You need to initialize the Galois_Field before !
    ! You need to have a dictionary file available !

    Output: bytes
    
    """

    if isinstance(key,list):
        toInv=bits_compactor(key)
    elif isinstance(key,int):
        toInv=int_to_bytes(key)
    else:
        toInv=key

    inv=config.INVERSIONS_DICT.get(bytes_to_int(toInv))
    d=int(config.DEGREE/8)

    return zfill_b(inv,d)


def invertGalois2_alpha(A):
    """Inversion method with lookup table."""
    A=int.from_bytes(A,"big")
    i=config.ALPHA_ELEMENTS.index(A)
    expo=2**config.DEGREE - 1 - i

    inv=poly_exp_mod_2(config.GENERATOR,expo,config.IRRED_POLYNOMIAL)
    inv=inv.to_bytes(bytes_needed(inv),"big")
    d=int(config.DEGREE/8)

    return zfill_b(inv,d)

def invertGalois2(A:bytes):
    """
    Invert given bytes in GF(2^degree)

    ! You need to initialize the Galois_Field with GF2(degree)

    Output: bytes
    
    """
    # A(x) . A(x)^-1 congruent to 1 mod P(x)
    # where P(x) irreductible polynomial of given degree
    # A ^ p^n - 2 = inverted

    inv=poly_exp_mod_2(bytes_to_int(A),config.NBR_ELEMENTS-2,config.IRRED_POLYNOMIAL)
    inv=inv.to_bytes(bytes_needed(inv),"big")
    d=int(config.DEGREE/8)

    return zfill_b(inv,d)

def genInverses():
    """Generates a list of elements and their respective inverses."""
    from core.interactions import writeVartoFile

    print("\n Inverses are going to be generated.")

    # Iterator (key,values)
    zip_iterator = zip(config.ELEMENTS, [invertGalois2(int_to_bytes(elt)) for elt in config.ELEMENTS])

    config.INVERSIONS_DICT = dict(zip_iterator)
    writeVartoFile(config.INVERSIONS_DICT,"inversion_dict")

    print("\n\t || Inverses are generated || \n")
    


def GF2(degree):
    """Initialize the Galois Field GF(p^degree) in Zn."""
    config.DEGREE=degree
    config.NBR_ELEMENTS = 2 ** degree
    config.IRRED_POLYNOMIAL = int.from_bytes(bits_compactor(config.IRRED_POLYNOMIAL),"big")
    config.GENERATOR = gen_GL_2(config.IRRED_POLYNOMIAL,degree)

    from core.interactions import query_yn

    if query_yn("- Do you want to generate the inverse dictionary's ? (No if file exist) "):
        
        from core.interactions import clear
        import threading
        import time
        import sys

        th=threading.Thread(target=genInverses)
        clear()
        
        # This thread dies when main thread (only non-daemon thread) exits.
        th.daemon = True

        th.start()
        time.sleep(2)

    else:
        from core.interactions import extractVarFromFile
        config.INVERSIONS_DICT=extractVarFromFile("inversion_dict")
