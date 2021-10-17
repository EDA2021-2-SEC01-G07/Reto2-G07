"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import sys
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
import datetime as dt
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el catálogo de artistas

    Crea una lista vacia para guardar todos los libros

    Se crean indices (Maps) por los siguientes criterios:
    Autores
    Obras

    Retorna el catalogo inicializado.
    """

    catalog = {
        'artists': None,
        'mediums': None
        
    }

    """
    Indices creados en el catalogo por medio, nacionalidad, años de nacimiento para autores, id de artistas y obras
    """
    catalog['mediums'] = mp.newMap(800, #5500   mp.size[mediums]/4
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=compareArtworkMedium)
    

    catalog['nationality'] = mp.newMap(800, #15   mp.size[nationality]//4
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=compareArtistNatio)

    catalog['years'] =  mp.newMap(800, #250        la diferencia entre fecha mas grande y menor/4
                                   maptype='CHAINING', 
                                   loadfactor=4,
                                   comparefunction=compareArtistDate)

    catalog['artist_id'] =  mp.newMap(800, #3900    tamaño archivo/4
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=compareArtistId)
    
    catalog['artwork_id'] =  mp.newMap(800, #38000   tamaño archivo/4
                                maptype='CHAINING',
                                loadfactor=4,
                                comparefunction=compareArtworkId)
    """
    Listas con todos los artistas y obras
    """
    catalog['artists'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['artworks'] = lt.newList(datastructure='ARRAY_LIST')
    return catalog
    

# Funciones para agregar informacion al catalogo

def newArtist(id, name, biography, nationality, gender, begin_date, end_date, wiki_id, ulan):
    artist = {'id': id,
    'name': name,
    'biography': biography,
    'nationality': nationality,
    'gender': gender,
    'begin_date': int(begin_date),
    'end_date': int(end_date),
    'wiki_id': wiki_id,
    'ulan': ulan
    }
    for key in artist:
        if artist[key] == "":
            artist[key] = "Unknown"
    return artist
def newArtwork(id, title, constituent_id, date, medium, dimensions, credit_line,
accession_number, classification, department, date_aquired, cataloged, url, circumference,
depth, diameter, height, lenght, weight, width, seat_height, duration):
    artwork = {"id": id,
    "title": title,
    "constituent_id": constituent_id,
    "date": date,
    "medium": medium,
    "dimensions": dimensions,
    "credit_line": credit_line,
    "accession_number": accession_number,
    "classification": classification,
    "department": department,
    "date_aquired": date_aquired,
    "cataloged": cataloged,
    "url": url,
    "circumference": circumference,
    "depth": depth,
    "diameter": diameter,
    "height": height,
    "lenght": lenght,
    "weight": weight,
    "width": width,
    "seat_height": seat_height,
    "duration": duration
    }

    for key in artwork:
        if artwork[key] == '':
            artwork[key] = "Unknown"
    return artwork

def addArtist(catalog, artist):
    a = newArtist(id=artist["ConstituentID"],
    name=artist["DisplayName"], 
    biography=artist["ArtistBio"],
    nationality=artist["Nationality"],
    gender=artist["Gender"],
    begin_date=artist["BeginDate"],
    end_date=artist["EndDate"],
    wiki_id=artist["Wiki QID"],
    ulan=artist["ULAN"])
    lt.addLast(catalog['artists'], a)
    for key in artist:
        if artist[key] == '':
            artist[key] = "Unknown"
    mp.put(catalog['artist_id'],artist['ConstituentID'],artist)

    years=catalog['years']  #Crea un mapa con indice por años de nacimiento de los artistas
    artist_year = artist['BeginDate']
    existYear = mp.contains(years,artist_year) #Valor booleano para saber si ya se creo la nacionalidad
    if existYear:
        entry = mp.get(years,artist_year)
        year = me.getValue(entry)
    else:
        year=newArtistYear(artist_year)#Crea un diccionaro con llave nacionalidad y valor una lista vacia
        mp.put(years,artist_year,year)# Se mete el artista en el mapa 
    lt.addLast(year['artists'],artist)#Añade toda la informacion del artista bajo la llave de su nacionalidad.


def loadNationality(catalog):
    nationalities=catalog['nationality']
    artist_map=catalog['artist_id']
    artworks=catalog['artworks']
    for artwork in lt.iterator(artworks):
        code=artwork["constituent_id"] 
        code=code[1:-1].replace(" ","").split(",")
        
        for artist_id in code:
            artist_nationality=me.getValue(mp.get(artist_map,artist_id))["Nationality"]
            if artist_nationality=="" or artist_nationality =="Nationality unknown":
                artist_nationality="Unknown"

            if mp.contains(nationalities,artist_nationality):
                entry = mp.get(nationalities,artist_nationality)
                natio = me.getValue(entry)
            else:
                natio = lt.newList('ARRAY_LIST')
                mp.put(nationalities, artist_nationality, natio) 
            
            lt.addLast(natio,artwork)
           
        

def addArtwork(catalog, artwork):
    a = newArtwork(id=artwork["ObjectID"],
    title=artwork["Title"],
    constituent_id=artwork["ConstituentID"],
    date=artwork["Date"],
    medium=artwork["Medium"],
    dimensions=artwork["Dimensions"],
    credit_line=artwork["CreditLine"],
    accession_number=artwork["AccessionNumber"],
    classification=artwork["Classification"],
    department=artwork["Department"],
    date_aquired=artwork["DateAcquired"],
    cataloged=artwork["Cataloged"],
    url=artwork["URL"],
    circumference=artwork["Circumference (cm)"],
    depth=artwork["Depth (cm)"],
    diameter=artwork["Diameter (cm)"],
    height=artwork["Height (cm)"],
    lenght=artwork["Length (cm)"],
    weight=artwork["Weight (kg)"],
    width=artwork["Width (cm)"],
    seat_height=artwork["Seat Height (cm)"],
    duration=artwork["Duration (sec.)"])
    lt.addLast(catalog['artworks'], a)
    for key in artwork:
        if artwork[key] == '':
            artwork[key] = "Unknown"

    mediums=catalog['mediums']#Crear map con indice de medio
    art_medium=artwork["Medium"]
    existMedium = mp.contains(mediums, art_medium)

    mp.put(catalog['artwork_id'],artwork['ObjectID'],artwork)

    if existMedium:
        entry = mp.get(mediums, art_medium)
        medium=me.getValue(entry)
    else:
        medium = lt.newList('ARRAY_LIST')
        mp.put(mediums , art_medium, medium)
    lt.addLast(medium,artwork)



def newMedium(art_medium):
    """
    Crea la estructura de datos que asocia las obras de arte a un medio
    'artworks' es una lista a la que se añaden todas las obras que cumplan el criterio de la llave-
    """
    entry={'Medium': "", "artworks": None}
    entry['Medium'] = art_medium
    entry["artworks"] = lt.newList('ARRAY_LIST')
    return entry

def newNationality(artist_natio):
    """
    Crea la estructura de datos que asocia las nacionalidades a un artista
    'artists' es una lista a la que se añaden todos los artistas que cumplan el criterio de la llave-
    """
    entry={'Nationality': "", "artworks": None}
    entry['Nationality'] = artist_natio
    entry["artworks"] = lt.newList('ARRAY_LIST')
    return entry

def newArtistYear(artist_year):
    """
    Crea la estructura de datos que asocia el año de nacimiento (begindate) a un artista.
    'artists' es una lista a la que se añaden todos los artistas que cumplan el criterio de la llave-
    """
    entry={'BeginDate': "", "artists": None}
    entry['BeginDate'] = artist_year
    entry["artists"] = lt.newList('ARRAY_LIST')
    return entry

def newArtistId(artist_id):
    """
    Crea la estructura de datos que asocia el id de un artista a su informacion.
    'artists' es una lista a la que se añaden todos los artistas que cumplan el criterio de la llave-
    """
    entry={'Id': "", "artists": None}
    entry['Id'] = artist_id
    entry["artists"] = lt.newList('ARRAY_LIST')
    return entry
# ==============================
# Funciones de Comparacion
# ==============================

def compareArtistsIds(id1,id2):
    """
    Compara dos Ids de artistas 
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareArtworkMedium(keyname,medium):
    """
    Compara dos medios de las obras
    """
    authentry = me.getKey(medium)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareArtistNatio(keyname,nationality):
    """
    Compara dos nacionalidades de los artistas
    """
    authentry = me.getKey(nationality)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareArtistDate(keyname,beginDate):
    """
    Compara dos años de nacimiento de los artistas
    """
    authentry = me.getKey(beginDate)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareArtistId(keyname,id):
    authentry = me.getKey(id)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareArtworkId(keyname,id):
    authentry = me.getKey(id)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def cmpArtworksByDates(artist1,artist2):
    return int(artist1["Date"]) < int(artist2["Date"])

