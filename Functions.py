#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import Worker
import Street

#Stworzenie obiektów będzie pomagać
workers = Worker.Workers()
streets = Street.Streets()

'''
funkcje potrzebne do algorytmu


'''
def finding_next_poit_init(i,n,P,A):
    for k in range(n):
        if A[i, k] == 1 and ((i, k) and (k, i) not in P):
            return k
    return -1
def finding_next_poit_init_not_OG(i,n,P,A):
    for k in range(n):
        if A[i, k] == 1 :
            return k
    return -1

def initialize(Workers): # inicjalizacja pierwszego rozwiazania
   i = 0
   while len(P)!= n:
       for j in range (0,w): # inny range ale nwm jaki
            next_node = finding_next_poit_init(i, n, P, A)
            if next_node != -1:
                pi[j].append(i, next_node)
                P.append(i, next_node)
            else:
                next_node = finding_next_poit_init_not_OG(i,n,P,A)
                pi[j].append(i, next_node)
            i = next_node
   for j in range(0, w):
       pi[j,:] = reconstruct_path(p,pi[j,-1](1),0,pi[j,:])
    return pi
def mutate(): # mutacje, mozliwe ze lepiej zrobic 3 osobne funkcje dla kazdej mutacji
    pass

def is_allowed(): #s sprawdza czy dana mutacja jest dozwolona (czy wszystkie ulice sa posprzatane
    pass

def accept_new(): # sprawdza czy przyjmujemy wygenerowane rozwiazenie
    pass

def is_cleaned(street: tuple, helper_matrix: np.array, G: np.array): # funkcja sprawdzajaca czy ulica jest posprzatana
    starting_index, final_index = street
    reversed_street = final_index, starting_index     # ta sama ulica moze byc opisana z obu stron ( (3,1) = (1,3))
    if helper_matrix[street] == 0:   # sprawdzenie czy ktos przeszedl ta ulica, jesli tak to jest ona posprzatana
        helper_matrix[street] += 1   # ulica jest posprzatana
        helper_matrix[reversed_street] += 1     # zachowanie symetrycznosci
        return G[street], helper_matrix      # zwraca koszt posprzatania ulicy zgodny z macierza G oraz zmieniana macierz helper_matrix
    else:
        return 0.5, helper_matrix       # zwraca koszt przejscia posprzatana ulica oraz niezmieniona macierz helper_matrix


def calculate_cost(workers: Worker.Workers, streets: Street.Streets): # liczy koszt (funkcja celu)
    current_worker_id = 0
    cost = 0
    helper_matrix = np.zeros(streets.G.shape()) # macierz sprawdzajaca czy ulica jest posprzatana ( 0 - nie posprzatana, 1 - posprzatana)

    for current_worker in workers.trasy:   # petla przechodzaca po kazdym pracowniku
        for street in current_worker:   # petla przechodzaca po kazdej ulicy (krotka z numerami wierzcholkow) danego pracownika
            g_value, helper_matrix = is_cleaned(tuple(street), helper_matrix, streets.G)
            cost += streets.L[tuple(street)] * g_value / workers.w[current_worker_id] # zwiekszenie funkcji kosztu
        current_worker_id += 1  # id kolejnego pracownika
    return cost

def graf(graph): # Floyd-Warshall lub djikstra z BFS
    #Floyd z opensourca,
    #number of vertices
    v = len(graph)

    # path reconstruction matrix
    p = np.zeros(graph.shape)
    for i in range(0, v):
        for j in range(0, v):
            p[i, j] = i
            if graph[i,j] == 0:
                p[i,j] = -30000
                graph[i,j] = 30000 # set zeros to any large number which is bigger then the longest way

    for k in range(0, v):
        for i in range(0, v):
            for j in range(0, v):
                if graph[i, j] > graph[i, k] + graph[k, j]:
                    graph[i, j] = graph[i, k] + graph[k, j]
                    p[i, j] = p[k, j]
    return p

def reconstruct_path(p, i, j,op):
    if (p[i, j] == i):
        op = np.append(op, (i, j))
        return op
    elif (p[i, j] == -30000):
        print(i, '-', j)
    else:
        op = np.append(op, (i, p[i, j]))
        k = p[i, j]
        k = int(k)
        while p[i, k] != i:
            k = int(k)
            op = np.append(op, (k, p[i, k]))
            k = p[i, k]
            k = int(k)
        op = np.append(op, (k, j))
    return op
def kochanie_Masia ():
    Maś = jest kochany
    pass