#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json 
import requests

# initialisation of the request

api_token = ''
api_url_base = 'https://api-adresse.data.gouv.fr/search/?q='

#https://api-adresse.data.gouv.fr/search/?q=lat=48.789&lon=2.789

headers = {'Content-Type': 'application/json',
          'Authorization': 'Bearer {0}'.format(api_token)}

# getting information about an adress

def getInfo(adresse):
    
    api_url = '{0}{1}+{2}&postcode={3}'.format(api_url_base, adresse['nb'], adresse['street'], adresse['ZIP'])

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200 :
        for i in json.loads(response.content.decode('utf-8'))['features']:
            if i['properties']['city'] == adresse['city'] :
                return i
        return None
    else:
        return None

# test 
# adresse = {'nb':58,
#             'street': "rue+du+général+leclerc",
#             'ZIP': 78570,
#             'city': "Andrésy"
#         }
#
# account_info = getInfo(adresse)
# print(account_info)
 