#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ressources.utils as ut


def inv(a:int,m:int,Verbose=False):
    """If a and m are prime to each other, then there is an a^(-1) such that a^(-1) * a is congruent to 1 mod m."""
    if ut.euclid(a,m) != 1 :
        if Verbose:
            print(f"gcd({a},{m}) = {ut.euclid(a,m)} != 1 thus you cannot get an invert of a.")
        raise ValueError("gcd(a,m) != 1 thus you cannot get an invert of a.")
        # a modular multiplicative inverse can be found directly
    
    elif a == 0:
        if Verbose:
            print(f" a = 0 and 0 cannot have multiplicative inverse ( 0 * nothing = 1 ) .")
        raise ValueError("0 cannot have multiplicative inverse.")

    elif ut.millerRabin(m) and m%a != 0:
        # A simple consequence of Fermat's little theorem is that if p is prime and does not divide a
        # then a^−1 ≡ a^(p − 2) (mod p) is the multiplicative 
        if Verbose: 
            print(f"From Fermat's little theorem, because {m} is prime and does not divide {a} so: a^-1 = a^{m}-2 mod {m}")
        u = ut.square_and_multiply(a,m-2,m)

    elif ut.coprime(a,m):
        #From Euler's theorem, if a and n are coprime, then a^−1 ≡ a^(φ(n) − 1) (mod n).
        if Verbose:
            print(f"From Euler's theorem, because {a} and {m} are coprime -> a^-1 = a^phi({m})-1 mod {m}")
        
        u = ut.square_and_multiply(a,phi(m,1,1,Verbose)-1,m)

    else:
        
        if Verbose:
            print(f"Modular inverse u solves the given equation: a.u+m.v=1.\n Let's use the euclid extended algorithm tho.")
        
        # Modular inverse u solves the given equation: a.u+m.v=1 
        # n number of iterations
        _,u,_,_,_=ut.euclid_ext(a,m,Verbose)
        
        if u < 0 : u+=m
    
    if Verbose:
        return u,f"u = {u} + {m}k, k in Z"
    else:
        return u

def phi(n:int,m:int=1,k:int=1,Verbose:bool=False):
    """
    Totient recurcive function for integer n.
    Can compute:
         phi(n*m) with phi(n,m).
         phi(p^k) with phi(p,1,k)
    """

    if Verbose:
        print(f"\n----------- phi(n={n},m={m},k={k})--------------")
    ## Special cases ##
    twoN = int(n/2)

    if m != 1:

        d = ut.euclid(n,m)
        if Verbose:
            print(f"gcd({n},{m}) = {d}")
            print(f"phi({n})*phi({m})*({d}/phi({d}))")
        return phi(n,1,k,Verbose)*phi(m,1,k,Verbose)*int((d/phi(d,1,k,Verbose)))

    elif k != 1:
        # phi(n^k) = n ^(k-1) * phi(n)

        mult = ut.square_and_multiply(n,k-1)
        
        if Verbose:
            print(f"phi(n^k) = n ^(k-1) * phi(n) = {mult} * phi({n})")

        return mult * phi(n,1,1,Verbose)

    else:

        if n>=0 and n<=123 :
            # Fastest results for common totients (sequence A000010 in the OEIS)
            totients=[0,1,1,2,2,4,2,6,4,6,4,10,
            4,12,6,8,8,16,6,18,8,12,10,22,
            8,20,12,18,12,28,8,30,16,20,16,24,
            12,36,18,24,16,40,12,42,20,24,22,46,
            16,42,20,32,24,52,18,40,24,36,28,58,
            16,60,30,36,32,48,20,66,32,44,24,70,
            24,72,36,40,36,60,24,78,32,54,40,82,
            24,64,42,56,40,88,24,72,44,60,46,72,
            32,96,42,60,40,100,32,102,48,48,52,106,
            36,108,40,72,48,112,36,88,56,72,58,96,
            32,110,60,80,60,100,36,126,64,84,48,130,
            40,108,66,72,64,136,44,138,44,138,48,92,70,120]

            r=totients[n]

            if Verbose:
                print(f"Common totient phi({n}) = {r}")

            return r

        elif ut.millerRabin(n):
            # n is a prime number so phi(p) = (p-1)
            # p^(k-1) * phi(p) = p^(k-1) * (p-1)

            if Verbose:
                print(f"{n} is a prime number so phi(p) = (p-1)")

            return (n-1)

        # If even:
        elif not twoN & 1 :
            if Verbose:
                print(f"phi({n}) = phi(2*{twoN}) = 2 * phi({twoN}).")
            return 2*phi(twoN,m,k,Verbose)

    ## Special cases ##

        else:

            if Verbose:
                print(f"Let's calculate phi({n}) with prime factors way.")

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

def multiplicativeOrder(n:int,p:int,Verbose=False):
    """
    The minimum period of the sequence of powers of a is called the order of a.
    So a is a primitive root mod n if and only if the order of a is ϕ(n). 
    Order of n in p is the smallest number M or n^M = 1 mod p
    """
    
    k = 1
    
    if Verbose:
            print(f"m = {n**0} , iterations: {k}")

    for e in range(1,p):
        m=ut.square_and_multiply(n,e,p)
        
        if m == 1:
            break
        else:
            k+=1
            if Verbose:
                print(f"m = {n}^{e} mod {p} = {m} , iterations: {k}")

    return k


def congruenceClasses(e:int):
    """
    Find coprimes elements of e.
    If n is a positive integer, the integers between 0 and n − 1 that are coprime to n (or equivalently, the congruence classes coprime to n) form a group.
    """
    elements = []
    for i in range(e):
        if ut.coprime(i,e):
            elements.append(i)

    return elements


