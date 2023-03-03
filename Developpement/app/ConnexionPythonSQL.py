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
import random
import string
import traceback
import sys
from sqlalchemy.sql import operators, extract
from sqlalchemy.orm import aliased
from sendgrid.helpers.mail import Content

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
from .CreneauRepas import CreneauRepas
from .CreneauTravail import CreneauTravail
from .Restaurant import Restaurant
from .Avoir import Avoir
from .Regime import Regime
from .Assister import Assister
from .Secretaire import Secretaire
from .Navette import Navette
from .Transporter import Transporter
from .Travailler import Travailler
from .Voyage import Voyage
from .Transport import Transport
from .Utilisateur import Utilisateur
from .constants import * 

from .app import login_manager
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

connexion ,engine = ouvrir_connexion("nardi","nardi",'servinfo-mariadb', "DBnardi")
#connexion ,engine = ouvrir_connexion("charpentier","charpentier","servinfo-mariadb", "DBcharpentier")
#connexion ,engine = ouvrir_connexion("doudeau","doudeau",'servinfo-mariadb', "DBdoudeau")
#connexion ,engine = ouvrir_connexion("doudeau","doudeau",'servinfo-mariadb', "DBdoudeau")
#connexion ,engine = ouvrir_connexion("doudeau","doudeau","localhost", "BDBOUM")
#connexion ,engine = ouvrir_connexion("nardi","nardi","localhost", "BDBOUM")
#connexion ,engine = ouvrir_connexion("root","charpentier","localhost", "BDBOUM")
#connexion ,engine = ouvrir_connexion("charpentier","charpentier","servinfo-mariadb", "DBcharpentier")



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

def datetime_to_dateAnglais(date):
    date = str(date)[:10]
    debut_new_date = date[8:]
    fin_new_date = date[:4]
    date = date[5:]
    date = date[:2]
    return fin_new_date + "-" + date + "-" + debut_new_date 

def datetime_to_heure(date):
    new_date = str(date)
    return new_date[11:]

def get_hotel(idH):
    return (sessionSQL.query(Hotel).filter(Hotel.idHotel == idH).first()).nomHotel

def get_nom_hotel_idP(idP) : 
    return sessionSQL.query(Hotel).join(Loger, Loger.idHotel == Hotel.idHotel).filter(Loger.idP == idP).first().nomHotel

def get_periode_hotel(idP):
    debut = (sessionSQL.query(Loger).filter(Loger.idP == idP).first()).dateDebut
    fin = (sessionSQL.query(Loger).filter(Loger.idP == idP).first()).dateFin
    return format_creneau(debut, fin)

def get_date_dormeur(idP):
    dateDeb = (sessionSQL.query(Loger).filter(Loger.idP == idP).first()).dateDebut
    dateFin = (sessionSQL.query(Loger).filter(Loger.idP == idP).first()).dateFin
    return (datetime_to_dateFrancais(dateDeb), datetime_to_dateFrancais(dateFin))

def get_consommateur(idP):
    return sessionSQL.query(Consommateur).filter(Consommateur.idP == idP).first()

def get_restaurant(idRepas):
    idRestaurant = (sessionSQL.query(Repas).filter(Repas.idRepas == idRepas).first()).idRest
    return (sessionSQL.query(Restaurant).filter(Restaurant.idRest == idRestaurant).first()).nomRest


def get_creneau_repas(idRepas):
    idCreneau = (sessionSQL.query(Repas).filter(Repas.idRepas == idRepas).first()).idCreneau
    debut = (sessionSQL.query(CreneauRepas).filter(CreneauRepas.idCreneau == idCreneau).first()).dateDebut
    fin = (sessionSQL.query(CreneauRepas).filter(CreneauRepas.idCreneau == idCreneau).first()).dateFin
    return format_creneau(debut, fin)

def get_intervenant(idP):
    return sessionSQL.query(Intervenant).filter(Intervenant.idP == idP).first()

def get_date_repas(idRepas):
    idCreneau = (sessionSQL.query(Repas).filter(Repas.idRepas == idRepas).first()).idCreneau
    debut = (sessionSQL.query(CreneauRepas).filter(CreneauRepas.idCreneau == idCreneau).first()).dateDebut
    return datetime_to_dateFrancais(debut)


def get_deb_voyage(idVoyage):
    return sessionSQL.query(Voyage).filter(Voyage.idVoy == idVoyage).first().heureDebVoy

def get_lieu_depart_voyage(idVoyage):
    if (sessionSQL.query(Voyage).filter(Voyage.idVoy == idVoyage).first()).directionGare:
        return "Festival → Gare Blois"
    else:
        return "Gare Blois → Festival"


def get_all_lieu() : 
    lieux = sessionSQL.query(Lieu).all()
    lieux_dict = {lieu.idLieu: lieu for lieu in lieux}
    return lieux_dict


def get_repas(idP, annee):
    resultat = sessionSQL.query(Repas, CreneauRepas, Restaurant)\
        .join(CreneauRepas, CreneauRepas.idCreneau == Repas.idCreneau)\
        .join(Restaurant, Restaurant.idRest == Repas.idRest)\
        .join(Manger, Manger.idRepas == Repas.idRepas)\
        .filter(Manger.idP == idP)\
        .filter(extract('year', CreneauRepas.dateDebut) == annee).order_by(CreneauRepas.dateDebut.asc()).all()
    
    liste_res = []
    if resultat:
        for res in resultat:
            repas, creneau, restaurant = res
            liste_res.append((repas, creneau, restaurant, JOURS_SEMAINES[creneau.dateDebut.strftime("%A")]))
    
    return liste_res

    

# def get_max_id_utilisateur(sessionSQL):
#     max_id = sessionSQL.query(func.max(Utilisateur.idP)).first()
    
#     if (max_id[0]) is None:
#         return 0
#     else:
#         return max_id[0]
    

def get_max_id_secretaire():
    max_id = sessionSQL.query(func.max(Secretaire.idP)).first()
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]
    
def get_max_id_exposant():
    max_id = sessionSQL.query(func.max(Exposant.idP)).first()
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_id_auteur():
    max_id = sessionSQL.query(func.max(Auteur.idP)).first()
    
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_id_invite():
    max_id = sessionSQL.query(func.max(Invite.idP)).first()
    
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_id_presse():
    max_id = sessionSQL.query(func.max(Presse.idP)).first()
    
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_id_staff():
    max_id = sessionSQL.query(func.max(Staff.idP)).first()
    
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_num_stand():
    max_num = sessionSQL.query(func.max(Exposant.numStand)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]

        
def get_max_id_repas():        
    max_num = sessionSQL.query(func.max(Repas.idRepas)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]
    
def get_mail(idParticipant):
    email = (sessionSQL.query(Utilisateur).filter(Utilisateur.idP == idParticipant).first()).emailP
    if email:
        return email
    return None

def get_max_id_creneau_repas():        
    max_num = sessionSQL.query(func.max(CreneauRepas.idCreneau)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]

def get_max_id_creneau_travail():        
    max_num = sessionSQL.query(func.max(CreneauTravail.idCreneau)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]

def get_max_id_restaurant():
    max_num = sessionSQL.query(func.max(Restaurant.idRest)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]
    
def get_max_id_voyage():
    max_num = sessionSQL.query(func.max(Voyage.idVoy)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]
def get_info_all_participants(prenomP, nomP, emailP, ddnP, role):
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



def get_info_all_invite(prenomP, nomP, emailP, invite, role): 
    participants = sessionSQL.query(Participant)
    if(prenomP != ""):
        participants = participants.filter(Participant.prenomP == prenomP)
    if(nomP != ""):
        participants = participants.filter(Participant.nomP == nomP)
    if(emailP != ""):
        participants = participants.filter(Participant.emailP == emailP)
    if(invite != ""):
        print(invite)
        print(bool(invite))
        print(type(bool(invite)))
        if invite == "True":
            participants = participants.filter(Participant.invite == True)
        else:
            participants = participants.filter(Participant.invite == False)
    if(role!= ""):
        participants = filtrer_par_role(role, participants)
    return participants.all()
 


def get_tout_dormeurs_avec_filtre(prenomP, nomP, nomHotel, dateArrive, dateDeparts):
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
        date_jour_debut = datetime.datetime(int(annee),int(mois),int(jour), 0,0,0)
        date_jour_fin = datetime.datetime(int(annee),int(mois),int(jour), 23,59,59)
        participants = participants.filter(Loger.dateDebut >= date_jour_debut).filter(Loger.dateDebut <= date_jour_fin)
    if(dateDeparts!= ""):
        jour = dateDeparts.split("/")[0]
        mois = dateDeparts.split("/")[1]
        annee = dateDeparts.split("/")[2]
        date_jour_debut = datetime.datetime(int(annee),int(mois),int(jour), 0,0,0)
        date_jour_fin = datetime.datetime(int(annee),int(mois),int(jour), 23,59,59)
        participants = participants.filter(Loger.dateFin >= date_jour_debut).filter(Loger.dateFin <= date_jour_fin)
    return participants.all()

