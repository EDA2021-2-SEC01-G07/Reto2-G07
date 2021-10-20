from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.DataStructures import mapentry as me

def techiniquesFromArtist(catalog, artist_name):

    returned_values = mp.newMap()

    medium_map = mp.newMap()

    artist = me.getValue(mp.get(catalog["artist_name"], artist_name))
    keyval = lt.newList("ARRAY_LIST")
    total_ammount = 0

    for artwork in lt.iterator(catalog["artworks"]):
        if artist_name in artwork["names"]:
            array = None
            medium = artwork["medium"]
            if mp.contains(medium_map, medium):
                array = me.getValue(mp.get(medium_map, medium))
            else:
                array = lt.newList("ARRAY_LIST")
                mp.put(medium_map, medium, array)
            lt.addLast(array, artwork)
            total_ammount += 1
        
    for key in lt.iterator(mp.keySet(medium_map)):
        lt.addLast(keyval, mp.get(medium_map, key))

    ms.sort(keyval, lambda keyval1, keyval2:
    lt.size(me.getValue(keyval1)) > lt.size(me.getValue(keyval2)))

    most_used = me.getKey(lt.getElement(keyval, 1))

    mp.put(returned_values, "id", artist["id"])
    mp.put(returned_values, "total_artworks", total_ammount)
    mp.put(returned_values, "most_used", most_used)
    mp.put(returned_values, "ranking_list", keyval)

    return returned_values

