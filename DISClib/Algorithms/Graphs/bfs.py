"""
 * Copyright 2020, Departamento de sistemas y ComputaciÃ³n,
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
 * ContribuciÃ³n de:
 *
 * Dario Correal
 *
 """

import config
from DISClib.ADT import graph as g
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import queue
from DISClib.ADT import map as map
from DISClib.ADT import stack
from DISClib.Utils import error as error
assert config


def BreadhtFisrtSearch(graph, source, maxtime):
    """
    Genera un recorrido BFS sobre el grafo graph
    Args:
        graph:  El grafo a recorrer
        source: Vertice de inicio del recorrido.
    Returns:
        Una estructura para determinar los vertices
        conectados a source
    Raises:
        Exception
    """
    try:
        search = {
                  'source': source,
                  'visited': None
                  }
        search['visited'] = map.newMap(numelements=g.numVertices(graph),
                                       maptype='PROBING',
                                       comparefunction=graph['comparefunction']
                                       )
        map.put(search['visited'], source, {'marked': True,
                                            'edgeTo': None,
                                            'distTo': 0,
                                            "final":False
                                            })
        bfsVertex(search, graph, source, maxtime)
        return search
    except Exception as exp:
        error.reraise(exp, 'bfs:BFS')


def bfsVertex(search, graph, source, maxtime):
    """
    Funcion auxiliar para calcular un recorrido BFS
    Args:
        search: Estructura para almacenar el recorrido
        vertex: Vertice de inicio del recorrido.
    Returns:
        Una estructura para determinar los vertices
        conectados a source
    Raises:
        Exception
    """
    try:
        adjsqueue = queue.newQueue()
        queue.enqueue(adjsqueue, source)
        
        while not queue.isEmpty(adjsqueue):
            
            vertex = queue.dequeue(adjsqueue)
            visited_v = map.get(search['visited'], vertex)['value']
            adjslst = g.adjacents(graph, vertex)
            adjslstiter = it.newIterator(adjslst)
            
            if not (it.hasNext(adjslstiter)):
                visited_v["final"]=True
            c=0
            while (it.hasNext(adjslstiter)) :
                if c==1 and vertex!=source:
                    break
                total_time=0
                w = it.next(adjslstiter)
                if not (it.hasNext(adjslstiter)) and c==0:
                    visited_v["final"]=True
                
                edge = g.getEdge(graph, vertex, w)
                time=edge['weight']/60
                visited_w = map.get(search['visited'], w)
                if visited_w is None:
                    if visited_v["final"]==False:                        
                        dist_to_w = visited_v['distTo'] + time
                        total_time=dist_to_w
                        if total_time<=maxtime:
                            visited_w = {'marked': True,
                                         'edgeTo': vertex,
                                         "distTo": dist_to_w,
                                         "final":False}
                            map.put(search['visited'], w, visited_w)
                            queue.enqueue(adjsqueue, w)
                            c=1
                        
        return search
    except Exception as exp:
        error.reraise(exp, 'bfs:bfsVertex')



def hasPathTo(search, vertex):
    """
    Indica si existe un camino entre el vertice source
    y el vertice vertex
    Args:
        search: Estructura de recorrido BFS
        vertex: Vertice destino
    Returns:
        True si existe un camino entre source y vertex
    Raises:
        Exception
    """
    try:
        element = map.get(search['visited'], vertex)
        if element and element['value']['marked'] is True:
            return True
        return False
    except Exception as exp:
        error.reraise(exp, 'bfs:hasPathto')


def pathTo(search, vertex):
    """
    Retorna el camino entre el vertices source y el
    vertice vertex
    Args:
        search: La estructura con el recorrido
        vertex: Vertice de destingo
    Returns:
        Una pila con el camino entre el vertices source y el
        vertice vertex
    Raises:
        Exception
    """
    try:
        if hasPathTo(search, vertex) is False:
            return None
        path = stack.newStack()
        while vertex != search['source']:
            stack.push(path, vertex)
            vertex = map.get(search['visited'],
                             vertex)['value']['edgeTo']
        stack.push(path, search['source'])
        return path
    except Exception as exp:
        error.reraise(exp, 'bfs:pathto')
