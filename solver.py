# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 19:24:38 2021

@author: carlo
"""

import random as r
import numpy as np

def ordenar(array):
    nuevo_array = []
    
    for valor in array:
        if valor != 0:
            nuevo_array.append(valor)
            
    while len(nuevo_array) != len(array):
        nuevo_array.append(0)
        
    return nuevo_array

def contenido(array):
    interior = []
    
    for valor in contenido:
        if valor == 0:
            break
        else:
            interior.append(valor)
            
    return interior, len(interior)

def generar_solucion_aleatoria(n):
    solucion = []
    
    n_ceros = r.randint(0,n-1) #almenos una ciudad
    
    
    for i in range(0,n-n_ceros):
        aleatorio = r.randint(1,n)
        
        while aleatorio in solucion:
            aleatorio = r.randint(1,n)
            
        solucion.append(aleatorio)
        
    for j in range(0,n_ceros):
        solucion.append(0)

    
    return solucion


def fitness(array,factores):
    valor = 0
    
    for i in range(0,len(array)):
        valor += array[i] * factores[i]
        
    return valor

def mutar(array):
    probabilidad = r.randint(1,4)

    if probabilidad == 1 : #aniadimos un cero
        _, tam = contenido(array)
        indice = r.randint(0,tam-1)
        nuevo_array = np.copy(array)
        nuevo_array[indice] = 0
        nuevo_array = ordenar(nuevo_array)

    elif probabilidad == 2: #quitamos un cero
        dentro, m = contenido(array)
        nuevo_valor = r.choice(list(range(0,len(array)))-dentro)
        nuevo_array = np.copy(array)
        nuevo_array[m] = nuevo_valor
        
    elif probabilidad == 3: #cambiamos uno
        _,tam = contenido(array)
        
        
#print(generar_solucion_aleatoria(10))
    
print(fitness(generar_solucion_aleatoria(10),generar_solucion_aleatoria(10)))
