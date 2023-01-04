from dataclasses import dataclass
from email.headerregistry import DateHeader
from logging import exception
from shutil import register_unpack_format
from sqlite3 import DatabaseError
from statistics import quantiles
from wsgiref.validate import PartialIteratorWrapper
import sqlalchemy
from sqlalchemy import func
from sqlalchemy import create_engine, cast
from sqlalchemy import Column , Integer, Text , Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from datetime import date

from .Exposant import Exposant
from .Intervenir import Intervenir
from .Consommateur import Consommateur
from .Staff import Staff
from .Intervenant import Intervenant
from .Auteur import Auteur
from .Presse import Presse
from .Invite import Invite
from .Participant import Participant
from .Loger import Loger
from .Hotel import Hotel
from .Deplacer import Deplacer
from .Manger import Manger
from .Repas import Repas
from .Creneau import Creneau
from .Restaurant import Restaurant
from .Avoir import Avoir
from .Regime import Regime
from .Assister import Assister
from .Secretaire import Secretaire
from .Navette import Navette
from .Transporter import Transporter
from .Voyage import Voyage
from .Mobiliser import Mobiliser
from .Transport import Transport
from .Utilisateur import Utilisateur

from .app import login_manager
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

#connexion ,engine = ouvrir_connexion("nardi","nardi",'servinfo-mariadb', "DBnardi")
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
session = Session()


def get_deb_voyage(session, idVoyage):
    row = session.query(Voyage.heureDebVoy).filter(Voyage.idVoy == idVoyage).first()
    return row[0]

def get_lieu_depart_voyage(session, idVoyage):
    if (session.query(Voyage).filter(Voyage.idVoy == idVoyage).first()).directionGare:
        return "Festival → Gare Blois"
    else:
        return "Gare Blois → Festival"

def get_max_id_participant(session):
    max_id = session.query(func.max(Participant.idP)).first()
    
    if (max_id[0]) is None:
        return 0
    else:
        return max_id[0]

def get_max_num_stand(session):
    max_num = session.query(func.max(Exposant.numStand)).first()
    if (max_num[0]) is None:
        return 0
    else:
        return max_num._data[0]

def ajoute_particpant(session, idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques):
    participant = Participant(idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques)
    personneP = session.query(Participant).filter(Participant.idP == participant.idP).first()
    if personneP is None:
        participant.idP = get_max_id_participant(session) + 1
        session.add(participant)
        try:
            session.commit()
            print("La Participant "+ str(participant) +" a bien été inséré dans la base de donnée")
        except:
            print("Erreur")
    else:
        print("Une personne a déjà cet identifiant dans la base de donnée")
        
def ajoute_participant_id(session, idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques):
    participant = Participant(idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques)
    personneP = session.query(Participant).filter(Participant.idP == participant.idP).first()
    if personneP is None:
        participant.idP = participant.idP
        session.add(participant)
        try:
            session.commit()
            print("La Participant "+ str(participant) +" a bien été inséré dans la base de donnée")
        except:
            print("Erreur")
    else:
        print("Une personne a déjà cet identifiant dans la base de donnée")
    
def ajoute_Consommateur(session, idP):
    consommateur = Consommateur(idP)
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

def ajoute_exposant(session, idP, numStand):
    exposant = Exposant(idP, numStand)
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

def ajoute_staff(session, idP):
    staff = Staff(idP)
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
            session.rollback()
    else:
        print("Un staff a déjà cet identifiant dans la base de donnée")
        
def ajoute_intervenant(session, idP):
    intervenant = Intervenant(idP)
    intervenantI = session.query(Intervenant).filter(Intervenant.idP == intervenant.idP).first()
    if intervenantI is None:
        personne = session.query(Participant).filter(Participant.idP == intervenant.idP).first()
        session.add(intervenant)
        try:
            session.commit()
            print("La personne " + str(personne) + " est devenu un(e) intervenant(e)")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Un intervenant a déjà cet identifiant dans la base de donnée")
    
