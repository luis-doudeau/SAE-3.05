from dataclasses import dataclass
from email.headerregistry import DateHeader
from logging import exception
import os
from shutil import register_unpack_format
from sqlite3 import DatabaseError
from statistics import quantiles
from wsgiref.validate import PartialIteratorWrapper
import sqlalchemy
from sqlalchemy import func
from sqlalchemy import create_engine, cast
from sqlalchemy import Column , Integer, Text , Date, DATETIME
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from datetime import date, datetime
import random
import string
import traceback
import sys
from sqlalchemy.sql import operators, extract
from sqlalchemy.orm import aliased

from .Exposant import Exposant
from .Intervenir import Intervenir
from .Consommateur import Consommateur
from .Staff import Staff
from .Intervenant import Intervenant
from .Auteur import Auteur
from .Presse import Presse
from .Invite import Invite
from .Intervention import Intervention
from .Participant import Participant
from .Loger import Loger
from .Hotel import Hotel
from .Deplacer import Deplacer
from .Manger import Manger
from .Lieu import Lieu
from .Repas import Repas
from .Creneau import Creneau
from .Restaurant import Restaurant
from .Avoir import Avoir
from .Regime import Regime
from .Assister import Assister
from .Secretaire import Secretaire
from .Navette import Navette
from .Transporter import Transporter
from .Travailler import Travailler
from .Voyage import Voyage
from .Mobiliser import Mobiliser
from .Transport import Transport
from .Utilisateur import Utilisateur

from .app import login_manager
# pour avoir sqlalchemy :
# sudo apt-get update 
# sudo apt-get install python3-sqlalchemy
# pip3 install mysql-connector-python
ROLE = ["Auteur", "Exposant", "Staff", "Presse", "Invite", "Secretaire", "Participant"]

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

#connexion ,engine = ouvrir_connexion("nardi","nardi",'servinfo-mariadb', "DBnardi")
#connexion ,engine = ouvrir_connexion("doudeau","doudeau",'servinfo-mariadb', "DBdoudeau")
#connexion ,engine = ouvrir_connexion("charpentier","charpentier","servinfo-mariadb", "DBcharpentier")
connexion ,engine = ouvrir_connexion("doudeau","doudeau",'servinfo-mariadb', "DBdoudeau")
#connexion ,engine = ouvrir_connexion("doudeau","doudeau","localhost", "BDBOUM")

# if __name__ == "__main__":
#     login=input("login MySQL ")
#     passwd=getpass.getpass("mot de passe MySQL ")
#     serveur=input("serveur MySQL ")
#     bd=input("nom de la base de données ")
#     cnx=ouvrir_connexion(login,passwd,serveur,bd)
#     # ici l'appel des procédures et fonctions
#     cnx.close()

Session = sessionmaker(bind=engine)
sessionSQL = Session()

def format_creneau(debut, fin):
    heuredebut = str(debut)[11:]
    heurefin = str(fin)[11:]
    return heuredebut + " - " + heurefin

def datetime_to_dateFrancais(date):
    date = str(date)[:10]
    debut_new_date = date[8:]
    fin_new_date = date[:4]
    date = date[5:]
    date = date[:2]
    return debut_new_date + "-" + date + "-" + fin_new_date 

def datetime_to_heure(date):
    new_date = str(date)
    return new_date[11:]

def get_hotel(sessionSQL, idH):
    return (sessionSQL.query(Hotel).filter(Hotel.idHotel == idH).first()).nomHotel

def get_periode_hotel(sessionSQL, idP):
    debut = (sessionSQL.query(Loger).filter(Loger.idP == idP).first()).dateDebut
    fin = (sessionSQL.query(Loger).filter(Loger.idP == idP).first()).dateFin
    return format_creneau(debut, fin)

def get_date_dormeur(sessionSQL, idP):
    dateDeb = (sessionSQL.query(Loger).filter(Loger.idP == idP).first()).dateDebut
    dateFin = (sessionSQL.query(Loger).filter(Loger.idP == idP).first()).dateFin
    return (datetime_to_dateFrancais(dateDeb), datetime_to_dateFrancais(dateFin))

def get_consommateur(sessionSQL, idP):
    return sessionSQL.query(Consommateur).filter(Consommateur.idP == idP).first()

def get_restaurant(sessionSQL, idRepas):
    idRestaurant = (sessionSQL.query(Repas).filter(Repas.idRepas == idRepas).first()).idRest
    return (sessionSQL.query(Restaurant).filter(Restaurant.idRest == idRestaurant).first()).nomRest

def get_creneau(sessionSQL, idRepas):
    idCreneau = (sessionSQL.query(Repas).filter(Repas.idRepas == idRepas).first()).idCreneau
    debut = (sessionSQL.query(Creneau).filter(Creneau.idCreneau == idCreneau).first()).dateDebut
    fin = (sessionSQL.query(Creneau).filter(Creneau.idCreneau == idCreneau).first()).dateFin
    return format_creneau(debut, fin)

def get_intervenant(sessionSQL, idP):
    return sessionSQL.query(Intervenant).filter(Intervenant.idP == idP).first()

def get_date(sessionSQL, idRepas):
    idCreneau = (sessionSQL.query(Repas).filter(Repas.idRepas == idRepas).first()).idCreneau
    debut = (sessionSQL.query(Creneau).filter(Creneau.idCreneau == idCreneau).first()).dateDebut
    return datetime_to_dateFrancais(debut)


def get_deb_voyage(sessionSQL, idVoyage):
    row = sessionSQL.query(Voyage.heureDebVoy).filter(Voyage.idVoy == idVoyage).first()
    return row[0]

def get_lieu_depart_voyage(sessionSQL, idVoyage):
    if (sessionSQL.query(Voyage).filter(Voyage.idVoy == idVoyage).first()).directionGare:
        return "Festival → Gare Blois"
    else:
        return "Gare Blois → Festival"


def get_all_lieu(session) : 
    lieux = session.query(Lieu).all()
    lieux_dict = {lieu.idLieu: lieu for lieu in lieux}
    return lieux_dict
    

