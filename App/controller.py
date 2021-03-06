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

import config as cf
import os
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips(citibike):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(citibike, filename)
    return citibike
    
def loadFile(citibike, tripfile):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding= "utf-8"),
                                delimiter = ",")
    for trip in input_file:
        model.addTrip(citibike, trip)
    return citibike
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def totalRoutes(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalRoutes(analyzer)
    
def totalStations(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStations(analyzer)
    
def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)
    
def sameCluster(analyzer,station1,station2):
    return model.sameCC(analyzer,station1,station2)
    
def getTop(analyzer):
    PQs = model.stationsUsage(analyzer)
    return model.organizeTop3(PQs)
    
def getClosestTouristicRoute(cont,coordsu,coordsd):
    return model.giveShortestRoute(cont, coordsu, coordsd)
 
def recorrido_resistencia(analyzer,initStation, Tmax):
    return model.recorrido_resistencia(analyzer, initStation, Tmax)

def recomendador_rutas(analyzer,rango):
    return model.recomendador_rutas(analyzer,rango)

def getCircularroute(analyzer, StartStationid, avaibleTimemin, avaibleTimemax):
    avaibleTimemin = int(avaibleTimemin)
    avaibleTimemax = int(avaibleTimemax)
    return model.circulargraph(analyzer, StartStationid, avaibleTimemin, avaibleTimemax)
    

def Bono1(analyzer, edad):
    return model.announcementStation(analyzer, edad)