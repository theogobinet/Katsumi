#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from ressources import config as c

######################
#       TESTS        #
######################

def createTestBC():

    c.BC_KEY_SIZE = 128

    # create the 1st block
    initChain()

    # create 2 users
    Al = addUser("Alice")

    # valid the block -> reward money to miner (Alice)
    validBlock(len(c.BC_CHAIN) - 1, Al)
    validBlock(len(c.BC_CHAIN) - 1, Al)

    Bo = addUser("Bob")

    # with reward, alice have enough to send to Bob
    addTransaction(Al, Bo, 10)

    validBlock(len(c.BC_CHAIN) - 1, Al)

    displayBC()

    print(validChain())

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

    addUser("Network")


def validChain():
    '''
        Check the integrity of the blockchain, return boolean
    '''

    # Don't check last block as it has not been validated
    for i in range(0, len(c.BC_CHAIN) - 1):
        if not isValidBlock(i):
            return False
    
    return True

def isValidBlock(blockI):
    '''
        Check transactions sinature without performing them, check block integrity (previous hash & salt)

        blockI: blockI: block id corresponding of its index in the block-chain
    '''

    from core.hashbased import hashFunctions as hf

    cBlock = c.BC_CHAIN[blockI]

    for b in cBlock:
        # if it's a transaction, valid it 
        if isinstance(b, list):
            if not validTransaction(b, False):
                return False

    prevH = cBlock[-2]
    
    # do not check previous hash for first block
    if blockI:
        prevBlockH = getBlockHash(blockI-1)
    else:
        prevBlockH = prevH

    # if the previous block calculated hash is the same that the one stored and the salt is ok, block is valid
    return prevBlockH == prevH and hf.nullBits(getBlockHash(blockI), c.BC_POW_NULL)


def validBlock(blockI, user):

    '''
        Valid a block referenced by its ID, verify the transactions, calcul the hash & salt
        Block format [transaction #0, transaction #1, transaction #2, ..., hash of block n-1, salt]

        blockI: block id corresponding of its index in the block-chain
        user: id of the miner (user which validated the block)
    '''

    from core.hashbased import hashFunctions as hf

    if not user:
        raise ValueError("Network can't valid block")

    cBlock = c.BC_CHAIN[blockI]

    unvalidTransactions = []

    for b in cBlock:
        # if it's a transaction, valid it 

        if isinstance(b, list):
            # if the transaction is not valid, it's ingored -> removed of the block for validation
            if not validTransaction(b):
                unvalidTransactions.append(b)

        else:
            raise Exception("Block seems to have already been validated or it's corrupted")

    for transaction in unvalidTransactions:
        cBlock.remove(transaction)


    # Adding the hash of the previous block
    cBlock.append(getBlockHash(c.BC_CHAIN[blockI - 1]))

    # Block validation -> calcul of proof of work
    cBlock.append(hf.PoW(arrayToBytes(cBlock), c.BC_POW_NULL))

    # Create a new block in the blockchain
    c.BC_CHAIN.append([])  

    # Reward the miner   
    addTransaction(0, user, c.BC_MINER_REWARD)


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


def validTransaction(transaction, perform=True):
    '''
        Verify the given transaction signature, and perform the UTXO exchange if perform is true

        transaction: array containing transaction information of the format {sender ID -> receiver ID :: amount} -> signed by sender
    '''

    from core.asymmetric.elGamal import verifying

    core = transaction[:-1]
    signature = transaction[-1]

    sender = core[0]

    isValid = verifying(arrayToBytes(core), getUserKey(sender, 0), signature)

    if isValid and perform:
        return transitUTXO(sender, core[1], core[2])
    elif isValid:
        return True
    else:
        return False


def getUserBalance(user):
    return sum([x[1] for x in getUserUTXO(user)])

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
    if not sender:
        c.BC_UTXO.append([receiver, amount])
        return True

    if not receiver:
        raise ValueError("Network can't be the destination of any transaction")

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

    return True

#######################
#       UTILS        #
######################

def displayBC():

    from ressources.interactions import getB64Keys
    import base64

    print (f"--------------- BLOCK-CHAIN ({len(c.BC_CHAIN)} blocks) ---------------")
    print()

    print("USERS:")
    for i, u in enumerate(c.BC_USERS):
        print(f"\t{u[1]}({u[0]}): {getUserBalance(u[0])}")

    print()

    for i, b in enumerate (c.BC_CHAIN):
        print(f"--- BLOCK {i} - HASH: {base64.b64encode(getBlockHash(b)).decode()} ---")
        print()

        complete = False

        print("Transactions:")
        for i, t in enumerate(b):
            if isinstance(t, list):
                print(f"\tTransaction {i}: {c.BC_USERS[t[0]][1]}({t[0]}) -> {c.BC_USERS[t[1]][1]}({t[1]}) :: {t[2]}")
                print(f"\tSignature: {getB64Keys(t[3])}")
                print()
            else:
                complete = True
        print()

        if complete:
            print (f'Block has been validated:')
            print (f"\tPrevious block hash: {base64.b64encode(b[-2]).decode()}")
            print (f"\tBlock salt: {base64.b64encode(b[-1]).decode()}")
            print()
        else:
            print (f'Block has not been validated yet')

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