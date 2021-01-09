import os
import sys

recursionL = sys.getrecursionlimit()
sys.setrecursionlimit(recursionL * 2)
# To avoid maximum recursion depth with huge integer (e.g euclid).


THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRECTORY_GEN = os.path.join(THIS_FOLDER,"ressources/generated/")
DIRECTORY_PROCESSING = os.path.join(THIS_FOLDER,"processing/")
DIRECTORY_FOUNT = os.path.join(DIRECTORY_GEN,"PrimeNumber's_Fount/")

# Keys
KL1 = []
KL2 = []
KO1 = [] 
KO2 = [] 
KO3 = []
KI1 = [] 
KI2 = []
KI3 = []

# Watch variables
WATCH_EXEC_STATUS = False
WATCH_READ_TIME = 0
WATCH_WRITE_TIME = 0
WATCH_BLOC_KASUMI = 0
WATCH_GLOBAL_KASUMI = 0
WATCH_CIPHER_TYPE = "ECB"
WATCH_BLOC_CIPHER = 0
WATCH_GLOBAL_CIPHER = 0
WATCH_PERCENTAGE = 0.01
WATCH_GLOBAL_TIME = 0
WATCH_GLOBAL_INVERSION = 0
WATCH_INVERSION_NUMBER = 0.002
WATCH_KASUMI_NUMBER = 0
WATCH_GLOBAL_MULT = 0
WATCH_MULT_NUMBER = 0
GALOIS_WATCH = False

# Galois Field
# Inversion creation check
IN_CREATION = False

DEGREE = 0
ALPHA_ELEMENTS = []
ELEMENTS = []
NBR_ELEMENTS = 0
# GF(2^16) [1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1] -> 
IRRED_POLYNOMIAL= [1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1]
GENERATOR = 0
INVERSIONS_BOX = []

# Key
KEY = bytearray()

# Block-Chain variables
BC_CHAIN = []
BC_USERS = []
BC_UTXO = []
BC_LOGS = []
BC_POW_FIRST = 10
BC_POW_RATIO = 1
BC_HASH_SIZE = 256
BC_KEY_SIZE = 128
BC_MINER_REWARD = 20
BC_TIME_START = 0
BC_SIGNING_ALG = "ElGamal"

BC_USER_PARAMS = [
    # Default value, param name, param desc, param type, is param a size, choices
    [10, "Bloc limit\t", "Block-chain simulation stops when this number of bloc is reached.", int, False, []],
    [2, "Number of miners\t", "Number of miners trying to validate each block, since users are created progressively, this number will only be reached when enough users are created.", int, False, []],
    [50, "Miner reward\t", "Amount of money rewarded to the miner for block validation.", int, False, []],
    [256, "Hash size\t\t", "Hash size used for POW calculation and bloc hashes, increasing this value makes it harder to validate a block.", int, True, []],
    [128, "Key size\t\t", "Key size used for signing transactions, increasing this value makes bloc much bigger and increases POW calculation time.", int, False, []],
    ["elGamal", "Signing algorithm\t", "Algorithm used for signing transaction.", str, False, ["elGamal", "RSA"]],
    [0.5, "POW ratio\t\t", "Ratio for POW calculation difficulty, 0.5 makes it easier to validate a block when 2 makes it harder. Has a direct influence on number of transaction per bloc", float, False, []],
    [10, "POW first value\t", "First block is not growing with new transactions (because nobody have enough money), so POW needs to have a fixed number of null bits.", int, False, []],
    [(2,3), "Cycle frequency\t", "Range in seconds between which cycle of transactions are generated (e.g. new cycle between every (1,2) seconds).", tuple, False, []],
    [(10,15), "Transaction per cycle", "Range between which number of transactions are generated per cycle (e.g. between (1,5) transactions are generated per cycle).", tuple, False, []],
    [(1,10), "Transaction amount", "Range between which amount of the transaction is choosen (e.g. transaction amount is between (1,10))", tuple, False, []]
]