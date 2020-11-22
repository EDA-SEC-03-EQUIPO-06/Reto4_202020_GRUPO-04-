"""
 * Copyright 2020, Departamento de sistemas y ComputaciÃ³n
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
 * ContribuciÃ³n de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacciÃ³n con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operaciÃ³n seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

file = "201801-1-citibike-tripdata.csv"
initialStation = None
recursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar informaciÃ³n de buses de singapur")
    print("3- Calcular componentes conectados")
    print("4- Establecer estaciÃ³n base:")
    print("5- Conseguir Top 3 de estaciones")
    print("6- Ruta de costo mÃ­nimo desde la estaciÃ³n base y estaciÃ³n: ")
    print("7- EstaciÃ³n que sirve a mas rutas: ")
    print("0- Salir")
    print("*******************************************")


def optionTwo():
    print("\nCargando informaciÃ³n de transporte de singapur ....")
    controller.loadFile(cont,file)
    numedges = controller.totalRoutes(cont)
    numvertex = controller.totalStations(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))


def optionThree():
    """
    Requerimento 1
    """
    print('El nÃºmero de componentes conectados es: ' +
          str(controller.connectedComponents(cont)))
    s1 = input("Inserte el id de una estacion: ")
    s2 = input("Inserte el id de otra estacion: ")
    same = controller.sameCluster(cont, s1, s2)
    if same == None:
        print("Alguna de las estaciones ingresadas no existe")
    elif same:
        print("Las estaciones estan en el mismo cluster")
    else:
        print("Las estaciones no estan en el mismo cluster")


def optionFour():
    """
    Requerimento 2
    """
    
def optionFive():
    """
    Requerimento 3
    """
    info = controller.getTop(cont)
    print("\nTop 3 de las estaciones con mas llegadas: \n")
    for i in info["In"]:
        print("â  "+ i["id"]+" con un total de "+ str(i["In"])+" llegadas")
    print("\nTop 3 de las estaciones con mas salidas \n")
    for i in info["Out"]:
        print("â  "+ i["id"]+" con un total de "+ str(i["Out"])+" llegadas")
    print("\nTop 3 de las estaciones menos usadas: \n")
    for i in info["Usage"]:
        print("â  "+ i["id"]+" con un total de "+ str(i["Usage"])+" llegadas y salidas")
    

def optionSix():
    """
    Requerimento 4
    """
    paths = controller.recorrido_resistencia(cont,initStation, Tmax)
    

def optionSeven():
    """
    Requerimento 5
    """
    resultados=controller.recomendador_rutas(cont,rango)
def optionEight():
    """
    Requerimento 6
    """
    info = controller.getClosestTouristicRoute(cont,coordsu,coordsd)
    print("\n=====================================================")
    print("La parada mas cercana a ti es: "+info["InitialStation"])
    print("La parada mas cercana a tu destino es: "+ info["EndStation"])
    if info["Route"] is None:
        print("Lo sentimos, no hay una ruta disponible entre estas dos paradas :(")
    else:
        print("La ruta con la que llegaras en menor tiempo es: ")
        for parada in info["Route"]:
            print("â  "+parada)
        print("El tiempo aproximado de esta ruta es de "+ str(info["Time"])+ " segundos. Buena suerte!")
    
    
    



"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opciÃ³n para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usarÃ¡ de acÃ¡ en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecuciÃ³n: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecuciÃ³n: " + str(executiontime))

    elif int(inputs[0]) == 4:
        msg = "EstaciÃ³n Base: BusStopCode-ServiceNo (Ej: 75009-10): "
        initialStation = input(msg)
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecuciÃ³n: " + str(executiontime))

    elif int(inputs[0]) == 5:
        #destStation = input("EstaciÃ³n destino (Ej: 15151-10): ")
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecuciÃ³n: " + str(executiontime))

    elif int(inputs[0]) == 6:
        Tmax=float(input("Ingere el tiempo mÃ¡ximo de resistencia en minutos: "))
        initStation = input("Ingrese el ID de la estaciÃ³n de inicio (Ej: 72): ")
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecuciÃÂ³n: " + str(executiontime))

    elif int(inputs[0]) == 7:
        rango=input("Ingrese rango de edad:")
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecuciÃ³n: " + str(executiontime))
        
    elif int(inputs[0]) == 8:
        latu = float(input("Ingrese la latitud de su ubicacion: "))
        lonu = float(input("Ingrese la longitud de su ubicacion:"))
        latd = float(input("Ingrese la latitud del sitio que desea visitar: "))
        lond = float(input("Ingrese la longitud del sitio que desea visitar: "))
        coordsu = (latu,lonu)
        coordsd = (latd,lond)
        executiontime = timeit.timeit(optionEight, number=1)

    else:
        sys.exit(0)
sys.exit(0)
