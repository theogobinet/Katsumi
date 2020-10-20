#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from math import log

THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_name=""
without_ext=""


def bytes_needed(n):
    if n == 0:
        return 1
    return int(log(n, 256)) + 1


def findFile(ext):
    """To find a file given extension and return is name."""
    for f in os.listdir(os.path.join(THIS_FOLDER,"share/")):
        if f.endswith(ext):
            name=f
    return name


def fileToBytes(file,message=True):
    """
    Read a file and convert to bytearray.
    True if it's a .txt file with a message.
    """

    global file_name, without_ext
    file_name=os.path.join(THIS_FOLDER, "share/"+file)
    without_ext=os.path.splitext(file)[0]

    print(f"Opening the {file} file.")

    with open(file_name,'rb') as f:
        data=bytearray(f.read())

    if not message: # If it's a file
        if len(data) < 1024: # At least some kilo_octets
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
    if not coded:
        thing[-1]=thing[-1].replace(b'\x00',b'')

    packed=packSplittedBytes(thing)

    if inFile:
        if coded:
            #Let's write byte per byte into a .kat file
            katFile=open(file_name+".kat","wb")
            katFile.write(bytes(packed))
        else:
            katFile=open(os.path.join(THIS_FOLDER,"share/decrypted-"+without_ext),"wb")
            katFile.write(bytes(packed))
        
        katFile.close()
        return None

    else:
        if coded:
            return packed.hex()
        else:
            try:
                print("Here is your ciphered message, copy it and send it !\n")
                return packed.decode()
            except UnicodeDecodeError:
                print("ERROR : Unable to decode the message, the decryption method does not match the encryption method or the encrypted message has been corrupted.\n")


def zfill_b(byteA,n:int):
    """Fill ByteArray till length n."""

    byteA = bytearray(byteA)

    while n > len(byteA) :
        byteA.insert(0,0)

    return byteA

def b_op(b1,b2,ope="XOR"):
    """Bitwise operation between two bytes arrays (XOR, AND, OR available)"""
    
    by=0
    m=max(len(b1),len(b2))

    if len(b1) != len(b2):
        b1 = zfill_b(b1,m)
        b2 = zfill_b(b2,m)
    
    b1 = int().from_bytes(b1,"big")
    b2 = int().from_bytes(b2,"big")

    if ope == "XOR":
        by = b1 ^ b2
    elif ope == "AND":
        by = b1 & b2
    elif ope == "OR":
        by = b1 | b2
    else:
        return None 

    return by.to_bytes(m,"big")

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