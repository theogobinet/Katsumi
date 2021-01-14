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
                      ; '   : :`-:     _.`* ;  Martin Azaël && Gobinet Théo 
                  .*' /  .*' ; .*`- +'  `*' 
                  `*-*   `*-*  `*-*'           

`Katsumi` is an interactive cryptographical tool.

**Designed** on Arch Linux and Windows 10 **for Linux and Windows operating systems**.

## Table of content

- [About](#About)
- [Installation](#Installation)
- [Overview](#Performance)
    - [Structure](#Structure)
        - [Symmetric](#Symmetric)
        - [Asymmetric](#Asymmetric)
        - [BlockChain](#BlockChain)
    - [Implementation choices](#Implementation_choices)
        - [Prime Numbers Fountain's](#Prime_Numbers_Fountain's)
    - [Performances](#Performances)
    - [Improvements](#Improvements)
- [Authors](#Authors)
- [License](#License)
- [Documentation](#Documentation)
## About
It is a school cryptography project carried out at the [UTT](https://www.utt.fr/) for the [GS15](images/GS15.png) subject.
For more information about this subject, click [here](pdfs/Projet.pdf) (it's in French).

## Installation
* Clone the repository then go to the eponymous folder and launch "katsumi.py" with python 3.

* **No requirements.txt needed** . Everything works without the need for additional libraries. A native installation of python3 is enough ! 

## Overview
This project was initially devoted to the development of a modified version of [Kasumi's symmetric encryption](https://en.wikipedia.org/wiki/KASUMI) algorithm, then to the generation of a public/private key pair to finally gather all the acquired knowledge and simulate a [blockchain](pdfs/blockChain_article.pdf).
### Structure
The source code is ordered as follows:
* The ["core" folder](core/) contains the core of the program. Everything related to symmetric, asymmetric and hash-based encryption methods (i.e. [the BlockChain](core/hashbased/blockchain.py)).
* The ["processing" folder](processing/) which contains all outputs of the program destined for the user (i.e. public/private keys, digital signatures and encrypted things).
* The ["resources" folder](ressources/) contains all the largest code files. This is where most of the primary functions reside.

#### Symmetric
<p align="center">
  <img src="images/sym.gif" alt="animated" />
</p>

#### Asymmetric

<p align="center">
  <img src="images/df.gif" alt="animated" />
</p>

#### BlockChain

<p align="center">
  <img src="images/bc.gif" alt="animated" />
</p>


### Implementation choices

* The primitive polynomial of the binary extension field GF(2) of degree 16 was found [online](https://www.partow.net/programming/polynomials/index.html) and hard-coded into a [config file](ressources/config.py)

* To make it easier to handle the inverses in the Galois fields, we have [pre-recorded in memory the inverses](ressources/generated/inversion_Sbox.txt) of the Galois field degree 16 (itself written in raw).

* The [Inversion_Sbox.txt](ressources/generated/inversion_Sbox.txt) is checked at each start and if it's corrupted (not here or wrong), the program will generate one before starting.

* Any generator for El-Gamal is designed to resist common attacks and it's found via the principle of [Schnorr's group](https://en.wikipedia.org/wiki/Schnorr_group). More information by reading the code about El-Gamal [here](core/asymmetric/elGamal.py).

* The generation of safe prime numbers is done by optimizing the search. We start from p prime number and check if 2p+1 is also prime OR if (p-1)/2 is also prime. [The source code dedicated to this subject](ressources/prng.py) has been commented in order to understand the thinking process.

* The difficulty of the [proof of work](https://en.wikipedia.org/wiki/Proof_of_work) established is adjusted according to the size of the blocks using a power function approximated by induction (i.e. by experimentation).

* The blockchain simulation is single-threaded, so adding miners will not speed up block validation. As we can directly influe on on the block validation difficulty this is not problematic for the simulation understanding.

* The simulation uses the [UTXO](https://medium.com/bitbees/what-the-heck-is-utxo-ca68f2651819) system which is for example used in Bitcoin.

* For [RSA](core/asymmetric/RSA.py) or [ElGamal](core/asymmetric/elGamal.py) encryption/decryption, **if the message is longer than our current modulus, it causes problem to process** (i.e. Mathematically outside the modulus). To overcome this, we **use a reversible mapping function** : *If the input message is larger (after conversion in integer) than the module of our encryption algorithm, we divide said message into several parts strictly smaller than the size of the module (i.e. With a 128-bit key, a 488-bit message is divided into 120-bit sub-messages)*.

* Base64 is used instead of hexadecimal for storing and displaying encrypted keys and/or messages. **Base64 takes 4 characters for every 3 bytes, so it's more efficient than hex.**

#### Prime Numbers Fountain's

Generating safe primes can take a lot of computing time. 
To overcome this problem, we have imagined storing our safe primes in an accessible and editable location.
We decided to call this thing: [**The Prime Numbers Fountain's**](ressources/generated/PrimeNumber's_Fount)

<p align="center">
  <img src="images/primeF.gif" alt="animated" />
</p>

With this method, the user can have safe prime numbers loaded in his free time and use them appropriately at the right time.

**Python natively uses only one core**. So [we have multiprocessed the safe prime number search](ressources/prng.py) using 85% of the core capacity.

### Performances
**Each measurement is based on a i7-10510U with 2.5GHz**.

* The generation of the inverses in a binary Galois field (Z2) of degree 16 takes about **85 secondes** (average over 5 trials).
* Generating a **safe prime of 512 bits** take at average **12.4 secondes** for 10 tests.
* Generating a **safe prime of 2048 bits** take at average **71 minutes** for 4 tests.

### Improvements
* An obvious improvement would be to integrate the [elliptic curves](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography). This is a notion that came up at the end of the semester and which, respecting the deadline, could not be implemented (and was not required).

* Using [Schnorr signatures](https://medium.com/digitalassetresearch/schnorr-signatures-the-inevitability-of-privacy-in-bitcoin-b2f45a1f7287) for our BlockChain.

* Group RSA and ElGamal into a parent class to benefit from function heritage (i.e. use object-oriented programming).
## Authors
* **Azaël MARTIN** - [n3rada](https://github.com/n3rada)
* **Théo GOBINET** - [Elec](https://github.com/theogobinet)
## License
Katsumi is licensed under the terms of the MIT Licence 
and is available for free - see the [LICENSE.md](LICENSE.md) file for details.

## Documentation
Here is some useful links for documentation concerning related subjects:

* https://en.wikipedia.org/wiki/Quadratic_residue
* https://en.wikipedia.org/wiki/Cryptographically_secure_pseudorandom_number_generator
* https://andersbrownworth.com/blockchain/
* https://www.random.org/analysis/
* https://en.wikipedia.org/wiki/Hamming_weight
* https://www.keylength.com/  - for choosing appropriated key length's.
* https://blkcipher.pl/assets/pdfs/gcm-spec.pdf - for GCM implementation