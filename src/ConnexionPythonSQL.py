from sqlite3 import DatabaseError
from statistics import quantiles
import sqlalchemy
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy import Column , Integer, Text , Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

# pour avoir sqlalchemy :
# sudo apt-get update 
# sudo apt-get install python3-sqlalchemy
# pip3 install mysql-connector-python

def ouvrir_connexion(user,passwd,host,database):
    """
    ouverture d'une connexion MySQL
    paramètres:
       user     (str) le login MySQL de l'utilsateur
       passwd   (str) le mot de passe MySQL de l'utilisateur
       host     (str) le nom ou l'adresse IP de la machine hébergeant le serveur MySQL
       database (str) le nom de la base de données à utiliser
    résultat: l'objet qui gère le connection MySQL si tout s'est bien passé
    """
    try:
        #creation de l'objet gérant les interactions avec le serveur de BD
        engine=sqlalchemy.create_engine('mysql+mysqlconnector://'+user+':'+passwd+'@'+host+'/'+database)
        #creation de la connexion
        cnx = engine.connect()
    except Exception as err:
        print(err)
        raise err
    print("connexion réussie")
    return cnx,engine

connexion ,engine = ouvrir_connexion("nardi","nardi","servinfo-mariadb", "DBnardi")
# if __name__ == "__main__":
#     login=input("login MySQL ")
#     passwd=getpass.getpass("mot de passe MySQL ")
#     serveur=input("serveur MySQL ")
#     bd=input("nom de la base de données ")
#     cnx=ouvrir_connexion(login,passwd,serveur,bd)
#     # ici l'appel des procédures et fonctions
#     cnx.close()
Session = sessionmaker(bind=engine)
session = Session()