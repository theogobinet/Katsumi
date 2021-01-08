#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import base64
from math import log

import ressources.config as config

def bytes_to_int(b:bytes):
    """Take bytes as input and return associated integer."""
    return int().from_bytes(b,"big")

def int_to_bits(i:int):
    """Take an integer as input and return the bits written version."""
    return "{:0{}b}".format(i,i.bit_length())

def isBase64(sb):
    """
    Check if both string and bytes objects are in base64.
    """
    import base64
    try:
            if isinstance(sb, str):
                    # If there's any unicode here, an exception will be thrown and the function will return false
                    sb_bytes = bytes(sb, 'ascii')
            elif isinstance(sb, bytes):
                    sb_bytes = sb
            else:
                    raise ValueError("Argument must be string or bytes")
            return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
            return False


def mult_to_bytes(obj:object) -> bytes:
    """Convert given {array of bits, bytes, int, str, b64} to bytes"""

    if isinstance(obj,list):
        i = int(''.join(['{:01b}'.format(x) for x in obj]),2)
        res = i.to_bytes(bytes_needed(i), byteorder='big')

    elif isinstance(obj,int):
        res = obj.to_bytes(bytes_needed(obj),"big")

    elif isBase64(obj):
        import base64
        res = base64.b64decode(obj)

    elif isinstance(obj,bytes):
        res = obj

    elif isinstance(obj,str):
        res = int(obj,2)
        return mult_to_bytes(res)
        
    else:
        res = bytes(obj)

    return res

def swapPos(list, pos1, pos2): 
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list

def bytes_needed(n:int):
    """Return BYTES needed to encode an integer."""
    if n == 0:
        return 1
    return int(log(n, 256)) + 1

def bits_extractor(byteA):
    """Take ether bytes or bytearray and return an array of bits."""
    return [int(b) for b in ''.join(['{:08b}'.format(x) for x in byteA])]

file_name=""
without_ext=""

def fileToBytes(file,message=True,directory=config.DIRECTORY_PROCESSING,Verbose=False):
    """
    Read a file and convert to bytearray.
    True if it's a .txt file with a message.
    """
    import time

    global file_name, without_ext
    file_name=os.path.join(directory, file)
    without_ext=os.path.splitext(file)[0]

    if Verbose: print(f"Opening the {file} file.")

    readTime = time.time()
    with open(file_name,'rb') as f:
        data=bytearray(f.read())
    config.WATCH_READ_TIME = time.time() - readTime

    if not message: # If it's a file
        if len(data) < 1024: # At least some kilo_octets
            return "Error: give in input at least some kilo_octets file's."
        else:
            return data
    else:
        return data

###################### - File Manager

def codeOut(thing,coded=True,inFile=""):
    '''
    Choose what to do with the text (ciphered or not) and deal with it.

    thing : Array of bytesArrays
    '''

    import time 

    # Pack and remove null bytes added by z_filling.
    if not coded:
        thing[-1]=thing[-1].replace(b'\x00',b'')

    packed=packSplittedBytes(thing)

    if inFile:
        
        wTime = time.time()

        if coded:
            #Let's write byte per byte into a .kat file
            katFile=open(inFile+".kat","wb")
            katFile.write(bytes(packed))
        else:
            katFile=open(os.path.join(os.path.dirname(inFile), f'dec_{os.path.basename(inFile)[:-4]}'),"wb")
            katFile.write(bytes(packed))
        
        katFile.close()

        config.WATCH_WRITE_TIME = time.time() - wTime
        config.WATCH_EXEC_STATUS = False
        
        return ""
        
    else:
        if coded:
            return base64.b64encode(packed).decode()
        else:
            try:
                decoded = packed.decode()
                return decoded
            except UnicodeDecodeError:
                raise UnicodeDecodeError("Unable to decode the message, the decryption method does not match the encryption method, the wrong key is used or the encrypted message has been corrupted.\n")


def zfill_b(byteA,n:int):
    """
    Fill byte till length n.

    Output: bytes
    
    """

    if not isinstance(byteA,bytearray):
        byteA = bytearray(byteA)

    while n > len(byteA) :
        byteA.insert(0,0)

    return bytes(byteA)

def b_op(b1,b2,ope="XOR"):
    """
    Bitwise operation between two bytes (XOR, AND, OR available)
    
    Output: bytes
    """
    
    by=0
    m=max(len(b1),len(b2))

    if len(b1) != len(b2):
        b1 = zfill_b(b1,m)
        b2 = zfill_b(b2,m)

    
    b1 = bytes_to_int(b1) 
    b2 = bytes_to_int(b2)

    if ope == "XOR":
        by = b1 ^ b2
    elif ope == "AND":
        by = b1 & b2
    elif ope == "OR":
        by = b1 | b2
    else:
        raise ValueError("Operation unvailable")

    return int.to_bytes(by, m,"big")

def splitBytes(data,n=8):
    """Split BytesArray into chunks of n (=8 by default) bytes."""
    return [data[i:i+n] for i in range(0, len(data), n)]

def packSplittedBytes(pSplitted):
    """
    Unsplit splitted array of bytes.

    Output: byterarray
    """
    
    packed=bytearray()
    for elt in pSplitted:
        packed+=elt
    
    return packed

def circularRotation(arr, dir=0,n=1): 
    '''
    Circular shift to dir (left=0, right=1) of n (=1 by default) bits
    
    Output: bytes
    '''

    nB = len(arr)*8
    arrInt = int.from_bytes(arr,'big')

    # Generate full bytes of 1 of the size of the array
    size = int("0x" + "".join(["FF" for _ in range(0,len(arr))]),16)

    # ((arrInt << n)        shift to left, create 0 to the right
    # (arrInt >> (nB - n))) get all bytes from left who needs to go right to the right, remainder is 0
    # AND                   the two bytes
    # & size                remove from left the oversized bits

    r = 0

    if(dir == 0):
        r = (((arrInt << n)|(arrInt >> (nB - n))) & size)
    else:
        r = (((arrInt >> n)|(arrInt << (nB - n))) & size)

    return r.to_bytes(len(arr), 'big')


def hammingWeight(n:object):
    """
    The number of symbols that are different from the zero-symbol of the alphabet used.
    """

    n = bytes_to_int(mult_to_bytes(n))

    weight=0

    for i in range(n.bit_length()):
        if ((n >> i) & 1):
            weight += 1

    return weight

