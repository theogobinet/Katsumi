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
    return os.path.exists(directory+name)

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
        while len(key) != 16:
            try:
                sKey = input()
                key = base64.b64decode(sKey)
                if(len(key) != 16):
                    print("Invalid key, key must be 16 bytes long!")
            except (binascii.Error, UnicodeEncodeError):
                print("Invalid key, key must be encoded in base64!")

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

def extractSafePrimes(nBits:int=1024,all:bool=True,directory=config.DIRECTORY_FOUNT):
    """
    Return list of tuples (Safe_Prime,Sophie_Germain_Prime) for given n bits.
    If list doesn't exist, create one with 1 tuple.

    all :
        - True for all list
        - False for one random tuple
    """
    name = f"{str(nBits)}_bits"

    if not isFileHere(name+".txt",directory):
        stockSafePrimes(nBits,1)
        extractSafePrimes(nBits,directory)
    else:
        v = extractVarFromFile(name,directory)

        if all:
            return v
        else:
            import random as rd
            return rd.choice(v)

def stockSafePrimes(n:int=1024,x:int=15,randomFunction=prng.xorshiftperso,Update=False,Verbose=False):
    """ 
    Stock (x * numbers of cpu) tuples of distincts (Safe prime, Sophie Germain prime) into a fount of given n bits length.
    
    Using parallelization for fastest generation.
    """
    # Create an appropriated directory.
    handleDirectory("PrimeNumber's_Fount")

    from multiprocessing import Pool, cpu_count, Manager
    import random as rd

    c = cpu_count()
    pool = Pool(c)

    if Verbose:
        clear()
        print(f"You have {c} Central Processing Units.")
        print(f"Each cpu will computes {x} tuple(s) of safe primes.")

    # Safety check, if already exist, then you just update it !
    if isFileHere(f"{str(n)}_bits.txt",config.DIRECTORY_FOUNT):
        if Verbose:
            print("Data concerning this number of bits already exists. Update in progress.")
        Update = True
    else:
        Update = False

    if Update:
        fount = extractSafePrimes(n)
        fount = Manager().list(fount) # Can be shared between process
    else:
        fount = Manager().list() # Can be shared between process

    if Verbose:
        print(f"Computing in progress. Please wait ...")

    # bool(rd.getrandbits(1)) faster than rd.choice([True,False])
    data = [(x,fount,n,randomFunction,bool(rd.getrandbits(1))) for _ in range(c)]

    pool.starmap(prng.genSafePrimes,data)

    if Verbose:
        print(f"Generation completed.")

    writeVartoFile(fount,f"{str(n)}_bits",config.DIRECTORY_FOUNT)

def updatePrimesFount(p:tuple,nBits:int):
    """
    Update prime number's fount (or create one with one element if not exist) and add given tuple if not present in stocked ones.
    """
    name = f"{str(nBits)}_bits"

    if not isFileHere(name+".txt",config.DIRECTORY_FOUNT):

        stockSafePrimes(nBits,1)
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
    from core.asymetric import elGamal

    question = query_yn("Do you want to choose parameters of ElGamal key generation's ( default = No => fastest way) ?")

    # Because here default is no so not(yes)
    if not question:
        question1 = query_yn("Do you want to choose the length of the key (default = 2048 bits) ?")
        
        if question1:
            n = select()
        else:
            n = 2048

        question2 = query_yn("Do you want to use the Prime Number's Fountain to generate the keys (fastest) ?")

        if question2:
            primes = extractSafePrimes(n,False)
            primes = None

            question3 = query_yn("Do you want to use easy Generator ? (fastest)")

            if question3:
                easyGenerator = True
            else:
                easyGenerator = False
            
            return elGamal.key_gen(n,primes,easyGenerator)
    else:
        n = 512
        primes = extractSafePrimes(n,False)
        return elGamal.key_gen(n,primes)
    


def keysVerif():
    """
    Used to verify existence of private or/and public keys of ElGamal.
    """
    import katsumi

    clear()
    katsumi.asciiCat()

    print("\nChecking the presence of keys in the system....")

    if isFileHere("public_key.txt",config.DIRECTORY_PROCESSING):

        print("Public key already here.\n")

        if isFileHere("private_key.txt",config.DIRECTORY_PROCESSING):
            
            print("Private key's too.\n")
            
            if not query_yn("Do you want to keep them ?"):
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

def dlogAttack():
    
    from core.asymetric import elGamal
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

    import core.symetric.ciphers as ciphers
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
                answer = readFromUser()

            print("Decryption started....")

            begin_time = datetime.now()
            print(ciphers.run(answer, fchoice, False, cipher, "", key))
            end = datetime.now() - begin_time
            input(f"Decryption finished in {end} seconds !\n")

            clear()
            asciiCat()

            return doSomethingElse()
        
        elif i == 3:
            katsumi.menu()
        else:
            clear()
            print("\n That's not available in the given menu lad !")
            time.sleep(1)
            return katsuSymm()
        
    return doSomething(selection)



def katsuAsymm():

    import katsumi
    import core.asymetric.elGamal as elG

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
            katsumi.menu()
        else:
            clear()
            print("\n That's not available in the given menu lad !")
            time.sleep(1)
            return katsuAsymm()
        
    return doSomething(selection)

