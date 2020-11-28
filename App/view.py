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


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
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
    print("2- Cargar información de citibike")
    print("3- Calcular componentes conectados")
    print("4- Encontrar rutas circulares: ")
    print("5- Conseguir Top 3 de estaciones: ")
    print("6- Rutas por resistencia: ")
    print("7- Valentina ")
    print("8- Buscar ruta por latitud y longitud: ")
    print("9 BONO")
    print("0- Salir")
    print("*******************************************")


def optionTwo():
    print("\nCargando información de transporte de singapur ....")
    controller.loadTrips(cont)
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
    print('El número de componentes conectados es: ' +
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
    r = controller.getCircularroute(cont,starstation, minTime,maxTime )  
    print("\nEl numero de rutas encontrdas fue "+ str(r[0]) + "\n") 
    print("El detalle cada ruta es: ")
    c = 0
    for i in (r[2]["R_Especifico"]):
        c+=1
        print("\n→ Ruta "+str(c)+ ", informacion: " +  str(r[2]["R_Especifico"][i]))

def optionFive():
    """
    Requerimento 3
    """
    info = controller.getTop(cont)
    print("\nTop 3 de las estaciones con mas llegadas: \n")
    for i in info["In"]:
        print("■  "+ i["id"]+" con un total de "+ str(i["In"])+" llegadas")
    print("\nTop 3 de las estaciones con mas salidas \n")
    for i in info["Out"]:
        print("■  "+ i["id"]+" con un total de "+ str(i["Out"])+" salidas")
    print("\nTop 3 de las estaciones menos usadas: \n")
    for i in info["Usage"]:
        print("■  "+ i["id"]+" con un total de "+ str(i["Usage"])+" llegadas y salidas")
    

def optionSix():
    """
    Requerimento 4
    """
    paths = controller.recorrido_resistencia(cont,initStation, Tmax)
    num=1
    for ruta in paths:
        i=0
        print("\nRuta "+str(num))
        while i<len(ruta["Duraciones"]):
            print("• Estación {0}: ".format(i+1)+ str(ruta["Estaciones"][i]))
            print("• Duración {0}->{1}: ".format(i+1,i+2)+str(round(ruta["Duraciones"][i],2))+" minutos")
            i+=1
        print("• Estación {0}: ".format(i+1)+str(ruta["Estaciones"][i]))
        num+=1

    

def optionSeven():
    """
    Requerimento 5
    """
    resultados=controller.recomendador_rutas(cont,rango)
    if resultados==0:
        print("\nNo se ecnontraron estaciones con usuarios en el rango de edad "+rango+".")
    else:
        print("\nRango elegido: "+rango+" años")
        print("\nEl id de la estación de la que más salen usuarios en el rango es: "+resultados[0]+".")
        print("El id de la estación a la que más llegan usuarios en el rango es: "+resultados[1]+".")
        if resultados[2] != None:
            print("La ruta de estaciones es: "+ " - ".join(resultados[2]))
        else:
            print("No hay ruta entre estas estaciones :(")

        
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
            print("■ "+parada)
        print("El tiempo aproximado de esta ruta es de "+ str(info["Time"])+ " segundos. Buena suerte!")

def optionNine(): 
    """
    Bono
    """
    print(controller.Bono1(cont, edad))
    
    

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        starstation = input("Identificador estacion de inicio: ")
        minTime = input("tiempo minimo en min: ")
        maxTime = input("Tiempo maximo en min: ")
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        Tmax=float(input("Ingere el tiempo mÃ¡ximo de resistencia en minutos: "))
        initStation = input("Ingrese el ID de la estación de inicio (Ej: 72): ")
        executiontime = timeit.timeit(optionSix, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        rango=input("Ingrese rango de edad:")
        executiontime = timeit.timeit(optionSeven, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))
        
    elif int(inputs[0]) == 8:
        latu = float(input("Ingrese la latitud de su ubicacion: "))
        lonu = float(input("Ingrese la longitud de su ubicacion:"))
        latd = float(input("Ingrese la latitud del sitio que desea visitar: "))
        lond = float(input("Ingrese la longitud del sitio que desea visitar: "))
        coordsu = (latu,lonu)
        coordsd = (latd,lond)
        executiontime = timeit.timeit(optionEight, number=1)
    elif int(inputs[0]) == 9:
        edad = input("Grupo de Edad :")
        executiontime = timeit.timeit(optionNine, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))
    else:
        sys.exit(0)
sys.exit(0)
