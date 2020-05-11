# Paperneast---Network-Coverage-API

Voici le rendu de l'exercice demandé. A partir d'une requête contenant une adresse, l'API renvoi
la couverture réseau 2G/3G/4G pour chaque opérateur si elle est disponible.

L'API tourne en local avec le port 8080. Les requêtes doivent se présenter sous la forme : 

http://localhost:8080/get/q=<int:nb_street>+<road_name>+<int:postal_code>+<city_name>

Voici un exemple de requête : http://localhost:8080/get/q=2+rue+galvani+91300+Massy

et sa réponse :

{
    "BOUYGUE": {
        "2G": true,
        "3G": true,
        "4G": true
    },
    "FREE": {
        "2G": false,
        "3G": true,
        "4G": true
    },
    "ORANGE": {
        "2G": false,
        "3G": false,
        "4G": false
    },
    "SFR": {
        "2G": true,
        "3G": true,
        "4G": true
    }
}

J'ai modifié le fichier csv initial contenant les différentes couvertures réseaux (dbModification.py). 

J'ai converti les coordonnées Lambert93 en coordonnées GPS et renseigné la ville rattachée à l'aide des api :
  - https://api-adresse.data.gouv.fr
  - http://open.mapquestapi.com 
  
J'ai ensuite créé un base sqlite utilisée par l'API (createDB.py). La base créée contenant plusieurs coordonnées par ville (et des villes homonymes), 
lors d'une requête, la distance entre les coordonnées de l'adresse et de celles de la base données ayant la même ville est calculé, puis l'API 
retourne les informations de couvertures la plus proche pour chaque opérateur si elle est disponible.

L'API a été développée en python 3.8.1.

J'ai utilisé les frameworks suivant : 
  - flask 
  - flask-sqlalchemy
  - pandas 
  - flask-marshmallow
  - pyproj 
  - marshmallow-sqlalchemy

# Run Server (http://localhst:8080)
python app.py

