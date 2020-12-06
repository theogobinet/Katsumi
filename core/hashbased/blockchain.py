#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from ressources import config as c

######################
#       TESTS        #
######################

def createTestBC():

    # create the 1st block
    initChain()

    c.BC_KEY_SIZE = 128

    # create 2 users
    Al = addUser("Alice")
    Bo = addUser("Bob")

    transitUTXO(-1, Al, 10)
    transitUTXO(-1, Al, 20)
    transitUTXO(-1, Al, 30)
    transitUTXO(-1, Al, 40)

    # add transactions
    addTransaction(Al, Bo, 91)
    addTransaction(Bo, Al, 30)

    print(c.BC_UTXO)

    # valid the block
    validBlock(len(c.BC_CHAIN) - 1)

    displayBC()

######################
#       CORE         #
######################

def initChain():
    '''
        Create the first block of the block-chain
    '''

    from core.hashbased import hashFunctions as hf

    firstBlock = [hf.sponge(b"Lorsqu'un canide aboie, ca fait BARK", c.BC_HASH_SIZE)]
    firstBlock.append(hf.PoW(arrayToBytes(firstBlock), c.BC_POW_NULL))

    c.BC_CHAIN.append(firstBlock)
    c.BC_CHAIN.append([])


def validChain():
    '''
        Check the integrity of the blockchain, return boolean
    '''

    for i in range(1, len(c.BC_CHAIN)):
        if not validBlock(i):
            return False
    
    return True


def validBlock(blockI):

    '''
        Valid a block referenced by its ID, verify the transactions, calcul or verify the hash & salt, return boolean of successfull validation
        Block format [transaction #0, transaction #1, transaction #2, ..., hash of block n-1, salt]

        blockI: block id corresponding of its index in the block-chain
    '''

    from core.hashbased import hashFunctions as hf


    cBlock = c.BC_CHAIN[blockI]

    if (blockI == len(c.BC_CHAIN) - 1) and not cBlock:
        return True

    isValid = True
    containsHash = False

    unvalidTransactions = []

    for b in cBlock:
        # if it's a transaction, valid it 

        if isinstance(b, list) and isValid:
            # if the transaction is not valid, it's ingored -> removed of the block for validation
            if not validTransaction(b):
                unvalidTransactions.append(b)

        # else it's the hash of block n-1 or the salt
        else:
            containsHash = True

    for transaction in unvalidTransactions:
        cBlock.remove(transaction)

    # if the block has been valided, check the hash
    if containsHash and isValid:
        prevH = cBlock[-2]
        prevBlockH = getBlockHash(blockI-1)

        # if the previous block calculated hash is the same that the one stored and the salt is ok, block is valid
        isValid = prevBlockH == prevH and hf.nullBits(prevBlockH, c.BC_POW_NULL)


    # if the block hasn't been valided yet, valid it
    if not containsHash and isValid:
        # Adding the hash of the previous block
        cBlock.append(getBlockHash(c.BC_CHAIN[blockI - 1]))

        # Block validation -> calcul of proof of work
        cBlock.append(hf.PoW(arrayToBytes(cBlock), c.BC_POW_NULL))

        # Create a new block in the blockchain
        c.BC_CHAIN.append([])     
    
    return isValid


def addUser(username, autoGenerateKeys=True, keys=[]):
    
    '''
        Create an user with the corresponding username to the users list and return the corresponding user id which can be used as index

        username: name of the user
        autoGenerateKeys: generate 2048 bits elGammal keys for the user
        keys: base64 of tuple (public key, private key) if keys are not generated for the user
    '''

    from core.asymmetric.elGamal import key_gen
    from ressources.interactions import getIntKey, extractSafePrimes 

    if autoGenerateKeys:
        # generate keys
        primes = extractSafePrimes(c.BC_KEY_SIZE)
        publicKey, privateKey = key_gen(c.BC_KEY_SIZE, primes)
    else:
        # decode base64 tuple of key

        publicKey, privateKey = getIntKey(keys, 2)
    
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


