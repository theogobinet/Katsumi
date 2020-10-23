#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from math import floor
from core.utils import millerR, primeFactors
import core.config as config

def poly_mult(A,B,nZ):
    """Polynomial multiplication in nZ."""
    return np.poly1d([elt%2 for elt in A*B])


def poly_exp_mod(P,exp,mod,nZ=2):
    """
    General method for fast computation of polynomials powers of a number.
    
    P: Polynomial
    exp: exposant
    mod: polynial to be coungruent to
    nZ: into Zn
    """

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

    inZn=[]
    # To avoid negative elt and being always in positive modulo
    for elt in res:
        if elt < 0 :
            elt+=nZ
        inZn.append(elt)

    return np.poly1d(inZn)


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

### Pas fini ne marche pas
def irreductiblePoly(P,degree):
    """
    Test all factor polynomials over GF of degree higher than
    zero and lower than given degree to see if p has no factor polynomial and
    thus is irreducible ofer GF(2).
    """

    for elt in config.ELEMENTS:
            if not (0 < len(elt) < degree):
                continue

            remainder=np.polydiv(P,elt)

            if np.count_nonzero(remainder) == 0:
                return False

    return True

def primitivePoly(P,degree):
    """Test of polynomial is primitive (and hence also irreductible)."""

    if not irreductiblePoly(P,degree):
        return False
    else: #irreductible
        return True
        
def invertGalois(A,bytes=True):
    """
    Invert given Array in a Galois Field degree in Zn.

    /!\ You need to initialize the Galois_Field with GF(degree).git/

    bytes : Enter True if you treat a bytearray.
    
    """

    # A(x) . A(x)^-1 congruent to 1 mod P(x)
    # where P(x) irreductible polynomial of given degree

    import numpy as np

    bits=A

    if bytes:
        bits=[int(b) for b in ''.join(['{:08b}'.format(x) for x in A])]

    A=np.poly1d(bits)
    gen=config.GENERATOR

    for i in range(1,config.NBR_ELEMENTS):

        test=poly_exp_mod(gen,i,config.IRRED_POLYNOMIAL)

        if test == A:
            exposant=config.NBR_ELEMENTS-1-i
            # alpha ^ exposant = inverted
            res = poly_exp_mod(gen,exposant,config.IRRED_POLYNOMIAL)
            
            return [elt for elt in res]

    
    return None


def GF(degree,p=2,Zn=2):
    """Initialize the Galois Field GF(p^degree) in Zn."""
    config.NBR_ELEMENTS = degree ** p 
    config.GENERATOR = gen_GL(config.IRRED_POLYNOMIAL,degree,p,Zn)
    return None
    


