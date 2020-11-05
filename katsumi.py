#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from core.interactions import *
import core.config as config

from core.kasumi import kasumi
from core.ciphers import run
from core.galois_Z2 import GF2

#################################################
################## Selection  ###################
#################################################

def work_with_selection(pSelection):
    """Interact with others py functions depending on user choice."""

    # Selection orientation 

    if pSelection == 1 :
        # Encryption
        cipher=cipher_choice()
        fchoice=query_yn("Do you want to encrypt a file ?")
        answer=""

        if fchoice:
            print("Please enter the filename (with extension) to encrypt.")
            
            answer=input("E.g: pic.jpg (leave blank by default): ")
            
            if answer=="":
                answer=findFile()
        else:
            answer=readFromUser()


        print("Encryption started....")

        begin_time = datetime.now()
        print(run(answer,fchoice,True,cipher))
        end=datetime.now() - begin_time
        input(f"Encryption finished in {end} seconds !\n")

        clear()


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
        fchoice=query_yn("Do you want to decrypt a file ?")  
        answer=""

        if fchoice:
            print("Please enter the filename (without .kat ext) to decrypt.")
            answer=input("E.g: encrypted-pic.jpg (leave blank by default) : ")
            
            if answer=="":
                # Find the first .kat file in the folder
                answer=findFile("kat")
        else:
            answer=readFromUser()+".kat"

        print("Decryption started....")

        begin_time = datetime.now()
        print(run(answer,fchoice,False,cipher))
        end=datetime.now() - begin_time
        input(f"Decryption finished in {end} seconds !\n")

        clear()

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

    #Galois field's initialization
    GF2(16)

    menu()


if __name__ == '__main__':
    main()
