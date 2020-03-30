# -*- coding: utf-8 -*-
# cython: language_level=3
"""
Created on Mon Mar 30 15:21:35 2020

@author: Liam Cornu
"""

import requests
from urllib3.util.retry import Retry
import urllib3
from requests.adapters import HTTPAdapter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lxml import html
from colorama import Style, Fore
from init import clean
import time


def Fetch_Coupons(Name):
    try:
        
        # En cas d'erreur HTTP, renvoyer la requête
        session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504, 408]
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))
        
        # Utilise l'API de recherche de promocodes.com pour chercher le nom du site Shopify
        fetch_url = session.get(
            f"https://www.promocodes.com/search?term={Name}",
            verify=False,
            allow_redirects=True,
        )
        try:

            url = fetch_url.json()["MerchantMatches"][0]["Url"]
            try:
                
                # Envoie une requête à la page promocodes.com du site shopify
                fetch_codes = session.get(
                    f"https://www.promocodes.com{url}",
                    verify=False,
                    allow_redirects=True,
                )
                root = html.fromstring(fetch_codes.text)
                
                # Scrap les IDs des codes promos
                coupon_ids = []
                for item in root.xpath(
                    '//*[@class="coupon-cta btn btn-main-outline"]/@data-coupon-id'
                ):
                    coupon_ids.append(item)
                for item in root.xpath(
                    '//*[@class="coupon-cta btn btn-main-outline js-coupon-modal"]/@data-coupon-id'
                ):
                    coupon_ids.append(item)
                try:
                    coupons = []
                    
                    # Récupères les codes promos à l'aide des IDs
                    for item in coupon_ids:
                        try:
                            get_coupon = session.get(
                                "https://www.promocodes.com/couponmodals/coupon",
                                params={"couponId": item},
                            )
                        except Exception as e:
                            print(e)
                            pass
                        if "No promo code needed" in get_coupon.text:
                            pass
                        else:
                            root = html.fromstring(get_coupon.text)
                            coupon = root.xpath(
                                '//*[@class="coupon-modal-code"]/text()'
                            )[0]
                            discount = root.xpath(
                                '//*[@class="coupon-headline-savings"]/text()'
                            )[0]
                            coupons.append([coupon, discount])
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
                    coupons = None

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
                coupons = None

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
            coupons = None

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
        coupons = None

    return coupons
