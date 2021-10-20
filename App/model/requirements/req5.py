import config as cf
import model.misc as misc
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.DataStructures import mapentry as me
from math import pi
assert cf

def cmpDates(artwork1, artwork2)->bool: 
    if artwork1["date"]=="Unknown":
        return artwork2["date"]
    if artwork2["date"]=="Unknown":
        return artwork1["date"]
    return int(artwork1["date"]) < int(artwork2["date"])

def costFromDepartment(catalog, department):
    returned_values = mp.newMap()
    dept_to_artworks = catalog["department"]
    
    total_cost, total_weight = 0, 0
    artworks = me.getValue(mp.get(dept_to_artworks, department))

    for artwork in lt.iterator(artworks):
        if "cost" not in artwork:
            artwork["cost"] = getTransportationCost(artwork)
        total_cost += artwork["cost"]
        if artwork["weight"] != "Unknown":
            total_weight += float(artwork["weight"])

    ms.sort(artworks, lambda artwork1, artwork2: artwork1["cost"] > artwork2["cost"])
    expensive = lt.subList(artworks, 1, 5)
    mp.put(returned_values, "expensive", expensive)

    ms.sort(artworks, cmpDates)
    oldest = lt.subList(artworks, 1, 5)
    mp.put(returned_values, "oldest", oldest)

    mp.put(returned_values, "cost", total_cost)
    mp.put(returned_values, "weight", total_weight)
    mp.put(returned_values, "length", lt.size(artworks))
    
    return returned_values

def getTransportationCost(artwork):
    cost = 42
    artworks = ['width', 'height', 'lenght', 'depth']
    weight = artwork['weight']
    width, height, lenght, radius = 0, 0, 0,0
    dimensions, total = 0, 0
    unit1, unit2 = "", ""

    for unit in artworks:
        value = artwork[unit]
        if value != "0" and value !="Unknown":
            unit1 = unit
            width = float(value)
    if width != 0:
        dimensions += 1
    for unit in artworks:
        value = artwork[unit]
        if value != "0" and value !="Unknown" and unit != unit1:
            unit2 = unit
            height = float(value)
    if height != 0:
        dimensions += 1
    for unit in artworks:
        value = artwork[unit]
        if value != "0" and value !="Unknown" and unit not in (unit1, unit2):
            lenght = float(value)
            break
    if lenght != 0:
        dimensions += 1
    
    if artwork['circumference'] != "0" and artwork['circumference']!="Unknown":
        radius = float(artwork['circumference'])/2*pi
    elif artwork['diameter'] != "0" and artwork['diameter']!="Unknown":
        radius = float(artwork['diameter'])/2
    
    if radius != 0:
        dimensions += 2
    
    if dimensions == 2 or dimensions ==3:
        if bool(radius):
            total = pi * radius**2
            total/=10000
            if width != 0:
                total *= width
                total/=100
        else:
            total = width * height
            total/=10000
            if lenght != 0:
                total *= lenght
                total/=100
    
    if weight != "0" and weight!="Unknown":
        if total!=0 and total > float(weight):
            cost = total * 72
        else:
            cost = float(weight) *72
    elif total!=0:
        cost = total * 72
    
    return round(cost,3)