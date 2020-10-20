#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def fileToBytes(file,message=True):
    """
    Read a file and convert to bytearray.
    True if it's a .txt file with a message.
    """

    print(f"Opening the {file} file.")

    with open(file,'rb') as f:
        data=bytearray(f.read())

    if not message: # If it's a file
        if len(data)*8 < 5000: # At least some kilo_octets
            return "Error: give in input at least some kilo_octets file's."
        else:
            return data
    else:
        return data

def codeOut(thing,coded=True,inFile=True):
    '''Choose what to do with the text (ciphered or not) and deal with it.

    thing : Array of bytesArrays
    '''
    # Pack and remove null bytes added by z_filling.
    packed=packSplittedBytes(thing)

    if not coded: 
        packed=packed.replace(b'\x00',b'')
    if inFile:

        if coded:
            #Let's write byte per byte into a .kat file
            katFile=open("encrypted.kat","wb")
            katFile.write(bytes(packed))
        else:
            katFile=open("decrypted","wb")
            katFile.write(bytes(packed))
        
        katFile.close()
        return None

    else:
        return packed


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

def circularRotation(arr, dir=0,n=1): 
    '''Circular shift to dir (left=0, right=1) of n (=1 by default) bits'''

    nB = len(arr)*8
    arrInt = int.from_bytes(arr,'big')

    # Generate full bytes of 1 of the size of the array
    size = int("0x" + "".join(["FF" for _ in range(0,len(arr))]),16)

    # ((arrInt << n)        shift to left, create 0 to the right
    # (arrInt >> (nB - n))) get all bytes from left who needs to go right to the right, rest is 0
    # AND                   the two bytes
    # & size                remove from left the oversize bits

    r = 0

    if(dir == 0):
        r = (((arrInt << n)|(arrInt >> (nB - n))) & size)
    else:
        r = (((arrInt >> n)|(arrInt << (nB - n))) & size)

    return r.to_bytes(len(arr), 'big')