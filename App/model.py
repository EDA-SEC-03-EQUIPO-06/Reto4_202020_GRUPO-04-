"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import edge as e
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    citibike = {"graph":None,
                "components": None}
    citibike["graph"] = gr.newGraph(datastructure='ADJ_LIST',
                                    directed=True,
                                    size=1000,
                                    comparefunction= compareStations)
    return citibike

# Funciones para agregar informacion al grafo
def addTrip(citibike, trip):
    """
    """
    origin = trip["start station id"]
    destination = trip["end station id"]
    duration = int(trip["tripduration"])
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)
    
def addStation(citibike, stationid):
    if not gr.containsVertex(citibike["graph"], stationid):
        gr.insertVertex(citibike["graph"], stationid)
    return citibike
    
def addConnection(citibike, origin, destination, duration):
    edge = gr.getEdge(citibike["graph"], origin, destination)
    if edge is None:
        gr.addEdge(citibike["graph"], origin, destination, duration)
    else:
        e.updateAverageWeight(edge,duration)
    return citibike
# ==============================
# Funciones de consulta
# ==============================

    
def totalRoutes(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])
    
def totalStations(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])
    
def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['graph'])
    return scc.connectedComponents(analyzer['components'])
    
def sameCC(analyzer,station1,station2):
    return scc.stronglyConnected(analyzer['components'],station1,station2)


# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1