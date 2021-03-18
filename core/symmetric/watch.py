#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ressources.interactions as it
import ressources.config as config
import time

# GLOBAL VAR


def initVar():
    config.WATCH_READ_TIME = 0
    config.WATCH_WRITE_TIME = 0
    config.WATCH_BLOC_KASUMI = 0
    config.WATCH_GLOBAL_KASUMI = 0
    config.WATCH_BLOC_CIPHER = 0
    config.WATCH_GLOBAL_CIPHER = 0
    config.WATCH_PERCENTAGE = 0.01
    config.WATCH_KASUMI_NUMBER = 0


def display():
    print("------------------------ KATSUMI WATCH ------------------------")
    print("")
    print("-- File --")
    print(("Reading file: {:.6f} seconds").format(config.WATCH_READ_TIME))
    print(("Writing file: {:.6f} seconds").format(config.WATCH_WRITE_TIME))
    print("")
    print("-- Kasumi --")
    print(
        ("Kasumi per bloc time: {:.3f} milliseconds").format(
            config.WATCH_BLOC_KASUMI * 1000
        )
    )
    print(("Kasumi global time: {:.3f} seconds").format(config.WATCH_GLOBAL_KASUMI))
    print(
        ("Kasumi's total runtime: {:.2f}%").format(
            (config.WATCH_GLOBAL_KASUMI / (time.time() - config.WATCH_GLOBAL_TIME))
            * 100
        )
    )
    print("")
    print(("-- CIPHER: {} --").format(config.WATCH_CIPHER_TYPE))
    print(
        ("{} per bloc time: {:.3f} milliseconds").format(
            config.WATCH_CIPHER_TYPE,
            (config.WATCH_BLOC_CIPHER - config.WATCH_BLOC_KASUMI) * 1000,
        )
    )
    print(
        ("{} global time: {:.3f} seconds").format(
            config.WATCH_CIPHER_TYPE,
            config.WATCH_GLOBAL_CIPHER - config.WATCH_GLOBAL_KASUMI,
        )
    )
    print("")
    if config.GALOIS_WATCH:
        print("-- GALOIS INVERSION --")
        print(("Inversion number: {:.0f} ").format(config.WATCH_INVERSION_NUMBER))
        print(
            ("Inversion per Kasumi: {:.0f} ").format(
                config.WATCH_INVERSION_NUMBER / config.WATCH_KASUMI_NUMBER
            )
        )
        print(
            ("Inversion global time: {:.3f} seconds").format(
                config.WATCH_GLOBAL_INVERSION
            )
        )
        print(
            ("Inversion's total runtime: {:.2f}%").format(
                (
                    config.WATCH_GLOBAL_INVERSION
                    / (time.time() - config.WATCH_GLOBAL_TIME)
                )
                * 100
            )
        )
        print(
            ("Modular mult per inversion: {:.0f} ").format(
                config.WATCH_MULT_NUMBER / config.WATCH_INVERSION_NUMBER
            )
        )
        print(("Modular mult time: {:.3f} seconds").format(config.WATCH_GLOBAL_MULT))
        print(
            ("Modular mult's total runtime: {:.2f}%").format(
                (config.WATCH_GLOBAL_MULT / (time.time() - config.WATCH_GLOBAL_TIME))
                * 100
            )
        )
        print("")
    print("-- Stats --")
    print(
        ("Total time: {:.3f} seconds").format((time.time() - config.WATCH_GLOBAL_TIME))
    )
    print(("Done: {:.2f}%").format(config.WATCH_PERCENTAGE))
    print(
        ("Time left: {:.3f} seconds").format(
            ((100 / config.WATCH_PERCENTAGE) * (time.time() - config.WATCH_GLOBAL_TIME))
            - (time.time() - config.WATCH_GLOBAL_TIME)
        )
    )


def watch():

    initVar()
    config.WATCH_GLOBAL_TIME = time.time()

    while config.WATCH_EXEC_STATUS:

        it.clear()
        # To avoid error of Division by 0
        if config.WATCH_PERCENTAGE == 0:
            config.WATCH_PERCENTAGE = 0.01
        display()
        time.sleep(0.5)
