#!/usr/bin/python
# -*- coding: utf-8 -*-

import Street
import Worker
import Functions
import random
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import time
import pandas as pd
import networkx as nx

# ___________ metrics _______________
avg_time = []
difference = []
avg_work_time = []
how_much_better = []
total_how_much_better = []
avg_revisited = []

# _________ plots __________
all_costs = []
all_rejected = []
all_deltas = []
all_delta_rejected = []
all_delta_accepted = []

for batch in range(10):
    print(' \n\n\nCURRENT BATCH ', batch)
    tic = time.clock()
    # ________parametry algorytmu____________
    temperature = 3000
    alfa = 0.99
    beta = 10

    workers = Worker.Workers()
    streets = Street.Streets()
    streets.load_matrices(r'przypadki_testowe/duzy/')
    streets.fw_graph = streets.Floyd_Warshall()
    streets.update_r()
    Functions.initialize(workers, streets)

    workers.calculate_cost(streets)
    current_cost = max(workers.cost)
    first_cost = max(workers.cost)
    first_sum_cost = sum(workers.cost)
    cost_list = [current_cost]
    delta_list = []
    iteration = 0
    when_minimum = 0
    rejected_list = []
    temp_list = []
    delta_accepted_list = []
    delta_rejected_list = []

    while temperature > 1:
        new_workers = deepcopy(workers)
        Functions.adjacent_solution(new_workers, streets)
        new_workers.calculate_cost(streets)
        new_cost = max(new_workers.cost)

        if new_cost + 1 < current_cost:
            when_minimum = iteration

        delta = current_cost - new_cost
        delta_list.append(delta)
        temp_list.append(temperature)

        if delta > 0:
            workers = deepcopy(new_workers)
            current_cost = deepcopy(new_cost)
        else:
            if random.random() < np.exp((beta * delta) / temperature):
                workers = deepcopy(new_workers)
                current_cost = deepcopy(new_cost)
                delta_accepted_list.append(delta)
            else:
                rejected_list.append(iteration)
                delta_rejected_list.append(delta)
                pass

        cost_list.append(current_cost)
        print('iteracja = ', iteration, 'koszt = ', current_cost)
        iteration += 1
        temperature *= alfa


    toc = time.clock()
    last_cost = max(workers.cost)
    last_sum_cost = sum(workers.cost)

    # _______ append metrics _____________
    avg_time.append(toc-tic)
    avg_revisited.append(Functions.mean_of_repeating_streets(workers))
    avg_work_time.append(Functions.average_time(workers))
    how_much_better.append((first_cost - last_cost)/first_cost * 100)
    total_how_much_better.append((first_sum_cost - last_sum_cost)/first_sum_cost * 100)
    difference.append(Functions.inequality(workers))

    # _______ append plots _______________
    all_costs.append(cost_list)
    all_delta_accepted.append(delta_accepted_list)
    all_delta_rejected.append(delta_rejected_list)
    all_deltas.append(delta_list)
    all_rejected.append(rejected_list)


    # ________________printy______________
    print('Czas trwania algorytmu to: ', toc - tic, 's')
    '''
    Functions.print_time()
    print("Funkcja celu zmalała o ", last_cost/first_cost * 100, '%')
    print("Całkowity czas zmalał o ", last_sum_cost/first_sum_cost * 100, '%')
    print('Ilość ulic w miescie = ', streets.r)
    print("Średnio ulice powtarzają się", Functions.mean_of_repeating_streets(workers)) # to powinno byc w klasie worker
    print('Average work time = ', Functions.average_time(workers)) # to powinno byc w klasie worker
    print('Difference between longest and shortest work time', Functions.inequality(workers)) # to pownno byc w klasie worker
    print("Minimum osiągnięto w iteracji:", when_minimum)
'''
'''
    # ________________ploty_________________________

    plt.plot(rejected_list, 'ro')
    plt.show()

    plt.plot(cost_list)
    plt.ylabel('time [minutes]')
    plt.xlabel('number of iterations')
    plt.show()

    plt.plot(delta_list)
    plt.title('Delta')
    plt.show()

    ax = plt.subplot(211)
    ax.plot(delta_accepted_list, 'o')
    ax.set_title('accepted')
    ax2 = plt.subplot(212)
    ax2.plot(delta_rejected_list, 'o')
    ax2.set_title('rejected')
    plt.show()
'''
'''
metrics = [avg_time, avg_work_time, avg_revisited, difference, how_much_better, total_how_much_better]
df = pd.DataFrame(data={'avg_time': avg_time, 'avg_work_time': avg_work_time, 'avg_revisited': avg_revisited, 'diffy': difference, 'how_much_better': how_much_better, 'total_better': total_how_much_better})
writer = pd.ExcelWriter('metrics.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='data', index=False)
writer.save()
'''

mean_cost = np.mean(all_costs, axis=0)

# NIE TAK DOBIERAĆ NAJLEPSZEI NAJGORSZE ROZWIAZANIE
max_cost = np.max(all_costs, axis=0)
min_cost = np.min(all_costs, axis=0)

plt.plot(mean_cost)
plt.plot(max_cost)
plt.plot(min_cost)
plt.legend(('mean','best','worst'))
plt.ylabel('time [minutes]')
plt.xlabel('number of iterations')
plt.show()



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

