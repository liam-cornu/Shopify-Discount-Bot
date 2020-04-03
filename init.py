# -*- coding: utf-8 -*-
# cython: language_level=3
"""
Created on Mon Mar 30 17:15:18 2020

@author: Liam Cornu
"""

import os
from colorama import Fore, Style
import logging

# ========================== Paramètres du log de crash ==========================
def logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler("crash.log")
    handler.setLevel(logging.INFO)

    # add the handlers to the logger
    logger.addHandler(handler)
    return logger


# ========================================================================

# Permet de nettoyer le CMD et de re-afficher le "logo"
def clean():
    print(Style.RESET_ALL)
    if os.name in ("nt", "dos"):
        os.system("cls")
    elif os.name in ("linux", "osx", "posix"):
        os.system("clear")
    else:
        print("\n") * 120
    print("\n" * 3)
    print("╔══════════════════════════════════════════╗".center(92))
    print("║                                          ║".center(92))
    print(
        (
            "║           "
            + (
                Style.BRIGHT
                + Fore.GREEN
                + "Shopify "
                + Fore.RED
                + "Discount"
                + Fore.GREEN
                + " Bot"
                + Style.RESET_ALL
            )
            + "           ║"
        ).center(115)
    )
    print(("║           ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯           ║").center(92))
    print(("║      Par Liam Cornu pour ParcourSup      ║").center(92))
    print("║                                          ║".center(92))
    print("╚══════════════════════════════════════════╝".center(92))
    print("\n" * 2)
