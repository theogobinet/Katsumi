#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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