# def get_max_id_utilisateur(sessionSQL):
#     max_id = sessionSQL.query(func.max(Utilisateur.idP)).first()
    
#     if (max_id[0]) is None:
#         return 0
#     else:
#         return max_id[0]
    

def get_max_id_secretaire(sessionSQL):
    max_id = sessionSQL.query(func.max(Secretaire.idP)).first()
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]
    
def get_max_id_exposant(sessionSQL):
    max_id = sessionSQL.query(func.max(Exposant.idP)).first()
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_id_auteur(sessionSQL):
    max_id = sessionSQL.query(func.max(Auteur.idP)).first()
    
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_id_invite(sessionSQL):
    max_id = sessionSQL.query(func.max(Invite.idP)).first()
    
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_id_presse(sessionSQL):
    max_id = sessionSQL.query(func.max(Presse.idP)).first()
    
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_id_staff(sessionSQL):
    max_id = sessionSQL.query(func.max(Staff.idP)).first()
    
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_num_stand(sessionSQL):
    max_num = sessionSQL.query(func.max(Exposant.numStand)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]

        
def get_max_id_repas(sessionSQL):        
    max_num = sessionSQL.query(func.max(Repas.idRepas)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]
    

def get_max_id_creneau(sessionSQL):        
    max_num = sessionSQL.query(func.max(Creneau.idCreneau)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]

def get_max_id_restaurant(sessionSQL):
    max_num = sessionSQL.query(func.max(Restaurant.idRest)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]
    
def get_info_all_participants(sessionSQL, prenomP, nomP, emailP, ddnP, role):
    participants = sessionSQL.query(Participant)
    if(prenomP != ""):
        participants = participants.filter(Participant.prenomP == prenomP)
    if(nomP != ""):
        participants = participants.filter(Participant.nomP == nomP)
    if(emailP != ""):
        participants = participants.filter(Participant.emailP == emailP)
    if(ddnP!= ""):
        jour = ddnP.split("/")[0]
        mois = ddnP.split("/")[1]
        annee = ddnP.split("/")[2]
        date = datetime.date(int(annee),int(mois),int(jour))
        participants = participants.filter(Participant.ddnP == date)
    if(role!= ""):
        participants = filtrer_par_role(role, participants)
    return participants.all()

def get_tout_dormeurs_avec_filtre(sessionSQL, prenomP, nomP, nomHotel, dateArrive, dateDeparts):
    participants = sessionSQL.query(Loger).join(Intervenant, Loger.idP == Intervenant.idP).join(Hotel, Loger.idHotel == Hotel.idHotel)
    if(prenomP != ""):
        participants = participants.filter(Intervenant.prenomP == prenomP)
    if(nomP != ""):
        participants = participants.filter(Intervenant.nomP == nomP)
    if(nomHotel != ""):
        participants = participants.filter(Hotel.nomHotel == nomHotel)
    if(dateArrive!= ""):
        jour = dateArrive.split("/")[0]
        mois = dateArrive.split("/")[1]
        annee = dateArrive.split("/")[2]
        date_jour_debut = datetime(int(annee),int(mois),int(jour), 0,0,0)
        date_jour_fin = datetime(int(annee),int(mois),int(jour), 23,59,59)
        participants = participants.filter(Loger.dateDebut >= date_jour_debut).filter(Loger.dateDebut <= date_jour_fin)
    if(dateDeparts!= ""):
        jour = dateDeparts.split("/")[0]
        mois = dateDeparts.split("/")[1]
        annee = dateDeparts.split("/")[2]
        print(jour, mois, annee)
        date_jour_debut = datetime(int(annee),int(mois),int(jour), 0,0,0)
        date_jour_fin = datetime(int(annee),int(mois),int(jour), 23,59,59)
        participants = participants.filter(Loger.dateFin >= date_jour_debut).filter(Loger.dateFin <= date_jour_fin)
    return participants.all()


def filtrer_par_role(role, participants):
    if role == "Secretaire":
        return participants.join(Secretaire, Participant.idP == Secretaire.idP)
    if role == "Exposant":
        return participants.join(Exposant, Participant.idP == Exposant.idP)
    if role == "Staff":
        return participants.join(Staff, Participant.idP == Staff.idP)
    if role == "Auteur":
        return participants.join(Auteur, Participant.idP == Auteur.idP)
    if role == "Presse":
        return participants.join(Presse, Participant.idP == Presse.idP)
    if role == "Invite":
        return participants.join(Invite, Participant.idP == Invite.idP)
        

def ajoute_secretaire(sessionSQL, idP, prenomP, nomP, emailP, mdpP): 
    secretaire = Secretaire(idP, prenomP, nomP, emailP, mdpP)
    sessionSQL.add(secretaire)
    try:
        sessionSQL.commit()
        print("La secretaire "+ str(secretaire.prenomP) +" a bien été inséré dans la base de donnée")
    except:
        print("Erreur")


def ajoute_exposant(sessionSQL, idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP):
    exposant = Exposant(idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP)
    sessionSQL.add(exposant)
    try:
        sessionSQL.commit()
    except Exception as inst:
        print(inst)
        sessionSQL.rollback()

def ajoute_staff(sessionSQL,idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP):
    staff = Staff(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP)
    personne = sessionSQL.query(Participant).filter(Participant.idP == staff.idP).first()
    sessionSQL.add(staff)
    try:
        sessionSQL.commit()
        print("La personne " + str(personne) + " est devenu un(e) staff")
    except:
        print("Erreur")
        sessionSQL.rollback()

        
def ajoute_intervenant(sessionSQL, idP):
    intervenant = Intervenant(idP)
    personne = sessionSQL.query(Participant).filter(Participant.idP == intervenant.idP).first()
    sessionSQL.add(intervenant)
    try:
        sessionSQL.commit()
        print("La personne " + str(personne) + " est devenu un(e) intervenant(e)")
    except:
        print("Erreur")
        sessionSQL.rollback()

    
def ajoute_auteur(sessionSQL, idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP): # NE MARCHE PAS TODO
    auteur = Auteur(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP)
    print("test")
    print(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP)
    print(auteur)
    sessionSQL.add(auteur)
    try:
        sessionSQL.commit()
    except Exception as inst:
        print(inst)
        sessionSQL.rollback()

