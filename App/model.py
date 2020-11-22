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
from DISClib.ADT import minpq as pq
from DISClib.ADT import stack as st
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me
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
    citibike["stationinfo"] = m.newMap(numelements=1400,
                                       maptype= 'PROBING',
                                       comparefunction= compareStationsMap)
    return citibike

# Funciones para agregar informacion al grafo
def addTrip(citibike, trip):
    """
    """
    origin = trip["start station id"]
    destination = trip["end station id"]
    
    if not m.contains(citibike["stationinfo"], origin):
        originInfo = organizeData(trip,True)
    else:
        originInfo = me.getValue(m.get(citibike["stationinfo"],origin))
    if not m.contains(citibike["stationinfo"], destination):
        destinationInfo = organizeData(trip,False)
    else:
        destinationInfo = me.getValue(m.get(citibike["stationinfo"],destination))
        
    duration = int(trip["tripduration"])
    addStation(citibike, origin, originInfo)
    addStation(citibike, destination, destinationInfo)
    addConnection(citibike, origin, destination, duration)
    addAges(originInfo,trip, True)
    addAges(destinationInfo, trip, False)
    
def addAges(station,info, origin):
    group = getAgeGroup(info["birth year"])
    en = {"In": 0, "Out": 0}
    if not m.contains(station["Ages"],group):
        m.put(station["Ages"], group, en)
    entry = me.getValue(m.get(station["Ages"], group))
    if origin:
        entry["Out"] += 1
    else:
        entry["In"] += 1
    m.put(station["Ages"], group, entry)
    return station
    
def addStation(citibike, id, info):
    if not gr.containsVertex(citibike["graph"], id):
        gr.insertVertex(citibike["graph"], id)
    if not m.contains(citibike['stationinfo'], id):
        m.put(citibike['stationinfo'],id,info)
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
    try: 
        return scc.stronglyConnected(analyzer['components'],station1,station2)
    except:
        return None
    

#Requerimento 3
def stationsUsage(analyzer):
    indegreePQ = pq.newMinPQ(cmpfunction= compareDegreeMax)
    outdegreePQ = pq.newMinPQ(cmpfunction= compareDegreeMax)
    lessUsedPQ = pq.newMinPQ(cmpfunction= compareDegreeMin)
    vortexLst = gr.vertices(analyzer["graph"])
    ite = it.newIterator(vortexLst)
    
    
    while it.hasNext(ite):
        station = it.next(ite)
        StationName = getName(analyzer["stationinfo"],station)
        #Se obtienen los valores de las estaciones que entran, que salen y su suma
        
        indegree = gr.indegree(analyzer["graph"],station)
        outdegree = gr.outdegree(analyzer["graph"],station)
        usage = outdegree+indegree
        #Se crean entradas para organizar en el PQ
        
        indegreeEntry = {"key": indegree, "station": StationName}
        outdegreeEntry = {"key": outdegree, "station": StationName}
        usageEntry = {"key": usage, "station": StationName}
        
        #Se inserta cada entrada en los PQ correspondientes
        pq.insert(indegreePQ, indegreeEntry)
        pq.insert(lessUsedPQ,usageEntry)
        pq.insert(outdegreePQ, outdegreeEntry)
        
    return {"In": indegreePQ,"Out": outdegreePQ, "Usage": lessUsedPQ}
    
def organizeTop3(PQs):
    InTop = []
    OutTop = []
    UsageTop = []
    for i in range (0,3):
        #Se sacan los 3 primeros de cada Pq
        In = pq.delMin(PQs["In"])
        Out = pq.delMin(PQs["Out"])
        Usage = pq.delMin(PQs["Usage"])
        
        InTop.append({"id": In["station"], "In": In["key"]} )
        OutTop.append({"id": Out["station"], "Out": Out["key"] })
        UsageTop.append({"id": Usage["station"], "Usage": Usage["key"] })
        
    return {"In": InTop,"Out": OutTop, "Usage": UsageTop}
    
#Requerimento 6