def get_info_all_consommateurs(prenomC, nomC, restaurant, la_date, creneau):
    consommateurs = sessionSQL.query(Manger).join(
                        Repas, Manger.idRepas == Repas.idRepas).join(
                        Restaurant, Repas.idRest == Restaurant.idRest).join(
                        Consommateur, Manger.idP == Consommateur.idP).join(
                        CreneauRepas, Repas.idCreneau == CreneauRepas.idCreneau)
    if(prenomC != ""):
        consommateurs = consommateurs.filter(Consommateur.prenomP == prenomC)
    if(nomC != ""):
        consommateurs = consommateurs.filter(Consommateur.nomP == nomC)
    if (restaurant != ""):
        consommateurs = consommateurs.filter(Restaurant.nomRest == restaurant)
    if(la_date!= ""):
        jour = la_date.split("/")[0]
        mois = la_date.split("/")[1]
        annee = la_date.split("/")[2]
        my_date = datetime.date(int(annee), int(mois), int(jour))
        consommateurs = consommateurs.filter(func.date(CreneauRepas.dateDebut) == my_date)
        
    if(creneau != ""):
        (heure_creneau_debut, minute_creneau_debut) = creneau.split('-')[0].split(':')
        (heure_creneau_fin, minute_creneau_fin) = creneau.split('-')[1].split(':')
        consommateurs = consommateurs.filter(extract('hour', CreneauRepas.dateDebut) == heure_creneau_debut).filter(extract('minute', CreneauRepas.dateDebut) == minute_creneau_debut)
        consommateurs = consommateurs.filter(extract('hour', CreneauRepas.dateFin) == heure_creneau_fin).filter(extract('minute', CreneauRepas.dateFin) == minute_creneau_fin)

    return consommateurs.all()

def get_tout_voyage_avec_filtre(id_voyage, direction, id_navette, date_depart):
    print(sessionSQL,id_voyage, direction, id_navette, date_depart)
    voyages = sessionSQL.query(Voyage)
    if(id_voyage != ""):
        voyages = voyages.filter(Voyage.idVoy == int(id_voyage))
    if(direction != ""):
        if(direction == "Gare"):
            voyages = voyages.filter(Voyage.directionGare == True)
        else:
            voyages = voyages.filter(Voyage.directionGare == False)
    if(id_navette != ""):
        voyages = voyages.filter(Voyage.idNavette == int(id_navette))
    if(date_depart != ""):
        jour = date_depart.split("/")[0]
        mois = date_depart.split("/")[1]
        annee = date_depart.split("/")[2]
        date_datetime = datetime(int(annee),int(mois),int(jour), 0,0,0)
        voyages = voyages.filter(func.date(Voyage.heureDebVoy) == date_datetime)
    return voyages.all()


def get_intervenant_dans_voyage_avec_filtre(id_voyage, prenom_p, nom_p):
    print(sessionSQL,id_voyage, prenom_p, nom_p)
    #intervenants = sessionSQL.query(Transporter).filter(
    #                Transporter.idVoy == id_voyage).join(
    #            Intervenant, Intervenant.idP == Transporter.idP)
    intervenants = sessionSQL.query(Intervenant).join(
                Transporter, Intervenant.idP == Transporter.idP).filter(
                Transporter.idVoy == id_voyage)
    if(nom_p != ""):
        intervenants = intervenants.filter(Intervenant.nomP == nom_p)
    if(prenom_p != ""):
        intervenants = intervenants.filter(Intervenant.prenomP == prenom_p)
    
    return intervenants.all()

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

def ajoute_secretaire(idP, prenomP, nomP, emailP, mdpP): 
    secretaire = Secretaire(idP, prenomP, nomP, emailP, mdpP)
    sessionSQL.add(secretaire)
    try:
        sessionSQL.commit()
        print("La secretaire "+ str(secretaire.prenomP) +" a bien été inséré dans la base de donnée")
    except:
        print("Erreur")


def ajoute_exposant(idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostalP, villeP):
    exposant = Exposant(idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostalP, villeP)
    sessionSQL.add(exposant)
    try:
        sessionSQL.commit()
    except Exception as inst:
        print(inst)
        sessionSQL.rollback()

def ajoute_staff(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostalP, villeP):
    staff = Staff(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostalP, villeP)
    personne = sessionSQL.query(Participant).filter(Participant.idP == staff.idP).first()
    sessionSQL.add(staff)
    try:
        sessionSQL.commit()
        print("La personne " + str(personne) + " est devenu un(e) staff")
    except:
        print("Erreur")
        sessionSQL.rollback()

        
def ajoute_intervenant(idP):
    intervenant = Intervenant(idP)
    personne = sessionSQL.query(Participant).filter(Participant.idP == intervenant.idP).first()
    sessionSQL.add(intervenant)
    try:
        sessionSQL.commit()
        print("La personne " + str(personne) + " est devenu un(e) intervenant(e)")
    except:
        print("Erreur")
        sessionSQL.rollback()

    
def ajoute_auteur(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostalP, villeP):
    auteur = Auteur(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostalP, villeP)
    sessionSQL.add(auteur)
    try:
        sessionSQL.commit()
    except Exception as inst:
        print(inst)
        sessionSQL.rollback()

def ajoute_presse(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP,codePostalP, villeP):
    presse = Presse(idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP,codePostalP, villeP)
    sessionSQL.add(presse)
    try:
        sessionSQL.commit()
    except:
        print("Erreur")
        sessionSQL.rollback()

def ajoute_invite(idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostalP, villeP):
    invite = Invite(idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP,codePostalP, villeP)
    sessionSQL.add(invite)
    try:
        sessionSQL.commit()
    except:
        print("Erreur")
        sessionSQL.rollback()
        

def ajoute_participant_role(prenomP, nomP, emailP, adresseP, codePostal, ville, telP, ddnP, role):
    if role in ROLE:
        mdpP = generate_password()
        if role == "Secretaire" : 
            idP = get_max_id_secretaire()+1
            ajoute_secretaire(idP, prenomP, nomP, emailP, mdpP )
        elif role == "Exposant":
            idP = get_max_id_exposant()+1
            ajoute_exposant(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostal,ville)
        elif role == "Staff":
            idP = get_max_id_staff()+1
            ajoute_staff(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostal, ville)
        elif role == "Auteur":
            idP = get_max_id_auteur()+1
            ajoute_auteur(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostal,ville)
        elif role == "Presse":
            idP = get_max_id_presse()+1
            ajoute_presse(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostal,ville)
        elif role == "Invite" :
            idP = get_max_id_invite()+1
            ajoute_invite(idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostal,ville)
    else:
        print("Le rôle n'est pas reconnu")


def ajoute_intervention(idP, idCreneau, idLieu, idIntervention, descIntervention):
    intervenir = Intervenir(idP, idCreneau, idLieu, idIntervention, descIntervention)
    intervention = sessionSQL.query(Intervenir).filter(Intervenir.idP == intervenir.idP).filter(Intervenir.idCreneau == intervenir.idCreneau).filter(Intervenir.idIntervention == idIntervention).first()
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

def ajouter_navette(idNavette, nomNavette, capaciteNavette):
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
def supprimer_personne_transporter(idP, idVoyage):
    liste_personne = sessionSQL.query(Transporter.idP).filter(Transporter.idVoy == idVoyage).all()
    if len(liste_personne) == 1:
        sessionSQL.query(Transporter).filter(Transporter.idP == idP).filter(Transporter.idVoy == idVoyage).delete()
        sessionSQL.query(Voyage).filter(Voyage.idVoy == idVoyage).delete()
        sessionSQL.commit()
        print("Le transport a été supprimé car cette personne était seul dans ce voyage")
    else:
        sessionSQL.query(Transporter).filter(Transporter.idP == idP).filter(Transporter.idVoy == idVoyage).delete()
        sessionSQL.commit()
        print("Cette personne a bien été supprimé du voyage")


# ajoute_intervention(sessionSQL, 300, 1, 1, "Dédicace", "Séance de dédicace avec les spectateurs")
        
def supprimer_utilisateur(id_utilisateur):
    sessionSQL.query(Utilisateur).filter(Utilisateur.idP == id_utilisateur).delete()
    sessionSQL.commit()
    print("L'utilisateur' a été supprimé")

def supprimer_secretaire(id_secretaire):
    sessionSQL.query(Secretaire).filter(Secretaire.idP == id_secretaire).delete()
    sessionSQL.commit()
    print("La secretaire a été supprimé")

def supprimer_participant(id_participant):
    sessionSQL.query(Participant).filter(Participant.idP == id_participant).delete()
    sessionSQL.commit()
    print("Le participant a été supprimé")

def supprimer_consommateur(id_consommateur):
    sessionSQL.query(Manger).filter(Manger.idP == id_consommateur).delete()
    sessionSQL.query(Avoir).filter(Avoir.idP == id_consommateur).delete()
    sessionSQL.commit()

    sessionSQL.query(Consommateur).filter(Consommateur.idP == id_consommateur).delete()
    sessionSQL.commit()
    print("Le consommateur a été supprimé")

