#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.cipher.galois import *
from ressources import *

import ressources.config as config
import numpy as np
import matplotlib.pyplot as plt
import sys
import sympy as sym
        
# For good printing of polynomials:
x = sym.symbols('x')
printPoly = lambda a: sym.printing.latex(sym.Poly(a.coef,x).as_expr())

def pprint(A):
    A=np.array(A)
    if A.ndim==1:
        print(A)
    else:
        w = max([len(str(s)) for s in A]) 
        print(u'\u250c'+u'\u2500'*w+u'\u2510') 
        for AA in A:
            print(' ', end='')
            print('[', end='')
            for i,AAA in enumerate(AA[:-1]):
                w1=max([len(str(s)) for s in A[:,i]])
                print(str(AAA)+' '*(w1-len(str(AAA))+1),end='')
            w1=max([len(str(s)) for s in A[:,-1]])
            print(str(AA[-1])+' '*(w1-len(str(AA[-1]))),end='')
            print(']')
        print(u'\u2514'+u'\u2500'*w+u'\u2518')  


def get_unique_numbers(numbers):
    """Return unique numbers in list."""
    unique = []
    for number in numbers:
        if number not in unique:
            unique.append(number)
    return unique

def find_fraction(f:float):
    """
    Return fractional form of most commmun float numbers.

    input: f as a float with 4 decimals
    """
    f="{:.4f}".format(f)

    for i in range(1,1001):
        for j in range(1,1001):
            if "{:.4f}".format(i/j) == f:
                return f"{i}/{j}"

def euclid_poly(a:np.poly1d,b:np.poly1d,Verbose=False):
    """Find the Greatest Common Divisor of poly a and b."""

    # The largest of the two numbers is replaced by the remainder of the Euclidean division of the larger 
    # number by the smaller one.
     
    if (b==np.poly1d([0])) :
        a1=printPoly(a)
        return print(a1)
    elif (b.order>a.order) :
        return euclid_poly(b,a,Verbose)
    else:
        div=np.polydiv(a,b)
        q,r=div[0],div[1]

        if Verbose:
            a1=printPoly(a)
            b1=printPoly(b)
            q1=printPoly(q)
            r1=printPoly(r)
            print(f"{a1} = ( {b1} ) * ({q1}) + ({r1}) \n")
        
        return euclid_poly(b,r,Verbose)

def GFverbose(irredPoly,degree,p=2,Zn=2):
    config.IRRED_POLYNOMIAL=irredPoly
    GF(degree,p,Zn)

    elts="0"
    for elt in config.ELEMENTS:
        elts+=f" , {printPoly(elt)}"
    
    print(f"Ce corps, de générateur {printPoly(config.GENERATOR)} est constitué de {p}^{degree} = {config.NBR_ELEMENTS} élements qui sont : {elts}\n")

    return [elts,p,degree]

def verifGen(toVerif):
    """Bien initialiser GF avant !"""
    p=np.poly1d(toVerif)
    elts=f"Avec gen = {printPoly(p)} : 0, 1 (= gen^0)"

    for i in range(1,config.NBR_ELEMENTS):
        buffer1=poly_exp_mod(p,i,config.IRRED_POLYNOMIAL)
        buffer2=p**i

        b1,b2=printPoly(buffer1),printPoly(buffer2)
        if buffer2.order > buffer1.order: 
            elts+=f", gen^{i} = {b2} = {b1}"
        else:
            elts+=f", gen^{i} = {b1}"
    return print(f"{elts}\n")

def lesInverses():
    """Bien initialiser GF avant !"""
    genElts()
    expo=config.NBR_ELEMENTS-1
    print(f"Comme gen^{expo} = 1 , tous les éléments inversibles de GF (tous sauf 0) possèdent un inverse qui peut être déterminé par la relation: gen^n . gen^({expo}-n) = gen^{expo} = 1 \n")

    res=f"On a alors : (1)^-1 = 1"
    for i,elt in enumerate(config.ALPHA_ELEMENTS):
        if not i or i == len(config.ALPHA_ELEMENTS) -1:
            continue
        printable=printPoly(elt)
        inv=invertGalois(elt)
        printableInv=printPoly(inv)
        res+=f", ({printable})^-1 = {printableInv}"
    return print(res)