def ajoute_presse(sessionSQL, idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP):
    presse = Presse(idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP)
    sessionSQL.add(presse)
    try:
        sessionSQL.commit()
    except:
        print("Erreur")
        sessionSQL.rollback()

def ajoute_invite(sessionSQL, idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP):
    invite = Invite(idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP)
    sessionSQL.add(invite)
    try:
        sessionSQL.commit()
    except:
        print("Erreur")
        sessionSQL.rollback()
        

def ajoute_participant_role(sessionSQL, prenomP, nomP, emailP, adresseP, telP, ddnP, role):
    if role in ROLE:
        mdpP = generate_password()
        if role == "Secretaire" : 
            idP = get_max_id_secretaire(sessionSQL)+1
            ajoute_secretaire(sessionSQL, idP, prenomP, nomP, emailP, mdpP )
        elif role == "Exposant":
            idP = get_max_id_exposant(sessionSQL)+1
            ajoute_exposant(sessionSQL, idP, prenomP, nomP, emailP, adresseP, ddnP, telP, role)
        elif role == "Staff":
            idP = get_max_id_staff(sessionSQL)+1
            ajoute_staff(sessionSQL, idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP)
        elif role == "Auteur":
            idP = get_max_id_auteur(sessionSQL)+1
            ajoute_auteur(sessionSQL, idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP)
        elif role == "Presse":
            idP = get_max_id_presse(sessionSQL)+1
            ajoute_presse(sessionSQL, idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP)
        elif role == "Invite" :
            idP = get_max_id_invite(sessionSQL)+1
            ajoute_invite(sessionSQL, idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP)
    else:
        print("Le rôle n'est pas reconnu")


def ajoute_intervention(session, idP, idCreneau, idLieu, idIntervention, descIntervention):
    intervenir = Intervenir(idP, idCreneau, idLieu, idIntervention, descIntervention)
    intervention = session.query(Intervenir).filter(Intervenir.idP == intervenir.idP).filter(Intervenir.idCreneau == intervenir.idCreneau).filter(Intervenir.idIntervention == idIntervention).first()
    if intervention is None:
        sessionSQL.add(intervenir)
        try:
            sessionSQL.commit()
            print("L'intervention " + str(intervenir) + " est maintenant créée !")
        except Exception as e:
            print("Une erreur est survenue :", str(e))
            print("Erreur")
            sessionSQL.rollback()
    else:
        print("Une intervention a déjà lieu à ce créneau pour cette personne")

def ajouter_navette(sessionSQL, idNavette, nomNavette, capaciteNavette):
    navette = Navette(idNavette, nomNavette, capaciteNavette)
    navette_existe = sessionSQL.query(Navette).filter(Navette.idNavette == idNavette).first()
    if navette_existe is None:
        sessionSQL.add(navette)
        try:
            sessionSQL.commit()
            print("Une nouvelle navette " + nomNavette + " a été créée")
        except:
            print("Erreur")
            sessionSQL.rollback()
    else:
        print("Une navette à déjà cet id")


#FONCTION A TESTER AVEC DES INSERTIONS
def supprimer_personne_transporter(sessionSQL, idP, idVoyage):
    liste_personne = sessionSQL.query(Transporter.idP).filter(Transporter.idVoy == idVoyage).all()
    if len(liste_personne) == 1:
        sessionSQL.query(Transporter).filter(Transporter.idP == idP).filter(Transporter.idVoy == idVoyage).delete()
        sessionSQL.query(Voyage).filter(Voyage.idVoy == idVoyage).delete()
        sessionSQL.query(Mobiliser).filter(Mobiliser.idVoy == idVoyage).delete()
        sessionSQL.commit()
        print("Le transport a été supprimé car cette personne était seul dans ce voyage")
    else:
        sessionSQL.query(Transporter).filter(Transporter.idP == idP).filter(Transporter.idVoy == idVoyage).delete()
        sessionSQL.commit()
        print("Cette personne a bien été supprimé du voyage")


# ajoute_intervention(sessionSQL, 300, 1, 1, "Dédicace", "Séance de dédicace avec les spectateurs")
        
def supprimer_utilisateur(sessionSQL, id_utilisateur):
    sessionSQL.query(Utilisateur).filter(Utilisateur.idP == id_utilisateur).delete()
    sessionSQL.commit()
    print("L'utilisateur' a été supprimé")

def supprimer_secretaire(sessionSQL, id_secretaire):
    sessionSQL.query(Secretaire).filter(Secretaire.idP == id_secretaire).delete()
    sessionSQL.commit()
    print("La secretaire a été supprimé")

def supprimer_participant(sessionSQL, id_participant):
    sessionSQL.query(Participant).filter(Participant.idP == id_participant).delete()
    sessionSQL.commit()
    print("Le participant a été supprimé")

def supprimer_consommateur(sessionSQL, id_consommateur):
    sessionSQL.query(Manger).filter(Manger.idP == id_consommateur).delete()
    sessionSQL.query(Avoir).filter(Avoir.idP == id_consommateur).delete()
    sessionSQL.commit()

    sessionSQL.query(Consommateur).filter(Consommateur.idP == id_consommateur).delete()
    sessionSQL.commit()
    print("Le consommateur a été supprimé")

def supprimer_intervenant(sessionSQL, id_intervenant):
    sessionSQL.query(Transporter).filter(Transporter.idP == id_intervenant).delete()
    sessionSQL.query(Deplacer).filter(Deplacer.idP == id_intervenant).delete()
    sessionSQL.query(Assister).filter(Assister.idP == id_intervenant).delete()
    sessionSQL.query(Loger).filter(Loger.idP == id_intervenant).delete()
    sessionSQL.commit()

    sessionSQL.query(Intervenant).filter(Intervenant.idP == id_intervenant).delete()
    sessionSQL.commit()
    print("L'intervenant a été supprimé")

def supprimer_exposant(sessionSQL, id_exposant):
    sessionSQL.query(Exposant).filter(Exposant.idP == id_exposant).delete()
    sessionSQL.commit()
    print("L'exposant a été supprimé")
  