def giveShortestRoute(analyzer, originCoords, destCoords):
    """
    Encuentra la ruta mas corta para ir desde una posicion (originCoords) a otra (destCoords).
    Args:
        analyzer: Estructura de datos principal
        originCoords: Tupla con las coordenadas x,y de la posicion del usuario.
        destCoords: Tupla con las coordenadas x,y del destino del usuario.
    """
    originStationId = getClosestStation(analyzer, originCoords)
    destinStationId = getClosestStation(analyzer, destCoords)
    
    search = djk.Dijkstra(analyzer["graph"], originStationId)
    path = djk.pathTo(search, destinStationId)
    
    originStationName = getName(analyzer["stationinfo"], originStationId)
    destinStationName = getName(analyzer["stationinfo"], destinStationId)
    time = djk.distTo(search, destinStationId)
    route = []
    
    if path is None:
        route = None
    else:
        while not st.isEmpty(path):
            entry = st.pop(path)
            id = entry["vertexA"]
            name = getName(analyzer["stationinfo"], id)
            route.append(name)
            if st.size(path) == 1:
                id2 = entry["vertexB"]
                name2 = getName(analyzer["stationinfo"],id2)
                route.append(name2)
    
    finalInfo = {"InitialStation": originStationName, "EndStation": destinStationName, "Route": route, "Time": time}
    return finalInfo
        
    
    


# ==============================
# Funciones Helper
# ==============================

def organizeData(information, origin):
    """
    Crea un diccionario con informacion sobre una estacion en particular
    Args:
        information: El diccionario que viene del archivo con toda la info sobre un viaje
        Origin: Un booleando que define si se esta arreglando la estacion de inicio o de final de un viaje en particular 
    """
    stationInfo = {"StationID":None, "StationName": None, "Coordinates": None,"Ages":None}
    if origin:
        stationInfo["StationID"] = information["start station id"]
        stationInfo["StationName"] = information["start station name"]
        stationInfo["Coordinates"] = (float(information["start station latitude"]),float(information["start station longitude"]))
        stationInfo["Ages"] = m.newMap(maptype="PROBING",
                                         comparefunction= compareAges)
        
    else:
        stationInfo["StationID"] = information["end station id"]
        stationInfo["StationName"] = information["end station name"]
        stationInfo["Coordinates"] = (float(information["end station latitude"]),float(information["end station longitude"]))
        stationInfo["Ages"] = m.newMap(maptype="PROBING",
                                         comparefunction= compareAges)
    return stationInfo
    
def getClosestStation(analyzer, coords):
    """
    Retorna el ID de la estacion mas cercana a las coordenadas dadas
    Args:
        analyzer: Estructura de datos principal
        coords: Coordenadas de donde se quiere hallar la estacion mas cercana
    """
    
    map = analyzer["stationinfo"]
    stations = m.keySet(map) #Obtiene los id de todas las estaciones en el analizador
    ite = it.newIterator(stations)
    
    closestDist = -1
    closestID = ""
    
    while it.hasNext(ite):
    
        id = it.next(ite)
        station = me.getValue(m.get(map,id))
        dist = getDistance(station["Coordinates"], coords)
        if closestDist == -1:
            closestDist = dist
            closestID = station["StationID"]
        else:
            if dist < closestDist:
                closestDist = dist
                closestID = station["StationID"]
    
    return closestID
    
def getDistance(coords1,coords2):
    """
    Retorna la distancia entre dos coordenadas dadas
    """
    distanceSquared = (coords1[0]-coords2[0])**2 + (coords1[1]-coords2[1])**2
    return distanceSquared**0.5

def getName(map, key):
    """
    Retorna el nombre de una estacion asociada al ID dado (key)
    """
    
    info = me.getValue(m.get(map,key))
    return info["StationName"]
    
def getAgeGroup(birth):
    age = 2018- int(birth)
    if age <= 10:
        return "0-10"
    elif age <= 20:
        return "11-20"
    elif age <= 30:
        return "21-30"
    elif age <= 40:
        return "31-40"
    elif age <= 50:
        return "41-50"
    elif age <= 60:
        return "51-60"
    else:
        return "60+"
        
    

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
        
def compareStationsMap(value1,value2):
    value2 = value2["key"]
    if value1 == value2:
        return 0
    elif value1 > value2:
        return -1
    else:
        return 1

        
def compareDegreeMax(value1,value2):
    value1 = value1["key"]
    value2 = value2["key"]
    if value1 == value2:
        return 0
    elif value1 > value2:
        return -1
    else:
        return 1
        
def compareDegreeMin(value1,value2):
    value1 = value1["key"]
    value2 = value2["key"]
    if value1 == value2:
        return 0
    elif value1 > value2:
        return 1
    else:
        return -1

def compareAges(value1,value2):
    value2 = value2["key"]
    if value1 == value2:
        return 0
    elif value1 > value2:
        return -1
    else:
        return 1