def ajoute_auteur(session, idP):
    auteur = Auteur(idP)
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
            session.rollback()
    else:
        print("Un auteur a déjà cet identifiant dans la base de donnée")

def ajoute_presse(session, idP):
    presse = Presse(idP)
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
            session.rollback()
    else:
        print("Une personne de la presse a déjà cet identifiant dans la base de donnée")

def ajoute_invite(session, idP):
    invite = Invite(idP)
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
        

def ajoute_participant_role(session, participant, role):
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

def ajoute_participant_role_id(session, participant, role):
    if role in ROLE:
        ajoute_participant_id(session, participant)
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


def ajoute_intervention(session, idP, idCreneau, idLieu, nomIntervention, descIntervention):
    intervenir = Intervenir(idP, idCreneau, idLieu, nomIntervention, descIntervention)
    intervention = session.query(Intervenir).filter(Intervenir.idP == intervenir.idP).filter(Intervenir.idCreneau == intervenir.idCreneau).first()
    if intervention is None:
        session.add(intervenir)
        try:
            session.commit()
            print("L'intervention " + str(intervenir) + " est maintenant créée !")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Une intervention a déjà lieu à ce créneau pour cette personne")

def ajouter_navette(session, idNavette, nomNavette, capaciteNavette):
    navette = Navette(idNavette, nomNavette, capaciteNavette)
    navette_existe = session.query(Navette).filter(Navette.idNavette == idNavette).first()
    if navette_existe is None:
        session.add(navette)
        try:
            session.commit()
            print("Une nouvelle navette " + nomNavette + " a été créée")
        except:
            print("Erreur")
            session.rollback()
    else:
        print("Une navette à déjà cet id")


#FONCTION A TESTER AVEC DES INSERTIONS
def supprimer_personne_transporter(session, idP, idVoyage):
    liste_personne = session.query(Transporter.idP).filter(Transporter.idVoy == idVoyage).all()
    if len(liste_personne) == 1:
        session.query(Transporter).filter(Transporter.idP == idP).filter(Transporter.idVoy == idVoyage).delete()
        session.query(Voyage).filter(Voyage.idVoy == idVoyage).delete()
        session.query(Mobiliser).filter(Mobiliser.idVoy == idVoyage).delete()
        session.commit()
        print("Le transport a été supprimé car cette personne était seul dans ce voyage")
    else:
        session.query(Transporter).filter(Transporter.idP == idP).filter(Transporter.idVoy == idVoyage).delete()
        session.commit()
        print("Cette personne a bien été supprimé du voyage")


# ajoute_intervention(session, 300, 1, 1, "Dédicace", "Séance de dédicace avec les spectateurs")
        
        
def supprimer_participant(session, id_participant):
    session.query(Participant).filter(Participant.idP == id_participant).delete()
    session.commit()
    print("Le participant a été supprimé")

def supprimer_consommateur(session, id_consommateur):
    session.query(Consommateur).filter(Consommateur.idP == id_consommateur).delete()
    session.commit()
    print("Le consommateur a été supprimé")

def supprimer_intervenant(session, id_intervenant):
    session.query(Intervenant).filter(Intervenant.idP == id_intervenant).delete()
    session.commit()
    print("L'intervenant a été supprimé")

def supprimer_exposant(session, id_exposant):
    session.query(Exposant).filter(Exposant.idP == id_exposant).delete()
    session.commit()
    print("L'exposant a été supprimé")
  
def supprimer_staff(session, id_staff):
    session.query(Staff).filter(Staff.idP == id_staff).delete()
    session.commit()
    print("Le staff a été supprimé")

def supprimer_auteur(session, id_auteur):
    session.query(Auteur).filter(Auteur.idP == id_auteur).delete()
    session.commit()
    print("L'auteur a été supprimé")

def supprimer_presse(session, id_presse):
    session.query(Presse).filter(Presse.idP == id_presse).delete()
    session.commit()
    print("Le membre de la presse a été supprimé")

