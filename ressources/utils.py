#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import sqrt
import random

def integer_sqrt(x):
    """
    Return the integer part of the square root of x, even for very
    large integer values.

    Python 'math' module does strange things with large integers...

    Got from https://stackoverflow.com/questions/47854635/square-root-of-a-number-greater-than-102000-in-python-3 .
    """

    assert x > 0

    _1_40 = 1 << 40  # 2**40

    if x < _1_40:
        return int(sqrt(x))  # use math's sqrt() for small parameters
    
    n = int(x)

    if n <= 1:
        return n  # handle sqrt(0)==0, sqrt(1)==1

    # Make a high initial estimate of the result (a little lower is slower!!!)
    r = 1 << ((n.bit_length() + 1) >> 1)

    while True:

        newr = (r + n // r) >> 1  # next estimate by Newton-Raphson
        if newr >= r:
            return r
        r = newr


def swapPos(list, pos1, pos2): 
    """Swap two elements in list."""
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list

def closestValue(givenV:int,aList:list):
    """
    Finding the nearest value in a list to a given one.
    """
    abs_diff = lambda list_value : abs(list_value - givenV)

    return min(aList, key=abs_diff)

def randomClosureChoice(bucket:list):
    """
    Pick randomly elements from a given list till is empty.

    Be careful to set bucket = GivenList.copy() to not loose original variable !
    """
    import secrets

    choice = secrets.choice(bucket)
    bucket.remove(choice)
    
    return choice


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

def lcm(a:int, b:int):
    """Find the Least Common Multiple of number a and b."""
    return (a*b) // euclid(a, b)

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
            print(f"\n{a} = {a_buffer}×{x1} + {b_buffer}×{y1}")
        n+=1
    
    s=f"gcd({a_buffer},{b_buffer})= {a_buffer}×{x0} + {b_buffer}×{y0} = {b}"
    
    return b, x0, y0, s, n

def  coprime(a:int,b:int):
    """
    Two values are said to be coprime if they have no common prime factors.
    This is equivalent to their greatest common divisor (gcd) being 1.
    """
    
    if euclid(a,b) == 1:
        return True
    else:
        return False

def pairwise_coprime(listing:list):
    """ Check if elements of a list are pairwise coprime."""

    assert isinstance(listing,list)
    
    size=len(listing)
    
    for i in range(0,size-1):
        for j in range(i+1,size):
            if not coprime(listing[i],listing[j]) : return False
    
    return True


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
    """
    Probalistic compositeness test.
    Determines whether a given number is likely to be prime (not composite).
    """

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

    # at this stage p-1 = 1 << u * r  holds
    assert p-1 == (1 << u) * r

    def witness(a):
        """
        Returns: True, if there is a witness that p is not prime.
                False, when p might be prime
        """
        z = square_and_multiply(a, r, p)
        if z == 1:
            return False

        for i in range(u):
            z = square_and_multiply(a, (1 << i) * r, p)
            if z == p1:
                return False
        return True

    for _ in range(s):
        a = random.randrange(2, p-2)
        if witness(a):
            return False

    return True


def findPrimeFactors(n:int,exponent = False) : 
    """
    Decomposes an integer n into prime factors and store in a set.

    A prime number can only be divided by 1 or itself, so it cannot be factored any further!
    Every other whole number can be broken down into prime number factors. 
    It is like the Prime Numbers are the basic building blocks of all numbers.

    Set exponent to True if you want to print p^e. 
    """
    s = []
    # Print the number of 2s that divide n  

    while (n % 2 == 0) : 
        s.append(2)  
        n = n // 2
  
    nroot = integer_sqrt(n)

    # n must be odd at this point. So we can   
    # skip one element (Note i = i +2)  
    for i in range(3, nroot , 2): 
          
        # While i divides n, print i and divide n  
        while (n % i == 0) :
            s.append(i)  
            n = n // i  
          
    # This condition is to handle the case  
    # when n is a prime number greater than 2  
    if (n > 2) : 
        s.append(n)

    uniqSorted = sorted(list(set(s)))

    if exponent:
        # using set to get unique list
        return dict(zip(uniqSorted,[s.count(e) for e in uniqSorted]))
    else:
        return uniqSorted
#########################################
############# - CRT - ###################
#########################################

def ChineseRemainder(integers:list,modulis:list,Verbose=False):
    
    """
    x congruent to a modulo n 
    [a1,..,ak] - integers
    [n1,..,nk] - modulis
    return result of Chinese Remainder.
    """

    from ressources.multGroup import inv
    
    product=1
    
    for elt in modulis:
        product *= elt

    if Verbose:
        print(f"Product of modulis is: {product}")

    if len(integers)==2 and len(modulis)==2:
         # Simplified chinese remainder theorem to deciphering
         a,b=integers[0],integers[1]
         m,n=modulis[0],modulis[1]
         if Verbose:
             print(f"x = [ {b} * {m}^(-1) * {m}  +  {a} * {n}^(-1) * {n} ] mod ({m*n}) ")
             m1,n1 = inv(m,n,Verbose)[0] , inv(n,m,Verbose)[0]
         else:
             m1,n1 = inv(m,n,Verbose) , inv(n,m,Verbose)

         solution = b*m1*m + a*n1*n

    else: 

        i=None
        
        # Condition one
        if not pairwise_coprime(modulis): raise ValueError("Error: n elements aren't pairwise coprime.")
        
        solution=0

        if Verbose:
            print(integers,modulis)
        
        for a,n in zip(integers,modulis):
            
            if not ((a>=0) and (a<n)) : raise ValueError("Error: '0 <= ai < ni' is not respected.")
            
            if Verbose:
                print(f" - x congruent to {a} modulo {n}")
            
            # According to the extended Euclid algorithm :
            Mk=int(product/n)

            if Verbose:
                yk=inv(Mk,n,Verbose)[0]
            else:
                yk=inv(Mk,n,Verbose)
            
            if Verbose:
                print(f" - y congruent to {yk} modulo {n}\n")
            
            solution += a*yk*Mk

    if Verbose:
        return (solution%product,product,f" x congruent to {solution%product} mod {product}")
    else:
        return solution%product


def mapperCRT(elt,p:int,q:int,action:bool=True,Verbose:bool=False):
    """
    Reversible mapping using Chinese Remainder Theorem into/from Zpq.

    Bijection : 
        Zpq = Zp * Zq

    action: 
        True - map
        False - unmap 
    """
    # Mapping
    if action:
        a = elt % p
        b = elt % q
        
        if Verbose and q != p:
            print(f"Converting {elt} in Zpq to a in Zp and b in Zq.")
            print(f"With a = {a} mod {p} and b = {b} mod {q}")
        
        return (a,b)
    else:
        x = ChineseRemainder(elt,[p,q],Verbose)
        return x

#########################################
############# - DLOG- ###################
#########################################

def bsgs(g:int,res:int,modulo:int):
    """
    Baby-Step Giant-Step solution for discrete algorithm problem.

    res = g^x mod modulo => log_g(res) = x mod modulo

    Use hash table for fast searching of huge values.
    """

    assert millerRabin(modulo)

    # https://en.wikipedia.org/wiki/Baby-step_giant-step

    from ressources.multGroup import inv

    m = integer_sqrt(modulo) + 1;  
  
    hashTable = {square_and_multiply(g, j, modulo): j for j in range(m)} # Baby-Step
    
    gm = square_and_multiply(g,m,modulo)
    invGm = inv(gm,modulo)

    #Initialization
    y = res

    # Search for an equivalence in the table - Giant-Step
    for i in range(m):  

        if y in hashTable:
            return i * m + hashTable[y]

        y = (y * invGm) % modulo
      
    return -1;

###
# Pollard Roh
###

def pollard_rho(g, h, n , order = None):
    """
    Pollard's Rho algorithm for discrete logarithm (HAC 3.60).
    Returns the dlog of h on the basis g and field Zn*
    """
    x = {0: 1}
    a = {0: 0}
    b = {0: 0}

    import ressources.multGroup as multGroup

    if order == None:
        order = multGroup.multiplicativeOrder(g,n)

    # from a, b and c, partitioning the field
    def step_xab(x, a, b, g, h, order, n):
        s = x % 3

        # S1
        if s == 1:
            x = x * h % n
            b = (b + 1) % order

        # S2
        if s == 0:
            x = square_and_multiply(x, 2, n)
            a = 2 * a % order
            b = 2 * b % order

        # S3
        if s == 2:
            x = x * g % n
            a = (a + 1) % order

        return x, a, b

    # returns x, a, b for a given i using memoization
    def get_xab(i):

        if i not in x:
            _x, _a, _b = get_xab(i - 1)

            x[i], a[i], b[i] = step_xab(_x, _a, _b, g, h, order, n)

        return x[i], a[i], b[i]

    def naturals_from(i):
        while True:
            # yield is a keyword that is used like return, except the function will return a generator.
            # https://www.google.com/search?client=firefox-b-d&q=yield+python
            yield i
            i += 1

    for i in naturals_from(1):

        x_i, a_i, b_i = get_xab(i)
        x_2i, a_2i, b_2i = get_xab(2 * i)

        if x_i == x_2i:

            r = (b_i - b_2i) % order

            if r == 0:  return False
            else:   return multGroup.inv(r, order) * (a_2i - a_i) % order

###
# Pohlig_Hellman
###
def pohlig_hellman(g,h,n):
    """
    Based on https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm
    """

    def group_of_prime_power_order(g,h,n=tuple):
        # n = (p,e) prime factor exponent times he appears
        p,e = n
        n = square_and_multiply(p,e)

        x = 0
        # By Lagrange's theorem, this element has order p.
        y = square_and_multiply(g,square_and_multiply(p,e-1,n),n)

        for k in range(e):
            hk = square_and_multiply(square_and_multiply(g,-x,n)*h,square_and_multiply(p,e-1-k,n),n)
            dk = pollard_rho(y,hk,n)
            x += dk * square_and_multiply(p,k,n)

        return x

    pFactors = findPrimeFactors(n,True)
    integers, modulis = [],[]

    for p,e in pFactors.items():
        ni = square_and_multiply(p,e)
        gi = square_and_multiply(g,(n//ni),n)
        hi = square_and_multiply(h,(n//ni),n)

        xi = group_of_prime_power_order(gi,hi,(p,e))

        integers.append(xi)
        modulis.append(ni)


    return ChineseRemainder(integers,modulis)


# Function to calculate k for given a, b, m  
def discreteLog(g:int, h:int, p:int,method:int=1):
    """
    Given a cyclic group of order 'p' a generator 'g' and a group element r, 
    the problem is to find an integer 'k' such that g^k = r (mod p) by using
    baby-step,giant-step algorithm or Pohlig-Hellman algorithm.

    method:
        0 - baby-step giant-step
        1 - pollard rho's algorithm (default - fastest)
        2 - pohlig-hellman 
    """

    if method == 0:
        return bsgs(g,h,p)
    elif method == 1:
        return pollard_rho(g,h,p)
    elif method == 2:
        return pohlig_hellman(g,h,p)
    else:
        return -1
    
    
    


