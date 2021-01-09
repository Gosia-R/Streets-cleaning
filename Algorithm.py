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


def SA(imported: bool, save: bool, folder_path: str = None):
    # ___________ save trasy __________
    trasy_list = []
    # ___________ metrics _______________
    avg_time = []
    difference = []
    avg_work_time = []
    how_much_better = []
    total_how_much_better = []
    avg_revisited = []
    when_minimum_list = []
    # _________ plots __________
    all_costs = []
    all_rejected = []
    all_deltas = []
    all_delta_rejected = []
    all_delta_accepted = []

    original_street = Street.Streets()

    for batch in range(5):
        print('Current batch = ', batch+1)
        tic = time.clock()
        # ________parametry algorytmu____________
        temperature = 3000
        alfa = 0.99
        beta = 1

        workers = Worker.Workers()
        streets = Street.Streets()
        if imported:
            streets.load_matrices(folder_path)
            streets.n = len(streets.A)
            streets.fw_graph = streets.Floyd_Warshall()
            streets.update_r()
        else:
            streets = deepcopy(original_street)
        if streets.n <= 16:
            workers.w = [5, 7]

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

            if delta >= 0:
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
            #print('iteracja = ', iteration, 'koszt = ', current_cost)
            iteration += 1
            temperature *= alfa


        toc = time.clock()
        last_cost = max(workers.cost)
        last_sum_cost = sum(workers.cost)


        # _______ plot tray _______
        if len(workers.trasy) < 3:
            Functions.plot_path(workers)

        # ________ append save trasy ____________
        if save:
            trasy_list.append(workers.trasy)

        # _______ append metrics _____________
        avg_time.append(toc-tic)
        avg_revisited.append(Functions.mean_of_repeating_streets(workers))
        avg_work_time.append(Functions.average_time(workers))
        how_much_better.append((first_cost - last_cost)/first_cost * 100)
        total_how_much_better.append((first_sum_cost - last_sum_cost)/first_sum_cost * 100)
        difference.append(Functions.inequality(workers))
        when_minimum_list.append(when_minimum)

        # _______ append plots _______________
        all_costs.append(cost_list)
        all_delta_accepted.append(delta_accepted_list)
        all_delta_rejected.append(delta_rejected_list)
        all_deltas.append(delta_list)
        all_rejected.append(rejected_list)


        # ________________printy______________
        '''
        print('Czas trwania algorytmu to: ', toc - tic, 's')
        Functions.print_time()
        print("Funkcja celu zmalała o ", last_cost/first_cost * 100, '%')
        print("Całkowity czas zmalał o ", last_sum_cost/first_sum_cost * 100, '%')
        print('Ilość ulic w miescie = ', streets.r)
        print("Średnio ulice powtarzają się", Functions.mean_of_repeating_streets(workers)) # to powinno byc w klasie worker
        print('Average work time = ', Functions.average_time(workers)) # to powinno byc w klasie worker
        print('Difference between longest and shortest work time', Functions.inequality(workers)) # to pownno byc w klasie worker
        print("Minimum osiągnięto w iteracji:", when_minimum)
    '''

    if save:
        df = pd.DataFrame(data={'Średni czas trwania algorytmu': avg_time, 'Średni czas pracy dla pracownika': avg_work_time, 'Średnia ilość ponownie odwiedzonych ulic': avg_revisited, 'Różnica między najdłużej a najkrócej pracującym pracownikiem': difference, 'Poprawa w %': how_much_better, 'Lączna poprawa w %': total_how_much_better, 'Kiedy minimum': when_minimum_list})
        writer = pd.ExcelWriter('metrics.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='data', index=False)
        writer.save()
        best_idx = how_much_better.index(np.max(how_much_better))
        df2 = pd.DataFrame(data=trasy_list[best_idx])
        writer = pd.ExcelWriter('trasy.xlsx', engine='xlsxwriter')
        df2.to_excel(writer, sheet_name='data', index=False)
        writer.save()


    # ________________ploty_________________________

    best_idx = how_much_better.index(np.max(how_much_better))
    worst_idx = how_much_better.index(np.min(how_much_better))
    mean_cost = np.mean(all_costs, axis=0)
    max_cost = all_costs[best_idx]
    min_cost = all_costs[worst_idx]

    plt.plot(mean_cost)
    plt.plot(max_cost)
    plt.plot(min_cost)
    plt.legend(('mean','best','worst'))
    plt.title('Cost function')
    plt.ylabel('time [minutes]')
    plt.xlabel('number of iterations')
    plt.show()

    plt.plot(all_rejected[best_idx], 'ro')
    plt.title('Rejected solutions')
    plt.xlabel('Rejected solution')
    plt.ylabel('Number of iteration')
    plt.show()

    plt.plot(all_deltas[best_idx])
    plt.title('Delta')
    plt.xlabel('Number of iteration')
    plt.ylabel('Value of delta')
    plt.show()

    ax = plt.subplot(211)
    ax.plot(all_delta_accepted[best_idx], 'o')
    ax.set_title('accepted')
    ax2 = plt.subplot(212)
    ax2.plot(all_delta_rejected[best_idx], 'o')
    ax2.set_title('rejected')
    plt.show()