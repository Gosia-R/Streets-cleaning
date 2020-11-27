#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
'''
funkcje potrzebne do algorytmu


'''

def initialize(): # inicjalizacja pierwszego rozwiazania
    pass

def mutate(): # mutacje, mozliwe ze lepiej zrobic 3 osobne funkcje dla kazdej mutacji
    pass

def is_allowed(): #s sprawdza czy dana mutacja jest dozwolona (czy wszystkie ulice sa posprzatane
    pass

def accept_new(): # sprawdza czy przyjmujemy wygenerowane rozwiazenie
    pass

def calculate_cost(): # liczy koszt (funkcja celu)
    pass

def graf(graph): # Floyd-Warshall lub djikstra z BFS
    #Floyd z opensourca,
    #number of vertices
    v = len(graph)

    # path reconstruction matrix
    p = np.zeros(graph.shape)
    for i in range(0, v):
        for j in range(0, v):
            p[i, j] = i
    #     if (i != j and graph[i,j] == 0): nwm po co to było, czm nie chcieli używać zerowych u nas chyba useless
    #        p[i,j] = -30000
    #         graph[i,j] = 30000 # set zeros to any large number which is bigger then the longest way

    for k in range(0, v):
        for i in range(0, v):
            for j in range(0, v):
                if graph[i, j] > graph[i, k] + graph[k, j]:
                    graph[i, j] = graph[i, k] + graph[k, j]
                    p[i, j] = p[k, j]
    return p

def reconstruct_path(p, i, j,op,k=0):
    i,j = int(i), int(j)
    if(i==j and k!=0):
        op.append(i)
        print (i,)
    #elif(p[i,j] == -30000):
        #print (i,'-',j)
    else:
        k = k+1
        reconstruct_path(p, i, p[i,j],op,k)
        op.append(j)
def kochanie_Masia ():
    Maś = jest kochany
    pass