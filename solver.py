# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 19:24:38 2021

@author: carlo
"""

import random as r
import numpy as np
import matplotlib.pyplot as plt

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
    
    for valor in array:
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


def get_factor(i,j):
    
    if i < 333:
        return 1
    elif i > 333 and i < 666:
        if j < 50:
            return 5
        else:
            return -10
    else:
        if j < 50:
            return -7
        else:
            return 15


def fitness(array,iteracion):
    valor = 0
    
    for i in range(0,len(array)):
        valor += array[i] + get_factor(iteracion,array[i])

    if valor == 0:
        valor = -1
        
    return valor

#def fitness(array):
#    valor = 0
#    
#    for i in range(0,len(array)):
#        valor += array[i] 
#        
#    return valor


def vecindario(array):
    if array[0] == 0:
        probabilidad = 2
    else:
       probabilidad = r.randint(1,4)
       
    nuevo_array = np.copy(array)
    
    if probabilidad == 1 : #aniadimos un cero
        _, tam = contenido(array)
        indice = r.randint(0,tam-1)
        nuevo_array = np.copy(array)
        nuevo_array[indice] = 0
        nuevo_array = ordenar(nuevo_array)

    elif probabilidad == 2: #quitamos un cero
        dentro, m = contenido(array)
        if m != len(array):
            numeros = set(range(0,len(array)))
            dentro = set(dentro)
            diferencia = numeros.difference(dentro)
            nuevo_valor = r.choice(list(diferencia))
            nuevo_array = np.copy(array)
            nuevo_array[m] = nuevo_valor
        
    elif probabilidad == 3: #cambiamos uno
        _,tam = contenido(array)
        indice1 = r.randint(0,tam-1)
        indice2 = r.randint(0,tam-1)
        nuevo_array = np.copy(array)
        nuevo_array[indice1] = array[indice2]
        nuevo_array[indice2] = array[indice1]
        
    return list(nuevo_array)
        
    
def cruce(padre,madre):
    N = len(padre)
    solucion = np.zeros(N)
    dentro, m_padre = contenido(padre)
    dentro, m_madre = contenido(madre)
    
    if m_padre < m_madre:
        solucion[:m_padre] = madre[:m_padre]
    else:
        solucion[:m_madre] = padre[:m_madre]
    
    return solucion



def generacional():
    N = 300 #poblacion de 30
    M = 100 #numero de columnas
    T = 50
    mejor_fitness = 0
    mejores_resultados = []
    
    poblacion = []
    for i in range(0,N):
        poblacion.append(generar_solucion_aleatoria(M))
        
    
    
    for i in range(0,1000):
        
# =============================================================================
#         ABEJAS EMPLEADAS
# =============================================================================
        for j in range(0,N):
            vecino = vecindario(poblacion[j])

            delta = (fitness(vecino,i) - fitness(poblacion[j],i) ) / fitness(poblacion[j],i)
            
            if delta >= 0:
                poblacion[j] = vecino
            else:
                r = np.random.rand(1,1)
                if r < np.exp(delta/T):
                    poblacion[j] = vecino
                    
# =============================================================================
#         ABEJAS EXPLORADORAS
# =============================================================================
        for j in range(0,N):     
            
            sumatorio = 0
            for k in range(0,N):
                sumatorio += fitness(poblacion[k],i)
            
            probabilidad = fitness(poblacion[j],i) / sumatorio
            
            r = np.random.rand(1,1)
            
            if r < probabilidad:
                vecino = vecindario(poblacion[j])
                
                delta = (fitness(vecino,i) - fitness(poblacion[j],i) ) / fitness(poblacion[j],i)
            
                if delta >= 0:
                    poblacion[j] = vecino
                else:
                    r = np.random.rand(1,1)
                    if r < np.exp(delta/T):
                        poblacion[j] = vecino
                        
# =============================================================================
#             MEJOR SOLUCION LOCAL
# =============================================================================
        current = 0
        for j in range(0,N):
            if fitness(poblacion[j],i) > current:
                current = fitness(poblacion[j],i)
        mejores_resultados.append(current)
                        
# =============================================================================
#           MEJOR SOLUCION
# =============================================================================
        for j in range(0,N):
            if fitness(poblacion[j],i) > mejor_fitness:
                mejor_fitness = fitness(poblacion[j],i)
                mejor_elemento = poblacion[j]
                mejor_iteracion = i                      
    
# =============================================================================
#         ENFRIAMIENTO
# =============================================================================
        if i % 10 == 0:
            T *= 0.98              
        
                    
                
    
    return mejor_elemento, mejor_iteracion, mejor_fitness, mejores_resultados
        


elemento, iteracion, valor, lista = generacional()
print(elemento, iteracion, valor)
plt.plot(lista)
plt.show()
