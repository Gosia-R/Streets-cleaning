#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import Worker
import Street
import random
from copy import deepcopy

#Stworzenie obiektów będzie pomagać
#workers = Worker.Workers()
#streets = Street.Streets()

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
            if len(workers.trasy[j])!=0:
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
       workers.trasy[j] = reconstruct_path(streets.fw_graph, workers.trasy[j][-1][1],0, workers.trasy[j]) #może Floyda robić już w klasie
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
    helper_matrix = np.zeros(streets.G.shape) # macierz sprawdzajaca czy ulica jest posprzatana ( 0 - nie posprzatana, 1 - posprzatana)

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


def adjacent_solution(new_worker : Worker.Workers, streets : Street.Streets): # mutacje, mozliwe ze lepiej zrobic 3 osobne funkcje dla kazdej mutacji
    chosen_type = random.choices(population=[1, 2, 3], weights=[45, 55 / 2, 55 / 2], k=1)  # rozne mutacje maja rozne prawdopodobienstwa
    chosen_type = chosen_type[0]

    chosen_type = 1
    if chosen_type == 1:  # zmiana ścieżki

        chosen_worker_idx = random.randrange(0, new_worker.m)  # wybor losowego pracownika
        chosen_node_idx1 = random.randrange(15, len(new_worker.trasy[chosen_worker_idx])-5)
        chosen_node_idx2 = random.randrange(2, 4) + chosen_node_idx1
        temp1, starting_node = new_worker.trasy[chosen_worker_idx][chosen_node_idx1]
        finishing_node, temp2 = new_worker.trasy[chosen_worker_idx][chosen_node_idx2]
        mutated_path = []
        mutated_path = reconstruct_path(streets.fw_graph, starting_node, finishing_node, mutated_path)
        new_path = new_worker.trasy[chosen_worker_idx][:chosen_node_idx1+1] + mutated_path + new_worker.trasy[chosen_worker_idx][chosen_node_idx2:]
        new_worker.P = create_new_P(new_worker.trasy, new_path, chosen_worker_idx)
        new_worker.trasy[chosen_worker_idx] = new_path
        if not is_allowed(streets.r, new_worker.P):
            fix(streets, new_worker)

        '''
        chosen_worker = random.randrange(0, new_worker.m)  # wybor losowego pracownika
        chosen_nodes_list = random.choices(new_worker.trasy[chosen_worker], k=2)  # wybor dwoch losowych skrzyzowan
        chosen_node_idx1 = new_worker.trasy[chosen_worker].index(chosen_nodes_list[0])  # znalezienie indeksu miejsca w ktorym trasa zaczyna sie zmieniac
        chosen_node_idx2 = new_worker.trasy[chosen_worker].index(
            chosen_nodes_list[1])  # znalezienie indeksu miejsca w ktorym trasa konczy sie zemieniac
        if chosen_node_idx1 > chosen_node_idx2:
            temp = chosen_nodes_list[0]
            chosen_nodes_list[0] = chosen_nodes_list[1]
            chosen_nodes_list[1] = temp
            temp = chosen_node_idx1
            chosen_node_idx1 = chosen_node_idx2
            chosen_node_idx2 = temp
        temp1, starting_node = chosen_nodes_list[0]  # pozyskanie punktu startowego
        finishing_node, temp2 = chosen_nodes_list[1]  # pozyskanie punku koncowego
        mutated_path = []
        mutated_path = reconstruct_path(streets.fw_graph, starting_node, finishing_node, mutated_path)  # uzyskanie zmienionej trasy miedzy dwoma punktami
        new_path = new_worker.trasy[chosen_worker][:chosen_node_idx1] + mutated_path + new_worker.trasy[chosen_worker][chosen_node_idx2 + 1:]
        new_worker.P = create_new_P(new_worker.trasy, new_path, chosen_worker)
        new_worker.trasy[chosen_worker] = new_path
        if not is_allowed(streets.r, new_worker.P):
            fix(streets, new_worker)
        '''
    elif chosen_type == 2:
        chosen_worker = random.randrange(0, new_worker.m)  # wybor losowego pracownika
        for street in new_worker.trasy[chosen_worker]:
            street_idx = new_worker.trasy[chosen_worker].index(street)
            new_worker.trasy[chosen_worker][street_idx].reverse()
        new_worker.trasy[chosen_worker].reverse()  # pracownik przechodzi trase w inna strone
    elif chosen_type == 3:  # para pracownikow zamienia trasy
        chosen_workers_list = random.choices(new_worker.trasy, k=3)
        chosen_worker_idx1 = new_worker.trasy.index(chosen_workers_list[0])
        chosen_worker_idx2 = new_worker.trasy.index(chosen_workers_list[1])
        chosen_worker_idx3 = new_worker.trasy.index(chosen_workers_list[2])
        most_efficient_worker = new_worker.w.index(max([new_worker.w[chosen_worker_idx1], new_worker.w[chosen_worker_idx2], new_worker.w[chosen_worker_idx3]]))
        route_length_list = []
        idx = 0
        for current_worker in chosen_workers_list:
            route_length_list.append(0)
            for current_street in current_worker:
                route_length_list[idx] += streets.L[tuple(current_street)]
            idx += 1
        longest_route_idx = new_worker.trasy.index(chosen_workers_list[route_length_list.index(max(route_length_list))])
        temp = new_worker.trasy[most_efficient_worker]
        new_worker.trasy[most_efficient_worker] = new_worker.trasy[longest_route_idx]
        new_worker.trasy[longest_route_idx] = temp

