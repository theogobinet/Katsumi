#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from cursesmenu import items
from cursesmenu.items import SelectionMenu


def work_with_selection(pSelection):
    """Interact with others py functions depending on user choice."""

    if pSelection == 0 :
        print("Hello")
    elif pSelection == 1 :
        print("Test")
    elif pSelection == 2 :
        print("Ceci est un deux.")
    elif pSelection == 3 :
        print("Test")
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
        print("Goodbye M'Lord.")
        exit()
    else:
        exit()
def main():
    os.system("clear")

    choices=["Encrypt a message.", "Uncrypt a message.", "Generate public/private key pairs.","Generate a hash / fingerprint.","Check a hash / a fingerprint.","Perform a proof of work.","Check a transaction.","Start / increment Block-chain.","Check Block-chain integrity's","I WANT IT ALL !! I WANT IT NOW !"]

    selection_menu = SelectionMenu.get_selection(choices,"Shibboleth - Encrypted communication tool","Bonjour Ô maître ! Que souhaitez-vous faire aujourd'hui ?")

    work_with_selection(selection_menu)


if __name__ == '__main__':
    main()
