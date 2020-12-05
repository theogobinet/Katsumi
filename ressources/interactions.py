#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.asymmetric.diffieHellman import agreement
from math import inf
import os
import time

from ressources import prng
from . import asciiWarehouse as asc 
from datetime import datetime

import ressources.config as config
import ressources.bytesManager as bm 

################################################
###############- Console Interactions - ########
################################################


def enumerateMenu(choices):
    """
    Menu enumeration
    """
    for i,elt in enumerate(choices):
        print(f"\t({i+1}) - {elt}")

    print()


def query_yn(question, default="yes"):
    """Ask a yes/no question via input() and return their answer."""

    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}

    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        choice = input(question + prompt).lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def clear():
    """Clearing the screen."""
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")


def readFromUser(msg="Enter the message:"):
    from sys import stdin

    phrase=""

    print(msg)
    
    for line in stdin:
        if line == '\n': # If empty string is read then stop the loop
            break
        else:
            phrase+=line

    # [:-1] to delete the last '\n'
    return phrase[:-1]

##############################
# LOOP FUNCTION TO GET INPUT #
##############################

def getFile():

    print("Please enter the filename with its extension (source folder is processing):")

    while True:
        f = input("> ")
        if f == "c":
            return None
        elif isFileHere(f, config.DIRECTORY_PROCESSING):
            return config.DIRECTORY_PROCESSING + f
        else:
            print(f"Error: file '{f}' not found, enter [c] to go back or enter a valid filename:")

        
def getInt(default=256, expected="hash", size=False, limit:int=inf):
    print(f"Enter {expected} ({default} by default):")

    while True:
        i = input("> ")
        if i == "c":
            return None
        elif i == "":
            return default
        else:
            try:
                val = int(i)
                if val >= 0 and (not size or (val % 8 == 0 and val >=32)) and val <= limit:
                    return val
                else:
                    print(f"Error: {i} is not a valid {expected}, leave blank or enter a valid {expected}:")
                
            except ValueError:
                print(f"'{i}' is not an integer, leave blank or enter a valid {expected}:")


def getb64(expected="message", size=-1):
    import base64
    import binascii

    print(f"Enter {expected} in base64:")
    while True:
        i = input("> ")
        if i == "c":
            return None
        else:
            try:
                data = base64.b64decode(i)
                if size == -1 or len(data) == size:
                    return data
                else:
                    print(f'Error: {expected} must be {size} bytes long, enter [c] to go back or enter a valid base64')
            except binascii.Error:
                print('Error: Unable to decode, the format is not in base64, enter [c] to go back or enter a valid base64')


def cipher_choice():

    clear()
    asc.asciiCat()

    print("Choice cypher method : ")
    print(" 1 - ECB \n 2 - CBC \n 3 - PCBC (Recommended) \n 4 - CTR (Stream) \n 5 - CGM (Authentification)")

    pCipher=getInt(3,"choices")

    # Cipher verification
    if pCipher > 5 :
        print("Error: You didn't choose a cipher properly.")
        time.sleep(1)

        from katsumi import menu
        menu()

    elif pCipher == 1:
        answer=query_yn("ECB is not recommended for use in cryptographic protocols. Are you sure ?")
        if answer:
            clear()
            return pCipher
        else: 
            clear()
            return cipher_choice()
        
    clear()
    asc.asciiCat()

    return pCipher



################################################
###############- File Manager - ################
################################################

def findFile(ext="",directory=config.DIRECTORY_PROCESSING):
    """
    To find a file given extension and return is name.
    """

    name=""

    if ext=="":
        # Return the first file in the directory that is not crypted
        for f in os.listdir(directory):
            if not(f.endswith("kat")):
                name=f
    else:
        for f in os.listdir(directory):
            if f.endswith(ext):
                name=f

    return name

def isFileHere(name:str,directory=config.DIRECTORY_GEN):
    """Return if given name file's is here or is not."""
    return os.path.isfile(directory+name)

def handleDirectory(dirName:str,directory=config.DIRECTORY_GEN):
    """ If given directory doesn't exist, then create it. """
    if not os.path.exists(directory+dirName):
        os.makedirs(directory+dirName)

def rmFile(name:str,directory=config.DIRECTORY_GEN):
    """Remove named file."""
    try:
        return os.remove(directory+name)
    except FileNotFoundError:
        pass


