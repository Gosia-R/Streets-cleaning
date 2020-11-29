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
    for k in range(n): #iterujemy
        if A[i, k] == 1 and ((i, k) and (k, i) not in P):
            return k
    return -1

def finding_next_poit_init_already_cleaned(i,n,P,A):
    for k in range(n):
        if A[i, k] == 1 :
            return k
    return -1

def initialize(workers,streets): # inicjalizacja pierwszego rozwiazania
    i = 0
    while len(streets.P)!= streets.n: #dopóki każda ulica nie będzie w P
        for j in range (0,workers.m): # iterujemy po pracownikach
            next_node = finding_next_poit_init(i, streets.n, streets.P, streets.A)#szukamy następnej ulicy, takej któr
            if next_node != -1:
                workers.trasy[j].append(i, next_node)
                workers.P.append(i, next_node)
            else:
                next_node = finding_next_poit_init_already_cleaned(i, streets.n, workers.P, streets.A)
                workers.trasy[j].append(i, next_node)
            i = next_node
    for j in range(0, workers.m):
       p = graf(streets.L)
       workers.trasy[j,:] = reconstruct_path(p,workers.trasy[j,-1](1),0, workers.trasy[j,:]) #może Floyda robić już w klasie
    return workers.trasy
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
    if p[i, j] == i:
        op.append([i, j])
        return op
    elif p[i, j] == -30000:
        print(i, '-', j)
    else:
        op.append([i, int(p[i, j])])
        k = p[i, j]
        k = int(k)
        while p[i, k] != i:
            k = int(k)
            op.append([k, int(p[i, k])])
            k = p[i, k]
            k = int(k)
        op.append([k, j])
    return op

graph = np.array([[0,10,20,30,50,30],[5,6,7,4,30,7],[3,5,1,3,4,5],[1,5,6,40,10,5],[2,3,12,34,34,4],[45,5,7,9,6,34]])
op =  []
p = graf(graph)
# reconstruct the path from 0 to 5
c = (reconstruct_path(p,0,4,op))
print(c)