def supprimer_invite(session, id_invite):
    session.query(Invite).filter(Invite.idP == id_invite).delete()
    session.commit()        
    print("L'invité a été supprimé")
     
def supprimer_participant_role(session, id_participant):
    participant_existe = session.query(Participant).filter(Participant.idP == id_participant).first()
    if participant_existe is not None:
        exposant = session.query(Exposant).filter(Exposant.idP == id_participant).first()
        staff = session.query(Staff).filter(Staff.idP == id_participant).first()
        auteur = session.query(Auteur).filter(Auteur.idP == id_participant).first()
        presse = session.query(Presse).filter(Presse.idP == id_participant).first()
        invite = session.query(Invite).filter(Invite.idP == id_participant).first()
        if exposant is not None:
            supprimer_exposant(session, id_participant)
        else:
            if staff is not None:
                supprimer_staff(session, id_participant)
            else:
                if auteur is not None:
                    supprimer_auteur(session, id_participant)
                elif presse is not None:
                    supprimer_presse(session, id_participant)
                elif invite is not None:
                    supprimer_invite(session, id_participant)
                supprimer_intervenant(session, id_participant)
            supprimer_consommateur(session, id_participant)
        supprimer_participant(session, id_participant)
    else:
        print("La personne que vous voulez supprimer n'existe pas")

     
def modifier_participant(session, idP, prenomP, nomP, ddnP, telP, emailP):
    session.query(Participant).filter(Participant.idP == idP).update(
        {Participant.prenomP : prenomP, Participant.nomP : nomP, Participant.ddnP : ddnP, 
         Participant.telP : telP, Participant.emailP : emailP})
    session.commit()
    print("Le participant a bien été modifié")
    

def modifier_participant_tout(session, idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques):
    session.query(Participant).filter(Participant.idP == idP).update(
        {Participant.prenomP : prenomP, Participant.nomP : nomP, Participant.ddnP : ddnP, 
         Participant.telP : telP, Participant.emailP : emailP, Participant.adresseP : adresseP, Participant.mdpP : mdpP,
         Participant.invite : invite, Participant.emailEnvoye : emailEnvoye, Participant.remarques : remarques})
    session.commit()
    print("Le participant a bien été modifié")
   

def modifier_participant_role(session, idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques, metier):
    participant = Participant(idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, invite, emailEnvoye, remarques)
    ancien_participant = Participant(participant.idP, participant.prenomP, participant.nomP, participant.ddnP, participant.telP, participant.emailP, participant.mdpP, participant.remarques, participant.invite, participant.emailEnvoye)
    supprimer_participant_role(session, participant.idP)
    ajoute_participant_role_id(session, ancien_participant, metier)
    print("Le role du participant a bien été modifié")

def modif_loger(session, ancien_loger, nouveau_loger):
    session.query(Loger).filter(Loger.idP == ancien_loger.idP).filter(Loger.idHotel == ancien_loger.idHotel).filter(Loger.dateDebut == ancien_loger.dateDebut).update({
        Loger.dateDebut : nouveau_loger.dateDebut, Loger.dateFin : nouveau_loger.dateFin, Loger.idHotel : nouveau_loger.idHotel})
    session.commit()
    print("Le logement de cette personne a bien été modifié")  
          

def modif_repas(session, ancien_repas, nouveau_repas):
    session.query(Manger).filter(Manger.idP == ancien_repas.idP).filter(Manger.idRepas == ancien_repas.idRepas).update(
        {Manger.idRepas : nouveau_repas.idRepas}
    )
    session.commit()
    print("Le repas du participant a bien été modifié")     

def get_info_personne(session, email, mdp):
    personne = session.query(Participant).filter(Participant.emailP == email).filter(Participant.mdpP == mdp).first()
    if personne is None:
        return None
    else:
        return personne

def get_participant(session, id_participant):
    return session.query(Participant).filter(Participant.idP == id_participant).first()

def get_secretaire(session, id_secretaire):
    return session.query(Secretaire).filter(Secretaire.idP == id_secretaire).first()

