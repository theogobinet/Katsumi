<a>
    <img src="images/Katsumi.png" alt="Katsumi logo" title="katsumi" align="center" />
</a>

`Katsumi` is an interactive cryptographical tool.

**Designed** on Arch Linux and Windows 10 **for Linux and Windows operating systems**.

## Table of content

- [About](#About)
- [Installation](#Installation)
- [Overview](#Performance)
    - [Structure](#Structure)
    - [Features](#Features)
    - [Performances](#Performances)
- [Authors](#Authors)
- [License](#License)
- [Links](#Links)
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
* The "core" folder contains the core of the program. Everything related to symmetric, asymmetric and hash-based encryption methods (i.e. [the BlockChain](core/hashbased/blockchain.py)).
* The ["processing" folder](processing/) which contains all outputs of the program destined for the user (i.e. public/private keys, digital signatures and encrypted things).
* The ["resources" folder](ressources/) contains all the largest code files. This is where most of the primary functions reside.



### Features

* To make it easier to handle the inverses in the Galois fields, we have [pre-recorded in memory the inverses](ressources/generated/inversion_Sbox.txt) of the Galois field degree 16 (itself written in raw).

* The Inversion_Sbox.txt is checked at each start and if it's corrupted (not here or wrong), the program will generate one before starting.

* Any generator for El-Gamal is designed to resist common attacks and is found via the principle of [Schnorr's group](https://en.wikipedia.org/wiki/Schnorr_group). More information by reading the code about El-Gamal [here](core/asymmetric/elGamal.py).

* The generation of safe prime numbers is done by optimizing the search. We start from p prime number and check if 2p+1 is also prime OR if (p-1)/2 is also prime. [The source code dedicated to this subject](ressources/prng.py) has been commented in order to understand the thinking process.

* The difficulty of the [proof of work](https://en.wikipedia.org/wiki/Proof_of_work) established is adjusted according to the size of the blocks using a logarithmic function approximated by induction (i.e. by experimentation).

#### Prime Number's Fountain

Generating safe primes can take a lot of computing time. 
To overcome this problem, we have imagined storing our safe primes in an accessible and editable location.
We decided to call this thing: [**The Prime Number's Fountain**](ressources/generated/PrimeNumber's_Fount)

<a>
    <img src="images/PrimeFount.png" alt="Fount" title="Prime Number's Fountain" align="center" />
</a>

With this method, the user can have safe prime numbers loaded in his free time and use them appropriately at the right time.

**Python natively uses only one core**. So [we have multiprocessed the safe prime number search](ressources/prng.py) using 85% of the core capacity.

### Performances
**Each measurement is based on a i7-10510U with 2.5GHz**.

* The generation of the inverses in a binary Galois field (Z2) of degree 16 takes about 46.7 secondes (average over 5 trials).
* Generating a safe prime of 512 bits take at average 12.4 secondes for 10 tests.
* Generating a safe prime of 2048 bits take at average 71 minutes for 4 tests.

## Authors
* **Azaël MARTIN** - [n3rada](https://github.com/n3rada)
* **Théo GOBINET** - [Elec](https://github.com/theogobinet)
## Licence
Katsumi is licensed under the terms of the MIT Licence 
and is available for free - see the [LICENSE.md](LICENSE.md) file for details.

## Links
