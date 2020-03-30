# -*- coding: utf-8 -*-
# cython: language_level=3
"""
Created on Tue Apr 16 23:02:40 2019

@author: Liam Cornu
"""

import ctypes
from ctypes import windll, byref
from ctypes.wintypes import SMALL_RECT
import os

# Paramètres CMD pour la page de notice
def Title_setting():
    # ===== Paramètres Window et CMD =====

    windll.kernel32.SetConsoleTitleW("Shopify Discount Bot Pour ParcourSup")

    os.system("mode con cols=110 lines=50")

    STDOUT = -11
    # ===================================

    # ========= Paramètres CMD Class et Font =========

    handle = ctypes.windll.kernel32.GetStdHandle(STDOUT)
    rect = SMALL_RECT(-2, 0, 89, 50)
    windll.kernel32.SetConsoleWindowInfo(handle, True, byref(rect))

    # ===============================================

# Paramètres CMD pour le logiciel
def Window_setting():
    # ===== Paramètres Window et CMD =====

    windll.kernel32.SetConsoleTitleW("Shopify Discount Bot Pour ParcourSup")

    os.system("mode con cols=92 lines=50")

    STDOUT = -11
    # ===================================

    # ========= Paramètres CMD Class et Font =========

    handle = ctypes.windll.kernel32.GetStdHandle(STDOUT)
    rect = SMALL_RECT(-2, 0, 89, 50)
    windll.kernel32.SetConsoleWindowInfo(handle, True, byref(rect))

    # ===============================================