def mvFile(name:str,src=config.DIRECTORY_PROCESSING,dst=config.DIRECTORY_GEN):
    """ Move named file """
    import shutil
    return shutil.move(src+name,dst)

def whatInThere(directory=config.DIRECTORY_FOUNT):
    """
    Return elements present in given directory in list format.
    """
    return [os.path.splitext(f)[0] for f in os.listdir(directory)]

def writeVartoFile(var:object,name:str,directory=config.DIRECTORY_GEN,ext:str=".txt"):
    """Write given variable into a file with variable name"""
    # r+ for reading and writing
    name=directory+name
    with open(name+ext,"w+") as f:
        f.truncate(0)
        f.write(f"{var}")

    return True

def extractVarFromFile(fileName:str,directory=config.DIRECTORY_GEN,ext:str=".kat"):
    """Extract variable contenant's from txt file."""
    import ast
    with open(directory+fileName+ext,"r+") as f:
        contents=f.read()
        extracted=ast.literal_eval(contents)

    return extracted

##############################
######## Key gestion #########
##############################

def getIntKey(b64, keyNumber):
    """
    Convert base64 key's into tuples of keyNumber integers.
    """
    import base64, binascii

    if isinstance(keyNumber,str):
        keyNumber = int(keyNumber)

    try:
        data = base64.b64decode(b64)
    except binascii.Error:
        # then it's already into b64 logically
        data = b64

    if keyNumber != 1:
        keys = ()
        kL = []
        for i in range(keyNumber):
            kL.append(int.from_bytes(data[i*2:i*2+2],"big"))

        padding = keyNumber * 2
        for i, s in enumerate(kL):
            keys += (int.from_bytes(data[padding: padding + s], "big"),)
            padding = padding + s
    else:
        keys = bm.bytes_to_int(data)

    return keys

def writeKeytoFile(key,fileName:str,directory=config.DIRECTORY_PROCESSING,ext:str=".kpk"):
    """
    Write key in b64 format to file .kpk with key length's as header.
    """

    def getB64Keys(key):
        import base64
        sizes = []
        tw = bytearray()

        if isinstance(key,tuple):
            for k in key:
                s = bm.bytes_needed(k)
                sizes.append(s)
                # Put the size into the coded b64
                tw += s.to_bytes(2,"big")

            for i, k in enumerate(key):
                tw += k.to_bytes(sizes[i], "big")
        else:
            #uniq key
            tw = bm.int_to_bytes(key)

        return base64.b64encode(tw).decode()

    if isinstance(key,tuple):
        size = len(key)
    else:
        size = 1
          
        

    b64Key = getB64Keys(key)

    b64Key = str(size) + b64Key

    writeVartoFile(b64Key,fileName,directory,ext)

    return b64Key


def extractKeyFromFile(fileName:str,directory=config.DIRECTORY_PROCESSING,ext:str=".kpk"):
    """
    Extract key's from b64 format to tuples from katsumi public/private keys file's.
    """

    fileName += ext
    if isFileHere(fileName, directory):
        f = open(os.path.join(directory, fileName),"r+")
        b64data = f.read()
        f.close()

        size = b64data[0]

        return getIntKey(b64data[1:], size)
        
    else:
        raise FileNotFoundError(f"File {fileName} not found")


def askForKey():
    import base64

    clear()
    asc.asciiCat()

    answer=query_yn("You have not yet defined a key, you want to enter one?","no")

    key = bytearray()

    if answer:
        key = getb64("key", 16)

        if not key:
            katsuSymm()

    else:
        import secrets as sr
        key = sr.randbits(128).to_bytes(16,"big")
        print("Your key was randomly generated:", base64.b64encode(key).decode())
    
    answer=query_yn("Do you want to keep your key in cache ?")
    
    if answer:
        config.KEY = key

    return key

##############################
######## Inversion Box #######
##############################

