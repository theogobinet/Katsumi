#!/usr/bin/env python3
# -*- coding: utf-8 -*-

######################################################################
# Digital Signature - https://en.wikipedia.org/wiki/Digital_signature
######################################################################


from . import hashFunctions as hashF
from ressources import multGroup as multG
from ressources import utils as ut
from ressources import interactions as it
from ressources import config as config

def elG_sign(docu,Verbose:bool=False):
    """

    """
    from core.asymmetric import elGamal as elG
    
    # If keys are not generated, then generate one with 2048 bits.
    if not it.isFileHere("public_key",config.DIRECTORY_PROCESSING) or not it.isFileHere("public_key.kat",config.DIRECTORY_PROCESSING):
        elG.key_gen(primeFount=True)
    
    hm = hashF.sponge(docu,elG.getSize())

    # y choosed randomly between 1 and p-2 with condition than y coprime to p-1
    p,_,g,_ = it.extractVarFromFile("public_key",config.DIRECTORY_PROCESSING)[0]

    import random as rd
    y = rd.randrange(1,p-2)

    while not ut.coprime(y,p-1):
        y = rd.randrange(1,p-2)

    if Verbose: print(f"Your secret integer is: {y}")

    s1 = ut.square_and_multiply(g,y,p)
    pasfini=0
    s2 = multG.inv(y,p-1) * (hm - pasfini)
    

    return None