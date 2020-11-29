#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ressources import prng

import os
from datetime import datetime
import time
import ressources.config as config

################################################
###############- Console Interactions - ########
################################################

def asciiJongling():
    return print(
        """
                        '   '    '     
                        '   '    '   
                    o/          '  \o 
                    /-'            -\ 
                    /\               /\
                    
            Do you feel as though you are juggling 
                a few to many responsibilities?
        """
    )

def asciiCat():
    return print('''                         
       _                        
       \`*-.                 _  __     _                       _    
        )  _`-.             | |/ /    | |                     (_)    
       .  : `. .            | ' / __ _| |_ ___ _   _ _ __ ___  _     
       : _   '  \           |  < / _` | __/ __| | | | '_ ` _ \| |    
       ; *` _.   `*-._      | . \ (_| | |_\__ \ |_| | | | | | | |    
       `-.-'          `-.   |_|\_\__,_|\__|___/\__,_|_| |_| |_|_|    
         ;       `       `.     
         :.       .        \               Remember: 
         . \  .   :   .-'   .     Encryption provides secrecy,
         '  `+.;  ;  '      :    not authentication or integrety.
         :  '  |    ;       ;-. 
         ; '   : :`-:     _.`* ;
     .*' /  .*' ; .*`- +'  `*' 
      `*-*   `*-*  `*-*'           
                                               
''')


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


def readFromUser(msg="Enter the message there:"):
    from sys import stdin

    phrase=""

    print(msg)
    
    for line in stdin:
        if line == '\n': # If empty string is read then stop the loop
            break
        phrase+=line

    clear()

    return phrase


def select():
    while True :
        try:
            selection=int(input("\n - Please enter your choice: "))
        except ValueError:
            print("Hmm.. Nope. Repeat please !")
            continue
        else:
            return selection

def cipher_choice():

    clear()
    asciiCat()

    print("Choice cypher method : ")
    print(" 1 - ECB \n 2 - CBC \n 3 - PCBC (Recommended) \n 4 - CTR (Stream) \n 5 - CGM (Authentification)")

    pCipher=select()

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
    asciiCat()

    return pCipher



################################################
###############- File Manager - ################
################################################

from .config import THIS_FOLDER


def findFile(ext="",directory="processing/"):
    """
    To find a file given extension and return is name.
    """

    name=""

    if ext=="":
        # Return the first file in the directory that is not crypted
        for f in os.listdir(os.path.join(THIS_FOLDER,directory)):
            if not(f.endswith("kat")):
                name=f
    else:
        for f in os.listdir(os.path.join(THIS_FOLDER,directory)):
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
    return os.remove(directory+name)

def mvFile(name:str,src=config.DIRECTORY_PROCESSING,dst=config.DIRECTORY_GEN):
    """ Move named file """
    import shutil
    return shutil.move(src+name,dst)

def whatInThere(directory=config.DIRECTORY_FOUNT):
    """
    Return elements present in given directory in list format.
    """
    return [os.path.splitext(f)[0] for f in os.listdir(directory)]

def writeVartoFile(var:object,name:str,directory=config.DIRECTORY_GEN):
    """Write given variable into a file with variable name"""
    # r+ for reading and writing
    name=directory+name
    with open(name+".txt","w+") as f:
        f.truncate(0)
        f.write(f"{var}")

    return True

def extractVarFromFile(fileName:str,directory=config.DIRECTORY_GEN):
    """Extract variable contenant's from txt file."""
    import ast
    with open(directory+fileName+".txt","r+") as f:
        contents=f.read()
        extracted=ast.literal_eval(contents)

    return extracted

def askForKey():
    import base64
    import binascii

    clear()
    asciiCat()

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


def doSomethingElse():
    """
    Ask user if he want to do something and if yes, get back to main menu.
    """
    answer = query_yn("Do you want to do something else ?")
    import katsumi

    print()

    if answer:
            clear()
            return katsumi.menu()
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
        stockSafePrimes(nBits,0,Verbose=True)
        extractSafePrimes(nBits,allE,easyGenerator,directory)
    else:
        v = extractVarFromFile(name,directory)

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
                            s = prng.safePrime(nBits,easyGenerator=True,Verbose=True)
                            updatePrimesFount(s,nBits)
                        else:
                            return elGamalKeysGeneration()
                else:
                    return s
            else:
                return s