def supprimer_intervenant(id_intervenant):
    sessionSQL.query(Transporter).filter(Transporter.idP == id_intervenant).delete()
    sessionSQL.query(Deplacer).filter(Deplacer.idP == id_intervenant).delete()
    sessionSQL.query(Assister).filter(Assister.idP == id_intervenant).delete()
    sessionSQL.query(Loger).filter(Loger.idP == id_intervenant).delete()
    sessionSQL.commit()

    sessionSQL.query(Intervenant).filter(Intervenant.idP == id_intervenant).delete()
    sessionSQL.commit()
    print("L'intervenant a été supprimé")

def supprimer_exposant(id_exposant):
    sessionSQL.query(Exposant).filter(Exposant.idP == id_exposant).delete()
    sessionSQL.commit()
    print("L'exposant a été supprimé")
  
def supprimer_staff(id_staff):
    sessionSQL.query(Travailler).filter(Travailler.idP == id_staff).delete()
    sessionSQL.commit()

    sessionSQL.query(Staff).filter(Staff.idP == id_staff).delete()
    sessionSQL.commit()
    print("Le staff a été supprimé")

def supprimer_auteur(id_auteur):
    sessionSQL.query(Intervenir).filter(Intervenir.idP == id_auteur).delete()
    sessionSQL.commit()
    sessionSQL.query(Auteur).filter(Auteur.idP == id_auteur).delete()
    sessionSQL.commit()
    print("L'auteur a été supprimé")

def supprimer_presse(id_presse):
    sessionSQL.query(Presse).filter(Presse.idP == id_presse).delete()
    sessionSQL.commit()
    print("Le membre de la presse a été supprimé")

def supprimer_invite(id_invite):
    sessionSQL.query(Invite).filter(Invite.idP == id_invite).delete()
    sessionSQL.commit()        
    print("L'invité a été supprimé")

def supprimer_repas_consommateur(id_consommateur, id_repas):
    sessionSQL.query(Manger).filter(Manger.idP == id_consommateur).filter(Manger.idRepas == id_repas).delete()
    sessionSQL.commit()

def supprimer_nuit_dormeur(id_dormeur, id_hotel, dateDeb, dateFin):
    liste_date_deb = transforme_datetime(dateDeb)
    liste_date_fin = transforme_datetime(dateFin)
    dateDeb_datetime = datetime.date(int(liste_date_deb[2]), int(liste_date_deb[1]), int(liste_date_deb[0]))
    dateFin_datetime = datetime.date(int(liste_date_fin[2]), int(liste_date_fin[1]), int(liste_date_fin[0]))
    test = sessionSQL.query(Loger).filter(Loger.idP == id_dormeur).filter(Loger.idHotel == id_hotel).filter(func.date(Loger.dateDebut) == dateDeb_datetime).filter(func.date(Loger.dateFin) == dateFin_datetime).first()
    sessionSQL.query(Loger).filter(Loger.idP == test.idP).filter(Loger.idHotel == test.idHotel).filter(Loger.dateDebut == test.dateDebut).filter(Loger.dateFin == test.dateFin).delete()
    sessionSQL.commit()

def get_role(id_utilisateur):
    utilisateur_existe = get_utilisateur(id_utilisateur)
    if utilisateur_existe is None:
        return None
    secretaire = get_secretaire(id_utilisateur)
    if secretaire is not None:
        return "Secretaire"
    exposant = get_exposant(id_utilisateur)
    if exposant is not None:
        return "Exposant"
    staff = get_staff(id_utilisateur)
    if staff is not None:
        return "Staff"
    auteur = get_auteur(id_utilisateur)
    if auteur is not None:
        return "Auteur"
    presse = get_presse(id_utilisateur)
    if presse is not None:
        return "Presse"
    invite = get_invite(id_utilisateur)
    if invite is not None:
        return "Invite"
    return "Pas de rôle"



def supprimer_utilisateur_role(id_utilisateur):
    role_utilisateur = get_role(id_utilisateur)
    if role_utilisateur is not None:
        if role_utilisateur == "Secretaire":
            supprimer_secretaire(id_utilisateur)
        else:
            if role_utilisateur == "Exposant":
                supprimer_exposant(id_utilisateur)
            else:
                if role_utilisateur == "Staff":
                    supprimer_staff(id_utilisateur)
                else:
                    if role_utilisateur == "Auteur":
                        supprimer_auteur(id_utilisateur)
                    elif role_utilisateur == "Presse":
                        supprimer_presse(id_utilisateur)
                    elif role_utilisateur == "Invite":
                        supprimer_invite(id_utilisateur)
                    supprimer_intervenant(id_utilisateur)
                supprimer_consommateur(id_utilisateur)
            supprimer_participant(id_utilisateur)
        supprimer_utilisateur(id_utilisateur)
    else:
        print("La personne que vous voulez supprimer n'existe pas")

     
def modifier_participant(idP, adresseP, codePostalP, villeP, ddnP, telP):
    sessionSQL.query(Participant).filter(Participant.idP == idP).update(
        {Participant.adresseP : adresseP, Participant.codePostalP : codePostalP, Participant.villeP : villeP,
        Participant.ddnP : ddnP, Participant.telP : telP})
    try : 
        sessionSQL.commit()
        print("Le participant a bien été modifié")
        return True
    except : 
        sessionSQL.rollback()
        print("erreur lors de la modif du participant")
        return False

def verif_regime_existe(nomRegime):
    regime = sessionSQL.query(Regime).filter(Regime.nomRegime == nomRegime).first()
    if regime is not None:
        return regime.idRegime
    else:
        ajoute_regime(nomRegime)

def get_id_creneau_repas(date_debut, date_fin):
    id_creneau = (sessionSQL.query(CreneauRepas).filter(CreneauRepas.dateDebut == date_debut).filter(CreneauRepas.dateFin == date_fin).first()).idCreneau
    return id_creneau

def est_midi(date_debut):
    # Obtenir l'heure de la date de début
    heure_debut = date_debut.time()
    
    # Définir l'heure de début et de fin de la période midi
    heure_midi_debut = datetime.time(11, 0)
    heure_midi_fin = datetime.time(13, 0)
    
    # Vérifier si l'heure de début est comprise entre l'heure de début et de fin de la période midi
    if heure_debut >= heure_midi_debut and heure_debut <= heure_midi_fin:
        return True
    else:
        return False    

def verif_repas_existe(nomRestaurant, date_debut, date_fin):
    id_restaurant = get_id_restaurant(nomRestaurant)
    id_creneau = get_id_creneau_repas(date_debut, date_fin)
    repas = sessionSQL.query(Repas).filter(Repas.idCreneau == id_creneau).filter(Repas.idRest == id_restaurant).first()
    if repas is not None:
        return repas.idRepas
    elif est_midi(date_debut):
        id = ajoute_repas(True, id_restaurant, id_creneau)
        return id
    else:
        id = ajoute_repas(False, id_restaurant, id_creneau)
        return id

def modifier_repas(idP, nomRestaurant, dateRepas, creneauRepas, idRepas):

    creneau_debut = creneauRepas.split("-")[0]
    liste_creneau_debut = creneau_debut.split(":")

    creneau_fin = creneauRepas.split("-")[1]
    liste_creneau_fin = creneau_fin.split(":")

    liste_date = dateRepas.split("-")

    date_debut = datetime.datetime(int(liste_date[2]), int(liste_date[1]), int(liste_date[0]), int(liste_creneau_debut[0]), int(liste_creneau_debut[1]), int(liste_creneau_debut[2]))
    date_fin = datetime.datetime(int(liste_date[2]), int(liste_date[1]), int(liste_date[0]), int(liste_creneau_fin[0]), int(liste_creneau_fin[1]), int(liste_creneau_fin[2]))

    new_idRepas = verif_repas_existe(nomRestaurant, date_debut, date_fin)
    sessionSQL.query(Manger).filter(Manger.idP == idP).filter(Manger.idRepas == idRepas).update({Manger.idRepas: new_idRepas})

    try : 
        sessionSQL.commit()
        print("Le repas associé à ce participant a bien été modifié")
        return True
    except : 
        sessionSQL.rollback()
        print("erreur lors de la modif du repas")
        return False


def modifier_hebergement(idp, nomHotel, dateDeb, dateFin, ancienHotel, ancienDateDeb, ancienDateFin):
    liste_dateDeb = dateDeb.split("-")
    liste_dateFin = dateFin.split("-")

    dateD = datetime.date(int(liste_dateDeb[2]), int(liste_dateDeb[1]), int(liste_dateDeb[0]))
    dateF = datetime.date(int(liste_dateFin[2]), int(liste_dateFin[1]), int(liste_dateFin[0]))

    liste_ancien_dateDeb = ancienDateDeb.split("-")
    liste_ancien_dateFin = ancienDateFin.split("-")

    ancien_dateD = datetime.date(int(liste_ancien_dateDeb[2]), int(liste_ancien_dateDeb[1]), int(liste_ancien_dateDeb[0]))
    ancien_dateF = datetime.date(int(liste_ancien_dateFin[2]), int(liste_ancien_dateFin[1]), int(liste_ancien_dateFin[0]))

    idHotel = get_id_hotel(nomHotel)
    ancien_idHotel = get_id_hotel(ancienHotel)
    print(ancien_idHotel)
    test = sessionSQL.query(Loger).filter(Loger.idP == idp).filter(Loger.idHotel == ancien_idHotel).first()
    print(test)

    sessionSQL.query(Loger).filter(Loger.idP == idp).filter(Loger.idHotel == ancien_idHotel).filter(func.date(Loger.dateDebut) == ancien_dateD).filter(func.date(Loger.dateFin) == ancien_dateF).update({
        Loger.idHotel: idHotel, Loger.dateDebut: dateD, Loger.dateFin: dateF
    }, synchronize_session=False)

    try : 
        sessionSQL.commit()
        print("L'hébergement associé à ce participant a bien été modifié")
        return True
    except : 
        sessionSQL.rollback()
        print("erreur lors de la modif de l'hébergement")
        return False
    
