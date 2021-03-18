#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################
# Hash functions #
##################

import ressources.bytesManager as bm


def sponge(N: bytearray, d: int):
    """
    Sponge construction for hash functions.

    N: Thing to hash \n
    d: size of hash wanted \n

    return bytearray
    """

    def pad(N, r):
        iN = bm.bytes_to_int(N)
        lN = int.bit_length(iN)

        # Number of 0 to add
        b = (r - ((lN + 3) % r)) % r

        # Padding using the SHA-3 pattern 10*1: a 1 bit, followed by zero or more 0 bits (maximum r − 1) and a final 1 bit.
        op = ((iN | (1 << b + lN + 1)) << 1) ^ 1

        return bm.mult_to_bytes(op)

    r = 8
    d = int(d / 8)

    blocks = bm.splitBytes(pad(N, r * 8), r)

    S = bytearray(16)

    # Absorbing
    for block in blocks:
        S[:r] = bm.b_op(S[:r], block)
        S = md5(S)

    O = bytearray()
    # Squeezing

    while len(O) < d:
        O += S[:r]
        S = md5(S)

    # Truncating with the desired length
    return O[:d]


def md5(block):
    """
    Return md5 hash

    block: bytearray of data to hash
    """

    import math

    # Done using the Wikipedia algorithm

    def iToB(i):
        return int.to_bytes(i, 4, "little")

    def p32(a, b):
        return (a + b) % (1 << 32)

    s = [
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        7,
        12,
        17,
        22,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        5,
        9,
        14,
        20,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        4,
        11,
        16,
        23,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21,
        6,
        10,
        15,
        21,
    ]

    K = []
    for i in range(64):
        K.append((math.floor(2 ** 32 * abs(math.sin(i + 1)))) % (1 << 32))

    iN = bm.bytes_to_int(block)
    lN = len(block) * 8

    # Number of 0 to add
    b = 512 - ((lN + 1) % 512)

    lN = int.from_bytes(
        lN.to_bytes(8, byteorder="little"), byteorder="big", signed=False
    )

    iN = (((iN << 1) | 1) << b) ^ lN

    block = bm.mult_to_bytes(iN)

    b512 = bm.splitBytes(block, 64)

    h1 = 0x67452301
    h2 = 0xEFCDAB89
    h3 = 0x98BADCFE
    h4 = 0x10325476

    for b5 in b512:

        blocks = bm.splitBytes(b5, 4)

        A = h1
        B = h2
        C = h3
        D = h4

        for i in range(64):
            if i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif i <= 31:
                F = (D & B) | (~D & C)
                g = (5 * i + 1) % 16
            elif i <= 47:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            else:
                # C xor (B or (not D))
                F = C ^ (B | ~D) % (1 << 32)
                g = (7 * i) % 16

            # F + A + K[i] + M[g]
            try:
                F = p32(p32(p32(F, A), K[i]), int.from_bytes(blocks[g], "little"))
            except IndexError:
                print(i, K, blocks[g])
                raise Exception("Error")

            A = D
            D = C
            C = B
            # B + leftrotate(F, s[i])
            B = p32(B, ((F << s[i]) | (F >> (32 - s[i]))))

        h1 = p32(A, h1)
        h2 = p32(B, h2)
        h3 = p32(C, h3)
        h4 = p32(D, h4)

    return bm.packSplittedBytes([iToB(h1), iToB(h2), iToB(h3), iToB(h4)])


def nullBits(H, nbZ):
    """
    Chech if the given hash ends with nBz null bits

    H -> bytearray of the hash
    nbZ -> number of null bits
    """
    H = bm.bytes_to_int(H)

    for i in range(0, nbZ):
        if ((H >> i) & 1) == 1:
            return False

    return True


def PoW(block, zBits=1, interruptOnChange=("", 0)):
    """
    Find a salt for which the md5 hash ends with zBits null

    block: bytearray of data
    zBits: number of ending null bits

    return [block|salt]
    """

    import random
    from ressources import config as c

    if interruptOnChange[0]:
        originalData = getattr(locals()["c"], interruptOnChange[0])[
            interruptOnChange[1]
        ].copy()

    if zBits >= 255:
        raise ValueError("The number of zero bits must be lower than 2^8")

    salt = 1
    H = sponge(block + bm.mult_to_bytes(salt), 256)

    while not nullBits(H, zBits):

        if interruptOnChange[0]:
            if (
                originalData
                != getattr(locals()["c"], interruptOnChange[0])[interruptOnChange[1]]
            ):
                return False

        salt = random.randint(0, 1 << 32)
        H = sponge(block + bm.mult_to_bytes(salt), 256)

    return bm.mult_to_bytes(salt)