def handleInvBox():

    if not isFileHere("inversion_Sbox.txt"):

        print("A necessary file for the substitution has been deleted from the system.\n")

        if query_yn("- Do you want to generate the inverse substitution box (No if you want to compute each time needed) ? "):
   
            import threading
            import time

            import core.symmetric.galois_Z2 as gz2

            th=threading.Thread(target = gz2.genInverses2)
            
            # This thread dies when main thread (only non-daemon thread) exits.
            th.daemon = True

            th.start()
            time.sleep(2)

        else:
            config.GALOIS_WATCH = True
    
    else:

        config.INVERSIONS_BOX=extractVarFromFile("inversion_Sbox",ext=".txt")

        if len(config.INVERSIONS_BOX) != config.NBR_ELEMENTS:
            rmFile("inversion_Sbox.txt")
            print("WARNING - Wrong Inversion Substition box ! \n")
            clear()
            handleInvBox()


def doSomethingElse(m=None):
    """
    Ask user if he want to do something and if yes, get back to main menu.
    """
    answer = query_yn("\nDo you want to do something else ?")
    import katsumi

    if m == None:
        m = katsumi.menu

    print()

    if answer:
            clear()
            return m()
    else:
        clear()
        return katsumi.work_with_selection(11)

#########################################
##### Prime number's fount gestion ######
#########################################

def extractSafePrimes(nBits:int=1024,allE:bool=True,easyGenerator:bool=False,directory:str=config.DIRECTORY_FOUNT):
    """
    Return list of tuples (Safe_Prime,Sophie_Germain_Prime) for given n bits.
    If list doesn't exist, create one with 1 tuple.

    all :
        - True for all list
        - False for one random tuple
    """
    name = f"{str(nBits)}_bits"

    if not isFileHere(name+".txt",directory):
        print("File doesn't exist. Creating it with one element.")
        stockSafePrimes(nBits,0)
        extractSafePrimes(nBits,allE,easyGenerator,directory)
    else:
        v = extractVarFromFile(name,directory,".txt")

        if allE:
            return v
        else:
            import ressources.utils as ut

            s = ut.randomClosureChoice(v)

            if easyGenerator:
                from core.asymmetric.elGamal import isEasyGeneratorPossible

                if not isEasyGeneratorPossible(s):
                    while len(s) != 0 and not isEasyGeneratorPossible(s):
                        s = ut.randomClosureChoice(v)
                        print(s,v)
                    
                    if len(s) == 0 and not isEasyGeneratorPossible(s):
                        # It's the only ramaining element and it's not possible to use easy gen with him.
                        print("No safe prime available for easy generator creation into current {nBits} bits fountain's.")

                        question = query_yn("Do you want to generate one compatible with this condition (It can be long) ? ")

                        if question:
                            s = prng.safePrime(nBits,easyGenerator=True)
                            updatePrimesFount(s,nBits)
                        else:
                            return elGamalKeysGeneration()
                else:
                    return s
            else:
                return s

def stockSafePrimes(n:int=1024,x:int=15,randomFunction=prng.xorshiftperso):
    """ 
    Stock x tuples of distincts (Safe prime, Sophie Germain prime) into a fount of given n bits length.
    """

    assert x > 0
    # Create an appropriated directory.
    handleDirectory("PrimeNumber's_Fount")
    
    # Safety check, if already exist, then you just update it !
    if isFileHere(f"{str(n)}_bits.txt",config.DIRECTORY_FOUNT):
        print("\nData concerning this number of bits already exists. Update in progress.")
        Update = True
    else:
        print("\nData not existing, creating file...")
        Update = False

    if Update:
        fount = extractSafePrimes(n)
        
    else:
        fount = []
    
    print(f"Computing in progress. Please wait ...")

    prng.genSafePrimes(x,fount,n,randomFunction)

    print(f"Generation completed.\n")

    writeVartoFile(fount,f"{str(n)}_bits",config.DIRECTORY_FOUNT)

def updatePrimesFount(p:tuple,nBits:int):
    """
    Update prime number's fount (or create one with one element if not exist) and add given tuple if not present in stocked ones.
    """
    name = f"{str(nBits)}_bits"

    if not isFileHere(name+".txt",config.DIRECTORY_FOUNT):
        print("\nData not existing, creating file...")
        stockSafePrimes(nBits,0)
        updatePrimesFount(p,nBits)

    else:

        buffer = extractVarFromFile(name,config.DIRECTORY_FOUNT,".txt")

        if p not in buffer:
            buffer.append(p)
            writeVartoFile(buffer,name,config.DIRECTORY_FOUNT)
            print(f"{p} successfully added to prime number's fount.\n")
        else:
            print(f"{p} already into prime number's fount. Not added.\n")
        

