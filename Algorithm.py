#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import time
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

import Functions
import Street
import Worker

'''
sama algorytm, wszystkie funkcje w osobnym pliku
'''
tic = time.clock()
temperature = 10000
alfa = 0.99
workers = Worker.Workers()
streets = Street.Streets()

Functions.initialize(workers, streets)
workers.calculate_cost(streets)
current_cost = max(workers.cost)
first_cost = max(workers.cost)
first_sum_cost = sum(workers.cost)
cost_list = [current_cost]
delta_list = []
iteration = 0
when_minimum = 0
idx = 0
iter_list = []
temp_list = []
delta_accepted_list = []
delta_rejected_list = []
print('Zainicjowana dlugosc P = ', len(workers.P))
P_first = deepcopy(workers.P)
while temperature > 1:
    new_workers = deepcopy(workers)
    Functions.adjacent_solution(new_workers, streets)
    new_workers.calculate_cost(streets)
    new_cost = max(new_workers.cost)
    if new_cost +1 <current_cost:
        when_minimum = iteration
    delta = current_cost - new_cost
    delta_list.append(delta)
    temp_list.append(temperature)
    if delta > 0:
        workers = deepcopy(new_workers)
        current_cost = deepcopy(new_cost)
    else:
        beta = 10
        if random.random() < np.exp((beta * delta) / temperature):
            workers = deepcopy(new_workers)
            current_cost = deepcopy(new_cost)
            delta_accepted_list.append(delta)
        else:
            idx += 1
            # print('nie zaakceptowano po raz : ', idx, ' w iteracji nr :', iteration)
            iter_list.append(iteration)
            delta_rejected_list.append(delta)
            pass

    # print('iteracja = ', iteration, 'dlugosc P workera = ', len(workers.P), 'dlugosc P new_workera = ', len(new_workers.P))
    cost_list.append(current_cost)
    # print('iteracja = ', iteration, 'koszt = ', current_cost)
    iteration += 1
    temperature *= alfa
toc = time.clock()

Functions.print_time()
last_cost = max(workers.cost)
last_sum_cost = sum(workers.cost)

print("Funkcja celu zmalała o ",  (first_cost - last_cost)/first_cost * 100, '%')
print("Całkowity czas zmalał o ", (first_sum_cost - last_sum_cost)/first_sum_cost * 100, '%')
x = Functions.mean_of_repeating_streets(workers)
print("Średnio ulice powtarzają się", Functions.mean_of_repeating_streets(workers))
print("Minimum osiągnięto w iteracji:", when_minimum)

# ________________wykresiki_________________________
print('Czas trwania algorytmu to: ', toc - tic, 's')
plt.plot(iter_list, 'ro')
plt.show()

plt.plot(cost_list)
plt.ylabel('time [minutes]')
plt.xlabel('number of iterations')
plt.show()

plt.plot(delta_list)
plt.title('Delta')
plt.show()

plt.plot(temp_list)
plt.title('temperatura')
plt.show()

ax = plt.subplot(211)
ax.plot(delta_accepted_list, 'o')
ax.set_title('accepted')

ax2 = plt.subplot(212)
ax2.plot(delta_rejected_list, 'o')
ax2.set_title('rejected')
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

