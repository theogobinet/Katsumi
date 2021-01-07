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
        print("Test")
 
    elif pSelection == 5:
        return it.primeNumbersFountain()
    elif pSelection == 6 or pSelection == -1:
        it.clear()
        print("\t --- Goodbye M'Lord. --- \n")
        sys.exit
    else:
        it.clear()
        menu()
    

#################################################
################## MENU  ########################
#################################################

def menu():

    choices=["Symmetric","Asymmetric","Hash","BlockChain","Prime Numbers Fountain's","Exit"]

    if it.correctSizeHook():

        print("------------------------------------------------------------------")
        asc.asciiCat()
        print("- Created by : Gobinet Théo && Martin Azaël ")
        print("- Free to use")
        print("- MIT License\n")

        it.enumerateMenu(choices)

        selection = it.getInt(1,"choices")


        return work_with_selection(selection)
        
    else:
        menu()


def main():
    it.clear()

    #Galois field's initialization
    GF2(16)

    return menu()


if __name__ == '__main__':
    main()
