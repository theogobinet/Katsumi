#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import sqrt, floor
import random
import numpy as np


def swapPos(list, pos1, pos2): 
    """Swap two elements in list."""
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list

def euclid(a:int,b:int):  
    
    """Find the Greatest Common Divisor of number a and b."""
    
    # The GCD of two relative integers is equal to the GCD of their absolute values.
    a,b=abs(a),abs(b) 
    # The GCD of two relative integers is equal to the GCD of their absolute values.
    
    # The largest of the two numbers is replaced by the remainder of the Euclidean division of the larger 
    # number by the smaller one. 
    if (b==0) :
        return a
    elif (b>a) :
        return euclid(b,a)
    else:
        r=a%b
        return euclid(b,r)

def euclid_ext(a:int,b:int):
    
    """Extension to the Euclidean algorithm, and computes, in addition to the greatest common divisor of integers a and b, also the coefficients of Bézout's identity, which are integers x and y such that a x + b y = gcd ( a , b )."""
    x0, x1, y0, y1 = 0, 1, 1, 0
    a_buffer,b_buffer=a,b
    n=1 # iterations
    
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, (y0 - q * y1)
        x0, x1 = x1, (x0 - q * x1)
        n+=1
    
    s=f"gcd({a_buffer},{b_buffer})={a_buffer}.{x0}+{b_buffer}.{y0}"
    
    return b, x0, y0, s, n
    
def inv(a:int,m:int):
    """If a and m are prime to each other, then there is an a^(-1) such that a^(-1) * a is congruent to 1 mod m."""
    
    if euclid(a,m) != 1 :
        print(f"gcd({a},{m}) != 1 thus you cannot get an invert of a.")
        return None
    
    # Modular inverse u solves the given equation: a.u+m.v=1 
    # n number of iterations
    _,u,_,_,_=euclid_ext(a,m)
    
    if u < 0 : u+=m
    
    return u,f"u = {u} + {m}k, k in Z"    
    
def primeFactors(n:int):
    
    """Decomposes an integer n into prime factors and calculates Euler’s Totient Function."""
    
    
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
    
    return res,phi_of_n,coprimes
        
def exp_mod(a,exp,mod):
    """General method for fast computation of large positive integer powers of a number"""

    if mod == 1:
        return 0

    res=1
    a=a%mod
    
    while (exp>0) :
        
        if(exp%2==1):
            res=(res*a)%mod
        
        # Deleting LSB
        exp=floor((exp/2))
        # Updating a
        a=(a*a)%mod
    
    return res

#### Polynomials 

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

    #inZn=np.poly1d([elt%2 for elt in res])

    return res

def gen_GL(poly,degree,p=2,Zn=2):
    """Return generator of Galois Field's GF(p^degree) in Zn."""
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

    for gen in genList:
        buffGen=gen.copy()
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
                goodGen=buffGen
                break

    return goodGen


#######
    
def millerR (n:int, s=40):

    """Use Rabin-Miller algorithm to return True (n is probably prime) or False (n is definitely composite)."""

    if n<4 or n%2 == 0 : return "Error: n>3 and need to be an odd number."

    def millerT(n):
        if n<6: # Shortcut for small cases here
            return [False,False,True,True,False,True][n]

        # Initialisation -> 2^0*d=n-1
        d = n - 1
        power = 0

        while d%2 == 0:
            d = d/2
            # c factors of 2
            power+=1

        import random as r
        import math as m

        a = r.randint(2, n-2)
        x = exp_mod(a,d,n)

        if(x == 1 or x == n - 1):
            return False
        else:
            for _ in range(0,power):
                x = m.pow(x,2) % n
                if(x == n - 1):
                    return False
            return True

    # Trying s times to check

    for _ in range(1, s):
        if millerT(n):
            return False

    return True