def supprimer_staff(sessionSQL, id_staff):
    sessionSQL.query(Travailler).filter(Travailler.idP == id_staff).delete()
    sessionSQL.commit()

    sessionSQL.query(Staff).filter(Staff.idP == id_staff).delete()
    sessionSQL.commit()
    print("Le staff a été supprimé")

def supprimer_auteur(sessionSQL, id_auteur):
    sessionSQL.query(Intervenir).filter(Intervenir.idP == id_auteur).delete()
    sessionSQL.commit()
    sessionSQL.query(Auteur).filter(Auteur.idP == id_auteur).delete()
    sessionSQL.commit()
    print("L'auteur a été supprimé")

def supprimer_presse(sessionSQL, id_presse):
    sessionSQL.query(Presse).filter(Presse.idP == id_presse).delete()
    sessionSQL.commit()
    print("Le membre de la presse a été supprimé")

def supprimer_invite(sessionSQL, id_invite):
    sessionSQL.query(Invite).filter(Invite.idP == id_invite).delete()
    sessionSQL.commit()        
    print("L'invité a été supprimé")


def get_role(sessionSQL, id_utilisateur):
    utilisateur_existe = get_utilisateur(sessionSQL, id_utilisateur)
    if utilisateur_existe is None:
        return None
    secretaire = get_secretaire(sessionSQL, id_utilisateur)
    if secretaire is not None:
        return "Secretaire"
    exposant = get_exposant(sessionSQL, id_utilisateur)
    if exposant is not None:
        return "Exposant"
    staff = get_staff(sessionSQL, id_utilisateur)
    if staff is not None:
        return "Staff"
    auteur = get_auteur(sessionSQL, id_utilisateur)
    if auteur is not None:
        return "Auteur"
    presse = get_presse(sessionSQL, id_utilisateur)
    if presse is not None:
        return "Presse"
    invite = get_invite(sessionSQL, id_utilisateur)
    if invite is not None:
        return "Invite"
    return "Pas de rôle"



def supprimer_utilisateur_role(sessionSQL, id_utilisateur):
    role_utilisateur = get_role(sessionSQL, id_utilisateur)
    if role_utilisateur is not None:
        if role_utilisateur == "Secretaire":
            supprimer_secretaire(sessionSQL, id_utilisateur)
        else:
            if role_utilisateur == "Exposant":
                supprimer_exposant(sessionSQL, id_utilisateur)
            else:
                if role_utilisateur == "Staff":
                    supprimer_staff(sessionSQL, id_utilisateur)
                else:
                    if role_utilisateur == "Auteur":
                        supprimer_auteur(sessionSQL, id_utilisateur)
                    elif role_utilisateur == "Presse":
                        supprimer_presse(sessionSQL, id_utilisateur)
                    elif role_utilisateur == "Invite":
                        supprimer_invite(sessionSQL, id_utilisateur)
                    supprimer_intervenant(sessionSQL, id_utilisateur)
                supprimer_consommateur(sessionSQL, id_utilisateur)
            supprimer_participant(sessionSQL, id_utilisateur)
        supprimer_utilisateur(sessionSQL, id_utilisateur)
    else:
        print("La personne que vous voulez supprimer n'existe pas")

     
def modifier_participant(sessionSQL, idP, adresseP, ddnP, telP):
    sessionSQL.query(Participant).filter(Participant.idP == idP).update(
        {Participant.adresseP : adresseP, Participant.ddnP : ddnP, Participant.telP : telP})
    sessionSQL.commit()
    print("Le participant a bien été modifié")
    
    
def modifier_utilisateur(sessionSQL, idP, prenomP, nomP, emailP):
    sessionSQL.query(Utilisateur).filter(Utilisateur.idP == idP).update(
        {Utilisateur.prenomP : prenomP, Utilisateur.nomP : nomP, Utilisateur.emailP : emailP})
    sessionSQL.commit()
    print("L'utilisateur a bien été modifié")

def modifier_participant_tout(sessionSQL, idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques):
    sessionSQL.query(Participant).filter(Participant.idP == idP).update(
        {Participant.prenomP : prenomP, Participant.nomP : nomP, Participant.ddnP : ddnP, 
         Participant.telP : telP, Participant.emailP : emailP, Participant.adresseP : adresseP, Participant.mdpP : mdpP,
         Participant.invite : invite, Participant.emailEnvoye : emailEnvoye, Participant.remarques : remarques})
    sessionSQL.commit()
    print("Le participant a bien été modifié")
   

# def modifier_participant_role(sessionSQL, idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques, metier):
#     participant = Participant(idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques)
#     ancien_participant = Participant(participant.idP, participant.prenomP, participant.nomP, participant.ddnP, participant.telP, participant.emailP, participant.mdpP, participant.remarques, participant.invite, participant.emailEnvoye)
#     supprimer_utilisateur_role(sessionSQL, participant.idP)
#     ajoute_participant_role_id(sessionSQL, ancien_participant, metier)
#     print("Le role du participant a bien été modifié")

def modif_loger(sessionSQL, ancien_loger, nouveau_loger):
    sessionSQL.query(Loger).filter(Loger.idP == ancien_loger.idP).filter(Loger.idHotel == ancien_loger.idHotel).filter(Loger.dateDebut == ancien_loger.dateDebut).update({
        Loger.dateDebut : nouveau_loger.dateDebut, Loger.dateFin : nouveau_loger.dateFin, Loger.idHotel : nouveau_loger.idHotel})
    sessionSQL.commit()
    print("Le logement de cette personne a bien été modifié")  
          

def modif_repas(sessionSQL, ancien_repas, nouveau_repas):
    sessionSQL.query(Manger).filter(Manger.idP == ancien_repas.idP).filter(Manger.idRepas == ancien_repas.idRepas).update(
        {Manger.idRepas : nouveau_repas.idRepas}
    )
    sessionSQL.commit()
    print("Le repas du participant a bien été modifié")     

def get_info_personne(sessionSQL, email, mdp):
    personne = sessionSQL.query(Participant).filter(Participant.emailP == email).filter(Participant.mdpP == mdp).first()
    if personne is None:
        return None
    else:
        return personne

