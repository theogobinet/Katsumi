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
    Al = addUser("Alic")
    Bo = addUser("Bobo")

    # valid the block -> reward money to miner (Alice)
    validBlock(len(c.BC_CHAIN) - 1, Al)
    validBlock(len(c.BC_CHAIN) - 1, Al)


    # with reward, alice have enough to send to Bob
    validBlock(len(c.BC_CHAIN) - 1, Bo)

    addTransaction(Al, Bo, 20)

    validBlock(len(c.BC_CHAIN) - 1, Al)

    displayLogs()
    displayBC()

    print(validChain(Al))

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


def validChain(user):
    '''
        Check the integrity of the blockchain, return boolean
    '''

    # Reset users UTXO to follow block-chain
    c.BC_UTXO = []

    # Don't check last block as it has not been validated
    for i in range(0, len(c.BC_CHAIN) - 1):
        if not isValidBlock(i, user):
            return False
    
    return True

def isValidBlock(blockI, user, lastValidedBlock=False):
    '''
        Check block integrity: previous hash, salt, transactions signature, transactions funds

        blockI: blockI: block id corresponding of its index in the block-chain
        user: user id of the user who perform the check
        lastValidedBlock: if the check only concernes the last validated block, transactions are not performed as we suppose the network has done it.
    '''

    from core.hashbased import hashFunctions as hf

    cBlock = c.BC_CHAIN[blockI]

    for b in cBlock:
        # if it's a transaction, valid it 
        if isinstance(b, list):
            if validTransaction(user, b):
                if not lastValidedBlock:
                    transitUTXO(b[0], b[1], b[2])
            else:
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
        return False

    addLog(user, 0, [blockI])

    cBlock = c.BC_CHAIN[blockI]

    unvalidTransactions = []

    for b in cBlock:
        # if it's a transaction, valid it 

        if isinstance(b, list):
            # if the transaction is not valid, it's ingored -> removed of the block for validation
            if not validTransaction(user, b):
                addLog(user, 1, [str(b)])
                unvalidTransactions.append(b)

        else:
            # Block already validated
            addLog(user, 8, [blockI])
            return False

    for transaction in unvalidTransactions:
        cBlock.remove(transaction)


    # Calculating the hash of the previous block
    prevH = getBlockHash(c.BC_CHAIN[blockI - 1])

    # Calculating the proof of work -> mining
    addLog(user, 5, [blockI])
    proof = hf.PoW(arrayToBytes(cBlock + [prevH]), c.BC_POW_NULL)

    # POW found
    addLog(user, 6, [blockI, proof])

    # Send the validation to the block-chain
    cBlock.extend([prevH, proof])

    addLog(user, 7, [blockI])

    # Perform all transactions in 
    for t in cBlock:
        if isinstance(t, list):
            transitUTXO(t[0], t[1], t[2])
            addLog(user, 4, [str(t)])

    # Create a new block in the blockchain
    c.BC_CHAIN.append([]) 

    # Reward the miner   
    addTransaction(0, user, c.BC_MINER_REWARD)

    return True


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


def validTransaction(user, transaction):
    '''
        Verify the given transaction

        user: user if of the user who perform the check
        transaction: array containing transaction information of the format {sender ID -> receiver ID :: amount} -> signed by sender
    '''

    from core.asymmetric.elGamal import verifying

    core = transaction[:-1]
    signature = transaction[-1]

    sender = core[0]
        

    if verifying(arrayToBytes(core), getUserKey(sender, 0), signature):
        if enoughToTransit(sender, core[2]):
            return True
        else:
            addLog(user, 2, [str(transaction)])
            return False
    else:
        addLog(user, 3, [str(transaction)]) 
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


def enoughToTransit(sender, amount):
    '''
        Returns if the user have enough money to send the given amount

        sender: user id of the sender
        amount: amount send
    '''

    # if sender is the network, don't check
    if not sender:
        return True

    senderUTXO = getUserUTXO(sender)
    senderUTXOam = [x[1] for x in senderUTXO]

    return sum(senderUTXOam) >= amount


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


def addLog(user, logID, params=[]):
    c.BC_LOGS.append([user, logID, params])

#######################
#       UTILS        #
######################

def displayLogs():
    print("--------------- LOGS ---------------")
    for i, log in enumerate(c.BC_LOGS):
        user = c.BC_USERS[log[0]]
        logID = log[1]
        params = log[2]

        header = f"{i}\t{user[1]} ({user[0]})"
        core = ""

        if logID == 0:
            core = f"Start to validate block: {params[0]}"
        elif logID == 1:
            core = f"Invalid transaction ignored: {params[0]}"
        elif logID == 2:
            core = f"Not enough money for transaction: {params[0]}"
        elif logID == 3:
            core = f"Wrong signature for transaction: {params[0]}"
        elif logID == 4:
            core = f"Transaction performed: {params[0]}"
        elif logID == 5:
            core = f"Calculating POW for block: {params[0]}"
        elif logID == 6:
            core = f"Found POW for block {params[0]}: {params[1]}"
        elif logID == 7:
            core = f"Block {params[0]} validated"
        elif logID == 8:
            core = f"Block {params[0]} has already been validated"
        else:
            core = "Log ID unknown"

        print(f'{header}\t{core}')

    print()

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