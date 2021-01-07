#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#############################################
############ X509 Certification #############
#############################################
# https://en.wikipedia.org/wiki/X.509

import ressources.interactions as it
import core.asymmetric.elGamal as elG


def x509(n:int=2048):

    CA_public_key,CA_private_key = elG.key_gen(n,primeFount=True)

    # The certificate is signed by the private key of the certification authority.
    # The one who manufactured and issued this certificate.
    import os
    #An X. 509 Serial Number is an integer whose value can be represented in 20 bytes 
    os.urandom(20)
    it.findAndReplace("X509.txt","SERIAL_N")

    return None