def get_participant(sessionSQL, id_participant):
    return sessionSQL.query(Participant).filter(Participant.idP == id_participant).first()

def get_exposant(sessionSQL, id_exposant):
    return sessionSQL.query(Exposant).filter(Exposant.idP == id_exposant).first()

def get_all_auteur(session):
    Auteur_alias = aliased(Auteur)
    liste_auteur = session.query(Auteur_alias).join(Participant, Auteur_alias.idP==Participant.idP).all()
    return {auteur.idP : auteur for auteur in liste_auteur}

def get_all_interventions(session) : 
    liste_interventions =  session.query(Intervention).all()
    return {intervention.idIntervention : intervention for intervention in liste_interventions}

def get_exposant(session, id_exposant):
    return session.query(Exposant).filter(Exposant.idP == id_exposant).first()

def get_invite(sessionSQL, id_invite):
    return sessionSQL.query(Invite).filter(Invite.idP == id_invite).first()

def get_staff(sessionSQL, id_staff):
    return sessionSQL.query(Staff).filter(Staff.idP == id_staff).first()

def get_auteur(sessionSQL, id_auteur):
    return sessionSQL.query(Auteur).filter(Auteur.idP == id_auteur).first()

def get_presse(sessionSQL, id_presse):
    return sessionSQL.query(Presse).filter(Presse.idP == id_presse).first()


def get_secretaire(sessionSQL, id_secretaire):
    return sessionSQL.query(Secretaire).filter(Secretaire.idP == id_secretaire).first()

def get_prenom(sessionSQL, id_participant):
    return (sessionSQL.query(Utilisateur).filter(Utilisateur.idP == id_participant).first()).prenomP

def get_nom(sessionSQL, id_participant):
    return (sessionSQL.query(Utilisateur).filter(Utilisateur.idP == id_participant).first()).nomP

def get_id_hotel(sessionSQL, nom_hotel):
    return (sessionSQL.query(Hotel).filter(Hotel.nomHotel == nom_hotel).first()).idHotel
   

def get_utilisateur(sessionSQL, id_utilisateur):
    return sessionSQL.query(Utilisateur).filter(Utilisateur.idP == id_utilisateur).first()

def affiche_participants(sessionSQL):
    liste_participants = []
    participants = sessionSQL.query(Participant)
    for part in participants:
        liste_participants.append(part)
    return liste_participants
   

def affiche_participant_trier(sessionSQL, trie):
     
        if trie == "Auteur" :
            return sessionSQL.query(Participant).join(Auteur, Participant.idP==Auteur.idP).all()

        elif trie == "Consommateur":
            return sessionSQL.query(Participant).join(Consommateur, Participant.idP==Consommateur.idP).all() 

        elif trie == "Exposant": 
            return sessionSQL.query(Participant).join(Exposant, Participant.idP==Exposant.idP).all() 
        
        elif trie == "Intervenant":
            return sessionSQL.query(Participant).join(Intervenant, Participant.idP==Intervenant.idP).all() 
        
        elif trie == "Invite":
            return sessionSQL.query(Participant).join(Invite, Participant.idP==Invite.idP).all() 
        
        elif trie == "Presse":
            return sessionSQL.query(Participant).join(Presse, Participant.idP==Presse.idP).all() 
        
        elif trie == "Staff": 
            return sessionSQL.query(Participant).join(Staff, Participant.idP==Staff.idP).all()
        
        else: 
            return sessionSQL.query(Participant).order_by(Participant.idP.asc()).all()

def affiche_participant_trier_consommateur(sessionSQL):
    participant = sessionSQL.query(Participant).all()
    return participant


def get_nom_restaurant():
    liste_nom_resteau = []
    for nom in sessionSQL.query(Restaurant):
        liste_nom_resteau.append((nom.nomRest, nom.idRest))
    return liste_nom_resteau

def get_nom_hotel():
    liste_nom_hotel = []
    for nom in sessionSQL.query(Hotel):
        liste_nom_hotel.append(nom.nomHotel)
    return liste_nom_hotel


    
        
def afficher_consommateur(sessionSQL, date_jour, restaurant, midi):
    if restaurant != "Restaurant":
        restaurant = int(restaurant)
        print(restaurant)
    if midi == "true":
        midi = True
    elif midi == "false":
        midi = False
    liste_consommateurs = []
    liste_creneau = []
    liste_repas = []
    liste_mangeur = []
    if restaurant != "Restaurant" and midi != "Journee":
        repas = sessionSQL.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau).filter(Repas.idRest == restaurant).filter(Repas.estMidi == midi).all()
    elif restaurant == "Restaurant" and midi == "Journee":
        repas = sessionSQL.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau)
    elif restaurant != "Restaurant":
        repas = sessionSQL.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau).filter(Repas.idRest == restaurant).all()
    elif midi != "Journee":
        repas = sessionSQL.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau).filter(Repas.estMidi == midi).all()
    
    if date_jour[0] != "Date":
        date_jour = date(int(date_jour[0]), int(date_jour[1]), int(date_jour[2]))
        for cren in repas:
            if cren[1].date() == date_jour:
                liste_creneau.append(cren[2])
        repas = sessionSQL.query(Repas, Repas.idCreneau, Repas.idRepas).all()
        for rep in repas:
            if rep[1] in liste_creneau:
                liste_repas.append(rep[2])
    else:
        for rep in repas:
            liste_repas.append(rep[3])

    manger = sessionSQL.query(Manger, Manger.idP, Manger.idRepas).all()
    for mangeur in manger:
        if mangeur[2] in liste_repas:
            liste_mangeur.append(mangeur[1])

    consommateurs = sessionSQL.query(Consommateur, Consommateur.idP).all()

    for consomm in consommateurs:
        if consomm[1] in liste_mangeur:
            liste_consommateurs.append(consomm[1])
    print(liste_consommateurs)
    liste_participants = get_liste_participant_idp_regime(sessionSQL, liste_consommateurs)
    return liste_participants

