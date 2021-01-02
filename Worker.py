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
        self.m = 20 # ilosc pracownikow

        self.w = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                  10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

        self.trasy = [] # wektor zawierajacy kolejno ulice (para wierzcholkow) ktorymi przechodzi kazdy pracownik

        self.P = []  # wektor posprzatanych ulic

    def route_lengths(self, L : np.array):
        route_lengths_list = []
        idx = 0
        for current_worker in self.trasy:
            route_lengths_list.append(0)
            for current_street in current_worker:
                route_lengths_list[idx] += L[tuple(current_street)]
            idx += 1
        return route_lengths_list

    def reset_P(self):
        self.P = []