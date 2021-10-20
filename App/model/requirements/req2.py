from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as ms
import model.misc as misc

def cronologicalArtwork(catalog, begin_date, end_date):

    begin, end = misc.textToDate(begin_date), misc.textToDate(end_date)

    artworks = lt.newList("ARRAY_LIST")
    purchased = 0

    for artwork in lt.iterator(catalog["artworks"]):
        if artwork["date_aquired"] == "Unknown":
            continue
        date = misc.textToDate(artwork["date_aquired"])
        if date >= begin and date <= end:
            lt.addLast(artworks,artwork)
            if "purchase" in artwork["credit_line"].lower():
                purchased+=1
    
    ms.sort(artworks, lambda artwork1, artwork2:
     misc.textToDate(artwork1["date_aquired"]) < misc.textToDate(artwork2["date_aquired"]))
    
    total = lt.newList("ARRAY_LIST")

    total = lt.subList(artworks, 1, 3)
    last = lt.subList(artworks, lt.size(artworks)-2, 3)

    for artwork in lt.iterator(last):
        lt.addLast(total, artwork)
    return total, lt.size(artworks), purchased
