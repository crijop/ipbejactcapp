#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
autor: José Jasnau Caeiro
data: 7 de junho de 2012
obs:
   permite carregar os docentes para a base de dados
'''

import csv


def leitura_docentes_csv():
    '''
    leitura dos docentes do ficheiro csv
    '''
    nome_ficheiro = "DSD1213Proposta360Dep30Mai12.csv"
    ficheiro = open(nome_ficheiro, 'rb')
    leitor = csv.reader(ficheiro,delimiter=',')
    for linha in leitor:
        if linha[2]:
            print linha[2]
        pass
    ficheiro.close()
    pass

leitura_docentes_csv()