def validTransaction(transaction):
    '''
        Valid the given transaction

        transaction: array containing transaction information of the format {sender ID -> receiver ID :: amount} -> signed by sender
    '''

    from core.asymmetric.elGamal import verifying

    core = transaction[:-1]
    signature = transaction[-1]

    sender = core[0]

    isValid = verifying(arrayToBytes(core), getUserKey(sender, 0), signature)

    if isValid:
        return transitUTXO(sender, core[1], core[2])
    else:
        return False


def getUserUTXO(user):
    '''
        Get a list containing the amount of each UTXO for a given user

        user: user id
    '''

    amounts = []
    for i, UTXO in enumerate(c.BC_UTXO):
        if UTXO[0] == user:
            amounts.append([i, UTXO[1]])

    return amounts


def transitUTXO(sender, receiver, amount):
    '''
        Manage the transaction with UTXO

        sender: user id of the sender (-1 if network)
        receiver: user id of the receiver
        amount: amount send
    '''

    # If the sender is the network, add the amount in one UTXO without check
    if sender == -1:
        c.BC_UTXO.append([receiver, amount])
        return True

    senderUTXO = getUserUTXO(sender)
    senderUTXOam = [x[1] for x in senderUTXO]

    if sum(senderUTXOam) < amount:
        return False

    senderUTXOam.sort(reverse=True)

    # improved possible -> find the best combinaison of UTXO to reach the amount



    Ui = []
    Uo = 0

    if amount in senderUTXOam:
        Ui.append(amount)
    else:
        for Uam in senderUTXOam:
            if sum(Ui) < amount:
                if(sum(Ui) + Uam > amount):
                    Uo = (sum(Ui) + Uam) - amount
                Ui.append(Uam)

    # Send a full UTXO
    senderUTXOam = [x[1] for x in senderUTXO]
    for i, Uam in enumerate(Ui):
        UTXOindex = senderUTXO[senderUTXOam.index(Uam)][0]
        
        if i == len(Ui) - 1:
            Uam = Uam - Uo

        c.BC_UTXO[UTXOindex] = [receiver, Uam]
    
    # Receive the change
    if Uo:
        c.BC_UTXO.append([sender, Uo])

    print(c.BC_UTXO)

    return True

#######################
#       UTILS        #
######################

def displayBC():

    from ressources.interactions import getB64Keys
    import base64

    print (f"--------------- BLOCK-CHAIN ({len(c.BC_CHAIN)} blocks) ---------------")
    print()

    for i, b in enumerate (c.BC_CHAIN):
        print(f"--- BLOCK {i} - HASH: {base64.b64encode(getBlockHash(b)).decode()} ---")

        complete = False

        for i, t in enumerate(b):
            if isinstance(t, list):
                print(f"\tTransaction {i}: {c.BC_USERS[t[0]][1]}({t[0]}) -> {c.BC_USERS[t[1]][1]}({t[1]}) :: {t[2]}")
                print(f"\tSignature: {getB64Keys(t[3])}")
                print()
            else:
                complete = True

        if complete:
            print (f"\tPrevious block hash: {base64.b64encode(b[-2]).decode()}")
            print (f"\tBlock salt: {base64.b64encode(b[-1]).decode()}")
            print()

    print()

def arrayToBytes(array):
    '''
        Convert an array to bytes, return bytearray

        array: data to convert
    '''
    byts=b''
    for x in array:
        if not isinstance(x, (bytes, bytearray)):
            byts += str(x).encode()
        else:
            byts += x

    return byts


def getBlockHash(block):
    '''
        Get an hash of the block

        block: block to hash -> format [transaction #0, transaction #1, transaction #2, ..., hash of block n-1, salt]
    '''
    from core.hashbased.hashFunctions import sponge

    if isinstance(block, int):
        block = c.BC_CHAIN[block]

    return sponge(arrayToBytes(block), c.BC_HASH_SIZE)