from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import mergesort as ms
import model.misc as misc

def techiniquesFromArtist(catalog, artist_name):

   technique_by_map = mp.newMap()

   artist = mp.get(catalog["artist_name"], artist_name)

   