#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import inf
import os
import time

from ressources import prng
from . import asciiWarehouse as asc
from datetime import datetime

import ressources.config as c
import ressources.bytesManager as bm

################################################
###############- Colored Interactions - ########
################################################
# colored text and background
from colorama import Fore, Style


def prRed(s):
    print(f"{Fore.RED}{s}{Style.RESET_ALL}")


def prGreen(s):
    print(f"{Fore.GREEN}{s}{Style.RESET_ALL}")


def prYellow(s):
    print(f"{Fore.YELLOW}{s}{Style.RESET_ALL}")


def prPurple(s):
    print(f"{Fore.MAGENTA}{s}{Style.RESET_ALL}")


def prCyan(s):
    print(f"{Fore.CYAN}{s}{Style.RESET_ALL}")


################################################
###############- Console Interactions - ########
################################################


def enumerateMenu(choices):
    """
    Menu enumeration
    """
    for i, elt in enumerate(choices):
        print(f"\t({i+1}) - {elt}")

    print()


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

        # meaning execution will leave the function, so there's no need for an else block:
        # all subsequent code after the return will, by definition, not be executed if the condition is true. It's redundant.

        if default is not None and choice == "":
            return valid[default]

        if choice in valid:
            return valid[choice]

        print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def clear():
    """Clearing the screen."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def correctSizeHook():
    """
    Ensures that the terminal window is suitable for the proper operation of the program.

    Return if size was correct
    """

    c, _ = os.get_terminal_size()

    if os.name == "nt":
        cE = 66
    else:
        cE = 69

    if c < cE:
        clear()
        prRed(f"Width needs to be at least {cE}!")

        while c < cE:
            c, _ = os.get_terminal_size()

        return False

    return True


def readFromUser(msg="Enter the message:"):
    from sys import stdin

    phrase = ""

    print(msg + "\n")

    for line in stdin:
        if line == "\n":  # If empty string is read then stop the loop
            break
        else:
            phrase += line

    # [:-1] to delete the last '\n'
    return phrase[:-1]


##############################
# LOOP FUNCTION TO GET INPUT #
##############################


def getFile():

    print("Please enter the filename with its extension (source folder is processing):")

    while True:
        f = input("> ")
        if f == "c":
            return None

        if isFileHere(f, c.DIRECTORY_PROCESSING):
            return c.DIRECTORY_PROCESSING + f

        print(
            f"Error: file '{f}' not found, enter [c] to go back or enter a valid filename:"
        )


def getInt(default=256, expected="hash", size=False, limit: int = inf):
    print(f"Enter {expected} ({default} by default):")

    while True:
        i = input("> ")

        if i == "":
            return default

        try:
            val = int(i)

            if val >= 0 and (not size or (val % 8 == 0 and val >= 32)) and val <= limit:
                return val

            print(
                f"Error: {i} is not a valid {expected}, leave blank or enter a valid {expected}:"
            )

        except ValueError:
            print(f"'{i}' is not an integer, leave blank or enter a valid {expected}:")


def getFloat(default=0.5, expected="value", limit: int = inf):
    print(f"Enter {expected} ({default} by default):")

    while True:
        f = input("> ")

        if f == "":
            return default

        try:
            val = float(f)

            if val >= 0 and val <= limit:
                return val

            raise ValueError

        except ValueError:
            print(
                f"'{f}' is not valid [float + under {limit}], leave blank or enter a valid {expected}:"
            )


def getRange(default=(1, 1)):
    while True:
        t1 = getInt(default[0], "min")
        t2 = getInt(default[1], "max")

        if t1 <= t2:
            return (t1, t2)

        print(
            f"Error: ({t1}, {t2}) is not a valid range, leave blank or enter a valid range"
        )


def getb64(expected="message", size=-1):
    import base64
    import binascii

    print(f"Enter {expected} in base64:")
    while True:
        i = input("> ")
        if i == "c":
            return None
        else:
            try:
                data = base64.b64decode(i)

                if size == -1 or len(data) == size:
                    return data

                print(
                    f"Error: {expected} must be {size} bytes long, enter [c] to go back or enter a valid base64"
                )

            except binascii.Error:
                print(
                    f'Error: Unable to decode "{i}", the format is not in base64, enter [c] to go back or enter a valid base64'
                )


def cipher_choice():

    clear()
    asc.asciiCat()

    print("Choice cypher method: ")
    print(
        " 1 - ECB \n 2 - CBC \n 3 - PCBC (Recommended) \n 4 - CTR (Stream) \n 5 - GCM (Authentification)"
    )

    pCipher = getInt(3, "choices")

    # Cipher verification
    if pCipher > 5:
        print("Error: You didn't choose a cipher properly.")
        time.sleep(1)

        from katsumi import menu

        menu()

    if pCipher == 1:

        answer = query_yn(
            "ECB is not recommended for use in cryptographic protocols. Are you sure?"
        )

        if answer:
            clear()
            return pCipher

        clear()
        return cipher_choice()

    clear()
    asc.asciiCat()

    return pCipher


################################################
###############- File Manager - ################
################################################


def findFile(ext="", directory=c.DIRECTORY_PROCESSING):
    """
    To find a file given extension and return is name.
    """

    name = ""

    if ext == "":
        # Return the first file in the directory that is not crypted
        for f in os.listdir(directory):
            if not (f.endswith("kat")):
                name = f
    else:
        for f in os.listdir(directory):
            if f.endswith(ext):
                name = f

    return name


def isFileHere(name: str, directory=c.DIRECTORY_GEN):
    """Return if given name file's is here or is not."""
    return os.path.isfile(directory + name)


