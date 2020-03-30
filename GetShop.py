# -*- coding: utf-8 -*-
# cython: language_level=3
"""
Created on Fri Feb 28 14:43:56 2020

@author: Liam Cornu
"""
from colorama import Fore, Style
from init import clean
from window_setting import Window_setting
import time
import json
from bs4 import BeautifulSoup as soup
import re
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
from product_list import liste

def URL():
    while True:
        Window_setting()
        clean()

        # Demande l'URL du site shopify à scrap
        try:
            print("Entrez l'URL Shopify (avec https://):".center(92))
            print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯".center(92))
            shopifyurl = input(
                "\n".center(45)
                + "["
                + Fore.CYAN
                + "→"
                + Style.RESET_ALL
                + "] "
                + Fore.YELLOW
            )
        except Exception:
            print(Style.RESET_ALL)
            clean()
            print(
                Style.BRIGHT
                + Fore.RED
                + "[ ERROR ] Veuillez entrer une URL valide".center(92)
                + Style.RESET_ALL
            )
            time.sleep(2)
            URL()
        
        # Vérifie via regex que le format de l'url est valide
        if (
            len(
                re.findall(
                    r"(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?",
                    shopifyurl,
                )
            )
            <= 0
        ):
            clean()
            print(
                Style.BRIGHT
                + Fore.RED
                + "[ ERROR ] Veuillez entrer une URL valide (vous devez inclure le https://)".center(
                    92
                )
                + Style.RESET_ALL
            )
            time.sleep(4)
            URL()
        clean()
        print("[ INFO ] En recherche de produits...".center(92) + "\n")
        try:
            try:
                # En cas d'erreur HTTP, renvoyer la requête
                session = requests.Session()
                retries = Retry(
                    total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504, 408],
                )
                session.mount("https://", HTTPAdapter(max_retries=retries))

                # Récupères en liste des produits du site
                r = session.get(
                    url=shopifyurl + "/collections/all/products.atom",
                    verify=False,
                    allow_redirects=True,
                )

                if r.status_code != 200:
                    raise Exception
            except Exception:
                try:
                    r = session.get(url=shopifyurl, verify=False)
                    
                    # Vérifie que le site est bien un site Shopify
                    if "shopify-features" in r.text:
                        clean()
                        print(
                            Style.BRIGHT
                            + Fore.RED
                            + "[ ERROR ] La collection du site est indisponible. Veuillez entrer".center(
                                92
                            )
                            + "\n"
                            + "uniquement l'index du site et non pas l'url d'un produit".center(
                                92
                            )
                            + Style.RESET_ALL
                        )
                        time.sleep(4)
                        URL()
                    else:
                        clean()
                        print(
                            Style.BRIGHT
                            + Fore.RED
                            + "[ ERROR ] L'url que vous avez entré ne semble pas être un site shopify".center(
                                92
                            )
                            + "\n"
                            + "veuillez essayer une autre url".center(92)
                            + Style.RESET_ALL
                        )
                        time.sleep(4)
                        URL()
                except Exception:
                    clean()
                    print(
                        Style.BRIGHT
                        + Fore.RED
                        + "[ ERROR ] Site web indisponible. Veuillez verifier votre connection internet".center(
                            92
                        )
                        + "\n"
                        + "et verifier que l'url est valide (avec https://)".center(92)
                        + Style.RESET_ALL
                    )
                    time.sleep(4)
                    URL()

            # Scrap les infos utiles des produits
            bs = soup(r.text, "html.parser")
            shoptitle = bs.select_one("title").text
            products = []
            for allProducts in bs.find_all("entry"):
                if len(allProducts) == 0:
                    print(Style.RESET_ALL)
                    clean()
                    print(
                        Style.BRIGHT
                        + Fore.RED
                        + "[ ERROR ] Aucun produit trouvé, veuillez verifier que l'url est valide et que le site ai au moins un item.".center(
                            92
                        )
                        + Style.RESET_ALL
                    )
                    time.sleep(3)
                    URL()

                for product in allProducts.find("title"):
                    # Nettoie les balises HTML des titres de produits
                    cleaned = re.compile('<.*?>') 
                    productTitle = re.sub(cleaned, '', product)
                    productLink = product.parent.parent.find("link")["href"]
                    price = product.parent.parent.find("s:price").text
                    currency = product.parent.parent.find("s:price")["currency"]
                    products.append([productTitle, productLink, price, currency])

            clean()
            
            # Récap que le site est bien le bon
            print(
                Fore.YELLOW
                + "".center(34)
                + "Titre du magasin: "
                + Fore.WHITE
                + shoptitle
                + Style.RESET_ALL
                + "\n"
            )
            print(
                "Cette information est-elle correcte?\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\n"
                + "["
                + Fore.RED
                + "1"
                + Style.RESET_ALL
                + "] "
                + Fore.GREEN
                + "OUI"
                + Style.RESET_ALL
                + "\n["
                + Fore.RED
                + "2"
                + Style.RESET_ALL
                + "] "
                + Fore.GREEN
                + "NON"
                + Style.RESET_ALL
            )
            try:
                validity = int(
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
                URL()
            if int(validity) < 1 or int(validity) > 2:
                clean()
                print(
                    Style.BRIGHT
                    + Fore.RED
                    + "[ ERROR ] Veuillez choisir une des options".center(92)
                    + Style.RESET_ALL
                )
                time.sleep(2)
                URL()
            if int(validity) == 1:
                try:
                    
                    # Récupères des données pour l'éventuelle checkout d'un produit
                    response = session.get(products[0][1], verify=False)

                    bs = soup(response.text, "html.parser")
                    scripts = bs.findAll("script")
                    jsonObj = None

                    for s in scripts:
                        if "var meta" in s.text:
                            script = s.text
                            script = script.split("var meta = ")[1]
                            script = script.split(";\nfor (var attr in meta)")[0]

                            jsonStr = script
                            jsonObj = json.loads(jsonStr)
                    for value in jsonObj["product"]["variants"]:
                        VariantPrice = int(value["price"]) / 100
                        variantID = value["id"]
                        break

                except Exception:
                    try:
                        response = session.get(products[0][1], verify=False)

                        bs = soup(response.text, "html.parser")
                        scripts = bs.findAll("script")
                        jsonObj = None

                        for s in scripts:
                            if "var meta" in s.text:
                                script = s.text
                                script = script.split("var meta = ")[1]
                                script = script.split(";\nfor (var attr in meta)")[0]

                                jsonStr = script
                                jsonObj = json.loads(jsonStr)
                        for value in jsonObj["product"]["variants"]:
                            VariantPrice = int(value["price"]) / 100
                            variantID = value["id"]
                            break
                    except Exception as e:
                        print(Style.RESET_ALL)
                        clean()
                        print(
                            Style.BRIGHT
                            + Fore.RED
                            + "[ ERROR ] Une erreur s'est produite:".center(92)
                            + "\n"
                            + str(e).center(92)
                            + Style.RESET_ALL
                        )
                        time.sleep(3)
                        URL()

                class Data:
                    pass

                Config = Data()
                Config.name = shoptitle
                Config.link = r.url.replace("/collections/all/products.atom", "")
                Config.currency = products[0][3]
                Config.productid = variantID
                Config.price = VariantPrice
                liste(products, Config)

            elif int(validity) == 2:
                URL()
        except Exception as e:
            print(Style.RESET_ALL)
            clean()
            print(
                Style.BRIGHT
                + Fore.RED
                + "[ ERROR ] Une erreur s'est produite:".center(92)
                + "\n"
                + str(e).center(92)
                + Style.RESET_ALL
            )
            time.sleep(3)
            URL()
