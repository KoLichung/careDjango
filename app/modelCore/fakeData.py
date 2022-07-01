import csv
import os
import datetime 
from .models import  User, City, County

def importCityCounty():
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'county.csv')

    file = open(file_path)
    reader = csv.reader(file, delimiter=',')
    for index, row in enumerate(reader):
        if index != 0:
            if City.objects.filter(name=row[0]).count()==0:
                city = City()
                city.name = row[0]
                city.save()
            else:
                city = City.objects.get(name=row[0])

            county_name = row[2].replace(row[0],'')
            county = County()
            county.city = city
            county.name = county_name
            county.save()
            print(city.name + " " + county.name)
            
def fakeData():
    user = User()
    user.name = 'user01'
    user.phone = '0915323131'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'user02'
    user.phone = '0985463816'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'user03'
    user.phone = '0985463888'
    user.is_active = True
    user.is_staff =  False
    user.is_servant = True
    user.save()
