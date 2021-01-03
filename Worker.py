#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import Street
'''
klasa zawierajaca informacje o pracownikach:
-ich wydajnosc
-liste list z ich trasami?
'''

class Workers :
    def __init__(self):
        self.m = 20 # ilosc pracownikow

        self.w = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                  10, 10, 10, 10, 10, 10, 10, 10, 10, 20]

        self.trasy = [] # wektor zawierajacy kolejno ulice (para wierzcholkow) ktorymi przechodzi kazdy pracownik

        self.P = []  # wektor posprzatanych ulic

        self.cost = np.zeros(self.m)

    def route_lengths(self, L : np.array):
        route_lengths_list = []
        idx = 0
        for current_worker in self.trasy:
            route_lengths_list.append(0)
            for current_street in current_worker:
                route_lengths_list[idx] += L[tuple(current_street)]
            idx += 1
        return route_lengths_list

    def is_cleaned(self, street: tuple, helper_matrix: np.array,
                   G: np.array):  # funkcja sprawdzajaca czy ulica jest posprzatana
        starting_index, final_index = street
        reversed_street = final_index, starting_index  # ta sama ulica moze byc opisana z obu stron ( (3,1) = (1,3))
        if helper_matrix[street] == 0:  # sprawdzenie czy ktos przeszedl ta ulica, jesli tak to jest ona posprzatana
            helper_matrix[street] += 1  # ulica jest posprzatana
            helper_matrix[reversed_street] += 1  # zachowanie symetrycznosci
            return G[
                       street], helper_matrix  # zwraca koszt posprzatania ulicy zgodny z macierza G oraz zmieniana macierz helper_matrix
        else:
            return 0.5, helper_matrix  # zwraca koszt przejscia posprzatana ulica oraz niezmieniona macierz helper_matrix

    def calculate_cost(self, streets: Street.Streets):  # liczy koszt (funkcja celu)
        current_worker_id = 0
        self.cost = np.zeros(self.m)
        helper_matrix = np.zeros(
            streets.G.shape)  # macierz sprawdzajaca czy ulica jest posprzatana ( 0 - nie posprzatana, 1 - posprzatana)

        for current_worker in self.trasy:  # petla przechodzaca po kazdym pracowniku
            for street in current_worker:  # petla przechodzaca po kazdej ulicy (krotka z numerami wierzcholkow) danego pracownika
                g_value, helper_matrix = self.is_cleaned(tuple(street), helper_matrix, streets.G)
                self.cost[current_worker_id] += streets.L[tuple(street)] * g_value / self.w[
                    current_worker_id]  # zwiekszenie funkcji kosztu
            current_worker_id += 1  # id kolejnego pracownika

    def reset_P(self):
        self.P = []