# -*- coding: utf-8 -*-
# cython: language_level=3
"""
Created on Wed Apr 17 00:22:26 2019

@author: Liam Cornu
"""

from init import clean
import time
from colorama import init, Style, Fore
from ctypes import windll, wintypes

init()
from tabulate import tabulate
from Menu import product_info


def liste(product_list, Config):
    clean()
    
    # Si le nombre de produits et supérieur à la taille du CMD, on ajoute une scroll bar
    if len(product_list) >= 32:
        handle = windll.kernel32.GetStdHandle(-11)
        buffsize = int(18 + len(product_list))
        bufsize = wintypes._COORD(92, buffsize)
        windll.kernel32.SetConsoleScreenBufferSize(handle, bufsize)

    # Liste les produits disponible sous forme de tableau ascii
    print(Style.DIM + Fore.YELLOW + (Config.name).center(92) + Style.RESET_ALL)
    print(("¯" * len(Config.name)).center(92))

    print(
        "==== Produits Disponibles ({}) ====\n".format(
            len([f for f in product_list])
        ).center(50)
    )
    rows = []
    for elt, content_file in enumerate(sorted(product_list)):
        headers = ["Id", "Nom", "Prix"]
        rows.append(
            [
                Style.BRIGHT + "[" + Fore.RED + str(elt) + Fore.WHITE + "]",
                Style.DIM + Fore.YELLOW + content_file[0],
                Fore.WHITE
                + content_file[2]
                + " "
                + Fore.CYAN
                + content_file[3]
                + Style.RESET_ALL,
            ]
        )
    print(tabulate(rows, headers=headers, tablefmt="rst"))
    print("\n")
    
    # Selection du produit voulu. 
    try:
        Choice = int(input("Choississez un produit (ID): " + Fore.YELLOW))
        print(Style.RESET_ALL)
        if Choice >= len([f for f in product_list]):
            raise Exception("Invalid number")
        for elt, product in enumerate(sorted(product_list)):
            if elt == Choice:
                product_info(product, Config)
                break
    except Exception as e:
        print(Style.RESET_ALL)
        clean()
        print(e)
        print(
            Style.BRIGHT
            + Fore.RED
            + "[ ERROR ] Veuillez entrer un nombre valide".center(92)
            + Style.RESET_ALL
        )
        time.sleep(2)
        liste(product_list)