def handleDirectory(dirName: str, directory=c.THIS_FOLDER):
    """ If given directory doesn't exist, then create it. """

    if directory == c.THIS_FOLDER:
        directory += "/"

    if not os.path.exists(directory + dirName):
        os.makedirs(directory + dirName)


def rmFile(name: str, directory=c.DIRECTORY_GEN):
    """Remove named file."""
    try:
        os.remove(directory + name)
    except FileNotFoundError:
        pass


def mvFile(name: str, src=c.DIRECTORY_PROCESSING, dst=c.DIRECTORY_GEN):
    """ Move named file """
    import shutil

    return shutil.move(src + name, dst)


def whatInThere(directory=c.DIRECTORY_FOUNT):
    """
    Return elements present in given directory in list format.
    """
    return [os.path.splitext(f)[0] for f in os.listdir(directory)]


def writeVartoFile(
    var: object, name: str, directory=c.DIRECTORY_GEN, ext: str = ".txt"
):
    """Write given variable into a file with variable name"""
    # r+ for reading and writing
    name = directory + name
    with open(name + ext, "w+") as f:
        f.truncate(0)
        f.write(f"{var}")

    return True


def extractVarFromFile(fileName: str, directory=c.DIRECTORY_GEN, ext: str = ".kat"):
    """Extract variable contenant's from txt file."""
    import ast

    with open(directory + fileName + ext, "r+") as f:
        contents = f.read()
        try:
            extracted = ast.literal_eval(contents)
        except Exception:
            extracted = contents

    return extracted


##############################
######## Key gestion #########
##############################


def getIntKey(data: bytes, keyNumber: int = 1):
    """
    Convert base64 key's into tuples of keyNumber integers.
    """
    assert isinstance(data, (bytes, bytearray))

    if isinstance(keyNumber, str):
        keyNumber = int(keyNumber)

    if keyNumber != 1:
        keys = ()
        kL = []
        for i in range(keyNumber):
            kL.append(int.from_bytes(data[i * 2 : i * 2 + 2], "big"))

        padding = keyNumber * 2
        for i, s in enumerate(kL):
            keys += (int.from_bytes(data[padding : padding + s], "big"),)
            padding = padding + s
    else:
        keys = bm.bytes_to_int(data)

    return keys


def getB64Keys(key):
    """
    Received in input key in tuple, bytes, list etc. and return key in base64.
    """
    import base64

    if isinstance(key, tuple):

        tw = bytearray()
        sizes = []

        for k in key:
            s = bm.bytes_needed(k)
            sizes.append(s)
            # Put the size into the coded b64
            tw += s.to_bytes(2, "big")

        for i, k in enumerate(key):
            tw += k.to_bytes(sizes[i], "big")

    elif isinstance(key, list):
        # E.g, ElGamal with M >= p (longer message)

        e = [getB64Keys(el) for el in key]

        tw = ""
        for el in e:
            tw += f"{el}|"

        tw = tw[:-1].encode()
    elif isinstance(key, bytes):
        # Already into bytes
        tw = key
    else:
        # uniq key
        tw = bm.mult_to_bytes(key)

    return base64.b64encode(tw).decode()


def writeKeytoFile(
    key, fileName: str, directory=c.DIRECTORY_PROCESSING, ext: str = ".kpk"
) -> str:
    """
    Write key in b64 format to file .kpk with key length's as header.
    """

    if isinstance(key, tuple):
        size = str(len(key))

    elif isinstance(key, list):
        # size of each element
        size = len(key[0])
        size = f"L{size}"

    else:
        size = "1"

    b64K = getB64Keys(key)

    b64Key = size + b64K

    writeVartoFile(b64Key, fileName, directory, ext)

    return b64K