def firstPrimitiveRoot(n:int,totient=None,Verbose=False):
    """ Find primitive root modulo n. """

    if totient == None:
        totient=phi(n,1,1,Verbose)

    if Verbose:
        print(f"phi({n}) = {totient} ")

    if n > 3 and  ut.millerRabin(n):

        if Verbose: print(f"Let's find all prime factors of {totient}:")
        s = ut.findPrimefactors(totient)

        if Verbose:
            print("\n-----------------------------")
            print(f"{n} is prime and prime factors of totient are: {s} ")
            print(f"Computing all g^(phi({n})/p_i) mod {n} with p_i prime factors.")
            print(f"If all the calculated values are different from 1, then g is a primitive root.")
            print("-----------------------------")


        for e in range(2,totient+1):

            # Iterate through all prime factors of phi.  
            # and check if we found a power with value 1
            flag = False

            for it in s:
                t = ut.square_and_multiply(e,totient // it,n)

                if Verbose:
                    print(f" {e}^(phi({n})/{it}) mod {n} = {t} ")

                if t == 1:
                    flag = True
                    break

            if not flag :
                if Verbose:
                    print(f"Generator is: {e}")
                return e
        # If no primitive root found  
        return -1

    else:
        if Verbose:
            print(f"According to Euler's theorem, a is a primitive root mod {n} if and only if the order of a is ϕ(n) = {totient}.")

        for e in range(1,n-1):
            o = multiplicativeOrder(e,n,Verbose)

            if Verbose:
                print(f"multiplicative order({e},{n}) = {o} \n")

            if o == totient:
                if Verbose:
                    print(f"Generator is: {e}")
                return e
            
        # If no primitive root found 
        if Verbose:
            print(f"Since there is no number whose order is {totient}, there are no pritive roots modulo {n}.")
        return -1

def reducedResidueSystem(n:int,g:int=None,Verbose=False):
    """
    Return all elements of Zn* with generator g.
    """
    totient = phi(n,Verbose)
    if g == None:
        if Verbose:
            print("No generator given in input. Computing one now ..")
        g = firstPrimitiveRoot(n,totient,Verbose)
        if g == -1:
            return -1
    
    res = []
    # 1 , g , g^2 , ... , g ^ phi(n)-1
    for elt in range(totient):
        res.append(ut.square_and_multiply(g,elt,n))

    return sorted(set(res))

def findOtherGenerators(gen:int,mod:int,Verbose=False):
    """
    In a cyclic group of order n, with generator a, all subgroups are cyclic, generated (by definition) by some a^k,
    and the order of a^k is equal to (n/gcd(n,k)).

    Therefore a^k mod n is another generator of the group if and only if k is coprime to n.
    """

    if gen == -1:
        return -1

    totient = phi(mod)

    if Verbose:
        print(f"Based on the fact that {gen} is a generator of Z{mod}, the generators are {gen}^k with gcd(phi({mod}),k) = 1. ")
        print(f"Therefore the generators of Z{mod} are {gen}^k for k coprime with {totient}.")
        print(f"Or you can say: {gen}^k (with k elements from congruences classes of {totient}) are generators of Z{mod}.")

    return [ut.square_and_multiply(gen,e,mod) for e in congruenceClasses(totient)]



def isGenerator(e:int,n:int,printOther=False,Verbose=False):
    """
    Tell if an element e is generator of Zn.
    By definition, g is a generator of Zn* if and only if that cycling does not occur before these n−1 iterations.
    """

    if not ut.millerRabin(n):
        elements = [1]
        for i in range(1,n):
            t = ut.square_and_multiply(e,i,n)
            elements.append(t)
            if Verbose:
                print(f"{e}^{i} = {t} mod {n}")

            #if cycling occurs
            if t == 1:
                return False

        
        if printOther:
            if Verbose:
                print(f"There are {phi(phi(n))} generators in Z{n}.")
                print(f"{e} is the a generator of Z{n} with elements: {elements}\n")

            others = findOtherGenerators(e,n,Verbose)

            return others
        
        if Verbose:
            print(f"There are {phi(phi(n))} generators in Z{n}.")
            print(f"{e} is the a generator of Z{n} with elements: {elements}\n")

        return True
    
    elif e%n != 0:
        # We can test if some g not divisible by p is a generator of Zp*
        # by checking if g^k mod p != 1
        # with k = (p-1)/q for q each of prime factors of p-1

        L = ut.findPrimefactors(n-1)
        for k in L:
            t = ut.square_and_multiply(e,k,n)
            if Verbose:
                print(f"{e}^{k} = {t} mod {n}")
            if t == 1:
                return False
        
        return True



        
def quadraticsResidues(n:int,sortedList=True):
    """
    For a given n a list of the quadratic residues modulo n may be obtained by simply squaring the numbers 0, 1, ..., n − 1.
    Because a2 ≡ (n − a)2 (mod n), the list of squares modulo n is symmetrical around n/2, and the list only needs to go that high. 
    
    N.B: 0 and 1 are always quadratics residues by definition.
    """

    if sortedList:
        return sorted(set([ut.square_and_multiply(e,2,n) for e in range(n)]))
    else:
        return [ut.square_and_multiply(e,2,n) for e in range(n)]

def legendreSymbol(a:int,p:int,quadraticList=None):
    """
    https://en.wikipedia.org/wiki/Legendre_symbol

    LegendreSymbol of quadratics Residues is always 1 except for 0 and 1.
    """
    assert ut.millerRabin(p)

    if quadraticList == None:
        quadraticList = quadraticsResidues(p)

    if a%p == 0:
        return 0
    elif a%p != 0 and a in quadraticList:
        return 1
    else:
        return -1
    

