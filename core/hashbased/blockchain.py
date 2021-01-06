#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from ressources import config as c

###########################
#       LIVE CHAIN        #
###########################

def network(limit, rangeTB=(10,15), rangeBS=(2,3)):
    '''
        Infinite loop that creates random users and transactions

        limit: stops when the number of block in the block-chain have reach limit

        rangeBS: range between each cycles of transactions (e.g. new cycle between every (1,2) seconds)
        rangeTB: range of transactions per cycles (e.g. between (3,5) transactions are generated per cycle)

        ex: each rand(rangeBS), rand(rangeTB) transactions are generated
    '''

    import time
    import random

    names = ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroix", "Moreau", "Simon", "Laurent", "Lefebvre", "Michel", "Garcia", "David", "Bertrand", "Roux", "Vincent", "Fournier", "Morel", "Girard", "André", "Lefèvre", "Mercier", "Dupont", "Lambert", "Bonnet", "Francois", "Matinez", "Gobinet", "Mazoin"]

    while len(c.BC_CHAIN) < limit:

        if int(time.time() % 2) or len(c.BC_USERS) <= 2:
            addUser(random.choice(names))

        nbUsers = len(c.BC_USERS)

        if len(c.BC_USERS) > 2:

            for _ in range(random.randint(rangeTB[0], rangeTB[1])):
                sender = random.randrange(1, nbUsers)
                receiver = random.randrange(1, nbUsers)

                while sender == receiver:
                    receiver = random.randrange(1, nbUsers)

                addTransaction(sender, receiver, random.randint(1, 5))

        time.sleep(random.randrange(rangeBS[0], rangeBS[1]))


def mine(user):
    '''
        Miner loop to validate a block until it has been validated by him or someone else

        user: user id of the miner
    '''

    import time
    time.sleep(1)

    cBIndex = len(c.BC_CHAIN) - 1

    index = -1
    cBlock = []
    cUTXO = []

    while cBIndex == (len(c.BC_CHAIN) - 1):

        res = validBlock(cBIndex, user, (index, cBlock, cUTXO))
        if isinstance(res, tuple) :
            index, cBlock, cUTXO = res


def startLive(limit, maxMiner):
    '''
        Main function to start the live execution of the block-chain

        limit: stops when the number of block in the block-chain have reach limit
        maxMiner: maximal number of simultaneous miner
    '''

    import threading
    import time
    import random

    c.BC_KEY_SIZE = 128

    initChain()

    tN = threading.Thread(target=network, args=(limit,))
    tN.daemon = True
    tN.start()

    cLogs = 0

    while len(c.BC_CHAIN) < limit:

        cL = len(c.BC_CHAIN)

        selectedMiner = []

        while not selectedMiner:
            nbMiner = min(len(c.BC_USERS) - 1, maxMiner)
            selectedMiner = random.sample(range(1, len(c.BC_USERS)), nbMiner)
            time.sleep(0.1)

        for miner in selectedMiner:
            tM = threading.Thread(target=mine, args=(miner,))
            tM.daemon = True
            tM.start()

        while cL == len(c.BC_CHAIN):
            cLogs = displayLogs(cLogs)
            time.sleep(0.1)

    displayLogs(cLogs)
    print()
    displayBC()

    return validChain(0)

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
    print(isValidBlock(Al, len(c.BC_CHAIN) - 1, True))


######################
#       CORE         #
######################

def initChain():
    '''
        Create the first block of the block-chain
    '''
    import time
    from core.hashbased import hashFunctions as hf

    firstBlock = [hf.sponge(b"Lorsqu'un canide aboie, ca fait BARK", c.BC_HASH_SIZE)]
    firstBlock.append(hf.PoW(arrayToBytes(firstBlock), c.BC_POW_NULL))

    c.BC_TIME_START = time.time()

    c.BC_CHAIN.append(firstBlock)
    c.BC_CHAIN.append([])

    addUser("Network")


def validChain(user):
    '''
        Check the integrity of the blockchain, return boolean
    '''

    # Reset users UTXO to follow block-chain
    UTXO = []

    # Don't check last block as it has not been validated
    for i in range(0, len(c.BC_CHAIN) - 1):
        if not isValidBlock(i, user, False, UTXO):
            print("Unvalid block: ", i)
            return False
    
    return True

def isValidBlock(blockI, user, lastValidedBlock=False, UTXO=c.BC_UTXO):
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
            if not validTransaction(user, b, UTXO):
                return False

    prevH = cBlock[-2]
    
    # do not check previous hash for first block
    if blockI:
        prevBlockH = getBlockHash(blockI-1)
    else:
        prevBlockH = prevH

    # if the previous block calculated hash is the same that the one stored and the salt is ok, block is valid
    return prevBlockH == prevH and hf.nullBits(getBlockHash(blockI), c.BC_POW_NULL)


