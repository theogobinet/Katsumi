#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##################
# Hash functions # 
##################

import ressources.bytesManager as bm

def sponge(N, d):


    initmd5()

    r = 64
    d = int(d/8)

    blocks = bm.splitBytes(pad(N, r*8), int(r))

    S = bytearray(r + 2*d)

    for block in blocks:
        S = md5(bm.b_op(S[:r], block))

    O = bytearray()
    while len(O) < d:
        O += S[:r]
        S = md5(S)

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

    blocks = bm.splitBytes(block, 4)

    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    for i in range(63):
        F, g = 0, 0

        if i <= 15:
            F = (B & C) | ((~ B) & D)
            g = i
        elif i <= 31:
            F = (D & B) | ((~ D) & C)
            g = (5*i + 1) % 16
        elif i <= 47:
            F = B ^ C ^ D
            g = (3*i + 5) % 16
        elif i <= 63:
            F = C ^ (B | (~ D))
            g = (7*i) % 16

        F = F + A + initmd5.K[i] + bm.bytes_to_int(blocks[g])
        A = D
        D = C
        C = B
        B = B + ((F << initmd5.s[i]) | (F >> (32 - initmd5.s[i])))

    return bm.packSplittedBytes([bm.int_to_bytes(A), bm.int_to_bytes(B), bm.int_to_bytes(C), bm.int_to_bytes(D)])

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
    
