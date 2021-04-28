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
    
    if i < 500:
        return j
    elif i > 500 and i < 100:
        if j < 50:
            return 50
        else:
            return -100
    else:
        if j < 50:
            return -75
        else:
            return 150


def fitness(array,iteracion):
    valor = 0
    
    for i in range(0,len(array)):
        valor += array[i] * get_factor(iteracion,array[i])
        
    return valor

#def fitness(array):
#    valor = 0
#    
#    for i in range(0,len(array)):
#        valor += array[i] 
#        
#    return valor


def mutar(array):
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
    Pm = 0.3
    
    poblacion = []
    for i in range(0,N):
        poblacion.append(generar_solucion_aleatoria(M))
        
    
    print(len(poblacion))
    for i in range(0,1500):

# =============================================================================
#         PARTE 0: GUARDAMOS EL MEJOR INDIVIDUO POR SI LO PERDEMOS
# =============================================================================

#        mex = 0
#        
#        for k in range(1,N):
##            print(poblacion[k].calificacion)
#            if fitness(poblacion[k]) > fitness(poblacion[mex]):
#                mex = k
#                
#        mejor_individuo = poblacion[mex]
      
        
        
# =============================================================================
#         PARTE 1: TORNEO BINARIO. ELEGIMOS DOS CROMOSOMAS AL AZAR Y
#         LO ANIADIMOS A LA NUEVA POBLACION.
# =============================================================================
        
        poblacion_prima = []
#        aleatorios = r.sample(range(N),k=N)
        
        for j in range(0,N): 
            w1 = r.randrange(N)
            w2 = r.randrange(N)
#            w1 = aleatorios[j]
#            w2 = aleatorios[N-j-1] 

            if fitness(poblacion[w1],i) > fitness(poblacion[w2],i):
                poblacion_prima.append(poblacion[w1])
            else:
#                poblacion_prima.append(cromosoma(M,iteracion,poblacion[w2].w))
                poblacion_prima.append(poblacion[w2])


                
    
# =============================================================================
#         PARTE 3: MUTACIONES. HACEMOS LO MISMO QUE ANTES: CALCULAMOS LA ESPERANZA
#         DEL NUMERO DE MUTACIONES QUE HABRÁ. GENERAMOS UN NUMERO ALEATORIO Y SELECCIONAMOS
#         ALEATORIAMENTE LA FILA Y LA COLUMNA A MUTAR.
#         
#         ESPERANZA MATEMATICA:
#         NUMERO ESPERADO DE MUTACIONES: Pm * N * M
# =============================================================================
        
        mutaciones = (int)(N * Pm)

        
        for j in range(0,mutaciones):

            poblacion_prima[j] = mutar(poblacion_prima[j])
            
# =============================================================================
#     FINAL: BUSCAMOS EL MEJOR CROMOSOMA DE LA POBLACION FINAL
#     PARA DEVOLVERLO, Y EVALUARLO DESPUES CON EL TEST.
# =============================================================================
    mex = 0
        
    for k in range(1,N):
        if fitness(poblacion[k],i) > fitness(poblacion[mex],i):
            mex = k
                
    mejor_individuo = poblacion[mex]
    
    return mejor_individuo, fitness(mejor_individuo,i)
        

    
        
print(generacional())
