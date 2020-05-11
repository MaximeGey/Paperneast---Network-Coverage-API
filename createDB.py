#!/usr/bin/env python
# -*- coding: utf-8 -*-

#The purpose of this file is to move the data of the csv file created to a SQlite db

from app import db, NetworkCoverage
import pandas as pd

db.create_all()

data = pd.read_csv("db_operator.csv", sep=',') # Coverage network data 

def add_network_coverage(ligne) :

    op = ligne['Opérateur']

    lon = ligne['x']
    lat = ligne['y']

    _2G = ligne['2G']
    _3G = ligne['3G']
    _4G = ligne['4G']

    city = ligne['city']

    new_network_coverage = NetworkCoverage(op, lon, lat, _2G, _3G, _4G, city)

    db.session.add(new_network_coverage)
    db.session.commit()

for i, row in data.iterrows() :

    add_network_coverage(row)
 