def modifier_utilisateur(idP, prenomP, nomP, emailP):
    sessionSQL.query(Utilisateur).filter(Utilisateur.idP == idP).update(
        {Utilisateur.prenomP : prenomP, Utilisateur.nomP : nomP, Utilisateur.emailP : emailP})
    try : 
        sessionSQL.commit()
        print("L'utilisateur a bien été modifié")
        return True
    except : 
        print("erreur lors de la modif du user")
        return False
    

def modifier_password(idP, new_password):
    sessionSQL.query(Utilisateur).filter(Utilisateur.idP == idP).update({Utilisateur.mdpP : new_password})
    try : 
        sessionSQL.commit()
        return True
    except :
        sessionSQL.rollback()
        print("erreur lors de la modif du MDP")
        return False
    
def modifier_participant_tout(idP, prenomP, nomP, ddnP, telP, emailP, adresseP, codePostalP, villeP, mdpP, invite, emailEnvoye, remarques):
    sessionSQL.query(Participant).filter(Participant.idP == idP).update(
        {Participant.prenomP : prenomP, Participant.nomP : nomP, Participant.ddnP : ddnP, 
         Participant.telP : telP, Participant.emailP : emailP, Participant.adresseP : adresseP, Participant.codePostalP : codePostalP,
         Participant.villeP : villeP, Participant.mdpP : mdpP, Participant.invite : invite, Participant.emailEnvoye : emailEnvoye, 
         Participant.remarques : remarques})
    sessionSQL.commit()
    print("Le participant a bien été modifié")
   

# def modifier_participant_role(sessionSQL, idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques, metier):
#     participant = Participant(idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques)
#     ancien_participant = Participant(participant.idP, participant.prenomP, participant.nomP, participant.ddnP, participant.telP, participant.emailP, participant.mdpP, participant.remarques, participant.invite, participant.emailEnvoye)
#     supprimer_utilisateur_role(sessionSQL, participant.idP)
#     ajoute_participant_role_id(sessionSQL, ancien_participant, metier)
#     print("Le role du participant a bien été modifié")

def modif_loger(ancien_loger, nouveau_loger):
    sessionSQL.query(Loger).filter(Loger.idP == ancien_loger.idP).filter(Loger.idHotel == ancien_loger.idHotel).filter(Loger.dateDebut == ancien_loger.dateDebut).update({
        Loger.dateDebut : nouveau_loger.dateDebut, Loger.dateFin : nouveau_loger.dateFin, Loger.idHotel : nouveau_loger.idHotel})
    sessionSQL.commit()
    print("Le logement de cette personne a bien été modifié")  
          

def modif_repas(ancien_repas, nouveau_repas):
    sessionSQL.query(Manger).filter(Manger.idP == ancien_repas.idP).filter(Manger.idRepas == ancien_repas.idRepas).update(
        {Manger.idRepas : nouveau_repas.idRepas}
    )
    sessionSQL.commit()
    print("Le repas du participant a bien été modifié")     

def get_info_personne(email, mdp):
    personne = sessionSQL.query(Participant).filter(Participant.emailP == email).filter(Participant.mdpP == mdp).first()
    if personne is None:
        return None
    else:
        return personne

def get_participant(id_participant):
    return sessionSQL.query(Participant).filter(Participant.idP == id_participant).first()

def get_exposant(id_exposant):
    return sessionSQL.query(Exposant).filter(Exposant.idP == id_exposant).first()

def get_all_auteur():
    Auteur_alias = aliased(Auteur)
    liste_auteur = sessionSQL.query(Auteur_alias).join(Participant, Auteur_alias.idP==Participant.idP).all()
    return {auteur.idP : auteur for auteur in liste_auteur}

def get_all_interventions() :
    """" Récupère un dictionnaire d'intervervention 
        Key : id de l'intervention (id_intervention)
        Value : l'intervention : (Intervention)
    """ 
    liste_interventions =  sessionSQL.query(Intervention).all()
    return {intervention.idIntervention : intervention for intervention in liste_interventions}

def get_intervenirs() : 
    return sessionSQL.query(Intervenir).all()

def get_intervenirs(idP) : 
    resultat = sessionSQL.query(Intervenir, Lieu, Intervention, CreneauTravail).join(Lieu, Lieu.idLieu == Intervenir.idLieu).join(Intervention, Intervention.idIntervention == Intervenir.idIntervention).join(CreneauTravail, CreneauTravail.idCreneau == Intervenir.idCreneau).filter(Intervenir.idP == idP).all()
    liste_res = list()
    if resultat:
        for res in resultat:
            intervenir, lieu, intervention, creneau = res
            liste_res.append((intervenir, lieu, intervention, creneau, JOURS_SEMAINES[creneau.dateDebut.strftime("%A")]))
    
    return liste_res


def get_exposant(id_exposant):
    return sessionSQL.query(Exposant).filter(Exposant.idP == id_exposant).first()

def get_invite(id_invite):
    return sessionSQL.query(Invite).filter(Invite.idP == id_invite).first()

def get_staff(id_staff):
    return sessionSQL.query(Staff).filter(Staff.idP == id_staff).first()

def get_auteur(id_auteur):
    return sessionSQL.query(Auteur).filter(Auteur.idP == id_auteur).first()

def get_presse(id_presse):
    return sessionSQL.query(Presse).filter(Presse.idP == id_presse).first()


def get_secretaire(id_secretaire):
    secretaire = sessionSQL.query(Secretaire).filter(Secretaire.idP == id_secretaire).first()
    return secretaire

def get_prenom(id_participant):
    return (sessionSQL.query(Utilisateur).filter(Utilisateur.idP == id_participant).first()).prenomP

def get_mot_de_passe(id_participant):
    print("het mdp")
    mdp = (sessionSQL.query(Utilisateur).filter(Utilisateur.idP == id_participant).first()).mdpP
    print(mdp)
    return mdp

def get_nom(id_participant):
    return (sessionSQL.query(Utilisateur).filter(Utilisateur.idP == id_participant).first()).nomP

def get_id_hotel(nom_hotel):
    return (sessionSQL.query(Hotel).filter(Hotel.nomHotel == nom_hotel).first()).idHotel


def get_id_restaurant(nom_restaurant):
    return (sessionSQL.query(Restaurant).filter(Restaurant.nomRest == nom_restaurant).first()).idRest

def get_utilisateur(id_utilisateur):
    return sessionSQL.query(Utilisateur).filter(Utilisateur.idP == id_utilisateur).first()

def affiche_participants():
    liste_participants = []
    participants = sessionSQL.query(Participant)
    for part in participants:
        liste_participants.append(part)
    return liste_participants
   

def affiche_participant_trier(trie):
     
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

def affiche_participant_trier_consommateur():
    participant = sessionSQL.query(Participant).all()
    return participant


def get_liste_nom_restaurant():
    liste_nom_resteau = []
    for nom in sessionSQL.query(Restaurant):
        liste_nom_resteau.append(nom.nomRest)
    return liste_nom_resteau


def get_liste_creneau_repas():
    liste_creneau = set()
    for creneau in sessionSQL.query(CreneauRepas):
        debut = creneau.dateDebut
        fin = creneau.dateFin
        format = format_creneau(debut, fin)
        liste_creneau.add(format)
    return list(liste_creneau)


def get_all_creneauxRepas():
    creneaux = sessionSQL.query(CreneauRepas).all()
    liste_creneaux = []
    for cren in creneaux:
        format_cren = format_creneau(cren.dateDebut, cren.dateFin)
        liste_creneaux.append(format_cren)
    return liste_creneaux


def get_nom_hotel():
    liste_nom_hotel = []
    for nom in sessionSQL.query(Hotel):
        liste_nom_hotel.append(nom.nomHotel)
    return liste_nom_hotel


