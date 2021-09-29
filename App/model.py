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

    # """
    # Este indice crea un map cuya llave es el identificador del artista
    # """
    # catalog['artists'] = mp.newMap(10000,
    #                                maptype='CHAINING',
    #                                loadfactor=4.0,
    #                                comparefunction=compareArtistsIds)
        
    """
    Este indice crea un map cuya llave es el metodo utilizado para la obra
    """
    catalog['mediums'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtworkMedium)
    
    """
    Listas con todos los artistas y obras
    """
    catalog['artists'] = lt.newList(datastructure='ARRAY_LIST')
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

def addArtwork(catalog, artwork):
    mediums=catalog['mediums']
    
    art_medium=artwork["Medium"]

    existMedium = mp.contains(mediums, art_medium)
    if existMedium:
        entry = mp.get(mediums, art_medium)
        medium=me.getValue(entry)
    else:
        medium = newMedium(art_medium)
        mp.put(mediums , art_medium, medium)
    lt.addLast(medium["artworks"],artwork)



def newMedium(art_medium):
    """
    Crea la estructura de datos que asocia las obras de arte a un medio
    """
    entry={'Medium': "", "artworks": None}
    entry['Medium'] = art_medium
    entry["artworks"] = lt.newList('ARRAY_LIST')
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

def cmpArtworksByDates(artist1,artist2):
    return int(artist1["Date"]) < int(artist2["Date"])


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
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