def get_prenom(session, id_participant):
    return (session.query(Participant).filter(Participant.idP == id_participant).first()).prenomP

def get_nom(session, id_participant):
    return (session.query(Participant).filter(Participant.idP == id_participant).first()).nomP

def get_id_hotel(session, nom_hotel):
    return (session.query(Hotel).filter(Hotel.nomHotel == nom_hotel).first()).idHotel
   

def get_utilisateur(session, id_utilisateur):
    return session.query(Utilisateur).filter(Utilisateur.idP == id_utilisateur).first()

def affiche_participants(session):
    liste_participants = []
    participants = session.query(Participant)
    for part in participants:
        liste_participants.append(part)
    return liste_participants
   

def affiche_participant_trier(session, trie):
     
        if trie == "Auteur" :
            return session.query(Participant).join(Auteur, Participant.idP==Auteur.idP).all()

        elif trie == "Consommateur":
            return session.query(Participant).join(Consommateur, Participant.idP==Consommateur.idP).all() 

        elif trie == "Exposant": 
            return session.query(Participant).join(Exposant, Participant.idP==Exposant.idP).all() 
        
        elif trie == "Intervenant":
            return session.query(Participant).join(Intervenant, Participant.idP==Intervenant.idP).all() 
        
        elif trie == "Invite":
            return session.query(Participant).join(Invite, Participant.idP==Invite.idP).all() 
        
        elif trie == "Presse":
            return session.query(Participant).join(Presse, Participant.idP==Presse.idP).all() 
        
        elif trie == "Staff": 
            return session.query(Participant).join(Staff, Participant.idP==Staff.idP).all()
        
        else: 
            return session.query(Participant).order_by(Participant.idP.asc()).all()

def affiche_participant_trier_consommateur(session):
    participant = session.query(Participant).all()
    return participant


def get_nom_restaurant():
    liste_nom_resteau = []
    for nom in session.query(Restaurant):
        liste_nom_resteau.append((nom.nomRest, nom.idRest))
    return liste_nom_resteau

def get_nom_hotel():
    liste_nom_hotel = []
    for nom in session.query(Hotel):
        liste_nom_hotel.append((nom.nomHotel, nom.idHotel))
    return liste_nom_hotel

    
        
def afficher_consommateur(session, date_jour, restaurant, midi):
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
        repas = session.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau).filter(Repas.idRest == restaurant).filter(Repas.estMidi == midi).all()
    elif restaurant == "Restaurant" and midi == "Journee":
        repas = session.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau)
    elif restaurant != "Restaurant":
        repas = session.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau).filter(Repas.idRest == restaurant).all()
    elif midi != "Journee":
        repas = session.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau).filter(Repas.estMidi == midi).all()
    
    if date_jour[0] != "Date":
        date_jour = date(int(date_jour[0]), int(date_jour[1]), int(date_jour[2]))
        for cren in repas:
            if cren[1].date() == date_jour:
                liste_creneau.append(cren[2])
        repas = session.query(Repas, Repas.idCreneau, Repas.idRepas).all()
        for rep in repas:
            if rep[1] in liste_creneau:
                liste_repas.append(rep[2])
    else:
        for rep in repas:
            liste_repas.append(rep[3])

    manger = session.query(Manger, Manger.idP, Manger.idRepas).all()
    for mangeur in manger:
        if mangeur[2] in liste_repas:
            liste_mangeur.append(mangeur[1])

    consommateurs = session.query(Consommateur, Consommateur.idP).all()

    for consomm in consommateurs:
        if consomm[1] in liste_mangeur:
            liste_consommateurs.append(consomm[1])
    print(liste_consommateurs)
    liste_participants = get_liste_participant_idp_regime(session, liste_consommateurs)
    return liste_participants

def get_liste_participant_idp_regime(session, liste_id):
    liste_participants = []
    participants = session.query(Participant).join(Consommateur, Participant.idP == Consommateur.idP).all()
    for une_personne in participants:
        if une_personne.idP in liste_id:
            liste_participants.append((une_personne, get_regime(session, une_personne.idP)))
    return liste_participants