def afficher_consommateur(date_jour, restaurant, midi):
    if restaurant != "Restaurant":
        restaurant = int(restaurant)
    if midi == "true":
        midi = True
    elif midi == "false":
        midi = False
    liste_consommateurs = []
    liste_creneau = []
    liste_repas = []
    liste_mangeur = []
    if restaurant != "Restaurant" and midi != "Journee":
        repas = sessionSQL.query(CreneauRepas, CreneauRepas.dateDebut, CreneauRepas.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == CreneauRepas.idCreneau).filter(Repas.idRest == restaurant).filter(Repas.estMidi == midi).all()
    elif restaurant == "Restaurant" and midi == "Journee":
        repas = sessionSQL.query(CreneauRepas, CreneauRepas.dateDebut, CreneauRepas.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == CreneauRepas.idCreneau)
    elif restaurant != "Restaurant":
        repas = sessionSQL.query(CreneauRepas, CreneauRepas.dateDebut, CreneauRepas.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == CreneauRepas.idCreneau).filter(Repas.idRest == restaurant).all()
    elif midi != "Journee":
        repas = sessionSQL.query(CreneauRepas, CreneauRepas.dateDebut, CreneauRepas.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == CreneauRepas.idCreneau).filter(Repas.estMidi == midi).all()
    
    if date_jour[0] != "Date":
        date_jour = datetime.date(int(date_jour[0]), int(date_jour[1]), int(date_jour[2]))
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
    liste_participants = get_liste_participant_idp_regime(liste_consommateurs)
    return liste_participants

def get_liste_participant_idp_regime(liste_id):
    """
    Il renvoie pour une liste de personne données tous leurs régimes sous forme de tuple
    
    :param liste_id: liste des identifiants des participants
    :return: Une liste de tuples, où chaque tuple est un participant et leur régime.
    """
    liste_participants = []
    participants = sessionSQL.query(Participant).join(Consommateur, Participant.idP == Consommateur.idP).all()
    for une_personne in participants:
        if une_personne.idP in liste_id:
            liste_participants.append((une_personne, get_regime(une_personne.idP)))
    return liste_participants


def get_navette(idP, annee) : 
    """
    Il la liste des navette utilisé par une personne à une année
    
    :param idP: l'identifiant de la personne
    :param annee: l'année de la navette
    :return: Une liste de tuples, chaque tuple contenant un objet Voyage et une chaîne représentant le
    jour de la semaine.
    """
    resultat = sessionSQL.query(Voyage).join(Transporter, Transporter.idVoy == Voyage.idVoy).filter(Transporter.idP == idP).filter(extract('year', Voyage.heureDebVoy) == annee).all()
    liste_res = []
    for res in resultat : 
        liste_res.append((res, JOURS_SEMAINES[res.heureDebVoy.strftime("%A")]))
    return liste_res

def get_regime(id_p):
    """
    Il renvoie une chaîne contenant les noms des régimes d'une personne donnée
    
    :param id_p: l'identifiant de la personne
    :return: Une chaîne contenant le nom du ou des régimes du patient avec l'identifiant donné.
    """
    str_regime = ""
    liste_regime = sessionSQL.query(Regime.nomRegime).join(Avoir, Avoir.idRegime == Regime.idRegime).filter(Avoir.idP == id_p).all()
    if len(liste_regime) == 0:
        str_regime = "Pas de régime"
    else:
        for un_regime in liste_regime:
            str_regime += str(un_regime[0]) + ", "
        str_regime = str_regime[:-2]
    return str_regime

def get_dormir(idP, annee):  
    """
    Il renvoie tous les hotels où une personne donnée dort à une année donnée

    :param idP: l'identifiant de la personne
    :param annee: l'année pour laquelle vous souhaitez obtenir les données
    :return: Une liste de tuples.
    """
    resultat = sessionSQL.query(Loger, Hotel).join(Hotel, Hotel.idHotel == Loger.idHotel).filter(Loger.idP == idP).filter(Loger.idP == idP).filter(extract('year', Loger.dateDebut)==annee).all()
    liste_res = []
    if resultat:
        for res in resultat:
            loger, hotel = res
            liste_res.append((loger, hotel, JOURS_SEMAINES[loger.dateDebut.strftime("%A")], JOURS_SEMAINES[loger.dateFin.strftime("%A")]))
    return liste_res

def id_transport_with_name(nom_transport):
    """
    Il prend un transport en entrée et retourne son id
    
    :param nom_transport: the name of the transport (avion, train, voiture, covoiturage)
    :return: L'id du transport avec le nom donné en paramètre
    """
    if nom_transport == "avion" : 
        return 1
    elif nom_transport == "train" : 
        return 2
    elif nom_transport == "voiture" : 
        return 3
    elif nom_transport == "covoiturage" :
        return 4
    

def supprime_deplacer_annee(idP, annee):
    """
    Il supprime tous les déplacements pour une personne donnée à une date données

    :param idP: l'identifiant de la personne
    :param annee: l'année des données que vous souhaitez supprimer
    """
    deplacement = sessionSQL.query(Deplacer).filter(Deplacer.idP == idP).filter(Deplacer.annee == annee)
    for dep in deplacement : 
        sessionSQL.delete(dep)
        try : 
            sessionSQL.commit()
        except : 
            sessionSQL.rollback()
            print("erreur supprimé déplacement !")



def ajoute_deplacer(idP, idTransport, lieuDepart, lieuArrive, annee) :
    """
    Affecte un déplacement à une personne
    
    :param idP: l'identifiant de la personne
    :param idTransport: 1 = voiture, 2 = train, 3 = avion, 4 = bateau
    :param lieuDepart: Le lieu de départ
    :param lieuArrive: L'endroit où la personne est arrivée
    :param annee: année
    """
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
  

def supprime_mangeur(idP):
    """
    Il supprime tous les repas pour une personne donnée de l'année actuelle
    """
    annee = datetime.datetime.now().year
    manger = sessionSQL.query(Manger).join(Repas, Manger.idRepas == Repas.idRepas).join(CreneauRepas, Repas.idCreneau == CreneauRepas.idCreneau).filter(Manger.idP == idP).filter(extract('year', CreneauRepas.dateDebut) == annee).all()
    for mang in manger :
        sessionSQL.query(Manger).filter(Manger.idP == mang.idP).filter(Manger.idRepas == mang.idRepas).delete()
        sessionSQL.commit()


def ajoute_mangeur(idP, idRepas):
    """
    Il affecte un repas à une personne
    :param idP: l'identifiant du consommateur
    :param idRepas: l'identifiant du repas
    """
    mangeur = Manger(idP, idRepas)
    manger = sessionSQL.query(Manger).join(Repas, Manger.idRepas == Repas.idRepas).join(CreneauRepas, Repas.idCreneau == CreneauRepas.idCreneau).filter(Manger.idP == idP).filter(Manger.idRepas == idRepas).first()
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
        

def suppprime_loger(idP):
    """
    Il supprime tous les logements de cette année pour une personne données
    
    :param idP: L'identifiant de la personne que vous souhaitez supprimer
    """
    annee = datetime.datetime.today().year
    loger = sessionSQL.query(Loger).filter(Loger.idP == idP).filter(extract('year', Loger.dateDebut) == annee).all()
    for log in loger :
        sessionSQL.query(Loger).filter(Loger.idP == log.idP).delete()
        sessionSQL.commit()


def ajoute_loger(idP, dateDebut, dateFin, idHotel):
    """
    Il prend l'identifiant d'une personne, une date de début, une date de fin et un identifiant d'hôtel,
    et ajoute une nouvelle ligne à la table Loger dans la base de données
    
    :param idP: l'identifiant de la personne
    :param dateDebut: La date à laquelle la personne s'est enregistrée
    :param dateFin: dateheure.dateheure(2019, 12, 31, 0, 0)
    :param idHotel: l'identifiant de l'hôtel
    """
    date_debut = datetime.datetime(dateDebut.year, dateDebut.month, dateDebut.day, dateDebut.hour, dateDebut.minute, dateDebut.second)
    date_fin = datetime.datetime(dateFin.year, dateFin.month, dateFin.day, dateFin.hour, dateFin.minute, dateFin.second)

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
        
        
def choix_hotel(idP):
    """
    Il renvoie l'identifiant de l'hôtel auquel l'utilisateur avec l'identifiant idP doit être affecté
    
    :param idP: l'identifiant de la personne qui effectue la réservation
    :return: L'identifiant de l'hôtel
    """
    return 1 #TODO
        
        
def ajoute_hebergement(idP): 
    """
    Il prend un idP comme entrée, puis trouve les dates de la conférence à laquelle le participant
    assiste, puis trouve l'hôtel dans lequel le participant séjourne, puis ajoute le participant à la
    table des logements
    
    :param idP: l'identifiant de la personne
    """
    annee = datetime.datetime.today().year
    dates = sessionSQL.query(Assister.dateArrive, Assister.dateDepart).filter(Assister.idP == idP).filter(extract('year', Assister.dateArrive) == annee).first()
    dateDebut = dates[0]
    dateFin = dates[1]
    idHotel = choix_hotel(idP)
    ajoute_loger(idP, dateDebut, dateFin, idHotel)
        
def get_max_id_regime(): 
    """
    Il renvoie la valeur idRegime maximale de la table Regime dans la base de données
    :return: L'idRegime maximum de la table Regime.
    """
    regime= sessionSQL.query(func.max(Regime.idRegime)).first()
    if (regime[0]) is None:
        return 0
    else:
        return regime._data[0]
        
        
