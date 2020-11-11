#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ressources.prng import safePrime
from ressources.utils import square_and_multiply
from random import randrange as rd

#############################################
########### - Key Generation - ##############
#############################################


def findGen():
    """
    Easy way of selecting a random generator :
    select a random value h between 2 and p−1
    """
    computed = square_and_multiply(rd(2,p-1),(p-1)/q,p)

    # If it's not one, it's the gen !
    while computed :
        computed = square_and_multiply(rd(2,p-1),(p-1)/q,p)
    
    return computed

def key_gen():
    s=safePrime(512)
    p,q=s[0],s[1]
    

        



#############################################
########### -   Encryption   - ##############
#############################################





