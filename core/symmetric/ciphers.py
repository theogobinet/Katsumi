#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import core.symmetric.kasumi as kasu
import core.symmetric.galois_Z2 as gz2

import ressources.config as config
import ressources.bytesManager as bm
import ressources.interactions as it
from core.symmetric.watch import watch

import time

#################################################
############ Main Method  #######################
#################################################

def cipher(arr, method=3, encrypt=True, aad=""):
    """Algorithm that uses a block cipher to provide information security such as confidentiality or authenticity."""

    # Dealing with possible last elt < 8 bytes
    last=arr[-1]

    if len(last) < 8:
        arr[-1] = bm.zfill_b(last,8)

    if method==1: #ECB
        config.WATCH_CIPHER_TYPE = "ECB"
        return ECB(arr, encrypt)
    
    elif method==2: #CBC
        config.WATCH_CIPHER_TYPE = "CBC"
        return CBC(arr, encrypt)

    elif method==3: #PCBC
        config.WATCH_CIPHER_TYPE = "PCBC"
        return PCBC(arr, encrypt)

    elif method==4: #CTR
        config.WATCH_CIPHER_TYPE = "CTR"
        return CTR(arr, encrypt)
    elif method==5: #CTR
        config.WATCH_CIPHER_TYPE = "GCM"
        return GCM(arr, encrypt, aad)

###### Running method to run everything:

def run(data, inFile="", encrypt=False, method=3, aad="", key=config.KEY):

    """
    Run encryption of decryption.
    
    data: file name with extension
    encrypt: False to decrypte
    method: Block cyphering method
    """

    from threading import Thread

    if len(data) > 100000:
        thread = Thread(target = watch)
        thread.daemon = True
        config.WATCH_EXEC_STATUS = True
        thread.start()

    # Keys initialisation
    kasu.set_key(key)

    if(len(data) > 0):
        splitted=bm.splitBytes(data)
        ciphered=cipher(splitted, method, encrypt, aad)
        
        return bm.codeOut(ciphered, encrypt, inFile)
    


    
#################################################
############ Electronic codebook ################
#################################################

def ECB(arr,encrypt=True):
    """The message is divided into blocks, and each block is encrypted separately."""
    res=[]
    
    for i, elt in enumerate(arr):

        config.WATCH_PERCENTAGE = ((len(arr) - (len(arr) - i)) / len(arr)) * 100
        exTime = time.time()

        res.append(kasu.kasumi(elt,encrypt))

        config.WATCH_GLOBAL_CIPHER += time.time() - exTime
        config.WATCH_BLOC_CIPHER = config.WATCH_GLOBAL_CIPHER / (i + 1)
        config.WATCH_BLOC_KASUMI = config.WATCH_GLOBAL_KASUMI / (i + 1)
    
    return res



#################################################
############ Cipher block chaining ##############
#################################################

def CBC(arr,encrypt=True):
    """In CBC mode, each block of plaintext is XORed with the previous ciphertext block before being encrypted. """
    
    # Initialisation Vector
    if encrypt:
        iv=IV(arr)
    else:
        iv=IV_action(arr)

    res=[]

    for i, message in enumerate(arr):

        config.WATCH_PERCENTAGE = ((len(arr) - (len(arr) - i)) / len(arr)) * 100
        exTime = time.time()

        if i == 0:
            # Initialization
            if encrypt:
                res.append(kasu.kasumi(bm.b_op(iv,message,"XOR")))
            else:
                res.append(bm.b_op(kasu.kasumi(message,False),iv,"XOR"))
        else:
            if encrypt:
                res.append(kasu.kasumi(bm.b_op(res[i-1],message,"XOR")))
            else:
                res.append(bm.b_op(kasu.kasumi(message,False),arr[i-1],"XOR"))

        config.WATCH_GLOBAL_CIPHER += time.time() - exTime
        config.WATCH_BLOC_CIPHER = config.WATCH_GLOBAL_CIPHER / (i + 1)
        config.WATCH_BLOC_KASUMI = config.WATCH_GLOBAL_KASUMI / (i + 1)
    

    if encrypt:
        # Adding the IV to the encrypted data
        IV_action(res,iv,"store")
        return res
    else:
        return res

#################################################
###### Propagating cipher block chaining ########
#################################################