def get_assister(idP, annee):
    """
    Il renvoie si la personne assiste au féstival pour une année donnée
    
    :param idP: l'identifiant du patient
    :param annee: l'année de la saison
    :return: la personne assiste au féstival pour une année donnée
    """
    return sessionSQL.query(Assister).filter(Assister.idP == idP).filter(extract('year', Assister.dateArrive) == annee).first()

def possede_regime(idP) -> bool :
    """
    > La fonction renvoie si la personne possede un régime ou non
    
    :param idP: l'identifiant de la personne
    """
    res = sessionSQL.query(Avoir.idRegime).filter(Avoir.idP == idP).first()
    if res is not None : 
        return res[0]
    else : 
        return None

def update_regime(idR, new_regime) :    
    """
    > Met à jour le nom du régime pour un identifiant donnée
    
    :param idR: l'identifiant du régime que vous souhaitez mettre à jour
    :param new_regime: le nom du nouveau régime
    :return: Le nombre de lignes mises à jour.
    """
    return sessionSQL.query(Regime).filter(Regime.idRegime == idR).update({Regime.nomRegime : new_regime})

def ajoute_regime(regime) :
    """
    Ajoute un regime à la base de données si il n'existe pas
    
    
    :param regime: le nom du régime
    :return: L'identité du régime
    """
    id_regime = get_max_id_regime()+1
    regime_existant = sessionSQL.query(Regime.idRegime).filter(Regime.nomRegime == regime).all() != []
    if regime_existant : 
        return regime_existant[0]
    else : 
        regime = Regime(id_regime, regime)
        sessionSQL.add(regime)
        print("l1276")
        try :
            sessionSQL.commit()
            return id_regime
        except : 
            print("erreur")
            sessionSQL.rollback() 
        
        
def supprime_regime(idP, idR) : 
    """
    Il supprime le régime pour une personne donnée
    
    :param idP: l'identifiant du patient
    :param idR: l'identité du régime
    """
    sessionSQL.query(Avoir).filter(Avoir.idP == idP).delete()
    sessionSQL.query(Regime).filter(Regime.idRegime == idR).delete()

        
def ajoute_avoir_regime(id_consommateur, id_regime) :
    """
    Il ajoute un régime à une personne donnée
    
    :param id_consommateur: L'identifiant du consommateur
    :param id_regime: l'id du régime
    """
    avoir_regime = Avoir(id_consommateur, id_regime)
    sessionSQL.add(avoir_regime)
    try :
        sessionSQL.commit()
        print("L'association regime-consommateur à bien été ajoutée !")
    except : 
        print("erreur")
        sessionSQL.rollback()
    
def est_intervenant(idP):
    """
    Il renvoie Vrai si la personne avec l'idP donné est un intervenant, Faux sinon
    
    :param idP: l'identifiant de la personne
    :return: Une valeur booléenne.
    """
    intervenant = sessionSQL.query(Intervenant).filter(Intervenant.idP == idP).first()
    return intervenant is not None
            
def est_secretaire(idP):
    """
    Il renvoie True si la personne avec l'identifiant donné est une secrétaire, et False sinon
    
    :param idP: l'identifiant de la personne
    :return: Une valeur booléenne.
    """
    secretaire = get_secretaire(idP)
    return secretaire is not None
        
def requete_transport_annee2(idP, annee) : 
    """
    Il renvoie tous les transport utilisé par une personne au cours d'une année
    
    :param idP: l'identifiant de la personne
    :param annee: l'année pour laquelle vous souhaitez obtenir les données
    :return: Une liste de tuples de la forme (Deplacer, Transport)
    """
    return sessionSQL.query(Deplacer, Transport).join(Transport, Transport.idTransport == Deplacer.idTransport).filter(Deplacer.idP == idP).filter(Deplacer.annee == annee).all()
    



def ajoute_assister(idP, dateArrive, dateDepart):
    """
    Si la personne n'a pas de date d'arrivé et de départ les ajoutes sinon
    cela les met à jour
    
    :param idP: L'identifiant de la personne
    :param dateArrive: La date à laquelle la personne est arrivée à l'événement
    :param dateDepart: La date à laquelle la personne a quitté le projet
    """
    assisteur = Assister(idP, dateArrive, dateDepart)
    assister = sessionSQL.query(Assister).filter(extract('year', Assister.dateArrive) == dateArrive.year).filter(Assister.idP == idP).first()
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

def modif_participant_remarque(idP, remarques) : 
    """
    Cette fonction prend un idP et une chaîne de remarques, et si la chaîne est alphabétique, elle
    ajoute les remarques aux remarques existantes du participant avec l'idP donné.
    
    La fonction renvoie True si les remarques ont été ajoutées avec succès, et False sinon.
    
    :param idP: l'identifiant du participant
    :param remarques: les nouvelles remarques à ajouter au participant
    """
    if remarques.isalpha():
        nouvelles_remarques = remarques + " / "+str((sessionSQL.query(Participant).filter(Participant.idP == idP).first()).remarques)
        sessionSQL.query(Participant).filter(Participant.idP == idP).update({Participant.remarques : nouvelles_remarques})
    try : 
        sessionSQL.commit()
        return True
    except : 
        print("erreur modif remarques")
        return False


def get_utilisateur_email_mdp(mail, mdp):
    """
    Il renvoie le mot de passe de l'utilisateur de la base de données dont l'e-mail et le mot de passe
    correspondent à ceux donnés en paramètres
    
    :param mail: l'email de l'utilisateur
    :param mdp: Le mot de passe que vous souhaitez utiliser
    :return: L'utilisateur qui correspond à l'e-mail et au mot de passe
    """
    utilisateur = sessionSQL.query(Utilisateur).filter(Utilisateur.emailP == mail).filter(Utilisateur.mdpP == mdp).first()
    if utilisateur is not None :
        return utilisateur
    

@staticmethod
def transforme_datetime(date):
    """
    Il prend une date sous forme de chaîne et la renvoie sous forme d'une liste d'entiers
    
    :param date: La date en string
    :return: Une liste de la date divisée par le "-" ou "/"
    """
    if "-" in date:
        date = date.split("-")
    elif "/" in date:
        date = date.split("/")
    return date

def ajoute_creneau_repas_v1(dateDebut,dateFin):
    """
    Il ajoute un créneau horaire de repas à la base de données
    
    :param dateDebut: la date de début du créneau repas
    :param dateFin: La date de fin du créneau repas
    :return: L'id du créneau
    """
    liste_date_deb = transforme_datetime(dateDebut)
    liste_date_fin = transforme_datetime(dateFin)
    dateDebut = datetime.datetime(int(liste_date_deb[0]), int(liste_date_deb[1]), int(liste_date_deb[2]), int(liste_date_deb[3]), int(liste_date_deb[4]),int(liste_date_deb[5]))
    dateFin = datetime.datetime(int(liste_date_fin[0]), int(liste_date_fin[1]), int(liste_date_fin[2]), int(liste_date_fin[3]), int(liste_date_fin[4]), int(liste_date_fin[5]))
    creneau_test = sessionSQL.query(CreneauRepas).filter(CreneauRepas.dateDebut == dateDebut).filter(CreneauRepas.dateFin == dateFin).first()
    if creneau_test is None :
        idCreneau = get_max_id_creneau_repas()+1
        creneau = CreneauRepas(idCreneau, dateDebut, dateFin)
        sessionSQL.add(creneau)
        try :
            sessionSQL.commit()
        except :
            print("erreur creneau")
            sessionSQL.rollback()
        return creneau.idCreneau
    return creneau_test.idCreneau

def ajoute_creneau_travail_v1(dateDebut,dateFin):
    """
    Il ajoute un créneau de travail à la base de données
    
    :param dateDebut: La date de début du créneau de travail
    :param dateFin: La date de fin du créneau de travail
    :return: L'id du créneau
    """
    liste_date_deb = transforme_datetime(dateDebut)
    liste_date_fin = transforme_datetime(dateFin)
    dateDebut = datetime.datetime(int(liste_date_deb[0]), int(liste_date_deb[1]), int(liste_date_deb[2]), int(liste_date_deb[3]), int(liste_date_deb[4]),int(liste_date_deb[5]))
    dateFin = datetime.datetime(int(liste_date_fin[0]), int(liste_date_fin[1]), int(liste_date_fin[2]), int(liste_date_fin[3]), int(liste_date_fin[4]), int(liste_date_fin[5]))
    creneau_test = sessionSQL.query(CreneauTravail).filter(CreneauTravail.dateDebut == dateDebut).filter(CreneauTravail.dateFin == dateFin).first()
    if creneau_test is None :
        idCreneau = get_max_id_creneau_travail()+1
        creneau = CreneauTravail(idCreneau, dateDebut, dateFin)
        sessionSQL.add(creneau)
        try :
            sessionSQL.commit()
        except :
            print("erreur creneau")
            sessionSQL.rollback()
        return creneau.idCreneau
    return creneau_test.idCreneau