def validBlock(blockI, user, validated=(-1, [], [])):

    '''
        Valid a block referenced by its ID, verify the transactions, calcul the hash & salt
        Block format [transaction #0, transaction #1, transaction #2, ..., hash of block n-1, salt]

        blockI: block id corresponding of its index in the block-chain
        user: id of the miner (user which validated the block)
        validated: (lastIndexChecked, [validTransactions], [UTXO state]) already validated transactions
    '''

    from core.hashbased import hashFunctions as hf

    if not user:
        return False

    addLog(user, 0, [blockI])

    # Make a copy of the current block and operate on the copy
    cBlock = c.BC_CHAIN[blockI].copy()

    # Length of block
    original = c.BC_CHAIN[blockI].copy()

    # Make a copy of current UTXO to check the transaction
    if validated[0] != -1:
        # if already validated transactions, get back the UTXO state of previous transactions
        cUTXO = validated[2]
    else:
        # No already validated transactions
        cUTXO = c.BC_UTXO.copy()

    unvalidTransactions = []

    i = 0
    for i, b in enumerate(cBlock):
        # if it's a transaction, valid it 
        
        if isinstance(b, list):

            if i > validated[0]:

                # if the transaction is not valid, it's ingored -> removed of the block for validation
                if not validTransaction(user, b, cUTXO):
                    addLog(user, 1, [transactionToString(b, cUTXO)])
                    unvalidTransactions.append(b)
            
        else:
            # Block already validated
            addLog(user, 8, [blockI])
            return False

    for transaction in unvalidTransactions:
        cBlock.remove(transaction)

    cBlock = validated[1] + cBlock[validated[0] + 1:]

    # Calculating the hash of the previous block
    prevH = getBlockHash(c.BC_CHAIN[blockI - 1])

    if(c.BC_CHAIN[blockI] != original):
        addLog(user, 9, [blockI])
        return (i, cBlock, cUTXO)

    # Calculating the proof of work -> mining
    addLog(user, 5, [blockI])
    proof = hf.PoW(arrayToBytes(cBlock + [prevH]), c.BC_POW_NULL, ('BC_CHAIN', blockI))

    if not proof:
        addLog(user, 9, [blockI])
        return (i, cBlock, cUTXO)

    # POW found
    addLog(user, 6, [blockI, proof])

    if(c.BC_CHAIN[blockI] != original):
        addLog(user, 9, [blockI])
        return (i, cBlock, cUTXO)

    # Send the validation to the block-chain by validating the real block
    c.BC_CHAIN[blockI] = cBlock + [prevH, proof]

    addLog(user, 7, [blockI])

    # Perform all transactions in 
    for t in cBlock:
        if isinstance(t, list):

            if not transitUTXO(t[0], t[1], t[2]):
                raise Exception("Valided transaction can't be proceeded")

            addLog(user, 4, [transactionToString(t)])

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
    addLog(0, 10, [len(c.BC_CHAIN) - 1, transactionToString(transaction)])


def getUserKey(user, key):
    '''
        Get the corresponding key of the user reprensented by its user id

        user: user id
        key: key type: 0 -> public key, 1 -> private key
    '''
    
    return c.BC_USERS[user][2 + key]


def validTransaction(user, transaction, UTXO=c.BC_UTXO):
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
        if transitUTXO(sender, core[1], core[2], UTXO):
            return True
        else:
            addLog(user, 2, [transactionToString(transaction, UTXO)])
            return False
    else:
        addLog(user, 3, [transactionToString(transaction, UTXO)]) 
        return False


def getUserBalance(user, UTXO=c.BC_UTXO):
    return sum([x[1] for x in getUserUTXO(user, UTXO)])


def getUserUTXO(user, UTXO=c.BC_UTXO):
    '''
        Get a list containing the amount of each UTXO for a given user

        user: user id
    '''

    amounts = []
    for i, u in enumerate(UTXO):
        if u[0] == user:
            amounts.append([i, u[1]])

    return amounts


def transitUTXO(sender, receiver, amount, UTXO=c.BC_UTXO):
    '''
        Manage the transaction with UTXO

        sender: user id of the sender (0 if network)
        receiver: user id of the receiver
        amount: amount send
        UTXO: array of UTXO to use instead of default one: c.BC_UTXO
    '''

    # If the sender is the network, add the amount in one UTXO without check

    if not sender:
        UTXO.append([receiver, amount])
        return True

    if not receiver:
        raise ValueError("Network can't be the destination of any transaction")

    senderUTXO = getUserUTXO(sender, UTXO)
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

        UTXO[UTXOindex] = [receiver, Uam]
    
    # Receive the change
    if Uo:
        UTXO.append([sender, Uo])

    return True


