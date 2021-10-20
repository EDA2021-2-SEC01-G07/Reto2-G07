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
    print('8- (Req5) Transportar obras de un departamento')

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
            table.add_row([row["Title"], row["ConstituentID"], 
            row["Date"], row["Medium"], row["Dimensions"], row["CreditLine"]])
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
        print('There are',str(cronologicalArtists[0]),'born between',str(first),"and",str(last)+"\n")

        print('The first and last 3 artists in range are...')
        table= pt.PrettyTable()
        table.field_names=["ConstituentID","DisplayName","BeginDate",
        "Nationality","Gender","ArtistBio","Wiki QID","ULAN"]
        table.max_width=30
        for line in lt.iterator(cronologicalArtists[1]):
            table.add_row([line["id"],line["name"],line["begin_date"],
            line["nationality"],line["gender"],line["biography"],line["wiki_id"],line["ulan"]])
        print(table)
        print("The processing time is: ",end_time, " ms.")
    elif int(inputs[0])== 5:
        start = input("Enter the starting date in a YYYY-MM-DD format: ")
        end = input("Enter the ending date in a YYYY-MM-DD format: ")
        start_time = time.process_time()

        results = controller.cronologicalArtwork(catalog, start, end)
        end_time=(time.process_time() - start_time)*1000
        sample = me.getValue(mp.get(results, "sample"))
        size = me.getValue(mp.get(results, "size"))
        artists = me.getValue(mp.get(results, "artists"))
        purchased = me.getValue(mp.get(results, "purchased"))

        print("="*15+ "Req No. 2 Inputs"+ "="*15)
        print(f"Artworks between {start} and {end}")
        print("="*15, "Req No. 2 Answers", "="*15)
        print(f"The MoMA acquired {size} unique pieces between {start} and {end}")
        print(f"With {artists} different artists and purchased {purchased} of them.")
        print("The first and last 3 artists in the range are...")

        table = pt.PrettyTable(hrules=pt.ALL)
        table.field_names = ["ObjectID", "Title", "ArtistsNames", "Medium", "Dimensions", "Date", "DateAcquired", "URL"]

        for n in lt.iterator(sample):
            names=str(n["names"])[1:-1].replace("'","")

            table.add_row([n["id"],n["title"],names,n["medium"],
            n["dimensions"],n["date"],n["date_aquired"],n["url"]])

        table.align="l"
        table._max_width={"ObjectID":17,"Title":17,"ArtistsNames":18,"Medium":18,
        "Dimensions":18,"Date":17,"DateAcquired":15,"URL":22}

        print(table)
        print("The processing time is: ",end_time, " ms.")

    elif int(inputs[0])== 6:
        artist_name = input("Enter the name of the artist to search: ")
        start_time = time.process_time()
        results = controller.techniquesFromArtist(catalog, artist_name)

        id = me.getValue(mp.get(results, "id"))
        total_artworks = me.getValue(mp.get(results, "total_artworks"))
        most_used = me.getValue(mp.get(results, "most_used"))
        ranking_list = me.getValue(mp.get(results, "ranking_list"))
        end_time=(time.process_time() - start_time)*1000
        print("="*15+ "Req No. 3 Inputs"+ "="*15)
        print("Examine the work of the artist named:",artist_name)
        print("="*15, "Req No. 3 Answers", "="*15)
        print(f"{artist_name} with MoMA ID {id} has {total_artworks} pieces in his/her name at the museum.")
        print(f"There are {lt.size(ranking_list)} different mediums/techniques in his/her work.")

        print("Her/His top 5 Medium/Techniques are: ")

        ranking_table = pt.PrettyTable(hrules=pt.ALL)
        ranking_table.field_names = ["MediumName", "Count"]

        for i in range(5):
            pair = lt.getElement(ranking_list, i+1)
            ranking_table.add_row([me.getKey(pair), lt.size(me.getValue(pair))])
        
        ranking_table._max_width={"MediumName": 20, "Count": 10}
        print(ranking_table)

        first_pair = lt.getElement(ranking_list, 1)

        print(f"His/Her most used Medium/Technique is: {me.getKey(pair)} with {lt.size(me.getValue(pair))} pieces.")
        print(f"A sample of {lt.size(me.getValue(pair))} Photogravure from the collection are:")

        sample_table = pt.PrettyTable(hrules=pt.ALL)
        sample_table.field_names = ["ObjectID", "Title", "Medium", "Date", "Dimensions",
         "DateAcquired", "Department", "Classification", "URL"]
        
        for n in lt.iterator(me.getValue(first_pair)):
            names=str(n["names"])[1:-1].replace("'","")

            sample_table.add_row([n["id"],n["title"],n["medium"],
            n["date"],n["dimensions"],n["date_aquired"],
            n["department"], n["classification"],n["url"]])
        sample_table._max_width = {"ObjectID":20, "Title":20, "Medium":20, "Date":20, "Dimensions":20,
         "DateAcquired":20, "Department":20, "Classification":20, "URL":20}
        print(sample_table)
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
        table2.field_names=["ObjectID","Title","ArtistsNames","Medium","Date",
        "Dimensions","Department","Classification","URL"]
        for n in lt.iterator(nationalities[2]):
            names=str(n["names"])[1:-1].replace("'","")
            table2.add_row([n["id"],n["title"],names,n["medium"],n["date"],
            n["dimensions"],n["department"],n["classification"],n["url"]])
        table2.align="l"
        table2._max_width={"ObjectID":17,"Title":17,"ArtistsNames":18,"Medium":18,
        "Date":17,"Dimensions":18,"Department":15,"Classification":17,"URL":22}
        table2.hrules = pt.ALL
        print(table2)
        
        print("The processing time is: ",end_time, " ms.")
    elif int(inputs[0]) == 8:
        department = input("Department to search: ")
        start_time = time.process_time()
        results = controller.costFromDepartment(catalog, department)
        end_time=(time.process_time() - start_time)*1000
        print("="*15, "Req No. 5 Inputs", "="*15)
        print("Estimate the cost to transport all artifacts in", department, "MoMA's department\n")
        print("="*15, "Req No. 5 Answers", "="*15)

        length = me.getValue(mp.get(results, "length"))
        cost = round(me.getValue(mp.get(results, "cost")),2)
        weight = round(me.getValue(mp.get(results, "weight")),2)
        oldest = me.getValue(mp.get(results, "oldest"))
        expensive = me.getValue(mp.get(results, "expensive"))

        print(f"The MoMA is going to transport {length} artifacts from the {department} MoMA's department")
        print(f"Estimated cargo weigth (kg): {weight}")
        print(f"Estimated cargo cost (USD): {cost}")

        expensive_table = pt.PrettyTable(hrules=pt.ALL)
        expensive_table.field_names = ["ObjectID", "Title", "ArtistsNames", "Medium", "Date",
         "Dimensions", "Classification", "TransCost (USD)", "URL"]
        expensive_table._max_width ={'ObjectID':17, 'Title':17,"ArtistsNames":17, 'Medium':17, 'Date':17, 'Dimensions':17,
     'Classifications':17, 'TransCost (USD)':17, 'URL':17}
        expensive_table.hrules = pt.ALL
        
        for artwork in lt.iterator(expensive):
            names = str(artwork["names"])[1:-1].replace("'", "")
            expensive_table.add_row([artwork["id"], artwork["title"], names, artwork["medium"], artwork["date"],
            artwork["dimensions"], artwork["department"], artwork["classification"], artwork["url"]])
        
        print(expensive_table)
        print("The TOP 5 oldest items to transport are:\n")
        oldest_table = pt.PrettyTable(hrules=pt.ALL)
        oldest_table.field_names = ["ObjectID", "Title", "ArtistsNames", "Medium", "Date",
         "Dimensions", "Classification", "TransCost (USD)", "URL"]
        oldest_table.hrules = pt.ALL
        oldest_table._max_width ={'ObjectID':17, 'Title':17,"ArtistsNames":17, 'Medium':17, 'Date':17, 'Dimensions':17,
     'Classifications':17, 'TransCost (USD)':17, 'URL':17}
        for artwork in lt.iterator(oldest):
            names = str(artwork["names"])[1:-1].replace("'", "")
            oldest_table.add_row([artwork["id"], artwork["title"], names, artwork["medium"], artwork["date"],
            artwork["dimensions"], artwork["department"], artwork["classification"], artwork["url"]])
        
        print(oldest_table)
        print("The processing time is: ",end_time, " ms.")
    else:
        sys.exit(0)