def create_new_P(trasy : list, new_path : list, path_idx :int):
    new_P = []
    idx = 0
    for current_worker in trasy:
        if idx == path_idx:
            current_worker = new_path
        for current_street in current_worker:
            start, end = current_street
            if ([start,end]) not in new_P and ([end,start]) not in new_P:
                new_P.append(current_street)

    return new_P

def fix  (streets: Street.Streets, new_workers : Worker.Workers):
    x, y = np.where(np.triu(streets.A))

    omitted_streets = []
    route_lengths_list = new_workers.route_lengths(streets.L)
    route_lengths_list_copy = route_lengths_list[:]
    temp_flag = True
    path_size = len(new_workers.P)
    for idx in range(0,len(x)):
        if [x[idx],y[idx]] or [y[idx],x[idx]] not in new_workers.P:
            omitted_streets.append([x[idx],y[idx]])
    for idx in range(0, len(omitted_streets)):
        temp_flag = False
        route_lengths_list = new_workers.route_lengths(streets.L)
        min_index = route_lengths_list.index(min(route_lengths_list))
        if len(new_workers.P) == path_size + len(omitted_streets):
            break
        while len(new_workers.P) < path_size + len(omitted_streets):
            if temp_flag:
                route_lengths_list_copy[min_index] = 2138764
                min_index = route_lengths_list_copy.index(min(route_lengths_list_copy))
            for jdx in range(len(new_workers.trasy[min_index])):
                idx = int(idx)
                jdx = int(jdx)
                min_index = int(min_index)
                if (int(x[idx]) == new_workers.trasy[min_index][jdx][0])or(int(x[idx]) == new_workers.trasy[min_index][jdx][1]) or (int(y[idx]) == new_workers.trasy[min_index][jdx][1]) or (int(y[idx]) == new_workers.trasy[min_index][jdx][0]):
                    new_workers.P.append([x[idx],y[idx]])
                    new_workers.trasy[min_index] = fix_add_street(new_workers.trasy[min_index],int(x[idx]),int(y[idx]),jdx)
                    temp_flag = True
                    break


def fix_add_street(trasa,x,y,jdx):
    front_half = trasa[:jdx]
    back_half = trasa[jdx+1:]
    if trasa[jdx][0] == x:
        trasa = front_half + [[x,y]] + [[y,x]] + back_half
    else:
        trasa = front_half + [[y,x]] +[[x,y]] +  back_half
    return trasa

