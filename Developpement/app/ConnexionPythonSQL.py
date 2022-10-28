from logging import exception
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
from Staff import Staff
from Intervenant import Intervenant
from Auteur import Auteur
from Presse import Presse
from Invite import Invite
from Participant import Participant

# pour avoir sqlalchemy :
# sudo apt-get update 
# sudo apt-get install python3-sqlalchemy
# pip3 install mysql-connector-python
ROLE = ["Auteur", "Exposant", "Staff", "Presse", "Invite"]

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

#connexion ,engine = ouvrir_connexion("charpentier","charpentier",'servinfo-mariadb', "DBcharpentier")
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

def get_max_id_participant(session):
    max_id = session.query(func.max(Participant.idP)).first()
    if (max_id._data[0]) is None:
        return 0
    else:
        return max_id._data[0]

def get_max_num_stand(session):
    max_num = session.query(func.max(Exposant.numStand)).first()
    if (max_num._data[0]) is None:
        return 0
    else:
        return max_num._data[0]

def ajoute_particpant(session, participant):
    personneP = session.query(Participant).filter(Participant.idP == participant.idP).first()
    if personneP is None:
        participant.idP = get_max_id_participant(session) + 1
        session.add(participant)
        try:
            session.commit()
            print("La Participant "+ str(participant) +" a bien été inséré dans la base de donnée")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Une personne a déjà cet identifiant dans la base de donnée")
    
def ajoute_Consommateur(session, consommateur):
    consommateurC = session.query(Consommateur).filter(Consommateur.idP == consommateur.idP).first()
    if consommateurC is None:
        personne = session.query(Participant).filter(Participant.idP == consommateur.idP).first()
        new_consommateur = Consommateur(consommateur.idP)
        session.add(new_consommateur)
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
        personne = session.query(Participant).filter(Participant.idP == exposant.idP).first()
        new_exposant = Exposant(exposant.idP, get_max_num_stand(session) + 1)
        session.add(new_exposant)
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
        personne = session.query(Participant).filter(Participant.idP == staff.idP).first()
        new_staff = Staff(staff.idP)
        session.add(new_staff)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) staff")
        except:
            print("Erreur")
    else:
        print("Un staff a déjà cet identifiant dans la base de donnée")
        
def ajoute_intervenant(session, intervenant):
    intervenantI = session.query(Intervenant).filter(Intervenant.idP == intervenant.idP).first()
    if intervenantI is None:
        personne = session.query(Participant).filter(Participant.idP == intervenant.idP).first()
        new_intervenant = Intervenant(intervenant.idP, None, None, None, None)
        session.add(new_intervenant)
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
        personne = session.query(Participant).filter(Participant.idP == auteur.idP).first()
        new_auteur = Auteur(auteur.idP, None)
        session.add(new_auteur)
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
        personne = session.query(Participant).filter(Participant.idP == presse.idP).first()
        new_presse = Presse(presse.idP)
        session.add(new_presse)
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
        personne = session.query(Participant).filter(Participant.idP == invite.idP).first()
        new_invite = Invite(invite.idP)
        session.add(new_invite)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) invité(e)")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Un invité a déjà cet identifiant dans la base de donnée")
        
def ajoute_participant(session, participant, role):
    if role in ROLE:
        ajoute_particpant(session, participant)
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
    else:
        print("Le rôle n'est pas reconnu")
    
def get_info_personne(session, email, mdp):
    personne = session.query(Participant).filter(Participant.emailP == email).filter(Participant.mdpP == mdp).first()
    if personne is None:
        return False
    else:
        return (True, personne)

    

        
                

# ajoute_personne(session, Participant(None, "a", "a", "2003-08-18", "0607080911", "maxym.charpentier@gmail.com", "A", "aucune", "Voiture"))
# ajoute_Consommateur(session, Consommateur(1))
# ajoute_exposant(session, Exposant(1, 1))
# ajoute_staff(session, Staff(1))
# ajoute_intervenant(session, Intervenant(1, "2020-03-03 12:00:00", "2020-03-03 13:00:00", "voiture", "aucune"))
# ajoute_auteur(session, Auteur(1, 1))
# ajoute_presse(session, Presse(1))
# ajoute_invite(session, Invite(1))
# ajoute_participant(session, Participant(None, "Mathieu", "Alpha", "2003-08-18", "0606060666", "maxym.charpentier@gmail.com", "A", "aucune", "Voiture"), "a")

#print(get_info_personne(session, "lenny@gmail.com", "le"))



