#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from math import floor
from core.utils import millerR, primeFactors
import core.config as config


def poly_mult(A,B,nZ=2):
    """Polynomial multiplication in nZ."""

    A,B=np.poly1d(A),np.poly1d(B)

    if  not isinstance(nZ, int) :
        print("[INFO] nZ wasn't an integer, it'll be converted to an integer.")

    return np.poly1d([round(elt%nZ) for elt in A*B])

def poly_mult_mod(A,B,mod,nZ=2):
    """Polynomial multiplication in nZ with modular output."""

    remainder=np.polydiv(poly_mult(A,B,nZ),mod)[1]

    return np.poly1d(positive_nZ(remainder,nZ))

def positive_nZ(poly,nZ=2):
    """
    To avoid negative elt and being always in nZ.
    
    poly: np.poly1d type's needed.
    """
    inZn=[]

    for elt in poly:
        elt=round(elt)
        if elt < 0 :
            elt+=nZ
        inZn.append(elt)

    return np.poly1d(inZn)

def poly_exp_mod(P,exp,mod,nZ=2):
    """
    General method for fast computation of polynomials powers of a number.
    
    P: Polynomial
    exp: exposant
    mod: polynial to be coungruent to
    nZ: into Zn
    """

    P=np.poly1d(P)

    if mod == np.poly1d([1]):
        return 0

    res=np.poly1d([1])
    P=np.polydiv(P,mod)[1]

    while (exp>0) :
        if(exp%2==1):
            res=np.polydiv(poly_mult(P,res,nZ),mod)[1]
        
        # Deleting LSB
        exp=floor((exp/2))
        # Updating P
        P=np.polydiv(poly_mult(P,P,nZ),mod)[1]

    return np.poly1d(positive_nZ(res,nZ))


def gen_GL(poly,degree,p=2,Zn=2):
    """Return generator of Galois Field's GF(p^degree) based on primitive polynomial poly in Zn."""
    # Order of multiplicative subgroup
    pn1=(p**degree)-1
    q=None

    un=np.poly1d([1])

    if millerR(pn1):
        q=[1]
    else:
        q=primeFactors(pn1)[0]

    genList=[]
    goodGen=None

    for i in range(1,p**degree):
        bits=[int(b) for b in '{value:0{size}b}'.format(value=i,size=degree)]
        genList.append(bits)

    config.ELEMENTS=genList

    for gen in genList:
        #buffGen=gen.copy()
        gen=np.poly1d(gen)

        # α(x)^(p^n-1) % f(x) == 1
        firstTest=poly_exp_mod(gen,pn1,poly,Zn)
        if firstTest==un:
            config.INVERT_EXPO=pn1
            isGood=True  
            for elt in q:
                # α(x)^((p^n-1)/q) % f(x) != 1, for all q that are prime factors of p^n-1
                secondTest=poly_exp_mod(gen,pn1/elt,poly,Zn)
                if secondTest == un:
                    isGood=False
            if isGood:
                goodGen=gen
                break

    return goodGen


def invertGalois(A):
    """
    Invert given Array in a Galois Field degree in Zn.

    /!\ You need to initialize the Galois_Field with GF(degree)

    NB: If A is a bytearray, it'll be treated as one - don't worry.
    
    """

    # A(x) . A(x)^-1 congruent to 1 mod P(x)
    # where P(x) irreductible polynomial of given degree

    import numpy as np

    bits=A
    res = None

    if isinstance(A,bytearray):
        bits=[int(b) for b in ''.join(['{:08b}'.format(x) for x in A])]

    A=np.poly1d(bits)
    gen=config.GENERATOR


    for i in range(1,config.NBR_ELEMENTS):

        test=poly_exp_mod(gen,i,config.IRRED_POLYNOMIAL)

        if test == A:
            exposant=config.NBR_ELEMENTS-1-i
            # alpha ^ exposant = inverted
            res = poly_exp_mod(gen,exposant,config.IRRED_POLYNOMIAL)
            
            print(res)

            res = [elt for elt in res]

    
    return res


def GF(degree,p=2,Zn=2):
    """Initialize the Galois Field GF(p^degree) in Zn."""
    config.NBR_ELEMENTS = p ** degree 
    config.GENERATOR = gen_GL(config.IRRED_POLYNOMIAL,degree,p,Zn)
    return None