def addLog(user, logID, params=[]):
    import time
    c.BC_LOGS.append([time.time() - c.BC_TIME_START, user, logID, params])


#######################
#       UTILS        #
######################

import base64

class bcolors:
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def transactionToString(transaction, UTXO=c.BC_UTXO):

    from ressources.interactions import getB64Keys

    sender = c.BC_USERS[transaction[0]]
    receiver = c.BC_USERS[transaction[1]]

    senderBalance = getUserBalance(sender[0], UTXO)
    receiverBalance = getUserBalance(receiver[0], UTXO)


    return f"{'{'}{sender[0]}.{sender[1]} ({senderBalance} $) -> {receiver[0]}.{receiver[1]} ({receiverBalance} $) :: {transaction[2]} ${'}'} -> {getB64Keys(transaction[3])}"


def displayLogs(last=0):

    if not c.BC_LOGS:
        return 0

    if not last:
        print("--------------- LOGS ---------------")

    i = 0
    for i, log in enumerate(c.BC_LOGS):

        if i > last or not last:

            time = log[0]
            user = c.BC_USERS[log[1]]

            if len(user) <= 10:
                user+='\t'

            logID = log[2]
            params = log[3]

            header = f"{i}\t{'{:.2f}'.format(time)}\t{user[1]} ({user[0]})"
            core = ""

            if logID == 0:
                core = f"Start to validate block: {params[0]}"
            elif logID == 1:
                core = f"{bcolors.FAIL}Invalid transaction ignored: {params[0]}{bcolors.ENDC}"
            elif logID == 2:
                core = f"{bcolors.FAIL}Not enough money for transaction: {params[0]}{bcolors.ENDC}"
            elif logID == 3:
                core = f"{bcolors.FAIL}Wrong signature for transaction: {params[0]}{bcolors.ENDC}"
            elif logID == 4:
                core = f"{bcolors.OKGREEN}Transaction performed: {params[0]}{bcolors.ENDC}"
            elif logID == 5:
                core = f"Calculating POW for block: {params[0]}"
            elif logID == 6:
                core = f"{bcolors.OKGREEN}Found POW for block {params[0]}: {base64.b64encode(params[1]).decode()}{bcolors.ENDC}"
            elif logID == 7:
                core = f"{bcolors.OKGREEN}Block {params[0]} validated{bcolors.ENDC}"
            elif logID == 8:
                core = f"{bcolors.WARNING}Block {params[0]} has already been validated{bcolors.ENDC}"
            elif logID == 9:
                core = f"{bcolors.WARNING}Block {params[0]} changed before POW calculation{bcolors.ENDC}"
            elif logID == 10:
                core = f"{bcolors.OKCYAN}Transaction added to block {params[0]}: {params[1]}{bcolors.ENDC}"
            else:
                core = "Log ID unknown"

            if len(header) <= 25:
                header+='\t'

            print(f'{header}\t{core}')

    return i

def displayBC():

    print (f"{bcolors.BOLD}==================== BLOCK-CHAIN ({len(c.BC_CHAIN)} blocks) ===================={bcolors.ENDC}")
    print()

    print(f"{bcolors.BOLD}USERS:{bcolors.ENDC}")
    for i, u in enumerate(c.BC_USERS):
        print(f"\t{u[1]}({u[0]}): {getUserBalance(u[0])} $")

    print()
    print()

    for i, b in enumerate (c.BC_CHAIN):
        print(f"{bcolors.BOLD}BLOCK {i} - HASH: {base64.b64encode(getBlockHash(b)).decode()}{bcolors.ENDC}")
        print()

        complete = False

        print(f"\t{bcolors.OKCYAN}Transactions:{bcolors.ENDC}")
        for i, t in enumerate(b):
            if isinstance(t, list):
                print(f'\t\t{i}: {transactionToString(t)}')
            else:
                complete = True
        print()

        if complete:
            print (f'\t{bcolors.OKGREEN}Block has been validated:{bcolors.ENDC}')
            print (f"\t\tPrevious block hash: {base64.b64encode(b[-2]).decode()}")
            print (f"\t\tBlock salt: {base64.b64encode(b[-1]).decode()}")
            print()
        else:
            print (f'\t{bcolors.WARNING}Block has not been validated yet{bcolors.ENDC}')

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