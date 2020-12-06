#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##################
# Block Chain
##################

from ressources import config as c

def validChain():
    '''
        Check the integrity of the blockchain, return boolean
    '''

    isValid = False

    blockH = validBlock(0)

    if blockH:
        for i in range(1, len(c.BC_CHAIN) - 1):
            blockHP = validBlock(i)

    # To define

def validBlock(block):

    '''
        Valid a block referenced by its ID, verify the transactions, calcul or verify the hash & salt, return boolean of successfull validation
        Block format [transaction #0, transaction #1, transaction #2, ..., hash of block n-1, salt]

        block: block id corresponding of its index in the block-chain
    '''

    from core.hashbased import hashFunctions as hf

    block = c.BC_CHAIN[block]

    isValid = True
    containsHash = False

    for b in block:
        # if it's a transaction, valid it 
        if isinstance(b, list) and isValid:
            isValid = validTransaction(b)

        # else it's the hash of block n-1 or the salt
        else:
            containsHash = True

    if containsHash and isValid:
        prevH = block [-2]
        salt = block [-1]

        isValid = hf.sponge(arrayToBytes(c.BC_CHAIN[block-1]), 256) == prevH

    # To define

    return isValid


def addUser(username, autoGenerateKeys=True, keys=[]):
    
    '''
        Create an user with the corresponding username to the users list and return the corresponding user id which can be used as index

        username: name of the user
        autoGenerateKeys: generate 2048 bits elGammal keys for the user
        keys: base64 of tuple (public key, private key) if keys are not generated for the user
    '''

    from core.asymmetric.elGamal import key_gen
    from ressources.interactions import getIntKey

    if autoGenerateKeys:
        # generate keys
        publicKey, privateKey  = key_gen(2048, None)
    else:
        # decode base64 tuple of key 
        publicKey, privateKey  = getIntKey(keys, 2)
    
    userID = len(c.BC_USERS)
    
    c.BC_USERS.append([userID, username, publicKey, privateKey])

    return userID

def addTransaction(sender, receiver, amount):
    
    '''
        Add the transaction to the last block of the block-chain
        Transaction format {sender ID -> receiver ID :: amount} -> signed by sender

        sender: user id of the sender
        receiver: user id of the receiver
        amount: amount send
    '''

    from core.asymmetric.elGamal import signing

    curBlock = c.BC_CHAIN[-1]

    transaction = [sender, receiver, amount]
    signature = signing(arrayToBytes(transaction), getUserKey(sender, 1))

    transaction.append(signature)

    curBlock.append(transaction)

def getUserKey(user, key):
    '''
        Get the corresponding key of the user reprensented by its user id

        user: user id
        key: key type: 0 -> public key, 1 -> private key
    '''
    
    return c.BC_USERS[user][2 + key]


def arrayToBytes(array):
    '''
        Convert an array to bytes, return bytearray

        array: data to convert
    '''

    return [str(x).encode() for x in array]


def validTransaction(transaction):
    '''
        Valid the given transaction

        transaction: array containing transaction information of the format {sender ID -> receiver ID :: amount} -> signed by sender
    '''

    # To define

    return True