def cmpTotalNationalities(natio1,natio2):
    return natio1["Artworks"]>natio2["Artworks"]  #Mayor a menor 
# Funciones para creacion de datos
def textToDate(text):
    if text!="Unknown":
        date=text.split("-")
        date=dt.date(int(date[0]),int(date[1]),int(date[2]))
        return date
    else:
        return dt.date(1,1,1)
# Funciones de consulta 

def getOldestByMedium(catalog,medium, display): 
    mediums_map=catalog['mediums']
    artworks=mp.get(mediums_map,medium)['value']['artworks']
    ms.sort(artworks, cmpArtworksByDates)
    oldest=lt.subList(artworks,1,display)
    return oldest

def cronologicalArtists(catalog,first,last):
    
    matchingArtists=lt.newList('ARRAY_LIST')
    while first<=last:
        date=str(first)
        pair=mp.get(catalog['years'],date)
        artists=me.getValue(pair)['artists']
        for a in lt.iterator(artists):
            lt.addLast(matchingArtists,a)    
        first+=1
    ms.sort(matchingArtists, cmpArtistByDate)
    joined=lt.newList(datastructure="ARRAY_LIST")
    first=lt.subList(matchingArtists,1,3)
    last=lt.subList(matchingArtists,lt.size(matchingArtists)-3,3)
    for i in lt.iterator(first):
        lt.addLast(joined,i)
    for n in lt.iterator(last):
        lt.addLast(joined,n)
    return lt.size(matchingArtists), joined

