#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time

def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

def work_with_selection(pSelection):
    """Interact with others py functions depending on user choice."""

    # Selection orientation 

    if pSelection == 1 :
        cipher=cipher_choice()
        print("Hello")
    elif pSelection == 2 :
        cipher=cipher_choice()
        print("Test")
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


def cipher_choice():
    clear()
    print(" Choice cypher method : ")
    print(" 1 - ECB \n 2 - CBC \n 3 - PCBC")
    pCipher=select()
    # Cipher verification
    if pCipher > 3 :
        print("Error: You didn't choose a cipher properly.")
        time.sleep(1)
        menu()
    clear()
    return pCipher


def menu():
    
    choices=["Encrypt a message.", "Uncrypt a message.", "Generate public/private key pairs.","Generate a hash / fingerprint.","Check a hash / a fingerprint.","Perform a proof of work.","Check a transaction.","Start / increment Block-chain.","Check Block-chain integrity's","I WANT IT ALL !! I WANT IT NOW !","Exit"]
    
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
         :.       .        \    
         . \  .   :   .-'   .   1
         '  `+.;  ;  '      :   
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
