# GLOBAL VAR
import core.config as config
import time
from katsumi import clear

def initVar():
    config.WATCH_READ_TIME = 0
    config.WATCH_WRITE_TIME = 0
    config.WATCH_BLOC_KASUMI = 0
    config.WATCH_GLOBAL_KASUMI = 0
    config.WATCH_BLOC_CIPHER = 0
    config.WATCH_GLOBAL_CIPHER = 0
    config.WATCH_PERCENTAGE = 0.001


def display():
        print("------------------------ KATSUMI WATCH ------------------------")
        print("")
        print("-- File --")
        print(("Reading file : {:.6f} seconds").format(config.WATCH_READ_TIME))
        print(("Writing file : {:.6f} seconds").format(config.WATCH_WRITE_TIME))
        print("")
        print("-- Kasumi --")
        print(("Kasumi per bloc time : {:.3f} milliseconds").format(config.WATCH_BLOC_KASUMI * 1000))
        print(("Kasumi global time : {:.3f} seconds").format(config.WATCH_GLOBAL_KASUMI))
        print("")
        print(("-- CIPHER : {} --").format(config.WATCH_CIPHER_TYPE))
        print(("{} per bloc time : {:.3f} milliseconds").format(config.WATCH_CIPHER_TYPE, (config.WATCH_BLOC_CIPHER - config.WATCH_BLOC_KASUMI) * 1000))
        print(("{} global time : {:.3f} seconds").format(config.WATCH_CIPHER_TYPE, config.WATCH_GLOBAL_CIPHER - config.WATCH_GLOBAL_KASUMI))
        print("")
        print("-- Stats --")
        print(("Total time : {:.3f} seconds").format((time.time() - config.WATCH_GLOBAL_TIME)))
        print(("Done : {:.2f}%").format(config.WATCH_PERCENTAGE))
        print(("Time left : {:.0f} seconds").format(((100/config.WATCH_PERCENTAGE) * (time.time() - config.WATCH_GLOBAL_TIME)) - (time.time() - config.WATCH_GLOBAL_TIME)))
        print(("Kasumi's total runtime : {:.2f}%").format((config.WATCH_GLOBAL_KASUMI/(time.time() - config.WATCH_GLOBAL_TIME)) * 100))

def watch():

    initVar()
    config.WATCH_GLOBAL_TIME = time.time()

    while config.WATCH_EXEC_STATUS:

        clear()
        display()
        time.sleep(0.5)

    clear()
    display()