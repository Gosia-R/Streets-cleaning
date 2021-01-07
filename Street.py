#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from copy import deepcopy

'''
klasa zawierajaca informacje o ulicach:
-dlugosc
-zabrudzenie
-macierz polaczen
-wektor posprzatanych ulic
'''


class Streets:
    def __init__(self):

        self.n = 16  # liczba skrzyzowan

        self.A = np.array([[0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
                         [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                         [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                         [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                         [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
                         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                         [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]])



        self.L = self.A * 10

        '''np.array([[0, 55, 18, 0, 0],  # macierz odleglosci pomiedzy skrzyzowaniami
                           [55, 0, 0, 0, 74],
                           [18, 0, 0, 68, 73],
                           [0, 0, 68, 0, 78],
                           [0, 74, 73, 78, 0]])'''

        self.G = np.array([[0, 5, 0, 10, 0, 0, 0, 0, 0, 0, 0, 15, 0, 5, 0, 0],
                         [5, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                         [0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
                         [10, 0, 0, 0, 10, 0, 15, 0, 0, 0, 15, 0, 0, 0, 0, 0],
                         [0, 5, 0, 10, 0, 5, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 5, 0, 5, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 15, 0, 0, 0, 15, 0, 15, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 10, 0, 15, 0, 10, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 10, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                         [0, 0, 0, 15, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0],
                         [15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 10, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 10, 0, 0],
                         [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 5, 0],
                         [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5],
                         [0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0]])

        '''np.array([[0, 2, 2, 0, 0],  # macierz zabrudzenia ulic
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
        #self.n = 40

        #self.A = self.generate_new_A()

        #self.L = self.generate_new_L(10, 80)

        #self.G = self.generate_new_G()

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

    def load_matrices(self, folder_path):
        temp1 = temp2 = temp3 = 0
        matrices = {'A': temp1, 'G': temp2, 'L': temp3}
        for key, value in matrices.items():
            file_path = folder_path + key + '.xlsx'
            df = pd.read_excel(file_path)
            matrices[key] = df.to_numpy()
        self.A = matrices['A']
        self.G = matrices['G']
        self.L = matrices['L']

    def save_matrices(self, folder_path):
        matrices = {'A': self.A, 'G': self.G, 'L': self.L}
        for key, value in matrices.items():
            file_path = folder_path + key + '.xlsx'
            df = pd.DataFrame(data=value)
            writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='data', index=False)
            writer.save()

    def Floyd_Warshall(self):  # Floyd-Warshall lub djikstra z BFS
        # Floyd z opensourca,

        G_copy = deepcopy(self.G)
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


'''
#Test zapisywania i wczytywania ulic
ulice1 = Streets()
ulice1.save_matrices(r'temp/')
ulice2 = Streets()
print(ulice2.A)
ulice2.load_matrices(r'temp/')

print('ul1', ulice1.A)
print('ul2', ulice2.A)
'''

'''
#miasto z mostem 

ulica = Streets()
print('To jest poczatkowe A:')
print(ulica.A)
for row in range(int(ulica.n/2), ulica.n):
    for col in range(int(ulica.n/2)):
        ulica.A[row][col] = 0

for row in range(int(ulica.n/2)):
    for col in range(int(ulica.n/2), ulica.n):
        ulica.A[row][col] = 0

ulica.A[15,3] = 1
ulica.A[3,15] = 1
print('\n \n To jest zmienione A:')
print(ulica.A)

ulica.G = ulica.generate_new_G()
ulica.L = ulica.generate_new_L(20, 80)
print('\n\n To jest zmienione G:')
print(ulica.G)
print('\n\n To jest zmienione L:')
print(ulica.L)
ulica.save_matrices(folder_path=r'most/')
'''

ulica = Streets()
ulica.save_matrices(folder_path=r'przypadki_testowe/maly/')