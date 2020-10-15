#!/usr/bin/env python3
# -*- coding: utf-8 -*-



def fileToBytes(file):
    """Read a .txt file and convert to bytearray."""

    with open(file+'.txt','rb') as f:
        data=bytearray(f.read())
        #data=f.read()

    return data


def zfill_b(byteA,n:int):
    """Fill ByteArray till length n."""

    while n > len(byteA) :
        byteA.insert(0,0)

    return byteA

def b_xor(b1,b2):
    """XORing two bytes arrays."""
    
    by=bytearray()

    if len(b1) != len(b2):
        m=max(len(b1),len(b2))

        b1=zfill_b(b1,m)
        b2=zfill_b(b2,m)
    
    for i,j in zip(b1,b2):
        by.append(int(i)^int(j))

    return by


def splitBytes(data,n=8):
    """Split BytesArray into chunks of n (=8 by default) bytes."""
    return [data[i:i+n] for i in range(0, len(data), n)]

def packSplittedBytes(pSplitted):
    """Unsplit splitted array of bytes."""
    
    packed=bytearray()
    for elt in pSplitted:
        packed+=elt
    
    return packed