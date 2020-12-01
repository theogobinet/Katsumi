#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##################
# Hash functions # 
##################

import ressources.bytesManager as bm


def sponge(N:bytearray, d:int):
    """
    Sponge construction for hash functions.

    N: Thing to hash \n
    d: size of hash wanted \n

    return bytearray
    """
    from core.symmetric.kasumi import set_key
    from core.symmetric.ciphers import CTR

    # Fixed value of key & IV for CTR used as a pseudorandom permutation function
    set_key(b'\xcd\x8a\xc1\xceV\x01\xc9\xfb\xec\xefj\xa4C\xce\xdcZ')
    iv = b'\xf9[\x91\xf0\x1d\xe5OM'

    # Fixed size of 512 bits is used as bitrate
    r = 64
    d = int(d/8)

    blocks = bm.splitBytes(pad(N, r*8), r)

    # Capacity = 2d as in SHA3 
    S = bytearray(r + 2*d)

    # Absorbing
    for block in blocks:
        S[:r] = bm.b_op(S[:r], block)
        
        # Using reversed of S because to decrypt a CTR crypted message, you have to inject it into CTR with the same params, here it's avoided
        S = bm.packSplittedBytes(CTR(list(reversed(bm.splitBytes(S))), True, iv)[:-1])

    O = bytearray()
    # Squeezing
    while len(O) < d:
        O += S[:r]
        S = bm.packSplittedBytes(CTR(list(reversed(bm.splitBytes(S))), True, iv))

    # Truncating with the desired length
    return O[:d]

def pad(N, r):

    iN = bm.bytes_to_int(N)
    lN = int.bit_length(iN)

    # Number of 0 to add
    b = (r - ((lN + 3) % r)) % r

    # Padding using the SHA-3 pattern 10*1: a 1 bit, followed by zero or more 0 bits (maximum r − 1) and a final 1 bit.
    op = ((iN | (1 << b + lN + 1)) << 1) ^ 1
    
    return bm.int_to_bytes(op)

def md5(block):

    initmd5()

    iN = bm.bytes_to_int(block)
    lN = int.bit_length(iN)

    # Number of 0 to add 
    b = 512 - ((lN + 1) % 512)

    iN = (((iN << 1) | 1) << b) ^ lN

    block = bm.int_to_bytes(iN)

    b512 = bm.splitBytes(block, 64)

    h1 = 0x67452301
    h2 = 0xefcdab89
    h3 = 0x98badcfe
    h4 = 0x10325476

    for b5 in b512:

        blocks = bm.splitBytes(b5, 4)

        A = h1
        B = h2
        C = h3
        D = h4

        for i in range(63):
            F, g = 0, 0

            if i <= 15:
                F = ((B & C) | ((~ B) & D)) % 1 << 32
                g = i
            elif i <= 31:
                F = ((D & B) | ((~ D) & C)) % 1 << 32
                g = (5*i + 1) % 16
            elif i <= 47:
                F = (B ^ C ^ D) % 1 << 32
                g = (3*i + 5) % 16
            elif i <= 63:
                F = (C ^ (B | (~ D))) % 1 << 32
                g = (7*i) % 16

            F = (F + A + initmd5.K[i] + bm.bytes_to_int(blocks[g])) % 1 << 32
            A = D
            D = C
            C = B
            B = (B + ((F << initmd5.s[i]) | (F >> (32 - initmd5.s[i])))) % 1 << 32
        
        h1 = (A + h1) % 1 << 32
        h2 = (B + h2) % 1 << 32
        h3 = (C + h3) % 1 << 32
        h4 = (D + h4) % 1 << 32

    return bm.packSplittedBytes([bm.int_to_bytes(h1), bm.int_to_bytes(h2), bm.int_to_bytes(h3), bm.int_to_bytes(h4)])

def initmd5():
    import math

    initmd5.s = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    ]

    initmd5.K = []
    for i in range (63):
        initmd5.K.append(math.floor(232 * abs(math.sin(i + 1))))