def stockSafePrimes(n:int=1024,x:int=15,randomFunction=prng.xorshiftperso,Update=False,Verbose=False):
    """ 
    Stock (x * numbers of cpu) tuples of distincts (Safe prime, Sophie Germain prime) into a fount of given n bits length.
    
    Using parallelization for fastest generation.
    """

    assert x >= 0
    # Create an appropriated directory.
    handleDirectory("PrimeNumber's_Fount")

    from multiprocessing import Pool, cpu_count, Manager
    import random as rd

    if x != 0 : 
        c = cpu_count()
        poule = Pool(c)

        if Verbose:
            clear()
            print(f"You have {c} Central Processing Units.")
            print(f"Each cpu will computes {x} tuple(s) of safe primes.")
    
    else:
        if Verbose:
            clear()
            print(f"Generating just one tuple for {n} bits safe prime -> No parallelization needed.")

    # Safety check, if already exist, then you just update it !
    if isFileHere(f"{str(n)}_bits.txt",config.DIRECTORY_FOUNT):
        if Verbose:
            print("Data concerning this number of bits already exists. Update in progress.")
        Update = True
    else:
        if Verbose:
            print("Data not existing, creating file...")
        Update = False

    if Update:
        fount = extractSafePrimes(n)

        if x != 0:
            fount = Manager().list(fount) # Can be shared between process
        
    else:
        if x != 0:
            fount = Manager().list() # Can be shared between process
        else:
            fount = []

    if Verbose:
        print(f"Computing in progress. Please wait ...")

    # bool(rd.getrandbits(1)) faster than rd.choice([True,False])

    if x != 0:
        data = [(x,fount,n,randomFunction,bool(rd.getrandbits(1))) for _ in range(c)]

        poule.starmap(prng.genSafePrimes,data)
        poule.close()

    else:
        prng.genSafePrimes(1,fount,n,randomFunction,bool(rd.getrandbits(1)))


    if Verbose:
        print(f"Generation completed.")

    writeVartoFile(fount,f"{str(n)}_bits",config.DIRECTORY_FOUNT)

def updatePrimesFount(p:tuple,nBits:int):
    """
    Update prime number's fount (or create one with one element if not exist) and add given tuple if not present in stocked ones.
    """
    name = f"{str(nBits)}_bits"

    if not isFileHere(name+".txt",config.DIRECTORY_FOUNT):

        stockSafePrimes(nBits,0)
        updatePrimesFount(p,nBits)

    else:

        buffer = extractVarFromFile(name,config.DIRECTORY_FOUNT)

        if p not in buffer:
            buffer.append(p)
            writeVartoFile(buffer,name,config.DIRECTORY_FOUNT)
            print(f"{p} successfully added to prime number's fount.")
        else:
            print(f"{p} already into prime number's fount. Not added.")
        

