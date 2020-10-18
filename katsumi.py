#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
from datetime import datetime

from core.kasumi import kasumi
from core.ciphers import run
from core.bytesManager import findFile


#################################################
############ Interact Methods  ##################
#################################################

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

def cipher_choice():
    clear()
    print(" Choice cypher method : ")
    print(" 1 - ECB \n 2 - CBC \n 3 - PCBC (Recommended)")

    pCipher=select()

    # Cipher verification
    if pCipher > 3 :
        print("Error: You didn't choose a cipher properly.")
        time.sleep(1)
        menu()

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


def work_with_selection(pSelection):
    """Interact with others py functions depending on user choice."""

    # Selection orientation 

    if pSelection == 1 :
        # Encryption
        cipher=cipher_choice()
        print("Please enter the filename (with extension) to encrypt.")
        
        answer=input("E.g: pic.jpg (leave blank by default): ")
        
        if answer=="":
            answer="clearMessage.txt"

        print("Encryption started....")

        begin_time = datetime.now()
        run(answer,True,True,cipher)
        end=datetime.now() - begin_time

        clear()
        print(f"Encryption finished in {end} seconds !\n")

        answer=query_yn("Do you want to do something else ?")
        if answer:
            clear()
            return menu()
        else: 
            clear()
            return work_with_selection(11)

    elif pSelection == 2 :
        # Decryption
        cipher=cipher_choice()
        
        print("Please enter the filename (without .kat ext) to decrypt.")
        answer=input("E.g: encrypted-pic.jpg (leave blank by default) : ")
        
        if answer=="":
            # Find the first .kat file in the folder
            answer=findFile(".kat")

        print("Decryption started....")

        begin_time = datetime.now()
        run(answer,True,False,cipher)
        end=datetime.now() - begin_time

        clear()
        print(f"Decryption finished in {end} seconds !\n")

        answer=query_yn("Do you want to do something else ?")
        if answer:
            clear()
            return menu()
        else: 
            clear()
            return work_with_selection(11)

    elif pSelection == 3 :
        print("Ceci est un deux.")
    elif pSelection == 4 :
        print("Test")
    elif pSelection == 5 :
        print("Test")
    elif pSelection == 6 :
        print("Test")
    elif pSelection == 7 :
        print("Test")
    elif pSelection == 8 :
        print("Test")
    elif pSelection == 9 :
        print("Test")
    elif pSelection == 10 :
        print("Test")
    elif pSelection == 11 :
        clear()
        print("\t --- Goodbye M'Lord. --- \n")
        sys.exit
    else:
        clear()
        print("\n That's not available in the given menu lad !")
        time.sleep(1)
        menu()
    
    return None

def select():
    while True :
        try:
            selection=int(input("\n - Please enter your choice: "))
        except ValueError:
            print("Hmm.. Nope. Repeat please !")
            continue
        else:
            return selection


#################################################
################## MENU  ########################
#################################################

def menu():
    
    choices=["Encrypt a message.", "Decrypt a message.", "Generate public/private key pairs.","Generate a hash / fingerprint.","Check a hash / a fingerprint.","Perform a proof of work.","Check a transaction.","Start / increment Block-chain.","Check Block-chain integrity's","I WANT IT ALL !! I WANT IT NOW !","Exit"]
    
    print("------------------------------------------------------------------")
    print('''                         
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
    print("- Created by : Gobinet Théo && Martin Azaël ")
    print("- Free to use")
    print()

    for i,elt in enumerate(choices):
        print(f"\t({i+1}) - {elt}")

    selection=select()

    work_with_selection(selection)



def main():
    clear()
    menu()


if __name__ == '__main__':
    main()
