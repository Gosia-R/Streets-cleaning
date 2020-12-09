#!/usr/bin/python
# -*- coding: utf-8 -*-
import Street
import Worker
import Functions
import random
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

'''
sama algorytm, wszystkie funkcje w osobnym pliku
'''

temperature = 3000
alfa = 0.99
workers = Worker.Workers()
streets = Street.Streets()

Functions.initialize(workers, streets)
current_cost = Functions.calculate_cost(workers, streets)
cost_list = [current_cost]
delta_list = []
iteration = 0
idx = 0
iter_list = []
temp_list = []
delta_accepted_list = []
delta_rejected_list = []
print('Zainicjowana dlugosc P = ', len(workers.P))
while temperature > 1:
    new_workers = deepcopy(workers)
    Functions.adjacent_solution(new_workers, streets)

    new_cost = Functions.calculate_cost(new_workers, streets)
    delta = current_cost - new_cost
    delta_list.append(delta)
    temp_list.append(temperature)
    if delta >= 0:
        workers = deepcopy(new_workers)
        current_cost = deepcopy(new_cost)
    else:
        beta = 30
        if random.random() < np.exp((beta * delta) / temperature):
            workers = deepcopy(new_workers)
            current_cost = deepcopy(new_cost)
            delta_accepted_list.append(delta)
        else:
            idx += 1
            #print('nie zaakceptowano po raz : ', idx, ' w iteracji nr :', iteration)
            iter_list.append(iteration)
            delta_rejected_list.append(delta)
            pass

    #print('iteracja = ', iteration, 'dlugosc P workera = ', len(workers.P), 'dlugosc P new_workera = ', len(new_workers.P))
    cost_list.append(current_cost)
    #print('iteracja = ', iteration, 'koszt = ', current_cost)
    iteration += 1
    temperature *= alfa


plt.plot(iter_list, 'ro')
plt.show()


plt.plot(cost_list)
plt.ylabel('time [mimutes]')
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