def primeNumbersFountain():
    """
    Deal with prime number's fountain.
    """

    clear()

    def asciiArt():
        return print( """
                              .      .       .       .
  .   .       .   1217   .      . .      .         .     337   .    .
         .       .         .    .   .         .         .            .
    .   .    .       .         . . .        .  2027   .     .    .
 .     13    .   .       .       . .      .        .  .              .
      .  .    .  .       .     . .    .       . .      .   .        .
 .   .       .    . .   89 .    . .   .      .     .    109    .     .
    .            .    .     .   . .  .     .   .               .
     .               .  .    .  . . .    .  .                 .
                        . .  .  . . .  . .
                            . . . . . .
                              . . . .
                               I . I
                 _______________III_______________
                |    .   Prime   .  Numbers   .   |
                 \SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS/
                    \ ======================= /
                        \SSSSSSSSSSSSSSSSS/
                     ________\       /________
                    (=+=+=+=+=+=+=+=+=+=+=+=+=)
                     ~~~~~~~~~~~~~~~~~~~~~~~~~

    """
    )

    asciiArt()

    print("The Foutain contains:")
    for elt in whatInThere():
        print(f"\t > {elt}")
    
    choices = ["Generate and stock safe primes","Update a list","Back to menu"]

    print("\n")
    for i,elt in enumerate(choices):
        print(f"({i+1}) - {elt}")

    selection = select()

    def doSomething(i:int):
        """ Handle choices for fountain. """
        clear()
        asciiArt()
        if i == 1:
            print("How many bits wanted for this generation ?")
            wanted = select()

            print("\nHow many generations per processor?")
            cpu = select()

            stockSafePrimes(wanted,cpu,Verbose=True)

            return doSomethingElse()

        elif i == 2:
            print("Enter number of bits for updating corresponding one's :")
            wanted = select()

            print("\nHow many generations per processor?")
            cpu = select()

            stockSafePrimes(wanted,cpu,Update=True,Verbose=True)
            
            return doSomethingElse()
        
        elif i == 3:
            import katsumi
            katsumi.menu()
        else:
            clear()
            print("\n That's not available in the given menu lad !")
            time.sleep(1)
            return primeNumbersFountain()
        
    return doSomething(selection)


#########################################
########## El Gamal Gestion #############
#########################################

def elGamalKeysGeneration():
    """
    Dealing with conditions for elGamal key generation.
    """
    from core.asymmetric import elGamal

    clear()
    asciiCat()

    question = query_yn("Do you want to use the fastest ElGamal key generation's ( No => Choose parameters) ?")

    # Because here default is no so not(yes)
    if not question:
        question1 = query_yn("Do you want to choose the length of the key (default = 2048 bits) ?")
        
        if question1:
            n = select()
        else:
            n = 2048

        question2 = query_yn("Do you want to use easy Generator ? (fastest)")

        if question2:
            easyGenerator = True
        else:
            easyGenerator = False


        question3 = query_yn("Do you want to use the Prime Number's Fountain to generate the keys (fastest) ?")

        if question3:
            
            if question2:
                primes = extractSafePrimes(n,False,easyGenerator)
            else:
                primes = extractSafePrimes(n,False)

        else:
            primes = None

        clear()
        asciiCat()

        print("\t.... Key generation in progress ....")
        
        return elGamal.key_gen(n,primes,easyGenerator,prng.xorshiftperso,True)
    else:
        n = 1024
        primes = extractSafePrimes(n,False)

        clear()
        asciiCat()

        print("\t.... Key generation in progress ....")

        return elGamal.key_gen(n,primes,Verbose=True)
    


def keysVerif():
    """
    Used to verify existence of private or/and public keys of ElGamal.
    """
    import katsumi

    clear()
    asciiCat()

    print("\nChecking the presence of keys in the system....")

    if isFileHere("public_key.txt",config.DIRECTORY_PROCESSING):

        print("Public key already here.\n")

        if isFileHere("private_key.txt",config.DIRECTORY_PROCESSING):
            
            print("Private key's too.\n")
            
            if not query_yn("Do you want to keep them ?"):
                rmFile("private_key.txt",config.DIRECTORY_PROCESSING)
                rmFile("public_key.txt",config.DIRECTORY_PROCESSING)
                rmFile("encrypted.txt",config.DIRECTORY_PROCESSING)
                return elGamalKeysGeneration()
            else:
                return katsumi.menu()

        else:
            print("Private key's missing.")
            answer = query_yn("Do you want to add them now ?")
            
            if answer:

                while not isFileHere("private_key.txt",config.DIRECTORY_PROCESSING):
                    clear()
                    input("Please put your 'private_key.txt' file into the 'processing' folder.")
                
                clear()
                print("Gotcha !")

                return keysVerif()
            else:
                return katsuAsymm()
    else:
        return elGamalKeysGeneration()

