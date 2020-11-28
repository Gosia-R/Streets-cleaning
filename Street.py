#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

'''
klasa zawierajaca informacje o ulicach:
-dlugosc
-zabrudzenie
-macierz polaczen
-wektor posprzatanych ulic
'''


class Streets:
    def __init__(self):
        self.n = 5  # liczba skrzyzowan

        self.A = [[0, 1, 1, 0, 0],  # macierz polaczen pomiedzy skrzyzowaniami
                  [1, 0, 0, 0, 1],
                  [1, 0, 0, 1, 1],
                  [0, 0, 1, 0, 1],
                  [0, 1, 1, 1, 0]]

        self.L = [[0, 55, 18, 0, 0],  # macierz odleglosci pomiedzy skrzyzowaniami
                  [55, 0, 0, 0, 74],
                  [18, 0, 0, 68, 73],
                  [0, 0, 68, 0, 78],
                  [0, 74, 73, 78, 0]]

        self.G = [[0, 2, 2, 0, 0], # macierz zabrudzenia ulic
                  [2, 0, 0, 0, 2],
                  [2, 0, 0, 3, 1],
                  [0, 0, 3, 0, 3],
                  [0, 2, 1, 3, 0]]

        self.n = np.sum(np.triu(self.A, 1))  # liczba ulic

        self.P = np.array([]) # wektor posprzatanych ulic

    def generate_new_A(self):
        matrix = np.random.rand(self.n, self.n)
        u_matrix = np.triu(matrix, 1)
        l_matrix = u_matrix.T
        sym_matrix = u_matrix + l_matrix
        self.A = np.round(sym_matrix)

    def generate_new_L(self, dist_min, dist_max):
        dist = np.random.randint(dist_min, dist_max, size=(self.n, self.n))
        u_dist = np.triu(dist, 1)
        l_dist = u_dist.T
        dist = u_dist + l_dist
        self.L = np.multiply(self.A, dist)

    def generate_new_G(self):
        g_matrix = np.random.randint(1, 4, (self.n, self.n))
        u_g_matrix = np.triu(g_matrix, 1)
        l_g_matrix = u_g_matrix.T
        g_matrix = u_g_matrix + l_g_matrix
        self.G = np.multiply(self.A, g_matrix)
