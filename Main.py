#!/usr/bin/python
# -*- coding: utf-8 -*-
import Algorithm

print('Witamy w programie rozdzielającym trasy pracownikom sprzątającym ulic')
inpt = input('Czy chcesz wczytac wlasne dane? [t/n] ')

if inpt == 't':
    folder_path = input('Podaj scieżkę do folderu z planami miasta, np. przypadki_testowe/normalny/ \n')
    save = input('Czy chcesz zapisać otrzymane ścieżki oraz metryki? [t/n] ')
    if save == 't':
        save = True
    else:
        save = False
    Algorithm.SA(imported=True, folder_path=folder_path, save=save)
elif inpt == 'n':
    save = input('Czy chcesz zapisać otrzymane ścieżki oraz metryki? [t/n] ')
    if save == 't':
        save = True
    else:
        save = False
    Algorithm.SA(imported=False, folder_path='place_holder', save=save)
else:
    print('blad')