def dlogAttack():
    
    from core.asymmetric import elGamal
    clear()
    asciiJongling()

    choices = ["Retieve private key with publicKey","Decrypt encrypted message.","Back to menu"]

    for i,elt in enumerate(choices):
        print(f"({i+1}) - {elt}")

    selection = select()

    def doSomething(i:int):
        """ Handle choices for dlog attack. """

        clear()
        asciiJongling()

        if i == 1:

            while not isFileHere("public_key.txt",config.DIRECTORY_PROCESSING):
                clear()
                asciiJongling()

                input("Please put your 'public_key.txt' file into the 'processing' folder.")
            
            clear()
            asciiJongling()
            print("Gotcha !\n")

            print("Compute dlog attack with pollard's rho algorithm.")
            print("It can takes times ...\n")

            el = elGamal.delog(extractVarFromFile("public_key",config.DIRECTORY_PROCESSING),None,True)
            
            writeVartoFile(el,"private_key",config.DIRECTORY_PROCESSING)
            
            print(f"Saved private_key : {el} into appropriated file.\n")


            return doSomethingElse()

        elif i == 2:

            while not isFileHere("public_key.txt",config.DIRECTORY_PROCESSING):
                clear()
                asciiJongling()

                input("Please put your 'public_key.txt' file into the 'processing' folder.")
            
            clear()
            asciiJongling()
            print("Gotcha !\n")
            
            while not isFileHere("encrypted.txt",config.DIRECTORY_PROCESSING):
                clear()
                asciiJongling()

                input("Please put your 'encrypted.txt' file into the 'processing' folder.")
            
            clear()
            asciiJongling()
            print("Gotcha !\n")

            print("Compute dlog attack with pollard's rho algorithm.")
            print("It can takes some times...\n")

            el = elGamal.delog(extractVarFromFile("public_key",config.DIRECTORY_PROCESSING),extractVarFromFile("encrypted",config.DIRECTORY_PROCESSING),True)
            print(f"Decrypted message is: \n \t -'{el}'\n")

            return doSomethingElse()
        
        elif i == 3:
            import katsumi
            katsumi.menu()
        else:
            clear()
            print("\n That's not available in the given menu lad !")
            time.sleep(1)
            return dlogAttack()
        
    return doSomething(selection)


#########################################
########## Other Choices  ###############
#########################################

def katsuSymm():

    import core.symmetric.ciphers as ciphers
    import katsumi

    clear()
    asciiCat()

    symmetric_choices=["Encrypt a message.", "Decrypt a message.","Back"]

    print("\n")
    for i,elt in enumerate(symmetric_choices):
        print(f"({i+1}) - {elt}")

    selection = select()

    def doSomething(i:int):
        """ Handle choices for symmetric things. """

        clear()
        asciiCat()

        if i in [1,2]:

            if not config.KEY:
                key = askForKey()
            else:
                key = config.KEY

        if i == 1:
            # Encryption
            cipher = cipher_choice()
            
            aad=""

            if cipher == 5:
                answer=query_yn("GCM allows to store authentified additional data (not encrypted), do you want to store some AAD ?")
                if answer:
                    aad = readFromUser()
                else: 
                    clear()
                    asciiCat()

            fchoice = query_yn("Do you want to encrypt a file ?")
            answer = ""

            if fchoice:
                print("Please enter the filename (with extension) to encrypt.")
                
                answer=input("E.g: pic.jpg (leave blank by default): ")
                
                if answer=="":
                    answer=findFile()
            else:
                answer=readFromUser()


            print("Encryption started....")

            begin_time = datetime.now()
            print(ciphers.run(answer, fchoice, True, cipher, aad, key))
            end=datetime.now() - begin_time
            input(f"Encryption finished in {end} seconds !\n")

            clear()
            asciiCat()

            return doSomethingElse()

        elif i == 2:
        
            # Decryption    
            cipher = cipher_choice()
            fchoice = query_yn("Do you want to decrypt a file ?")  
            answer = ""

            if fchoice:
                print("Please enter the filename (without .kat ext) to decrypt.")
                answer=input("E.g: encrypted-pic.jpg (leave blank by default) : ")
                
                if answer == "":
                    # Find the first .kat file in the folder
                    answer = findFile("kat")
            else:
                answer = getb64()
                if not answer:
                    katsuSymm()

            print("Decryption started....")

            begin_time = datetime.now()
            print(ciphers.run(answer, fchoice, False, cipher, "", key))
            end = datetime.now() - begin_time
            input(f"Decryption finished in {end} seconds !\n")

            clear()
            asciiCat()
            return doSomethingElse()
        
        elif i == 3:
            clear()
            katsumi.menu()
        else:
            clear()
            print("\n That's not available in the given menu lad !")
            time.sleep(1)
            return katsuSymm()
        
    return doSomething(selection)