def extractKeyFromFile(
    fileName: str, directory=c.DIRECTORY_PROCESSING, ext: str = ".kpk"
):
    """
    Extract key's from b64 format to tuples from katsumi public/private keys file's.
    """

    fileName += ext

    if isFileHere(fileName, directory):
        f = open(os.path.join(directory, fileName), "r+")
        b64data = f.read()
        f.close()

        from base64 import b64decode

        if b64data[0] == "L":
            # It's a list !
            # Case when message is longer than modulus -> separation into list of keys
            return [
                getIntKey(b64decode(el), b64data[1])
                for el in b64decode(b64data[2:]).decode().split("|")
            ]

        return getIntKey(b64decode(b64data[1:]), b64data[0])

    raise FileNotFoundError(f"File {fileName} not found")


def askForKey():
    import base64

    clear()
    asc.asciiCat()

    answer = query_yn("You have not yet defined a key, you want to enter one?", "no")

    key = bytearray()

    if answer:
        key = getb64("key", 16)

        if not key:
            katsuSymm()

    else:
        import secrets as sr

        key = sr.randbits(128).to_bytes(16, "big")
        print("Your key was randomly generated: ", end="")
        prGreen(base64.b64encode(key).decode())

    answer = query_yn("Do you want to keep your key in cache?")

    if answer:
        c.KEY = key

    return key


def getKeySize(key: object = "public_key") -> int:
    """
    Return size of current key based on prime fount's.
    """

    sizes = [int(elt.split("_")[0]) for elt in whatInThere()]

    if isinstance(key, str):
        pK = extractKeyFromFile(key, c.DIRECTORY_PROCESSING, ".kpk")
    else:
        pK = key

    bits = bm.bytes_needed(pK[0]) * 8

    import ressources.utils as ut

    return ut.closestValue(sizes, bits)


##############################
######## Inversion Box #######
##############################


def handleInvBox(doIt: bool = False):
    """
    Deal with inversion box of given degree.

    doIt: argument for debugging, run directly the thing.
    """

    handleDirectory(dirName="generated", directory=c.DIRECTORY_RESSOURCES)

    if doIt:
        import threading
        import core.symmetric.galois_Z2 as gz2

        th = threading.Thread(target=gz2.genInverses2)

        # This thread dies when main thread (only non-daemon thread) exits.
        th.daemon = True

        th.start()
        time.sleep(2)

    else:

        if not isFileHere("inversion_Sbox.txt"):

            print(
                "A necessary file for the substitution has been deleted / corrupted from the system.\n"
            )

            if query_yn(
                "- Do you want to generate the inverse substitution box (No if you want to compute each time needed)? "
            ):

                handleInvBox(True)

            else:
                c.GALOIS_WATCH = True

        else:

            c.INVERSIONS_BOX = extractVarFromFile("inversion_Sbox", ext=".txt")

            if len(c.INVERSIONS_BOX) != c.NBR_ELEMENTS:
                rmFile("inversion_Sbox.txt")
                clear()
                handleInvBox()


def doSomethingElse(m=None):
    """
    Ask user if he want to do something and if yes, get back to main menu.
    """
    answer = query_yn("\nDo you want to do something else?")
    import katsumi

    if m is None:
        m = katsumi.menu

    print()

    if answer:
        clear()
        return m()

    return katsumi.work_with_selection(-1)


#########################################
##### Prime number's fount gestion ######
#########################################


def extractSafePrimes(
    nBits: int = 1024,
    allE: bool = True,
    easyGenerator: bool = False,
    directory: str = c.DIRECTORY_FOUNT,
    Verbose=False,
):
    """
    Return list of tuples (Safe_Prime, Sophie_Germain_Prime) for given n bits.
    If list doesn't exist, create one with 1 tuple.

    all:
        - True for all list
        - False for one random tuple
    """
    name = f"{str(nBits)}_bits"

    if not isFileHere(name + ".txt", directory):
        print("File doesn't exist. Creating it with one element.")
        stockSafePrimes(nBits, 1)
        extractSafePrimes(nBits, allE, easyGenerator, directory)
    else:
        v = extractVarFromFile(name, directory, ".txt")

        if allE:
            return v

        import ressources.utils as ut

        s = ut.randomClosureChoice(v)

        if easyGenerator:
            from core.asymmetric.elGamal import isEasyGeneratorPossible

            if not isEasyGeneratorPossible(s):
                while len(s) != 0 and not isEasyGeneratorPossible(s):
                    s = ut.randomClosureChoice(v)

                if len(s) == 0 and not isEasyGeneratorPossible(s):
                    # It's the only ramaining element and it's not possible to use easy gen with him.

                    if Verbose:
                        print(
                            "No safe prime available for easy generator creation into current {nBits} bits fountain's."
                        )

                        question = query_yn(
                            "Do you want to generate one compatible with this condition (It can be long)? "
                        )

                        if question:
                            s = prng.safePrime(nBits, easyGenerator=True)
                            if s:
                                updatePrimesFount(s, nBits)
                            else:
                                return s  # False
                        else:
                            return elGamalKeysGeneration()
                    else:
                        # No choice.
                        updatePrimesFount(s, nBits)

            return s

        return s


