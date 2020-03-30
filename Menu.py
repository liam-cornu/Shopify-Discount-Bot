# -*- coding: utf-8 -*-
# cython: language_level=3
"""
Created on Mon Mar 30 16:14:15 2020

@author: Liam Cornu
"""
from colorama import Style, Fore
from init import clean
import time
from FetchCoupons import Fetch_Coupons
from tabulate import tabulate
from CheckBalance import Check_Balance


def product_info(product, Config):
    try:
        clean()
        print("[ INFO ] En recherche de coupons...".center(92) + "\n")
        
        # Récupères le coupons
        coupons = Fetch_Coupons(Config.name)
        clean()
        # Liste les infos sur le produit
        print(
            Style.DIM
            + Fore.YELLOW
            + "Informations sur le produit"
            + Style.RESET_ALL
            + "\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"
        )
        print("Titre: " + Fore.YELLOW + product[0] + Style.RESET_ALL)
        print("\n")
        print("Prix: " + product[2] + Fore.CYAN + " " + product[3] + Style.RESET_ALL)
        print("\n")
        print("Url: " + Fore.YELLOW + product[1] + Style.RESET_ALL)
        print("\n")
        if coupons is None:
            len_coupons = 0
        else:
            len_coupons = len(coupons)
        print(
            "Nombre de coupons trouvés: "
            + Fore.YELLOW
            + str(len_coupons)
            + Style.RESET_ALL
        )
        print("\n")
        print(
            "Que voudriez-vous faire?:\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\n"
            + "["
            + Fore.RED
            + "1"
            + Style.RESET_ALL
            + "] "
            + Fore.GREEN
            + "Afficher les coupons"
            + Style.RESET_ALL
            + "\n["
            + Fore.RED
            + "2"
            + Style.RESET_ALL
            + "] "
            + Fore.GREEN
            + "Vérifier le solde d'une carte cadeau/coupon"
            + Style.RESET_ALL
            + "\n["
            + Fore.RED
            + "3"
            + Style.RESET_ALL
            + "] "
            + Fore.RED
            + "Retourner au menu"
            + Style.RESET_ALL
        )
        try:
            choice = int(
                input("[" + Fore.CYAN + "→" + Style.RESET_ALL + "] " + Fore.YELLOW)
            )
        except Exception:
            print(Style.RESET_ALL)
            clean()
            print(
                Style.BRIGHT
                + Fore.RED
                + "[ ERROR ] Veuillez entrer un nombre".center(92)
                + Style.RESET_ALL
            )
            time.sleep(2)
            product_info(product, Config)
        if int(choice) < 1 or int(choice) > 3:
            clean()
            print(
                Style.BRIGHT
                + Fore.RED
                + "[ ERROR ] Veuillez choisir une des options".center(92)
                + Style.RESET_ALL
            )
            time.sleep(2)
            product_info(product, Config)
            
        # Liste les codes de réduction
        if int(choice) == 1:
            if coupons is None:
                clean()
                print(
                    Style.BRIGHT
                    + Fore.RED
                    + "[ ERROR ] Aucun coupon disponible".center(92)
                    + Style.RESET_ALL
                )      
                time.sleep(3)
                product_info(product, Config)
            else:
                clean()
                print(Style.DIM + Fore.YELLOW + (Config.name).center(92) + Style.RESET_ALL)
                print(("¯" * len(Config.name)).center(92))
    
                print(
                    "==== Coupons Disponibles ({}) ====\n".format(
                        len([f for f in coupons])
                    ).center(30)
                )
                rows = []
                for elt, content_file in enumerate(sorted(coupons)):
                    headers = ["Id", "Code du coupon", "Discount/Valeur"]
                    rows.append(
                        [
                            Style.BRIGHT + "[" + Fore.RED + str(elt) + Fore.WHITE + "]",
                            Style.DIM + Fore.YELLOW + content_file[0],
                            Fore.GREEN + content_file[1] + Style.RESET_ALL,
                        ]
                    )
                print(tabulate(rows, headers=headers, tablefmt="rst"))
                print("\n" * 2)
                print(
                    "Appuyez sur Entrée pour continuer\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"
                )
                input()
                product_info(product, Config)
                
        # Vérifie le sole d'un coupon ou d'une carte cadeau
        elif int(choice) == 2:
            clean()
            print(
                "Veuillez entrer un code de carte cadeau ou un coupon:\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"
            )
            try:
                code = input(
                    "[" + Fore.CYAN + "→" + Style.RESET_ALL + "] " + Fore.YELLOW
                )
            except Exception:
                print(Style.RESET_ALL)
                clean()
                print(
                    Style.BRIGHT
                    + Fore.RED
                    + "[ ERROR ] Veuillez entrer un code valide".center(92)
                    + Style.RESET_ALL
                )
                time.sleep(2)
                product_info(product, Config)
            Check_Balance(code, Config)
            
        # Retourne à la sélection de site Shopify
        elif int(choice) == 3:
            pass
    except Exception as e:
        print(Style.RESET_ALL)
        clean()
        print(
            Style.BRIGHT
            + Fore.RED
            + "[ ERROR ] Une erreur s'est produite: ".center(92)
            + "\n"
            + str(e).center(92)
            + Style.RESET_ALL
        )
        time.sleep(2)
