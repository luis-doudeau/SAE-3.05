from curses import set_escdelay
from sqlite3 import DatabaseError
from statistics import quantiles
import sqlalchemy
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy import Column , Integer, Text , Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Consommateur import Consommateur
from Personne import Personne

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

def get_max_id_Personne(session):
    max_id = session.query(func.max(Personne.idP)).first()
    if (max_id._data[0]) is None:
        return 0
    else:
        return max_id._data[0]

def ajoute_personne(session, personne):
    personneP = session.query(Personne).filter(Personne.idP == personne.idP).first()
    if personneP is None:
        session.add(personne)
        try:
            session.commit()
            print("La personne "+ str(personne) +" a bien été inséré dans la base de donnée")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Une personne a déjà cet identifiant dans la base de donnée")
    
def ajoute_Consommateur(session, consommateur):
    consommateurC = session.query(Consommateur).filter(Consommateur.idP == consommateur.idP).first()
    if consommateurC is None:
        personne = session.query(Personne).filter(Personne.idP == consommateur.idP).first()
        session.add(consommateur)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) consommateur")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Un consommateur a déjà cet identifiant dans la base de donnée")

#ajoute_personne(session, Personne(get_max_id_Personne(session)+1, "a", "a", "2003-08-18", "0607080911", "maxym.charpentier@gmail.com", "A", "aucune", "Voiture"))
ajoute_Consommateur(session, Consommateur(1))
