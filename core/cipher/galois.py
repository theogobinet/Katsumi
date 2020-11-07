#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This ensure that you are just importing things into the __init__.py

import numpy as np
from math import floor
import ressources.utils as utils
import ressources.config as config
import ressources.bytesManager as bm



def polydiv_mod(A,B,nZ=2):
    """Polynomial division in nZ"""
    buffer=np.polydiv(A,B)

    return (np.poly1d([round(elt%nZ) for elt in buffer[0]]) , np.poly1d([round(elt%nZ) for elt in buffer[1] ]) )


def poly_add(A,B,nZ=2):
    """Polynomial multiplication in nZ."""

    A,B=np.poly1d(A),np.poly1d(B)

    if  not isinstance(nZ, int) :
        print("[INFO] nZ wasn't an integer, it'll be converted to an integer.")

    return np.poly1d([round(elt%nZ) for elt in A+B])


def poly_add_mod(A,B,mod,nZ=2):
    """Polynomial multiplication in nZ with modular output."""

    remainder=np.polydiv(poly_add(A,B,nZ),mod)[1]

    return np.poly1d(positive_nZ(remainder,nZ))

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
        elt=int(round(elt%nZ))
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

    P,mod=np.poly1d(P),np.poly1d(mod)

    if mod == np.poly1d([1]):
        return 0

    res=np.poly1d([1])
    P=polydiv_mod(P,mod,nZ)[1]

    while (exp>0) :
        if(exp%2==1):
            res=polydiv_mod(poly_mult_mod(P,res,mod,nZ),mod,nZ)[1]
        
        # Deleting LSB
        exp=floor((exp/2))
        # Updating P
        P=polydiv_mod(poly_mult_mod(P,P,mod,nZ),mod,nZ)[1]

    return positive_nZ(res,nZ)


def gen_GL(poly,degree,p=2,Zn=2):
    """Return generator of Galois Field's GF(p^degree) based on primitive polynomial poly in Zn."""
    # Order of multiplicative subgroup
    pn1=(p**degree)-1

    un=np.poly1d([1])

    if utils.millerR(pn1):
        q=[pn1]
    else:
        q=utils.primeFactors(pn1)[0]

    genList=[]
    goodGen=None

    for i in range(1,p**degree):
        bits=[int(b) for b in '{value:0{size}b}'.format(value=i,size=degree)]
        genList.append(np.poly1d(bits))

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


def genElts():
    """Generate the list of elements sorted by alpha^n."""
    # When you get the generator, use it to generate proper list of elements
    config.ALPHA_ELEMENTS=[]
    for expo in range(0,config.NBR_ELEMENTS):
        config.ALPHA_ELEMENTS.append(poly_exp_mod(config.GENERATOR,expo,config.IRRED_POLYNOMIAL))
    
    return True



def invertGalois(A,output=1):
    """
    Invert given Array in a Galois Field degree in Zn.

    \! You need to initialize the Galois_Field with GF(degree)

    output: 0 for an array
            1 for a polynomial
            2 for bytes

    NB: input of bytearray and bytes acccepted. 
    
    """

    # A(x) . A(x)^-1 congruent to 1 mod P(x)
    # where P(x) irreductible polynomial of given degree

    if isinstance(A,bytearray) or isinstance(A,bytes):
        bits=[int(b) for b in ''.join(['{:08b}'.format(x) for x in A])]
    else:
        bits=np.poly1d(A)

    A=np.poly1d(bits)
            
    # A ^ p^n - 2 = inverted
    res = poly_exp_mod(A,config.NBR_ELEMENTS-2,config.IRRED_POLYNOMIAL)

    if output==0:
        return list(res)
    elif output==1:
        return res
    elif output==2:
        return bm.bits_compactor(list(res))
    else:
        return None


def GF(degree,p=2,Zn=2):
    """Initialize the Galois Field GF(p^degree) in Zn."""
    config.DEGREE=degree
    config.NBR_ELEMENTS = p ** degree 
    config.GENERATOR = gen_GL(config.IRRED_POLYNOMIAL,degree,p,Zn)
    return None