def stockSafePrimes(n: int = 1024, x: int = 15, randomFunction=prng.xorshiftperso):
    """
    Stock x tuples of distincts (Safe prime, Sophie Germain prime) into a fount of given n bits length.
    """

    assert x > 0
    # Create an appropriated directory.
    handleDirectory("PrimeNumber's_Fount", directory=c.DIRECTORY_GEN)

    # Safety check, if already exist, then you just update it !
    if isFileHere(f"{str(n)}_bits.txt", c.DIRECTORY_FOUNT):
        print(
            "\nData concerning this number of bits already exists. Update in progress."
        )
        Update = True
    else:
        print("\nData not existing, creating file...")
        Update = False

    if Update:
        fount = extractSafePrimes(n, Verbose=True)

    else:
        fount = []

    print("Computing in progress. Please wait ...")

    fount = prng.genSafePrimes(x, fount, n, randomFunction)

    if fount:
        prYellow("Generation completed.\n")
        writeVartoFile(fount, f"{str(n)}_bits", c.DIRECTORY_FOUNT)
    else:
        asc.asciiArt()
        prRed("Generation stopped.\n")


def updatePrimesFount(p: tuple, nBits: int):
    """
    Update prime number's fount (or create one with one element if not exist) and add given tuple if not present in stocked ones.
    """
    name = f"{str(nBits)}_bits"

    if not isFileHere(name + ".txt", c.DIRECTORY_FOUNT):
        print("\nData not existing, creating file...")
        stockSafePrimes(nBits, 0)
        updatePrimesFount(p, nBits)

    else:

        buffer = extractVarFromFile(name, c.DIRECTORY_FOUNT, ".txt")

        if p not in buffer:
            buffer.append(p)
            writeVartoFile(buffer, name, c.DIRECTORY_FOUNT)
            print(f"{p} successfully added to prime number's fount.\n")
        else:
            print(f"{p} already into prime number's fount. Not added.\n")


def primeNumbersFountain():
    """
    Deal with prime number's fountain.
    """

    clear()
    asc.asciiArt()

    print("The Foutain contains:\n")

    for elt in whatInThere():
        numberOfTuples = len(extractSafePrimes(elt.split("_")[0]))
        print(f"\t > {elt} - {numberOfTuples} tuples")

    choices = [
        "Generate and stock safe primes",
        "Update a list",
        "Delete a list",
        "Back to menu",
    ]

    print("\n")
    enumerateMenu(choices)

    selection = getInt(2, "choices")

    def doSomethingFount(i: int):
        """ Handle choices for fountain. """
        clear()
        asc.asciiArt()
        if i == 1:
            print("How many bits wanted for this generation?")
            wanted = getInt(2048, "bits size", True)

            print("\nHow many generations?")
            numbers = getInt(1, "generations")

            stockSafePrimes(wanted, numbers)

            doSomethingElse(primeNumbersFountain)

        elif i == 2:
            print("Enter number of bits for updating corresponding one's:")
            wanted = getInt(2048, "bits size", True)

            print("\nHow many generations?")
            numbers = getInt(1, "generations")

            stockSafePrimes(wanted, numbers)

            doSomethingElse(primeNumbersFountain)

        elif i == 3:
            clear()
            asc.asciiDeath()
            print(
                "Enter the number of bits corresponding to the list you would like to be removed."
            )
            lnumber = getInt(2048, "bits size", True)
            name = f"{str(lnumber)}_bits.txt"

            if query_yn("Are you sure?"):
                rmFile(name, c.DIRECTORY_FOUNT)
                print(f"{name} removed successfully.\n")

                doSomethingElse(primeNumbersFountain)
            else:
                primeNumbersFountain()

        elif i == 4:
            import katsumi

            katsumi.menu()
        else:
            clear()
            primeNumbersFountain()

    doSomethingFount(selection)


#########################################
########## El Gamal Gestion #############
#########################################


def elGamalKeysGeneration():
    """
    Dealing with conditions for elGamal key generation.
    """
    from core.asymmetric import elGamal

    clear()
    asc.asciiCat()

    # Because here default is no so not(yes)
    if not query_yn(
        "Do you want to use the fastest ElGamal key generation's (default: no)?", "no"
    ):

        if query_yn(
            "Do you want to choose the length of the key (default = 2048 bits)?", "no"
        ):
            n = getInt(2048, "key size", True)
        else:
            n = 2048

        eGen = query_yn(
            "Do you want to use easy Generator (fastest generation) (default: No)?",
            "no",
        )

        if query_yn(
            "Do you want to use the Prime Number's Fountain to generate the keys (fastest) (default: yes)?"
        ):
            primes = extractSafePrimes(n, False, eGen, Verbose=True)
        else:
            primes = False

        clear()
        asc.asciiCat()

        print("\t.... Key generation in progress ....\n")

        elGamal.key_gen(n, primes, eGen, prng.xorshiftperso, True, True)
    else:
        n = 1024
        primes = extractSafePrimes(n, False, Verbose=True)

        clear()
        asc.asciiCat()

        print("\t.... Key generation in progress ....")

        elGamal.key_gen(n, primes, saving=True, Verbose=True)

    doSomethingElse(katsuAsymm)


