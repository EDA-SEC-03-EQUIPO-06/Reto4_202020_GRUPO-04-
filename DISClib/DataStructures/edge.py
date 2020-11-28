"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribución de:
 * Darío Correal
 """

import config
assert config
from DISClib.ADT import map as map 

"""
Este código está basado en las implementaciones propuestas en:
- Algorithms, 4th Edition.  R. Sedgewick
- Data Structures and Algorithms in Java, 6th Edition.  Michael Goodrich
"""


def newEdge(va, vb, weight=0):
    """
    Crea un nuevo arco entrelos vertices va y vb
    """
    edge = {'vertexA': va,
            'vertexB': vb,
            'weight': weight,
            'usertype':{"0-10": {'Subscriber': 0, 'Customer':0}, "11-20": {'Subscriber': 0, 'Customer':0}, 
            "21-30": {'Subscriber': 0, 'Customer':0}, "31-40": {'Subscriber': 0, 'Customer':0}, 
            "41-50": {'Subscriber': 0, 'Customer':0}, "51-60": {'Subscriber': 0, 'Customer':0},
            "60+": {'Subscriber': 0, 'Customer':0}},
            'count': 1,
            'sum': weight,
            }
    return edge

def weight(edge):
    """
    Retorna el peso de un arco
    """
    return edge['weight']

def usertype(edge): 
    """
    Retorna un dic con los tipos de usuario y su cantidad
    """
    return edge['usertype']
    
def getTotaltrips(edge):
    """
    Retorna la cantidad de viajes por estación
    """
    trips = 0
    trips += edge['usertype']["0-10"]["Subscriber"]
    trips += edge['usertype']["0-10"]["Customer"]
    trips += edge['usertype']["11-20"]["Subscriber"]
    trips += edge['usertype']["11-20"]["Customer"]
    trips += edge['usertype']["21-30"]["Subscriber"]
    trips += edge['usertype']["21-30"]["Customer"]
    trips += edge['usertype']["31-40"]["Subscriber"]
    trips += edge['usertype']["31-40"]["Customer"]
    trips += edge['usertype']["41-50"]["Subscriber"]
    trips += edge['usertype']["41-50"]["Customer"]
    trips += edge['usertype']["51-60"]["Subscriber"]
    trips += edge['usertype']["51-60"]["Customer"]
    trips += edge['usertype']["60+"]["Subscriber"]
    trips += edge['usertype']["60+"]["Customer"]

    return trips
     
     
     

def either(edge):
    """
    Retorna el vertice A del arco
    """
    return edge['vertexA']


def other(edge, vertex):
    """
    Retorna el vertice B del arco
    """
    return edge['vertexB']


def compareedges(edge1, edge2):
    """
    Compara dos arcos y retorna True si son iguales
    """
    e1v = either(edge1)
    e2v = either(edge2)

    if e1v == e2v:
        if other(edge1, e1v) == other(edge2, e2v):
            return True
    return False


def updateUserType(edge, usertype, group): 
    """
    Actualiza el numero de usarios por clase de usario
    """
    edge['usertype'][group][usertype] += 1

def updateAverageWeight(graph, edge, newweight, vb):
    """
    Actualiza el peso del arco entre los vertices usando el promedio entre los pesos
    """
    edge['sum']+= newweight
    edge['count']+=1 
    edge['weight'] = edge['sum']/edge['count']
    if graph["directed"]:
        degree = map.get(graph['indegree'], vb)
        map.put(graph['indegree'], vb, degree['value']+1)
        
