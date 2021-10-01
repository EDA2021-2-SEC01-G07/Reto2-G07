"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import prettytable
import config as cf
import sys
import controller
from prettytable import PrettyTable
from DISClib.ADT import list as lt
import time
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Get oldest artworks by medium")

catalog = None

def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()

def loadData(catalog):
    """
    Carga los libros en la estructura de datos
    """
    controller.loadData(catalog)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        start_time = time.process_time()
        catalog=initCatalog()
        loadData(catalog)
        end_time=(time.process_time() - start_time)*1000
        print("The processing time is: ",end_time, " ms.")
        

    elif int(inputs[0]) == 2:
        medium=input("Escriba el medio que desea consultar: ")
        display=int(input("Escriba la cantidad de obras (mas antiguas) que desea mostrar: "))
        result=controller.getOldestByMedium(catalog,medium, display)
        
        table=PrettyTable(hrules=prettytable.ALL)
        table.field_names = ["Title", "ConstituentID", "Date", "Medium", "Dimensions", "CreditLine"]
        for row in lt.iterator(result):
            table.add_row([row["Title"], row["ConstituentID"], row["Date"], row["Medium"], row["Dimensions"], row["CreditLine"]])
        print(table)

    else:
        sys.exit(0)
sys.exit(0)