def PCBC(arr,encrypt=True):
    """In CBC mode, each block of plaintext is XORed with the previous ciphertext block before being encrypted. """

    # Initialisation Vector
    if encrypt:
        iv=IV(arr)
    else:
        iv=IV_action(arr)
        
    res=[]

    for i,message in enumerate(arr):

        config.WATCH_PERCENTAGE = ((len(arr) - (len(arr) - i)) / len(arr)) * 100
        exTime = time.time()

        if i == 0:
            # Initialization (same as CBC)
            if encrypt:
                res.append(kasu.kasumi(bm.b_op(iv,message,"XOR")))
            else:
                res.append(bm.b_op(kasu.kasumi(message,False),iv,"XOR"))
        else:
            if encrypt:            
                # XORing past clear message and ciphered one
                buffer=bm.b_op(arr[i-1],res[i-1],"XOR")
                # XORing buffer and current clear message
                res.append(kasu.kasumi(bm.b_op(buffer,message,"XOR")))
            else:

                # XORing past ciphered and past clear message
                buffer=bm.b_op(arr[i-1],res[i-1],"XOR")
                # XORing buffer and current ciphered message
                res.append(bm.b_op(buffer,kasu.kasumi(message,False),"XOR"))

        config.WATCH_GLOBAL_CIPHER += time.time() - exTime
        config.WATCH_BLOC_CIPHER = config.WATCH_GLOBAL_CIPHER / (i + 1)
        config.WATCH_BLOC_KASUMI = config.WATCH_GLOBAL_KASUMI / (i + 1)

    if encrypt:
        # Adding the IV to the encrypted data
        IV_action(res,iv,"store")
    
    return res

############################
###### Counter Mode ########
############################

def CTR(arr, encrypt=True):

    '''
    Counter Mode is xoring the message with a encrypted counter (IV + incr(0))

    arr: array of bytearray of 8 bytes of data to encrypt/decrypt
    encrypt: true to encrypt
    '''

    if encrypt:
        iv=IV(arr)
    else:
        iv=IV_action(arr)

    res = []

    for i, message in enumerate(arr):

        config.WATCH_PERCENTAGE = ((len(arr) - (len(arr) - i)) / len(arr)) * 100
        exTime = time.time()

        noc = bm.b_op(iv, (i + 1).to_bytes(8,"big"), "XOR")
        kas = kasu.kasumi(noc, True)
        coded = bm.b_op(message, kas, "XOR")

        res.append(coded)

        config.WATCH_GLOBAL_CIPHER += time.time() - exTime
        config.WATCH_BLOC_CIPHER = config.WATCH_GLOBAL_CIPHER / (i + 1)
        config.WATCH_BLOC_KASUMI = config.WATCH_GLOBAL_KASUMI / (i + 1)
    
    if encrypt:
        # Adding the IV to the encrypted data
        IV_action(res,iv,"store")

    return res

###################################
###### Galois Counter Mode ########
###################################

# https://blkcipher.pl/assets/pdfs/gcm-spec.pdf