def keysVerif(verif: bool = True):
    """
    Used to verify existence of private or/and public keys of ElGamal.
    """

    clear()
    asc.asciiCat()

    print("\nChecking the presence of keys in the system....")

    if isFileHere("public_key.kpk", c.DIRECTORY_PROCESSING):

        from core.asymmetric import elGamal as elG

        publicS = getKeySize()
        print(f"\nPublic key's of {publicS} bits already here.\n")

        if isFileHere("private_key.kpk", c.DIRECTORY_PROCESSING):

            privateS = getKeySize("private_key")
            print(f"Private key's of {privateS} bits too.\n")

            if publicS != privateS:
                clear()
                asc.asciiDeath()
                print(
                    f"Key sizes do not match ({privateS} != {publicS}). Suspected corruption."
                )

                if query_yn("Do you want to delete them?"):

                    print("Keys are going to be deleted...")
                    for f in ["public_key", "private_key"]:
                        rmFile(f + ".kpk", c.DIRECTORY_PROCESSING)

                    clear()
                    asc.asciiDeath()
                    print("Done. Generating other keys now...\n")
                    time.sleep(1)
                    clear()
                    asc.asciiCat()

            else:

                if verif and not query_yn(
                    "Do you want to keep them? (default: No)", "no"
                ):
                    rmFile("public_key.kpk", c.DIRECTORY_PROCESSING)
                    rmFile("private_key.kpk", c.DIRECTORY_PROCESSING)
                    rmFile("encrypted.kat", c.DIRECTORY_PROCESSING)
                    return True

                clear()
                asc.asciiCat()

        else:
            prRed("Private key's missing.\n")

            if query_yn("Do you want to add them now?\n"):

                while not isFileHere("private_key.kpk", c.DIRECTORY_PROCESSING):
                    clear()
                    input(
                        "Please put your 'private_key.kpk' file into the 'processing' folder."
                    )

                clear()
                print("Gotcha !")

                keysVerif()

            else:
                katsuAsymm()

    elif isFileHere("private_key.kpk", c.DIRECTORY_PROCESSING):
        print("\nPrivate key's already here but not public one's.\n")

        if query_yn("Do you want to add them now? ( default: No)\n", "no"):

            while not isFileHere("public_key.kpk", c.DIRECTORY_PROCESSING):
                clear()
                input(
                    "Please put your 'public_key.kpk' file into the 'processing' folder."
                )

            clear()
            print("Gotcha !")

            keysVerif()
        else:
            return True

    else:
        return True

    return False


def dlogAttack():

    from core.asymmetric import elGamal

    clear()
    asc.asciiJongling()

    choices = [
        "Retieve private key with publicKey",
        "Decrypt encrypted message.",
        "Back to menu",
    ]

    enumerateMenu(choices)

    selection = getInt(1, "choices")

    def doSomething(i: int):
        """ Handle choices for dlog attack. """

        clear()
        asc.asciiJongling()

        if i == 1:

            while not isFileHere("public_key.kpk", c.DIRECTORY_PROCESSING):
                clear()
                asc.asciiJongling()

                input(
                    "Please put your 'public_key.kpk' file into the 'processing' folder."
                )

            clear()
            asc.asciiJongling()
            print("Gotcha !\n")

            print("Compute dlog attack with pollard's rho algorithm.")
            print("It can takes times ...\n")

            el = elGamal.delog(
                extractKeyFromFile("public_key", c.DIRECTORY_PROCESSING, ".kpk"),
                None,
                True,
            )

            el = writeKeytoFile(el, "private_key", c.DIRECTORY_PROCESSING, ".kpk")

            print(f"Saved private_key: {el} into appropriated file.\n")

            doSomethingElse(dlogAttack)

        elif i == 2:

            while not isFileHere("public_key.kpk", c.DIRECTORY_PROCESSING):
                clear()
                asc.asciiJongling()

                input(
                    "Please put your 'public_key.kpk' file into the 'processing' folder."
                )

            clear()
            asc.asciiJongling()
            print("Gotcha !\n")

            while not isFileHere("encrypted.kat", c.DIRECTORY_PROCESSING):
                clear()
                asc.asciiJongling()

                input(
                    "Please put your 'encrypted.kat' file into the 'processing' folder."
                )

            clear()
            asc.asciiJongling()
            print("Gotcha !\n")

            print("Compute dlog attack with pollard's rho algorithm.")
            print("It can takes some times...\n")

            el = elGamal.delog(
                extractKeyFromFile("public_key", c.DIRECTORY_PROCESSING),
                extractKeyFromFile("encrypted", c.DIRECTORY_PROCESSING, ".kat"),
                True,
            )

            print("Decrypted message is:\n")
            prYellow(el)

            doSomethingElse(dlogAttack)

        else:
            katsuAsymm()

    doSomething(selection)


