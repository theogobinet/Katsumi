#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time

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


def readFromUser():
    from sys import stdin

    phrase=""

    print("Enter the message there:")
    
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
    print(" Choice cypher method : ")
    print(" 1 - ECB \n 2 - CBC \n 3 - PCBC (Recommended)")

    pCipher=select()

    # Cipher verification
    if pCipher > 3 :
        print("Error: You didn't choose a cipher properly.")
        time.sleep(1)

        import katsumi
        katsumi.menu()

    elif pCipher == 1:
        answer=query_yn(" ECB is not recommended for use in cryptographic protocols. Are you sure ?")
        if answer:
            clear()
            return pCipher
        else: 
            clear()
            return cipher_choice()

    clear()
    return pCipher



###################### - File Manager

from core.config import THIS_FOLDER


def findFile(ext=""):
    """To find a file given extension and return is name."""

    name=""

    if ext=="":
        # Return the first file in the directory that is not crypted
        for f in os.listdir(os.path.join(THIS_FOLDER,"share/")):
            if not(f.endswith("kat")):
                name=f
    else:
        for f in os.listdir(os.path.join(THIS_FOLDER,"share/")):
            if f.endswith(ext):
                name=f

    return name

def writeVartoFile(var:object,name:str):
    """Write given variable into a file with variable name"""
    from core.config import INVERSIONS_DICT
    # r+ for reading and writing
    with open(name+".txt","w+") as f:
        f.truncate(0)
        f.write(f"{INVERSIONS_DICT}")

    return True

def extractVarFromFile(fileName:str):
    """Extract variable contenant's from txt file."""
    import ast
    with open(fileName+".txt","r+") as f:
        contents=f.read()
        extracted=ast.literal_eval(contents)

    return extracted

