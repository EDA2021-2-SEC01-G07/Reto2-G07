from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
import model.compare as cmp

def newCatalog():
    """ Inicializa el catálogo de artistas

    Crea una lista vacia para guardar todos los libros

    Se crean indices (Maps) por los siguientes criterios:
    Autores
    Obras

    Retorna el catalogo inicializado.
    """

    catalog = {}

    """
    Indices creados en el catalogo por medio, nacionalidad, años de nacimiento para autores, id de artistas y obras
    """
    catalog['mediums'] = mp.newMap(5500, #5500   mp.size[mediums]/4
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=cmp.compareArtworkMedium)
    

    catalog['nationality'] = mp.newMap(15, #15   mp.size[nationality]//4
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=cmp.compareArtistNatio)

    catalog['years'] =  mp.newMap(250, #250        la diferencia entre fecha mas grande y menor/4
                                   maptype='CHAINING', 
                                   loadfactor=4,
                                   comparefunction=cmp.compareArtistDate)

    catalog['artist_id'] =  mp.newMap(3900, #3900    tamaño archivo/4
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=cmp.compareArtistId)
    
    catalog['artwork_id'] =  mp.newMap(38000, #38000   tamaño archivo/4
                                maptype='CHAINING',
                                loadfactor=4,
                                comparefunction=cmp.compareArtworkId)

    catalog['department']=  mp.newMap(23, #38000   tamaño mp.size*/0.5
                                maptype='PROBING',
                                loadfactor=0.4,
                                comparefunction=cmp.compareArtworkDep)

    catalog['artist_name']=  mp.newMap(3900, #38000   tamaño archivo/4
                                maptype='CHAINING',
                                loadfactor=4,
                                comparefunction=cmp.compareArtistName)
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
    "constituent_id": constituent_id[1:-1].replace(" ", "").split(","),
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

def addArtist(catalog, a):
    artist = newArtist(id=a["ConstituentID"],
    name=a["DisplayName"], 
    biography=a["ArtistBio"],
    nationality=a["Nationality"],
    gender=a["Gender"],
    begin_date=a["BeginDate"],
    end_date=a["EndDate"],
    wiki_id=a["Wiki QID"],
    ulan=a["ULAN"])
    lt.addLast(catalog['artists'], artist)

    mp.put(catalog['artist_id'],artist['id'], artist) #Crea el indice de artist_id, al ser unicos no se necesita ninguna lista en el valor.
    
    years=catalog['years']  #Crea un mapa con indice por años de nacimiento de los artistas
    artist_year = artist['begin_date']
    existYear = mp.contains(years,artist_year) #Valor booleano para saber si ya se creo la fecha 
    if existYear:
        year = me.getValue(mp.get(years,artist_year)) #Obtiene la lista que es el valor bajo la fecha
    else:
        year=lt.newList("ARRAY_LIST")#Crea una lista vacia
        mp.put(years,artist_year,year)# Se mete la lista bajo la llave 'fecha'
    lt.addLast(year,artist)#Añade toda la informacion del artista bajo la llave de su fecha.

    mp.put(catalog['artist_name'],artist['name'],artist)


def loadNationality(catalog):
    """
    La funcion crea el indice de nacionalidad en el catalogo
    Se recorre cada obra de arte y cada codigo de artista que esta en dicha obra.
        Si no esta se crea un ARRAYLIST 
        Si ya esta simplemente se le agrega al ARRAYLIST previamente creado.
    """
    nationalities=catalog['nationality']
    artist_map=catalog['artist_id']
    artworks=catalog['artworks']
    for artwork in lt.iterator(artworks):
        code=artwork["constituent_id"] 
        for artist_id in code:
            artist_nationality=me.getValue(mp.get(artist_map,artist_id))["nationality"]
            if artist_nationality=="" or artist_nationality =="Unknown":
                artist_nationality="Unknown"

            if mp.contains(nationalities,artist_nationality):
                entry = mp.get(nationalities,artist_nationality)
                natio = me.getValue(entry)
            else:
                natio = lt.newList('ARRAY_LIST')
                mp.put(nationalities, artist_nationality, natio) 
            
            lt.addLast(natio,artwork)

def addArtwork(catalog, a):
    artwork = newArtwork(id=a["ObjectID"],
    title=a["Title"],
    constituent_id=a["ConstituentID"],
    date=a["Date"],
    medium=a["Medium"],
    dimensions=a["Dimensions"],
    credit_line=a["CreditLine"],
    accession_number=a["AccessionNumber"],
    classification=a["Classification"],
    department=a["Department"],
    date_aquired=a["DateAcquired"],
    cataloged=a["Cataloged"],
    url=a["URL"],
    circumference=a["Circumference (cm)"],
    depth=a["Depth (cm)"],
    diameter=a["Diameter (cm)"],
    height=a["Height (cm)"],
    lenght=a["Length (cm)"],
    weight=a["Weight (kg)"],
    width=a["Width (cm)"],
    seat_height=a["Seat Height (cm)"],
    duration=a["Duration (sec.)"])

    lt.addLast(catalog['artworks'], artwork)

    mp.put(catalog['artwork_id'],artwork['id'],artwork) #Crea el indice de artwork_id, al ser unicos no se necesita ninguna lista en el valor.

    mediums=catalog['mediums']#Crear map con indice de medio
    art_medium=artwork["medium"]
    existMedium = mp.contains(mediums, art_medium)
    if existMedium:
        entry = mp.get(mediums, art_medium)
        medium=me.getValue(entry)
    else:
        medium = lt.newList('ARRAY_LIST')
        mp.put(mediums , art_medium, medium)
    lt.addLast(medium,artwork)

    departments=catalog['department']
    art_department=artwork['department']
    existDepartment = mp.contains(departments, art_department)
    if existDepartment:
        entry=mp.get(departments,art_department)
        department=me.getValue(entry)
    else:
        department=lt.newList('ARRAY_LIST')
        mp.put(departments,art_department,department)
    lt.addLast(department,artwork)