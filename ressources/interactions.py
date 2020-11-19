#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import ressources.config as config
import ressources.interactions as it

################################################
###############- Console Interactions - ########
################################################


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
    return pCipher



###################### - File Manager

from .config import THIS_FOLDER


def findFile(ext="",directory="processing/"):
    """To find a file given extension and return is name."""

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
    import os
    return os.path.exists(directory+name)

def rmFile(name:str,directory="ressources/"):
    """Remove named file."""
    import os
    return os.remove(directory+name)

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