#########################################
########## Diffie Hellman ###############
#########################################
def dHgestion():
    """
    Sharing private key with Diffie Hellman.
    """
    import core.asymmetric.diffieHellman as dH

    choices = ["Choose agreement", "Process with agreement", "Back"]

    clear()
    asc.asciiKeys()

    enumerateMenu(choices)

    selection = getInt(2, "choices")

    def doSomethingDH(i: int, processWithAgreement: bool = False):

        if i == 1:
            asc.asciiKeys()

            print("On what size n (bits) did you agree with your penpal?")

            size = getInt(2048, "bits size", True)
            asc.asciiKeys()

            print(f"Checking existence of fountain of {size} bits...")

            if not isFileHere(f"{size}_bits.txt", c.DIRECTORY_FOUNT):
                print("\n\tFile unavailable !")
                print("\n\fOne will be created.\n")
                fountain = False
            else:
                print("\n\tFile available !\n")
                fountain = True

            accord = dH.agreement(size, fountain)

            accord = writeKeytoFile(accord, "dH_agreement")
            print(
                "According to the size of the private key, your agreement is: ", end=""
            )
            prGreen(accord)

            if query_yn("Do you want to process with given agreement now?"):
                doSomethingDH(2, True)
            else:
                doSomethingElse(dHgestion)

        elif i == 2:
            asc.asciiKeys()

            if not processWithAgreement:
                if query_yn(
                    "Do you want to use the dH_agreement.kat file's? (default: Yes)"
                ):
                    accord = extractKeyFromFile("dH_agreement")
                else:
                    accord = getIntKey(getb64("agreement"), 2)

            else:
                accord = extractKeyFromFile("dH_agreement")

            # asc.asciiKeys()

            print(f"\nNow, choose a secret value into [0, {accord[0]}]")

            import random as rd

            secret = getInt(
                rd.randrange(2, accord[0]), "your secret integer", False, accord[0]
            )

            asc.asciiKeys()

            secret = dH.chooseAndSend(accord, secret, saving=True, Verbose=True)

            sended = getIntKey(getb64("his secret"), 1)

            dH_shared = dH.compute(accord, [secret, sended], saving=True)

            asc.asciiKeys()

            print("Shared key created.\n")
            prGreen(f"\t > {dH_shared}\n")

            doSomethingElse(dHgestion)

        elif i == 3:
            katsuAsymm()
        else:
            dHgestion()

    doSomethingDH(selection)


#########################################
############ Symmetric Menu #############
#########################################


def katsuSymm():

    import core.symmetric.ciphers as ciphers
    import katsumi

    clear()
    asc.asciiCat()

    symmetric_choices = ["Encrypt a message.", "Decrypt a message.", "Back"]

    enumerateMenu(symmetric_choices)

    selection = getInt(1, "choices")

    def doSomethingSymm(i: int):
        """ Handle choices for symmetric things. """

        clear()
        asc.asciiCat()

        if i in [1, 2]:

            if not c.KEY:
                key = askForKey()
            else:
                key = c.KEY

        if i == 1:
            # Encryption
            cipher = cipher_choice()

            aad = ""
            inFile = ""

            if cipher == 5:
                if query_yn(
                    "GCM allows to store authentified additional data (not encrypted), do you want to store some AAD?"
                ):
                    aad = readFromUser()
                else:
                    clear()
                    asc.asciiCat()

            if query_yn("Do you want to encrypt a file?", "no"):
                inFile = getFile()
                if inFile:
                    data = bm.fileToBytes(inFile)
                else:
                    katsuSymm()
            else:
                data = readFromUser().encode()

            print("Encryption started....")

            begin_time = datetime.now()
            print("Here is your ciphered message, copy it and send it !\n")
            prGreen(ciphers.run(data, inFile, True, cipher, aad, key))
            end = datetime.now() - begin_time
            input(f"\nEncryption finished in {end} seconds !")

            clear()
            asc.asciiCat()

            doSomethingElse(katsuSymm)

        elif i == 2:

            # Decryption
            cipher = cipher_choice()
            inFile = False

            if query_yn("Do you want to decrypt a file?", "no"):
                inFile = getFile()
                if inFile:
                    data = bm.fileToBytes(inFile)
                else:
                    katsuSymm()
            else:
                data = getb64()
                if not data:
                    katsuSymm()

            print("Decryption started....\n")

            begin_time = datetime.now()

            prYellow(ciphers.run(data, inFile, False, cipher, "", key))

            end = datetime.now() - begin_time
            input(f"\nDecryption finished in {end} seconds !")

            clear()
            asc.asciiCat()
            doSomethingElse(katsuSymm)

        elif i == 3:
            clear()
            katsumi.menu()
        else:

            katsuSymm()

    doSomethingSymm(selection)


