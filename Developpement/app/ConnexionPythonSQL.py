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
from Exposant import Exposant
from Consommateur import Consommateur
from Staff import Staff
from Intervenant import Intervenant
from Auteur import Auteur
from Presse import Presse
from Invite import Invite
from Participant import Participant
from Loger import Loger
from Hotel import Hotel
from Manger import Manger
from Repas import Repas
from Creneau import Creneau
from Restaurant import Restaurant

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
        
def ajoute_intervenant(session, intervenant):
    intervenantI = session.query(Intervenant).filter(Intervenant.idP == intervenant.idP).first()
    if intervenantI is None:
        personne = session.query(Participant).filter(Participant.idP == intervenant.idP).first()
        new_intervenant = Intervenant(intervenant.idP, None, None)
        session.add(new_intervenant)
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

     
def modifier_participant(session, participant):
    session.query(Participant).filter(Participant.idP == participant.idP).update(
        {Participant.prenomP : participant.prenomP, Participant.nomP : participant.nomP, Participant.ddnP : participant.ddnP, 
         Participant.telP : participant.telP, Participant.emailP : participant.emailP, Participant.mdpP : participant.mdpP,
         Participant.invite : participant.invite, Participant.emailEnvoye : participant.emailEnvoye, Participant.remarques : participant.remarques})
    session.commit()
    print("Le participant a bien été modifié")        

def modifier_participant_role(session, participant, metier):
    ancien_participant = Participant(participant.idP, participant.prenomP, participant.nomP, participant.ddnP, participant.telP, participant.emailP, participant.mdpP, participant.remarques, participant.invite, participant.emailEnvoye)
    supprimer_participant_role(session, participant.idP)
    ajoute_participant_role_id(session, ancien_participant, metier)
    print("Le role du participant a bien été modifié")

def modif_loger(session, ancien_loger, nouveau_loger):
    session.query(Loger).filter(Loger.idP == ancien_loger.idP).filter(Loger.idHotel == ancien_loger.idHotel).filter(Loger.dateDebut == ancien_loger.dateDebut).update({
        Loger.idHotel : nouveau_loger.idHotel, Loger.dateDebut : nouveau_loger.dateDebut, Loger.dateFin : nouveau_loger.dateFin})
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

def get_id_hotel(session, nom_hotel):
    return (session.query(Hotel).filter(Hotel.nomHotel == nom_hotel).first()).idHotel
   
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
            return session.query(Participant).join(Exposant, Participant.idP==Intervenant.idP).all() 
        
        elif trie == "Invite":
            return session.query(Participant).join(Exposant, Participant.idP==Invite.idP).all() 
        
        elif trie == "Presse":
            return session.query(Participant).join(Presse, Participant.idP==Presse.idP).all() 
        
        elif trie == "Staff": 
            return session.query(Participant).join(Staff, Participant.idP==Staff.idP).all()
        
        else: 
            return session.query(Participant).order_by(Participant.nomP.asc()).all()

    
def affiche_participant_trier_consommateur(session):
    participant = session.query(Participant).all()
    return participant


def get_nom_restaurant():
    liste_nom_resteau = []
    for nom in session.query(Restaurant):
        liste_nom_resteau.append(nom.nomRest)
    return liste_nom_resteau

def get_nom_hotel():
    liste_nom_hotel = []
    for nom in session.query(Hotel):
        liste_nom_hotel.append((nom.nomHotel, nom.idHotel))
    return liste_nom_hotel



def afficher_consommateur(session, date, restaurant, midi):
    liste_consommateurs = []
    liste_creneau = []
    liste_repas = []
    liste_mangeur = []
    if restaurant != "Restaurant" and midi != "Journee":
        repas = session.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau).filter(Restaurant.nomRest == restaurant).filter(Repas.estMidi == midi).all()
    elif restaurant == "Restaurant" and midi == "Journee":
        repas = session.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau)
    elif restaurant != "Restaurant":
        repas = session.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau).filter(Restaurant.nomRest == restaurant).all()
    elif midi != "Journee":
        repas = session.query(Creneau, Creneau.dateDebut, Creneau.idCreneau, Repas.idRepas).join(Repas, Repas.idCreneau == Creneau.idCreneau).filter(Repas.estMidi == midi).all()
    
    if date != "Date":
        for cren in repas:
            if cren[1].date() == date:
                liste_creneau.append(cren[2])
        repas = session.query(Repas, Repas.idCreneau, Repas.idRepas).all()
        for rep in repas:
            if rep[1] in liste_creneau:
                liste_repas.append(rep[2])
    else:
        for rep in repas:
            liste_repas.append(rep[3])

    manger = session.query(Manger, Manger.idRepas, Manger.idP).all()
    for mangeur in manger:
        if mangeur[1] in liste_repas:
            liste_mangeur.append(mangeur[2])

    consommateurs = session.query(Consommateur, Consommateur.idP).all()

    for consomm in consommateurs:
        if consomm[1] in liste_mangeur:
            liste_consommateurs.append(consomm[1])
    liste_participants = get_liste_participant_id_consommateur(session, liste_consommateurs)
    return liste_participants

