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

def b_op(b1,b2,ope="XOR"):
    """Bitwise operation between two bytes arrays (XOR, AND, OR available)"""
    
    by=bytearray()

    if len(b1) != len(b2):
        m=max(len(b1),len(b2))

        b1=zfill_b(b1,m)
        b2=zfill_b(b2,m)
    
    for i,j in zip(b1,b2):
        if ope == "XOR":
            by.append(int(i) ^ int(j))
        elif ope == "AND":
            by.append(int(i) & int(j))
        elif ope == "OR":
            by.append(int(i) | int(j))
        else:
            return None 

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

def leftRotate(arr, n=1): 
    '''Circular shift to left of n (=1 by default) bits'''

    nB = len(arr)*8
    arrInt = int.from_bytes(arr,'big')

    # Generate full bytes of 1 of the size of the array
    size = int("0x" + "".join(["FF" for _ in range(0,len(arr))]),16)

    # ((arrInt << n)        shift to left, create 0 to the right
    # (arrInt >> (nB - n))) get all bytes from left who needs to go right to the right, rest is 0
    # AND                   the two bytes
    # & size                remove from left the oversize bits

    return (((arrInt << n)|(arrInt >> (nB - n))) & size).to_bytes(2, 'big')