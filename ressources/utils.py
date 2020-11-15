#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import sqrt, floor
import random
import numpy as np


def swapPos(list, pos1, pos2): 
    """Swap two elements in list."""
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list

def euclid(a:int,b:int,Verbose=False):  
    
    """Find the Greatest Common Divisor of number a and b."""
    
    # The GCD of two relative integers is equal to the GCD of their absolute values.
    a,b=abs(a),abs(b) 

    # The largest of the two numbers is replaced by the remainder of the Euclidean division of the larger 
    # number by the smaller one. 
    if (b==0) :
        return a
    elif (b>a) :
        return euclid(b,a,Verbose)
    else:
        r=a%b

        if Verbose:
            q=a//b
            print(f"{a} = {b}*{q} + {r}")
        
        return euclid(b,r,Verbose)


def euclid_ext(a:int, b:int, Verbose=False):
    
    """Extension to the Euclidean algorithm, and computes, in addition to the greatest common divisor of integers a and b, also the coefficients of Bézout's identity, which are integers x and y such that a x + b y = gcd ( a , b )."""
    x0, x1, y0, y1 = 0, 1, 1, 0
    a_buffer,b_buffer=a,b
    n=1 # iterations
    
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, (y0 - q * y1)
        x0, x1 = x1, (x0 - q * x1)
        if Verbose and a!=0:
            print(f"{a}= {a_buffer}×{x1} + {b_buffer}×{y1}")
        n+=1
    
    s=f"gcd({a_buffer},{b_buffer})= {a_buffer}×{x0} + {b_buffer}×{y0}"
    
    return b, x0, y0, s, n
    
def inv(a:int,m:int):
    """If a and m are prime to each other, then there is an a^(-1) such that a^(-1) * a is congruent to 1 mod m."""
    if euclid(a,m) != 1 :
        print(f"gcd({a},{m}) = {euclid(a,m)} != 1 thus you cannot get an invert of a.")
        return None
        # a modular multiplicative inverse can be found directly
    elif millerRabin(m):
        # A simple consequence of Fermat's little theorem is that if p is prime
        # then a^−1 ≡ a^(p − 2) (mod p) is the multiplicative 
        u = square_and_multiply(a,m-2,m)
    else:
        # Modular inverse u solves the given equation: a.u+m.v=1 
        # n number of iterations
        _,u,_,_,_=euclid_ext(a,m)
        
        if u < 0 : u+=m
        
    return u,f"u = {u} + {m}k, k in Z"

def phi(n:int,m:int=1,k:int=1,Verbose:bool=False):
    """
    Totient recurcive function for integer n.
    Can compute:
         phi(n*m) with phi(n,m).
         phi(p^k) with phi(p,1,k)
    """

    if Verbose:
        print(f"----------- phi(n={n},m={m},k={k})--------------")
    ## Special cases ##
    twoN = int(n/2)

    if m != 1:

        d=euclid(n,m)
        if Verbose:
            print(f"gcd({n},{m}) = {d}")
            print(f"phi({n})*phi({m})*({d}/phi({d}))")
        return phi(n,1,k,Verbose)*phi(m,1,k,Verbose)*int((d/phi(d,1,k,Verbose)))

    elif k != 1:
        # phi(n^k) = n ^(k-1) * phi(n)
        
        if Verbose:
            print(f"phi(n^k) = n ^(k-1) * phi(n)")

        return square_and_multiply(n,k-1) * phi(n,1,1,Verbose)

    else:

        if n>=0 and n<=10 :
            # Fastest results for common totients
            totients=[0,1,1,2,2,4,2,6,4,6,4,10]
            r=totients[n]

            if Verbose:
                print(f"Common totient phi({n}) = {r}")

            return r

        elif millerRabin(n):
            # n is a prime number so phi(p) = (p-1)
            # p^(k-1) * phi(p) = p^(k-1) * (p-1)

            if Verbose:
                print(f"{n} is a prime number so phi(p) = (p-1)")

            return (n-1)

        # If even:
        elif not twoN & 1 :
            if Verbose:
                print(f"2*phi({twoN})")
            return 2*phi(twoN,m,k,Verbose)

    ## Special cases ##

        else:
            result = n   # Initialize result as n 
            
            # Consider all prime factors 
            # of n and for every prime 
            # factor p, multiply result with (1 - 1 / p) 
            p = 2
            while p * p <= n : 
        
                # Check if p is a prime factor. 
                if n % p == 0 : 
        
                    # If yes, then update n and result 
                    while n % p == 0 : 
                        n = n // p 
                    result *=  (1 - (1 / p)) 
                p += 1
                
                
            # If n has a prime factor 
            # greater than sqrt(n) 
            # (There can be at-most one 
            # such prime factor) 
            if n > 1 : 
                result *= (1 - (1 / n)) 
        
            return int(result) 
    
