#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####### - Usefuls links
# https://cryptobook.nakov.com/secure-random-generators/secure-random-generators-csprng
# https://en.wikipedia.org/wiki/List_of_random_number_generators

import os
import ressources.bytesManager as bm
from ressources.utils import millerRabin
from secrets import randbits


def xorshiftperso(evenOrodd: int = 0, nBits: int = 512):
    """
    Personal implementation of a random number generator using XORshift

    nBits: number of bits needed (e.g 2048 bits to output 2048 bits lenght's number).

    return even or odd number:
         - 0 odd
         - 1 even
         - both
    """

    assert nBits > 23
    bytes = int(nBits / 8)

    # Unpredictable random seed
    state1, state2 = os.urandom(bytes), os.urandom(bytes)

    a, b = bm.bytes_to_int(state1), bm.bytes_to_int(state2)

    a ^= bm.bytes_to_int(bm.circularRotation(state1, 0, 23))
    b ^= bm.bytes_to_int(bm.circularRotation(state2, 1, 17))

    # Generate full bytes of 1 of the size of the array
    size = int("0x" + "".join(["FF" for _ in range(0, nBits)]), 16)
    # For n bits
    a &= size
    b &= size

    r = b + a

    if evenOrodd and r & 1:
        # Bitwsing and with "-2" (number with all bits set to one except lowest one)
        # always kills just the LSB of your number and forces it to be even
        r &= -2
    elif not evenOrodd and not (r & 1):
        # Force the number to the next odd
        r |= 1

    return r


def randomInt(evenOrodd: int = 0, n: int = 512):
    """
    Return a random integer using secrets module.

    For even or odd number:
         - 0 odd
         - 1 even
         - 2 both
    """
    r = randbits(n)

    if evenOrodd and r & 1:
        # Bitwsing and with "-2" (number with all bits set to one except lowest one)
        # always kills just the LSB of your number and forces it to be even
        r &= -2
    elif not evenOrodd and not (r & 1):
        # Force the number to the next odd
        r |= 1

    return r


def randomPrime(
    nBits: int = 512, gen=None, condition=lambda p: p == p, k: int = 1, Verbose=False
):
    """
    Return generated prime numbers with bitlength nBits.
    Stops after the generation of k prime numbers.

    You can verify a condition with condition method.
    """

    # Generate random odd number of nBits
    assert nBits >= 8 and nBits <= 4096

    if not gen:
        gen = randomInt

    def find(Verbose: bool):
        maybe = gen(0, nBits)

        if Verbose:
            print("Finding one who respect given condition(s).")

        while not condition(maybe):
            maybe = gen(0, nBits)

        if Verbose:
            print("Found !")

        return maybe

    maybe = find(Verbose)

    b = k
    primes = []

    while k > 0:

        if millerRabin(maybe):
            primes.append(maybe)
            k -= 1

        maybe = find(Verbose)

    if b:
        return primes[0]

    return primes


def safePrime(
    nBits: int = 1024, randomFunction=xorshiftperso, easyGenerator: bool = False
):
    """
    The number 2p + 1 associated with a Sophie Germain prime is called a safe prime.
    In number theory, a prime number p is a Sophie Germain prime if 2p + 1 is also prime

        nBits: number of bits wanted for output prime number.

    Based on:
    https://eprint.iacr.org/2003/186.pdf

    The primes to be generated need to be 1024 bit to 2048 bit long for good cryptographical uses.

    Multiprocessing safe prime computing using cpu_percentage of your cpus.

    Return (safe_prime,sophieGermain_prime) tuple's
    """

    from multiprocessing import Pool, cpu_count, Manager
    import signal  # https://docs.python.org/3/library/signal.html

    manager = Manager()

    c = int((85 / 100) * cpu_count())

    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    poule = Pool(c)
    signal.signal(signal.SIGINT, original_sigint_handler)

    flag = manager.Value("i", 0)  # Can be shared between processes.

    return_list = manager.list([])

    data = [
        (nBits, randomFunction, easyGenerator, False, flag, return_list)
        for _ in range(c)
    ]

    # Permit to quit safe prime generation with exit signal
    try:
        poule.starmap(safePrime_worker, data)
    except KeyboardInterrupt:
        poule.terminate()
        return False
    else:
        poule.close()

    return list(return_list)[0]


def safePrime_worker(
    nBits: int = 1024,
    randomFunction=None,
    easyGenerator: bool = False,
    Verbose: bool = False,
    flag=None,
    returnL: list = [],
):
    """
    Function executed on each process for safe prime generation
    """

    import ressources.interactions as it
    from multiprocessing import Manager

    if not flag:
        flag = Manager().Value("i", 0)

    if easyGenerator:
        if Verbose:
            print("Easy generator choosen.")

        p_filter = lambda p: p % 3 == 2 and (
            p % 12 == 1 or p % 12 == 11
        )  # p = 1 mod 12 make 11 as primitive root

    else:

        p_filter = lambda p: p % 3 == 2

    while not bool(flag.value):
        # For faster searching
        # Calculate 2q +1 and (q-1)//2
        # Return Sophie Germain's prime according to what is prime.

        if randomFunction is None:
            randomFunction = randomInt

        q = randomPrime(nBits, randomFunction, p_filter, 1)

        p1 = 2 * q + 1

        p2 = (q - 1) // 2

        if Verbose:
            it.clear()
            print(f"Prime {q} candidate's.")

        if millerRabin(p1):

            if Verbose:
                print("q is prime and 2q +1 too.")
                print(f"\nSophie Germain prime's: {q}\n")

            sophieGermain_prime, safe_prime = q, p1

            # Safe prime found
            flag.value = 1
            returnL.append((safe_prime, sophieGermain_prime))

        elif millerRabin(p2):

            if Verbose:
                print("q is prime and (q-1)/2 too.")
                print(f"\nSophie Germain prime's: {p2}\n")

            sophieGermain_prime, safe_prime = p2, q

            # Safe prime found
            flag.value = 1
            returnL.append((safe_prime, sophieGermain_prime))

        else:
            if Verbose:
                print(
                    "But 2 * him + 1 and (him - 1) / 2 doesn't seem to be primes...\n"
                )


def genSafePrimes(n: int, L: list, nBits: int, randomFunction=None):
    """
    Generate n tuples of distincts safe primes number's and append them into a list L.
    Randomly choosing easy generator or not.
    """
    import random as rd

    for _ in range(n):
        # bool(rd.getrandbits(1)) faster than rd.choice([True,False])
        s = safePrime(nBits, randomFunction, bool(rd.getrandbits(1)))

        if not s:  # s is false due to interruption of research
            return s

        if s not in L:
            L.append(s)

    return L
