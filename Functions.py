#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import Worker
import Street
import random
from copy import deepcopy
import time
import networkx as nx
import matplotlib.pyplot as plt

fix_time = []
adj1_time = []
adj2_time = []
adj3_time = []



'''
funkcje potrzebne do algorytmu
'''


def finding_next_poit_init(i, n, P, A):
    chosen_streets_list = []
    for k in range(n):  # iterujemy po skrzyżowaniach
        if A[i, k] and ([i, k] not in P) and (
                [k, i] not in P):  # do trasy szukamy tylko takej ulicy która nie została posprzątana
            chosen_streets_list.append(k)
    if len(chosen_streets_list) != 0:
        return random.choice(chosen_streets_list)
    else:
        return -1


def finding_next_poit_init_already_cleaned(i, n, P, A):
    chosen_streets_list = []
    for k in range(n):  # iterujemy po skrzyżowaniach
        if A[i, k]:  # do trasy szukamy którejkolwiek ulicy
            chosen_streets_list.append(k)
    if len(chosen_streets_list) != 0:
        return random.choice(chosen_streets_list)
    else:
        return -1


def initialize(workers, streets):  # inicjalizacja pierwszego rozwiazania
    i = 0
    for j in range(0, workers.m):
        workers.trasy.append([])
    while len(workers.P) < streets.r:  # dopóki każda ulica nie będzie w P
        for j in range(0, workers.m):  # iterujemy po pracownikach
            if len(workers.trasy[j]) != 0:
                i = int(workers.trasy[j][-1][1])
            next_node = finding_next_poit_init(i, streets.n, workers.P,
                                               streets.A)  # szukamy następnej ulicy, takej która jeszcze nie została posprzątana

            if next_node != -1:
                workers.trasy[j].append([i, next_node])  # dodajemy ulicę do trasy i rozwiąznia
                workers.P.append([i, next_node])
            else:
                next_node = finding_next_poit_init_already_cleaned(i, streets.n, workers.P,
                                                                   streets.A)#szukamy następnej ulicy, jakielkolwiek
                workers.trasy[j].append([i, next_node]) #dodajemy ulicę do trasy
        i = 1
    for j in range(0, workers.m):
        workers.trasy[j] = reconstruct_path(streets.fw_graph, workers.trasy[j][-1][1],0,
                                            workers.trasy[j]) #może Floyda robić już w klasie


    return workers.trasy


def is_allowed(r: int, test_P: list):  # sprawdza czy dana mutacja jest dozwolona (czy wszystkie ulice sa posprzatane
    if len(test_P) == r:
        return True
    else:
        return False


def reconstruct_path(p, i, j, op):
    if p[i, j] == i:
        op.append([i, j])
        return op
    elif p[i, j] == -30000:
        print(i, '-', j)
    else:
        path = [int(p[i, j])]
        k = p[i, j]
        k = int(k)
        while p[i, k] != i:
            k = int(k)
            path.append(int(p[i, k]))
            k = p[i, k]
            k = int(k)
        op.append([i, path[-1]])
        for i in range(1, len(path)):
            op.append([path[-i], path[-1 - i]])
        op.append([path[0], j])
    return op


def adjacent_solution(new_worker: Worker.Workers,
                      streets: Street.Streets):  # mutacje, mozliwe ze lepiej zrobic 3 osobne funkcje dla kazdej mutacji
    chosen_type = random.choices(population=[1, 2, 3], weights=[45, 55 / 2, 55 / 2],
                                 k=1)  # rozne mutacje maja rozne prawdopodobienstwa
    chosen_type = chosen_type[0]

    if chosen_type == 1:  # zmiana ścieżki
        tic = time.clock()
        chosen_worker_idx = random.randrange(0, new_worker.m)  # wybor losowego pracownika
        chosen_node_idx1 = random.randrange(1, len(new_worker.trasy[chosen_worker_idx]) - 5)
        chosen_node_idx2 = random.randrange(3, 5) + chosen_node_idx1
        temp1, starting_node = new_worker.trasy[chosen_worker_idx][chosen_node_idx1]
        finishing_node, temp2 = new_worker.trasy[chosen_worker_idx][chosen_node_idx2]
        mutated_path = []
        mutated_path = reconstruct_path(streets.fw_graph, starting_node, finishing_node, mutated_path)

        new_path = new_worker.trasy[chosen_worker_idx][:chosen_node_idx1 + 1] + mutated_path + new_worker.trasy[
                                                                                                   chosen_worker_idx][
                                                                                               chosen_node_idx2:]
        new_P = create_new_P(new_worker.trasy, new_path, chosen_worker_idx)

        new_worker.trasy[chosen_worker_idx] = new_path
        new_worker.P = new_P

        toc = time.clock()
        adj1_time.append(toc - tic)
        if not is_allowed(streets.r, new_worker.P):
            tic = time.clock()
            fix(streets, new_worker)
            toc = time.clock()
            fix_time.append(toc - tic)
    elif chosen_type == 2:
        tic = time.clock()
        chosen_worker = random.randrange(0, new_worker.m)  # wybor losowego pracownika
        for street_idx in range(0, len(new_worker.trasy[chosen_worker])):
            new_worker.trasy[chosen_worker][street_idx].reverse()
        new_worker.trasy[chosen_worker].reverse()  # pracownik przechodzi trase w inna strone
        toc = time.clock()
        adj2_time.append(toc - tic)
    elif chosen_type == 3:  # para pracownikow zamienia trasy
        tic = time.clock()
        chosen_workers_list = random.choices(new_worker.trasy, k=3)
        chosen_worker_idx1 = new_worker.trasy.index(chosen_workers_list[0])
        chosen_worker_idx2 = new_worker.trasy.index(chosen_workers_list[1])
        chosen_worker_idx3 = new_worker.trasy.index(chosen_workers_list[2])
        most_efficient_worker = new_worker.w.index(
            max([new_worker.w[chosen_worker_idx1], new_worker.w[chosen_worker_idx2], new_worker.w[chosen_worker_idx3]]))
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
        toc = time.clock()
        adj3_time.append(toc - tic)