#########################################
############ Asymmetric Menu ############
#########################################


def katsuAsymm():

    import katsumi
    import core.asymmetric.elGamal as elG

    clear()
    asc.asciiCat()

    asymmetric_choices = [
        "Using ElGamal to generate public/private key pairs.",
        "Show keys",
        "Encrypt a message with ElGamal",
        "Decrypt a message encrypted by ElGamal.",
        "Share private key with Diffie-Hellman.",
        "Discrete Logarithmic attack on ElGamal.",
        "Keys deletion",
        "Back",
    ]

    enumerateMenu(asymmetric_choices)

    selection = getInt(2, "choices")

    def doSomethingAssym(i: int):
        """ Handle choices for symmetric things. """
        clear()
        asc.asciiCat()

        if i == 1:
            print(
                "You are going to generate public/private key pairs with ElGamal algorithm."
            )

            if keysVerif():
                elGamalKeysGeneration()
            else:
                clear()
                asc.asciiCat()

                print("Your current public key is: ", end="")
                prGreen(getB64Keys(extractKeyFromFile("public_key")))

                doSomethingElse(katsuAsymm)

        elif i == 2:

            try:
                publicK = getB64Keys(extractKeyFromFile("public_key"))
                privateK = getB64Keys(extractKeyFromFile("private_key"))

                print("Public Key: ", end="")
                prGreen(publicK)
                print()
                print("Private Key: ", end="")
                prGreen(privateK)

            except FileNotFoundError:
                print("One key doesn't exist. Please regenerate them.")

            doSomethingElse(katsuAsymm)

        elif i == 3:

            if not isFileHere("public_key.kpk", c.DIRECTORY_PROCESSING):
                print("No public key found into the system...")
                time.sleep(1)
                doSomethingAssym(1)
            else:
                keysVerif(verif=False)
                answer = readFromUser().encode()
                e = elG.encrypt(
                    answer,
                    extractKeyFromFile("public_key", c.DIRECTORY_PROCESSING),
                    saving=True,
                )

                print("Saved encrypted message into appropriated file: ", end="")
                prGreen(e)

                doSomethingElse(katsuAsymm)

        elif i == 4:

            print("Let's check if everything is there.")

            #####
            while not isFileHere("public_key.kpk", c.DIRECTORY_PROCESSING):
                asc.asciiCat()

                input(
                    "Please put your 'private_key.kpk' file into the 'processing' folder."
                )

            print("Gotcha !\n")

            while not isFileHere("encrypted.kat", c.DIRECTORY_PROCESSING):
                asc.asciiCat()

                input(
                    "Please put your 'encrypted.kat' file into the 'processing' folder."
                )

            print("Gotcha !\n")
            #####

            asc.asciiCat()

            if query_yn("Do you want to use the encrypted.kat file's? (default: Yes)"):
                e = extractKeyFromFile("encrypted", c.DIRECTORY_PROCESSING, ".kat")
            else:
                e = getIntKey(getb64("key"), 2)

            d = elG.decrypt(
                e, extractKeyFromFile("private_key", c.DIRECTORY_PROCESSING), asTxt=True
            )

            asc.asciiCat()

            prYellow(d)

            doSomethingElse(katsuAsymm)

        elif i == 5:
            dHgestion()
        elif i == 6:
            dlogAttack()

        elif i == 7:
            clear()
            asc.asciiDeath()
            print("You're going to erase all key's from the system.\n")

            if query_yn("Are you sure?"):

                for f in [
                    "public_key",
                    "private_key",
                    "dH_shared_key",
                    "dH_agreement",
                    "dH_sendable",
                ]:
                    rmFile(f + ".kpk", c.DIRECTORY_PROCESSING)

                clear()
                asc.asciiDeath()
                print("Done.\n")
                return doSomethingElse(katsuAsymm)

            else:
                katsuAsymm()

        elif i == 8:
            clear()
            katsumi.menu()
        else:
            katsuAsymm()

    doSomethingAssym(selection)


#########################################
############   Hash Menu  ###############
#########################################