def get_liste_participant_idp_regime(sessionSQL, liste_id):
    liste_participants = []
    participants = sessionSQL.query(Participant).join(Consommateur, Participant.idP == Consommateur.idP).all()
    for une_personne in participants:
        if une_personne.idP in liste_id:
            liste_participants.append((une_personne, get_regime(sessionSQL, une_personne.idP)))
    return liste_participants

def affiche_navette(sessionSQL, date, navette, directionGare):
    if navette != "Navette" :
        navette = int(navette)
    if directionGare == "true" : 
        directionGare = True
    elif directionGare == "false" : 
        directionGare = False
    liste_consommateurs = []
    liste_creneau = []
    liste_transport = []
    liste_mangeur = []
    if navette != "Navette" and directionGare != "Direction":
        transport = sessionSQL.query(Voyage.idVoy, Participant.prenomP, Participant.nomP, Voyage.directionGare, Navette.nomNavette, Voyage.heureDebVoy).join(Mobiliser, Mobiliser.idVoy == Voyage.idVoy).join(Navette, Navette.idNavette == Mobiliser.idNavette).join(Transporter, Voyage.idVoy == Transporter.idVoy).join(Intervenant, Intervenant.idP == Transporter.idP).join(Participant, Participant.idP == Intervenant.idP).filter(Navette.idNavette == navette).filter(Voyage.directionGare == directionGare).distinct().all()
    elif navette == "Navette" and directionGare == "Direction":
        transport = sessionSQL.query(Voyage.idVoy, Participant.idP, Participant.prenomP, Participant.nomP, Voyage.directionGare, Voyage.heureDebVoy).join(Mobiliser, Mobiliser.idVoy == Voyage.idVoy).join(Navette, Navette.idNavette == Mobiliser.idNavette).join(Transporter, Voyage.idVoy == Transporter.idVoy).join(Intervenant, Intervenant.idP == Transporter.idP).join(Participant, Participant.idP == Intervenant.idP).distinct().all()
    elif navette != "Restaurant":
        transport = sessionSQL.query(Voyage.idVoy, Participant.prenomP, Participant.nomP, Voyage.directionGare, Navette.nomNavette, Voyage.heureDebVoy).join(Mobiliser, Mobiliser.idVoy == Voyage.idVoy).join(Navette, Navette.idNavette == Mobiliser.idNavette).join(Transporter, Voyage.idVoy == Transporter.idVoy).join(Intervenant, Intervenant.idP == Transporter.idP).join(Participant, Participant.idP == Intervenant.idP).filter(Navette.idNavette == navette).distinct().all()
    elif directionGare != "Direction":
        transport = sessionSQL.query(Voyage.idVoy, Participant.prenomP, Participant.nomP, Voyage.directionGare, Navette.nomNavette, Voyage.heureDebVoy).join(Mobiliser, Mobiliser.idVoy == Voyage.idVoy).join(Navette, Navette.idNavette == Mobiliser.idNavette).join(Transporter, Voyage.idVoy == Transporter.idVoy).join(Intervenant, Intervenant.idP == Transporter.idP).join(Participant, Participant.idP == Intervenant.idP).filter(Voyage.directionGare == directionGare).distinct().all()
    
    print(transport)
    
    if date[0] != "Date":
        date = date(int(date[0]), int(date[1]), int(date[2])) # modifier ça et modifier le HTML
        for cren in transport:
            if cren[1].date() == date:
                liste_creneau.append(cren[2])
        transport = sessionSQL.query(Repas, Repas.idCreneau, Repas.idRepas).all()
        for rep in transport:
            if rep[1] in liste_creneau:
                liste_transport.append(rep[2])
    else:
        for tran in transport:
            liste_transport.append(tran[3])

    return liste_transport

# affiche_navette(sessionSQL, "Date", "Navette", "Direction")
         

def get_liste_participant_id_consommateur(sessionSQL, liste_id):
    liste_participants = []
    participants = sessionSQL.query(Participant).join(Consommateur, Participant.idP == Consommateur.idP).all()
    for une_personne in participants:
        if une_personne.idP in liste_id:
            liste_participants.append(une_personne)
    return liste_participants

def get_regime(sessionSQL, id_p):
    str_regime = ""
    liste_regime = sessionSQL.query(Regime.nomRegime).join(Avoir, Avoir.idRegime == Regime.idRegime).filter(Avoir.idP == id_p).all()
    if len(liste_regime) == 0:
        str_regime = "Pas de regime"
    else:
        for un_regime in liste_regime:
            str_regime += str(un_regime[0]) + ", "
        str_regime = str_regime[:-2]
    return str_regime

def get_dormeur(sessionSQL, date_jour, hotel):
    if date_jour[0] != "Date":
        date_jour = date(int(date_jour[0]), int(date_jour[1]), int(date_jour[2]))
    else:
        date_jour = date_jour[0]
        print(date_jour)
    liste_dormeur_date_hotel = []
    if hotel == "Hôtel":
        hotel = None
    else:
        hotel = int(hotel)
    dormeurs = sessionSQL.query(Loger.idP, Loger.dateDebut, Loger.dateFin, Loger.idHotel).all()
    for un_dormeur in dormeurs:
        date_deb = un_dormeur[1].date()
        date_fin = un_dormeur[2].date()
        if date_jour == "Date" :
            if hotel is None or un_dormeur.idHotel == hotel:
                liste_dormeur_date_hotel.append(un_dormeur[0])

        elif date_deb <= date_jour and date_fin >= date_jour and hotel is None or un_dormeur.idHotel == hotel : 
            liste_dormeur_date_hotel.append(un_dormeur[0])
                
    liste_participants = get_liste_participant_id_consommateur(sessionSQL, liste_dormeur_date_hotel)

    return liste_participants


def id_transport_with_name(nom_transport):
    if nom_transport == "avion" : 
        return 1
    elif nom_transport == "train" : 
        return 2
    elif nom_transport == "voiture" : 
        return 3
    elif nom_transport == "covoiturage" :
        return 4
    