def katsuAsymm():

    import katsumi
    import core.asymmetric.elGamal as elG

    clear()
    asciiCat()

    asymmetric_choices= ["Using ElGamal to generate public/private key pairs.","Encrypt a message with ElGamal","Decrypt a message encrypted by ElGamal.","Share private key with Diffie-Hellman.","Discrete Logarithmic attack on ElGamal.","Back"]

    print("\n")
    for i,elt in enumerate(asymmetric_choices):
        print(f"({i+1}) - {elt}")

    selection = select()

    def doSomething(i:int):
        """ Handle choices for symmetric things. """
        clear()
        asciiCat()

        if i == 1:
            print("You are going to generate public/private key pairs with ElGamal algorithm.")
            keysVerif()

        elif i == 2:
            
            if not isFileHere("public_key.txt",config.DIRECTORY_PROCESSING):
                doSomething(1)
            else:
                answer = readFromUser().encode()
                e = elG.encrypt(answer,extractVarFromFile("public_key",config.DIRECTORY_PROCESSING))

                print(f"Saved encrypted message: {e} into appropriated file.\n")

                return doSomethingElse()
        elif i == 3:

            print("Let's check if everything is there.")

            #####
            while not isFileHere("private_key.txt",config.DIRECTORY_PROCESSING):
                clear()
                asciiCat()

                input("Please put your 'private_key.txt' file into the 'processing' folder.")
            
            clear()
            asciiCat()
            print("Gotcha !\n")
            
            while not isFileHere("encrypted.txt",config.DIRECTORY_PROCESSING):
                clear()
                asciiCat()

                input("Please put your 'encrypted.txt' file into the 'processing' folder.")
            
            clear()
            asciiCat()
            print("Gotcha !\n")
            #####

            e = extractVarFromFile("encrypted.txt",config.DIRECTORY_PROCESSING)

            d = elG.decrypt(e,extractVarFromFile("private_key",config.DIRECTORY_PROCESSING),asTxt=True)

            print(f"Decrypted message is: \n \t -'{d}'\n")

            return doSomethingElse()

        elif i == 5:
            dlogAttack()

        elif i == 6:
            clear()
            katsumi.menu()
        else:
            clear()
            print("\n That's not available in the given menu lad !")
            time.sleep(1)
            return katsuAsymm()
        
    return doSomething(selection)


def katsuHash():

    import ressources.bytesManager as bm 
    import core.hashbased.hashFunctions as hf
    import base64

    clear()
    asciiCat()

    choices = ["Generate a hash","Check a hash","Back to menu"]

    for i,elt in enumerate(choices):
        print(f"({i+1}) - {elt}")

    selection = select()

    if selection == 1:

        size = getSize()

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

    doSomethingElse()

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

        
def getSize(default=256):
    print(f"Please enter the hash size ({default} bits by default):")

    while True:
        i = input("> ")
        if i == "c":
            return None
        elif i == "":
            return default
        else:
            try:
                val = int(i)
                if val % 8 == 0 and val >=32:
                    return val
                else:
                    print(f"Error: {i} is not a valid digest size, leave blank or enter a valid hash size:")
                
            except ValueError:
                print(f"Error: '{i}' is not an integer, leave blank or enter a valid hash size:")


def getb64(expected="message", size=-1):
    import base64
    import binascii

    print(f"Enter the {expected} in base64:")
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