def create_new_P(trasy: list, new_path: list, path_idx: int):
    new_P = []
    idx = 0
    for current_worker in trasy:
        if idx == path_idx:
            current_worker = new_path
        for current_street in current_worker:
            start, end = current_street
            if (([start, end]) not in new_P) and (([end, start]) not in new_P):
                new_P.append(current_street)
        idx += 1

    return new_P


def fix(streets: Street.Streets, new_workers: Worker.Workers):
    x, y = np.where(np.triu(streets.A))
    omitted_streets = []
    path_size = len(new_workers.P)
    for idx in range(0, len(x)):
        if ([x[idx], y[idx]] not in new_workers.P) and ([y[idx], x[idx]] not in new_workers.P):
            omitted_streets.append([x[idx], y[idx]])
    for idx in range(0, len(omitted_streets)):
        cost = deepcopy(new_workers.cost)
        min_index = np.argmin(cost)
        temp_flag = False
        if len(new_workers.P) == path_size + len(omitted_streets):
            break
        while not temp_flag:
            temp_flag = check_if_possible_to_add(new_workers,min_index,idx,omitted_streets)
            if not temp_flag:
                cost[min_index] = 20000
                min_index = np.argmin(cost)


def check_if_possible_to_add(new_workers, min_index, idx, omitted_streets):
    for jdx in range(len(new_workers.trasy[min_index])):
        idx = int(idx)
        jdx = int(jdx)
        min_index = int(min_index)
        if (omitted_streets[idx][0] == new_workers.trasy[min_index][jdx][0]) or (
                omitted_streets[idx][1] == new_workers.trasy[min_index][jdx][1]) or (
                omitted_streets[idx][1] == new_workers.trasy[min_index][jdx][0]) or (
                omitted_streets[idx][0] == new_workers.trasy[min_index][jdx][1]):
            new_workers.P.append(omitted_streets[idx])
            new_workers.trasy[min_index] = fix_add_street(new_workers.trasy[min_index], omitted_streets[idx][0],
                                                          omitted_streets[idx][1], jdx)
            return True

    return False


def fix_add_street(trasa, x, y, jdx):
    front_half0 = trasa[:jdx]
    back_half0 = trasa[jdx:]
    front_half1 = trasa[:jdx + 1]
    back_half1 = trasa[jdx + 1:]

    if (trasa[jdx][0] == x) and (jdx == 0):
        trasa = [[x, y]] + [[y, x]] + trasa
        return trasa
    if (trasa[jdx][0] == y) and (jdx == 0):
        trasa = [[y, x]] + [[x, y]] + trasa
        return trasa
    if (trasa[jdx][1] == x) and (jdx == 0):
        trasa = front_half1 + [[x, y]] + [[y, x]] + back_half1
        return trasa
    if (trasa[jdx][1] == y) and (jdx == 0):
        trasa = front_half1 + [[y, x]] + [[x, y]] + back_half1
        return trasa
    if (trasa[jdx][0] == x) and (jdx != 0):
        trasa = front_half0 + [[x, y]] + [[y, x]] + back_half0
        return trasa
    if (trasa[jdx][0] == y) and (jdx != 0):
        trasa = front_half0 + [[y, x]] + [[x, y]] + back_half0
        return trasa
    if (trasa[jdx][1] == x) and (jdx != 0):
        trasa = front_half1 + [[x, y]] + [[y, x]] + back_half1
        return trasa
    if (trasa[jdx][1] == y) and (jdx != 0):
        trasa = front_half1 + [[y, x]] + [[x, y]] + back_half1
        return trasa
    else:
        return [[1, 1]]


def print_time():
    print('Average time for 1 adjacency = ', np.mean(adj1_time) * 10 ** 3, 'ms')
    print('Average time for 2 adjacency = ', np.mean(adj2_time) * 10 ** 3, 'ms')
    print('Average time for 3 adjacency = ', np.mean(adj3_time) * 10 ** 3, 'ms')
    print('Average time for fix = ', np.mean(fix_time) * 10 ** 3, 'ms')


def average_time(workers: Worker.Workers):
    return np.mean(workers.cost)


def inequality(workers: Worker.Workers):
    return np.amax(workers.cost) - np.amin(workers.cost)

def mean_of_repeating_streets(workers: Worker.Workers):
    list_of_streets = []
    counter = np.zeros([workers.m])
    for i in range(workers.m):
        for x, y in workers.trasy[i]:
            # x,y = j
            if ([x, y] in list_of_streets) or ([y, x] in list_of_streets):
                counter[i] = counter[i] + 1
            else:
                list_of_streets.append([x, y])
    mean_of_repetition = counter.mean()
    return mean_of_repetition

def plot_path(workers):

    U = nx.DiGraph()
    colors = ['r','g','b']
    for i in range(len(workers.trasy)):
        for w in range(len(workers.trasy[i])):
            U.add_edge(workers.trasy[i][w][0], workers.trasy[i][w][1],color = colors[i])
    edges = U.edges()
    colors = [U[u][v]['color'] for u,v in edges]
    nx.draw(U, pos=nx.spring_layout(U),edges = edges, edge_color = colors, with_labels=True)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()