from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt

def cronologicalArtists(catalog,first,last):
    
    matchingArtists=lt.newList("ARRAY_LIST")
    while first<=last:
        if mp.contains(catalog['years'], first):
            artists=me.getValue(mp.get(catalog['years'], first))
            for a in lt.iterator(artists): #Recorre el bucket dentro de el valor (Maximo 4 elementos)
                lt.addLast(matchingArtists,a)
        first+=1
    
    joined=lt.newList(datastructure="ARRAY_LIST")
    last=lt.subList(matchingArtists,lt.size(matchingArtists)-2,3)
    first=lt.subList(matchingArtists,1,3)
    for i in lt.iterator(first):
        lt.addLast(joined,i)
    for n in lt.iterator(last):
        lt.addLast(joined,n)
    return lt.size(matchingArtists), joined