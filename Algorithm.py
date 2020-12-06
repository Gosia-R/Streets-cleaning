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

temperature = 30000
alfa = 0.99
workers = Worker.Workers()
streets = Street.Streets()

Functions.initialize(workers, streets)
current_cost = Functions.calculate_cost(workers, streets)
cost_list = [current_cost]
delta_list = []
iteration = 0
exp_list = []

while temperature > 1:
    new_workers = deepcopy(workers)
    Functions.adjacent_solution(new_workers, streets)

    new_cost = Functions.calculate_cost(new_workers, streets)
    cost_list.append(new_cost)
    delta = current_cost - new_cost
    delta_list.append(delta)
    if delta > 0:
        workers = new_workers
        current_cost = new_cost
    else:
        beta = 1
        exp_list.append(np.exp(-(beta * delta) / temperature))
        if random.random() < np.exp(-(beta * delta) / temperature):
            workers = new_workers
            current_cost = new_cost
        else:
            pass

    print('iteracja = ', iteration, 'koszt = ', current_cost)
    iteration += 1
    temperature *= alfa

plt.plot(cost_list)
plt.ylabel('time [mimutes]')
plt.xlabel('number of iterations')
plt.show()

plt.plot(delta_list)
plt.title('Delta')
plt.show()

plt.plot(exp_list)
plt.title('exp')
plt.show()