def primeFactors(n:int):
    
    """
    Decomposes an integer n into prime factors.
    
    Output: prime factors , Coprimes numbers
    """
    
    if n < 2 : 
        print("By definition, A prime number (or prime) is a natural number greater than 1 that has no positive divisors other than 1 and itself.")
        # 1 is primary with itself
        return None,1   
    
    coprimes=[1]
    
    # a and b are said to be coprime if the only positive integer (factor) that divides both of them is 1.
    for i in range(2,n):
        if coprime(i,n):
            coprimes.append(i)
    
    
    res=[]
    
    #While n is divisible by 2, print 2 and divide n by 2
    while not n & 1:
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

    prime_decompo = dict()

    # Return unique numbers in list.
    unique = []
    for number in res:
        if number not in unique:
            unique.append(number)

    for elt in unique:
        prime_decompo[elt]=prime_decompo.get(elt,res.count(elt))
    

    return prime_decompo,coprimes
        
def square_and_multiply(x, k, p=None):
    """
    Square and Multiply Algorithm
    Parameters: positive integer x and integer exponent k,
                optional modulus p
    Returns: x**k or x**k mod p when p is given
    """
    b = bin(k).lstrip('0b')
    r = 1
    for i in b:
        r = r**2
        if i == '1':
            r = r * x
        if p:
            r %= p
    return r

def millerRabin(p, s=40):
    """Determines whether a given number is likely to be prime."""
    if p == 2: # 2 is the only prime that is even
        return True
    if not (p & 1): # n is a even number and can't be prime
        return False

    p1 = p - 1
    u = 0
    r = p1  # p-1 = 2**u * r

    while r % 2 == 0:
        r >>= 1
        u += 1

    # at this stage p-1 = 2**u * r  holds
    assert p-1 == 2**u * r

    def witness(a):
        """
        Returns: True, if there is a witness that p is not prime.
                False, when p might be prime
        """
        z = square_and_multiply(a, r, p)
        if z == 1:
            return False

        for i in range(u):
            z = square_and_multiply(a, 2**i * r, p)
            if z == p1:
                return False
        return True

    for _ in range(s):
        a = random.randrange(2, p-2)
        if witness(a):
            return False

    return True


def coprime(a:int,b:int):
    """
    Two values are said to be coprime if they have no common prime factors.
    This is equivalent to their greatest common divisor (gcd) being 1.
    """
    
    if euclid(a,b):
        return True
    else:
        return False

def pairwise_coprime(listing):
    """ Check if elements of a list are pairwise coprime."""
    
    size=len(listing)
    
    for i in range(0,size-1):
        for j in range(i+1,size):
            if not coprime(listing[i],listing[j]) : return False
    
    return True

def ChineseRemainder(integers:list,modulis:list,Verbose=False):
    
    """
    x congruent to a modulo n 
    [a1,..,ak] - integers
    [n1,..,nk] - modulis
    return result of Chinese Remainder.
    """
    
    product=1
    
    for elt in modulis:
        product *= elt
        if Verbose:
            print(f"Product of modulis is: {product}")

    i=None
    
    # Condition one
    if not pairwise_coprime(modulis): return "Error: n elements aren't pairwise coprime."
    
    solution=0

    if Verbose:
        print(integers,modulis)
    
    for a,n in zip(integers,modulis):
        
        if not ((a>=0) and (a<n)) : return "Error: '0 <= ai < ni' is not respected."
        
        if Verbose:
            print(f" - x congruent to {a} modulo {n}")
        
        # According to the extended Euclid algorithm :
        Mk=int(product/n)
        yk=inv(Mk,n)[0]
        
        if Verbose:
            print(f" - y congruent to {yk} modulo {n}\n")
        
        solution += a*yk*Mk
    
    
    if Verbose:
        return (solution%product,product,f" x congruent to {solution%product} mod {product}")
    else:
        return solution%product

def order(n,p):
    """Order of n in p is the smallest number M or n^M = 1 mod p"""
    m=n
    k=1
    for _ in range(p-1):
        m*=n%p
        print(f"m = {m} , iterations: {k}")
        k+=1
        if m:
            break