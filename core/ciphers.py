#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.kasumi import kasumi, set_key
from core.bytesManager import b_op, splitBytes, zfill_b, findFile, bytes_needed
import time
import core.config as config


#################################################
############ Main Method  #######################
#################################################

def cipher(arr,method=3,encrypt=True):
    """Algorithm that uses a block cipher to provide information security such as confidentiality or authenticity."""
    
    import core.config as config

    # Dealing with possible last elt < 8 bytes
    last=arr[-1]

    if len(last) < 8:
        arr[-1] = zfill_b(last,8)

    if method==1: #ECB
        config.WATCH_CIPHER_TYPE = "ECB"
        return ECB(arr, encrypt)
    
    elif method==2: #CBC
        config.WATCH_CIPHER_TYPE = "CBC"
        return CBC(arr, encrypt)

    elif method==3: #PCBC
        config.WATCH_CIPHER_TYPE = "PCBC"
        return PCBC(arr, encrypt)
    else:
        return "Error: Not implemented cipher mode. (Not yet ?) "

    return None

###### Running method to run everything:

def run(input=findFile(".kat"),inFile=True,encrypt=False,method=3):

    """
    Run encryption of decryption.
    
    input: file name with extension
    inFile: True to write an output file
    encrypt: False to decrypte
    method: Block cyphering method
    """
    from core.bytesManager import fileToBytes, codeOut
    from core.watch import watch
    from threading import Thread
    
    data=bytearray()

    if inFile:
        readTime = time.time()

        data=fileToBytes(input)

        if len(data) > 9100000:
            thread = Thread(target = watch)
            thread.daemon = True
            config.WATCH_EXEC_STATUS = True
            thread.start()

        config.WATCH_READ_TIME = time.time() - readTime
    else:
        if encrypt:
            data=bytearray(input.encode())
        else:
            try:
                first=int(input,16)
                bits=bytes_needed(first)
                data=first.to_bytes(bits,"big")

            except ValueError:
                print('ERROR : Unable to decode the message, the format of the encrypted message does not correspond to the expected one (hexadecimal).\n')

    # Keys initialisation
    set_key()

    if(len(data) > 0):
        splitted=splitBytes(data)
        ciphered=cipher(splitted,method,encrypt)
    
        return codeOut(ciphered,encrypt,inFile)
    
    return "Encoding failed"

    
#################################################
############ Electronic codebook ################
#################################################

def ECB(arr,encrypt=True):
    """The message is divided into blocks, and each block is encrypted separately."""
    res=[]
    
    for i, elt in enumerate(arr):

        config.WATCH_PERCENTAGE = ((len(arr) - (len(arr) - i)) / len(arr)) * 100
        exTime = time.time()

        res.append(kasumi(elt,encrypt))

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
                res.append(kasumi(b_op(iv,message,"XOR")))
            else:
                res.append(b_op(kasumi(message,False),iv,"XOR"))
        else:
            if encrypt:
                res.append(kasumi(b_op(res[i-1],message,"XOR")))
            else:
                res.append(b_op(kasumi(message,False),arr[i-1],"XOR"))

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
                res.append(kasumi(b_op(iv,message,"XOR")))
            else:
                res.append(b_op(kasumi(message,False),iv,"XOR"))
        else:
            if encrypt:            
                # XORing past clear message and ciphered one
                buffer=b_op(arr[i-1],res[i-1],"XOR")
                # XORing buffer and current clear message
                res.append(kasumi(b_op(buffer,message,"XOR")))
            else:

                # XORing past ciphered and past clear message
                buffer=b_op(arr[i-1],res[i-1],"XOR")
                # XORing buffer and current ciphered message
                res.append(b_op(buffer,kasumi(message,False),"XOR"))

        config.WATCH_GLOBAL_CIPHER += time.time() - exTime
        config.WATCH_BLOC_CIPHER = config.WATCH_GLOBAL_CIPHER / (i + 1)
        config.WATCH_BLOC_KASUMI = config.WATCH_GLOBAL_KASUMI / (i + 1)

    if encrypt:
        # Adding the IV to the encrypted data
        IV_action(res,iv,"store")
    
    return res

#################### Initialization Vector #################################
#https://en.wikipedia.org/wiki/Initialization_vector#Block_ciphers
#https://www.cryptofails.com/post/70059609995/crypto-noobs-1-initialization-vectors
#https://defuse.ca/cbcmodeiv.htm
############################################################################

def IV_action(arr,iv=None,action="extract"):
    """Extract or store IV at the end of the arr."""

    if action == "store" and iv != None:
        arr.append(iv)
        return None

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
    import random as rd
    message=arr[rd.randrange(0,len(arr))]

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


