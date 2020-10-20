#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.bytesManager import b_op, splitBytes, circularRotation, zfill_b, swapPos

#################################################
############ Key Schedule #######################
#################################################

KL1 = []
KL2 = []
KO1 = [] 
KO2 = [] 
KO3 = []
KI1 = [] 
KI2 = []
KI3 = []

def set_key(km="y/B?E(H+MbQeThVm".encode()):
    '''Kasumi's keyscheduler.'''

    global KL1, KL2, KO1, KO2, KO3, KI1, KI2, KI3
    # Chosen as a "nothing up my sleeve" number
    nums = b'\x124Vx\x9a\xbc\xde\xff\xed\xcb\xa9\x87eC!\x00'

    # Additionally a modified key K', similarly divided into 16-bit sub keys K'i, is used.
    kp = b_op(km,nums,"XOR")

    # The 128-bit key K is divided into eight 16-bit sub keys Ki
    skm, skp = splitBytes (km,2), splitBytes (kp,2)


    KL1 = [bytearray(circularRotation (skm[x], 0, 1)) for x in range (0,8)]
    KL2 = [skp[(x+2) % 8] for x in range (0,8)]
    KO1 = [bytearray(circularRotation (skm[(x + 1) % 8], 0, 5)) for x in range (0,8)]
    KO2 = [bytearray(circularRotation (skm[(x + 5) % 8], 0, 8)) for x in range (0,8)]
    KO3 = [bytearray(circularRotation (skm[(x + 6) % 8], 0, 13)) for x in range (0,8)]
    KI1 = [skp[(x + 4) % 8] for x in range (0,8)]
    KI2 = [skp[(x + 3) % 8] for x in range (0,8)]
    KI3 = [skp[(x + 7) % 8] for x in range (0,8)]

    return None

#################################################
############### Algorithm #######################
#################################################
def kasumi (arr, encrypt=True):

    # Keys initialisation
    set_key()

    if(len(arr) > 8):
        return "Error: FL takes 64 bits as 8 bytes array in input"
    else:
        arr = splitBytes(arr,4)
        l = arr[0]
        r = arr[1]

        for i in range(0, 8):

            if not encrypt:
                i = 7 - i
            
            KO = [KO1[i], KO2[i], KO3[i]]
            KI = [KI1[i], KI2[i], KI3[i]]
            KL = [KL1[i], KL2[i]]
            lp = l

            if(i % 2 == 0):
                l = FL(KL, FO(KO, KI, l))
            else:
                l = FO(KO, KI, FL(KL, l))

            l = b_op(l, r, "XOR")
            r = lp
                
        return r+l

#######
### FL
#######
def FL(KL, arr):

    if(len(arr) != 4):
        return "Error: FL takes 32 bits as 4 bytes array in input"
    else:
        arr = splitBytes(arr,2)
        l = arr[0]
        r = arr[1]

        rp = b_op(circularRotation(b_op(l,KL[0],"AND"), 0, 1), r, "XOR")
        lp = b_op(circularRotation(b_op(rp,KL[1],"OR"), 0, 1), l, "XOR")

        return rp + lp


#######
###FO
#######
def FO(KO, KI, arr):
    if(len(arr) != 4):
        return "Error: FO takes 32 bits as 4 bytes array in input"
    else:
        arr = splitBytes(arr,2)
        l = arr[0]
        r = arr[1]

        for i in range (0,3):
            l = r
            r = b_op(r, FI(b_op(l, KO[i], "XOR"), KI[i]),"XOR")
        
        return l + r


#######
###FI
#######
def FI(b1, KI):
     ''' '''
     b1 = circularRotation(b1, 1, 2)

     z = splitBytes(KI,1)

     subZ1 =S1[int.from_bytes(z[0],"big")].to_bytes(1,"big")
     subZ2 =S2[int.from_bytes(z[1],"big")].to_bytes(1,"big")

     return b_op(b1, subZ1 + subZ2, "XOR")


########################
### Substitution boxes
########################
# https://en.wikipedia.org/wiki/S-box
#######################################

# Using RC4 initialization and adding 

S1=[]
S2=[]

def initRC4(K:bytes,iterationKey):
    """Create a shaked array with a key of length between 8 and 24 bytes."""

    global S1,S2

    # To be sure to use a bytearrayed key
    K=bytearray(K)
    mid=len(K)/2
    K1,K2=K[:mid],K[mid:]

    if len(K)<8 or len(K)>24:
        return "Error: key need to be between 8 and 24 bytes."

    S1,S2=[i for i in range(0,256)],[i for i in range(0,256)]

    j=0
    for i in range(0,256):

        j=(j+S1[i]+K1[i%len(K)])%256
        k=(k+S2[i]+K2[i%len(K)])%256

        S1,S2=swapPos(S1,i,j),swapPos(S2,i,k)


    return S1,S2