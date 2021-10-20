from DISClib.DataStructures import mapentry as me

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

def compareArtworkDep(keyname,department):
    authentry = me.getKey(department)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1