def tablesOpe(GF,mod,Zn=2):
    """
    Bien initialiser GF avant !
    """
    elts,p,d=GF[0],GF[1],GF[-1]

    print(f"\nLes {p**d} ({p}^{d}) restes possibles dans la division Euclidienne par {printPoly(np.poly1d(config.IRRED_POLYNOMIAL))} sont: {elts} ")
    print("\n La table d'opération pour (+) est : ")
    
    t=config.NBR_ELEMENTS+1
    plus=np.zeros((t,t),dtype='object')

    elts=config.ELEMENTS.copy()

    if elts[0] != np.poly1d([0]):
        elts.insert(0,np.poly1d([0]))

    #Initializatoin
    for i,elt in enumerate(elts):
        #For matrix presentation
        i+=1
        p=printPoly(elt)
        plus[i][0]=p
        plus[0][i]=p

    plus[0][0]="(+)"

    for i,u in enumerate(elts):
        i+=1
        for j,d in enumerate(elts):
            j+=1
            calc=poly_add_mod(u,d,mod)
            pCalc=printPoly(calc)
            plus[i][j]=pCalc

    pprint(plus)

    plus[0][0]="(x)"

    for i,u in enumerate(elts):
        i+=1
        for j,d in enumerate(elts):
            j+=1
            calc=poly_mult_mod(u,d,mod)
            pCalc=printPoly(calc)
            plus[i][j]=pCalc

    return pprint(plus)


##################################
def primeF(n:int,Verbose=True):
    
    """
    Decomposes an integer n into prime factors and calculates Euler’s Totient Function.
    
    Output: prime factors , Totient Function , Coprimes numbers
    """
    
    if Verbose:
        buffer=n
    
    if n < 2 : 
        print("By definition, A prime number (or prime) is a natural number greater than 1 that has no positive divisors other than 1 and itself.")
        # 1 is primary with itself
        return None,1   
    
    ####
    # Euler’s Totient Function
    # To do before changing n value succently 
    ####
    
    phi_of_n=1
    coprimes=[1]
    
    # a and b are said to be coprime if the only positive integer (factor) that divides both of them is 1.
    for i in range(2,n):
        if euclid(i,n) == 1 :
            coprimes.append(i)
            phi_of_n+=1
    
    
    res=[]
    
    #While n is divisible by 2, print 2 and divide n by 2
    while n%2 == 0:
        res.append(2)
        n=n/2

    # n must be odd at this point (difference of two prime factors must be at least 2)
    # so a skip of 2 ( i = i + 2) can be used 
    
    # Running the loop till square root of n not till n.
    # почему ? Let's says that a.b=n. If a>sqrt(n) and b>sqrt(n) then a.b>sqrt(n).sqrt(n). Let a.b>n.
    # QED ad absurdum
    
    for i in range(3,int(sqrt(n))+1,2): # From 3 to
        # while i divides n , print i ad divide n 
        while n % i== 0:
            res.append(int(i))
            n = n / i 
              
    # Condition if n is a prime 
    # number greater than 2 
    if n > 2: 
        res.append(int(n))

    uniq=get_unique_numbers(res)
    prime_decompo = dict()

    for elt in uniq:
        prime_decompo[elt]=prime_decompo.get(elt,res.count(elt))
    
    if Verbose:

        verbose = ""
        for k, v in prime_decompo.items():
            if k == list(prime_decompo.keys())[-1]:
                verbose+=f"{k}^{v}"
            else:
                verbose+=f"{k}^{v} + "

        print(f" n = {buffer} se décompose en {verbose} avec Phi({buffer}) = {phi_of_n} .\n")
        print(f" Les éléments suivants sont coprimes avec {buffer} : {coprimes} ")
    else:
        return prime_decompo,phi_of_n,coprimes
        