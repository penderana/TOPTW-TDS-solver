# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 19:24:38 2021

@author: carlo
"""

import random as r
import numpy as np
import matplotlib.pyplot as plt

f = open("c_r_rc_100_50/50_c103.txt")
datos = f.readlines()
f.close()




indices = [4,8,9]
contenido = []
profits = []
puntuaciones = []
intervalo = []
duraciones = []
duraciones_ = []

for i in range(2,53):
    if i < 12:
        contenido.append(datos[i].split(" ")[10:12])
        duraciones_.append(datos[i].split(" ")[5:6])
        profits.append(datos[i].split(" ")[6:7])
    else:
        contenido.append(datos[i].split(" ")[9:11])
        duraciones_.append(datos[i].split(" ")[4:5])
        profits.append(datos[i].split(" ")[5:6])
        


for i in range(0,51):
    puntuaciones.append(float(profits[i][0]))   
    duraciones.append(float(duraciones_[i][0]))
    if i > 0:
        intervalo.append([int(contenido[i][0]),int(contenido[i][1])])
    else:
        intervalo.append([0,int(contenido[i][0])])
        

diccionario_intervalos = {}
diccionario_duraciones = {}
diccionario_puntuaciones = {}

for i in range(0,51):
    diccionario_intervalos[i] = intervalo[i]
    diccionario_duraciones[i] = duraciones[i]
    diccionario_puntuaciones[i] = puntuaciones[i]
    
    
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

    solucion[0] = 0 #forzar que empiecen bien
    
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


def visualizar_proceso_solucion(array):
    numeros = []
    indices = comprobar(array)
    T = 0
    numeros.append(0)
    for i in range(0,len(array)):
        if indices[i]:
            T += diccionario_duraciones[array[i]]
        numeros.append(T)

            
    plt.plot(numeros)
    
def comprobar(array):
    indices = np.zeros(len(array))
    indices[0] = 1
    T = 16
    T_MAX = (diccionario_intervalos[0])[1]
    
    if array[0] == 0:
        for i in range(1,len(array)):
            elemento = array[i]
            if elemento != 0:
                coste = diccionario_duraciones[elemento]+T #falta incluir el coste de traspaso de nodo a nodo
                #if T >= (diccionario_intervalos[elemento])[0] and coste < (diccionario_intervalos[elemento])[1] and coste < T_MAX:
                if T >= (diccionario_intervalos[elemento])[0] and T < (diccionario_intervalos[elemento])[1] and coste < T_MAX:
                    T = coste
                    indices[i] = 1
            
    return indices

def fitness(array,T):
    valor = 0
    indices = comprobar(array)
    
    for i in range(0,len(array)):
        if indices[i]:
            valor += diccionario_puntuaciones[i] 

        

    return valor

#def fitness(array,iteracion):
#    valor = 0
#    
#    for i in range(0,len(array)):
#        valor += array[i] + get_factor(iteracion,array[i])
#
#    if valor == 0:
#        valor = -1
#        
#    return valor

#def fitness(array):
#    valor = 0
#    
#    for i in range(0,len(array)):
#        valor += array[i] 
#        
#    return valor


def vecindario(array):
    _,tam = contenido(array)
    if tam > 2:
        probabilidad = r.randint(1,3)
    else:
        probabilidad = 2
       
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
        
    nuevo_array[0] = 0 # forzamos a correcta solucion
    
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
    N = 300 #poblacion de 300
    M = 50 #numero de columnas
    T = 50
    mejor_fitness = -1
    mejores_resultados = []
    mejor_elemento = list(np.zeros(M))
    poblacion = []
    mejor_iteracion = -1
    
    for i in range(0,N):
        poblacion.append(generar_solucion_aleatoria(M))
        
    
    
    for i in range(0,1500):
        
# =============================================================================
#         ABEJAS EMPLEADAS
# =============================================================================
        for j in range(0,N):
            vecino = vecindario(poblacion[j])

            if fitness(poblacion[j],i) != 0:
                delta = (fitness(vecino,i) - fitness(poblacion[j],i) ) / fitness(poblacion[j],i)
            else:
                delta = 1
            
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
            
            if sumatorio != 0:
                probabilidad = fitness(poblacion[j],i) / sumatorio
            else:
                probabilidad = 0
            
            r = np.random.rand(1,1)
            
            if r < probabilidad:
                vecino = vecindario(poblacion[j])
                
                if fitness(poblacion[j],i) != 0:
                    delta = (fitness(vecino,i) - fitness(poblacion[j],i) ) / fitness(poblacion[j],i)
                else:
                    delta = 1
            
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
#             HBC
# =============================================================================
        poblacion = []     
        for j in range(0,N):
            poblacion.append(generar_solucion_aleatoria(M))
        for j in range(0,N):
            if fitness(poblacion[j],i) < mejor_fitness:
                poblacion[j] = mejor_elemento
                break
    
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
