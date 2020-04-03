# -*- coding: utf-8 -*-
# cython: language_level=3
"""
Created on Mon Mar 30 12:45:51 2020

@author: Liam Cornu
"""

from colorama import Style, Fore, init
from GetShop import URL
from window_setting import Title_setting


def Start():
    
    # Mise en place du titre et de la page d'information sur le produit
    Title_setting()
    init()
    print("\n" * 3)
    print("╔══════════════════════════════════════════╗".center(110))
    print("║                                          ║".center(110))
    print(
        (
            "║           "
            + Style.BRIGHT
            + Fore.GREEN
            + "Shopify "
            + Fore.RED
            + "Discount"
            + Fore.GREEN
            + " Bot"
            + Style.RESET_ALL
            + "           ║"
        ).center(133)
    )
    print("║           ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯           ║".center(110))
    print("║      Par Liam Cornu pour ParcourSup      ║".center(110))
    print("║                                          ║".center(110))
    print("╚══════════════════════════════════════════╝".center(110))
    print("\n" * 2)
    print(
        Style.BRIGHT
        + Fore.YELLOW
        + "Information importante:".center(110)
        + Style.RESET_ALL
        + "\n"
        + "¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯".center(110)
        + "\n"
    )
    print(
        "Ce programme a été construit en moins de 24h en guise d'exemple des capacités informatiques de Liam Cornu".center(
            110
        )
    )
    print("\n")
    print(
        "Cet exemple est dirigé aux établissements sur Parcoursup, néanmoins il reste open-source sous license MIT".center(
            110
        )
    )
    print("\n")
    print(
        "Pour plus d'informations, veuillez consulter le github créé pour l'occasion: https://liamco.io/ParcourSup".center(
            110
        )
    )
    print("\n")
    print("Copyright © 2020 Liam Cornu, All Rights Reserved.".center(110))
    print("\n" * 4)
    print("Appuyez sur la touche Entrée pour continuer".center(110))
    print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯".center(110))
    input()
    URL()
