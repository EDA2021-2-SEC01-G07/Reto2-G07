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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtist(catalog)
    loadArtWork(catalog)
    
    
def loadArtist(catalog):
    """
    Carga la información que asocia tags con libros.
    """
    artistfiles = cf.data_dir + 'Artists-utf8-small.csv'
    input_file = csv.DictReader(open(artistfiles, encoding='utf-8'))
    for authors in input_file:
        model.addArtist(catalog, authors)


def loadArtWork(catalog):
    """
    Carga la información que asocia tags con libros.
    """
    artfiles = cf.data_dir + 'Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(artfiles, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)

def getOldestByMedium(catalog,medium, display):
    return model.getOldestByMedium(catalog,medium, display)
# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def cronologicalArtists(catalog,first,last):
    return model.cronologicalArtists(catalog,first,last)