def supprime_deplacer_annee(sessionSQL, idP, annee):
    deplacement = sessionSQL.query(Deplacer).filter(Deplacer.idP == idP).filter(Deplacer.annee == annee)
    for dep in deplacement : 
        sessionSQL.delete(dep)
        try : 
            sessionSQL.commit()
        except : 
            sessionSQL.rollback()
            print("erreur supprimé déplacement !")



def ajoute_deplacer(sessionSQL, idP, idTransport, lieuDepart, lieuArrive, annee) :
    deplacement = Deplacer(idP, idTransport, lieuDepart, lieuArrive, annee)
    deplacer = sessionSQL.query(Deplacer).filter(Deplacer.idP == idP).filter(Deplacer.idTransport == idTransport).filter(Deplacer.lieuDepart == lieuDepart).filter(Deplacer.lieuArrive == lieuArrive).filter(Deplacer.annee == annee).first()
    if deplacer is None:
        sessionSQL.add(deplacement)
        try: 
            sessionSQL.commit()
            print("Le deplacement à bien été inséré")
        except:
            print("Erreur !")
            sessionSQL.rollback()
    else:
        print("Un même déplacement existe déjà pour cette personne")
  

def supprime_mangeur(sessionSQL, idP):
    annee = datetime.now().year
    manger = sessionSQL.query(Manger).join(Repas, Manger.idRepas == Repas.idRepas).join(Creneau, Repas.idCreneau == Creneau.idCreneau).filter(Manger.idP == idP).filter(extract('year', Creneau.dateDebut) == annee).all()
    for mang in manger :
        sessionSQL.query(Manger).filter(Manger.idP == mang.idP).filter(Manger.idRepas == mang.idRepas).delete()
        sessionSQL.commit()


def ajoute_mangeur(sessionSQL, idP, idRepas):
    mangeur = Manger(idP, idRepas)
    manger = sessionSQL.query(Manger).join(Repas, Manger.idRepas == Repas.idRepas).join(Creneau, Repas.idCreneau == Creneau.idCreneau).filter(Manger.idP == idP).filter(Manger.idRepas == idRepas).first()
    if manger is None:
        sessionSQL.add(mangeur)
        try: 
            sessionSQL.commit()
            print("Le consommateur à bien été associé à un repas")  

        except Exception as e:
            print(idP)
            print(traceback.format_exc())
            print("Erreur !")
            sessionSQL.rollback()
    else: 
        print("Un consommateur mange déjà ce repas")
        

def suppprime_loger(sessionSQL, idP):
    annee = datetime.today().year
    loger = sessionSQL.query(Loger).filter(Loger.idP == idP).filter(extract('year', Loger.dateDebut) == annee).all()
    for log in loger :
        sessionSQL.query(Loger).filter(Loger.idP == log.idP).delete()
        sessionSQL.commit()


def ajoute_loger(sessionSQL, idP, dateDebut, dateFin, idHotel):
    date_debut = datetime(dateDebut.year, dateDebut.month, dateDebut.day, dateDebut.hour, dateDebut.minute, dateDebut.second)
    date_fin = datetime(dateFin.year, dateFin.month, dateFin.day, dateFin.hour, dateFin.minute, dateFin.second)

    logeur = Loger(idP, date_debut, date_fin, idHotel)
    sessionSQL.add(logeur)
    try:
        sessionSQL.commit()
        print("Le loger à bien été associé à un hôtel")  

    except Exception:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info) 
        print("Erreur !")
        sessionSQL.rollback()
        
        
def choix_hotel(sessionSQL, idP):
    return 1 #TODO
        
        
def ajoute_hebergement(sessionSQL, idP): 
    annee = datetime.today().year
    dates = sessionSQL.query(Assister.dateArrive, Assister.dateDepart).filter(Assister.idP == idP).filter(extract('year', Assister.dateArrive) == annee).first()
    dateDebut = dates[0]
    dateFin = dates[1]
    idHotel = choix_hotel(sessionSQL, idP)
    ajoute_loger(sessionSQL, idP, dateDebut, dateFin, idHotel)
        
def get_max_id_regime(sessionSQL): 
    regime= sessionSQL.query(func.max(Regime.idRegime)).first()
    if (regime[0]) is None:
        return 0
    else:
        return regime._data[0]
        
def ajoute_regime(sessionSQL, idP, regime) :
    sessionSQL.query
    id_regime = get_max_id_regime(sessionSQL)+1
    regime = Regime(id_regime, regime)
    sessionSQL.add(regime)
    try :
        sessionSQL.commit()
        return id_regime
    except : 
        print("erreur")
        sessionSQL.rollback() 
        
def ajoute_avoir_regime(sessionSQL, id_consommateur, id_regime) :
    avoir_regime = Avoir(id_consommateur, id_regime)
    sessionSQL.add(avoir_regime)
    try :
        sessionSQL.commit()
        print("L'association regime-consommateur à bien été ajoutée !")
    except : 
        print("erreur")
        sessionSQL.rollback() 
    
def est_intervenant(sessionSQL, idP):
    intervenant = sessionSQL.query(Intervenant).filter(Intervenant.idP == idP).first()
    return intervenant is not None
            
def est_secretaire(sessionSQL, idP):
    print(str(idP) + " secrea")
    secretaire = get_secretaire(sessionSQL, idP)
    print(secretaire)
    return secretaire is not None
        
        
def requete_transport_annee(sessionSQL, idP, annee) : 
    liste_transport = sessionSQL.query(Deplacer, Assister.dateDepart).join(Assister, Deplacer.idP == Assister.idP).filter(Deplacer.idP == idP).all()
    liste_deplacement = list()
    annee = annee.year
    for transport in liste_transport: 
        annee_req = transport[1].year
        if annee_req == annee: 
            liste_deplacement.append(transport)
    return liste_deplacement       



def ajoute_assister(sessionSQL, idP, dateArrive, dateDepart):
    assisteur = Assister(idP, dateArrive, dateDepart)
    assister = sessionSQL.query(Assister).filter(extract('year', Assister.dateArrive) == dateArrive.year).first()
    if assister is None :
        sessionSQL.add(assisteur)
        try : 
            sessionSQL.commit()
            print("L'intervenant à bien été ajouté à ces dates") 
        except : 
            print("Erreur !")
            sessionSQL.rollback()
    else :
        sessionSQL.query(Assister).filter(extract('year', Assister.dateArrive) == dateArrive.year).filter(Assister.idP == idP).update({Assister.dateArrive: dateArrive, Assister.dateDepart: dateDepart},synchronize_session='fetch')
        sessionSQL.commit()
        
