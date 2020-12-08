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
BC_POW_NULL = 8
BC_HASH_SIZE = 256
BC_KEY_SIZE = 2048
BC_MINER_REWARD = 10
BC_TIME_START = 0