#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math


def strToBinStr(str):
    '''Return string as a binary string'''
    hexString = str.encode('utf_8','ignore').hex()
    
    return ''.join(['{:08b}'.format(int(hexString[x*2:(x+1)*2],16)) for x in range(0,round(len(hexString)/2))])

def strToBinArr(str):
    '''Return string as a binary array'''
    hexString = str.encode('utf_8','ignore').hex()

    return ['{:08b}'.format(int(hexString[x*2:(x+1)*2],16)) for x in range(0,round(len(hexString)/2))]


def binArrToStr(bin):
    '''Return binary array as a string'''

    # To keep only those different than 0 during conversion.
    bin=list(filter(lambda elt : elt != '00000000',bin))

    return b''.join([int(x,2).to_bytes(1, byteorder='big') for x in bin]).decode()

def binStrToStr(bin):
    '''Return binary string as a string'''
    bytes = [bin[x*8:(x+1)*8] for x in range (0, round ((len(bin) / 8)))]

    return b''.join([int(x,2).to_bytes(1, byteorder='big') for x in bytes]).decode()

######

def binArrToBlocArr (arr, size=64):
    '''Return array divised by blocks of size bits'''
    if size % 8 != 0 or size==0:
        print ('Size must be a non null multiple of 8')
    else:
        blockSize = int(size / 8)

        if len(arr) % blockSize != 0:
            for x in range (blockSize - (len(arr) % blockSize)):
                arr.append("00000000")

        return [arr[x*blockSize:(x+1)*blockSize] for x in range (0, math.ceil(len(arr)/blockSize))]

def blocArrToBinArr (arr):
    '''Return blocks of bits array concatenated into one array'''
    return [x for i in arr for x in i]

######

def XOR(a,b):
    """Exclusive OR between two bytes."""
    res=''
    
    for i,j in zip(a,b):
        i,j=int(i),int(j)
        res+=str(i^j)

    return res

def XOR_Arr(arr1,arr2):
    """Exclusive OR between two arrays of same lenght."""
    res=[]

    if len(arr1) != len(arr2):
        return "Error: Arrays needs to be lenght equals."
    else:
        for b1,b2 in zip(arr1,arr2):
            res.append(XOR(b1,b2))
            
    return res

######