def affiche_navette(session, date, navette, directionGare):
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
        transport = session.query(Voyage.idVoy, Participant.prenomP, Participant.nomP, Voyage.directionGare, Navette.nomNavette, Voyage.heureDebVoy).join(Mobiliser, Mobiliser.idVoy == Voyage.idVoy).join(Navette, Navette.idNavette == Mobiliser.idNavette).join(Transporter, Voyage.idVoy == Transporter.idVoy).join(Intervenant, Intervenant.idP == Transporter.idP).join(Participant, Participant.idP == Intervenant.idP).filter(Navette.idNavette == navette).filter(Voyage.directionGare == directionGare).distinct().all()
    elif navette == "Navette" and directionGare == "Direction":
        transport = session.query(Voyage.idVoy, Participant.idP, Participant.prenomP, Participant.nomP, Voyage.directionGare, Voyage.heureDebVoy).join(Mobiliser, Mobiliser.idVoy == Voyage.idVoy).join(Navette, Navette.idNavette == Mobiliser.idNavette).join(Transporter, Voyage.idVoy == Transporter.idVoy).join(Intervenant, Intervenant.idP == Transporter.idP).join(Participant, Participant.idP == Intervenant.idP).distinct().all()
    elif navette != "Restaurant":
        transport = session.query(Voyage.idVoy, Participant.prenomP, Participant.nomP, Voyage.directionGare, Navette.nomNavette, Voyage.heureDebVoy).join(Mobiliser, Mobiliser.idVoy == Voyage.idVoy).join(Navette, Navette.idNavette == Mobiliser.idNavette).join(Transporter, Voyage.idVoy == Transporter.idVoy).join(Intervenant, Intervenant.idP == Transporter.idP).join(Participant, Participant.idP == Intervenant.idP).filter(Navette.idNavette == navette).distinct().all()
    elif directionGare != "Direction":
        transport = session.query(Voyage.idVoy, Participant.prenomP, Participant.nomP, Voyage.directionGare, Navette.nomNavette, Voyage.heureDebVoy).join(Mobiliser, Mobiliser.idVoy == Voyage.idVoy).join(Navette, Navette.idNavette == Mobiliser.idNavette).join(Transporter, Voyage.idVoy == Transporter.idVoy).join(Intervenant, Intervenant.idP == Transporter.idP).join(Participant, Participant.idP == Intervenant.idP).filter(Voyage.directionGare == directionGare).distinct().all()
    
    print(transport)
    
    if date[0] != "Date":
        date = date(int(date[0]), int(date[1]), int(date[2])) # modifier ça et modifier le HTML
        for cren in transport:
            if cren[1].date() == date:
                liste_creneau.append(cren[2])
        transport = session.query(Repas, Repas.idCreneau, Repas.idRepas).all()
        for rep in transport:
            if rep[1] in liste_creneau:
                liste_transport.append(rep[2])
    else:
        for tran in transport:
            liste_transport.append(tran[3])

    return liste_transport

# affiche_navette(session, "Date", "Navette", "Direction")
         

def get_liste_participant_id_consommateur(session, liste_id):
    liste_participants = []
    participants = session.query(Participant).join(Consommateur, Participant.idP == Consommateur.idP).all()
    for une_personne in participants:
        if une_personne.idP in liste_id:
            liste_participants.append(une_personne)
    return liste_participants

def get_regime(session, id_p):
    str_regime = ""
    liste_regime = session.query(Regime.nomRegime).join(Avoir, Avoir.idRegime == Regime.idRegime).filter(Avoir.idP == id_p).all()
    if len(liste_regime) == 0:
        str_regime = "Pas de regime"
    else:
        for un_regime in liste_regime:
            str_regime += str(un_regime[0]) + ", "
        str_regime = str_regime[:-2]
    return str_regime

