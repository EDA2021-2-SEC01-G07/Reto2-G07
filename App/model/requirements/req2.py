from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import mergesort as ms
import model.misc as misc

def cronologicalArtwork(catalog, begin_date, end_date):

    returned_values = mp.newMap()
    begin, end = misc.textToDate(begin_date), misc.textToDate(end_date)

    artists = set()
    artworks = lt.newList("ARRAY_LIST")
    purchased = 0

    misc.addArtworkArtists(artworks, catalog["artist_id"])

    for artwork in lt.iterator(catalog["artworks"]):
        if artwork["date_aquired"] == "Unknown":
            continue
        date = misc.textToDate(artwork["date_aquired"])
        if date >= begin and date <= end:
            lt.addLast(artworks,artwork)
            if "purchase" in artwork["credit_line"].lower():
                purchased+=1
        artists.update(artwork["names"])
    
    ms.sort(artworks, lambda artwork1, artwork2:
     misc.textToDate(artwork1["date_aquired"]) < misc.textToDate(artwork2["date_aquired"]))
    
    total = lt.newList("ARRAY_LIST")

    total = lt.subList(artworks, 1, 3)
    last = lt.subList(artworks, lt.size(artworks)-2, 3)

    for artwork in lt.iterator(last):
        lt.addLast(total, artwork)
    
    mp.put(returned_values, "sample", total)
    mp.put(returned_values, "size", lt.size(artworks))
    mp.put(returned_values, "artists", len(artists))
    mp.put(returned_values, "purchased", purchased)

    return returned_values