def katsuHash():

    import core.hashbased.hashFunctions as hf
    import base64

    clear()
    asc.asciiCat()

    choices = ["Generate a hash", "Check a hash", "Back to menu"]

    enumerateMenu(choices)

    selection = getInt(1, "choices")

    if selection == 1:

        size = getInt(256, "hash", True)

        if query_yn("Do you want to hash a file?", "no"):

            f = getFile()
            clear()

            if f:
                print(
                    f"File hash: {base64.b64encode(hf.sponge(bm.fileToBytes(f), size)).decode()}"
                )

            else:
                katsuHash()
        else:
            msg = readFromUser("Enter the text to hash:")

            print(
                f"Text hash: {base64.b64encode(hf.sponge(msg.encode(), size)).decode()}"
            )

    elif selection == 2:

        def verifyHash(h, msg):
            h2 = hf.sponge(msg, len(h) * 8)

            if h == h2:
                print("Hashes are the same !")
            else:
                print("Hashes are not the same !")

        h = getb64("hash")

        if h:
            if query_yn("Do you want to compare this hash to a file's one?", "no"):
                f = getFile()
                if f:
                    verifyHash(h, bm.fileToBytes(f))
                else:
                    katsuHash()
            else:
                verifyHash(
                    h, readFromUser("Enter the text to compare with the hash:").encode()
                )
        else:
            katsuHash()
    else:
        import katsumi

        clear()
        katsumi.menu()

    doSomethingElse(katsuHash)


#########################################
#######  Certificate Menu    ############
#########################################


def certificate():

    import core.asymmetric.certificate as ca

    clear()
    asc.asciiBark()

    choices = [
        "Get a public key certificate",
        "Show current digital certificate",
        "Back to menu",
    ]

    enumerateMenu(choices)

    selection = getInt(1, "choices")

    if selection == 1:
        clear()
        asc.asciiBark()

        k = getb64("public key")

        if not k:
            certificate()

        clear()
        asc.asciiBark()

        ca.x509(k, out=False)
        print("Certifcate generated !")

        doSomethingElse(certificate)

    elif selection == 2:

        clear()
        asc.asciiBark()

        if not isFileHere("X509.ca", c.DIRECTORY_PROCESSING):
            print("Certificate not present into the system.")
            print("Getting back ..")
            time.sleep(1)
            certificate()
        else:
            f = open(c.DIRECTORY_PROCESSING + "X509.ca")
            for line in f.readlines():
                print(line)

        doSomethingElse(certificate)

    else:
        import katsumi

        clear()
        katsumi.menu()

    doSomethingElse(certificate)


#########################################
#######  BlockChain Menu    #############
#########################################

from core.hashbased import blockchain as bc


def bcSimulationParam():

    asc.asciiBlockC()
    print(
        "List of simulation parameters, select the corresponding parameter to view its description and edit it:\n"
    )
    params = (
        [f"{bc.bcolors.BOLD}START THE SIMULATION{bc.bcolors.ENDC}"]
        + [f"{x[1]} \t\t | {x[0]}" for x in c.BC_USER_PARAMS]
        + ["Back to menu"]
    )

    enumerateMenu(params)
    selection = getInt(1, "choices")

    if selection == 1:
        values = [x[0] for x in c.BC_USER_PARAMS]

        c.BC_MINER_REWARD = values[2]
        c.BC_HASH_SIZE = values[3]
        c.BC_KEY_SIZE = values[4]
        c.BC_SIGNING_ALG = values[5]
        c.BC_POW_RATIO = values[6]
        c.BC_POW_FIRST = values[7]

        clear()

        if bc.startLive(values[0], values[1], values[8], values[9], values[10]):
            print("Block-chain validation performed without error")
        else:
            print("An error occured during block-chain validation")

    elif selection <= len(c.BC_USER_PARAMS) + 1:

        asc.asciiBlockC()

        param = c.BC_USER_PARAMS[selection - 2]

        pName = param[1].replace("\t", "")

        print(f"{pName}: {param[2]} \n")

        if param[3] == int:
            param[0] = getInt(param[0], "value", param[4])
        elif param[3] == float:
            param[0] = getFloat(param[0], "value")
        elif param[3] == tuple:
            param[0] = getRange((param[0]))
        elif param[3] == str:
            enumerateMenu(param[5])
            param[0] = param[5][
                getInt(param[5].index(param[0]) + 1, "algorithm", False, len(param[5]))
                - 1
            ]

        bcSimulationParam()

    else:
        katsuBlockChain()


def katsuBlockChain():

    asc.asciiBlockC()
    choices = ["Block-chain live simulation", "Quick block-chain test", "Back to menu"]
    enumerateMenu(choices)

    selection = getInt(1, "choices")

    if selection == 1:
        bcSimulationParam()

    elif selection == 2:
        clear()
        print("Generating the test block-chain...")
        bc.createTestBC()

    else:
        import katsumi

        katsumi.menu()

    doSomethingElse(katsuBlockChain)