def primeNumbersFountain():
    """
    Deal with prime number's fountain.
    """

    clear()
    asc.asciiArt()

    print("The Foutain contains:")
    for elt in whatInThere():
        print(f"\t > {elt}")
    
    choices = ["Generate and stock safe primes","Update a list","Delete a list","Back to menu"]

    print("\n")
    enumerateMenu(choices)

    selection = getInt(2,"choices")

    def doSomethingFount(i:int):
        """ Handle choices for fountain. """
        clear()
        asc.asciiArt()
        if i == 1:
            print("How many bits wanted for this generation ?")
            wanted = getInt(2048,"bits size",True)

            print("\nHow many generations ?")
            numbers = getInt(1,"generations")

            stockSafePrimes(wanted,numbers)

            return doSomethingElse(primeNumbersFountain)

        elif i == 2:
            print("Enter number of bits for updating corresponding one's :")
            wanted = getInt(2048,"bits size",True)

            print("\nHow many generations ?")
            numbers = getInt(1,"generations")

            stockSafePrimes(wanted,numbers)
            return doSomethingElse(primeNumbersFountain)
        
        elif i == 3:
            clear()
            asc.asciiDeath()
            print("Enter the number of bits corresponding to the list you would like to be removed.")
            lnumber = getInt(2048,"bits size",True)
            name = f"{str(lnumber)}_bits.txt"

            if query_yn("Are you sure ?"):
                rmFile(name,config.DIRECTORY_FOUNT)
                print(f"{name} removed successfully.\n")
                return doSomethingElse(primeNumbersFountain)
            else:
                doSomethingFount()

        elif i == 4:
            import katsumi
            katsumi.menu()
        else:
            clear()
            print("\n Not available. Getting back...")
            time.sleep(1)
            return primeNumbersFountain()
        
    return doSomethingFount(selection)


#########################################
########## El Gamal Gestion #############
#########################################

def elGamalKeysGeneration():
    """
    Dealing with conditions for elGamal key generation.
    """
    from core.asymmetric import elGamal

    clear()
    asc.asciiCat()

    # Because here default is no so not(yes)
    if not query_yn("Do you want to use the fastest ElGamal key generation's (default: no) ?","no"):
        
        if query_yn("Do you want to choose the length of the key (default = 2048 bits) ?","no"):
            n = getInt(2048,"key size",True)
        else:
            n = 2048

        eGen = query_yn("Do you want to use easy Generator (fastest generation) (default: No) ?","no")

        if query_yn("Do you want to use the Prime Number's Fountain to generate the keys (fastest) (default: yes) ?"):
            primes = extractSafePrimes(n,False,eGen)
        else:
            primes = None

        clear()
        asc.asciiCat()

        print("\t.... Key generation in progress ....")
        
        elGamal.key_gen(n,primes,eGen,prng.xorshiftperso,True,True)
    else:
        n = 1024
        primes = extractSafePrimes(n,False)

        clear()
        asc.asciiCat()

        print("\t.... Key generation in progress ....")

        elGamal.key_gen(n,primes,saving=True,Verbose=True)

    doSomethingElse(katsuAsymm)
    


