# -*- coding: utf-8 -*-
# cython: language_level=3
"""
Created on Mon Mar 30 18:03:31 2020

@author: Liam Cornu
"""
import requests
from colorama import Style, Fore
from init import clean
import time
from lxml import html
import datetime
import random
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def Check_Balance(Code, Config):
    
    # Ajoute un item au panier
    clean()
    print("[ INFO ] En cours de checkout...".center(92) + "\n")
    session = requests.Session()
    retries = Retry(
        total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504, 408]
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    link = "%s/cart/add.js?quantity=1&id=%s" % (Config.link, str(Config.productid))

    try:
        session.get(link, verify=False, allow_redirects=True)
    except Exception:
        try:
            session.get(link, verify=False, allow_redirects=True)
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
    
    # Passe au checkout
    tempLink = "%s//checkout.json" % Config.link
    try:
        response = session.get(tempLink, verify=False, allow_redirects=True)
    except Exception:
        try:
            time.sleep(5)
            response = session.get(tempLink, verify=False, allow_redirects=True)
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
    
    # Scrap de données et mises en place des paramètres de checkout
    tree = html.fromstring(response.text)
    authToken = tree.xpath('//*[@name="authenticity_token"]/@value')[0]
    checkout = response.url
    _landing_page = response.url.replace(Config.link, "")
    _orig_referrer = Config.link + "/cart"
    checkoutLink = checkout.replace(Config.link, "https://checkout.shopify.com")
    
    # Placeholder des cookies
    _secure_session_id = "null"
    checkout_token_cookie = "null"
    checkout_cookie = "null"
    _shopify_s = "null"
    _shopify_y = "null"
    _shopify_fs = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    tracked_start_checkout = "null"
    checkout_locale = "en"
    for cookie in response.cookies:
        if cookie.name == "checkout":
            checkout_cookie = cookie.value
        elif cookie.name == "checkout_token":
            checkout_token_cookie = cookie.value
        elif cookie.name == "_secure_session_id":
            _secure_session_id = cookie.value
        elif cookie.name == "_shopify_y":
            _shopify_y = cookie.value
        elif cookie.name == "_shopify_s":
            _shopify_s = cookie.value
        elif cookie.name == "tracked_start_checkout":
            tracked_start_checkout = cookie.value
        elif cookie.name == "checkout_locale":
            checkout_locale = cookie.value
    time.sleep(0.8)
    _shopify_sa_t = (
        datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    )
    
    # Mise en place des cookies de la requête
    request_cookies = {
        "_landing_page": _landing_page,
        "_orig_referrer": _orig_referrer,
        "_s": _shopify_s,
        "_secure_session_id": _secure_session_id,
        "_shopify_fs": _shopify_fs,
        "_shopify_s": _shopify_s,
        "_shopify_sa_p": "",
        "_shopify_sa_t": _shopify_sa_t,
        "_shopify_y": _shopify_y,
        "cart_sig": "",
        "checkout": checkout_cookie,
        "checkout_locale": checkout_locale,
        "checkout_token": checkout_token_cookie,
        "secure_customer_sig": "",
        "test_cookie": "",
        "tracked_start_checkout": tracked_start_checkout,
    }
    browser_width = str(random.randint(1080, 2046))
    browser_height = str(random.randint(720, 1080))
    ts = time.time()
    utc_offset = round(
        (
            datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts)
        ).total_seconds()
        / 60
    )
    
    # Paramètres data pour la requête POST
    params = {
        "_method": "patch",
        "authenticity_token": authToken,
        "step": "contact_information",
        "checkout[reduction_code]": Code,
        "checkout[client_details][browser_width]": browser_width,
        "checkout[client_details][browser_height]": browser_height,
        "checkout[client_details][javascript_enabled]": "1",
        "checkout[client_details][color_depth]": "24",
        "checkout[client_details][java_enabled]": "false",
        "checkout[client_details][browser_tz]": utc_offset,
    }
    # Applique le code carte cadeau/coupon au produit
    try:
        check = requests.post(
            checkoutLink, cookies=request_cookies, data=params, allow_redirects=True
        )
    except Exception:
        try:
            check = requests.post(
                checkoutLink, cookies=request_cookies, data=params, allow_redirects=True
            )
        except Exception:
            check = None
    clean()
    print(Style.BRIGHT + "Résultats".center(92) + "\n" + "¯¯¯¯¯¯¯¯¯".center(92))
    if check is None:
        print(
            "La carte/code "
            + Fore.YELLOW
            + Code
            + Style.RESET_ALL
            + " n'est pas valide ou a une valeur nul"
        )
    else:
        
        # Vérifie si la valeur du produit a changé
        tree = html.fromstring(check.text)
        price = (
            int(
                tree.xpath(
                    '//*[@class="total-recap__final-price"]/@data-checkout-payment-due-target'
                )[0]
            )
            / 100
        )
        
        # Si oui on calcule la valeur du code/carte cadeau
        if float(price) != float(Config.price):
            balance = float(Config.price) - float(price)
            percentage = float(balance) / float(price) * 100
            print(
                "La carte/code "
                + Fore.YELLOW
                + Code
                + Style.RESET_ALL
                + " a une valeur de "
                + Fore.GREEN
                + str("{:.2f}".format(balance))
                + " "
                + Style.DIM
                + Config.currency
                + Style.RESET_ALL
                + " (soit "
                + str("{:.2f}".format(percentage))
                + "%)"
                + Style.RESET_ALL
            )
        
        # Si la valeur n'a pas changé, le code est invalide ou de valeur nul
        else:
            print(
                "La carte/code "
                + Fore.YELLOW
                + Code
                + Style.RESET_ALL
                + " n'est pas valide ou a une valeur nul"
            )
    print("\n" * 3)
    print(
        "Appuyez sur la touche Entrée pour continuer\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"
    )
    input()
