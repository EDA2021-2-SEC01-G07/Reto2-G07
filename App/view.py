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

import prettytable as pt 
import config as cf
import sys
import controller
from prettytable import PrettyTable
from DISClib.ADT import list as lt
import time
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
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
    print("2- (Lab5) Obtener ultimas obras por medio")
    print('3- (Lab6) Numero total de obras por nacionalidad')
    print("4- (Req1) Listar cronologicamente los artistas")
    print("5- (Req2) Listar cronologicamente las adquisiciones")
    print("6- (Req3) Clasificar obras de artista por tecnica")
    print("7- (Req4) Clasificar obras por nacionalidad")

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
        print(catalog['department'])
        end_time=(time.process_time() - start_time)*1000
        print('Numero de artistas cargados: ' + str(lt.size(catalog['artists'])))
        print('Numero de obras cargadas: ' + str(lt.size(catalog['artworks']))+"\n")
        print("The processing time is: ",end_time, " ms.")

    elif int(inputs[0]) == 2:
        medium=input("Escriba el medio que desea consultar: ")
        display=int(input("Escriba la cantidad de obras (mas antiguas) que desea mostrar: "))
        result=controller.getOldestByMedium(catalog,medium, display)
        
        table=PrettyTable(hrules=pt.ALL)
        table.field_names = ["Title", "ConstituentID", "Date", "Medium", "Dimensions", "CreditLine"]
        for row in lt.iterator(result):
            table.add_row([row["Title"], row["ConstituentID"], row["Date"], row["Medium"], row["Dimensions"], row["CreditLine"]])
        print(table)
    
    elif int(inputs[0])== 3:
        nationality=input('Nacionalidad a buscar: ')
        result=controller.getTotalNationalities(catalog,nationality)
        print('Para la nacionalidad ' + nationality+ ' se encontraron '+ str(result)+' obras de arte.')
    elif int(inputs[0])== 4:
        first=int(input("Año inicial: "))
        last=int(input("Año final: "))
        start_time = time.process_time()
        cronologicalArtists=controller.cronologicalArtists(catalog,first,last)
        end_time=(time.process_time() - start_time)*1000
        print("="*15+ "Req No. 1 Inputs"+ "="*15)
        print("Artist born between "+ str(first)+" and " +str(last))
        print("="*15, "Req No. 1 Answers", "="*15)
        print('There are '+ str(cronologicalArtists[0]),' born between'+ str(first)+" and " +str(last)+"\n")

        print('The first and last 3 artists in range are...')
        table= pt.PrettyTable()
        table.field_names=["ConstituentID","DisplayName","BeginDate","Nationality","Gender","ArtistBio","Wiki QID","ULAN"]
        table.max_width=30
        for line in lt.iterator(cronologicalArtists[1]):
            table.add_row([line["ConstituentID"],line["DisplayName"],line["BeginDate"],line["Nationality"],line["Gender"],line["ArtistBio"],line["Wiki QID"],line["ULAN"]])
        print(table)
        print("The processing time is: ",end_time, " ms.")

    elif int(inputs[0])== 7:
        start_time = time.process_time()
        nationalities=controller.sortByNationality(catalog)
        end_time=(time.process_time() - start_time)*1000

        print("="*15+ "Req No. 4 Inputs"+ "="*15)
        print("Ranking countries by their number of artworks in the MoMA...\n")
        print("="*15, "Req No. 4 Answers", "="*15)
        print("The TOP 10 Countries in the MoMA are:")
        table= pt.PrettyTable()
        table.field_names=["Nationality","Artworks"]
        table.hrules = pt.ALL
        table.max_width=30
        for n in range(1,11):
            line=lt.getElement(nationalities[0],n)
            table.add_row([line["nationality"],line["Artworks"]])
        print(table)
        
        top=lt.getElement(nationalities[0],1)["nationality"]
        print("\nThe TOP nacionality in the museum is",top,"with", lt.size(nationalities[1]),"unique pieces.")
        print("The first and last 3 objects in the",top,"artwork list are:")  
        
        table2=pt.PrettyTable()
        table2.field_names=["ObjectID","Title","ArtistsNames","Medium","Date","Dimensions","Department","Classification","URL"]
        for n in lt.iterator(nationalities[2]):
            names=str(n["Names"])
            names=names[1:len(names)-1].replace("'","")
            table2.add_row([n["id"],n["title"],names,n["medium"],n["date"],n["dimensions"],n["department"],n["classification"],n["url"]])
        table2.align="l"
        table2._max_width={"ObjectID":17,"Title":17,"ArtistsNames":18,"Medium":18,"Date":17,"Dimensions":18,"Department":15,"Classification":17,"URL":22}
        table2.hrules = pt.ALL
        print(table2)
        
        print("The processing time is: ",end_time, " ms.")
    else:
        sys.exit(0)
sys.exit(0)