def ajoute_creneau_repas(date_debut, date_fin):
    """
    Il ajoute un nouveau créneau horaire de repas à la base de données s'il n'existe pas déjà
    
    :param date_debut: la date de début du créneau repas
    :param date_fin: La date de fin de la période de repas
    :return: L'id du créneau
    """
    creneau_test = sessionSQL.query(CreneauRepas).filter(CreneauRepas.dateDebut == date_debut).filter(CreneauRepas.dateFin == date_fin).first()
    if creneau_test is None :
        idCreneau = get_max_id_creneau_repas()+1
        creneau = CreneauRepas(idCreneau, date_debut, date_fin)
        sessionSQL.add(creneau)
        try :
            sessionSQL.commit()
        except : 
            print("erreur creneau")
            sessionSQL.rollback()
        return creneau.idCreneau
    else : 
        print("un creneau similaire existe déjà")
        return creneau_test.idCreneau

def ajoute_creneau_travail(date_debut, date_fin):
    """
    Il ajoute un nouveau créneau de travail à la base de données s'il n'existe pas déjà
    
    :param date_debut: la date de début du créneau de travail
    :param date_fin: La date de fin du créneau de travail
    :return: L'id du créneau
    """
    creneau_test = sessionSQL.query(CreneauTravail).filter(CreneauTravail.dateDebut == date_debut).filter(CreneauTravail.dateFin == date_fin).first()
    if creneau_test is None :
        idCreneau = get_max_id_creneau_travail()+1
        creneau = CreneauTravail(idCreneau, date_debut, date_fin)
        sessionSQL.add(creneau)
        try :
            sessionSQL.commit()
        except : 
            print("erreur creneau")
            sessionSQL.rollback()
        return creneau.idCreneau
    else : 
        print("un creneau similaire existe déjà")
        return creneau_test.idCreneau    

def ajoute_repas(estMidi,idRest,idCreneau) : 
    """
    Il ajoute un nouveau repas à la base de données s'il n'existe pas déjà
    
    :param estMidi: Vrai si c'est un déjeuner, Faux si c'est un dîner
    :param idRest: l'identifiant du restaurant
    :param idCreneau: l'identifiant du créneau horaire
    :return: L'identifiant du repas
    """
    repas_verif = sessionSQL.query(Repas).filter(Repas.estMidi == estMidi).filter(Repas.idRest == idRest).filter(Repas.idCreneau == idCreneau).first()
    if repas_verif is None :
        idRepas = get_max_id_repas()+1
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

def ajoute_restaurant(nomRest) : 
    """
    Il ajoute un restaurant à la base de données s'il n'existe pas déjà
    
    :param nomRest: Le nom du restaurant
    :return: L'identifiant du restaurant
    """
    restaurant_test = sessionSQL.query(Restaurant).filter(Restaurant.nomRest == nomRest).first()
    if restaurant_test is None :
        idRestaurant = get_max_id_restaurant()+1
        restaurant = Restaurant(idRestaurant, nomRest)
        sessionSQL.add(restaurant)
        try : 
            sessionSQL.commit()
        except : 
            print("erreur restaurant")
            sessionSQL.rollback()
    return restaurant_test.idRest

   
 
def ajoute_repas_mangeur(idP, liste_repas, liste_horaire_restau, dico_horaire_restau):
    """
    Il ajoute un repas à une personne
    
    :param idP: l'identifiant de la personne
    :param liste_repas: une liste de booléens, un pour chaque repas, indiquant si la personne veut
    manger à ce repas
    :param liste_horaire_restau: une liste de chaînes, chaque chaîne est le nom d'un restaurant
    :param dico_horaire_restau: un dictionnaire de la forme {'midi': '12:00/14:00', 'soir':
    '19:00/21:00'}
    """
    supprime_mangeur(idP)
    for i in range(0, len(liste_repas)):
        if liste_repas[i] == 'true':
            horaire = dico_horaire_restau[liste_horaire_restau[i]]
            idCreneau = ajoute_creneau_repas_v1(horaire.split("/")[0], horaire.split("/")[1])
            idRepas = ajoute_repas(False if liste_horaire_restau[i][-4:] == "soir" else True, 1 if liste_horaire_restau[i][-4:] == "soir" else 1 , idCreneau)
            ajoute_mangeur(idP, idRepas)

def invite_un_participant(idP):
    """
    Il met à jour la valeur de la colonne "invite" de la table "Participant" à True pour la personne
    donnée
    
    :param idP: L'identifiant du participant
    """
    sessionSQL.query(Participant).filter(Participant.idP == idP).update(
        {Participant.invite : True})
    sessionSQL.commit()

def voyage_est_complet(voyage):
    """
    Elle renvoie Vrai si le voyage est complet
    
    :param voyage: le voyage que nous voulons vérifier
    :return: Une valeur booléenne
    """
    nb_place_dispo = sessionSQL.query(Navette).filter(Navette.idNavette == voyage.idNavette).first().capaciteNavette
    voyageurs = sessionSQL.query(Transporter).filter(Transporter.idVoy == voyage.idVoy).all()
    return (voyageurs is not None and len(voyageurs)>=nb_place_dispo)

def get_navette_dispo(heureDeb, heureFin):
    """
    Il renvoie l'identifiant de la première navette qui n'est pas déjà réservée pour l'intervalle de
    temps donné
    
    :param heureDeb: l'heure à laquelle le voyage commence
    :param heureFin: l'heure à laquelle le voyage se termine
    :return: L'identifiant de la première navette disponible
    """
    voyages = sessionSQL.query(Voyage).filter((Voyage.heureDebVoy <= heureFin) &
                              (Voyage.heureDebVoy+Voyage.DureeVoy >= heureDeb) &
                              func.date(Voyage.heureDebVoy) == heureDeb.date()).all()
    navette_ids = {voyage.idNavette for voyage in voyages}
    navettes = sessionSQL.query(Navette).all()
    for navette in navettes:
        if not navette.idNavette in navette_ids:
            return navette.idNavette
    


def cree_un_voyage(heureDebVoy, directionGARE):
    """
    Il crée un nouveau voyage, et renvoie son identifiant
    
    :param heureDebVoy: le temps du voyage
    :param directionGARE: Vrai si la navette va à la gare, Faux si elle va à l'aéroport
    :return: L'identifiant du nouveau voyage
    """
    id_navette_dispo = get_navette_dispo(heureDebVoy, heureDebVoy+datetime.timedelta(minutes=10))
    nouvelle_id_voyage = get_max_id_voyage()+1
    if id_navette_dispo is not None:
        if directionGARE : 
            t = datetime.time(0,20)
            t0 = datetime.time(0,0)
            dt = datetime.datetime.combine(heureDebVoy.date(), t)
            dt2 = datetime.datetime.combine(heureDebVoy.date(), t0)
            diff = heureDebVoy - dt
            # Ajouter la différence à l'objet datetime d'origine
            heureDebVoy2 = dt2 + diff

        else : 
            heureDebVoy2 = heureDebVoy
        sessionSQL.add(Voyage(nouvelle_id_voyage, heureDebVoy2, datetime.time(0, 10, 0), directionGARE, id_navette_dispo))
        sessionSQL.commit()
        return nouvelle_id_voyage

def supprimer_intervenant_voyage_navette(idP):
    """
    Il supprime tous les voyages en navette pour une personne données
    
    :param idP: l'identifiant de la personne à supprimer de la base de données
    """
    annee_en_cours =  datetime.date.today().year
    transports = sessionSQL.query(Transporter).filter(Transporter.idP == idP).all()
    for transport in transports:
        voyage = sessionSQL.query(Voyage).filter((Voyage.idVoy == transport.idVoy)  & (extract('year', Voyage.heureDebVoy) == annee_en_cours) ).first()
        if voyage is not None:
            sessionSQL.delete(transport)
            sessionSQL.commit()
            nb_voyageurs = len(sessionSQL.query(Transporter).filter(Transporter.idVoy == voyage.idVoy).all())
            if nb_voyageurs == 0:
                sessionSQL.delete(voyage)
                sessionSQL.commit()
                
def affecter_intervenant_voyage_depart_gare(idP):
    """
    Il prend l'identité d'une personne comme argument, et lui affecte une navette pour le voyage entre la gare et le festival
    
    :param idP: l'identifiant de la personne
    :return: Vrai si il a bien était affecté
    """
    annee_en_cours =  datetime.date.today().year
    date_arrive = sessionSQL.query(Assister).filter((Assister.idP == int(idP)) & (extract('year', Assister.dateArrive) == annee_en_cours)).first().dateArrive
    if date_arrive is None:
        print("Pas de date d'arrive")
        return None
    voyages_dispo = sessionSQL.query(Voyage).filter(Voyage.directionGare == False).filter(Voyage.heureDebVoy.between(date_arrive-datetime.timedelta(seconds=1), date_arrive+datetime.timedelta(minutes=10,seconds=1))).all()
    print("voy dispo ",voyages_dispo)
    if voyages_dispo is not None:
        for voyage in voyages_dispo:
            if not voyage_est_complet(voyage) and not voyage.directionGare:
                print("ici")
                print(idP, voyage.idVoy)
                sessionSQL.add(Transporter(idP, voyage.idVoy))
                sessionSQL.commit()
                return True
    id_voyage = cree_un_voyage(date_arrive, False)
    sessionSQL.add(Transporter(idP, id_voyage))
    sessionSQL.commit()
    return True

