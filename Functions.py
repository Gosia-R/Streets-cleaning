#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import Worker
import Street
import random

#Stworzenie obiektów będzie pomagać
workers = Worker.Workers()
streets = Street.Streets()

'''
funkcje potrzebne do algorytmu


'''
def finding_next_poit_init(i,n,P,A):
    chosen_streets_list = []
    for k in range(n): #iterujemy po skrzyżowaniach
        if A[i, k] and ([i, k] not in P) and ([k, i] not in P):  #do trasy szukamy tylko takej ulicy która nie została posprzątana
                chosen_streets_list.append(k)
    if len(chosen_streets_list )!= 0:
        return random.choice(chosen_streets_list)
    else:
        return -1

def finding_next_poit_init_already_cleaned(i,n,P,A):
    chosen_streets_list = []
    for k in range(n): #iterujemy po skrzyżowaniach
        if A[i, k]  : #do trasy szukamy którejkolwiek ulicy
            chosen_streets_list.append(k)
    if len(chosen_streets_list) != 0:
        return random.choice(chosen_streets_list)
    else:
        return -1

def initialize(workers,streets): # inicjalizacja pierwszego rozwiazania
    i = 0
    for j in range(0, workers.m):
        workers.trasy.append([])
    while len(workers.P)< streets.r: #dopóki każda ulica nie będzie w P
        for j in range (0,workers.m): #iterujemy po pracownikach
            if i != 0:
                i = int(workers.trasy[j][-1][1])
            next_node = finding_next_poit_init(i, streets.n, workers.P, streets.A)#szukamy następnej ulicy, takej która jeszcze nie została posprzątana

            if next_node != -1:
                workers.trasy[j].append([i, next_node])  #dodajemy ulicę do trasy i rozwiąznia
                workers.P.append([i, next_node])
            else:
                next_node = finding_next_poit_init_already_cleaned(i, streets.n, workers.P, streets.A)#szukamy następnej ulicy, jakielkolwiek
                workers.trasy[j].append([i, next_node]) #dodajemy ulicę do trasy
        i = 1
    for j in range(0, workers.m):
       workers.trasy[j] = reconstruct_path(workers.fw_graph, workers.trasy[j][-1][1],0, workers.trasy[j]) #może Floyda robić już w klasie
    return workers.trasy


def is_allowed(r : int, test_P : list ): #s sprawdza czy dana mutacja jest dozwolona (czy wszystkie ulice sa posprzatane
    if len(test_P) == r:
        return True
    else:
        return False

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


def adjacent_solution(workers : Worker.Workers, streets : Street.Streets): # mutacje, mozliwe ze lepiej zrobic 3 osobne funkcje dla kazdej mutacji
    chosen_type = random.choices([1, 2, 3], [45, 55 / 2, 55 / 2], 1)  # rozne mutacje maja rozne prawdopodobienstwa

    if chosen_type == 1:  # zmiana ścieżki
        chosen_worker = random.randrange(0, workers.m)  # wybor losowego pracownika
        chosen_nodes_list = random.choices(workers.trasy[chosen_worker], k=2)  # wybor dwoch losowych skrzyzowan
        starting_node, temp1 = chosen_nodes_list[0]  # pozyskanie punktu startowego
        chosen_node_idx1 = workers.trasy[chosen_worker].index(chosen_nodes_list[0])  # znalezienie indeksu miejsca w ktorym trasa zaczyna sie zmieniac
        temp2, finishing_node = chosen_nodes_list[1]  # pozyskanie punku koncowego
        chosen_node_idx2 = workers.trasy[chosen_worker].index(
        chosen_nodes_list[1])  # znalezienie indeksu miejsca w ktorym trasa konczy sie zemieniac
        mutated_path = []
        mutated_path = reconstruct_path(streets.fw_graph, starting_node, finishing_node, mutated_path)  # uzyskanie zmienionej trasy miedzy dwoma punktami
        new_path = workers.trasy[chosen_worker][:chosen_node_idx1] + mutated_path + workers.trasy[chosen_worker][chosen_node_idx2 + 1:]
        test_P = create_new_P(workers.trasy, new_path, chosen_worker)
        if is_allowed(streets.r, test_P):
            workers.trasy[chosen_worker] = new_path
        else:
    elif chosen_type == 2:
        chosen_worker = random.randrange(0, workers.m)  # wybor losowego pracownika
        for street in chosen_worker:
            workers.trasy[chosen_worker][street] = workers.trasy[chosen_worker][street].revesed()
        workers.trasy[chosen_worker] = workers.trasy[chosen_worker].reversed()  # pracownik przechodzi trase w inna strone
    elif chosen_type == 3:  # para pracownikow zamienia trasy
        chosen_workers_list = random.choices(workers.trasy, k=3)
        chosen_worker_idx1 = workers.trasy.index(chosen_workers_list[0]) 
        chosen_worker_idx2 = workers.trasy.index(chosen_workers_list[1])
        chosen_worker_idx3 = workers.trasy.index(chosen_workers_list[2])
        most_efficient_worker = workers.w.index(max([workers.w[chosen_worker_idx1], workers.w[chosen_worker_idx2], workers.w[chosen_worker_idx3]]))
        route_length_list = []
        idx = 0
        for current_worker in chosen_workers_list:
            for current_street in current_worker:
                route_length_list[idx] += streets.L[tuple(current_street)]
            idx += 1
        longest_route_idx = workers.trasy.index(chosen_workers_list[route_length_list.index(max(route_length_list))])
        temp = workers.trasy[most_efficient_worker]
        workers.trasy[most_efficient_worker] = workers.trasy[longest_route_idx]
        workers.trasy[longest_route_idx] = temp

def create_new_P(trasy : list, new_path : list, path_idx :int):
    new_P = []
    idx = 0
    for current_worker in trasy:
        if idx == path_idx:
            current_worker = new_path
        for current_street in current_worker:
            if current_street not in new_P and current_street.reversed() not in new_P:
                new_P.append(current_street)

    return new_P

def fix  (streets: Street.Streets, workers : Worker.Workers):
    x, y = np.nonzero(np.triu(streets.A))
    omitted_streets = []
    route_lengths_list = workers.route_lengths(streets.L)
    min_index = route_lengths_list.index(min(route_lengths_list))
    for idx in range(0,len(x)):
        if [x[idx],y[idx]] or [y[idx],x[idx]] not in workers.P:
            omitted_streets.append([x[idx],y[idx]])
    for idx in range (0,len(omitted_streets)):
        for jdx in range (0, len(workers.trasy[min_index])):
            if x(idx) or y(idx) in workers.trasy[min_index][jdx]:

    pass


print((np.nonzero(np.triu(streets.A))))