from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
import datetime as dt

def textToDate(text):
    if text!="Unknown":
        date=text.split("-")
        date=dt.date(int(date[0]),int(date[1]),int(date[2]))
        return date
    else:
        return dt.date(1,1,1)

def addArtworkArtists(artworks,artists_map):
    """
    Añade al array artworks los nombres de los artistas para cada obra
    """
    for artwork in lt.iterator(artworks):
        names=[]
        code=artwork["constituent_id"]
        for artist_id in code:
            names.append(mp.get(artists_map,artist_id)['value']['name'])
        artwork["names"]=names

def getOldestByMedium(catalog,medium,display): 
    mediums_map=catalog['mediums']
    artworks=mp.get(mediums_map,medium)['value']['artworks']
    ms.sort(artworks, lambda artist1, artist2: int(artist1["date"]) < int(artist2["date"]))
    oldest=lt.subList(artworks,1,display)
    return oldest

def getTotalNationalities(catalog,nationality):
    natio=me.getValue(mp.get(catalog['nationality'],nationality))
    natio_size=lt.size(natio)
    return natio_size