def affecter_intervenant_voyage_depart_festival(idP):
    """
    Il prend l'identité d'une personne comme argument, et lui affecte une navette pour le voyage entre le festival et la gare
    
    :param idP: l'identifiant de la personne
    :return: Vrai si il a bien était affecté
    """
    annee_en_cours =  datetime.date.today().year
    date_depart = sessionSQL.query(Assister).filter((Assister.idP == idP) & (extract('year', Assister.dateDepart) == annee_en_cours)).first().dateDepart
    if date_depart is None:
        print("Pas de date de depart")
        return None
    voyages_dispo = sessionSQL.query(Voyage).filter(Voyage.directionGare == True).filter(Voyage.heureDebVoy.between(date_depart-datetime.timedelta(seconds=1), date_depart+datetime.timedelta(minutes=10,seconds=1))).all()
    if voyages_dispo is not None:
        for voyage in voyages_dispo:
            if not voyage_est_complet(voyage) and voyage.directionGare:
                sessionSQL.add(Transporter(idP, voyage.idVoy))
                sessionSQL.commit()
                return True
    id_voyage = cree_un_voyage(date_depart, True)
    sessionSQL.add(Transporter(idP, id_voyage))
    sessionSQL.commit()
    return True

def liste_datetime_horaire_restaurant() : 
    """
    Il convertit le dictionnaire des heures d'ouverture en une liste de tuples, chaque tuple contenant
    les heures d'ouverture et de fermeture du restaurant pour un jour donné
    :return: Une liste de tuples.
    """
    res = list()
    for (jour, creneau) in DICO_HORAIRE_RESTAURANT.items() : 
        deb, fin = creneau.split("/")
        res.append((string_to_datetime(deb), string_to_datetime(fin), jour))
    return res

def get_repas_present(idP, annee) : 
    """
    > La fonction `get_repas_present` prend en entrée l'id d'une personne et l'année de l'événement, et
    renvoie une liste de chaînes représentant les repas auxquels la personne sera présente
    
    :param idP: l'identifiant du participant
    :param annee: l'année de l'événement
    :return: liste_creneau_repas_present est une liste de chaînes.
    """
    liste_creneau_repas_present = list()
    assister = get_assister(idP, annee)
    date_arrive = assister.dateArrive
    date_depart = assister.dateDepart # look like : (datetime.datetime(2023, 11, 16, 19, 30)
    liste_creneau = liste_datetime_horaire_restaurant() # liste sous cette forme : [(datetime.datetime(2023, 11, 16, 19, 30), datetime.datetime(2023, 11, 16, 22, 0), 'jeudi_soir'), ...]
    for creneau in liste_creneau : 
        if date_arrive <= creneau[0] and date_depart > creneau[1]:
            liste_creneau_repas_present.append(creneau[2])
    return liste_creneau_repas_present

@login_manager.user_loader
def load_user(participant_id):
    """
    Si l'utilisateur est une secrétaire, retourner l'objet secrétaire, sinon retourner l'objet
    participant
    
    :param participant_id: L'identifiant de l'utilisateur à charger
    :return: L'objet utilisateur
    """
    # since the user_id is just the primary key of our user table, use it in the query for the user
    if est_secretaire(participant_id):
        return get_secretaire(participant_id)
    else:
        return get_participant(participant_id)

def reiniatilise_invitation(): 
    """
    Il prend tous les participants dans la base de données et définit leur statut d'invitation sur faux.
    
    Ceci est utile si vous souhaitez réinviter tous les participants de la base de données.
    """
    participants = sessionSQL.query(Participant).all()
    for p in participants : 
        sessionSQL.query(Participant).filter(Participant.idP == p.idP).update({Participant.invite : False})
        sessionSQL.commit()
        
@staticmethod
def string_to_datetime(s):
    """
    Il prend une chaîne au format 'AAAA-MM-JJ-HH-MM-SS' et renvoie un objet datetime
    
    :param s: la chaîne à convertir
    :return: Un objet datetime
    """
    return datetime.datetime.strptime(s, '%Y-%m-%d-%H-%M-%S')


def get_date_heure_arrive_intervenant(idP):
    """
    Il renvoie la date et l'heure d'arrivée de la personne avec l'idP donné
    
    :param idP: l'identifiant de la personne
    :return: La date et l'heure d'arrivée de l'intervenant auprès de l'idP
    """
    annee_en_cours =  datetime.date.today().year
    return sessionSQL.query(Assister).filter((Assister.idP == int(idP)) & (extract('year', Assister.dateArrive) == annee_en_cours) ).first().dateArrive

def get_date_heure_depart_intervenant(idP):
    """
    Il renvoie la date et l'heure de départ de la personne avec l'idP donné
    
    :param idP: l'identifiant de la personne
    :return: La date et l'heure de départ de l'intervenant avec l'idP = idP
    """
    annee_en_cours =  datetime.date.today().year
    return sessionSQL.query(Assister).filter((Assister.idP == int(idP)) & (extract('year', Assister.dateDepart) == annee_en_cours)).first().dateDepart


def cree_mail(id_participant):
    """
    Il crée un contenu de courrier pour un participant
    
    :param id_participant: L'identifiant du participant auquel vous souhaitez envoyer un e-mail
    :return: Le contenu du courrier
    """
    status = get_role(id_participant)
    nom = get_nom(id_participant)
    prenom = get_prenom(id_participant)
    mdp = get_mot_de_passe(id_participant)
    content = Content("text/plain",
    "Cher(e)"+prenom +" "+nom+", Nous avons le plaisir de vous inviter au festival bdBOUM en tant qu'"+ status+", un événement incontournable pour les fans de bandes dessinées.\
 Cette année, le festival se déroulera du vendredi 17 Novembre au Dimanche 19 Novembre 2023, à Blois.\ Durant ces trois jours, vous aurez l'opportunité de découvrir\
 les dernières tendances en matière de BD, de rencontrer des auteurs talentueux et de participer à des activités ludiques et éducatives.\
 Nous espérons que vous pourrez vous joindre à nous pour célébrer la passion de la BD et passer un moment inoubliable en notre compagnie.\n\
 Votre mot de passe est le suivant pour vous connecter au site : "+mdp+"\n\
 Bien cordialement,\n\
 L'équipe BDBOUM")
    return content

@staticmethod
def generate_password(length=8):
    """
    Il génère un mot de passe aléatoire d'une longueur donnée
    
    :param length: La longueur du mot de passe à générer. La valeur par défaut est 8, defaults to 8
    (optional)
    :return: Une chaîne de caractères aléatoires
    """
    # Get a list of all the ASCII lowercase letters, uppercase letters, and digits
    characters = string.ascii_letters + string.digits + string.punctuation
    # Use the random.sample function to get a list of `length` random elements from the list of characters
    password = ''.join(random.sample(characters, length))
    return password


@staticmethod
def get_heure(time) :
    """
    Il prend une chaîne de la forme "hh:mm" et renvoie un tuple de la forme (hh, mm)
    
    :param time: l'heure de la journée, au format HH:MM:SS
    :return: L'heure et la minute du temps.
    """
    heure = time.split(':')[0]
    minute = time.split(':')[1][0:2]
    return (heure, minute)
    

@staticmethod
def get_all_lieu_train(file_path="./Developpement/app/static/txt/gare.txt"): 
    """
    Il ouvre le fichier, lit toutes les lignes et renvoie une liste des lignes
    
    :param file_path: Le chemin d'accès au fichier que vous voulez lire, defaults to
    ./Developpement/app/static/txt/gare.txt (optional)
    :return: Une liste de toutes les gares de France
    """
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        return [line.strip() for line in lines]
    

@staticmethod
def get_all_lieu_avion(file_path="./Developpement/app/static/txt/aeroport.txt"): 
    """
    > La fonction `get_all_lieu_avion` prend en argument un chemin de fichier et renvoie la liste de
    toutes les lignes du fichier
    
    :param file_path: Le chemin d'accès au fichier que vous voulez lire, defaults to
    ./Developpement/app/static/txt/aeroport.txt (optional)
    :return: Une liste de tous les aéroports du monde.
    """
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        return [line.strip() for line in lines]
    

def date_str_datetime(date_str):
    """
    Il prend une chaîne au format jj/mm/aaaa et renvoie un objet datetime
    
    :param date_str: La chaîne de date que vous souhaitez convertir en objet datetime
    :return: Un objet datetime
    """
    date_format = "%d/%m/%Y"
    date_object = datetime.datetime.strptime(date_str, date_format)
    return date_object

def datetime_str_to_datetime(date_str, heure_str):
    """
    Il prend une chaîne de date et une chaîne d'heure, et renvoie un objet datetime
    
    :param date_str: La date au format chaîne
    :param heure_str: La chaîne d'heure, au format "HH:MM"
    :return: Un objet datetime
    """
    date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
    time_obj = datetime.datetime.strptime(heure_str, "%H:%M")

    # Combiner la date et l'heure pour créer un objet datetime unique
    datetime_obj = datetime.datetime.combine(date_obj.date(), time_obj.time())
    return datetime_obj