def cherche_transport(sessionSQL, nom_transport) : 
    liste_transport = sessionSQL.query(Transport.idTransport, Transport.nomTransport).all()
    res = list()
    for transport in liste_transport : 
        if nom_transport in transport : 
            res.append(transport)
    return res


def modif_participant_remarque(sessionSQL, idP, remarques) : 
    if remarques.isalpha():
        nouvelles_remarques = remarques + " / "+str((sessionSQL.query(Participant).filter(Participant.idP == idP).first()).remarques)
        sessionSQL.query(Participant).filter(Participant.idP == idP).update({Participant.remarques : nouvelles_remarques})
        sessionSQL.commit()


def get_utilisateur_email_mdp(sessionSQL, mail, mdp):
    utilisateur = sessionSQL.query(Utilisateur).filter(Utilisateur.emailP == mail).filter(Utilisateur.mdpP == mdp).first()
    if utilisateur is not None :
        return utilisateur
    

@staticmethod
def transforme_datetime(date):
    date = date.split("-")
    return date

def ajoute_creneau_v1(session, dateDebut,dateFin):
    liste_date_deb = transforme_datetime(dateDebut)
    liste_date_fin = transforme_datetime(dateFin)
    dateDebut = datetime(int(liste_date_deb[0]), int(liste_date_deb[1]), int(liste_date_deb[2]), int(liste_date_deb[3]), int(liste_date_deb[4]),int(liste_date_deb[5]))
    dateFin = datetime(int(liste_date_fin[0]), int(liste_date_fin[1]), int(liste_date_fin[2]), int(liste_date_fin[3]), int(liste_date_fin[4]), int(liste_date_fin[5]))
    creneau_test = sessionSQL.query(Creneau).filter(Creneau.dateDebut == dateDebut).filter(Creneau.dateFin == dateFin).first()
    if creneau_test is None :
        idCreneau = get_max_id_creneau(sessionSQL)+1
        creneau = Creneau(idCreneau, dateDebut, dateFin)
        sessionSQL.add(creneau)
        try :
            session.commit()
        except :
            print("erreur creneau")
            sessionSQL.rollback()
        return creneau.idCreneau
    return creneau_test.idCreneau


def ajoute_creneau(session, date_debut, date_fin):
    creneau_test = session.query(Creneau).filter(Creneau.dateDebut == date_debut).filter(Creneau.dateFin == date_fin).first()
    if creneau_test is None :
        idCreneau = get_max_id_creneau(session)+1
        creneau = Creneau(idCreneau, date_debut, date_fin)
        session.add(creneau)
        try :
            session.commit()
        except : 
            print("erreur creneau")
            session.rollback()
        return creneau.idCreneau
    else : 
        print("un creneau similaire existe déjà")
        return creneau_test.idCreneau
    

def ajoute_repas(session, estMidi,idRest,idCreneau) : 
    repas_verif = session.query(Repas).filter(Repas.estMidi == estMidi).filter(Repas.idRest == idRest).filter(Repas.idCreneau == idCreneau).first()
    if repas_verif is None :
        idRepas = get_max_id_repas(sessionSQL)+1
        repas = Repas(idRepas, estMidi, idRest, idCreneau)
        sessionSQL.add(repas)
        try : 
            sessionSQL.commit()
        except Exception:
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            print(traceback.format_exc())
            print("erreur repas")
            sessionSQL.rollback()
        return repas.idRepas
    return repas_verif.idRepas

def ajoute_restaurant(sessionSQL, nomRest) : 
    restaurant_test = sessionSQL.query(Restaurant).filter(Restaurant.nomRest == nomRest).first()
    if restaurant_test is None :
        idRestaurant = get_max_id_restaurant(sessionSQL)+1
        restaurant = Restaurant(idRestaurant, nomRest)
        sessionSQL.add(restaurant)
        try : 
            sessionSQL.commit()
        except : 
            print("erreur restaurant")
            sessionSQL.rollback()
    return restaurant_test.idRest

def choix_restaurant(sessionSQL): 
    pass # TODO SELON LE ROLE METTRE UN CERTAIN RESTAU 
    
 
def ajoute_repas_mangeur(sessionSQL, idP, liste_repas, liste_horaire_restau, dico_horaire_restau):
    supprime_mangeur(sessionSQL, idP)
    for i in range(0, len(liste_repas)):
        if liste_repas[i] == 'true':
            horaire = dico_horaire_restau[liste_horaire_restau[i]]
            idCreneau = ajoute_creneau_v1(sessionSQL, horaire.split("/")[0], horaire.split("/")[1])
            idRest = choix_restaurant(sessionSQL) # ajouter ROLE TODO
            idRepas = ajoute_repas(sessionSQL, False if liste_horaire_restau[i][-4:] == "soir" else True, 1 if liste_horaire_restau[i][-4:] == "soir" else 1 , idCreneau) #TODO
            ajoute_mangeur(sessionSQL, idP, idRepas)


@login_manager.user_loader
def load_user(participant_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    print(str(participant_id) + str("iddd"))
    print("l1070")
    if est_secretaire(sessionSQL, participant_id):
        return get_secretaire(sessionSQL, participant_id)
    else:
        return get_participant(sessionSQL, participant_id)



@staticmethod
def generate_password(length=8):
  # Get a list of all the ASCII lowercase letters, uppercase letters, and digits
  characters = string.ascii_letters + string.digits + string.punctuation
  # Use the random.sample function to get a list of `length` random elements from the list of characters
  password = ''.join(random.sample(characters, length))
  return password


@staticmethod
def get_heure(time) :
    heure = time.split(':')[0]
    minute = time.split(':')[1][0:2]
    return (heure, minute)
    

@staticmethod
def get_all_lieu_train(file_path="./Developpement/app/static/txt/gare.txt"): 
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]