def GCM(arr, encrypt=True, aad=""):

    '''
    GCM is CTR mode with authentification of additional data (AAD) authenticated with multiplication in a Galois Field

    arr: array of bytearray of 8 bytes of data to encrypt/decrypt
    encrypt: boolean, true to encypt
    aad: string of additional authenticated data
    '''

    if encrypt:
        iv=IV(arr)
    else:
        iv=IV_action(arr)
        # Integrity Check Balue
        icv=IV_action(arr)

    # Additional authenticated data (AAD), which is denoted as A
    A = []

    if encrypt:
        if(aad != ""):
            aadc = aad.encode()

            if len(aadc) > 1 << 64:
                raise Exception("Too much AAD")

            A = bm.splitBytes(aadc,8)
            A[-1] = bm.zfill_b(A[-1], 8)
    else:
        header = arr[0]
        epos = int.from_bytes(header, "big")
        A = arr[1:epos]
        arr = arr[epos:]

    # Encrypted message
    C = []

    # 1 + α + α3 + α4 + α64 - 64 field polynomial
    p = int("10000000000000000000000000000000000000000000000000000000000001111",2)

    def bti(b):
        return int.from_bytes(b, "big")

    def lenb(i):
        return (len(i)*8).to_bytes(8, "big")

    def GHASH64(H, A, C, X, i):
        n = len(C)
        m = len(A)

        if i <= m:
            # A1 = A[1-1]
            return gz2.poly_mult_mod_2(bti(bm.b_op(X, A[i - 1], "XOR")), H, p)
        elif i <= m + n:
            return gz2.poly_mult_mod_2(bti(bm.b_op(X, C[i - m - 1], "XOR")), H, p)
        elif i == m + n + 1:
            return gz2.poly_mult_mod_2(bti(bm.b_op(gz2.poly_mult_mod_2(bti(bm.b_op(X, lenb(A), "XOR")), H, p).to_bytes(8,"big"), lenb(C), "XOR")), H, p)

    H = bti(kasu.kasumi(b'\x00' * 8))

    Y = GHASH64(H, b'', [iv], b'\x00', 1).to_bytes(8,"big")
    E0 = kasu.kasumi(Y)

    n = len(arr)
    m = len(A)

    # equivalent of CTR mode
    for i in range(n):
        config.WATCH_PERCENTAGE = (((n*2 + m + 1) - ((n*2 + m + 1) - i)) / (n*2 + m + 1)) * 100
        exTime = time.time()
        
        # treats the rightmost 32bits of its argument as a nonnegative integer with the least significant bit on the right, and increments this value modulo 2^32
        Y = Y[:4] + ((int.from_bytes(Y[-4:],"big") + 1) % 1 << 32).to_bytes(4,"big")
        E = kasu.kasumi(Y)

        C.append(bm.b_op(arr[i], E, "XOR"))

        config.WATCH_GLOBAL_CIPHER += time.time() - exTime
        config.WATCH_BLOC_CIPHER = config.WATCH_GLOBAL_CIPHER / (i + 1)
        config.WATCH_BLOC_KASUMI = config.WATCH_GLOBAL_KASUMI / (i + 1)

    res = C

    # plaintext is in C when we decrypt, me must replace it with the ciphertext
    if not encrypt:
        C = arr

    # first init of X = GHASH64(i=0) = b'\x00'
    X = b'\x00'

    for i in range(n + m + 1):
        config.WATCH_PERCENTAGE = (((n*2 + m + 1) - ((n*2 + m + 1) - (i + n))) / (n*2 + m + 1)) * 100
        exTime = time.time()

        X = GHASH64(H, A, C, X, i+1).to_bytes(8,"big")

        config.WATCH_GLOBAL_CIPHER += time.time() - exTime
        config.WATCH_BLOC_CIPHER = config.WATCH_GLOBAL_CIPHER / (i + 1)

    icvc = bm.b_op(E0, X, "XOR")

    if not encrypt:
        if icv != icvc:
            print("\nWARNING: INTEGRITY CHECK CONTROL INCORRECT, AAD HAVE BEEN MODIFIED !!")

    if encrypt:
        IV_action(res,icvc,"store")
        # Adding the IV to the encrypted data
        IV_action(res,iv,"store")

        header = (1 + len(A)).to_bytes(8,"big")
        res = [header] + A + res

    return res

#################### Initialization Vector #################################
#https://en.wikipedia.org/wiki/Initialization_vector#Block_ciphers
#https://www.cryptofails.com/post/70059609995/crypto-noobs-1-initialization-vectors
#https://defuse.ca/cbcmodeiv.htm
############################################################################

def IV_action(arr, iv=None, action="extract"):
    """Extract or store IV at the end of the arr."""

    if action == "store" and iv != None:
        arr.append(iv)

    elif action == "extract" and iv == None:
        iv=arr.pop()
        return iv
    else:
        return "Error: No action assigned."


def IV(arr,key="y/B?E(H+MbQeThVm".encode()):
    """
    The IV must, in addition to being unique, be unpredictable at encryption time.
    
    Return a 8 bytes array.
    """

    # Select a random encrypted message as initial vector to transform.
    import secrets as sr
    r1=sr.randbelow(len(arr))
    r2=sr.randbits(8)
    message=bm.bytes_to_int(arr[r1]) ^ r2
    message=bm.mult_to_bytes(message)

    # Let's use the principle of hmac
    # The basic idea is to concatenate the key and the message, and hash them together. 
    # https://pymotw.com/3/hmac/

    import hmac
    import hashlib

    # Default algorithm for hmac is MD5, it's not the most secure
    # so let's use SHA-1

    digest_maker=hmac.new(key,message,hashlib.sha1)
    digest = digest_maker.hexdigest()

    return bytearray(bytes.fromhex(digest)[:8])


