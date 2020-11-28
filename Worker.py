#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
'''
klasa zawierajaca informacje o pracownikach:
-ich wydajnosc
-liste list z ich trasami?
'''

class Workers :
    def __init__(self):
        self.m = 3 # ilosc pracownikow

        self.wydajnosc = np.array([10, 10, 30])

        self.trasy = np.array([np.array([])]) # wektor zawierajacy kolejno ulice (para wierzcholkow) ktorymi przechodzi kazdy pracownik