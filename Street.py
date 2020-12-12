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
        '''
        self.n = 5  # liczba skrzyzowan

        self.A = np.array([[0, 1, 1, 1, 1, 0, 1, 0]
                         [1, 0, 1, 0, 0, 0, 1, 0]
                         [1, 1, 0, 1, 0, 1, 1, 0]
                         [1, 0, 1, 0, 1, 0, 0, 1]
                         [1, 0, 0, 1, 0, 1, 0, 0]
                         [0, 0, 1, 0, 1, 0, 1, 1]
                         [1, 1, 1, 0, 0, 1, 0, 1]
                         [0, 0, 0, 1, 0, 1, 1, 0]])

        self.L = np.array([[0, 55, 18, 0, 0],  # macierz odleglosci pomiedzy skrzyzowaniami
                           [55, 0, 0, 0, 74],
                           [18, 0, 0, 68, 73],
                           [0, 0, 68, 0, 78],
                           [0, 74, 73, 78, 0]])

        self.G = np.array([[0, 2, 2, 0, 0],  # macierz zabrudzenia ulic
                           [2, 0, 0, 0, 2],
                           [2, 0, 0, 3, 1],
                           [0, 0, 3, 0, 3],
                           [0, 2, 1, 3, 0]])


            self.A = np.array([[0, 1, 1, 1, 1, 0, 1, 0],
                     [1, 0, 1, 0, 0, 0, 1, 0],
                     [1, 1, 0, 1, 0, 1, 1, 0],
                     [1, 0, 1, 0, 1, 0, 0, 1],
                     [1, 0, 0, 1, 0, 1, 0, 0],
                     [0, 0, 1, 0, 1, 0, 1, 1],
                     [1, 1, 1, 0, 0, 1, 0, 1],
                     [0, 0, 0, 1, 0, 1, 1, 0]])
        '''
        self.n = 40

        self.A = self.generate_new_A()

        self.L = self.generate_new_L(10, 80)

        self.G = self.generate_new_G()

        self.r = np.sum(np.triu(self.A, 1))  # liczba ulic

        self.fw_graph = self.Floyd_Warshall()


    def generate_new_A(self):
        matrix = np.random.rand(self.n, self.n)
        u_matrix = np.triu(matrix, 1)
        l_matrix = u_matrix.T
        sym_matrix = u_matrix + l_matrix
        new_A = np.round(sym_matrix)
        return new_A

    def generate_new_L(self, dist_min, dist_max):
        dist = np.random.randint(dist_min, dist_max, size=(self.n, self.n))
        u_dist = np.triu(dist, 1)
        l_dist = u_dist.T
        dist = u_dist + l_dist
        new_L = np.multiply(self.A, dist)
        return new_L

    def generate_new_G(self):
        g_matrix = np.random.randint(1, 4, (self.n, self.n))
        u_g_matrix = np.triu(g_matrix, 1)
        l_g_matrix = u_g_matrix.T
        g_matrix = u_g_matrix + l_g_matrix
        new_G = np.multiply(self.A, g_matrix)
        return new_G

    def Floyd_Warshall(self):  # Floyd-Warshall lub djikstra z BFS
        # Floyd z opensourca,

        G_copy = self.G
        # path reconstruction matrix
        fw_graph = np.zeros(self.G.shape)
        for i in range(0, self.n):
            for j in range(0, self.n):
                fw_graph[i, j] = i
                if G_copy[i, j] == 0:
                    fw_graph[i, j] = -30000
                    G_copy[i, j] = 30000  # set zeros to any large number which is bigger then the longest way

        for k in range(0, self.n):
            for i in range(0, self.n):
                for j in range(0, self.n):
                    if G_copy[i, j] > G_copy[i, k] + G_copy[k, j]:
                        G_copy[i, j] = G_copy[i, k] + G_copy[k, j]
                        fw_graph[i, j] = fw_graph[k, j]
        return fw_graph



