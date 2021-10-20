import model.misc as misc
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import mergesort as ms

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
        size=int(lt.size(mp.get(natio_map,natio)['value']))#Saca el tamaña de cada nacionalidad
        lt.addLast(list_of_nationalities, {"nationality":natio,"Artworks":size})
    sorted_nationalities=ms.sort(list_of_nationalities, lambda natio1, natio2: natio1["Artworks"]>natio2["Artworks"])

    top=lt.getElement(sorted_nationalities,1)["nationality"]
    top_nationality_artwork= mp.get(natio_map,top)['value'] #Saca todas las obras que estan bajo la nacionaldiad mas alta
    unique_artworks=lt.newList(datastructure="ARRAY_LIST")
    artworkID=None
    for artwork in lt.iterator(top_nationality_artwork): #Este loop es para quitar repeteciones de obras de artes 
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
    
    return sorted_nationalities,unique_artworks, joined