def get_dormeur(session, date_jour, hotel):
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
    dormeurs = session.query(Loger.idP, Loger.dateDebut, Loger.dateFin, Loger.idHotel).all()
    for un_dormeur in dormeurs:
        date_deb = un_dormeur[1].date()
        date_fin = un_dormeur[2].date()
        if date_jour == "Date" :
            if hotel is None or un_dormeur.idHotel == hotel:
                liste_dormeur_date_hotel.append(un_dormeur[0])

        elif date_deb <= date_jour and date_fin >= date_jour and hotel is None or un_dormeur.idHotel == hotel : 
            liste_dormeur_date_hotel.append(un_dormeur[0])
                
    liste_participants = get_liste_participant_id_consommateur(session, liste_dormeur_date_hotel)

    return liste_participants
#print(get_dormeur(session, "2022-11-19", 2))

def ajoute_deplacer(session, idP, idTransport, lieuDepart, lieuArrive) : 
    deplacement = Deplacer(idP, idTransport, lieuDepart, lieuArrive)
    deplacer = session.query(Deplacer).filter(Deplacer.idP == idP).filter(Deplacer.idTransport == idTransport).filter(Deplacer.lieuDepart == lieuDepart).filter(Deplacer.lieuArrive == lieuArrive).first()
    if deplacer is None:
        session.add(deplacement)
        try: 
            session.commit()
            print("Le deplacement à bien été inséré")
        except:
            print("Erreur !")
            session.rollback()
 
    else:
        print("Un même déplacement existe déjà pour cette personne")
  
#ajoute_deplacer(session, 300, 1, "Paris", "Blois")

def ajoute_mangeur(session, idP, idRepas):
    mangeur = Manger(idP, idRepas)
    manger = session.query(Manger).filter(Manger.idP == idP).filter(Manger.idRepas == idRepas).first()
    if manger is None:
        session.add(mangeur)
        try: 
            session.commit()
            print("Le consommateur à bien été associé à un repas")  

        except: 
            print("Erreur !")
            session.rollback()
    else: 
        print("Un consommateur mange déjà ce repas")


def ajoute_loger(session, idP, dateDebut, dateFin, idHotel):
    logeur = Loger(idP, dateDebut, dateFin, idHotel)
    loger = session.query(Loger.dateDebut, Loger.dateFin).filter(Loger.idP == idP).all()
    
    for log in loger: 
        date_deb = log[0].date()
        date_fin = log[1].date()
        dateDeb = dateDebut.date()
        dateFin = dateFin.date()
        print(dateFin)
        if (dateDeb <= date_deb <= dateFin) or (date_deb <= dateDeb <= date_fin):
            print("Cette intervenant est déjà logé dans un hôtel à ces dates")
            return
    session.add(logeur)
    try:
        session.commit()
        print("Le loger à bien été associé à un hôtel")  

    except: 
        print("Erreur !")
        session.rollback()
        
def get_max_id_regime(session): 
    regime= session.query(func.max(Regime.idRegime)).first()
    if (regime[0]) is None:
        return 0
    else:
        return regime._data[0]
        
def ajoute_regime(session, regime) : 
    id_regime = get_max_id_regime(session)+1
    regime = Regime(id_regime, regime)
    session.add(regime)
    try :
        session.commit()
        return id_regime
    except : 
        print("erreur")
        session.rollback() 
        
def ajoute_avoir_regime(session, id_consommateur, id_regime) :
    avoir_regime = Avoir(id_consommateur, id_regime)
    session.add(avoir_regime)
    try :
        session.commit()
        print("L'association regime-consommateur à bien été ajoutée !")
    except : 
        print("erreur")
        session.rollback() 
    
def est_intervenant(session, idP):
    intervenant = session.query(Intervenant).filter(Intervenant.idP == idP).first()
    return intervenant is not None
            
def est_secretaire(session, idP):
    secretaire = session.query(Secretaire).filter(Secretaire.idP == idP).first()
    return secretaire is not None

        
