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
list_of_streets = []
counter = np.zeros([workers.m])
for i in range(workers.m):
    for x,y in workers.trasy[i]:
        #x,y = j
        if ([x,y] in list_of_streets) or ([y,x] in list_of_streets):
            counter[i] = counter[i] + 1
        else:
            list_of_streets.append([x,y])
mean_of_repetition = counter.mean()

last_cost = max(workers.cost)
last_sum_cost = sum(workers.cost)

print("Funkcja celu zmalała o ", last_cost/first_cost * 100, '%')
print("Całkowity czas zmalał o ", last_sum_cost/first_sum_cost * 100, '%')
print("Średnio ulice powtarzają się", mean_of_repetition)
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