def keysVerif(verif:bool=True):
    """
    Used to verify existence of private or/and public keys of ElGamal.
    """

    clear()
    asc.asciiCat()

    print("\nChecking the presence of keys in the system....")

    if isFileHere("public_key.kpk",config.DIRECTORY_PROCESSING):

        from core.asymmetric import elGamal as elG

        publicS = elG.getSize()
        print(f"\nPublic key's of {publicS} bits already here.\n")

        if isFileHere("private_key.kpk",config.DIRECTORY_PROCESSING):
            
            privateS = elG.getSize("private_key")
            print(f"Private key's of {privateS} bits too.\n")

            if publicS != privateS:
                clear()
                asc.asciiDeath()
                print(f"Key sizes do not match ({privateS} != {publicS}). Suspected corruption.")
                
                if query_yn("Do you want to delete them ?"):
                    
                    print("Keys are going to be deleted...")
                    for f in ["public_key","private_key"]:
                        rmFile(f+".kpk",config.DIRECTORY_PROCESSING)

                    clear()
                    asc.asciiDeath()
                    print("Done. Generating other keys now...\n")
                    time.sleep(1)
                    clear()
                    asc.asciiCat()

            else:
                if verif and not query_yn("Do you want to keep them ? (default: No)","no"):
                    rmFile("public_key.kpk",config.DIRECTORY_PROCESSING)
                    rmFile("private_key.kpk",config.DIRECTORY_PROCESSING)
                    rmFile("encrypted.kat",config.DIRECTORY_PROCESSING)
                else:
                    clear()
                    asc.asciiCat()

        else:
            print("Private key's missing.\n")
        
            if query_yn("Do you want to add them now ?\n"):

                while not isFileHere("private_key.kpk",config.DIRECTORY_PROCESSING):
                    clear()
                    input("Please put your 'private_key.kpk' file into the 'processing' folder.")
                
                clear()
                print("Gotcha !")

                keysVerif()
            else:
                katsuAsymm()

    elif isFileHere("private_key.kpk",config.DIRECTORY_PROCESSING):
        print("\nPrivate key's already here but not public one's.\n")

        if query_yn("Do you want to add them now ? ( default: No)\n","no"):

                while not isFileHere("public_key.kpk",config.DIRECTORY_PROCESSING):
                    clear()
                    input("Please put your 'public_key.kpk' file into the 'processing' folder.")
                
                clear()
                print("Gotcha !")

                keysVerif()
        else:
            katsuAsymm()

    else:
        elGamalKeysGeneration()

def dlogAttack():
    
    from core.asymmetric import elGamal
    clear()
    asc.asciiJongling()

    choices = ["Retieve private key with publicKey","Decrypt encrypted message.","Back to menu"]

    enumerateMenu(choices)

    selection = getInt(1,"choices")

    def doSomething(i:int):
        """ Handle choices for dlog attack. """

        clear()
        asc.asciiJongling()

        if i == 1:

            while not isFileHere("public_key.kpk",config.DIRECTORY_PROCESSING):
                clear()
                asc.asciiJongling()

                input("Please put your 'public_key.kpk' file into the 'processing' folder.")
            
            clear()
            asc.asciiJongling()
            print("Gotcha !\n")

            print("Compute dlog attack with pollard's rho algorithm.")
            print("It can takes times ...\n")

            el = elGamal.delog(extractVarFromFile("public_key.kpk",config.DIRECTORY_PROCESSING),None,True)
            
            writeVartoFile(el,"private_key",config.DIRECTORY_PROCESSING)
            
            print(f"Saved private_key : {el} into appropriated file.\n")

            doSomethingElse(dlogAttack)

        elif i == 2:

            while not isFileHere("public_key.kpk",config.DIRECTORY_PROCESSING):
                clear()
                asc.asciiJongling()

                input("Please put your 'public_key.kpk' file into the 'processing' folder.")
            
            clear()
            asc.asciiJongling()
            print("Gotcha !\n")
            
            while not isFileHere("encrypted.kat",config.DIRECTORY_PROCESSING):
                clear()
                asc.asciiJongling()

                input("Please put your 'encrypted.kat' file into the 'processing' folder.")
            
            clear()
            asc.asciiJongling()
            print("Gotcha !\n")

            print("Compute dlog attack with pollard's rho algorithm.")
            print("It can takes some times...\n")

            el = elGamal.delog(extractKeyFromFile("public_key",config.DIRECTORY_PROCESSING),extractKeyFromFile("encrypted",config.DIRECTORY_PROCESSING),True)
            
            print(f"Decrypted message is:")

            el = el.split("\n")
            print(el)

            for phrase in el:
                print(f"\t -'{phrase}'")

            doSomethingElse(dlogAttack)
        
        elif i == 3:
            import katsumi
            katsumi.menu()
        else:
            
            dlogAttack()
        
    doSomething(selection)

