#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time

def work_with_selection(pSelection):
    """Interact with others py functions depending on user choice."""

    if pSelection == 1 :
        print("Hello")
    elif pSelection == 2 :
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
        os.system("clear")
        print("\t --- Goodbye M'Lord. --- \n")
        sys.exit
    else:
        os.system("clear")
        print("\n That's not available in the given menu lad !")
        time.sleep(1)
        menu()

def menu():
    
    choices=["Encrypt a message.", "Uncrypt a message.", "Generate public/private key pairs.","Generate a hash / fingerprint.","Check a hash / a fingerprint.","Perform a proof of work.","Check a transaction.","Start / increment Block-chain.","Check Block-chain integrity's","I WANT IT ALL !! I WANT IT NOW !","Exit"]
    
    print("------------------------------------------------------")
    print('''
     __ _     _ _     _           _      _   _     
    / _\ |__ (_) |__ | |__   ___ | | ___| |_| |__  
    \ \| '_ \| | '_ \| '_ \ / _ \| |/ _ \ __| '_ \ 
    _\ \ | | | | |_) | |_) | (_) | |  __/ |_| | | |
    \__/_| |_|_|_.__/|_.__/ \___/|_|\___|\__|_| |_|
                                               
''')
    print("- Created by : Gobinet Théo && Martin Azaël ")
    print("- Free to use")
    print()

    for i,elt in enumerate(choices):
        print(f"\t({i+1}) - {elt}")
    
    while True :
        try:
            selection=int(input("\n - Please enter your choice: "))
        except ValueError:
            print("Hmm.. Nope. Repeat please !")
            continue
        else:
            break

    work_with_selection(selection)



def main():
    os.system("clear")
    menu()

if __name__ == '__main__':
    main()
