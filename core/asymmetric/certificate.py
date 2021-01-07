#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#############################################
############ X509 Certification #############
#############################################
# https://en.wikipedia.org/wiki/X.509

import ressources.interactions as it
import core.asymmetric.elGamal as elG


def x509(subjectPublicKey,name:str="X509",out:bool=True):

    import ressources.bytesManager as bm

    if not bm.isBase64(subjectPublicKey):
        subjectPublicKey = it.getB64Keys(subjectPublicKey)

    # Get key size's
    n = elG.getSize(it.getIntKey(subjectPublicKey,3))
    CA_public_key,CA_private_key = elG.key_gen(n,primeFount=True)

    import os
    #An X. 509 Serial Number is an integer whose value can be represented in 20 bytes 
    serialN=it.getB64Keys(os.urandom(20))

    from datetime import date
    today = date.today()
    nextY = today.replace(year = today.year + 1)


    # The certificate is signed by the private key of the certification authority.
    # The one who manufactured and issued this certificate.
    
    signature = it.getB64Keys(elG.signing(bm.mult_to_bytes(subjectPublicKey),CA_private_key))

    CA = f"""
    Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: {serialN}
        Signature Algorithm: El-Gamal
        Issuer: CN = BARK_CA
        Validity
            Not Before: {today.strftime("%b-%d-%Y")}
            Not After : {nextY.strftime("%b-%d-%Y")}
        Subject: CN = Katsumi User
        Subject Public Key Info:
            Public Key Algorithm: El-Gamal
                Public-Key: ({str(n)} bit)
                pub:
                    {str(subjectPublicKey)}
    
    Signature Algorithm: El-Gamal
         {signature}
    """


    if out:
        print(CA)
    else:
        from ressources import config
        #Write into file
        it.writeVartoFile(CA,name,config.DIRECTORY_PROCESSING,".ca")


    return it.getB64Keys(CA_public_key)