#########################################
########## Diffie Hellman ###############
#########################################
def dHgestion():
    """
    Sharing private key with Diffie Hellman.
    """
    import core.asymmetric.diffieHellman as dH

    choices = ["Choose agreement","Process with agreement","Back"]

    clear()
    asc.asciiKeys()

    enumerateMenu(choices)

    selection = getInt(2,"choices")

    def doSomethingDH(i:int):
        
        if i == 1:
            clear()
            asc.asciiKeys()

            print("On what size n (bits) did you agree with your penpal?")

            size = getInt(2048,"bits size",True)

            clear()
            asc.asciiKeys()

            print(f"Checking existence of fountain of {size} bits...")

            if not isFileHere(f"{size}_bits.txt",config.DIRECTORY_FOUNT):
                print("\n\tFile unavailable !")
                print("\n\fOne will be created.\n")
                fountain = False
            else:
                print("\n\tFile available !\n")
                fountain = True

            accord = dH.agreement(size,fountain)

            accord = writeKeytoFile(accord,"dH_agreement")
            print(f"According to the size of the private key, your agreement is: {accord} ")

            doSomethingElse(dHgestion)

        elif i == 2:
            clear()
            asc.asciiKeys()

            if query_yn("Do you want to use the dH_agreement.kat file's ? (default: Yes)"):
                accord = extractKeyFromFile("dH_agreement")
            else:
                accord = getIntKey(getb64("agreement"),2)

            print(f"\nNow, choose a secret value into [0,{accord[0]}]")
            
            import random as rd
            
            secret = getInt(rd.randrange(2,accord[0]),"your secret integer",False,accord[0])

            clear()
            asc.asciiKeys()

            dH.chooseAndSend(accord,secret,saving=True,Verbose=True)

            clear()
            asc.asciiKeys()

            dH_shared = dH.compute(accord,secret,saving=True,Verbose=True)
            
            clear()
            asc.asciiKeys()

            print("Shared key created.")
            print(f"\t > {dH_shared}\n")

            doSomethingElse(dHgestion)

            

        elif i == 3:
            import katsumi
            katsumi.menu()
        else:
            dHgestion()

    doSomethingDH(selection)


#########################################
############ Other Menus  ###############
#########################################

def katsuSymm():

    import core.symmetric.ciphers as ciphers
    import katsumi

    clear()
    asc.asciiCat()

    symmetric_choices=["Encrypt a message.", "Decrypt a message.","Back"]
    
    enumerateMenu(symmetric_choices)

    selection = getInt(1,"choices")

    def doSomethingSymm(i:int):
        """ Handle choices for symmetric things. """

        clear()
        asc.asciiCat()

        if i in [1,2]:

            if not config.KEY:
                key = askForKey()
            else:
                key = config.KEY

        if i == 1:
            # Encryption
            cipher = cipher_choice()
            
            aad = ""
            inFile = ""

            if cipher == 5:
                if query_yn("GCM allows to store authentified additional data (not encrypted), do you want to store some AAD ?"):
                    aad = readFromUser()
                else: 
                    clear()
                    asc.asciiCat()

            if query_yn("Do you want to encrypt a file ?"):
                inFile = getFile()
                if inFile:
                    data = bm.fileToBytes(inFile)
                else:
                    katsuSymm()
            else:
                data = readFromUser().encode()


            print("Encryption started....")

            begin_time = datetime.now()
            print(ciphers.run(data, inFile, True, cipher, aad, key))
            end=datetime.now() - begin_time
            input(f"Encryption finished in {end} seconds !\n")

            clear()
            asc.asciiCat()

            doSomethingElse(katsuSymm)

        elif i == 2:
        
            # Decryption    
            cipher = cipher_choice()
            inFile = False

            if query_yn("Do you want to decrypt a file ?"):
                inFile = getFile()
                if inFile:
                    data = bm.fileToBytes(inFile)
                else:
                    katsuSymm()
            else:
                data = getb64()
                if not data:
                    katsuSymm()


            print("Decryption started....")

            begin_time = datetime.now()
            print(ciphers.run(data, inFile, False, cipher, "", key))
            end = datetime.now() - begin_time
            input(f"Decryption finished in {end} seconds !")

            clear()
            asc.asciiCat()
            doSomethingElse(katsuSymm)
        
        elif i == 3:
            clear()
            katsumi.menu()
        else:
            
            katsuSymm()
        
    doSomethingSymm(selection)


