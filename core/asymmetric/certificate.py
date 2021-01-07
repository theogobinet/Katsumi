#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#############################################
############ X509 Certification #############
#############################################
# https://en.wikipedia.org/wiki/X.509

import ressources.interactions as it
import core.asymmetric.elGamal as elG


def x509(subjectPublicKey,n:int=2048):

    CA_public_key,CA_private_key = elG.key_gen(n,primeFount=True)

    import os
    #An X. 509 Serial Number is an integer whose value can be represented in 20 bytes 
    serialN=os.urandom(20)

    from datetime import date
    today = date.today()
    nextY = today.replace(year = today.year + 1)

    it.findAndReplace("X509.txt","SERIAL_N",serialN)
    it.findAndReplaceInPlace("X509.txt","DATESTART",today.strftime("%b-%d-%Y"))
    it.findAndReplaceInPlace("X509.txt","DATEEND",nextY)
    it.findAndReplaceInPlace("X509.txt","NUMBER_OF_BITS",str(n))
    it.findAndReplaceInPlace("X509.txt","THE_PUBLIC_KEY",str(subjectPublicKey))

    # The certificate is signed by the private key of the certification authority.
    # The one who manufactured and issued this certificate.
    from ressources.bytesManager import mult_to_bytes
    
    signature = elG.signing(mult_to_bytes(subjectPublicKey),CA_private_key)

    it.findAndReplaceInPlace("X509.txt","SIGNATURE",signature)

    return CA_public_key