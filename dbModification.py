#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The purpose of this file convert the Lambert 93 coordonates into GSP coordonates, which 
# will be used to add a city column to the data, thanks to api-adresse.data.gouv.fr. However,
# some coordonates where missing in this API. Therefore, an other API (open.mapquestapi.com) is
# also used to fill the missing data

from pyproj import Proj, transform
import pyproj
import numpy
import pandas as pd
import requests
import json

inProj = Proj(init='epsg:2154')
outProj = Proj(init='epsg:4326')

def lambert2GPS(x1, y1):
    x2,y2 = transform(inProj,outProj,x1,y1)
    return x2,y2

# print(lambert2GPS(1233910,6162876))

# Récupération des villes avec l'API api-adresse.data.gouv.fr

api_token = ''
api_url_base = 'https://api-adresse.data.gouv.fr/reverse/?lon='

headers = {'Content-Type': 'application/json',
          'Authorization': 'Bearer {0}'.format(api_token)}

def getCity(tuple):
    
    api_url = '{0}{1}&lat={2}'.format(api_url_base, round(tuple[0],6), round(tuple[1],6))

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200 :
        if json.loads(response.content.decode('utf-8'))['features'] == [] :
            return getCity2(tuple)
        for i in json.loads(response.content.decode('utf-8'))['features']:
            return i['properties']['city']
    else:
        None

# Récupération des villes manquantes avec l'API open.mapquest

#http://open.mapquestapi.com/geocoding/v1/reverse?key=oqrtGZJWtAkwQfyOpOFPGM77w9HSgDPB&location=48.54889079852077,1.0066711412246688

api_url_base2 = 'http://open.mapquestapi.com/geocoding/v1/reverse?key=oqrtGZJWtAkwQfyOpOFPGM77w9HSgDPB&location='


def getCity2(tuple):
    
    # indice = 0 
    # print(indice)

    api_url = '{0}{1},{2}'.format(api_url_base2, tuple[1], tuple[0])

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200 :
        for i in json.loads(response.content.decode('utf-8'))['results']:
            for j in i['locations'] :
                return j['adminArea5']
    else:
        return None

data = pd.read_csv("Data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv", sep=';')

df = data.apply(lambda x: lambert2GPS(x['X'], x['Y']) , axis=1)

df2 = pd.concat([data, df], axis=1)

df2.columns = ['Opérateur', 'X', 'Y', '2G', '3G', '4G', 'GPS']

df3 = df2.apply(lambda x: getCity(x['GPS']), axis=1)

df4 = pd.concat([df2, df3], axis=1)

df4.columns = ['Opérateur', 'X', 'Y', '2G', '3G', '4G', 'GPS', 'city']

df5 = df.apply(pd.Series) # conversion du tuples GPS en deux colonnes pour éviter des problèmes de conversion en csv

df6 = pd.concat([df4, df5], axis=1)

del df6['GPS']

df6.columns = ['Opérateur', 'X', 'Y', '2G', '3G', '4G', 'city', 'x', 'y']

print(df6) 

df6.to_csv("db_operator.csv") 


 