def katsuAsymm():

    import katsumi
    import core.asymmetric.elGamal as elG

    clear()
    asc.asciiCat()

    asymmetric_choices= ["Using ElGamal to generate public/private key pairs.","Encrypt a message with ElGamal","Decrypt a message encrypted by ElGamal.","Share private key with Diffie-Hellman.","Discrete Logarithmic attack on ElGamal.","Keys deletion","Back"]

    enumerateMenu(asymmetric_choices)

    selection = getInt(2,"choices")

    def doSomethingAssym(i:int):
        """ Handle choices for symmetric things. """
        clear()
        asc.asciiCat()

        if i == 1:
            print("You are going to generate public/private key pairs with ElGamal algorithm.")
            time.sleep(1)
            keysVerif()
            elGamalKeysGeneration()

        elif i == 2:
            
            if not isFileHere("public_key.kpk",config.DIRECTORY_PROCESSING):
                print("No public key found into the system...")
                time.sleep(1)
                doSomethingAssym(1)
            else:
                keysVerif(verif=False)
                answer = readFromUser().encode()
                e = elG.encrypt(answer,extractKeyFromFile("public_key",config.DIRECTORY_PROCESSING),saving=True)

                print(f"Saved encrypted message: {e} into appropriated file.")

                doSomethingElse(katsuAsymm)

        elif i == 3:

            print("Let's check if everything is there.")

            #####
            while not isFileHere("public_key.kpk",config.DIRECTORY_PROCESSING):
                clear()
                asc.asciiCat()

                input("Please put your 'private_key.kpk' file into the 'processing' folder.")
            
            clear()
            asc.asciiCat()
            print("Gotcha !\n")
            
            while not isFileHere("encrypted.kat",config.DIRECTORY_PROCESSING):
                clear()
                asc.asciiCat()

                input("Please put your 'encrypted.kat' file into the 'processing' folder.")
            
            clear()
            asc.asciiCat()
            print("Gotcha !\n")
            #####

            e = extractKeyFromFile("encrypted",config.DIRECTORY_PROCESSING,".kat")

            d = elG.decrypt(e,extractKeyFromFile("private_key",config.DIRECTORY_PROCESSING),asTxt=True)

            d = d.split("\n")

            for phrase in d:
                print(f"\t -'{phrase}'")

            doSomethingElse(katsuAsymm)
        elif i == 4:
            dHgestion()
        elif i == 5:
            dlogAttack()

        elif i == 6:
            clear()
            asc.asciiDeath()
            print("You're going to erase all key's from the system.\n")

            if query_yn("Are you sure ?"):

                for f in ["public_key","private_key","dH_shared_key","dH_agreement","dH_sendable"]:
                    rmFile(f+".kpk",config.DIRECTORY_PROCESSING)

                clear()
                asc.asciiDeath()
                print("Done.\n")
                return doSomethingElse(katsuAsymm)

            else:
                doSomethingAssym()

        elif i == 7:
            clear()
            katsumi.menu()
        else:
            
            katsuAsymm()
        
    doSomethingAssym(selection)


def katsuHash():

    import core.hashbased.hashFunctions as hf
    import base64

    clear()
    asc.asciiCat()

    choices = ["Generate a hash","Check a hash","Back to menu"]

    enumerateMenu(choices)

    selection = getInt(1,"choices")

    if selection == 1:

        size = getInt(256, "hash", True)

        if query_yn("Do you want to hash a file ?","no"):

            f = getFile()
            clear()
            
            if f:
               print (f"File hash: {base64.b64encode(hf.sponge(bm.fileToBytes(f), size)).decode()}")
            
            else:
                katsuHash()  
        else:
            msg = readFromUser("Enter the text to hash:")

            print (f"Text hash: {base64.b64encode(hf.sponge(msg.encode(), size)).decode()}")
            

    elif selection == 2:
        
        def verifyHash(h, msg):
            h2 = hf.sponge(msg, len(h)*8)
            
            if h == h2:
                print("Hashes are the same !")
            else:
                print("Hashes are not the same !")

        h = getb64("hash")

        if  h:
            if query_yn("Do you want to compare this hash to a file's one ?", "no"):
                f = getFile()
                if f:
                    verifyHash(h, bm.fileToBytes(f))
                else:
                    katsuHash()
            else:
                verifyHash(h, readFromUser("Enter the text to compare with the hash:").encode()) 
        else:
            katsuHash()
    else:
        import katsumi

        clear()
        katsumi.menu()

    doSomethingElse(katsuHash)