# ajoute_loger(session, 400, datetime.datetime(2022, 11, 19), datetime.datetime(2022, 11, 19), 1)
        
        
def requete_transport_annee(session, idP, annee) : 
    liste_transport = session.query(Deplacer, Assister.dateDepart).join(Assister, Deplacer.idP == Assister.idP).filter(Deplacer.idP == idP).all()
    liste_deplacement = list()
    annee = annee.year
    for transport in liste_transport: 
        annee_req = transport[1].year
        if annee_req == annee: 
            liste_deplacement.append(transport)
    return liste_deplacement       


def ajoute_assister(session, idP, dateArrive, dateDepart):
    assisteur = Assister(idP, dateArrive, dateDepart)
    assister = session.query(Assister).filter(Assister.dateArrive == dateArrive).filter(Assister.dateDepart == dateDepart).first()
    if assister is None :
        session.add(assisteur)
        try : 
            session.commit()
            print("L'intervenant à bien été ajouté à ces dates") 
        except : 
            print("Erreur !")
            session.rollback()
            
    else :
        print("Cet intervenant assiste déjà au festival à ces dates")
        
def cherche_transport(session, nom_transport) : 
    liste_transport = session.query(Transport.idTransport, Transport.nomTransport).all()
    res = list()
    for transport in liste_transport : 
        if nom_transport in transport : 
            res.append(transport)
    return res


def modif_participant_remarque(session, idP, remarques) : 
    participant = session.query(Participant.idP, Participant.prenomP, Participant.nomP, Participant.ddnP, Participant.telP,\
    Participant.emailP, Participant.adresseP, Participant.mdpP, Participant.invite, Participant.emailEnvoye,\
    Participant.remarques).filter(Participant.idP == idP).first()
    
    modifier_participant_tout(session, participant[0], participant[1], participant[2], participant[3], participant[4], participant[5],\
    participant[6], participant[7], participant[8], participant[9], participant[10]+ " | "+ str(remarques))
    


def get_utilisateur_email_mdp(session, mail, mdp):
    utilisateur = session.query(Utilisateur).filter(Utilisateur.emailP == mail).filter(Utilisateur.mdpP == mdp).first()
    if utilisateur is not None :
        return utilisateur


@login_manager.user_loader
def load_user(participant_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    if est_secretaire(session, participant_id):
        return get_secretaire(session, participant_id)
    else:
        return get_participant(session, participant_id)
# print(requete_transport_annee(session, 301,datetime.datetime(2022, 11, 18)))
        
# ajoute_loger(session, 300, datetime.datetime(2022,11,16, 10,30), datetime.datetime(2022, 11, 21, 13,00), 1)


#print(get_liste_participant_id_consommateur(session, [100, 101, 200]))

#ajoute_particpant(session, None, "prenom", "nom", "2003-08-18", "0607080911", "maxym.charpentier@gmail.com", "Adresse", "MDP", "aucune", False, False)

#print(get_info_personne(session, "lenny@gmail.com", "le"))

#modifier_participant_role(session, get_participant(session, 14), "Exposant")
    
#modifier_participant(session, 7, "test", "test", "2005-08-18", "0700000000", "a.a@gmail.com", "b", "jsp", invite=True, emailEnvoye=True)


#print(afficher_consommateur(session, datetime.datetime(2022,11,18,11,30).date(), "Erat Eget Tincidunt Incorporated", True))


# [(2, 'Plato', 'Lewis', False, 'Navette 2', datetime.datetime(2022, 11, 19, 10, 30)),
#  (2, 'Finn', 'Rowland', False, 'Navette 2', datetime.datetime(2022, 11, 19, 10, 30)),
#  (2, 'Dahlia', 'Barton', False, 'Navette 2', datetime.datetime(2022, 11, 19, 10, 30)),
#  (2, 'Plato', 'Lewis', False, 'Navette 1', datetime.datetime(2022, 11, 19, 10, 30)), 
#  (2, 'Finn', 'Rowland', False, 'Navette 1', datetime.datetime(2022, 11, 19, 10, 30)),
#  (2, 'Dahlia', 'Barton', False, 'Navette 1', datetime.datetime(2022, 11, 19, 10, 30))]
