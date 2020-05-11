#!/usr/bin/env python
# -*- coding: utf-8 -*-

# o	Function GET
# http://XX.XX.XX.XX:8080/get/q=<int:nb_street>+<road_name>+<int:postal_code>+<city_name>
# example: http://localhost:8080/get/API/q=2+rue+galvani+91300+Massy

from flask import Flask, request, jsonify
import json, os
import pandas as pd
import math


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from getAdress import getInfo
from networkInformation import NetworkInformation


# data = pd.read_csv("db_operator.csv", sep=',') # Coverage network data 

# API creation

app=Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)

#init ma
ma = Marshmallow(app)

#NetworkCoverage Class/Model
class NetworkCoverage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    op = db.Column(db.Integer)

    lon = db.Column(db.Float)
    lat = db.Column(db.Float)

    _2G = db.Column(db.Boolean)
    _3G = db.Column(db.Boolean)
    _4G = db.Column(db.Boolean)

    city = db.Column(db.String(100))

    def __init__(self, op, lon, lat, _2g, _3g, _4g, city):
        self.op = op
        self.lon = lon
        self.lat = lat
        self._2G = _2g
        self._3G = _3g
        self._4G = _4g
        self.city = city

# NetworkCoverage Schema
class NetworkCoverageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'op', 'lon', 'lat', '2g', '3g', '4g', 'city')

#Init schema
network_coverage_schema = NetworkCoverageSchema()
network_coverages_schema = NetworkCoverageSchema(many=True)

# rooting

@app.route("/")
def hello():
    return "Welcolme to France network coverage API, you can add a request to the url to get information of the network coverage. \n \
        For instance : http://localhost:8080/get/API/q=2+rue+galvani+91300+Massy"


@app.route("/get/q=<int:nb_street>+<road_name>+<int:postal_code>+<city_name>", methods=['GET'])
def GET(nb_street, road_name, postal_code, city_name):

    try :
        # the fisrt caracter of the city name needs to be a capital letter
        city_first = str.upper(city_name[0])
        city = city_first+city_name[1:]

        #response initialisation
        reponse = NetworkInformation()

        adresse = {'nb':nb_street,
                'street': road_name,
                'ZIP': postal_code,
                'city': city}
        
        # getting GPS coordonates of the adress

        info = getInfo(adresse)

        reponse.setCor([info['geometry']['coordinates'][0],info['geometry']['coordinates'][1]])

        # getting coverage network data of the city

        ncs = NetworkCoverage.query.filter(NetworkCoverage.city == city)

        # running through the different coverage network datas of the city

        for row in ncs:

            if row.op == 20801 :
                ope = "ORANGE"
            elif row.op == 20810 :
                ope = "SFR"
            elif row.op == 20815 :
                ope = "FREE"
            else :
                ope = "BOUYGUE"

            inf = {'2G':row._2G, '3G':row._4G, '4G':row._3G}


            # getting the closest data of coverage network by calculating the distance between the adress indicated and the coordonates of the data

            if reponse.getDistance()[ope] == None :

                x = (row.lon - info['geometry']['coordinates'][0])*math.cos((row.lat+info['geometry']['coordinates'][0])/2)
                y = row.lon-info['geometry']['coordinates'][0]
                z = math.sqrt(x*x+y*y)
                d = 1.852*60*z # km conversion
                if d < 50 :  # if two different cities have the same name
                    reponse.setDistance(ope, d)
                    reponse.setInfo(inf)
                    reponse.addInfo(row.op)
            else :
                x = (row.lon - info['geometry']['coordinates'][0])*math.cos((row.lat+info['geometry']['coordinates'][0])/2)
                y = row.lon-info['geometry']['coordinates'][0]
                z = math.sqrt(x*x+y*y)
                d = 1.852*60*z  # km conversion
                if d < 50 :  # if two different cities have the same name
                    if d < reponse.getDistance()[ope] :
                        reponse.setDistance(ope, d)
                        reponse.setInfo(inf)
                        reponse.addInfo(row.op)      

        # returning the info sought

        return jsonify(reponse.getDict())

    except Exception as e :
        return "The adress doesn't exist, please check the city name or the city code"



# test of the sqlite db

@app.route('/getSome/<city>', methods=['GET'])
def getSomeNetworkCoverages(city):
    ncs = NetworkCoverage.query.filter(NetworkCoverage.city == city)
    for row in ncs:
       print ("ID:", row.id, "Ope: ",row.op, "lon:",row.lon, "lat:",row.lat)
    return "hello"

@app.route('/getAll', methods=['GET'])
def getNetworkCoverages():
    all = NetworkCoverage.query.all()
    result = network_coverages_schema.dump(all)
    return jsonify(result)

@app.route('/get/<int:id>', methods=['GET'])
def get(id):
    nc = NetworkCoverage.query.get(id)
    return network_coverage_schema.jsonify(nc)

@app.route('/post/<int:id>', methods=['POST'])
def post(id):
    op = op.json['op']
    lon = lon.json['lon']
    lat = lat.json['lat']
    _2G = _2g.json['2G']
    _3G = _3g.json['3G']
    _4G = _4g.json['4G']
    city = city.json['city']

    new_nc = NetworkCoverage(op, lon, lat, _2G, _3G, _4G, city)

    db.session.add(new_nc)
    db.session.commit()

    return network_coverage_schema.jsonify(new_nc)

@app.route('/del/<int:id>', methods=['DELETE'])
def delete(id):
    nc = NetworkCoverage.query.get(id)
    db.session.delete(p)
    db.session.commit()
    return network_coverage_schema.jsonify(nc)

# run API

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
 