def get_liste_participant_id_consommateur(session, liste_id):
    liste_participants = []
    participants = session.query(Participant).join(Consommateur, Participant.idP == Consommateur.idP).all()
    for une_personne in participants:
        if une_personne.idP in liste_id:
            liste_participants.append(une_personne)
    return liste_participants

#print(affiche_participant_date(session, datetime.datetime(2022,11,18,11,30).date(), "Erat Eget Tincidunt Incorporated", True))
#print(affiche_participant_date_dateFalse(session,"Donec Est Mauris LLP", True))
#print(affiche_participant_date_resaurantFalse(session, datetime.datetime(2022,11,19,12,30).date(), True))
#print(affiche_participant_date_dateOnly(session, datetime.datetime(2022,11,19,12,30).date()))
#print(affiche_participant_date_restaurantOnly(session, "Erat Eget Tincidunt Incorporated"))
#print(affiche_participant_date_journeeOnly(session, False))

#print(get_liste_participant_id_consommateur(session, [100, 101, 200]))

#ajoute_particpant(session, None, "prenom", "nom", "2003-08-18", "0607080911", "maxym.charpentier@gmail.com", "Adresse", "MDP", "aucune", False, False)
# ajoute_Consommateur(session, Consommateur(1))
# ajoute_exposant(session, Exposant(1, 1))
# ajoute_staff(session, Staff(1))
# ajoute_intervenant(session, Intervenant(1, "2020-03-03 12:00:00", "2020-03-03 13:00:00", "voiture", "aucune"))
# ajoute_auteur(session, Auteur(1, 1))
# ajoute_presse(session, Presse(1))
# ajoute_invite(session, Invite(1))
#ajoute_participant_role(session, Participant(None, "Mathieu", "Alpha", "2003-08-18", "0606060666", "maxym.charpentier@gmail.com", "A", "aucune", emailEnvoye = True), "Auteur")

#print(get_info_personne(session, "lenny@gmail.com", "le"))

#print(datetime.datetime.now().date())

#print(get_participant(session, 14))

#print(datetime.datetime(2022,11,18))

# ajoute_participant_role_id(session, Participant(14, "Mathieu", "Alpha", "2003-08-18", "0606060666", "maxym.charpentier@gmail.com", "A", "aucune", emailEnvoye = True), "Auteur")
# modifier_participant_role(session, get_participant(session, 14), "Exposant")
    
    
#ajoute_participant_role(session, Participant(None, "TEST PRENOM", "TEST NOM", "2003-08-18", "0606060666", "maxym.charpentier@gmail.com", "A", "aucune"), "Staff")
# supprimer_participant_role(session, 8)
#modifier_participant(session, Participant(7, "test", "test", "2005-08-18", "0700000000", "a.a@gmail.com", "b", "jsp", invite=True, emailEnvoye=True))
#get_nom_restaurant()


def get_dormeur(session, date, hotel):
    liste_dormeur_date_hotel = []
    dormeurs = session.query(Loger.idP, Loger.idHotel, Loger.dateDebut, Loger.dateFin).all()
    for un_dormeur in dormeurs:
        date_deb = str(str(un_dormeur[2])[:10])
        date_fin = str(str(un_dormeur[3])[:10])
        if date == "Date" or (date_deb <= date and date_fin >= date) and (hotel is None or un_dormeur.idHotel == hotel):
            liste_dormeur_date_hotel.append(un_dormeur[0])

    liste_participants = get_liste_participant_id_consommateur(session, liste_dormeur_date_hotel)

    return liste_participants

#print(get_dormeur(session, "2022-11-19", 1))




#print(afficher_consommateur(session, datetime.datetime(2022,11,18,11,30).date(), "Erat Eget Tincidunt Incorporated", True))
#print(afficher_consommateur(session, "Date", "Donec Est Mauris LLP", True))
