# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:44:33 2020

@author: Liam Cornu
"""
from init import logger
from title import Start
import sys

# Code principal qui lance l'application
def main():
    try:
        Start()
    # En cas d'erreur on enregistre le traceback dans un log
    except Exception as e:
        logger().exception("Erreur\n" + str(e) + "\n===============================")
        sys.exit()


main()