def getTotalNationalities(catalog,nationality):
    natio=me.getValue(mp.get(catalog['nationality'],nationality))
    natio_size=lt.size(natio)
    return natio_size

def sortByNationality(catalog):
    """
    La funcion cuenta las obras de arte de cada nacionalidad (con repetecion y obras unicas) y saca las 3 
    primeras y ultimas obras consiguiendo tambien el nombre de sus respectivos artistas.
    
    - Returns
    sorted_nationalities: ArrayList ordenado descendentemente con nacionalidad : cantidad de obras de la nacionalidad
    unique_artworks: ArrayList que contiene todas las artworks de la top nacionalidad sin repeticiones (Obras unicas)
    joined: ArrayList de las 3 primeras y ultimas obras de arte con el nombre de sus autores agregados
    """
    list_of_nationalities=lt.newList(datastructure="ARRAY_LIST")
    natio_map=catalog['nationality']
    keys=mp.keySet(natio_map)  

    for natio in lt.iterator(keys):
        size=int(lt.size(mp.get(natio_map,natio)['value']))#Esta primera parte la puedo hacer en el modelo 
        lt.addLast(list_of_nationalities, {"nationality":natio,"Artworks":size})
    sorted_nationalities=ms.sort(list_of_nationalities,cmpTotalNationalities)

    top=lt.getElement(sorted_nationalities,1)["nationality"]
    top_nationality_artwork= mp.get(natio_map,top)['value']
    unique_artworks=lt.newList(datastructure="ARRAY_LIST")
    artworkID=None
    for artwork in lt.iterator(top_nationality_artwork):
        if artwork['id']!=artworkID:
            lt.addLast(unique_artworks,artwork)
            artworkID=artwork['id']
    
    joined=lt.newList(datastructure="ARRAY_LIST")
    first=lt.subList(unique_artworks,1,3)
    last=lt.subList(unique_artworks,lt.size(unique_artworks)-3,3)
    for i in lt.iterator(first):
        lt.addLast(joined,i)
    for n in lt.iterator(last):
        lt.addLast(joined,n) 
    #Se sacan los primeros y ultimos tres a un array aparte
    
    addArtworkArtists(joined,catalog['artist_id'])
    
    return sorted_nationalities,unique_artworks, joined

def addArtworkArtists(artworks,artists_map):
    """
    Añade al array artworks los nombres de los artistas para cada obra
    """
    for artwork in lt.iterator(artworks):
        names=[]
        code=artwork["constituent_id"]
        code=code[1:-1].replace(" ","").split(",")
        for artist_id in code:
            names.append(mp.get(artists_map,artist_id)['value']['DisplayName'])
        artwork["Names"]=names
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def cmpArtistByDate(artist1, artist2)->bool: 
    """ 
    Devuelve verdadero (True) si el 'DateAcquired' de artwork1 es menores que el de 
    artwork2 
    Args: 
        artwork1: informacion de la primera obra que incluye su valor 'DateAcquired' 
        artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired' 
    """
    return artist1["BeginDate"] < artist2["BeginDate"]