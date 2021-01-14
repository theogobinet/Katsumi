#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ressources import interactions as it
from core.symmetric.galois_Z2 import GF2
import ressources.asciiWarehouse as asc

import sys
import time

#################################################
################## Selection  ###################
#################################################

def work_with_selection(pSelection):
    """Interact with others py functions depending on user choice."""

    it.clear()
    asc.asciiCat()

    # Selection orientation 
    if pSelection == 1 :
        it.katsuSymm()

    elif pSelection == 2 :
        it.katsuAsymm()
        
    elif pSelection == 3 :
        it.katsuHash()

    elif pSelection == 4 :
        it.certificate()
    
    elif pSelection == 5:
        it.katsuBlockChain()
 
    elif pSelection == 6:
        return it.primeNumbersFountain()

    elif pSelection in [7,-1]:
        asc.asciiGoodBye()
        sys.exit()

    else:
        it.clear()
        menu()
    

#################################################
################## MENU  ########################
#################################################

def menu():

    it.clear()

    choices=["Symmetric","Asymmetric","Hash","Get X509 Certificate","BlockChain","Prime Numbers Fountain's","Exit"]

    if it.correctSizeHook():

        print("------------------------------------------------------------------")
        asc.asciiCat()
        print("- Created by : Gobinet Théo && Martin Azaël ")
        print("- Free to use")
        print("- MIT License\n")

        it.enumerateMenu(choices)

        try:
            selection = it.getInt(1,"choices")
            work_with_selection(selection)
        except KeyboardInterrupt:
            work_with_selection(-1)

    else:
        menu()


def main():
    it.clear()

    #Galois field's initialization
    GF2(16)
    menu()

if __name__ == '__main__':
    main()
