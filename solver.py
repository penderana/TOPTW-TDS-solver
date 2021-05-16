# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 19:24:38 2021

@author: carlo
"""

import random as r
import numpy as np
import matplotlib.pyplot as plt

f = open("c_r_rc_100_50/50_c103_processed.txt")
datos = f.readlines()
f.close()

diccionario_intervalos = {}
diccionario_duraciones = {}
diccionario_puntuaciones = {}
diccionario_distancias =  {}
diccionario_factores = {}

for i in range(0,51):
    separado = datos[i].split(" ")
    diccionario_distancias[i] = separado[0:51]
    diccionario_duraciones[i] = separado[51:52]
    diccionario_puntuaciones[i] = separado[52:53]
    diccionario_intervalos[i] = separado[53:55]
    diccionario_factores[i] = separado[55:59]
    
    
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
    
def arreglar(array):
    #QUITAMOS NODOS QUE NO SE PUEDAN VISITAR PORQUE VIOLEN RESTRICCIONES
    bueno = np.zeros(len(array))
    T_MAX = float((diccionario_intervalos[0])[1])
    T = 0
    contador = 1
    
    for i in range(1,len(array)):
        elemento = array[i]
        
        #la restriccion es que no sobrepasemos el tiempo entre ir al siguiente nodo y lo que dure su estancia
        coste_ir = float(diccionario_distancias[elemento][int(array[i-1])]) + float(diccionario_duraciones[elemento][0])
        
        if coste_ir + T <= T_MAX:
            bueno[contador] = elemento
            contador += 1
            T += coste_ir
        
    return bueno

#def comprobar(array):
#    indices = np.zeros(len(array))
#    indices[0] = 1
#    T = 0
#    T_MAX = (diccionario_intervalos[0])[1]
#    
#    if array[0] == 0:
#        for i in range(1,len(array)):
#            elemento = array[i]
#            if elemento != 0:
#                coste = diccionario_duraciones[elemento]+T #falta incluir el coste de traspaso de nodo a nodo
#                #if T >= (diccionario_intervalos[elemento])[0] and coste < (diccionario_intervalos[elemento])[1] and coste < T_MAX:
#                if T >= (diccionario_intervalos[elemento])[0] and T < (diccionario_intervalos[elemento])[1] and coste < T_MAX:
#                    T = coste
#                    indices[i] = 1
#            
#    return indices

def fitness(array,T):
    valor = 0
    
    for i in range(0,len(array)):
        if i == 0 or array[i] != 0:
            valor += float(diccionario_puntuaciones[int(array[i])][0]) * float(diccionario_factores[int(array[i])][T])

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
    if tam > 1:
        probabilidad = r.randint(1,4)
    else:
        probabilidad = 2
       
    nuevo_array = np.copy(array)
    
    if probabilidad == 1 : # invertirmos un subsitring
        _, tam = contenido(array)
        indice1 = r.randint(0,tam-1)
        indice2 = r.randint(0,tam-1)
        
        if indice1 > indice2:
            nuevo_array[indice2:indice1] = array[indice2:indice1:-1]
        else:
            nuevo_array[indice1:indice2] = array[indice1:indice2:-1]


    elif probabilidad == 2: #quitamos un cero
        dentro, m = contenido(array)
        if m <= 1:
            indice = 1
        else:
            indice = r.randint(1,m-1)
        if m < len(array):
            numeros = set(range(0,len(array)))
            dentro = set(dentro)
            diferencia = numeros.difference(dentro)
            nuevo_valor = r.choice(list(diferencia))
            nuevo_array = np.copy(array)
            nuevo_array[indice] = nuevo_valor
            
        
    elif probabilidad == 3: #swap de posiciones
        _,tam = contenido(array)
        indice1 = r.randint(0,tam-1)
        indice2 = r.randint(0,tam-1)
        nuevo_array = np.copy(array)
        nuevo_array[indice1] = array[indice2]
        nuevo_array[indice2] = array[indice1]
        
    elif probabilidad == 4: #swap de posicion con posicion anterior
        _,tam = contenido(array)
        indice1 = r.randint(1,tam-1)
        indice2 = r.randint(1,tam-1)
        valor = nuevo_array.pop(indice1)
        nuevo_array.insert(indice2,valor)

        
    nuevo_array[0] = 0 # forzamos a correcta solucion
    
    return arreglar(list(nuevo_array)) #Trabajamos siempre con soluciones factibles
        
    
#def cruce(padre,madre):
#    N = len(padre)
#    solucion = np.zeros(N)
#    dentro, m_padre = contenido(padre)
#    dentro, m_madre = contenido(madre)
#    
#    if m_padre < m_madre:
#        solucion[:m_padre] = madre[:m_padre]
#    else:
#        solucion[:m_madre] = padre[:m_madre]
#    
#    return solucion

def ensenar_ruta(ruta):
    elementos = comprobar(ruta)
    lista = []
    contador = 0
    
    for i in range(0,len(ruta)):
        if elementos[i]:
            contador += 1
            lista.append(dicionario_coordenadas[ruta[i]][0])
            lista.append(dicionario_coordenadas[ruta[i]][1])
            if i+1 < len(ruta) - 1:
                for j in range(i+1,len(ruta)):
                    if elementos[j]:
                        break
            else:
                j = 0
            lista.append(dicionario_coordenadas[ruta[j]][0] - dicionario_coordenadas[ruta[i]][0])
            lista.append(dicionario_coordenadas[ruta[j]][1] - dicionario_coordenadas[ruta[i]][1])
            
    lista = np.reshape(lista,(contador,4))
    lista = np.array(lista,np.float64)
        
    plt.scatter(lista[:,0],lista[:,1],s=20*2**3)
    plt.quiver(lista[:,0],lista[:,1], lista[:,2], lista[:,3], angles='xy', scale=1, scale_units='xy')
    
    plt.xlim(5,50)
    plt.ylim(20,100)
    plt.show()
    
    return lista
        

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
        poblacion.append(arreglar(generar_solucion_aleatoria(M)))
        
    

    for i in range(0,700):
        
        horario = i % 100
        
        if horario < 25:
            epoca = 0
        elif horario >= 25 and horario < 50:
            epoca = 1
        elif horario >= 50 and horario < 75:
            epoca = 2
        elif horario >= 75:
            epoca = 3
  
# =============================================================================
#         ABEJAS EMPLEADAS
# =============================================================================
        for j in range(0,N):
            vecino = vecindario(poblacion[j])

            if fitness(poblacion[j],epoca) != 0:
                delta = (fitness(vecino,epoca) - fitness(poblacion[j],epoca) ) / fitness(poblacion[j],epoca)
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
                sumatorio += fitness(poblacion[k],epoca)
            
            if sumatorio != 0:
                probabilidad = fitness(poblacion[j],epoca) / sumatorio
            else:
                probabilidad = 0
            
            r = np.random.rand(1,1)
            
            if r < probabilidad:
                vecino = vecindario(poblacion[j])
                
                if fitness(poblacion[j],epoca) != 0:
                    delta = (fitness(vecino,epoca) - fitness(poblacion[j],epoca) ) / fitness(poblacion[j],epoca)
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
            if fitness(poblacion[j],epoca) > current:
                current = fitness(poblacion[j],epoca)
        mejores_resultados.append(current)
                        
# =============================================================================
#           MEJOR SOLUCION
# =============================================================================
        for j in range(0,N):
            if fitness(poblacion[j],epoca) > mejor_fitness:
                mejor_fitness = fitness(poblacion[j],epoca)
                mejor_elemento = poblacion[j]
                mejor_iteracion = i       
                
            
# =============================================================================
#             HBC
# =============================================================================
#        poblacion = []     
#        for j in range(0,N):
#            poblacion.append(generar_solucion_aleatoria(M))
#        for j in range(0,N):
#            if fitness(poblacion[j]) < mejor_fitness:
#                poblacion[j] = mejor_elemento
#                break
    
# =============================================================================
#         ENFRIAMIENTO
# =============================================================================
        if i % 10 == 0:
            T *= 0.98              
        
                    
                
    
    return mejor_elemento, mejor_iteracion, mejor_fitness, mejores_resultados
        


#elemento, iteracion, valor, lista = generacional()
#print(elemento, iteracion, valor)
#plt.plot(lista)
#plt.show()
#
#lista = ensenar_ruta(elemento)
#print(lista)
    
suma1 = 0
suma2 = 0
suma3 = 0
suma4 = 0

for i in range(0,51):
    suma1 += float(diccionario_factores[i][0])
    suma2 += float(diccionario_factores[i][1]) 
    suma3 += float(diccionario_factores[i][2]) 
    suma4 += float(diccionario_factores[i][3]) 
    
print("Media factores etapa 1:",suma1/51)
print("Media factores etapa 2:",suma2/51)
print("Media factores etapa 3:",suma3/51)
print("Media factores etapa 4:",suma4/51)
