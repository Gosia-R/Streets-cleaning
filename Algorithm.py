#!/usr/bin/python
# -*- coding: utf-8 -*-
import Street
import Worker
import Functions
import random
import numpy as np

'''
sama algorytm, wszystkie funkcje w osobnym pliku
'''

temperature = 1000
alfa = 0.99
workers = Worker.Workers()
streets = Street.Streets()

Functions.initialize(workers, streets)
current_cost = Functions.calculate_cost(workers, streets)
cost_list = [current_cost]

while temperature > 1:
    new_workers = workers
    Functions.adjacent_solution(new_workers, streets)

    new_cost = Functions.calculate_cost(new_workers, streets)
    cost_list.append(new_cost)
    delta = current_cost - new_cost

    if delta > 0:
        workers = new_workers
    else:
        beta = 100
        if random.random() < np.exp(-(beta * delta) / temperature):
            workers = new_workers
        else:
            pass

    temperature *= alfa

