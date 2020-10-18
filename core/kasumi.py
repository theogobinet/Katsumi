#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.bytesManager import b_op, splitBytes, leftRotate, zfill_b

#################################################
############ Key Schedule #######################
#################################################

# To convert hexadecimal to an array of bytes
hexToArr = lambda h : ['{:08b}'.format(int(h[x*2:(x+1)*2],16)) for x in range(0,round(len(h)/2))]
KL1 = KL2 = KO1 = KO2 = KO3 = KI1 = KI2 = KI3 = []

def set_key(km="y/B?E(H+MbQeThVm".encode()):
    '''Kasumi's keyscheduler.'''

    global KL1, KL2, KO1, KO2, KO3, KI1, KI2, KI3
    # Chosen as a "nothing up my sleeve" number
    nums = b'\x124Vx\x9a\xbc\xde\xff\xed\xcb\xa9\x87eC!\x00'

    # Additionally a modified key K', similarly divided into 16-bit sub keys K'i, is used.
    kp = b_op(km,nums,"XOR")

    # The 128-bit key K is divided into eight 16-bit sub keys Ki
    skm, skp = splitBytes (km,2), splitBytes (kp,2)


    KL1 = [bytearray(leftRotate (skm[x],1)) for x in range (0,8)]
    KL2 = [skp[(x+2) % 8] for x in range (0,8)]
    KO1 = [bytearray(leftRotate (skm[(x + 1) % 8], 5)) for x in range (0,8)]
    KO2 = [bytearray(leftRotate (skm[(x + 5) % 8], 8)) for x in range (0,8)]
    KO3 = [bytearray(leftRotate (skm[(x + 6) % 8], 13)) for x in range (0,8)]
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
        # If arr < 64 bits, let's fill it !
        arr = zfill_b(arr,8)
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

        rp = b_op(leftRotate(b_op(l,KL[0],"AND"),1), r, "XOR")
        lp = b_op(leftRotate(b_op(rp,KL[1],"OR"),1), l, "XOR")

        return rp + lp


#######
###FO
#######
def FO(KO, KL, arr):
    if(len(arr) != 4):
        return "Error: FO takes 32 bits as 4 bytes array in input"
    else:
        arr = splitBytes(arr,2)
        l = arr[0]
        r = arr[1]

        for i in range (0,3):
            l = r
            r = b_op(r, FI(b_op(l, KO[i], "XOR"), KL[i]),"XOR")
        
        return l + r


#######
###FI
#######
def FI(b1, b2):
     ''' '''
     b1 = (int.from_bytes(b1,"big") >> 2).to_bytes(2,"big")

     z = splitBytes(b2,1)

     subZ1 =S1[int.from_bytes(z[0],"big")].to_bytes(1,"big")
     subZ2 =S2[int.from_bytes(z[1],"big")].to_bytes(1,"big")

     return b_op(b1, subZ1 + subZ2, "XOR")


########################
### Substitution boxes
########################
# https://en.wikipedia.org/wiki/S-box
#######################################


S1 = [
   54, 50, 62, 56, 22, 34, 94, 96, 38,  6, 63, 93,  2, 18,123, 33,
   55,113, 39,114, 21, 67, 65, 12, 47, 73, 46, 27, 25,111,124, 81,
   53,  9,121, 79, 52, 60, 58, 48,101,127, 40,120,104, 70, 71, 43,
   20,122, 72, 61, 23,109, 13,100, 77,  1, 16,  7, 82, 10,105, 98,
  117,116, 76, 11, 89,106,  0,125,118, 99, 86, 69, 30, 57,126, 87,
  112, 51, 17,  5, 95, 14, 90, 84, 91,  8, 35,103, 32, 97, 28, 66,
  102, 31, 26, 45, 75,  4, 85, 92, 37, 74, 80, 49, 68, 29,115, 44,
   64,107,108, 24,110, 83, 36, 78, 42, 19, 15, 41, 88,119, 59,  3,

   54, 50, 62, 56, 22, 34, 94, 96, 38,  6, 63, 93,  2, 18,123, 33,
   55,113, 39,114, 21, 67, 65, 12, 47, 73, 46, 27, 25,111,124, 81,
   53,  9,121, 79, 52, 60, 58, 48,101,127, 40,120,104, 70, 71, 43,
   20,122, 72, 61, 23,109, 13,100, 77,  1, 16,  7, 82, 10,105, 98,
  117,116, 76, 11, 89,106,  0,125,118, 99, 86, 69, 30, 57,126, 87,
  112, 51, 17,  5, 95, 14, 90, 84, 91,  8, 35,103, 32, 97, 28, 66,
  102, 31, 26, 45, 75,  4, 85, 92, 37, 74, 80, 49, 68, 29,115, 44,
   64,107,108, 24,110, 83, 36, 78, 42, 19, 15, 41, 88,119, 59,  3
]

S2 = [    
   54, 50, 62, 56, 22, 34, 94, 96, 38,  6, 63, 93,  2, 18,123, 33,
   55,113, 39,114, 21, 67, 65, 12, 47, 73, 46, 27, 25,111,124, 81,
   53,  9,121, 79, 52, 60, 58, 48,101,127, 40,120,104, 70, 71, 43,
   20,122, 72, 61, 23,109, 13,100, 77,  1, 16,  7, 82, 10,105, 98,
  117,116, 76, 11, 89,106,  0,125,118, 99, 86, 69, 30, 57,126, 87,
  112, 51, 17,  5, 95, 14, 90, 84, 91,  8, 35,103, 32, 97, 28, 66,
  102, 31, 26, 45, 75,  4, 85, 92, 37, 74, 80, 49, 68, 29,115, 44,
   64,107,108, 24,110, 83, 36, 78, 42, 19, 15, 41, 88,119, 59,  3,

   54, 50, 62, 56, 22, 34, 94, 96, 38,  6, 63, 93,  2, 18,123, 33,
   55,113, 39,114, 21, 67, 65, 12, 47, 73, 46, 27, 25,111,124, 81,
   53,  9,121, 79, 52, 60, 58, 48,101,127, 40,120,104, 70, 71, 43,
   20,122, 72, 61, 23,109, 13,100, 77,  1, 16,  7, 82, 10,105, 98,
  117,116, 76, 11, 89,106,  0,125,118, 99, 86, 69, 30, 57,126, 87,
  112, 51, 17,  5, 95, 14, 90, 84, 91,  8, 35,103, 32, 97, 28, 66,
  102, 31, 26, 45, 75,  4, 85, 92, 37, 74, 80, 49, 68, 29,115, 44,
   64,107,108, 24,110, 83, 36, 78, 42, 19, 15, 41, 88,119, 59,  3
]