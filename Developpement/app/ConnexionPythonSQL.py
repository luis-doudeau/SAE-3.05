from sqlite3 import DatabaseError
from statistics import quantiles
import sqlalchemy
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy import Column , Integer, Text , Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Exposant import Exposant
from Consommateur import Consommateur
from Personne import Personne
from Staff import Staff
from Intervenant import Intervenant
from Auteur import Auteur
from Presse import Presse
from Invite import Invite

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

connexion ,engine = ouvrir_connexion("charpentier","charpentier",'servinfo-mariadb', "DBcharpentier")
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

def ajoute_exposant(session, exposant):
    exposantE = session.query(Exposant).filter(Exposant.idP == exposant.idP).first()
    if exposantE is None:
        personne = session.query(Personne).filter(Personne.idP == exposant.idP).first()
        session.add(exposant)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) exposant(e)")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Un exposant a déjà cet identifiant dans la base de donnée")

def ajoute_staff(session, staff):
    staffS = session.query(Staff).filter(Staff.idP == staff.idP).first()
    if staffS is None:
        personne = session.query(Personne).filter(Personne.idP == staff.idP).first()
        session.add(staff)
        try:
            print(staff)
            print(personne)
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) staff")
        except:
            print("Erreur")
    else:
        print("Un staff a déjà cet identifiant dans la base de donnée")
        
def ajoute_intervenant(session, intervenant):
    intervenantI = session.query(Intervenant).filter(Intervenant.idP == intervenant.idP).first()
    if intervenantI is None:
        personne = session.query(Personne).filter(Personne.idP == intervenant.idP).first()
        session.add(intervenant)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) intervenant(e)")
        except:
            print("Erreur")
    else:
        print("Un intervenant a déjà cet identifiant dans la base de donnée")
    
def ajoute_auteur(session, auteur):
    auteurA = session.query(Auteur).filter(Auteur.idP == auteur.idP).first()
    if auteurA is None:
        personne = session.query(Personne).filter(Personne.idP == auteur.idP).first()
        session.add(auteur)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) auteur / autrice")
        except:
            print("Erreur")
    else:
        print("Un auteur a déjà cet identifiant dans la base de donnée")

def ajoute_presse(session, presse):
    presseP = session.query(Presse).filter(Presse.idP == presse.idP).first()
    if presseP is None:
        personne = session.query(Personne).filter(Personne.idP == presse.idP).first()
        session.add(presse)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu membre de la presse")
        except:
            print("Erreur")
    else:
        print("Une personne de la presse a déjà cet identifiant dans la base de donnée")

def ajoute_invite(session, invite):
    inviteI = session.query(Invite).filter(Invite.idP == invite.idP).first()
    if inviteI is None:
        personne = session.query(Personne).filter(Personne.idP == invite.idP).first()
        session.add(invite)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) invité(e)")
        except:
            print("Erreur")
    else:
        print("Un invité a déjà cet identifiant dans la base de donnée")
        
def ajoute_participant(session, participant, role):
    ajoute_personne(session, participant)
    if role == "Exposant":
        ajoute_exposant(session, participant)
    else:
        ajoute_Consommateur(session, participant)
        if role == "Staff":
            ajoute_staff(session, participant)
        else:
            ajoute_intervenant(session, participant)
            if role == "Auteur":
                ajoute_auteur(session, participant)
            elif role == "Presse":
                ajoute_presse(session, participant)
            else:
                ajoute_invite(session, participant)
    
def get_info_personne(session, email, mdp):
    personne = session.query(Personne).filter(Personne.emailP == email).filter(Personne.mdpP == mdp).first()
    if personne is None:
        return False
    else:
        return (True, personne)

    
                

#ajoute_personne(session, Personne(get_max_id_Personne(session)+1, "a", "a", "2003-08-18", "0607080911", "maxym.charpentier@gmail.com", "A", "aucune", "Voiture"))
#ajoute_Consommateur(session, Consommateur(2))
# ajoute_exposant(session, Exposant(1, 1))
#ajoute_staff(session, Staff(2))
#ajoute_intervenant(session, Intervenant(2, "2020-03-03 12:00:00", "2020-03-03 13:00:00", "voiture", "aucune"))
#ajoute_auteur(session, Auteur(2, 1))
#ajoute_presse(session, Presse(2))
#ajoute_invite(session, Invite(2))
#ajoute_participant(session, Exposant(8, 1), "Exposant")

print(get_info_personne(session, "lenny@gmail.com", "le"))



